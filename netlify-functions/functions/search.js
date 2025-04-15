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
      const { data: expertsData, error: expertsError } = await supabase
        .from('experts')
        .select('id, name, type, title, affiliation, city_id, is_diaspora, image')
        .or(`name.ilike.%${searchTerm}%,description.ilike.%${searchTerm}%`);
        
      if (expertsError) throw expertsError;
      
      // Search in expert_tags table
      const { data: tagMatches, error: tagsError } = await supabase
        .from('expert_tags')
        .select('expert_id')
        .ilike('tag', `%${searchTerm}%`);
        
      if (tagsError) throw tagsError;
      
      // Get the experts matching the tags
      let tagMatchedExperts = [];
      if (tagMatches && tagMatches.length > 0) {
        const expertIds = [...new Set(tagMatches.map(match => match.expert_id))];
        
        const { data: taggedExperts, error: taggedExpertsError } = await supabase
          .from('experts')
          .select('id, name, type, title, affiliation, city_id, is_diaspora, image')
          .in('id', expertIds);
          
        if (taggedExpertsError) throw taggedExpertsError;
        tagMatchedExperts = taggedExperts;
      }
      
      // Combine results, removing duplicates
      const allExperts = [...expertsData];
      tagMatchedExperts.forEach(expert => {
        if (!allExperts.some(e => e.id === expert.id)) {
          allExperts.push(expert);
        }
      });
      
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
