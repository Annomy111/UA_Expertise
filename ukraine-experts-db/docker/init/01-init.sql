-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE expert_type AS ENUM ('individual', 'organization');
CREATE TYPE focus_area AS ENUM (
    'advocacy', 
    'humanitarian', 
    'cultural_diplomacy', 
    'political_mobilization', 
    'research', 
    'policy_analysis', 
    'community_support', 
    'integration', 
    'education', 
    'media'
);

-- Create cities table
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, country)
);

-- Create experts table (for both individuals and organizations)
CREATE TABLE experts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type expert_type NOT NULL,
    title VARCHAR(255),
    affiliation VARCHAR(255),
    city_id INTEGER REFERENCES cities(id),
    description TEXT,
    founding_year INTEGER,
    is_diaspora BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create table for expert focus areas (many-to-many)
CREATE TABLE expert_focus_areas (
    id SERIAL PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    focus_area focus_area NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(expert_id, focus_area)
);

-- Create contacts table
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    contact_type VARCHAR(50) NOT NULL, -- email, phone, website, social_media
    contact_value TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create links table
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create key_figures table (for organizations)
CREATE TABLE key_figures (
    id SERIAL PRIMARY KEY,
    organization_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create activities table
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    date_start DATE,
    date_end DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create publications table
CREATE TABLE publications (
    id SERIAL PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    publication_date DATE,
    publisher VARCHAR(255),
    url TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create relationships table (for connections between experts)
CREATE TABLE relationships (
    id SERIAL PRIMARY KEY,
    expert_id_1 UUID REFERENCES experts(id) ON DELETE CASCADE,
    expert_id_2 UUID REFERENCES experts(id) ON DELETE CASCADE,
    relationship_type VARCHAR(100) NOT NULL, -- collaboration, affiliation, partnership
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CHECK (expert_id_1 <> expert_id_2)
);

-- Create tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create expert_tags table (many-to-many)
CREATE TABLE expert_tags (
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (expert_id, tag_id)
);

-- Create indexes for performance
CREATE INDEX idx_experts_city_id ON experts(city_id);
CREATE INDEX idx_experts_type ON experts(type);
CREATE INDEX idx_expert_focus_areas_expert_id ON expert_focus_areas(expert_id);
CREATE INDEX idx_contacts_expert_id ON contacts(expert_id);
CREATE INDEX idx_links_expert_id ON links(expert_id);
CREATE INDEX idx_key_figures_organization_id ON key_figures(organization_id);
CREATE INDEX idx_activities_expert_id ON activities(expert_id);
CREATE INDEX idx_publications_expert_id ON publications(expert_id);
CREATE INDEX idx_relationships_expert_id_1 ON relationships(expert_id_1);
CREATE INDEX idx_relationships_expert_id_2 ON relationships(expert_id_2);
CREATE INDEX idx_expert_tags_expert_id ON expert_tags(expert_id);
CREATE INDEX idx_expert_tags_tag_id ON expert_tags(tag_id);

-- Insert initial cities
INSERT INTO cities (name, country, description) VALUES
('Brussels', 'Belgium', 'Capital of Belgium and administrative center of the European Union'),
('Berlin', 'Germany', 'Capital and largest city of Germany'),
('Paris', 'France', 'Capital and most populous city of France'),
('Warsaw', 'Poland', 'Capital and largest city of Poland');

-- Create views for easier querying
CREATE VIEW experts_with_cities AS
SELECT 
    e.*,
    c.name AS city_name,
    c.country
FROM 
    experts e
JOIN 
    cities c ON e.city_id = c.id;

CREATE VIEW organizations_with_key_figures AS
SELECT 
    e.*,
    c.name AS city_name,
    c.country,
    json_agg(
        json_build_object(
            'id', kf.id,
            'name', kf.name,
            'role', kf.role,
            'description', kf.description
        )
    ) AS key_figures
FROM 
    experts e
JOIN 
    cities c ON e.city_id = c.id
LEFT JOIN 
    key_figures kf ON e.id = kf.organization_id
WHERE 
    e.type = 'organization'
GROUP BY 
    e.id, c.name, c.country;

-- Create function to update timestamps
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at timestamps
CREATE TRIGGER update_experts_modtime
    BEFORE UPDATE ON experts
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_cities_modtime
    BEFORE UPDATE ON cities
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_contacts_modtime
    BEFORE UPDATE ON contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_key_figures_modtime
    BEFORE UPDATE ON key_figures
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_activities_modtime
    BEFORE UPDATE ON activities
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column(); 