const { Pool } = require('pg');
require('dotenv').config();

// Initialize PostgreSQL connection pool with better configuration for serverless
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' 
    ? { rejectUnauthorized: false } 
    : false,
  // Better defaults for serverless environment
  max: 1, // Maximum number of clients
  idleTimeoutMillis: 120000, // Close idle clients after 2 minutes
  connectionTimeoutMillis: 10000, // Return an error after 10 seconds if connection could not be established
});

// Connection error handler
pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);
});

// Function to execute queries with improved error handling
async function query(text, params) {
  const client = await pool.connect();
  try {
    const start = Date.now();
    const result = await client.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: result.rowCount });
    return result;
  } catch (err) {
    console.error('Database query error:', err);
    throw err;
  } finally {
    client.release();
  }
}

// Function to execute queries within a transaction
async function transaction(callback) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const result = await callback(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    console.error('Transaction error:', err);
    throw err;
  } finally {
    client.release();
  }
}

module.exports = {
  query,
  transaction,
  pool
};
