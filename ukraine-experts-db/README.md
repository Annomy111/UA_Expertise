# Ukraine Experts Database

A comprehensive database of Ukrainian experts and organizations in Europe, with a focus on diaspora groups in Brussels, Berlin, Paris, and Warsaw.

## Overview

This project provides a PostgreSQL database and REST API for storing and accessing information about Ukrainian experts, organizations, and diaspora groups across major European cities. The database includes detailed information about:

- Individual experts and their affiliations
- Organizations and their key figures
- Focus areas and activities
- Contact information and links
- Relationships between experts and organizations

## Features

- **Comprehensive Data Model**: Structured schema for experts, organizations, cities, focus areas, and more
- **REST API**: FastAPI-based API for easy data access and management
- **Docker Deployment**: Ready-to-use Docker setup for quick deployment
- **Admin Interface**: pgAdmin included for database management
- **Sample Data**: Pre-loaded with sample data of Ukrainian experts and organizations

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ukraine-experts-db
   ```

2. Start the services:
   ```
   cd docker
   docker-compose up -d
   ```

3. Access the services:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - pgAdmin: http://localhost:5050 (login with admin@example.com / password)

## API Endpoints

The API provides the following endpoints:

- `/cities` - List all cities
- `/experts/city/{city_id}` - Get experts by city
- `/organizations` - List organizations with key figures
- `/experts/{expert_id}` - Get detailed expert information
- `/search?q={search_term}` - Search for experts
- `/experts/focus/{focus_area}` - Get experts by focus area
- `/diaspora/organizations` - List diaspora organizations
- `/statistics` - Get database statistics

## Database Schema

The database includes the following main tables:

- `cities` - European cities where experts and organizations are based
- `experts` - Both individual experts and organizations
- `expert_focus_areas` - Areas of expertise or focus
- `key_figures` - Key people in organizations
- `contacts` - Contact information
- `links` - Relevant links (websites, profiles, etc.)
- `activities` - Activities and events
- `publications` - Publications by experts
- `tags` - Tags for categorization

## Development

### Local Development

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the database:
   ```
   cd docker
   docker-compose up -d postgres pgadmin
   ```

3. Run the API locally:
   ```
   cd src
   uvicorn api:app --reload
   ```

### Adding More Data

You can add more data through:

1. The API endpoints
2. Direct SQL in pgAdmin
3. Adding SQL scripts to the `docker/init` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details. 