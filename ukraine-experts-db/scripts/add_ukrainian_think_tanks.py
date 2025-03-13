#!/usr/bin/env python3
import requests
import json
import uuid
from datetime import datetime

# API-Endpunkt
API_URL = "http://localhost:8000"

# Stadt-IDs (aus der Datenbank)
CITY_IDS = {
    "Kyiv": 1,  # Annahme: Kyiv hat ID 1
    "Berlin": 2,
    "Brussels": 3,
    "Warsaw": 4,
    "Paris": 5
}

# Ukrainische Think Tanks
think_tanks = [
    {
        "id": str(uuid.uuid4()),
        "name": "ADASTRA",
        "type": "organization",
        "description": "ADASTRA is a Ukrainian independent think tank of social science fellows developing data-driven research for policy innovation. Ranked as Best New Think Tank by the 2020 Global Go To Think Tank Index, ADASTRA focuses on international relations and policy analysis with a particular emphasis on Ukraine's position in global affairs.",
        "founding_year": 2019,
        "city_id": CITY_IDS["Kyiv"],
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis", "education"],
        "contacts": [
            {
                "type": "website",
                "value": "http://adastra.org.ua/en",
                "is_primary": True
            },
            {
                "type": "email",
                "value": "adastra@adastra.org.ua",
                "is_primary": True
            },
            {
                "type": "phone",
                "value": "+38 (066) 499 04 30",
                "is_primary": True
            },
            {
                "type": "address",
                "value": "UNIT.City, Ukraine, Kyiv, str. Dorohozhytska, 3",
                "is_primary": True
            },
            {
                "type": "linkedin",
                "value": "https://www.linkedin.com/company/adastra-ua",
                "is_primary": False
            }
        ],
        "key_figures": [
            {
                "name": "Taras Prodaniuk",
                "role": "President"
            },
            {
                "name": "Viktor Karvatskyi",
                "role": "Development Director"
            },
            {
                "name": "Yaroslav Suprun",
                "role": "Research Director"
            }
        ],
        "tags": ["think tank", "policy analysis", "Ukraine", "international relations", "data-driven research"]
    }
]

def add_think_tank(think_tank):
    """Fügt einen Think Tank zur Datenbank hinzu."""
    # Erstelle den Experten (Organisation)
    expert_data = {
        "id": think_tank["id"],
        "name": think_tank["name"],
        "type": think_tank["type"],
        "description": think_tank["description"],
        "founding_year": think_tank["founding_year"],
        "city_id": think_tank["city_id"],
        "is_diaspora": think_tank["is_diaspora"],
        "focus_areas": think_tank["focus_areas"],
        "tags": think_tank["tags"],
        "contacts": think_tank["contacts"],
        "key_figures": think_tank.get("key_figures", [])
    }
    
    # Sende die Anfrage
    response = requests.post(f"{API_URL}/experts", json=expert_data)
    
    if response.status_code == 201:
        print(f"Think Tank '{think_tank['name']}' erfolgreich hinzugefügt mit ID: {think_tank['id']}")
        return True
    elif response.status_code == 409:
        print(f"Think Tank '{think_tank['name']}' existiert bereits in der Datenbank.")
        return False
    else:
        print(f"Fehler beim Hinzufügen des Think Tanks '{think_tank['name']}': {response.text}")
        return False

def main():
    """Hauptfunktion zum Hinzufügen aller Think Tanks."""
    successful = 0
    skipped = 0
    
    for think_tank in think_tanks:
        if add_think_tank(think_tank):
            successful += 1
        else:
            skipped += 1
    
    print(f"\nZusammenfassung:")
    print(f"Insgesamt versuchte Think Tanks: {len(think_tanks)}")
    print(f"Erfolgreich hinzugefügt: {successful}")
    print(f"Übersprungen (existieren bereits): {skipped}")

if __name__ == "__main__":
    main() 