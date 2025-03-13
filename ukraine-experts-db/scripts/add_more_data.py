#!/usr/bin/env python3
import sys
import os
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the database utilities
import db_utils

def add_more_organizations():
    """Add more Ukrainian diaspora organizations to the database."""
    # Get city IDs
    cities = db_utils.get_all_cities()
    city_map = {city['name']: city['id'] for city in cities}
    
    # Additional organizations to add
    new_organizations = [
        # Brussels
        {
            "name": "Ukrainian Voices Refugee Committee",
            "type": "organization",
            "city_id": city_map["Brussels"],
            "description": "A committee representing Ukrainian refugees in Belgium, focused on advocacy and integration support. Its mission is to provide essential support, advocacy, and resources to Ukrainian refugees and to amplify their voices while preserving cultural heritage.",
            "is_diaspora": True,
            "founding_year": 2022,
            "focus_areas": ["advocacy", "community_support", "integration"],
            "contacts": [
                {"type": "website", "value": "refugee-committee.org", "is_primary": True}
            ],
            "key_figures": [],
            "tags": ["refugee support", "advocacy", "diaspora", "integration"]
        },
        # Berlin
        {
            "name": "Ukrainian Cultural Community in Berlin",
            "type": "organization",
            "city_id": city_map["Berlin"],
            "description": "A cultural diplomacy and support platform founded in Berlin in 2022 to assist displaced Ukrainian artists and preserve Ukrainian art in exile.",
            "is_diaspora": True,
            "founding_year": 2022,
            "focus_areas": ["cultural_diplomacy", "community_support"],
            "contacts": [
                {"type": "social_media", "value": "instagram.com/ucc_berlin", "is_primary": True}
            ],
            "key_figures": [
                {
                    "name": "Anastasiia Pasichnyk",
                    "role": "Founder & Director",
                    "description": "Artist and curator who established UCC Berlin to support compatriot artists forced to flee the war"
                }
            ],
            "tags": ["cultural diplomacy", "diaspora", "arts", "refugee support"]
        },
        {
            "name": "Ukrainian 'Ukr-Dim' Berlin",
            "type": "organization",
            "city_id": city_map["Berlin"],
            "description": "A community hub (launched 2020) providing information and support to Ukrainians in Berlin. Publishes Ukrainian-language guides on living in Germany, covering integration topics (housing, jobs, healthcare).",
            "is_diaspora": True,
            "founding_year": 2020,
            "focus_areas": ["community_support", "integration", "education"],
            "contacts": [
                {"type": "website", "value": "ukr-dim.de", "is_primary": True}
            ],
            "key_figures": [
                {
                    "name": "Dmytro Budnikov",
                    "role": "Coordinator",
                    "description": "Coordinates the community hub activities"
                }
            ],
            "tags": ["diaspora", "integration", "education", "community support"]
        },
        # Paris
        {
            "name": "Union of Ukrainians in Île-de-France",
            "type": "organization",
            "city_id": city_map["Paris"],
            "description": "Regional association (est. 2000) promoting cultural, economic and humanitarian exchange between France and Ukraine. Encourages Franco-Ukrainian cultural projects and has actively participated in aid efforts during the war.",
            "is_diaspora": True,
            "founding_year": 2000,
            "focus_areas": ["cultural_diplomacy", "humanitarian", "community_support"],
            "contacts": [],
            "key_figures": [],
            "tags": ["diaspora", "cultural diplomacy", "humanitarian aid", "Franco-Ukrainian relations"]
        },
        {
            "name": "France-Ukraine",
            "type": "organization",
            "city_id": city_map["Paris"],
            "description": "A nationwide friendship and aid association based in Paris. Coordinates relief efforts for Ukraine and assistance to refugees across France. Facilitates host family networks, job placement, and material donations via its platform.",
            "is_diaspora": True,
            "founding_year": None,
            "focus_areas": ["humanitarian", "cultural_diplomacy", "integration"],
            "contacts": [
                {"type": "website", "value": "france-ukraine.com", "is_primary": True}
            ],
            "key_figures": [
                {
                    "name": "Jean-Pierre Reymond",
                    "role": "President",
                    "description": "Leads the France-Ukraine association"
                }
            ],
            "tags": ["humanitarian aid", "refugee support", "cultural diplomacy", "Franco-Ukrainian relations"]
        },
        # Warsaw
        {
            "name": "Ukrainian Women's Club in Warsaw",
            "type": "organization",
            "city_id": city_map["Warsaw"],
            "description": "Support network for Ukrainian refugee women in Warsaw, providing community assistance, cultural activities, and integration support.",
            "is_diaspora": True,
            "founding_year": 2022,
            "focus_areas": ["community_support", "integration", "humanitarian"],
            "contacts": [],
            "key_figures": [],
            "tags": ["women", "diaspora", "refugee support", "community support"]
        }
    ]
    
    # Add each organization
    for org in new_organizations:
        try:
            org_id = db_utils.add_expert(org)
            print(f"Added organization: {org['name']} (ID: {org_id})")
        except Exception as e:
            print(f"Error adding {org['name']}: {e}")
    
    print("\nAdded additional organizations to the database.")

def add_more_experts():
    """Add more individual experts to the database."""
    # Get city IDs
    cities = db_utils.get_all_cities()
    city_map = {city['name']: city['id'] for city in cities}
    
    # Additional experts to add
    new_experts = [
        # Brussels
        {
            "name": "Dr. Svitlana Krasynska",
            "type": "individual",
            "title": "Research Fellow",
            "affiliation": "Centre for European Policy Studies (CEPS)",
            "city_id": city_map["Brussels"],
            "description": "Ukrainian researcher specializing in civil society development, democratization, and European integration. Her work focuses on Ukraine's reform processes and EU-Ukraine relations.",
            "is_diaspora": True,
            "focus_areas": ["research", "policy_analysis"],
            "tags": ["civil society", "EU integration", "democratization", "policy analysis"]
        },
        # Berlin
        {
            "name": "Dr. Sabine Fischer",
            "type": "individual",
            "title": "Senior Fellow",
            "affiliation": "German Institute for International and Security Affairs (SWP)",
            "city_id": city_map["Berlin"],
            "description": "Foreign policy expert at SWP specializing in Russia and post-Soviet conflicts. Researches Russia's war against Ukraine, EU–Russia relations, and unresolved conflicts in Eastern Europe. Adviser to the German government and prominent media voice during the Ukraine invasion.",
            "is_diaspora": False,
            "focus_areas": ["research", "policy_analysis"],
            "tags": ["Russia-Ukraine conflict", "EU-Russia relations", "security policy", "Eastern Europe"]
        },
        # Paris
        {
            "name": "Dr. Anna Colin Lebedev",
            "type": "individual",
            "title": "Associate Professor",
            "affiliation": "Paris Nanterre University",
            "city_id": city_map["Paris"],
            "description": "Sociologist specializing in post-Soviet societies. Her research examines the social impact of conflicts in Ukraine and Russia. Since 2022, she has become a prominent public expert explaining the war's historical and societal roots to French audiences. Author of 'Jamais Frères? Ukraine et Russie: une tragédie postsoviétique' (2022).",
            "is_diaspora": False,
            "focus_areas": ["research", "education"],
            "tags": ["sociology", "post-Soviet studies", "Ukraine-Russia relations", "conflict studies"]
        },
        # Warsaw
        {
            "name": "Maria Piechowska",
            "type": "individual",
            "title": "Analyst on Ukraine",
            "affiliation": "Polish Institute of International Affairs (PISM)",
            "city_id": city_map["Warsaw"],
            "description": "Researcher in PISM's Eastern Europe programme focusing on Ukraine. Covers Ukraine's foreign and domestic policy and socio-cultural issues, including Ukraine's reform progress and wartime society. Contributor to PISM reports on Ukraine's foreign strategy.",
            "is_diaspora": False,
            "focus_areas": ["research", "policy_analysis"],
            "tags": ["Ukraine foreign policy", "Ukraine reforms", "Eastern Europe", "policy analysis"]
        }
    ]
    
    # Add each expert
    for expert in new_experts:
        try:
            expert_id = db_utils.add_expert(expert)
            print(f"Added expert: {expert['name']} (ID: {expert_id})")
        except Exception as e:
            print(f"Error adding {expert['name']}: {e}")
    
    print("\nAdded additional experts to the database.")

if __name__ == "__main__":
    print("Adding more data to the Ukraine Experts Database...")
    add_more_organizations()
    add_more_experts()
    print("\nData addition completed successfully!") 