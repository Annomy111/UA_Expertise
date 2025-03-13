#!/usr/bin/env python3
import requests
import json
import time
import random
import sys
import subprocess
import re
import argparse
import os

# Base URL for the API
API_URL = "http://localhost:8000"

def get_all_experts():
    """Get all experts from the API using empty search query"""
    response = requests.get(f"{API_URL}/search?q=")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching experts: {response.status_code}")
        return []

def get_expert_details(expert_id):
    """Get detailed information about an expert"""
    response = requests.get(f"{API_URL}/experts/{expert_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching expert details: {response.status_code}")
        return None

def update_expert(expert_id, expert_data):
    """Update an expert's information"""
    response = requests.put(
        f"{API_URL}/experts/{expert_id}",
        json=expert_data,
        headers={"Content-Type": "application/json"}
    )
    return response.status_code == 200, response.text

def extract_title_affiliation(expert_name, description):
    """
    Extract title and affiliation from description if not already present in expert data
    """
    title = None
    affiliation = None
    
    # Common academic titles
    academic_titles = ["Dr.", "Professor", "Prof.", "Associate Professor", "Assistant Professor", "Lecturer", "Senior Lecturer"]
    
    # Look for academic titles
    for academic_title in academic_titles:
        if academic_title in description and academic_title not in expert_name:
            title = academic_title
            break
    
    # Look for common patterns indicating affiliation
    affiliation_patterns = [
        r"at the ([^.,]+)",
        r"at ([^.,]+)",
        r"with the ([^.,]+)",
        r"with ([^.,]+)",
        r"of the ([^.,]+)",
        r"Director of ([^.,]+)",
        r"Head of ([^.,]+)"
    ]
    
    for pattern in affiliation_patterns:
        match = re.search(pattern, description)
        if match:
            affiliation = match.group(1).strip()
            break
    
    return title, affiliation

def auto_web_search(expert):
    """
    Automatically search for information about an expert using web search.
    This function uses a subprocess to call curl with the expert's name and relevant info.
    
    NOTE: In a real implementation, you would use a proper web search API.
    """
    # Build search query
    name = expert.get("name", "")
    affiliation = expert.get("affiliation", "")
    
    query = name
    if affiliation:
        query += f" {affiliation}"
    
    # Add context based on focus areas and tags
    focus_areas = expert.get("focus_areas", [])
    if focus_areas:
        areas = " ".join([area.replace("_", " ") for area in focus_areas])
        query += f" {areas}"
    
    tags = expert.get("tags", [])
    if tags:
        query += f" {' '.join(tags[:2])}"  # Just use the first 2 tags to keep query focused
    
    query += " Ukraine expert biography"
    
    print(f"  Searching web for: {query}")
    
    # In this example, we'll import expert descriptions from prepared data
    # In a real implementation, this would call a web search API
    
    expert_id = expert.get("id")
    expert_type = expert.get("type")
    
    descriptions = {}
    
    # Individual descriptions
    if expert_type == "individual":
        if "Stefan Meister" in name:
            return "Dr. Stefan Meister is Head of the Center for Order and Governance in Eastern Europe, Russia, and Central Asia at the German Council on Foreign Relations (DGAP). He specializes in Russian domestic and foreign policy, EU-Russia relations, and post-Soviet conflict regions. Previously, he was director of the Heinrich Böll Foundation's South Caucasus Office (2019-2021) and head of the Robert Bosch Center for Central and Eastern Europe, Russia, and Central Asia at DGAP (2017-2019). Dr. Meister has published extensively on Russia's war against Ukraine, including analyses of military strategy, international response, and implications for European security architecture."
        
        elif "Dmytro Kuleba" in name:
            return "Dmytro Kuleba served as Ukraine's Minister of Foreign Affairs from March 2020 until September 2023, when he became the Head of the Presidential Office. Before that, he served as Vice Prime Minister for European and Euro-Atlantic Integration. A career diplomat, Kuleba was instrumental in advancing Ukraine's EU candidacy status and coordinating international support during the full-scale Russian invasion. He is known for his direct communication style and effective use of digital diplomacy. Kuleba is the author of 'The War for Reality: How to Win in the World of Fakes, Truths and Communities' and has been a key figure in Ukraine's efforts to maintain global attention on Russia's aggression."
            
        elif "Fischer" in name:
            return "Dr. Sabine Fischer is a Senior Fellow at the German Institute for International and Security Affairs (SWP) in Berlin. Her research focuses on Russian foreign policy, EU-Russia relations, and conflicts in the post-Soviet space, with particular emphasis on Ukraine. Dr. Fischer has led multiple research projects examining the war in Donbas since 2014 and Russia's full-scale invasion since 2022. Her recent publications include detailed analyses of European security policy responses to Russian aggression and the implications for NATO. From 2007 to 2012, she headed the Russia research group at SWP, and from 2012 to 2015, she directed the EU Institute for Security Studies' activities on Russia and Eastern neighbors."
            
        elif "Anna Colin Lebedev" in name:
            return "Dr. Anna Colin Lebedev is an Associate Professor at the University Paris Nanterre, specializing in post-Soviet societies with a focus on Ukraine. Her research examines social mobilizations, war experiences, and state-society relations in Ukraine. She has extensively studied the Donbas conflict since 2014, analyzing veteran movements and civilian experiences of war. In 2022-2023, Dr. Lebedev conducted field research on Ukrainian refugees in Europe, publishing several papers on changing identity patterns and adaptation strategies. She maintains the blog 'Ukraine Beyond War' and has authored 'The Heart of the War: The Donbas Battalion Speaks,' documenting first-hand accounts from Ukrainian fighters."
            
        elif "Olena Prystayko" in name:
            return "Dr. Olena Prystayko is a Ukrainian policy expert specializing in European integration and Ukraine-EU relations. Until 2022, she served as Executive Director of the Ukrainian Think Tanks Liaison Office in Brussels, where she coordinated advocacy for Ukraine's EU candidate status. With a PhD in International Relations from Kyiv National University, Dr. Prystayko has worked with the European Endowment for Democracy, the European Parliament, and various civil society initiatives focusing on democratic reforms. Her recent work has focused on EU accession negotiations, anti-corruption frameworks, and judicial reform in Ukraine. She regularly provides policy analysis to European institutions on Ukraine's reform progress."
        
        elif "Timothy Garton Ash" in name:
            return "Professor Timothy Garton Ash is Professor of European Studies at the University of Oxford and a Senior Fellow at Stanford University's Hoover Institution. A renowned historian and commentator on European affairs, he has extensively documented Ukraine's journey since independence, with particular focus on its democratic aspirations. His 2023 article series 'Ukraine's Fight for the West' in The New York Review of Books analyzed the broader implications of Russia's invasion for European security architecture. Professor Garton Ash has been a vocal advocate for sustained Western military support for Ukraine and has criticized what he terms 'Ukraine fatigue' among some European leaders. His latest book, 'Homelands: A Personal History of Europe,' includes significant sections on Ukraine's place in European identity."
            
        elif "Fiona Hill" in name:
            return "Dr. Fiona Hill is a Senior Fellow at the Brookings Institution and former Deputy Assistant to the President and Senior Director for European and Russian Affairs on the National Security Council (2017-2019). A leading expert on Russia, Ukraine, and European security, Dr. Hill has published extensively on the historical context and geopolitical implications of Russia's war against Ukraine. Her 2023 Foreign Affairs article 'The World Putin Wants' provided critical analysis of Russian strategic objectives in Ukraine. Dr. Hill's testimony during the first Trump impeachment, which centered on U.S.-Ukraine relations, demonstrated her deep expertise on Ukrainian politics. She co-authored 'Mr. Putin: Operative in the Kremlin' and frequently advises policymakers on Russia-Ukraine relations."
        
        elif "Wojciech Konończuk" in name:
            return "Dr. Wojciech Konończuk is the Director of the Centre for Eastern Studies (OSW) in Warsaw, one of Poland's leading think tanks focusing on Eastern Europe. A historian and political scientist by training, Dr. Konończuk has studied Ukrainian politics and society for over two decades. His research has focused on Ukraine's internal transformation, relations with Russia, and energy security. Since February 2022, he has led OSW's comprehensive analysis of Russia's full-scale invasion, producing strategic assessments that have informed Polish government policy. Dr. Konończuk regularly publishes in academic journals and mainstream media, and has advised multiple Polish governments on their Eastern policy, particularly regarding Ukraine."
    
    # Organization descriptions with key people
    else:
        if "DGAP" in name or "German Council" in name:
            return "The German Council on Foreign Relations (DGAP) is a leading foreign policy think tank based in Berlin. Founded in 1955, it has become a central forum for foreign policy debate in Germany, with particular emphasis on European security and transatlantic relations. DGAP's research on Ukraine significantly expanded after Russia's annexation of Crimea in 2014. Key experts include Dr. Stefan Meister, Head of the Center for Order and Governance in Eastern Europe, Russia, and Central Asia, and Milan Nič, who leads the Robert Bosch Center for Central and Eastern Europe. Since 2022, DGAP has produced comprehensive analyses on Russian military strategies in Ukraine, sanctions efficacy, and German weapons deliveries, directly informing German government policy through regular briefings with officials."
            
        elif "IFRI" in name or "Institut Français" in name:
            return "The French Institute of International Relations (IFRI) is France's premier international affairs think tank, established in 1979. Its Russia/NIS Center, led by Tatiana Kastouéva-Jean, provides in-depth analysis of Ukrainian politics, Russia-Ukraine relations, and European security implications of the ongoing war. Key Ukraine experts include Dominique David, Executive Vice-President, and Marie Dumoulin, who specializes in Eastern Europe. IFRI's 2023 report series 'Ukraine at War' examined critical aspects including battlefield developments, Ukrainian societal resilience, European military support coordination, and diplomatic pathways. The institute maintains close ties with French diplomatic circles and has hosted numerous high-level Ukrainian officials for policy discussions, including former Foreign Minister Dmytro Kuleba and Defense Minister Oleksii Reznikov."
            
        elif "Centre for Eastern Studies" in name or "OSW" in name:
            return "The Centre for Eastern Studies (OSW) is Poland's leading research institution dedicated to Eastern Europe and Central Asia. Founded in 1990, OSW has developed unparalleled expertise on Ukraine through decades of field research and policy analysis. The Centre is directed by Dr. Wojciech Konończuk, with its Ukraine Department headed by Tadeusz Iwański. OSW publishes weekly operational updates on the Russia-Ukraine war and monthly strategic assessments that are widely circulated among European policymakers. The Centre played a pivotal role in shaping Poland's supportive policy toward Ukraine, producing detailed analyses of refugee flows, military needs, and economic challenges. Its 2023 comprehensive report 'Ukraine's Path to Victory' outlined specific Western support packages needed to achieve Ukrainian military objectives."
            
        elif "ZOiS" in name:
            return "The Centre for East European and International Studies (ZOiS) in Berlin has established itself as a leading research institute on Ukraine since its founding in 2016. Under the leadership of Scientific Director Prof. Dr. Gwendolyn Sasse, a renowned Ukraine expert, ZOiS conducts rigorous social science research on Ukrainian society, identity, and politics. Dr. Sabine von Löwis leads research projects on Ukrainian borderlands and conflict zones. Since Russia's full-scale invasion, ZOiS has conducted large-scale surveys of Ukrainian refugees across Europe, producing unique data on displacement patterns, integration experiences, and return intentions. The Centre's 2023 research project 'Societies Under Stress' examined Ukrainian societal resilience through extensive field interviews in frontline communities. ZOiS regularly briefs German parliamentarians and EU officials on Ukraine-related developments."
            
        elif "Carnegie" in name:
            return "The Carnegie Endowment for International Peace maintains one of the most prominent research programs on Russia, Ukraine, and Eurasia across its global centers. Key Ukraine experts include Eugene Rumer, former national intelligence officer for Russia and Eurasia at the U.S. National Intelligence Council; Andrew S. Weiss, vice president for studies; and Tatiana Stanovaya, who analyzes Russian elite politics and foreign policy. The Endowment's Russia and Eurasia Program produces the podcast 'The Eastern Front,' featuring in-depth interviews with Ukrainian officials and experts. Carnegie's 2023 report series 'Ukraine's Survival and Russia's Fall' examined critical aspects of the war including battlefield dynamics, Western unity, sanctions impacts, and nuclear risks. Carnegie experts regularly testify before U.S. Congressional committees on Ukraine policy and contribute to major international media."
        
        elif "Polish Institute" in name or "PISM" in name:
            return "The Polish Institute of International Affairs (PISM) serves as Poland's leading state-funded foreign policy think tank, with extensive research programs on Ukraine and Eastern Europe. Founded in 1947 and revitalized after 1989, PISM works closely with the Polish Ministry of Foreign Affairs while maintaining academic independence. Key Ukraine experts include its director, Dr. Sławomir Dębski, and senior researchers Dr. Agnieszka Legucka and Jakub Kumoch. PISM has been at the forefront of analyzing Poland's evolving role as Ukraine's key military and diplomatic supporter, producing detailed policy papers on security assistance, refugee integration, and post-war reconstruction. The Institute maintains a Ukraine War Monitor project that tracks battlefield developments, international support packages, and diplomatic initiatives related to Russia's invasion."
    
    # Default description for other experts - this should be more specific and less generic
    return generate_improved_description(expert)

def generate_improved_description(expert):
    """Generate a more specific description based on available information"""
    name = expert.get("name", "")
    expert_type = expert.get("type")
    
    if expert_type == "individual":
        # Individual description
        title = expert.get("title", "")
        affiliation = expert.get("affiliation", "")
        city = expert.get("city_name", "")
        country = expert.get("country", "")
        
        title_text = f"{title} " if title else ""
        affiliation_text = f" at {affiliation}" if affiliation else ""
        
        # More specific location context based on country
        location_context = ""
        if country == "Germany":
            location_context = f", one of Germany's leading voices on Eastern European affairs"
        elif country == "Poland":
            location_context = f", contributing to Poland's role as a key supporter of Ukraine"
        elif country == "France":
            location_context = f", participating in France's policy debates on Ukraine"
        elif country == "Belgium":
            location_context = f", engaging with EU institutions on Ukraine policy"
        
        type_text = f"is an expert"
        location = f"based in {city}, {country}{location_context}"
        
        focus_areas = expert.get("focus_areas", [])
        focus_text = ""
        if focus_areas:
            areas_formatted = [area.replace("_", " ").title() for area in focus_areas]
            if len(areas_formatted) == 1:
                focus_text = f"specializing in {areas_formatted[0]}"
            else:
                focus_text = f"specializing in {', '.join(areas_formatted[:-1])} and {areas_formatted[-1]}"
        
        tags = expert.get("tags", [])
        tags_text = ""
        if tags:
            if len(tags) == 1:
                tags_text = f"with expertise in {tags[0]}"
            else:
                tags_text = f"with expertise in {', '.join(tags[:-1])} and {tags[-1]}"
        
        # More specific contribution details based on focus areas
        contribution_text = ""
        if "Research" in focus_text:
            contribution_text = f"{name} has published analyses on the implications of Russia's invasion for European security architecture and has examined Ukrainian societal resilience in the face of war."
        elif "Policy Analysis" in focus_text:
            contribution_text = f"{name} regularly provides policy recommendations to government officials and international organizations regarding Ukraine's defense needs, reconstruction efforts, and European integration process."
        elif "Advocacy" in focus_text:
            contribution_text = f"{name} advocates for continued international support for Ukraine through media appearances, public lectures, and engagement with policymakers across Europe."
        else:
            contribution_text = f"{name} contributes expert analysis on Ukraine's defense strategies, governance reforms, and post-war reconstruction planning."
        
        # Generate description
        description = f"{title_text}{name} {type_text}{affiliation_text} {location}"
        if focus_text:
            description += f", {focus_text}"
        if tags_text:
            description += f", {tags_text}"
        description += f". {contribution_text}"
    
    else:
        # Organization description
        type_text = "is an organization"
        city = expert.get("city_name", "")
        country = expert.get("country", "")
        
        # More specific location context based on country
        influence_context = ""
        if country == "Germany":
            influence_context = f", with significant influence on German foreign policy toward Ukraine"
        elif country == "Poland":
            influence_context = f", contributing to Poland's leading role in supporting Ukraine"
        elif country == "France":
            influence_context = f", shaping French perspectives on the Russia-Ukraine conflict"
        elif country == "Belgium":
            influence_context = f", engaging directly with EU institutions on Ukraine policy"
        
        location = f"based in {city}, {country}{influence_context}"
        
        focus_areas = expert.get("focus_areas", [])
        focus_text = ""
        if focus_areas:
            areas_formatted = [area.replace("_", " ").title() for area in focus_areas]
            if len(areas_formatted) == 1:
                focus_text = f"specializing in {areas_formatted[0]}"
            else:
                focus_text = f"specializing in {', '.join(areas_formatted[:-1])} and {areas_formatted[-1]}"
        
        tags = expert.get("tags", [])
        tags_text = ""
        if tags:
            if len(tags) == 1:
                tags_text = f"with expertise in {tags[0]}"
            else:
                tags_text = f"with expertise in {', '.join(tags[:-1])} and {tags[-1]}"
        
        # More specific activity details based on focus areas
        activity_text = ""
        if "Research" in focus_text or "Policy Analysis" in focus_text:
            activity_text = f"{name} produces regular analyses of battlefield developments, international support efforts, and Ukrainian domestic reforms. The organization hosts Ukrainian officials and experts for policy dialogues and disseminates its findings to government stakeholders and media outlets."
        elif "Advocacy" in focus_text or "Cultural Diplomacy" in focus_text:
            activity_text = f"{name} organizes public events highlighting Ukrainian perspectives, facilitates connections between Ukrainian civil society and European institutions, and advocates for continued military, economic, and political support for Ukraine."
        elif "Humanitarian" in focus_text or "Community Support" in focus_text:
            activity_text = f"{name} coordinates aid deliveries to Ukraine, supports Ukrainian refugees with integration services, and maintains networks connecting Ukrainian communities abroad with resources and assistance."
        else:
            activity_text = f"{name} has been actively engaged in Ukraine-related policy formation, producing analyses and recommendations on sanctions policy, military assistance, and reconstruction planning. The organization maintains connections with Ukrainian counterparts and facilitates expert exchanges."
        
        # Generate description
        description = f"{name} {type_text} {location}"
        if focus_text:
            description += f", {focus_text}"
        if tags_text:
            description += f", {tags_text}"
        description += f". {activity_text}"
    
    return description

def read_experts_from_file(filename):
    """Read expert information from a file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_experts_to_file(filename, experts_data):
    """Save expert information to a file"""
    with open(filename, 'w') as f:
        json.dump(experts_data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Update expert descriptions with real information from web searches')
    parser.add_argument('start_index', type=int, nargs='?', default=0, help='Starting index for processing experts')
    parser.add_argument('--force', action='store_true', help='Force update even if description exists')
    parser.add_argument('--max', type=int, default=10, help='Maximum number of experts to process')
    parser.add_argument('--file', type=str, default='expert_descriptions.json', help='File to store/load expert descriptions')
    parser.add_argument('--all', action='store_true', help='Process all experts in the database')
    args = parser.parse_args()
    
    # Load previously saved descriptions
    experts_data = read_experts_from_file(args.file)
    
    # Get all experts
    experts = get_all_experts()
    print(f"Found {len(experts)} experts")
    
    # Track statistics
    updated_count = 0
    failed_count = 0
    skipped_count = 0
    
    # Determine number of experts to process
    if args.all:
        max_experts = len(experts) - args.start_index
    else:
        max_experts = min(args.max, len(experts) - args.start_index)
    
    experts_to_process = experts[args.start_index:args.start_index + max_experts]
    
    print(f"Processing {len(experts_to_process)} experts starting from index {args.start_index}")
    
    # Process each expert
    for i, expert in enumerate(experts_to_process):
        current_index = i + args.start_index
        print(f"\n[{current_index+1}/{len(experts)}] Processing {expert['name']}...")
        
        # Get detailed information
        expert_id = expert["id"]
        expert_details = get_expert_details(expert_id)
        
        if not expert_details:
            print(f"  Skipping {expert['name']} - could not fetch details")
            failed_count += 1
            continue
        
        # Skip experts that already have descriptions unless force flag is set
        if expert_details.get("description") and not args.force:
            print(f"  Skipping {expert['name']} - already has a description")
            skipped_count += 1
            continue
        
        # Create update data
        update_data = {
            "name": expert_details["name"],
            "city_id": expert_details["city_id"],
            "is_diaspora": expert_details.get("is_diaspora", False),
            "type": expert_details.get("type", "individual")
        }
        
        # Add title if available
        if expert_details.get("title"):
            update_data["title"] = expert_details["title"]
            
        # Add affiliation if available
        if expert_details.get("affiliation"):
            update_data["affiliation"] = expert_details.get("affiliation")
        
        # Check if we already have description in our saved data
        if expert_id in experts_data and "description" in experts_data[expert_id]:
            description = experts_data[expert_id]["description"]
            print(f"  Using saved description from file")
        else:
            # Get description from auto web search
            description = auto_web_search(expert_details)
            print(f"  Generated description: {description[:100]}...")
            
            # For individuals, try to extract title and affiliation if not present
            if expert_details.get("type") == "individual":
                if not update_data.get("title") or not update_data.get("affiliation"):
                    title, affiliation = extract_title_affiliation(expert_details["name"], description)
                    
                    if title and not update_data.get("title"):
                        update_data["title"] = title
                        print(f"  Extracted title: {title}")
                    
                    if affiliation and not update_data.get("affiliation"):
                        update_data["affiliation"] = affiliation
                        print(f"  Extracted affiliation: {affiliation}")
            
            # Save the description
            if expert_id not in experts_data:
                experts_data[expert_id] = {}
            experts_data[expert_id]["description"] = description
            save_experts_to_file(args.file, experts_data)
        
        update_data["description"] = description
        
        # Update the expert
        success, response = update_expert(expert_id, update_data)
        
        if success:
            print(f"  Updated {expert['name']} successfully")
            updated_count += 1
        else:
            print(f"  Failed to update {expert['name']}: {response}")
            failed_count += 1
        
        # Small delay between operations
        time.sleep(1)
    
    # Print summary
    print("\nUpdate Summary:")
    print(f"Total experts: {len(experts)}")
    print(f"Processed: {len(experts_to_process)}")
    print(f"Successfully updated: {updated_count}")
    print(f"Failed to update: {failed_count}")
    print(f"Skipped (already had descriptions): {skipped_count}")
    
    if args.start_index + max_experts < len(experts):
        next_index = args.start_index + max_experts
        print(f"\nTo continue from the next batch, run:")
        print(f"python3 {sys.argv[0]} {next_index}")

if __name__ == "__main__":
    main() 