-- Ukraine Experts Database Schema

-- Cities Table
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    description TEXT
);

-- Experts Table
CREATE TABLE experts (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('individual', 'organization')),
    title TEXT,
    affiliation TEXT,
    city_id INTEGER REFERENCES cities(id),
    description TEXT,
    founding_year INTEGER,
    is_diaspora BOOLEAN DEFAULT FALSE,
    image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Contacts Table
CREATE TABLE contacts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    value TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE
);

-- Key Figures Table
CREATE TABLE key_figures (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    role TEXT,
    description TEXT
);

-- Expert Focus Areas Table
CREATE TABLE expert_focus_areas (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    focus_area TEXT NOT NULL
);

-- Expert Tags Table
CREATE TABLE expert_tags (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    expert_id UUID REFERENCES experts(id) ON DELETE CASCADE,
    tag TEXT NOT NULL
);

-- Sample Data: Cities
INSERT INTO cities (name, country, description) VALUES
('Kyiv', 'Ukraine', 'Capital city of Ukraine'),
('Warsaw', 'Poland', 'Capital city of Poland'),
('Berlin', 'Germany', 'Capital city of Germany'),
('Paris', 'France', 'Capital city of France'),
('London', 'UK', 'Capital city of the United Kingdom');

-- Sample Expert (individual)
INSERT INTO experts (id, name, type, title, city_id, is_diaspora) VALUES
('11111111-1111-1111-1111-111111111111', 'Olena Zelenska', 'individual', 'First Lady of Ukraine', 1, false);

-- Sample Expert (organization)
INSERT INTO experts (id, name, type, description, city_id, is_diaspora, founding_year) VALUES
('22222222-2222-2222-2222-222222222222', 'Ukraine Support Network', 'organization', 'NGO supporting Ukraine', 2, true, 2022);

-- Sample Contacts
INSERT INTO contacts (expert_id, type, value, is_primary) VALUES
('11111111-1111-1111-1111-111111111111', 'email', 'olena@example.com', true),
('22222222-2222-2222-2222-222222222222', 'website', 'https://ukrainesupport.example.org', true),
('22222222-2222-2222-2222-222222222222', 'phone', '+48 123 456 789', false);

-- Sample Key Figures
INSERT INTO key_figures (expert_id, name, role) VALUES
('22222222-2222-2222-2222-222222222222', 'Maria Kowalska', 'Executive Director'),
('22222222-2222-2222-2222-222222222222', 'Jan Nowak', 'Program Coordinator');

-- Sample Focus Areas
INSERT INTO expert_focus_areas (expert_id, focus_area) VALUES
('11111111-1111-1111-1111-111111111111', 'humanitarian'),
('11111111-1111-1111-1111-111111111111', 'cultural_diplomacy'),
('22222222-2222-2222-2222-222222222222', 'humanitarian'),
('22222222-2222-2222-2222-222222222222', 'advocacy'),
('22222222-2222-2222-2222-222222222222', 'integration');

-- Sample Tags
INSERT INTO expert_tags (expert_id, tag) VALUES
('11111111-1111-1111-1111-111111111111', 'diplomacy'),
('11111111-1111-1111-1111-111111111111', 'humanitarian aid'),
('22222222-2222-2222-2222-222222222222', 'refugee support'),
('22222222-2222-2222-2222-222222222222', 'humanitarian aid'),
('22222222-2222-2222-2222-222222222222', 'diaspora');
