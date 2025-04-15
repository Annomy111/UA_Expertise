const { query, transaction } = require('./utils/db');
const { v4: uuidv4 } = require('uuid');

exports.handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
  };

  // Handle preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  const path = event.path.replace('/.netlify/functions/experts', '').replace('/api/experts', '');
  const pathSegments = path.split('/').filter(segment => segment);
  const method = event.httpMethod;

  try {
    // GET /experts - List all experts
    if (method === 'GET' && pathSegments.length === 0) {
      const result = await query(
        'SELECT id, name, type, title, affiliation, description, city_id, is_diaspora, image FROM experts'
      );
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(result.rows)
      };
    }
    
    // GET /experts/{id} - Get expert details
    if (method === 'GET' && pathSegments.length === 1) {
      const expertId = pathSegments[0];
      
      // Get expert basic info
      const expertResult = await query(
        'SELECT * FROM experts WHERE id = $1',
        [expertId]
      );
      
      if (expertResult.rows.length === 0) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ message: 'Expert not found' })
        };
      }
      
      const expert = expertResult.rows[0];
      
      // Get expert contacts
      const contactsResult = await query(
        'SELECT * FROM contacts WHERE expert_id = $1',
        [expertId]
      );
      
      // Get expert key figures
      const keyFiguresResult = await query(
        'SELECT * FROM key_figures WHERE expert_id = $1',
        [expertId]
      );
      
      // Get expert focus areas
      const focusAreasResult = await query(
        'SELECT focus_area FROM expert_focus_areas WHERE expert_id = $1',
        [expertId]
      );
      
      // Get expert tags
      const tagsResult = await query(
        'SELECT tag FROM expert_tags WHERE expert_id = $1',
        [expertId]
      );
      
      // Combine all data
      const expertDetails = {
        ...expert,
        contacts: contactsResult.rows,
        key_figures: keyFiguresResult.rows,
        focus_areas: focusAreasResult.rows.map(fa => fa.focus_area),
        tags: tagsResult.rows.map(t => t.tag)
      };
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(expertDetails)
      };
    }
    
    // POST /experts - Create a new expert
    if (method === 'POST' && pathSegments.length === 0) {
      const expertData = JSON.parse(event.body);
      const expertId = uuidv4();
      
      // Extract related data from the expert object
      const { 
        contacts = [], 
        key_figures = [], 
        focus_areas = [], 
        tags = [], 
        ...expertBasicData 
      } = expertData;
      
      // Use transaction to ensure data consistency
      await transaction(async (client) => {
        // Insert basic expert data
        const columns = Object.keys(expertBasicData).join(', ');
        const placeholders = Object.keys(expertBasicData).map((_, i) => `$${i + 1}`).join(', ');
        const values = Object.values(expertBasicData);
        
        await client.query(
          `INSERT INTO experts (id, ${columns}) VALUES ($1, ${placeholders})`,
          [expertId, ...values]
        );
        
        // Insert contacts
        if (contacts.length > 0) {
          for (const contact of contacts) {
            await client.query(
              'INSERT INTO contacts (expert_id, type, value, is_primary) VALUES ($1, $2, $3, $4)',
              [expertId, contact.type, contact.value, contact.is_primary || false]
            );
          }
        }
        
        // Insert key figures
        if (key_figures.length > 0) {
          for (const figure of key_figures) {
            await client.query(
              'INSERT INTO key_figures (expert_id, name, role, description) VALUES ($1, $2, $3, $4)',
              [expertId, figure.name, figure.role, figure.description]
            );
          }
        }
        
        // Insert focus areas
        if (focus_areas.length > 0) {
          for (const area of focus_areas) {
            await client.query(
              'INSERT INTO expert_focus_areas (expert_id, focus_area) VALUES ($1, $2)',
              [expertId, area]
            );
          }
        }
        
        // Insert tags
        if (tags.length > 0) {
          for (const tag of tags) {
            await client.query(
              'INSERT INTO expert_tags (expert_id, tag) VALUES ($1, $2)',
              [expertId, tag]
            );
          }
        }
      });
      
      return {
        statusCode: 201,
        headers,
        body: JSON.stringify({ id: expertId, message: 'Expert created successfully' })
      };
    }
    
    // PUT /experts/{id} - Update an expert
    if (method === 'PUT' && pathSegments.length === 1) {
      const expertId = pathSegments[0];
      const updateData = JSON.parse(event.body);
      
      // Check if expert exists
      const expertResult = await query(
        'SELECT id FROM experts WHERE id = $1',
        [expertId]
      );
      
      if (expertResult.rows.length === 0) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ message: 'Expert not found' })
        };
      }
      
      // Extract related data from the update object
      const { 
        contacts,
        key_figures,
        focus_areas,
        tags,
        ...expertBasicData 
      } = updateData;
      
      // Use transaction to ensure data consistency
      await transaction(async (client) => {
        // Update basic expert data if provided
        if (Object.keys(expertBasicData).length > 0) {
          const setClause = Object.keys(expertBasicData)
            .map((key, i) => `${key} = $${i + 2}`)
            .join(', ');
            
          const values = Object.values(expertBasicData);
          
          await client.query(
            `UPDATE experts SET ${setClause} WHERE id = $1`,
            [expertId, ...values]
          );
        }
        
        // Update contacts if provided
        if (contacts) {
          // Delete existing contacts
          await client.query(
            'DELETE FROM contacts WHERE expert_id = $1',
            [expertId]
          );
          
          // Insert new contacts
          if (contacts.length > 0) {
            for (const contact of contacts) {
              await client.query(
                'INSERT INTO contacts (expert_id, type, value, is_primary) VALUES ($1, $2, $3, $4)',
                [expertId, contact.type, contact.value, contact.is_primary || false]
              );
            }
          }
        }
        
        // Update key figures if provided
        if (key_figures) {
          // Delete existing key figures
          await client.query(
            'DELETE FROM key_figures WHERE expert_id = $1',
            [expertId]
          );
          
          // Insert new key figures
          if (key_figures.length > 0) {
            for (const figure of key_figures) {
              await client.query(
                'INSERT INTO key_figures (expert_id, name, role, description) VALUES ($1, $2, $3, $4)',
                [expertId, figure.name, figure.role, figure.description]
              );
            }
          }
        }
        
        // Update focus areas if provided
        if (focus_areas) {
          // Delete existing focus areas
          await client.query(
            'DELETE FROM expert_focus_areas WHERE expert_id = $1',
            [expertId]
          );
          
          // Insert new focus areas
          if (focus_areas.length > 0) {
            for (const area of focus_areas) {
              await client.query(
                'INSERT INTO expert_focus_areas (expert_id, focus_area) VALUES ($1, $2)',
                [expertId, area]
              );
            }
          }
        }
        
        // Update tags if provided
        if (tags) {
          // Delete existing tags
          await client.query(
            'DELETE FROM expert_tags WHERE expert_id = $1',
            [expertId]
          );
          
          // Insert new tags
          if (tags.length > 0) {
            for (const tag of tags) {
              await client.query(
                'INSERT INTO expert_tags (expert_id, tag) VALUES ($1, $2)',
                [expertId, tag]
              );
            }
          }
        }
      });
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ message: 'Expert updated successfully' })
      };
    }
    
    // DELETE /experts/{id} - Delete an expert
    if (method === 'DELETE' && pathSegments.length === 1) {
      const expertId = pathSegments[0];
      
      // Check if expert exists
      const expertResult = await query(
        'SELECT id FROM experts WHERE id = $1',
        [expertId]
      );
      
      if (expertResult.rows.length === 0) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ message: 'Expert not found' })
        };
      }
      
      // Use transaction to delete expert and related data
      await transaction(async (client) => {
        // Delete related data first (foreign key constraints)
        await client.query('DELETE FROM contacts WHERE expert_id = $1', [expertId]);
        await client.query('DELETE FROM key_figures WHERE expert_id = $1', [expertId]);
        await client.query('DELETE FROM expert_focus_areas WHERE expert_id = $1', [expertId]);
        await client.query('DELETE FROM expert_tags WHERE expert_id = $1', [expertId]);
        
        // Delete expert
        await client.query('DELETE FROM experts WHERE id = $1', [expertId]);
      });
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ message: 'Expert deleted successfully' })
      };
    }
    
    // If no route matches
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ message: 'Not found' })
    };
    
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ message: 'Internal server error', error: error.message })
    };
  }
};
