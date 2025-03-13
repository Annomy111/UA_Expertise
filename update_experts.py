#!/usr/bin/env python3
import requests
import json
import time
import random
import sys

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

def generate_description(expert):
    """Generate a description for the expert based on available information"""
    name = expert.get("name", "")
    type_text = "is an individual expert" if expert.get("type") == "individual" else "is an organization"
    location = f"based in {expert.get('city_name', '')}, {expert.get('country', '')}"
    
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
    
    # Generate description
    description = f"{name} {type_text} {location}"
    if focus_text:
        description += f", {focus_text}"
    if tags_text:
        description += f", {tags_text}"
    description += "."
    
    return description

def main():
    # Get all experts
    experts = get_all_experts()
    print(f"Found {len(experts)} experts")
    
    # Track statistics
    updated_count = 0
    failed_count = 0
    
    # Start from a specific index (for resuming)
    start_index = 0
    if len(sys.argv) > 1:
        try:
            start_index = int(sys.argv[1])
        except ValueError:
            pass
    
    # Process each expert
    for i, expert in enumerate(experts[start_index:]):
        current_index = i + start_index
        print(f"[{current_index+1}/{len(experts)}] Processing {expert['name']}...")
        
        # Get detailed information
        expert_id = expert["id"]
        expert_details = get_expert_details(expert_id)
        
        if not expert_details:
            print(f"  Skipping {expert['name']} - could not fetch details")
            failed_count += 1
            continue
        
        # Skip experts that already have descriptions
        if expert_details.get("description"):
            print(f"  Skipping {expert['name']} - already has a description")
            continue
        
        # Create update data
        update_data = {
            "name": expert_details["name"],
            "city_id": expert_details["city_id"],
            "is_diaspora": expert_details.get("is_diaspora", False),
        }
        
        # Add description if missing
        if not expert_details.get("description"):
            update_data["description"] = generate_description(expert_details)
            print(f"  Generated description: {update_data['description']}")
        
        # Update the expert
        success, response = update_expert(expert_id, update_data)
        
        if success:
            print(f"  Updated {expert['name']} successfully")
            updated_count += 1
        else:
            print(f"  Failed to update {expert['name']}: {response}")
            failed_count += 1
        
        # Delay to avoid overwhelming the API
        time.sleep(random.uniform(0.5, 1.5))
    
    # Print summary
    print("\nUpdate Summary:")
    print(f"Total experts: {len(experts)}")
    print(f"Successfully updated: {updated_count}")
    print(f"Failed to update: {failed_count}")
    print(f"Skipped: {len(experts) - updated_count - failed_count}")

if __name__ == "__main__":
    main() 