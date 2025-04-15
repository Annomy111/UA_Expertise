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
      // Get count of experts by type
      const expertTypesResult = await query(
        'SELECT type, COUNT(*) as count FROM experts GROUP BY type'
      );
      
      // Get count of experts by country
      const expertsByCountryResult = await query(
        'SELECT c.country, COUNT(*) as count FROM experts e JOIN cities c ON e.city_id = c.id GROUP BY c.country'
      );
      
      // Get count of experts by city
      const expertsByCityResult = await query(
        'SELECT e.city_id, c.name, c.country, COUNT(*) as count FROM experts e JOIN cities c ON e.city_id = c.id GROUP BY e.city_id, c.name, c.country ORDER BY count DESC'
      );
      
      // Get count of experts by focus area
      const expertsByFocusAreaResult = await query(
        'SELECT focus_area, COUNT(*) as count FROM expert_focus_areas GROUP BY focus_area ORDER BY count DESC'
      );
      
      // Get total count of experts
      const totalExpertsResult = await query('SELECT COUNT(*) as count FROM experts');
      
      // Format the statistics
      const statistics = {
        total_experts: parseInt(totalExpertsResult.rows[0].count),
        experts_by_type: Object.fromEntries(
          expertTypesResult.rows.map(item => [item.type, parseInt(item.count)])
        ),
        experts_by_country: Object.fromEntries(
          expertsByCountryResult.rows.map(item => [item.country, parseInt(item.count)])
        ),
        top_cities: expertsByCityResult.rows.map(item => ({
          city: item.name,
          country: item.country,
          count: parseInt(item.count)
        })),
        top_focus_areas: expertsByFocusAreaResult.rows.map(item => ({
          focus_area: item.focus_area,
          count: parseInt(item.count)
        }))
      };
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(statistics)
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
