#!/usr/bin/env python3
import requests
import json

# API endpoint
API_URL = "http://localhost:8000/experts"

# Sample organization data from the list
organization_data = {
    "name": "Vitsche e.V.",
    "type": "organization",
    "city_id": 2,  # Berlin
    "description": "A youth-led Ukrainian activist community founded in January 2022. Stands for freedom and development of Ukraine, using protests, cultural diplomacy, and innovative campaigns.",
    "founding_year": 2022,
    "is_diaspora": True,
    "focus_areas": ["advocacy", "cultural_diplomacy", "political_mobilization"],
    "contacts": [
        {
            "type": "website",
            "value": "https://vitsche.org",
            "is_primary": True
        },
        {
            "type": "social",
            "value": "https://instagram.com/vitsche_berlin",
            "is_primary": False
        }
    ],
    "key_figures": [
        {
            "name": "Iryna Shulikina",
            "role": "Chairwoman & Executive Director",
            "description": "Leads the youth-driven Ukrainian diaspora NGO in Berlin"
        },
        {
            "name": "Eva Yakubovska",
            "role": "Advocacy Lead",
            "description": "Coordinates advocacy efforts for the organization"
        },
        {
            "name": "Krista-Marija Läbe",
            "role": "Spokesperson",
            "description": "Press spokesperson for the organization"
        }
    ],
    "tags": ["diaspora", "youth", "activism", "cultural diplomacy", "protests"]
}

def add_organization():
    try:
        response = requests.post(API_URL, json=organization_data)
        
        if response.status_code == 201:
            print("Organization added successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to add organization. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_organization() 