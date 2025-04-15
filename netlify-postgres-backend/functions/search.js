const { query } = require('./utils/db');

exports.handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS'
  };

  // Handle preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    if (event.httpMethod === 'GET') {
      // Extract search query from query parameters
      const params = new URLSearchParams(event.queryStringParameters || {});
      const searchTerm = params.get('q');
      
      if (!searchTerm) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ message: 'Search term is required' })
        };
      }
      
      // Search in experts table (name, description)
      const expertsResult = await query(
        `SELECT id, name, type, title, affiliation, city_id, is_diaspora, image 
         FROM experts 
         WHERE name ILIKE $1 OR description ILIKE $1`,
        [`%${searchTerm}%`]
      );
      
      // Search in expert_tags table
      const tagsResult = await query(
        `SELECT DISTINCT e.id, e.name, e.type, e.title, e.affiliation, e.city_id, e.is_diaspora, e.image 
         FROM experts e
         JOIN expert_tags t ON e.id = t.expert_id
         WHERE t.tag ILIKE $1`,
        [`%${searchTerm}%`]
      );
      
      // Combine results, removing duplicates
      const expertsFromName = expertsResult.rows;
      const expertsFromTags = tagsResult.rows;
      
      // Create a Map to eliminate duplicates
      const expertsMap = new Map();
      
      // Add experts from name/description search
      expertsFromName.forEach(expert => {
        expertsMap.set(expert.id, expert);
      });
      
      // Add experts from tag search (will override duplicates)
      expertsFromTags.forEach(expert => {
        expertsMap.set(expert.id, expert);
      });
      
      // Convert Map back to array
      const allExperts = Array.from(expertsMap.values());
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(allExperts)
      };
    }
    
    // If method not allowed
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ message: 'Method not allowed' })
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
