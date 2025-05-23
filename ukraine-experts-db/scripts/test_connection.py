#!/usr/bin/env python3
import sys
import os
# Ensure the repository root is on the Python path so that our local
# stub modules (e.g. a lightweight psycopg2 replacement) can be
# imported when running this script directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import psycopg2
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the database utilities
import db_utils

# Überschreibe die Datenbankverbindungsparameter für den Docker-Container
db_utils.DB_PARAMS = {
    "host": "localhost",  # Docker-Container ist über localhost erreichbar
    "database": "ukraine_experts",
    "user": "admin",
    "password": "password",
    "port": 5433
}

def test_connection():
    """Test the connection to the database and print some statistics."""
    try:
        # Debug: Zeige die Verbindungsparameter an
        print("Verbindungsparameter:", db_utils.DB_PARAMS)
        
        # Direkte Verbindung testen
        conn = psycopg2.connect(**db_utils.DB_PARAMS)
        print("Direkte Verbindung zur Datenbank erfolgreich!")
        conn.close()
        
        # Get database statistics
        stats = db_utils.get_statistics()
        print("\nDatabase Statistics:")
        print(json.dumps(stats, indent=2))
        
        # Get diaspora organizations
        print("\nDiaspora Organizations:")
        diaspora_orgs = db_utils.get_diaspora_organizations()
        for org in diaspora_orgs:
            print(f"- {org['name']} ({org['city_name']}, {org['country']})")
        
        return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1) 