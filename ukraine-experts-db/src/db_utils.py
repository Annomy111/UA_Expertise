import psycopg2
import psycopg2.extras
from typing import Dict, List, Any, Optional, Tuple
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "ukraine_experts"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "port": int(os.getenv("DB_PORT", "5433"))
}

def get_connection():
    """Establish a connection to the database."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def execute_query(query: str, params: tuple = None, fetch: bool = True) -> List[Dict]:
    """Execute a query and return results as a list of dictionaries."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                results = cur.fetchall()
                return [dict(row) for row in results]
            else:
                conn.commit()
                return []
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error executing query: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_cities() -> List[Dict]:
    """Get all cities from the database."""
    query = "SELECT * FROM cities ORDER BY name"
    return execute_query(query)

def get_experts_by_city(city_id: int) -> List[Dict]:
    """Get all experts for a specific city."""
    query = """
    SELECT e.*, c.name as city_name, c.country
    FROM experts e
    JOIN cities c ON e.city_id = c.id
    WHERE e.city_id = %s
    ORDER BY e.name
    """
    return execute_query(query, (city_id,))

def get_organizations_with_key_figures(city_id: Optional[int] = None) -> List[Dict]:
    """Get organizations with their key figures."""
    query = """
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
    """
    
    if city_id:
        query += " AND e.city_id = %s"
        params = (city_id,)
    else:
        params = None
        
    query += """
    GROUP BY 
        e.id, c.name, c.country
    ORDER BY 
        e.name
    """
    
    return execute_query(query, params)

def get_expert_details(expert_id: str) -> Dict:
    """Get detailed information about an expert or organization."""
    expert_query = """
    SELECT 
        e.id, e.name, e.title, e.affiliation, e.city_id, e.description, 
        e.founding_year, e.is_diaspora, e.type, e.created_at, e.updated_at,
        e.image,
        c.name as city_name, c.country
    FROM experts e
    JOIN cities c ON e.city_id = c.id
    WHERE e.id = %s
    """
    expert_info = execute_query(expert_query, (expert_id,))
    
    if not expert_info:
        return {}
    
    expert = expert_info[0]
    
    # Get focus areas
    focus_areas_query = """
    SELECT focus_area
    FROM expert_focus_areas
    WHERE expert_id = %s
    """
    focus_areas = execute_query(focus_areas_query, (expert_id,))
    expert['focus_areas'] = [area['focus_area'] for area in focus_areas]
    
    # Get contacts
    contacts_query = """
    SELECT *
    FROM contacts
    WHERE expert_id = %s
    """
    expert['contacts'] = execute_query(contacts_query, (expert_id,))
    
    # Get links
    links_query = """
    SELECT *
    FROM links
    WHERE expert_id = %s
    """
    expert['links'] = execute_query(links_query, (expert_id,))
    
    # Get tags
    tags_query = """
    SELECT t.name
    FROM expert_tags et
    JOIN tags t ON et.tag_id = t.id
    WHERE et.expert_id = %s
    """
    tags = execute_query(tags_query, (expert_id,))
    expert['tags'] = [tag['name'] for tag in tags]
    
    # Get activities
    activities_query = """
    SELECT *
    FROM activities
    WHERE expert_id = %s
    ORDER BY date_start DESC
    """
    expert['activities'] = execute_query(activities_query, (expert_id,))
    
    # If organization, get key figures
    if expert['type'] == 'organization':
        key_figures_query = """
        SELECT *
        FROM key_figures
        WHERE organization_id = %s
        """
        expert['key_figures'] = execute_query(key_figures_query, (expert_id,))
    
    # If individual, get publications
    if expert['type'] == 'individual':
        publications_query = """
        SELECT *
        FROM publications
        WHERE expert_id = %s
        ORDER BY publication_date DESC
        """
        expert['publications'] = execute_query(publications_query, (expert_id,))
    
    return expert

def search_experts(search_term: str) -> List[Dict]:
    """Search for experts by name, description, or tags."""
    query = """
    SELECT DISTINCT e.*, c.name as city_name, c.country
    FROM experts e
    JOIN cities c ON e.city_id = c.id
    LEFT JOIN expert_tags et ON e.id = et.expert_id
    LEFT JOIN tags t ON et.tag_id = t.id
    WHERE 
        e.name ILIKE %s OR
        e.description ILIKE %s OR
        e.title ILIKE %s OR
        e.affiliation ILIKE %s OR
        t.name ILIKE %s
    ORDER BY e.name
    """
    search_pattern = f"%{search_term}%"
    params = (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)
    return execute_query(query, params)

def get_experts_by_focus_area(focus_area: str) -> List[Dict]:
    """Get experts by focus area."""
    query = """
    SELECT e.*, c.name as city_name, c.country
    FROM experts e
    JOIN cities c ON e.city_id = c.id
    JOIN expert_focus_areas efa ON e.id = efa.expert_id
    WHERE efa.focus_area = %s
    ORDER BY e.name
    """
    return execute_query(query, (focus_area,))

def get_diaspora_organizations() -> List[Dict]:
    """Get all diaspora organizations."""
    query = """
    SELECT e.*, c.name as city_name, c.country
    FROM experts e
    JOIN cities c ON e.city_id = c.id
    WHERE e.type = 'organization' AND e.is_diaspora = TRUE
    ORDER BY c.name, e.name
    """
    return execute_query(query)

def add_expert(expert_data: Dict) -> str:
    """Add a new expert or organization to the database."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Insert expert
            expert_query = """
            INSERT INTO experts (
                name, type, title, affiliation, city_id, 
                description, founding_year, is_diaspora
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id
            """
            
            cur.execute(expert_query, (
                expert_data['name'],
                expert_data['type'],
                expert_data.get('title'),
                expert_data.get('affiliation'),
                expert_data['city_id'],
                expert_data.get('description'),
                expert_data.get('founding_year'),
                expert_data.get('is_diaspora', False)
            ))
            
            expert_id = cur.fetchone()[0]
            
            # Insert focus areas
            if 'focus_areas' in expert_data:
                for focus_area in expert_data['focus_areas']:
                    cur.execute(
                        "INSERT INTO expert_focus_areas (expert_id, focus_area) VALUES (%s, %s)",
                        (expert_id, focus_area)
                    )
            
            # Insert contacts
            if 'contacts' in expert_data:
                for contact in expert_data['contacts']:
                    cur.execute(
                        """
                        INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (expert_id, contact['type'], contact['value'], contact.get('is_primary', False))
                    )
            
            # Insert key figures for organizations
            if expert_data['type'] == 'organization' and 'key_figures' in expert_data:
                for figure in expert_data['key_figures']:
                    cur.execute(
                        """
                        INSERT INTO key_figures (organization_id, name, role, description) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (expert_id, figure['name'], figure.get('role'), figure.get('description'))
                    )
            
            # Insert tags
            if 'tags' in expert_data:
                for tag_name in expert_data['tags']:
                    # Check if tag exists
                    cur.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
                    tag_result = cur.fetchone()
                    
                    if tag_result:
                        tag_id = tag_result[0]
                    else:
                        # Create new tag
                        cur.execute("INSERT INTO tags (name) VALUES (%s) RETURNING id", (tag_name,))
                        tag_id = cur.fetchone()[0]
                    
                    # Link tag to expert
                    cur.execute(
                        "INSERT INTO expert_tags (expert_id, tag_id) VALUES (%s, %s)",
                        (expert_id, tag_id)
                    )
            
            conn.commit()
            return expert_id
            
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error adding expert: {e}")
        raise
    finally:
        if conn:
            conn.close()

def update_expert(expert_id: str, expert_data: Dict) -> bool:
    """Update an existing expert or organization."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Update expert
            expert_query = """
            UPDATE experts SET
                name = %s,
                title = %s,
                affiliation = %s,
                city_id = %s,
                description = %s,
                founding_year = %s,
                is_diaspora = %s,
                image = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            
            cur.execute(expert_query, (
                expert_data['name'],
                expert_data.get('title'),
                expert_data.get('affiliation'),
                expert_data['city_id'],
                expert_data.get('description'),
                expert_data.get('founding_year'),
                expert_data.get('is_diaspora', False),
                expert_data.get('image'),
                expert_id
            ))
            
            # Handle focus areas - delete existing and add new
            if 'focus_areas' in expert_data:
                cur.execute("DELETE FROM expert_focus_areas WHERE expert_id = %s", (expert_id,))
                for focus_area in expert_data['focus_areas']:
                    cur.execute(
                        "INSERT INTO expert_focus_areas (expert_id, focus_area) VALUES (%s, %s)",
                        (expert_id, focus_area)
                    )
            
            # Handle contacts - delete existing and add new
            if 'contacts' in expert_data:
                cur.execute("DELETE FROM contacts WHERE expert_id = %s", (expert_id,))
                for contact in expert_data['contacts']:
                    cur.execute(
                        """
                        INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (expert_id, contact['type'], contact['value'], contact.get('is_primary', False))
                    )
            
            # Handle key figures for organizations
            if 'key_figures' in expert_data:
                cur.execute("DELETE FROM key_figures WHERE organization_id = %s", (expert_id,))
                for figure in expert_data['key_figures']:
                    cur.execute(
                        """
                        INSERT INTO key_figures (organization_id, name, role, description) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (expert_id, figure['name'], figure.get('role'), figure.get('description'))
                    )
            
            # Handle tags
            if 'tags' in expert_data:
                cur.execute("DELETE FROM expert_tags WHERE expert_id = %s", (expert_id,))
                for tag_name in expert_data['tags']:
                    # Check if tag exists
                    cur.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
                    tag_result = cur.fetchone()
                    
                    if tag_result:
                        tag_id = tag_result[0]
                    else:
                        # Create new tag
                        cur.execute("INSERT INTO tags (name) VALUES (%s) RETURNING id", (tag_name,))
                        tag_id = cur.fetchone()[0]
                    
                    # Link tag to expert
                    cur.execute(
                        "INSERT INTO expert_tags (expert_id, tag_id) VALUES (%s, %s)",
                        (expert_id, tag_id)
                    )
            
            conn.commit()
            return True
            
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error updating expert: {e}")
        raise
    finally:
        if conn:
            conn.close()

def delete_expert(expert_id: str) -> bool:
    """Delete an expert or organization."""
    query = "DELETE FROM experts WHERE id = %s"
    try:
        execute_query(query, (expert_id,), fetch=False)
        return True
    except Exception:
        return False

def get_statistics() -> Dict:
    """Get database statistics."""
    stats = {}
    
    # Count experts by type
    type_query = """
    SELECT type, COUNT(*) as count
    FROM experts
    GROUP BY type
    """
    type_counts = execute_query(type_query)
    stats['by_type'] = {item['type']: item['count'] for item in type_counts}
    
    # Count by city
    city_query = """
    SELECT c.name, c.country, COUNT(*) as count
    FROM experts e
    JOIN cities c ON e.city_id = c.id
    GROUP BY c.name, c.country
    ORDER BY count DESC
    """
    stats['by_city'] = execute_query(city_query)
    
    # Count by focus area
    focus_query = """
    SELECT focus_area, COUNT(*) as count
    FROM expert_focus_areas
    GROUP BY focus_area
    ORDER BY count DESC
    """
    stats['by_focus_area'] = execute_query(focus_query)
    
    # Count diaspora vs non-diaspora
    diaspora_query = """
    SELECT is_diaspora, COUNT(*) as count
    FROM experts
    GROUP BY is_diaspora
    """
    diaspora_counts = execute_query(diaspora_query)
    stats['by_diaspora'] = {
        str(item['is_diaspora']): item['count'] for item in diaspora_counts
    }
    
    # Most common tags
    tags_query = """
    SELECT t.name, COUNT(*) as count
    FROM expert_tags et
    JOIN tags t ON et.tag_id = t.id
    GROUP BY t.name
    ORDER BY count DESC
    LIMIT 10
    """
    stats['top_tags'] = execute_query(tags_query)
    
    return stats

if __name__ == "__main__":
    # Example usage
    print("Database Statistics:")
    stats = get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\nDiaspora Organizations:")
    diaspora_orgs = get_diaspora_organizations()
    for org in diaspora_orgs:
        print(f"{org['name']} ({org['city_name']}, {org['country']})") 