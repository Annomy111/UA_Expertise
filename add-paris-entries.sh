#!/bin/bash

# Stadt-IDs:
# 1 - Brussels
# 2 - Berlin
# 3 - Paris
# 4 - Warsaw

echo "Füge Pariser Organisationen und Experten hinzu..."

# Tatiana Kastueva-Jean
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Tatiana Kastueva-Jean",
  "type": "individual",
  "title": "Director, Russia/New Independent States Center",
  "affiliation": "French Institute of International Relations (IFRI)",
  "city_id": 3,
  "description": "Political scientist heading the Russia/NIS Center at the French Institute of International Relations in Paris. Research areas include Russia'"'"'s domestic and foreign policy and Ukraine. Provides analysis on Russia'"'"'s war in Ukraine and its global implications in French and international media.",
  "is_diaspora": false,
  "tags": ["Russia", "Ukraine", "foreign policy"],
  "focus_areas": ["research", "policy_analysis"]
}'

# Marie Dumoulin
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Marie Dumoulin",
  "type": "individual",
  "title": "Director, Wider Europe Programme",
  "affiliation": "European Council on Foreign Relations (ECFR)",
  "city_id": 3,
  "description": "Former French diplomat now leading ECFR'"'"'s Paris-based Wider Europe program. Focuses on Europe'"'"'s Eastern Neighbourhood and protracted conflicts. Co-authored European policy proposals on supporting Ukraine'"'"'s resilience and EU integration.",
  "is_diaspora": false,
  "tags": ["diplomacy", "Eastern Neighbourhood", "EU integration"],
  "focus_areas": ["policy_analysis", "research"]
}'

# Dr. Anna Colin Lebedev
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Dr. Anna Colin Lebedev",
  "type": "individual",
  "title": "Associate Professor",
  "affiliation": "Paris Nanterre University",
  "city_id": 3,
  "description": "Sociologist specializing in post-Soviet societies. Her research examines the social impact of conflicts in Ukraine and Russia. Since 2022, she has become a prominent public expert explaining the war'"'"'s historical and societal roots to French audiences. Author of Jamais Frères? Ukraine et Russie : une tragédie postsoviétique (2022).",
  "is_diaspora": true,
  "tags": ["sociology", "post-Soviet studies", "Ukraine-Russia relations"],
  "focus_areas": ["research", "education"]
}'

# Institut Français des Relations Internationales (IFRI)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Institut Français des Relations Internationales (IFRI)",
  "type": "organization",
  "city_id": 3,
  "description": "France'"'"'s leading independent research institute on international affairs, providing in-depth analysis and policy advice. IFRI'"'"'s Russia/NIS Center produces extensive research on the war in Ukraine, European security, and Eastern Europe, informing French policy and public debate.",
  "founding_year": 1979,
  "is_diaspora": false,
  "key_figures": [
    {"name": "Tatiana Kastueva-Jean", "role": "Director, Russia/NIS Center", "description": "Leads research on Ukraine and Russia"}
  ],
  "tags": ["think tank", "international relations", "European security"],
  "focus_areas": ["research", "policy_analysis"]
}'

# Association France–Ukraine
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Association France–Ukraine",
  "type": "organization",
  "city_id": 3,
  "description": "A Paris-based volunteer association (\"loi 1901\") dedicated to supporting the Ukrainian people amid Russia'"'"'s aggression. Mobilizes humanitarian aid shipments to Ukraine and assists Ukrainian refugees in France. Acts as a hub for French-Ukrainian solidarity efforts since 2014.",
  "founding_year": 2014,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Jean-Pierre Reymond", "role": "President", "description": "Coordinates humanitarian and solidarity actions"}
  ],
  "tags": ["humanitarian aid", "refugee support", "solidarity"],
  "focus_areas": ["humanitarian", "community_support"]
}'

# Union of Ukrainians in France (UDUF)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Union of Ukrainians in France (UDUF)",
  "type": "organization",
  "city_id": 3,
  "description": "The central umbrella organization of the Ukrainian diaspora in France, representing over 80,000 people. Founded by post-WWII émigrés, UDUF has long safeguarded Ukrainian culture and identity in France. Today it is a driving force in advocacy and public diplomacy: it leads rallies, memorials, and information campaigns across France.",
  "founding_year": 1949,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Bohdan Bilot", "role": "President", "description": "Historian and community leader"},
    {"name": "Volodymyr Kogutyak", "role": "Vice-President", "description": "Also VP at Ukrainian World Congress"}
  ],
  "tags": ["diaspora", "cultural preservation", "advocacy"],
  "focus_areas": ["advocacy", "cultural_diplomacy", "community_support"]
}'

# A Travers l'Europe
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "A Travers l'"'"'Europe",
  "type": "organization",
  "city_id": 3,
  "description": "A Paris-based humanitarian association (\"Across Europe\") created in 1999 to support vulnerable Ukrainians. Founded by Ukrainian expatriates including famed opera singer Vasyl Slipak, it initially promoted cultural ties, but Russia'"'"'s 2014 aggression refocused its work on aid. Sends regular shipments of donated supplies to Ukraine and hosts Ukrainian children for respite holidays in France.",
  "founding_year": 1999,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Alla Lazareva", "role": "President", "description": "Leads humanitarian efforts for Ukraine"},
    {"name": "Vasyl Slipak", "role": "Co-founder (deceased)", "description": "Opera singer who later died fighting for Ukraine"}
  ],
  "tags": ["humanitarian aid", "children", "cultural exchange"],
  "focus_areas": ["humanitarian", "cultural_diplomacy"]
}'

# Association des Femmes Ukrainiennes en France
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Association des Femmes Ukrainiennes en France",
  "type": "organization",
  "city_id": 3,
  "description": "A diaspora women-led charity focusing on humanitarian aid to Ukraine. Since 2022, it has sent critical supplies: ambulances, generators, medical gear, food and clothing to war zones. Works via a broad network of partners to reach all regions of Ukraine. Also assists Ukrainian women and children refugees in France.",
  "is_diaspora": true,
  "key_figures": [
    {"name": "Nadia Myhal", "role": "President", "description": "Coordinates aid shipments and refugee assistance"}
  ],
  "tags": ["women", "humanitarian aid", "refugee support"],
  "focus_areas": ["humanitarian", "community_support"]
}'

# Union of Ukrainians in Île-de-France (IDFU)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Union of Ukrainians in Île-de-France (IDFU)",
  "type": "organization",
  "city_id": 3,
  "description": "Regional association (est. 2000) promoting cultural, economic and humanitarian exchange between France and Ukraine. Encourages Franco-Ukrainian cultural projects and has actively participated in aid efforts during the war. Provides integration support for Ukrainian displaced persons around Paris.",
  "founding_year": 2000,
  "is_diaspora": true,
  "tags": ["cultural exchange", "humanitarian aid", "integration"],
  "focus_areas": ["cultural_diplomacy", "community_support", "humanitarian"]
}'

# Aide Médicale & Caritative France–Ukraine (AMCFU)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Aide Médicale & Caritative France–Ukraine (AMCFU)",
  "type": "organization",
  "city_id": 3,
  "description": "Founded in 2014 after the Maidan revolution, AMCFU is a Franco-Ukrainian initiative providing lifesaving aid to Ukraine. The association organizes a network of medical and humanitarian solidarity between France and Ukraine, delivering medical supplies, ambulances, and generators to war-torn regions. Since 2022, AMCFU has shipped over 2,000 tons of medical equipment and medicines to Ukrainian hospitals.",
  "founding_year": 2014,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Dr. Dmytro Atamanyuk", "role": "President", "description": "Coordinates medical aid efforts"}
  ],
  "tags": ["medical aid", "humanitarian", "healthcare"],
  "focus_areas": ["humanitarian"]
}'

echo "Hinzufügen der Pariser Einträge abgeschlossen." 