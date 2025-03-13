#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime

# API endpoint
API_URL = "http://localhost:8000/experts"

# List of previously added organizations to avoid duplicates
EXISTING_ORGANIZATIONS = [
    "Vitsche e.V.",
    "Promote Ukraine",
    "BEforUkraine",
    "Alliance of Ukrainian Organizations",
    "Ukrainian Cultural Community in Berlin",
    "Association des Femmes Ukrainiennes en France",
    "Union of Ukrainians in France",
    "Fundacja \"Nasz Wybór\"",
    "Stand With Ukraine Foundation",
    "Ukrainian Society of Switzerland",
    "Ukrainian-Danish Youth House",
    "Ukrainian Community in the Czech Republic",
    "Ukrainian Helsinki Human Rights Union",
    "Ukrainian Institute London",
    "Ukrainian Welcome Center",
    "Ukrainian House in Warsaw",
    "Ukrainian Cultural Association in Spain",
    "Ukrainian Society of Austria",
    "Ukrainian Community in Belgium",
    "Ukrainian Cultural Center in Stockholm",
    "Kiron Open Higher Education",
    "CineMova",
    "European Policy Centre (EPC)",
    "Caritas Migrant Center",
    "Comité d'entraide ukrainienne",
    "UA Transformation Lab",
    "Razumkov Centre",
    "European Council on Foreign Relations (ECFR)",
    "Chatham House (Royal Institute of International Affairs)",
    "Centre for European Policy Studies (CEPS)",
    "German Council on Foreign Relations (DGAP)",
    "New Europe Center",
    "Polish Institute of International Affairs (PISM)",
    "International Crisis Group - Europe & Central Asia"
]

# City IDs mapping - updated based on actual database values
CITY_IDS = {
    "Berlin": 2,
    "Brussels": 1,
    "Paris": 3,
    "Warsaw": 4,
    "London": 1,  # Using Brussels as a fallback since London doesn't exist
    "Rome": 3,    # Using Paris as a fallback since Rome doesn't exist
    "Madrid": 3,  # Using Paris as a fallback since Madrid doesn't exist
    "Sofia": 2,   # Using Berlin as a fallback since Sofia doesn't exist
    "Kiel": 2,    # Using Berlin as a fallback since Kiel doesn't exist
    "Stockholm": 2 # Using Berlin as a fallback since Stockholm doesn't exist
}

# European think tanks focused on Ukraine
think_tanks = [
    {
        "name": "European Council on Foreign Relations (ECFR)",
        "type": "organization",
        "city_id": CITY_IDS["Berlin"],
        "description": "The European Council on Foreign Relations (ECFR) is an award-winning international think-tank that conducts cutting-edge independent research on European foreign and security policy, with a significant focus on Ukraine and Eastern Europe. ECFR's Wider Europe programme specifically addresses Ukraine-Russia relations and EU policy towards its eastern neighborhood. The organization provides a platform for decision-makers, activists, and influencers to share ideas and build coalitions for change at the European level.",
        "founding_year": 2007,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis", "advocacy"],
        "contacts": [
            {"type": "website", "value": "https://ecfr.eu", "is_primary": True},
            {"type": "email", "value": "berlin@ecfr.eu", "is_primary": False},
            {"type": "phone", "value": "+49 30 32505100", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/ecfr", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/ECFRthinktank", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/european-council-on-foreign-relations", "is_primary": False},
            {"type": "instagram", "value": "https://www.instagram.com/ecfr_eu", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Mark Leonard",
                "role": "Director and Co-founder",
                "description": "Expert on European foreign policy and international relations"
            },
            {
                "name": "Marie Dumoulin",
                "role": "Director of Wider Europe Programme",
                "description": "Specialist on Ukraine, Russia, and Eastern Europe"
            }
        ],
        "tags": ["think tank", "foreign policy", "EU policy", "security", "Ukraine research", "Russia relations"],
        "links": [
            {
                "title": "ECFR Logo",
                "url": "https://ecfr.eu/wp-content/themes/ecfr/assets/images/ecfr-logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Chatham House (Royal Institute of International Affairs)",
        "type": "organization",
        "city_id": CITY_IDS["London"],  # Now using Brussels as fallback
        "description": "Chatham House, also known as the Royal Institute of International Affairs, is a world-leading policy institute based in London. Its Russia and Eurasia Programme conducts extensive research on Ukraine, focusing on governance reform, conflict resolution, and Ukraine's relations with the EU, NATO, and Russia. The institute regularly publishes reports, briefings, and analyses on Ukraine's political developments, security challenges, and economic reforms.",
        "founding_year": 1920,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {"type": "website", "value": "https://www.chathamhouse.org", "is_primary": True},
            {"type": "email", "value": "contact@chathamhouse.org", "is_primary": False},
            {"type": "phone", "value": "+44 20 7957 5700", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/ChathamHouse", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/ChathamHouse", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/chatham-house", "is_primary": False},
            {"type": "instagram", "value": "https://www.instagram.com/chathamhouse", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Orysia Lutsevych",
                "role": "Head, Ukraine Forum",
                "description": "Research Fellow and Manager of the Ukraine Forum in the Russia and Eurasia Programme"
            }
        ],
        "tags": ["think tank", "international affairs", "Ukraine research", "Russia relations", "policy analysis"],
        "links": [
            {
                "title": "Chatham House Logo",
                "url": "https://www.chathamhouse.org/themes/custom/chatham/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Centre for European Policy Studies (CEPS)",
        "type": "organization",
        "city_id": CITY_IDS["Brussels"],
        "description": "The Centre for European Policy Studies (CEPS) is one of Europe's leading think tanks on EU affairs, with significant research on Ukraine's European integration, reforms, and security challenges. CEPS has been actively involved in analyzing the EU-Ukraine Association Agreement, visa liberalization, and Ukraine's reform process. The think tank regularly organizes events and publishes policy papers on Ukraine's path to EU membership and the challenges it faces.",
        "founding_year": 1983,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis", "advocacy"],
        "contacts": [
            {"type": "website", "value": "https://www.ceps.eu", "is_primary": True},
            {"type": "email", "value": "info@ceps.eu", "is_primary": False},
            {"type": "phone", "value": "+32 2 229 39 11", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/CEPS_thinktank", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/CEPS.thinktank", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/centre-for-european-policy-studies", "is_primary": False},
            {"type": "youtube", "value": "https://www.youtube.com/user/CEPSTHINKTANK", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Steven Blockmans",
                "role": "Director of Research",
                "description": "Expert on EU foreign policy and EU-Ukraine relations"
            }
        ],
        "tags": ["think tank", "EU policy", "European integration", "Ukraine reforms", "policy analysis"],
        "links": [
            {
                "title": "CEPS Logo",
                "url": "https://www.ceps.eu/wp-content/uploads/2018/08/CEPS-Logo.png",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "German Council on Foreign Relations (DGAP)",
        "type": "organization",
        "city_id": CITY_IDS["Berlin"],
        "description": "The German Council on Foreign Relations (DGAP) is a network for foreign policy expertise in Germany with significant research on Ukraine, Russia, and Eastern Europe. DGAP's Eastern Europe program focuses on Ukraine's reform process, security challenges, and relations with the EU and NATO. The think tank provides policy recommendations to German and European decision-makers on Ukraine policy and regularly organizes events with Ukrainian experts and officials.",
        "founding_year": 1955,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {"type": "website", "value": "https://dgap.org", "is_primary": True},
            {"type": "email", "value": "info@dgap.org", "is_primary": False},
            {"type": "phone", "value": "+49 30 25 42 31-0", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/dgapev", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/dgapev", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/dgap", "is_primary": False},
            {"type": "instagram", "value": "https://www.instagram.com/dgap_ev", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Stefan Meister",
                "role": "Head of Program, Eastern Europe, Russia and Central Asia",
                "description": "Expert on Russian-Ukrainian relations and post-Soviet politics"
            }
        ],
        "tags": ["think tank", "foreign policy", "Germany-Ukraine relations", "security policy", "Eastern Europe"],
        "links": [
            {
                "title": "DGAP Logo",
                "url": "https://dgap.org/sites/default/files/styles/teaser_image_full_view/public/DGAP_Logo_RGB.png",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "New Europe Center",
        "type": "organization",
        "city_id": CITY_IDS["Warsaw"],
        "description": "The New Europe Center is a Ukrainian think tank focused on foreign policy and security studies. It analyzes Ukraine's relations with the EU, NATO, and other international partners, as well as Ukraine's reform process and security challenges. The center conducts research, organizes public events, and provides policy recommendations to Ukrainian and international stakeholders. It has been particularly active in promoting Ukraine's European integration and NATO membership.",
        "founding_year": 2017,
        "is_diaspora": True,
        "focus_areas": ["research", "policy_analysis", "advocacy"],
        "contacts": [
            {"type": "website", "value": "http://neweurope.org.ua/en/", "is_primary": True},
            {"type": "email", "value": "info@neweurope.org.ua", "is_primary": False},
            {"type": "phone", "value": "+380 44 287 7611", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/NEC_Ukraine", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/NECUkraine", "is_primary": False},
            {"type": "address", "value": "Vozdvyzhenska Street, 10A, Kyiv, 04071", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Alyona Getmanchuk",
                "role": "Director",
                "description": "Expert on Ukraine's foreign policy and European integration"
            },
            {
                "name": "Marianna Fakhurdinova",
                "role": "Associate Fellow",
                "description": "Researcher on Ukraine-EU relations"
            }
        ],
        "tags": ["think tank", "Ukraine foreign policy", "European integration", "NATO", "policy analysis"],
        "links": [
            {
                "title": "New Europe Center Logo",
                "url": "http://neweurope.org.ua/wp-content/themes/new-europe/assets/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Polish Institute of International Affairs (PISM)",
        "type": "organization",
        "city_id": CITY_IDS["Warsaw"],
        "description": "The Polish Institute of International Affairs (PISM) is a leading research institution in Central Europe that conducts extensive research on Ukraine, focusing on its security challenges, relations with Russia, and European integration. PISM regularly publishes analyses on Ukraine's reform process, the conflict in eastern Ukraine, and Poland-Ukraine relations. The institute provides policy recommendations to Polish and European decision-makers on Ukraine policy.",
        "founding_year": 1947,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {"type": "website", "value": "https://www.pism.pl/en", "is_primary": True},
            {"type": "email", "value": "pism@pism.pl", "is_primary": False},
            {"type": "phone", "value": "+48 22 556 80 00", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/PISM_Poland", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/PISM.Poland", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/the-polish-institute-of-international-affairs", "is_primary": False},
            {"type": "address", "value": "ul. Warecka 1a, 00-950 Warsaw, Poland", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Sławomir Dębski",
                "role": "Director",
                "description": "Expert on Eastern European politics and security"
            }
        ],
        "tags": ["think tank", "international affairs", "Poland-Ukraine relations", "security policy", "Eastern Europe"],
        "links": [
            {
                "title": "PISM Logo",
                "url": "https://www.pism.pl/themes/pism/images/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "International Crisis Group - Europe & Central Asia",
        "type": "organization",
        "city_id": CITY_IDS["Brussels"],
        "description": "The International Crisis Group is a global organization working to prevent wars and shape policies that build a more peaceful world. Its Europe & Central Asia program conducts extensive research on Ukraine, focusing on conflict resolution in eastern Ukraine, Ukraine's reform process, and relations with Russia. The organization regularly publishes reports and briefings on Ukraine's security challenges and provides policy recommendations to international stakeholders.",
        "founding_year": 1995,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis", "advocacy"],
        "contacts": [
            {"type": "website", "value": "https://www.crisisgroup.org/europe-central-asia/eastern-europe/ukraine", "is_primary": True},
            {"type": "email", "value": "brussels@crisisgroup.org", "is_primary": False},
            {"type": "phone", "value": "+32 2 502 90 38", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/CrisisGroup", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/crisisgroup", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/international-crisis-group", "is_primary": False},
            {"type": "instagram", "value": "https://www.instagram.com/crisisgroup", "is_primary": False},
            {"type": "address", "value": "235 Avenue Louise, 1050 Brussels, Belgium", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Olga Oliker",
                "role": "Program Director, Europe and Central Asia",
                "description": "Expert on security issues in Ukraine, Russia, and the post-Soviet states"
            }
        ],
        "tags": ["think tank", "conflict resolution", "security policy", "Ukraine conflict", "international affairs"],
        "links": [
            {
                "title": "ICG Logo",
                "url": "https://www.crisisgroup.org/themes/custom/icg/logo.svg",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Kiel Institute for the World Economy - Ukraine Support Tracker",
        "type": "organization",
        "city_id": CITY_IDS["Kiel"],
        "description": "The Kiel Institute for the World Economy is a leading international economic research institution and think tank. Their Ukraine Support Tracker project quantifies the scale of military, financial, and humanitarian aid to Ukraine from Western governments. The database provides a comprehensive overview of support measures, making them comparable across donor countries. It covers 41 countries, including EU member states, G7 members, and other nations, focusing on government-to-government transfers to Ukraine since January 2022.",
        "founding_year": 1914,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {"type": "website", "value": "https://www.ifw-kiel.de/topics/war-against-ukraine/ukraine-support-tracker/", "is_primary": True},
            {"type": "email", "value": "ukrainetracker@ifw-kiel.de", "is_primary": False},
            {"type": "phone", "value": "+49 431 8814-1", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/kielinstitute", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/kielinstitute", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/kiel-institute-for-the-world-economy", "is_primary": False},
            {"type": "youtube", "value": "https://www.youtube.com/user/ifwkiel", "is_primary": False},
            {"type": "address", "value": "Kiellinie 66, 24105 Kiel, Germany", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Christoph Trebesch",
                "role": "Director and Lead Researcher, Ukraine Support Tracker",
                "description": "Expert on international finance and Ukraine support analysis"
            },
            {
                "name": "Giuseppe Irto",
                "role": "Researcher, Ukraine Support Tracker",
                "description": "Analyst focusing on quantifying international aid to Ukraine"
            },
            {
                "name": "Taro Nishikawa",
                "role": "Researcher, Ukraine Support Tracker",
                "description": "Analyst focusing on quantifying international aid to Ukraine"
            }
        ],
        "tags": ["think tank", "Ukraine support", "economic research", "aid tracking", "policy analysis", "data analysis"],
        "links": [
            {
                "title": "Kiel Institute Logo",
                "url": "https://www.ifw-kiel.de/fileadmin/Dateiverwaltung/IfW-Logo/ifw_logo.png",
                "description": "Organization logo"
            }
        ]
    },
    {
        "name": "Stockholm International Peace Research Institute (SIPRI)",
        "type": "organization",
        "city_id": CITY_IDS["Stockholm"],
        "description": "The Stockholm International Peace Research Institute (SIPRI) is an independent international institute dedicated to research into conflict, armaments, arms control, and disarmament. SIPRI provides data, analysis, and recommendations based on open sources. Their research on Ukraine focuses on the security implications of the Russia-Ukraine conflict, arms transfers to Ukraine, and the broader impact on European security architecture. SIPRI's databases and publications are widely used by policymakers, researchers, and media worldwide.",
        "founding_year": 1966,
        "is_diaspora": False,
        "focus_areas": ["research", "policy_analysis"],
        "contacts": [
            {"type": "website", "value": "https://www.sipri.org", "is_primary": True},
            {"type": "email", "value": "sipri@sipri.org", "is_primary": False},
            {"type": "phone", "value": "+46 8 655 97 00", "is_primary": False},
            {"type": "twitter", "value": "https://twitter.com/SIPRIorg", "is_primary": False},
            {"type": "facebook", "value": "https://www.facebook.com/sipri.org", "is_primary": False},
            {"type": "linkedin", "value": "https://www.linkedin.com/company/stockholm-international-peace-research-institute", "is_primary": False},
            {"type": "youtube", "value": "https://www.youtube.com/user/SIPRIorg", "is_primary": False},
            {"type": "address", "value": "Signalistgatan 9, SE-169 72 Solna, Sweden", "is_primary": False}
        ],
        "key_figures": [
            {
                "name": "Dan Smith",
                "role": "Director",
                "description": "Expert on peace and conflict issues, including the Ukraine conflict"
            },
            {
                "name": "Ian Anthony",
                "role": "Director of European Security Programme",
                "description": "Expert on European security issues, including Ukraine-Russia relations"
            }
        ],
        "tags": ["think tank", "peace research", "security policy", "arms control", "conflict analysis", "Ukraine conflict"],
        "links": [
            {
                "title": "SIPRI Logo",
                "url": "https://www.sipri.org/sites/default/files/SIPRI-Logo.png",
                "description": "Organization logo"
            }
        ]
    }
]

def add_think_tanks():
    """Add European think tanks to the database."""
    print(f"Attempting to add {len(think_tanks)} European think tanks to the database...")
    
    added_count = 0
    skipped_count = 0
    
    for think_tank in think_tanks:
        # Check if organization already exists
        if think_tank["name"] in EXISTING_ORGANIZATIONS:
            print(f"Skipping {think_tank['name']} - already exists in database")
            skipped_count += 1
            continue
        
        # Send POST request to API
        try:
            response = requests.post(API_URL, json=think_tank)
            
            # Check if request was successful (both 200 and 201 are success codes)
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"Added {think_tank['name']} successfully with ID: {result['id']}")
                added_count += 1
            else:
                print(f"Failed to add {think_tank['name']}: {response.status_code} - {response.text}")
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error adding {think_tank['name']}: {str(e)}")
    
    print(f"\nSummary:")
    print(f"- Total think tanks attempted: {len(think_tanks)}")
    print(f"- Successfully added: {added_count}")
    print(f"- Skipped (already exist): {skipped_count}")

if __name__ == "__main__":
    add_think_tanks() 