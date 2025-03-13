#!/bin/bash

# Mehr Organisationen hinzufügen
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Ukrainian Institute Berlin",
  "type": "organization",
  "city_id": 4,
  "description": "The Ukrainian Institute Berlin promotes Ukrainian culture and fosters German-Ukrainian dialogue through exhibitions, lectures, and cultural events.",
  "founding_year": 2015,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Olena Schmidt", "role": "Director", "description": "Cultural manager with over 10 years of experience"}
  ],
  "tags": ["cultural diplomacy", "arts", "education"],
  "focus_areas": ["cultural_diplomacy", "community_support"]
}'

curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Ukraine Crisis Media Center",
  "type": "organization",
  "city_id": 1,
  "description": "UCMC provides information about events in Ukraine, challenges of Russian disinformation, and promotes Ukrainian interests internationally.",
  "founding_year": 2014,
  "is_diaspora": false,
  "key_figures": [
    {"name": "Natalia Popovych", "role": "Co-founder", "description": "Communications expert and civic activist"}
  ],
  "tags": ["media", "information warfare", "advocacy"],
  "focus_areas": ["advocacy", "research", "policy_analysis"]
}'

curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Razom for Ukraine",
  "type": "organization",
  "city_id": 3,
  "description": "Razom means \"together\" in Ukrainian. The organization was founded during the Revolution of Dignity to support the people of Ukraine.",
  "founding_year": 2014,
  "is_diaspora": true,
  "key_figures": [
    {"name": "Maryna Prykhodko", "role": "President", "description": "Ukrainian-American activist"}
  ],
  "tags": ["humanitarian aid", "advocacy", "civil society"],
  "focus_areas": ["humanitarian", "advocacy", "community_support"]
}'

curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Ukrainian Helsinki Human Rights Union",
  "type": "organization",
  "city_id": 2,
  "description": "UHHRU works to protect and promote human rights in Ukraine through monitoring, advocacy, and legal assistance.",
  "founding_year": 2004,
  "is_diaspora": false,
  "key_figures": [
    {"name": "Oleksandr Pavlichenko", "role": "Executive Director", "description": "Human rights defender with extensive experience"}
  ],
  "tags": ["human rights", "legal assistance", "advocacy"],
  "focus_areas": ["advocacy", "research", "policy_analysis"]
}'

# Mehr Einzelpersonen hinzufügen
curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Olena Halushka",
  "type": "individual",
  "title": "Anti-corruption expert",
  "affiliation": "Anti-Corruption Action Center",
  "city_id": 1,
  "description": "Olena is a board member of the Anti-Corruption Action Center and an expert on anti-corruption reforms in Ukraine.",
  "is_diaspora": false,
  "tags": ["anti-corruption", "governance", "reforms"],
  "focus_areas": ["advocacy", "policy_analysis"]
}'

curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Dmytro Kuleba",
  "type": "individual",
  "title": "Foreign Policy Expert",
  "affiliation": "Former Minister of Foreign Affairs of Ukraine",
  "city_id": 1,
  "description": "Dmytro is a diplomat and foreign policy expert with extensive experience in international relations.",
  "is_diaspora": false,
  "tags": ["diplomacy", "foreign policy", "international relations"],
  "focus_areas": ["policy_analysis", "advocacy"]
}'

curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Yaroslav Hrytsak",
  "type": "individual",
  "title": "Historian",
  "affiliation": "Ukrainian Catholic University",
  "city_id": 2,
  "description": "Yaroslav is a prominent Ukrainian historian specializing in the history of Ukraine and Eastern Europe.",
  "is_diaspora": false,
  "tags": ["history", "education", "research"],
  "focus_areas": ["research", "education"]
}'

curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Svitlana Krakovska",
  "type": "individual",
  "title": "Climate Scientist",
  "affiliation": "Ukrainian Hydrometeorological Institute",
  "city_id": 3,
  "description": "Svitlana is a leading climate scientist and Ukraine'"'"'s representative to the IPCC.",
  "is_diaspora": true,
  "tags": ["climate change", "environmental policy", "science"],
  "focus_areas": ["research", "policy_analysis"]
}'

curl -X POST http://localhost:8000/experts -H "Content-Type: application/json" -d '{
  "name": "Serhiy Plokhii",
  "type": "individual",
  "title": "Professor of Ukrainian History",
  "affiliation": "Harvard University",
  "city_id": 4,
  "description": "Serhiy is a leading authority on Ukraine, Russia, and Eastern Europe and the author of several award-winning books.",
  "is_diaspora": true,
  "tags": ["history", "education", "research"],
  "focus_areas": ["research", "education"]
}'

echo "Added 10 more experts to the database." 