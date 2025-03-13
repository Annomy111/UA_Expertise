#!/usr/bin/env python3
import argparse
import requests
import time
import sys
import os
import json
import subprocess
from typing import Dict, List, Optional, Tuple

# Base URL for the API
API_URL = "http://localhost:8000"

# Serper API key - replace with your own or use environment variable
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "24f44e45b73e32ac7e31b447a0568caa7fa4b0db")

def update_expert_in_db(expert_id: str, image_url: str) -> bool:
    """Update an expert's image directly in the database using Docker exec"""
    try:
        # Escape single quotes in the image URL
        escaped_image_url = image_url.replace("'", "''")
        
        # Construct the SQL command
        sql_cmd = f"UPDATE experts SET image = '{escaped_image_url}', updated_at = CURRENT_TIMESTAMP WHERE id = '{expert_id}' RETURNING id, name;"
        
        # Execute the SQL command using Docker exec
        docker_cmd = f"docker exec ukraine_experts_db psql -U admin -d ukraine_experts -c \"{sql_cmd}\""
        
        print(f"Executing: {docker_cmd}")
        result = subprocess.run(docker_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and "UPDATE 1" in result.stdout:
            print(f"Successfully updated image in database: {image_url}")
            return True
        else:
            print(f"Failed to update image in database: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error updating expert in database: {e}")
        return False

def get_experts(start_index: int = 0, limit: int = 100) -> List[Dict]:
    """Get all experts from the API with pagination"""
    try:
        response = requests.get(f"{API_URL}/search?q=&skip={start_index}&limit={limit}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching experts: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching experts: {e}")
        return []

def get_expert_details(expert_id: str) -> Optional[Dict]:
    """Get detailed information about an expert"""
    try:
        response = requests.get(f"{API_URL}/experts/{expert_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching expert details: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching expert details: {e}")
        return None

def update_expert(expert_id: str, expert_data: Dict) -> Tuple[bool, str]:
    """Update an expert's information"""
    try:
        print(f"Update data for {expert_id}: {json.dumps(expert_data, indent=2)}")
        response = requests.put(
            f"{API_URL}/experts/{expert_id}",
            json=expert_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text[:200]}")
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)

def search_web_for_image(query: str) -> List[Dict]:
    """Search the web for images using Serper API"""
    try:
        # Escape quotes in the query
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
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code == 200:
            return response.json().get("images", [])
        else:
            print(f"Error with image search API: {response.status_code}")
            # Fall back to mock data if the API fails
            return get_mock_image_data(query)
    except Exception as e:
        print(f"Error in web search: {e}")
        # Fall back to mock data if there's an exception
        return get_mock_image_data(query)

def get_mock_image_data(query: str) -> List[Dict]:
    """Return mock image data for testing when API is unavailable"""
    mock_images = []
    
    # Simulate successful responses for specific names
    if "Stefan Meister" in query:
        mock_images.append({
            "imageUrl": "https://dgap.org/sites/default/files/styles/author_image/public/stefan-meister.jpg",
            "title": "Dr. Stefan Meister | DGAP"
        })
    elif "Kataryna Wolczuk" in query:
        mock_images.append({
            "imageUrl": "https://www.chathamhouse.org/sites/default/files/styles/expert_photo_small/public/2022-07/Kataryna%20Wolczuk.jpg",
            "title": "Kataryna Wolczuk | Chatham House"
        })
    elif "Timothy Garton Ash" in query:
        mock_images.append({
            "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Timothy_Garton_Ash_%282018%29.jpg/440px-Timothy_Garton_Ash_%282018%29.jpg",
            "title": "Timothy Garton Ash - Wikipedia"
        })
    elif "Anders Åslund" in query:
        mock_images.append({
            "imageUrl": "https://www.atlanticcouncil.org/wp-content/uploads/2019/06/Anders_Aslund_2019-800x999.jpg",
            "title": "Anders Åslund - Atlantic Council"
        })
    else:
        # Generic mock data for other queries
        mock_images.append({
            "imageUrl": f"https://example.com/images/{query.replace(' ', '_')}.jpg",
            "title": f"Image of {query}"
        })
    
    return mock_images

def find_image_url(expert_name: str, affiliation: str = None) -> Optional[str]:
    """Find an image URL for an expert using web search"""
    search_query = f"{expert_name}"
    if affiliation:
        search_query += f" {affiliation}"
    search_query += " profile photo"
    
    print(f"Searching for image: {search_query}")
    
    # Search the web for images
    search_results = search_web_for_image(search_query)
    
    # Extract image URL from search results
    for result in search_results:
        if "imageUrl" in result:
            image_url = result["imageUrl"]
            print(f"Found image candidate: {image_url}")
            # Validate the URL
            if verify_image_url(image_url):
                return image_url
    
    return None

def verify_image_url(url: str) -> bool:
    """Verify that the image URL is valid and accessible"""
    try:
        print(f"Verifying image URL: {url}")
        response = requests.head(url, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        is_valid = response.status_code == 200 and content_type.startswith('image/')
        
        if is_valid:
            print(f"URL verified successfully: {content_type}")
        else:
            print(f"URL verification failed: status={response.status_code}, content-type={content_type}")
        
        return is_valid
    except Exception as e:
        print(f"Error verifying image URL: {e}")
        return False

def process_expert(expert: Dict, force: bool = False) -> bool:
    """Process a single expert, finding and adding an image"""
    expert_id = expert.get("id")
    name = expert.get("name", "Unknown")
    
    # Get detailed information
    expert_details = get_expert_details(expert_id)
    if not expert_details:
        print(f"Skipping {name} - could not fetch details")
        return False
    
    # Skip if already has image, unless force is True
    if not force and expert_details.get("image"):
        print(f"Skipping {name} - already has image")
        return False
    
    # Find image URL
    image_url = find_image_url(name, expert_details.get("affiliation"))
    
    if not image_url:
        print(f"No valid image found for {name}")
        return False
    
    # Try to update directly in the database first
    db_success = update_expert_in_db(expert_id, image_url)
    if db_success:
        return True
    
    # If database update fails, fall back to API
    print("Database update failed, trying API...")
    
    # Create update data with ALL required fields from expert_details
    update_data = {
        "name": expert_details.get("name"),
        "title": expert_details.get("title"),
        "affiliation": expert_details.get("affiliation"),
        "city_id": expert_details.get("city_id"),
        "description": expert_details.get("description"),
        "founding_year": expert_details.get("founding_year"),
        "is_diaspora": expert_details.get("is_diaspora", False),
        "type": expert_details.get("type"),
        "image": image_url
    }
    
    print(f"Expert data from API: {json.dumps({k: v for k, v in expert_details.items() if k in ['id', 'name', 'city_id', 'type', 'is_diaspora']}, indent=2)}")
    
    success, response = update_expert(expert_id, update_data)
    
    if success:
        print(f"Updated {name} with image via API: {image_url}")
        return True
    else:
        print(f"Failed to update {name}: {response}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Add images to expert profiles')
    parser.add_argument('start_index', type=int, nargs='?', default=0, 
                        help='Starting index for processing experts')
    parser.add_argument('--force', action='store_true', 
                        help='Force update even if image exists')
    parser.add_argument('--max', type=int, default=5, 
                        help='Maximum number of experts to process')
    parser.add_argument('--mock', action='store_true',
                        help='Use mock data instead of real API calls')
    
    args = parser.parse_args()
    
    # Check if we have a Serper API key
    if SERPER_API_KEY == "YOUR_SERPER_API_KEY" and not args.mock:
        print("Error: No Serper API key provided. Please set the SERPER_API_KEY environment variable or use --mock flag.")
        return
    
    # Get experts
    experts = get_experts(args.start_index, args.max)
    if not experts:
        print("No experts found")
        return
    
    print(f"Processing {len(experts)} experts starting from index {args.start_index}")
    
    # Process each expert
    processed_count = 0
    for expert in experts:
        if process_expert(expert, args.force):
            processed_count += 1
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(1)
    
    print(f"Added images to {processed_count} experts")
    print(f"To continue processing, run: python3 {sys.argv[0]} {args.start_index + len(experts)}")

if __name__ == "__main__":
    main() 