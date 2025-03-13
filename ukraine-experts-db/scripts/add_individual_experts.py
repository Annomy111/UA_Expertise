#!/usr/bin/env python3
import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000/experts"

# Sample individual experts data from the list
experts = [
    {
        "name": "Amanda Paul",
        "type": "individual",
        "title": "Senior Policy Analyst",
        "affiliation": "European Policy Centre (EPC)",
        "city_id": 1,  # Brussels
        "description": "Senior analyst focusing on Europe's Eastern flank (Ukraine, Moldova, South Caucasus) and Black Sea security; leads EPC's \"Ukraine's European Future\" project",
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {
                "type": "website",
                "value": "https://epc.eu/en/staff/Amanda-Paul~1c1a94",
                "is_primary": True
            }
        ],
        "tags": ["policy analysis", "Ukraine-EU relations", "security"]
    },
    {
        "name": "Dr. Olena Prystayko",
        "type": "individual",
        "title": "Executive Director",
        "affiliation": "Ukrainian Think Tanks Liaison Office in Brussels",
        "city_id": 1,  # Brussels
        "description": "Heads the Brussels liaison office that connects Ukrainian think tanks with EU policymakers. Former Council of Europe officer; co-author of Freedom House's Nations in Transit report on Ukraine",
        "is_diaspora": True,
        "focus_areas": ["advocacy", "policy_analysis", "research"],
        "contacts": [
            {
                "type": "website",
                "value": "https://bruegel.org/people/olena-prystayko",
                "is_primary": True
            }
        ],
        "tags": ["think tanks", "EU integration", "policy analysis"]
    },
    {
        "name": "Prof. Gwendolyn Sasse",
        "type": "individual",
        "title": "Director",
        "affiliation": "Centre for East European and International Studies (ZOiS)",
        "city_id": 2,  # Berlin
        "description": "Political scientist leading ZOiS (Berlin). Her research focuses on Eastern Europe – particularly Ukrainian politics and society – and EU enlargement. Author of Russia's War Against Ukraine (2023) and frequent commentator on Ukraine in European media",
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis", "education"],
        "contacts": [
            {
                "type": "website",
                "value": "https://www.zois-berlin.de/en/about-us/team/prof-dr-gwendolyn-sasse",
                "is_primary": True
            }
        ],
        "tags": ["research", "Ukraine politics", "EU enlargement"]
    },
    {
        "name": "Dr. Sabine Fischer",
        "type": "individual",
        "title": "Senior Fellow",
        "affiliation": "German Institute for International and Security Affairs (SWP)",
        "city_id": 2,  # Berlin
        "description": "Foreign policy expert at SWP specializing in Russia and post-Soviet conflicts. Researches Russia's war against Ukraine, EU–Russia relations, and unresolved conflicts in Eastern Europe. Adviser to the German government and prominent media voice during the Ukraine invasion.",
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {
                "type": "website",
                "value": "https://www.swp-berlin.org/en/researcher/sabine-fischer",
                "is_primary": True
            }
        ],
        "tags": ["Russia-Ukraine conflict", "EU policy", "security"]
    },
    {
        "name": "Tatiana Kastueva-Jean",
        "type": "individual",
        "title": "Director",
        "affiliation": "Russia/New Independent States Center, IFRI",
        "city_id": 3,  # Paris
        "description": "Political scientist heading the Russia/NIS Center at the French Institute of International Relations in Paris. Research areas include Russia's domestic and foreign policy and Ukraine. Provides analysis on Russia's war in Ukraine and its global implications in French and international media",
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {
                "type": "website",
                "value": "https://www.ifri.org/en/about/team/tatiana-kastueva-jean",
                "is_primary": True
            }
        ],
        "tags": ["Russia-Ukraine relations", "policy analysis", "French foreign policy"]
    },
    {
        "name": "Dr. Anna Colin Lebedev",
        "type": "individual",
        "title": "Associate Professor",
        "affiliation": "Paris Nanterre University",
        "city_id": 3,  # Paris
        "description": "Sociologist specializing in post-Soviet societies. Her research examines the social impact of conflicts in Ukraine and Russia. Since 2022, she has become a prominent public expert explaining the war's historical and societal roots to French audiences. Author of Jamais Frères? Ukraine et Russie : une tragédie postsoviétique (2022).",
        "is_diaspora": False,
        "focus_areas": ["research", "education"],
        "contacts": [
            {
                "type": "website",
                "value": "https://www.lagency.org/anna-colin-lebedev",
                "is_primary": True
            }
        ],
        "tags": ["sociology", "Ukraine-Russia relations", "post-Soviet studies"]
    },
    {
        "name": "Wojciech Konończuk",
        "type": "individual",
        "title": "Director",
        "affiliation": "Centre for Eastern Studies (OSW)",
        "city_id": 4,  # Warsaw
        "description": "Seasoned analyst heading OSW in Warsaw. Formerly led OSW's department on Ukraine, Belarus, and Moldova, he specializes in the political and economic dynamics of Eastern Europe and Russia–Ukraine relations. Regularly briefs Polish authorities and media on developments in Ukraine",
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {
                "type": "website",
                "value": "https://www.osw.waw.pl/en/eksperci/wojciech-kononczuk",
                "is_primary": True
            }
        ],
        "tags": ["Eastern Europe", "policy analysis", "Ukraine politics"]
    },
    {
        "name": "Maria Piechowska",
        "type": "individual",
        "title": "Analyst on Ukraine",
        "affiliation": "Polish Institute of International Affairs (PISM)",
        "city_id": 4,  # Warsaw
        "description": "Researcher in PISM's Eastern Europe programme focusing on Ukraine. Covers Ukraine's foreign and domestic policy and socio-cultural issues, including Ukraine's reform progress and wartime society. Contributor to PISM reports on Ukraine's foreign strategy.",
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {
                "type": "website",
                "value": "https://www.pism.pl/experts/maria-piechowska",
                "is_primary": True
            }
        ],
        "tags": ["Ukraine reforms", "policy analysis", "Eastern Europe"]
    }
]

def add_experts():
    for i, expert in enumerate(experts):
        try:
            print(f"Adding expert: {expert['name']}...")
            response = requests.post(API_URL, json=expert)
            
            if response.status_code == 201:
                print(f"✅ Successfully added: {expert['name']}")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"❌ Failed to add: {expert['name']}. Status code: {response.status_code}")
                print(response.text)
            
            # Add a small delay between requests to avoid overwhelming the API
            if i < len(experts) - 1:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error adding {expert['name']}: {e}")
    
    print(f"\nAttempted to add {len(experts)} individual experts.")

if __name__ == "__main__":
    add_experts() 