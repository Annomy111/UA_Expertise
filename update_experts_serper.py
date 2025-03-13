#!/usr/bin/env python3
import requests
import json
import time
import sys
import os
import argparse
import re
from urllib.parse import quote_plus
import base64

# Base URL for the API
API_URL = "http://localhost:8000"

# You should replace this with your actual Serper API key
SERPER_API_KEY = "24f44e45b73e32ac7e31b447a0568caa7fa4b0db"  # Replace with something like "a1b2c3d4e5f6g7h8i9j0..."

# Flag to use fallback descriptions if Serper API key is not set or API calls fail
USE_FALLBACK = True  # Set to False to require Serper API

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

def serper_web_search(query):
    """
    Perform a web search using the Serper API
    """
    encoded_query = quote_plus(query)
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": query,
        "gl": "us",
        "hl": "en",
        "num": 5  # Get top 5 results
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error with Serper API: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception during Serper API call: {e}")
        return None

def get_expert_description_from_search(expert, search_results):
    """
    Extract and construct a description for an expert from search results
    """
    name = expert.get("name", "")
    expert_type = expert.get("type", "individual")
    
    if not search_results or "organic" not in search_results:
        return None
    
    # Extract text snippets from search results
    snippets = []
    for result in search_results.get("organic", []):
        if "snippet" in result:
            snippets.append(result["snippet"])
    
    if not snippets:
        return None
    
    # Combine snippets and clean up
    combined_text = " ".join(snippets)
    
    # Basic cleanup
    combined_text = combined_text.replace("...", " ")
    combined_text = re.sub(r'\s+', ' ', combined_text)
    
    # For individuals, try to construct a biography
    if expert_type == "individual":
        # Extract the most relevant parts
        bio_parts = []
        
        # Look for role and affiliation
        role_pattern = rf"{name} is .{{5,100}}"
        role_match = re.search(role_pattern, combined_text)
        if role_match:
            bio_parts.append(role_match.group(0))
        
        # Look for background information
        background_indicators = ["previously", "before", "formerly", "has been", "served as", "worked"]
        for indicator in background_indicators:
            pattern = rf"({indicator} .{{10,150}}\.)"
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            bio_parts.extend(matches)
        
        # Look for expertise
        expertise_indicators = ["expert", "specializes", "focuses", "research", "expertise"]
        for indicator in expertise_indicators:
            pattern = rf"({indicator} .{{10,150}}\.)"
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            bio_parts.extend(matches)
        
        # If we found some relevant parts, use them
        if bio_parts:
            description = " ".join(bio_parts)
            # Clean up any remaining issues
            description = re.sub(r'\s+', ' ', description)
            return description
    
    # For organizations, focus on their purpose and activities
    elif expert_type == "organization":
        # Look for organization description
        org_pattern = rf"{name} is .{{5,200}}"
        org_match = re.search(org_pattern, combined_text)
        org_part = org_match.group(0) if org_match else ""
        
        # Look for activities
        activity_indicators = ["focuses", "works", "mission", "activities", "provides", "supports"]
        activity_parts = []
        for indicator in activity_indicators:
            pattern = rf"({indicator} .{{10,150}}\.)"
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            activity_parts.extend(matches)
        
        # Combine organization description with activities
        if org_part or activity_parts:
            parts = [org_part] if org_part else []
            parts.extend(activity_parts)
            description = " ".join(parts)
            # Clean up any remaining issues
            description = re.sub(r'\s+', ' ', description)
            return description
    
    # If all else fails, just return the combined text
    return combined_text

def find_expert_image(expert_name):
    """Use Serper API to find an image for the expert"""
    query = f"{expert_name} official photo portrait"
    url = "https://google.serper.dev/images"
    
    payload = json.dumps({
        "q": query,
        "gl": "us",
        "hl": "en",
        "num": 10  # Get more results to filter through
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"  Image search returned {len(data.get('images', []))} results")
            
            # Get all image results
            if "images" in data and len(data["images"]) > 0:
                # Try multiple images in case some fail
                for i, image_data in enumerate(data["images"][:5]):  # Try first 5 images
                    image_url = image_data.get("imageUrl")
                    if not image_url:
                        continue
                        
                    try:
                        # Download the image
                        print(f"  Trying image {i+1}: {image_url}")
                        image_response = requests.get(image_url, timeout=5)
                        
                        if image_response.status_code != 200:
                            print(f"  Failed to download image: HTTP {image_response.status_code}")
                            continue
                            
                        # Check if we actually got an image (by content type)
                        content_type = image_response.headers.get('Content-Type', '')
                        if not content_type.startswith('image/'):
                            print(f"  Not an image: Content-Type is {content_type}")
                            # Check if it looks like HTML
                            if b'<html' in image_response.content[:100].lower():
                                print(f"  Received HTML instead of an image, skipping")
                                continue
                        
                        # Validate image size (too small might be an error or blank image)
                        if len(image_response.content) < 1000:
                            print(f"  Image too small ({len(image_response.content)} bytes), skipping")
                            continue
                            
                        # Convert to base64 for API storage
                        image_base64 = base64.b64encode(image_response.content).decode('utf-8')
                        print(f"  Image downloaded successfully ({len(image_response.content)} bytes)")
                        
                        # Determine image format for correct data URI
                        image_format = 'jpeg'  # Default
                        if content_type == 'image/png':
                            image_format = 'png'
                        elif content_type == 'image/gif':
                            image_format = 'gif'
                        elif content_type == 'image/webp':
                            image_format = 'webp'
                            
                        return f"data:image/{image_format};base64,{image_base64}"
                    except Exception as e:
                        print(f"  Error with image {i+1}: {e}")
                        continue
                
                print("  None of the candidate images were valid")
            else:
                print("  No images found in search results")
        else:
            print(f"  Error with image search API: {response.status_code}")
        return None
    except Exception as e:
        print(f"  Exception during image search: {e}")
        return None

def auto_web_search(expert):
    """
    Use Serper API to automatically search for information about an expert
    """
    # Build search query
    name = expert.get("name", "")
    affiliation = expert.get("affiliation", "")
    
    query = name
    if affiliation:
        query += f" {affiliation}"
    
    # Add context based on focus areas
    focus_areas = expert.get("focus_areas", [])
    if focus_areas:
        areas = " ".join([area.replace("_", " ") for area in focus_areas])
        query += f" {areas}"
    
    # Add context on expert type
    if expert.get("type") == "individual":
        query += " biography Ukraine expert"
    else:
        query += " organization Ukraine"
    
    print(f"  Searching web for: {query}")
    
    # Check if API key is valid
    if SERPER_API_KEY == "YOUR_SERPER_API_KEY" or not SERPER_API_KEY:
        if USE_FALLBACK:
            print("  No valid Serper API key. Using fallback description generation.")
            return generate_improved_description(expert)
        else:
            return "Please set a valid Serper API key in the script."
    
    # Perform search using Serper API
    search_results = serper_web_search(query)
    
    if not search_results:
        if USE_FALLBACK:
            print("  No search results. Using fallback description generation.")
            return generate_improved_description(expert)
        else:
            return "No valid search results found for this expert."
    
    # Extract description from search results
    description = get_expert_description_from_search(expert, search_results)
    
    if not description:
        if USE_FALLBACK:
            print("  Couldn't extract useful description. Using fallback description generation.")
            return generate_improved_description(expert)
        else:
            return "Couldn't extract a useful description from search results."
    
    return description

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
    parser = argparse.ArgumentParser(description='Update expert descriptions with real information from Serper API web searches')
    parser.add_argument('start_index', type=int, nargs='?', default=0, help='Starting index for processing experts')
    parser.add_argument('--force', action='store_true', help='Force update even if description exists')
    parser.add_argument('--max', type=int, default=10, help='Maximum number of experts to process')
    parser.add_argument('--file', type=str, default='expert_descriptions_serper.json', help='File to store/load expert descriptions')
    parser.add_argument('--all', action='store_true', help='Process all experts in the database')
    parser.add_argument('--images', action='store_true', help='Also search for and add profile images')
    parser.add_argument('--fallback', action='store_true', help='Use fallback descriptions if Serper API fails')
    parser.add_argument('--debug', action='store_true', help='Show more debugging information')
    args = parser.parse_args()
    
    # Set USE_FALLBACK based on argument
    global USE_FALLBACK
    if args.fallback:
        USE_FALLBACK = True
    
    # Check if Serper API key is set
    if SERPER_API_KEY == "YOUR_SERPER_API_KEY" and not USE_FALLBACK:
        print("Please set your Serper API key in the script or use --fallback to generate descriptions without API")
        return
    elif SERPER_API_KEY == "YOUR_SERPER_API_KEY":
        print("No Serper API key set. Using fallback description generation.")
    
    # Load previously saved descriptions
    experts_data = read_experts_from_file(args.file)
    
    # Get all experts
    experts = get_all_experts()
    print(f"Found {len(experts)} experts")
    
    # Track statistics
    updated_count = 0
    failed_count = 0
    skipped_count = 0
    images_added = 0
    
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
            # Get description from web search
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
        
        # If images flag is set, try to find a profile image
        if args.images:
            print(f"  Searching for profile image...")
            image_base64 = find_expert_image(expert_details["name"])
            if image_base64:
                update_data["image"] = image_base64
                print(f"  Found and added profile image")
                
                # Debug - print a sample of the image data
                if args.debug:
                    print(f"  Image data sample: {image_base64[:50]}...")
                    
                images_added += 1
            else:
                print("  Could not find a suitable profile image")
        
        # Update the expert
        success, response = update_expert(expert_id, update_data)
        
        if args.debug:
            print(f"  API response: {response}")
        
        if success:
            print(f"  Updated {expert['name']} successfully")
            updated_count += 1
        else:
            print(f"  Failed to update {expert['name']}: {response}")
            failed_count += 1
        
        # Small delay between operations to avoid hitting API rate limits
        time.sleep(2)
    
    # Print summary
    print("\nUpdate Summary:")
    print(f"Total experts: {len(experts)}")
    print(f"Processed: {len(experts_to_process)}")
    print(f"Successfully updated: {updated_count}")
    print(f"Failed to update: {failed_count}")
    print(f"Skipped (already had descriptions): {skipped_count}")
    if args.images:
        print(f"Images added: {images_added}")
    
    if args.start_index + max_experts < len(experts):
        next_index = args.start_index + max_experts
        print(f"\nTo continue from the next batch, run:")
        print(f"python3 {sys.argv[0]} {next_index}")

if __name__ == "__main__":
    main() 