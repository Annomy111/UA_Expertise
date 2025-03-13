#!/usr/bin/env python3
import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000/experts"

# European organizations data from the provided list
organizations = [
    # Berlin, Germany
    {
        "name": "Alliance of Ukrainian Organisations (AUO)",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "An umbrella organization coordinating 15+ Ukrainian groups in Berlin. Established in 2022 to coordinate humanitarian aid and advocacy efforts for Ukraine.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "community_support", "humanitarian"],
        "contacts": [
            {
                "type": "email",
                "value": "info@ukr-alliance.de",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://ukr-alliance.de",
                "is_primary": False
            }
        ],
        "key_figures": [
            {
                "name": "Nataliya Pryhornytska",
                "role": "Coordinator",
                "description": "Coordinates the alliance's humanitarian efforts"
            }
        ],
        "tags": ["diaspora", "coalition", "humanitarian aid"]
    },
    {
        "name": "Opora e.V.",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "A legal and social support organization for Ukrainian refugees in Berlin. Provides legal counseling, housing assistance, and integration support.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["community_support", "integration"],
        "contacts": [
            {
                "type": "email",
                "value": "kontakt@opora-berlin.de",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://opora-berlin.de",
                "is_primary": False
            }
        ],
        "tags": ["legal support", "refugee assistance", "diaspora"]
    },
    {
        "name": "Kwitne Queer",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "An LGBTQ+ Ukrainian advocacy group in Berlin focusing on the specific needs of queer refugees from Ukraine. Provides safe spaces, counseling, and community events.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "community_support"],
        "contacts": [
            {
                "type": "email",
                "value": "kontakt@kwitne-queer.de",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://instagram.com/kwitne_queer",
                "is_primary": False
            }
        ],
        "tags": ["LGBTQ+", "diaspora", "advocacy"]
    },
    {
        "name": "Berlin to Borders",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "A volunteer-run humanitarian initiative delivering medical supplies and aid directly to frontline cities in Ukraine. Has delivered over 40 tons of medical supplies since 2022.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["humanitarian"],
        "contacts": [
            {
                "type": "email",
                "value": "contact@berlintoborders.org",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://berlintoborders.org",
                "is_primary": False
            }
        ],
        "tags": ["humanitarian aid", "medical supplies", "frontline support"]
    },
    {
        "name": "BIPoC Ukraine & Friends",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "An organization supporting Black, Indigenous, and People of Color from Ukraine who face additional discrimination as refugees. Advocates for anti-racist refugee policies.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "community_support"],
        "contacts": [
            {
                "type": "email",
                "value": "bipoc.ukraine@gmail.com",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://instagram.com/bipoc.ukraine",
                "is_primary": False
            }
        ],
        "tags": ["anti-racism", "diaspora", "advocacy"]
    },
    
    # Brussels, Belgium
    {
        "name": "Ukrainian Voices Refugee Committee",
        "type": "organization",
        "city_id": 1,  # Brussels
        "description": "A refugee support committee providing emergency housing, mental health services, and integration assistance for Ukrainians in Belgium. Works closely with UNHCR.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["community_support", "humanitarian"],
        "contacts": [
            {
                "type": "phone",
                "value": "+32 478 55 12 34",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://facebook.com/UVRefugeeCommittee",
                "is_primary": False
            }
        ],
        "tags": ["refugee support", "mental health", "diaspora"]
    },
    {
        "name": "Plast Belgium",
        "type": "organization",
        "city_id": 1,  # Brussels
        "description": "The Belgian branch of the Ukrainian scouting organization Plast. Provides youth programs, trauma counseling, and community activities for Ukrainian children and teenagers.",
        "founding_year": 2010,
        "is_diaspora": True,
        "focus_areas": ["education", "community_support"],
        "contacts": [
            {
                "type": "email",
                "value": "plastbelgium@gmail.com",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://facebook.com/PlastBelgium",
                "is_primary": False
            }
        ],
        "tags": ["youth", "scouting", "diaspora"]
    },
    
    # Warsaw, Poland
    {
        "name": "Ukrainian Science Diaspora Poland",
        "type": "organization",
        "city_id": 4,  # Warsaw
        "description": "A network of Ukrainian academics and researchers in Poland. Facilitates integration of Ukrainian scholars into Polish academia and supports scientific collaboration.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["research", "education"],
        "contacts": [
            {
                "type": "email",
                "value": "science.diaspora.pl@gmail.com",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://facebook.com/UkrainianScienceDiaspora",
                "is_primary": False
            }
        ],
        "tags": ["academic", "research", "diaspora"]
    },
    {
        "name": "Euromaidan Warsaw",
        "type": "organization",
        "city_id": 4,  # Warsaw
        "description": "A grassroots activist movement organizing demonstrations, rallies, and advocacy campaigns for Ukraine in Poland. Has organized over 50 rallies for military aid since 2022.",
        "founding_year": 2014,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "political_mobilization"],
        "contacts": [
            {
                "type": "email",
                "value": "euromaidan.warszawa@gmail.com",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://facebook.com/EuromaidanWarszawa",
                "is_primary": False
            }
        ],
        "tags": ["activism", "political mobilization", "diaspora"]
    },
    
    # Paris, France
    {
        "name": "Cité internationale universitaire",
        "type": "organization",
        "city_id": 3,  # Paris
        "description": "An international university campus in Paris that has created a special program for Ukrainian students and academics. Has hosted over 300 Ukrainian students since 2022.",
        "founding_year": 1925,
        "is_diaspora": False,
        "focus_areas": ["education", "research"],
        "contacts": [
            {
                "type": "email",
                "value": "solidarite@ciup.fr",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://www.ciup.fr",
                "is_primary": False
            }
        ],
        "tags": ["education", "student housing", "academic support"]
    },
    
    # Pan-European
    {
        "name": "Alliance4Ukraine",
        "type": "organization",
        "city_id": 2,  # Berlin (HQ)
        "description": "A cross-border coalition coordinating 50+ NGOs across the EU. Manages a €5M housing fund and facilitates cooperation between Ukrainian and European civil society organizations.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "humanitarian", "community_support"],
        "contacts": [
            {
                "type": "email",
                "value": "contact@alliance4ukraine.eu",
                "is_primary": True
            },
            {
                "type": "website",
                "value": "https://alliance4ukraine.eu",
                "is_primary": False
            }
        ],
        "key_figures": [
            {
                "name": "Maria Mezentseva",
                "role": "Advisory Board Member",
                "description": "Ukrainian MP who advises on policy priorities"
            }
        ],
        "tags": ["coalition", "cross-border", "civil society"]
    }
]

# Names of organizations we've already added to avoid duplicates
existing_organizations = [
    "Vitsche e.V.",
    "Promote Ukraine",
    "BEforUkraine",
    "Alliance of Ukrainian Organizations",  # Similar to "Alliance of Ukrainian Organisations (AUO)"
    "Ukrainian Cultural Community in Berlin",
    "Association des Femmes Ukrainiennes en France",
    "Union of Ukrainians in France",
    "Fundacja \"Nasz Wybór\"",
    "Stand With Ukraine Foundation"
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