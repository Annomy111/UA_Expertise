#!/usr/bin/env python3
import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000/experts"

# Sample organizations data from the list
organizations = [
    {
        "name": "Promote Ukraine",
        "type": "organization",
        "city_id": 1,  # Brussels
        "description": "A non-profit advocacy and media hub established during the 2014 Revolution of Dignity. Became \"Ukraine's public voice in Brussels\", organising rallies, humanitarian aid collection points, and advocacy events at EU institutions.",
        "founding_year": 2014,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "humanitarian", "media"],
        "contacts": [
            {
                "type": "website",
                "value": "https://promoteukraine.org",
                "is_primary": True
            },
            {
                "type": "social",
                "value": "https://facebook.com/PromoteUkraine",
                "is_primary": False
            }
        ],
        "key_figures": [
            {
                "name": "Marta Barandiy",
                "role": "Founder & President",
                "description": "Ukrainian lawyer and civil society advocate who founded Promote Ukraine. Since Russia's 2022 invasion, she has amplified the Ukrainian perspective in Brussels."
            }
        ],
        "tags": ["advocacy", "civil society", "EU integration", "diaspora"]
    },
    {
        "name": "BEforUkraine",
        "type": "organization",
        "city_id": 1,  # Brussels
        "description": "A citizens' initiative launched in March 2022 to deliver humanitarian aid and refugee support. Has transported medical equipment, ambulances, school buses and relocated hundreds of Ukrainian refugees to host families in Belgium.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["humanitarian", "community_support"],
        "contacts": [
            {
                "type": "website",
                "value": "https://beforua.be",
                "is_primary": True
            }
        ],
        "key_figures": [
            {
                "name": "Thibault De Sadeleer",
                "role": "Co-founder",
                "description": "Belgian volunteer who helped establish the initiative in response to the 2022 invasion"
            },
            {
                "name": "Xavier Holst",
                "role": "Co-founder",
                "description": "Co-founder of the Belgian-Ukrainian humanitarian initiative"
            }
        ],
        "tags": ["humanitarian aid", "refugee support", "solidarity"]
    },
    {
        "name": "Alliance of Ukrainian Organizations",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "Formed in 2022 as a coalition uniting Berlin's Ukrainian cultural, humanitarian, and political groups. Mobilizes the diaspora for demonstrations and advocacy, builds partnerships with German and international institutions.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "cultural_diplomacy", "community_support"],
        "key_figures": [
            {
                "name": "Nataliya Pryhornytska",
                "role": "Co-Founder",
                "description": "Co-founded the alliance to coordinate Ukrainian diaspora efforts in Berlin"
            },
            {
                "name": "Oleksandra Keudel",
                "role": "Co-Founder",
                "description": "Co-founded the alliance to strengthen Ukrainian voices in Germany"
            }
        ],
        "tags": ["diaspora", "coalition", "advocacy"]
    },
    {
        "name": "Ukrainian Cultural Community in Berlin",
        "type": "organization",
        "city_id": 2,  # Berlin
        "description": "A dynamic cultural hub launched by diaspora artists after 2022, UCC uses art and culture to build understanding. It has a history of hosting creative events of social importance, facilitating exchange and mutual growth between Ukrainian and European artists.",
        "founding_year": 2022,
        "is_diaspora": True,
        "focus_areas": ["cultural_diplomacy", "education"],
        "contacts": [
            {
                "type": "social",
                "value": "https://instagram.com/ucc_berlin",
                "is_primary": True
            }
        ],
        "tags": ["cultural diplomacy", "arts", "diaspora"]
    },
    {
        "name": "Association des Femmes Ukrainiennes en France",
        "type": "organization",
        "city_id": 3,  # Paris
        "description": "A diaspora women-led charity focusing on humanitarian aid to Ukraine. Since 2022, it has sent critical supplies: ambulances, generators, medical gear, food and clothing to war zones.",
        "is_diaspora": True,
        "focus_areas": ["humanitarian", "community_support"],
        "key_figures": [
            {
                "name": "Nadia Myhal",
                "role": "President",
                "description": "Leads the Ukrainian women's association in France"
            }
        ],
        "tags": ["humanitarian aid", "women-led", "diaspora"]
    },
    {
        "name": "Union of Ukrainians in France",
        "type": "organization",
        "city_id": 3,  # Paris
        "description": "Founded in 1949 by Ukrainian refugees in France, it is the oldest Ukrainian diaspora association in Paris. Preserves Ukrainian heritage and represents the community nationally.",
        "founding_year": 1949,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "cultural_diplomacy", "community_support"],
        "key_figures": [
            {
                "name": "Bohdan Bilot",
                "role": "President",
                "description": "Leads the historic Ukrainian diaspora organization in France"
            },
            {
                "name": "Volodymyr Kogutyak",
                "role": "Vice-President",
                "description": "Vice-President of the Union and also affiliated with the Ukrainian World Congress"
            }
        ],
        "tags": ["diaspora", "cultural heritage", "advocacy"]
    },
    {
        "name": "Fundacja \"Nasz Wybór\"",
        "type": "organization",
        "city_id": 4,  # Warsaw
        "description": "Founded in 2009 by Ukrainians and Polish friends to support Ukrainian migrants in Poland. Operates the Ukrainian House in Warsaw, a cultural and information center offering legal advice, job assistance, language courses, and community events for Ukrainians.",
        "founding_year": 2009,
        "is_diaspora": True,
        "focus_areas": ["community_support", "integration", "education"],
        "key_figures": [
            {
                "name": "Myroslava Keryk",
                "role": "President",
                "description": "Ukrainian historian and community leader who heads the foundation"
            }
        ],
        "tags": ["integration", "community support", "diaspora"]
    },
    {
        "name": "Stand With Ukraine Foundation",
        "type": "organization",
        "city_id": 4,  # Warsaw
        "description": "A grassroots civil movement of Ukrainians in Warsaw born out of the 2013–14 Maidan. Advocates for Ukraine's freedom and EU integration, and organizes major solidarity actions in Poland.",
        "founding_year": 2014,
        "is_diaspora": True,
        "focus_areas": ["advocacy", "political_mobilization"],
        "key_figures": [
            {
                "name": "Natalia Panchenko",
                "role": "Founder & Leader",
                "description": "Founded and leads the diaspora activist movement and charity"
            }
        ],
        "tags": ["advocacy", "EU integration", "political mobilization"]
    }
]

def add_organizations():
    for i, org in enumerate(organizations):
        try:
            print(f"Adding organization: {org['name']}...")
            response = requests.post(API_URL, json=org)
            
            if response.status_code == 201:
                print(f"✅ Successfully added: {org['name']}")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"❌ Failed to add: {org['name']}. Status code: {response.status_code}")
                print(response.text)
            
            # Add a small delay between requests to avoid overwhelming the API
            if i < len(organizations) - 1:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error adding {org['name']}: {e}")
    
    print(f"\nAttempted to add {len(organizations)} organizations.")

if __name__ == "__main__":
    add_organizations() 