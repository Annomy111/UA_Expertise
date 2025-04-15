const supabase = require('./utils/supabase');

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
      const { data: expertTypes, error: typesError } = await supabase
        .from('experts')
        .select('type, count')
        .group('type');
        
      if (typesError) throw typesError;
      
      // Get count of experts by country
      const { data: expertsByCountry, error: countryError } = await supabase
        .from('experts')
        .select('cities(country), count')
        .group('cities(country)');
        
      if (countryError) throw countryError;
      
      // Get count of experts by city
      const { data: expertsByCity, error: cityError } = await supabase
        .from('experts')
        .select('city_id, cities(name, country), count')
        .group('city_id, cities(name, country)')
        .order('count', { ascending: false });
        
      if (cityError) throw cityError;
      
      // Get count of experts by focus area
      const { data: expertsByFocusArea, error: focusError } = await supabase
        .from('expert_focus_areas')
        .select('focus_area, count')
        .group('focus_area')
        .order('count', { ascending: false });
        
      if (focusError) throw focusError;
      
      // Format the statistics
      const statistics = {
        total_experts: expertTypes.reduce((sum, item) => sum + item.count, 0),
        experts_by_type: Object.fromEntries(
          expertTypes.map(item => [item.type, item.count])
        ),
        experts_by_country: Object.fromEntries(
          expertsByCountry.map(item => [item.cities.country, item.count])
        ),
        top_cities: expertsByCity.map(item => ({
          city: item.cities.name,
          country: item.cities.country,
          count: item.count
        })),
        top_focus_areas: expertsByFocusArea.map(item => ({
          focus_area: item.focus_area,
          count: item.count
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
