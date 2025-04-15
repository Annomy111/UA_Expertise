# Ukraine Experts Database - Netlify Serverless API

This is a serverless implementation of the Ukraine Experts Database API using Netlify Functions that connects to your existing PostgreSQL database.

## Setup Instructions

### 1. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```
   cp .env.example .env
   ```

2. Fill in your PostgreSQL database connection details in the `.env` file:
   ```
   DATABASE_URL=postgres://username:password@hostname:5432/ukraine_experts
   ```

### 2. Install Dependencies

```bash
npm install
```

### 3. Local Development

To run the functions locally:

```bash
npm install -g netlify-cli
netlify dev
```

This will start a local server at http://localhost:8888 with your API accessible at:
- http://localhost:8888/.netlify/functions/api
- http://localhost:8888/api/* (via redirects)

### 4. Deploy to Netlify

1. Create a new site on Netlify:
   ```bash
   netlify deploy --prod
   ```

2. Alternatively, you can use the Netlify dashboard:
   - Connect to your Git repository
   - Set the build settings:
     - Build command: leave blank
     - Publish directory: `public`
   - Set your environment variables (DATABASE_URL) in the Netlify dashboard
   - Deploy!

## Connecting to Your PostgreSQL Database

For the serverless functions to access your database, you have two options:

1. **Self-hosted PostgreSQL**: Expose your PostgreSQL database with appropriate security measures (SSL, firewall rules, VPN, etc.).

2. **Managed PostgreSQL Service**: Use a cloud PostgreSQL provider like:
   - Heroku Postgres
   - DigitalOcean Managed Databases
   - AWS RDS
   - Google Cloud SQL
   - Azure Database for PostgreSQL

The simplest approach is to migrate your data to one of these services. If you're hosting PostgreSQL locally, you'll need to ensure it's accessible from the internet with proper security.

## API Endpoints

- `/api/` - Welcome message and API info
- `/api/experts` - Get all experts or create a new one (GET, POST)
- `/api/experts/{id}` - Get, update or delete a specific expert (GET, PUT, DELETE)
- `/api/cities` - Get all cities (GET)
- `/api/search?q={term}` - Search for experts (GET)
- `/api/statistics` - Get database statistics (GET)

## Connecting the Frontend

Update the frontend API URL in your Next.js app to point to your Netlify Functions API:

```
NEXT_PUBLIC_API_URL=https://your-netlify-site.netlify.app/api
```
