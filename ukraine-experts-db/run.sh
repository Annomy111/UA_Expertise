#!/bin/bash

# Navigate to the docker directory
cd docker

# Start the services
docker-compose up -d

# Wait for services to start
echo "Starting services..."
sleep 5

# Check if services are running
echo "Checking services..."
docker-compose ps

# Print access information
echo ""
echo "Services are now running!"
echo "Access the API at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "pgAdmin: http://localhost:5050 (login with admin@example.com / password)"
echo ""
echo "To stop the services, run: docker-compose down" 