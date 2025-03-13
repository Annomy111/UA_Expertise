#!/usr/bin/env python3
import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000/experts"

# Final set of organizations with detailed information
organizations = [
    # Berlin, Germany
    {
        "name": "Kiron Open Higher Education",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "A digital education platform providing free online courses to refugees, including Ukrainians. Has provided over 500 free online courses to Ukrainian refugees since 2022.",
        "founding_year": 2015,
        "is_diaspora": False,
        "focus_areas": ["education"],
        "contacts": [
            {
                "type": "email",
                "value": "volunteer@kiron.ngo",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://kiron.ngo",
                "is_primary": False
            }
        ],
        "tags": ["online education", "refugee support", "digital learning"],
        "links": [
            {
                "title": "Logo",
                "url": "https://kiron.ngo/wp-content/themes/kiron/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "CineMova",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "A Ukrainian film collective in Berlin organizing film festivals and screenings to promote Ukrainian cinema and culture. Has hosted over 30 events in 2024.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["cultural_diplomacy"],
        "contacts": [
            {
                "type": "email",
                "value": "info@cinemova.org",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://cinemova.org",
                "is_primary": False
            }
        ],
        "tags": ["film", "cultural diplomacy", "diaspora"],
        "links": [
            {
                "title": "Logo",
                "url": "https://cinemova.org/wp-content/uploads/logo-cinemova.png",
                "description": "Organization logo"
            }
        ]
    },
    
    # Brussels, Belgium
    {
        "name": "European Policy Centre (EPC)",
        "type": "organization",
        "city_id": 1,  # Brussels
        "description": "A Brussels-based think tank with a strong focus on Ukraine and EU-Ukraine relations. Their 2024 policy paper shaped the €50B Ukraine Facility.",
        "founding_year": 1997,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis", "advocacy"],
        "contacts": [
            {
                "type": "email",
                "value": "info@epc.eu",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://epc.eu",
                "is_primary": False
            }
        ],
        "key_figures": [
            {
                "name": "Amanda Paul",
                "role": "Senior Policy Analyst",
                "description": "Leads EPC's Ukraine's European Future project"
            }
        ],
        "tags": ["EU policy", "policy analysis", "Ukraine-EU relations"],
        "links": [
            {
                "title": "Logo",
                "url": "https://www.epc.eu/images/epc_logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    
    # Warsaw, Poland
    {
        "name": "Caritas Migrant Center",
        "type": "organization",
        "city_id": 4,  # Warsaw
        "description": "A Catholic charity providing food aid, job placement, and social services to Ukrainian refugees in Poland. Distributed over 20,000 food packages in 2024.",
        "founding_year": 1990,
        "is_diaspora": False,
        "focus_areas": ["humanitarian", "community_support"],
        "contacts": [
            {
                "type": "email",
                "value": "migranci@caritas.pl",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://caritas.pl",
                "is_primary": False
            }
        ],
        "tags": ["food aid", "job placement", "humanitarian aid"],
        "links": [
            {
                "title": "Logo",
                "url": "https://caritas.pl/wp-content/themes/caritas/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    
    # Paris, France
    {
        "name": "Comité d'entraide ukrainienne",
        "type": "organization",
        "city_id": 3,  # Paris
        "description": "A Ukrainian mutual aid committee in Paris distributing medical supplies, food, and clothing to Ukraine. Sends over 1,000 medical kits monthly to frontline units.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["humanitarian", "community_support"],
        "contacts": [
            {
                "type": "email",
                "value": "entraide.ukraine.paris@orange.fr",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://facebook.com/EntraideUkraineParis",
                "is_primary": False
            }
        ],
        "tags": ["medical aid", "humanitarian aid", "diaspora"],
        "links": [
            {
                "title": "Logo",
                "url": "https://comite-entraide-ukrainienne.fr/images/logo-ceu.jpg",
                "description": "Organization logo"
            }
        ]
    },
    
    # Pan-European
    {
        "name": "UA Transformation Lab",
        "type": "organization",
        "city_id": 2,  # Berlin (HQ)
        "description": "A joint German-Ukrainian initiative developing reforms for Ukraine's EU accession process. Co-developed judicial reforms critical for Ukraine's EU accession talks in 2024.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["research", "policy_analysis", "advocacy"],
        "contacts": [
            {
                "type": "email",
                "value": "lab@iep-berlin.de",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://iep-berlin.de",
                "is_primary": False
            }
        ],
        "tags": ["EU accession", "reforms", "policy analysis"],
        "links": [
            {
                "title": "Logo",
                "url": "https://iep-berlin.de/wp-content/uploads/ua-transformation-lab-logo.png",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Razumkov Centre",
        "type": "organization",
        "city_id": 4,  # Warsaw (European office)
        "description": "A leading Ukrainian think tank with a European office in Warsaw, advising the EU on decentralization reforms for Ukraine's reconstruction.",
        "founding_year": 1994,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {
                "type": "email",
                "value": "office@razumkov.org.ua",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://razumkov.org.ua",
                "is_primary": False
            }
        ],
        "tags": ["policy analysis", "decentralization", "reconstruction"],
        "links": [
            {
                "title": "Logo",
                "url": "https://razumkov.org.ua/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    }
]

# Names of organizations we've already added to avoid duplicates
existing_organizations = [
    "Vitsche e.V.",
    "Promote Ukraine",
    "BEforUkraine",
    "Alliance of Ukrainian Organizations",
    "Alliance of Ukrainian Organisations (AUO)",
    "Ukrainian Cultural Community in Berlin",
    "Association des Femmes Ukrainiennes en France",
    "Union of Ukrainians in France",
    "Fundacja \"Nasz Wybór\"",
    "Stand With Ukraine Foundation",
    "Opora e.V.",
    "Kwitne Queer",
    "Berlin to Borders",
    "BIPoC Ukraine & Friends",
    "Ukrainian Voices Refugee Committee",
    "Plast Belgium",
    "Ukrainian Science Diaspora Poland",
    "Euromaidan Warsaw",
    "Cité internationale universitaire",
    "Alliance4Ukraine",
    "Ukrainisches Institut in Deutschland",
    "Zentralverband der Ukrainer (ZVUD)",
    "Ukraine-Hilfe Berlin e.V.",
    "Association of Ukrainians in Belgium",
    "Solidarity with Ukraine (Belgium)",
    "Ocalenie Foundation",
    "Konsorcjum Migracyjne",
    "Ukrainian Embassy Cultural Center",
    "Association France-Ukraine",
    "Ukrainian World Congress",
    "Cedos Think Tank"
]

def add_organizations():
    added_count = 0
    skipped_count = 0
    
    for i, org in enumerate(organizations):
        # Skip if organization with similar name already exists
        if any(existing.lower() in org["name"].lower() or org["name"].lower() in existing.lower() 
               for existing in existing_organizations):
            print(f"⚠️ Skipping (potential duplicate): {org['name']}")
            skipped_count += 1
            continue
            
        try:
            print(f"Adding organization: {org['name']}...")
            response = requests.post(API_URL, json=org)
            
            if response.status_code == 201:
                print(f"✅ Successfully added: {org['name']}")
                print(json.dumps(response.json(), indent=2))
                added_count += 1
            else:
                print(f"❌ Failed to add: {org['name']}. Status code: {response.status_code}")
                print(response.text)
            
            # Add a small delay between requests to avoid overwhelming the API
            if i < len(organizations) - 1:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error adding {org['name']}: {e}")
    
    print(f"\nSummary: Added {added_count} organizations, skipped {skipped_count} potential duplicates.")
    print(f"Attempted to add {len(organizations)} organizations in total.")

if __name__ == "__main__":
    add_organizations() 