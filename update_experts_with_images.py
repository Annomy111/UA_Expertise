#!/usr/bin/env python3
import argparse
import json
import requests
import time
import sys
import re
import subprocess
from typing import Dict, List, Optional, Any

# Base URL for the API
API_BASE_URL = "http://localhost:8000"

def get_experts(start_index: int = 0, limit: int = 100) -> List[Dict]:
    """Fetch experts from the API."""
    response = requests.get(f"{API_BASE_URL}/experts?skip={start_index}&limit={limit}")
    if response.status_code != 200:
        print(f"Error fetching experts: {response.status_code}")
        return []
    return response.json()

def get_expert_details(expert_id: str) -> Dict:
    """Fetch detailed information about an expert."""
    response = requests.get(f"{API_BASE_URL}/experts/{expert_id}")
    if response.status_code != 200:
        print(f"Error fetching expert details: {response.status_code}")
        return {}
    return response.json()

def update_expert(expert_id: str, data: Dict) -> bool:
    """Update an expert's information."""
    response = requests.put(f"{API_BASE_URL}/experts/{expert_id}", json=data)
    if response.status_code != 200:
        print(f"Error updating expert: {response.status_code}, {response.text}")
        return False
    return True

def search_web_for_expert(expert_name: str, affiliation: str = None) -> Dict[str, str]:
    """Search the web for information about an expert."""
    search_query = expert_name
    if affiliation:
        search_query += f" {affiliation}"
    
    print(f"Searching for: {search_query}")
    
    try:
        # Use Google search
        search_url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "q": search_query,
            "cx": "YOUR_SEARCH_ENGINE_ID",
            "key": "YOUR_API_KEY"
        }
        response = requests.get(search_url, params=params)
        search_results = response.json()
        
        # Extract relevant information
        info = ""
        if "items" in search_results:
            for item in search_results["items"][:3]:
                if "snippet" in item:
                    info += item["snippet"] + " "
        
        # Try to find an image
        image_url = None
        image_search_query = f"{expert_name} profile photo"
        image_params = {
            "q": image_search_query,
            "cx": "YOUR_SEARCH_ENGINE_ID",
            "key": "YOUR_API_KEY",
            "searchType": "image"
        }
        image_response = requests.get(search_url, params=image_params)
        image_results = image_response.json()
        
        if "items" in image_results and len(image_results["items"]) > 0:
            image_url = image_results["items"][0].get("link")
        
        return {
            "info": info[:1000],  # Limit to 1000 characters
            "image_url": image_url
        }
    except Exception as e:
        print(f"Error searching web: {e}")
        return {"info": "", "image_url": None}

def generate_description(expert: Dict, web_info: str) -> str:
    """Generate a description for an expert based on their information and web search results."""
    name = expert.get("name", "")
    title = expert.get("title", "")
    affiliation = expert.get("affiliation", "")
    
    # Start with basic information
    description = f"{name} is "
    if title:
        description += f"a {title} "
    if affiliation:
        description += f"at {affiliation}. "
    
    # Add web information if available
    if web_info:
        description += web_info
    else:
        description += f"An expert in their field with valuable insights and experience."
    
    return description

def process_expert(expert: Dict, force: bool = False, images_only: bool = False) -> bool:
    """Process a single expert, updating their description and image if needed."""
    expert_id = expert.get("id")
    name = expert.get("name")
    
    # Get detailed information
    expert_details = get_expert_details(expert_id)
    
    # Skip if already has description and image, unless force is True
    if not force and expert_details.get("description") and expert_details.get("image"):
        print(f"Skipping {name} - already has description and image")
        return False
    
    # Search for expert information
    web_results = search_web_for_expert(name, expert.get("affiliation"))
    
    # Prepare update data
    update_data = {}
    
    # Update description if needed and not in images-only mode
    if not images_only and (force or not expert_details.get("description")):
        description = generate_description(expert, web_results.get("info", ""))
        update_data["description"] = description
    
    # Add image if found
    if web_results.get("image_url"):
        update_data["image"] = web_results.get("image_url")
    
    # Skip if nothing to update
    if not update_data:
        print(f"No updates needed for {name}")
        return False
    
    # Update expert
    success = update_expert(expert_id, update_data)
    if success:
        print(f"Updated {name}")
        if "image" in update_data:
            print(f"  Added image: {update_data['image']}")
    
    return success

def main():
    parser = argparse.ArgumentParser(description="Update expert profiles with descriptions and images")
    parser.add_argument("start_index", type=int, nargs="?", default=0, 
                        help="Starting index for processing experts")
    parser.add_argument("--force", action="store_true", 
                        help="Force update even if description exists")
    parser.add_argument("--max", type=int, default=10, 
                        help="Maximum number of experts to process")
    parser.add_argument("--images-only", action="store_true",
                        help="Only update images, keep existing descriptions")
    
    args = parser.parse_args()
    
    # Fetch experts
    experts = get_experts(args.start_index, args.max)
    if not experts:
        print("No experts found")
        return
    
    print(f"Processing {len(experts)} experts starting from index {args.start_index}")
    
    # Process each expert
    processed_count = 0
    for expert in experts:
        if process_expert(expert, args.force, args.images_only):
            processed_count += 1
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(1)
    
    print(f"Processed {processed_count} experts")
    print(f"To continue processing, run: python3 {sys.argv[0]} {args.start_index + len(experts)}")

if __name__ == "__main__":
    main() 