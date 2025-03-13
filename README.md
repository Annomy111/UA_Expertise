# Ukraine Experts Database

A searchable directory of Ukraine experts and organizations.

## Overview

This application provides a searchable database of Ukraine experts and organizations. It consists of:

- A FastAPI backend (API)
- A Next.js frontend (UI)
- SQLite database for data storage

## Local Development

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local UI development)
- Python 3.9+ (for local API development)

### Running with Docker Compose

The easiest way to run the application locally is using Docker Compose:

```bash
docker-compose up -d
```

This will start both the API and UI services:
- API: http://localhost:8000
- UI: http://localhost:3000

### Running Services Individually

#### API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload
```

#### UI

```bash
cd ukraine-experts-ui

# Install dependencies
npm install

# Run the development server
npm run dev
```

## Deployment on Render

This project is configured for deployment on Render using the `render.yaml` file.

1. Fork or clone this repository to your GitHub account
2. In Render, create a new "Blueprint" instance
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` configuration
5. Deploy the services

## Project Structure

```
.
├── Dockerfile              # Docker configuration for API
├── docker-compose.yml      # Docker Compose configuration
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
├── experts.db              # SQLite database (generated)
└── ukraine-experts-ui/     # Next.js frontend application
```

## Features

- Search for experts by name, expertise, and organization
- Filter experts by country, city, and expertise
- View detailed expert profiles
- Browse organizations
- View statistics about the expert database

## License

MIT 