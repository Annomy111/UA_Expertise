#!/bin/bash

# Stadt-IDs:
# 1 - Brussels
# 2 - Berlin
# 3 - Paris
# 4 - Warsaw

echo "Füge Warschauer Organisationen und Experten hinzu..."

# Wojciech Konończuk
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Wojciech Konończuk",
  "type": "individual",
  "title": "Director",
  "affiliation": "Centre for Eastern Studies (OSW)",
  "city_id": 4,
  "description": "Seasoned analyst heading OSW in Warsaw. Formerly led OSW'"'"'s department on Ukraine, Belarus, and Moldova, he specializes in the political and economic dynamics of Eastern Europe and Russia–Ukraine relations. Regularly briefs Polish authorities and media on developments in Ukraine.",
  "is_diaspora": false,
  "tags": ["Eastern Europe", "foreign policy", "Russia-Ukraine relations"],
  "focus_areas": ["research", "policy_analysis"]
}'

# Maria Piechowska
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Maria Piechowska",
  "type": "individual",
  "title": "Analyst on Ukraine",
  "affiliation": "Polish Institute of International Affairs (PISM)",
  "city_id": 4,
  "description": "Researcher in PISM'"'"'s Eastern Europe programme focusing on Ukraine. Covers Ukraine'"'"'s foreign and domestic policy and socio-cultural issues, including Ukraine'"'"'s reform progress and wartime society. Contributor to PISM reports on Ukraine'"'"'s foreign strategy.",
  "is_diaspora": false,
  "tags": ["Ukraine policy", "reforms", "society"],
  "focus_areas": ["research", "policy_analysis"]
}'

# Piotr Buras
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Piotr Buras",
  "type": "individual",
  "title": "Director, ECFR Warsaw Office",
  "affiliation": "European Council on Foreign Relations",
  "city_id": 4,
  "description": "Head of the European Council on Foreign Relations in Warsaw and a leading foreign policy thinker. Analyses European policy vis-à-vis Poland and Ukraine – argues that Central Europe, amid Ukraine'"'"'s fight, is now shaping the future of the continent. Co-authored plans for Ukraine'"'"'s EU accession and security integration.",
  "is_diaspora": false,
  "tags": ["EU policy", "European security", "EU accession"],
  "focus_areas": ["policy_analysis", "research"]
}'

# Centre for Eastern Studies (OSW)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Centre for Eastern Studies (OSW)",
  "type": "organization",
  "city_id": 4,
  "description": "Warsaw-based think tank (est. 1990) conducting independent research on the political, economic and social situations in Central and Eastern Europe, with special focus on Russia and Ukraine. OSW'"'"'s analyses of the war in Ukraine inform Polish government policy and media coverage.",
  "founding_year": 1990,
  "is_diaspora": false,
  "key_figures": [
    {"name": "Wojciech Konończuk", "role": "Director", "description": "Expert on Ukraine and Eastern Europe"}
  ],
  "tags": ["think tank", "Eastern Europe", "security policy"],
  "focus_areas": ["research", "policy_analysis"]
}'

# Polish Institute of International Affairs (PISM)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Polish Institute of International Affairs (PISM)",
  "type": "organization",
  "city_id": 4,
  "description": "A leading Warsaw-based institute founded by the Polish government in 1996 to study international affairs. Produces analyses and forecasts on issues affecting Poland'"'"'s security – including extensive work on transatlantic support for Ukraine and implications of Russia'"'"'s war – to advise policymakers and engage the public.",
  "founding_year": 1996,
  "is_diaspora": false,
  "key_figures": [
    {"name": "Maria Piechowska", "role": "Ukraine Analyst", "description": "Researcher specializing in Ukrainian affairs"}
  ],
  "tags": ["think tank", "international affairs", "security policy"],
  "focus_areas": ["research", "policy_analysis"]
}'

# Nasz Wybór Foundation
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Nasz Wybór Foundation – Ukrainian House in Warsaw",
  "type": "organization",
  "city_id": 4,
  "description": "Founded in 2009 by Ukrainian immigrants, Fundacja \"Nasz Wybór\" (\"Our Choice\") runs the Ukrainian House in Warsaw, a cultural and assistance center for Poland'"'"'s large Ukrainian community. Historian Myroslava Keryk leads efforts to integrate Ukrainian refugees and migrant workers into Polish society while preserving their identity. The foundation provides Polish language classes, job counseling, legal advice, and a welcome space for newcomers.",
  "founding_year": 2009,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Myroslava Keryk", "role": "President", "description": "Historian and community leader bridging Ukrainian diaspora with Polish society"}
  ],
  "tags": ["diaspora", "integration", "community support"],
  "focus_areas": ["community_support", "integration", "advocacy"]
}'

# Stand With Ukraine (Euromaidan-Warszawa)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Stand With Ukraine (Euromaidan-Warszawa)",
  "type": "organization",
  "city_id": 4,
  "description": "An outgrowth of the 2014 Euromaidan protests, this Warsaw-based diaspora movement has been promoting Ukraine'"'"'s EU integration and mobilizing political support in Poland. After 2022, Panchenko formally established Stand With Ukraine as a foundation to scale up its volunteer efforts. The group organizes rallies, awareness campaigns, and policy advocacy, and provides direct aid to refugees.",
  "founding_year": 2014,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Natalia Panchenko", "role": "Founder & Leader", "description": "Prominent voice for Ukrainian causes in Poland"},
    {"name": "Mykola Petryga", "role": "Coordinator", "description": "Coordinates protest actions and advocacy campaigns"}
  ],
  "tags": ["diaspora activism", "EU integration", "civil society"],
  "focus_areas": ["advocacy", "political_mobilization", "community_support"]
}'

# Union of Ukrainians in Poland (ZUwP)
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Union of Ukrainians in Poland (ZUwP)",
  "type": "organization",
  "city_id": 4,
  "description": "ZUwP was established in 1990 as the representative body for Poland'"'"'s historic Ukrainian minority (communities resettled post-WWII). It focuses on preserving Ukrainian language, culture, and minority rights in Poland. The Union operates Ukrainian cultural centers and Saturday schools, organizes festivals, and maintains media in Ukrainian. Since 2022, ZUwP has also coordinated relief for war refugees.",
  "founding_year": 1990,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Mirosław Skórka", "role": "President", "description": "Leads ZUwP since 2021, advocating for Ukrainian minority rights"},
    {"name": "Piotr Tyma", "role": "Former President (2006-2021)", "description": "Long-term leader of Ukraine-Polish relations"}
  ],
  "tags": ["cultural preservation", "minority rights", "diaspora"],
  "focus_areas": ["cultural_diplomacy", "community_support", "advocacy"]
}'

# Ukrainian Women's Club in Warsaw
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Ukrainian Women'"'"'s Club in Warsaw",
  "type": "organization",
  "city_id": 4,
  "description": "A support network for Ukrainian women refugees in Warsaw, focusing on integration, psychological support, and professional development. Provides a safe space for Ukrainian women to connect, share experiences, and access resources while adjusting to life in Poland. Organizes workshops, social events, and mentoring programs to help women overcome the trauma of war and displacement.",
  "founding_year": 2022,
  "is_diaspora": true,
  "tags": ["women", "refugee support", "integration"],
  "focus_areas": ["community_support", "integration"]
}'

echo "Hinzufügen der Warschauer Einträge abgeschlossen." 