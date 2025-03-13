#!/usr/bin/env python3
import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000/experts"

# Organizations with logo URLs from the provided list
organizations = [
    # Berlin, Germany
    {
        "name": "Ukrainisches Institut in Deutschland",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "A cultural institute promoting Ukrainian culture and academic exchanges in Germany. Focuses on cultural diplomacy and building bridges between Ukrainian and German societies.",
        "founding_year": 2020,
        "is_diaspora": True,
        "focus_areas": ["cultural_diplomacy", "education"],
        "contacts": [
            {
                "type": "email",
                "value": "germany@ui.org.ua",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://ui.org.ua",
                "is_primary": False
            }
        ],
        "tags": ["cultural diplomacy", "academic exchanges", "diaspora"],
        "links": [
            {
                "title": "Logo",
                "url": "https://ui.org.ua/wp-content/uploads/logo.png",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Zentralverband der Ukrainer (ZVUD)",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "The Central Association of Ukrainians in Germany, coordinating community activities and advocacy efforts for the Ukrainian diaspora in Germany.",
        "founding_year": 1945,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "community_support", "cultural_diplomacy"],
        "contacts": [
            {
                "type": "email",
                "value": "info@zvud.de",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://zvud.de",
                "is_primary": False
            }
        ],
        "tags": ["diaspora", "community coordination", "cultural heritage"],
        "links": [
            {
                "title": "Logo",
                "url": "https://zvud.de/wp-content/themes/zvud/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Ukraine-Hilfe Berlin e.V.",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "A volunteer organization providing housing support, integration assistance, and humanitarian aid for Ukrainian refugees in Berlin.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["humanitarian", "community_support", "integration"],
        "contacts": [
            {
                "type": "email",
                "value": "info@ukraine-hilfe-berlin.de",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://ukraine-hilfe-berlin.de",
                "is_primary": False
            }
        ],
        "tags": ["refugee integration", "housing support", "humanitarian aid"],
        "links": [
            {
                "title": "Logo",
                "url": "https://ukraine-hilfe-berlin.de/img/logo-uhb.png",
                "description": "Organization logo"
            }
        ]
    },
    
    # Brussels, Belgium
    {
        "name": "Association of Ukrainians in Belgium",
        "type": "organization",
        "city_id": 1,  # Brussels
        "description": "The main Ukrainian diaspora organization in Belgium, preserving Ukrainian cultural heritage and providing legal aid and support to the community.",
        "founding_year": 1948,
        "is_diaspora": True,
        "focus_areas": ["cultural_diplomacy", "community_support", "advocacy"],
        "contacts": [
            {
                "type": "email",
                "value": "ua.refugee.committee@gmail.com",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://facebook.com/UkrainiansBelgium",
                "is_primary": False
            }
        ],
        "tags": ["cultural preservation", "legal aid", "diaspora"],
        "links": [
            {
                "title": "Logo",
                "url": "https://ukrainians.be/wp-content/themes/uab/images/logo.png",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Solidarity with Ukraine (Belgium)",
        "type": "organization",
        "city_id": 1,  # Brussels
        "description": "A grassroots solidarity movement mobilizing donations and support for Ukraine in Belgium. Has raised over €500,000 for humanitarian aid since 2022.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["humanitarian", "advocacy"],
        "contacts": [
            {
                "type": "social",
                "value": "https://facebook.com/SolidarityUkraineBelgium",
                "is_primary": True
            }
        ],
        "tags": ["humanitarian aid", "solidarity", "fundraising"],
        "links": [
            {
                "title": "Logo",
                "url": "https://solidarity-ukraine.be/images/logo-solidarity.jpg",
                "description": "Organization logo"
            }
        ]
    },
    
    # Warsaw, Poland
    {
        "name": "Ocalenie Foundation",
        "type": "organization",
        "city_id": 4,  # Warsaw
        "description": "A Polish foundation providing housing support, legal counseling, and integration assistance for refugees, including Ukrainians. Has assisted over 3,000 Ukrainian refugees since 2022.",
        "founding_year": 2000,
        "is_diaspora": False,
        "focus_areas": ["humanitarian", "community_support", "integration"],
        "contacts": [
            {
                "type": "email",
                "value": "warszawa@ocalenie.org.pl",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://ocalenie.org.pl",
                "is_primary": False
            }
        ],
        "tags": ["housing support", "legal counseling", "refugee assistance"],
        "links": [
            {
                "title": "Logo",
                "url": "https://ocalenie.org.pl/wp-content/themes/ocalenie/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Konsorcjum Migracyjne",
        "type": "organization",
        "city_id": 4,  # Warsaw
        "description": "A consortium of Polish NGOs working on migration policy research and advocacy, with a focus on Ukrainian refugees since 2022. Has published influential policy reports cited by the Polish Parliament.",
        "founding_year": 2007,
        "is_diaspora": False,
        "focus_areas": ["research", "advocacy", "policy_analysis"],
        "contacts": [
            {
                "type": "email",
                "value": "biuro@konsorcjum.org.pl",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://konsorcjum.org.pl",
                "is_primary": False
            }
        ],
        "tags": ["migration policy", "research", "policy analysis"],
        "links": [
            {
                "title": "Logo",
                "url": "https://konsorcjum.org.pl/images/konsorcjum-logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    
    # Paris, France
    {
        "name": "Ukrainian Embassy Cultural Center",
        "type": "organization",
        "city_id": 3,  # Paris
        "description": "The cultural center of the Ukrainian Embassy in Paris, offering language courses, literary events, and cultural programs to promote Ukrainian culture in France.",
        "founding_year": 2010,
        "is_diaspora": False,
        "focus_areas": ["cultural_diplomacy", "education"],
        "contacts": [
            {
                "type": "email",
                "value": "culture@amb-ukraine.fr",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://france.mfa.gov.ua",
                "is_primary": False
            }
        ],
        "tags": ["language courses", "cultural events", "literary events"],
        "links": [
            {
                "title": "Logo",
                "url": "https://france.mfa.gov.ua/assets/images/logo-embassy.png",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Association France-Ukraine",
        "type": "organization",
        "city_id": 3,  # Paris
        "description": "A French-Ukrainian friendship association coordinating humanitarian aid for Ukraine and promoting cultural exchanges between the two countries.",
        "founding_year": 1991,
        "is_diaspora": True,
        "focus_areas": ["humanitarian", "cultural_diplomacy", "advocacy"],
        "contacts": [
            {
                "type": "email",
                "value": "contact@france-ukraine.org",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://france-ukraine.org",
                "is_primary": False
            }
        ],
        "tags": ["humanitarian aid", "cultural exchange", "Franco-Ukrainian relations"],
        "links": [
            {
                "title": "Logo",
                "url": "https://france-ukraine.org/wp-content/uploads/logo-afu.png",
                "description": "Organization logo"
            }
        ]
    },
    
    # Pan-European
    {
        "name": "Ukrainian World Congress",
        "type": "organization",
        "city_id": 1,  # Brussels (European office)
        "description": "The global coordinating body for Ukrainian diaspora organizations worldwide, with chapters across Europe. Lobbies for sanctions against Russia and coordinates global aid efforts for Ukraine.",
        "founding_year": 1967,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "policy_analysis", "community_support"],
        "contacts": [
            {
                "type": "email",
                "value": "info@ukrainianworldcongress.org",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://ukrainianworldcongress.org",
                "is_primary": False
            }
        ],
        "key_figures": [
            {
                "name": "Paul Grod",
                "role": "President",
                "description": "Leads the global Ukrainian diaspora organization"
            }
        ],
        "tags": ["global advocacy", "sanctions lobbying", "diaspora coordination"],
        "links": [
            {
                "title": "Logo",
                "url": "https://ukrainianworldcongress.org/wp-content/themes/uwc/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Cedos Think Tank",
        "type": "organization",
        "city_id": 4,  # Warsaw (European office)
        "description": "A Ukrainian think tank with a European office in Warsaw, providing data-driven policy analysis on migration, education, and urban development. Their displacement data has influenced EU humanitarian aid policies.",
        "founding_year": 2010,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis", "education"],
        "contacts": [
            {
                "type": "email",
                "value": "info@cedos.org.ua",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://cedos.org.ua",
                "is_primary": False
            }
        ],
        "tags": ["policy analysis", "data-driven research", "migration"],
        "links": [
            {
                "title": "Logo",
                "url": "https://cedos.org.ua/wp-content/themes/cedos/assets/images/logo.svg",
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
    "Alliance4Ukraine"
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