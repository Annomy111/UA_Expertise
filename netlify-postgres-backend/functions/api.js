// Main API entry point
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

  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      message: "Welcome to the Ukraine Experts Database API",
      version: "1.0.0",
      endpoints: [
        "/api/experts - Get all experts",
        "/api/experts/{id} - Get expert details, update or delete an expert",
        "/api/cities - Get all cities",
        "/api/search?q={term} - Search for experts",
        "/api/statistics - Get database statistics"
      ]
    })
  };
};
