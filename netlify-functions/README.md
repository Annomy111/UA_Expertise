# Ukraine Experts Database - Serverless API

This is a serverless implementation of the Ukraine Experts Database API using Netlify Functions with a Supabase database backend.

## Setup Instructions

### 1. Set Up Supabase 

1. Create a new Supabase project at [https://app.supabase.com](https://app.supabase.com)
2. Set up the following tables in Supabase:

#### Database Schema

**experts**
- id (UUID, primary key)
- name (text, not null)
- type (text, not null) - 'individual' or 'organization'
- title (text)
- affiliation (text)
- city_id (integer, foreign key to cities.id)
- description (text)
- founding_year (integer)
- is_diaspora (boolean, default false)
- image (text)
- created_at (timestamp with time zone, default now())
- updated_at (timestamp with time zone, default now())

**cities**
- id (integer, primary key)
- name (text, not null)
- country (text, not null)
- description (text)

**contacts**
- id (UUID, primary key)
- expert_id (UUID, foreign key to experts.id)
- type (text, not null)
- value (text, not null)
- is_primary (boolean, default false)

**key_figures**
- id (UUID, primary key)
- expert_id (UUID, foreign key to experts.id)
- name (text, not null)
- role (text)
- description (text)

**expert_focus_areas**
- id (UUID, primary key)
- expert_id (UUID, foreign key to experts.id)
- focus_area (text, not null)

**expert_tags**
- id (UUID, primary key)
- expert_id (UUID, foreign key to experts.id)
- tag (text, not null)

3. Set up Row Level Security (RLS) policies for your tables
4. Get your Supabase URL and service key from the Supabase dashboard

### 2. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```
   cp .env.example .env
   ```

2. Fill in your Supabase credentials in the `.env` file:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_SERVICE_KEY=your-supabase-service-key-here
   ```

### 3. Install Dependencies

```bash
npm install
```

### 4. Local Development

To run the functions locally:

```bash
npm install -g netlify-cli
netlify dev
```

This will start a local server at http://localhost:8888 with your API accessible at:
- http://localhost:8888/.netlify/functions/api
- http://localhost:8888/api/* (via redirects)

### 5. Deploy to Netlify

1. Create a new site on Netlify
2. Connect to your Git repository
3. Set the build settings:
   - Build command: leave blank
   - Publish directory: `public`
4. Set your environment variables (SUPABASE_URL and SUPABASE_SERVICE_KEY) in the Netlify dashboard
5. Deploy!

## API Endpoints

- `/api/` - Welcome message and API info
- `/api/experts` - Get all experts or create a new one (GET, POST)
- `/api/experts/{id}` - Get, update or delete a specific expert (GET, PUT, DELETE)
- `/api/cities` - Get all cities (GET)
- `/api/search?q={term}` - Search for experts (GET)
- `/api/statistics` - Get database statistics (GET)

## Migrating Data

To migrate your existing data from the PostgreSQL database to Supabase:

1. Export your existing data to JSON or CSV files
2. Import the data to Supabase using the Supabase dashboard or API

## Connecting the Frontend

Update the frontend API URL in your Next.js app to point to your Netlify Functions API:

```
NEXT_PUBLIC_API_URL=https://your-netlify-site.netlify.app/api
```

## Limitations

- This serverless implementation does not include the expert research functionality that was in the original FastAPI app
- Transactions are handled differently in this implementation as Supabase JS client doesn't support transactions directly
