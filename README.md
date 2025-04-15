# Ukraine Experts Database

A searchable directory of Ukraine experts and organizations.

## Overview

This application provides a searchable database of Ukraine experts and organizations. It consists of:

- A FastAPI backend (API)
- A Next.js frontend (UI)
- PostgreSQL database for data storage

## Local Development

### Prerequisites

- PostgreSQL 15+
- Node.js 20+ (for frontend development)
- Python 3.9+ (for backend development)

### Setup without Docker

We provide scripts to make setup and running the application easy:

1. Run the setup script to configure your local environment:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. Start the application using:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

This will start both the API and UI services:
- API: http://localhost:8000
- UI: http://localhost:3000

### Alternative: Running with Docker Compose

If you prefer using Docker, you can still run the application with Docker Compose:

```bash
docker-compose up -d
```

This will start both the API and UI services:
- API: http://localhost:8000
- UI: http://localhost:3001

### Running Services Individually

#### API

```bash
cd ukraine-experts-db

# Install dependencies
pip install -r requirements.txt

# Run the API
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

#### UI

```bash
cd ukraine-experts-ui

# Install dependencies
npm install

# Run the development server
npm run dev
```

## Project Structure

```
.
├── ukraine-experts-db/      # Backend API application
│   ├── src/                 # Source code
│   │   ├── api.py           # FastAPI application entry point
│   │   └── db_utils.py      # Database utilities
│   └── requirements.txt     # Python dependencies
├── ukraine-experts-ui/      # Next.js frontend application
│   ├── src/                 # Source code
│   └── package.json         # Node.js dependencies
├── docker-compose.yml       # Docker Compose configuration (optional)
├── .env                     # Environment variables
├── db-schema.sql            # Database schema
├── setup.sh                 # Setup script for local development
└── start.sh                 # Script to start the application locally
```

## Features

- Search for experts by name, expertise, and organization
- Filter experts by country, city, and expertise
- View detailed expert profiles
- Browse organizations
- View statistics about the expert database

## License

MIT 