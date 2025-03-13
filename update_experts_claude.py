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

def fetch_expert_research_results(expert, num_experts_to_research=1):
    """
    This function prepares a list of experts that need additional research.
    You'll need to manually search for information about each expert and enter it into the program.
    """
    # Select experts that need research
    research_list = []
    
    for i, expert in enumerate(expert[:num_experts_to_research]):
        # Extract basic info for searching
        name = expert.get("name", "")
        affiliation = expert.get("affiliation", "")
        focus_areas = [area.replace("_", " ") for area in expert.get("focus_areas", [])]
        tags = expert.get("tags", [])
        
        # Build search query
        search_query = name
        if affiliation:
            search_query += f" {affiliation}"
        if focus_areas:
            search_query += f" {' '.join(focus_areas[:2])}"
        if tags:
            search_query += f" {' '.join(tags[:2])}"
        search_query += " Ukraine expert biography"
        
        research_list.append({
            "id": expert.get("id"),
            "name": name,
            "search_query": search_query
        })
    
    return research_list

def manual_web_search(expert_info):
    """
    Function that prompts the user to search the web for information about an expert
    """
    expert_name = expert_info["name"]
    search_query = expert_info["search_query"]
    
    print("\n" + "="*80)
    print(f"EXPERT: {expert_name}")
    print(f"SEARCH QUERY: {search_query}")
    print("="*80)
    
    print("Please search the web for information about this expert.")
    print("Copy and paste a good description below.")
    print("Enter a blank line when done or type 'skip' to use a basic description.")
    
    lines = []
    while True:
        line = input("> ")
        if not line:
            break
        if line.lower() == 'skip':
            return None
        lines.append(line)
    
    return " ".join(lines)

def generate_basic_description(expert):
    """Generate a basic description based on available information"""
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
    parser = argparse.ArgumentParser(description='Update expert descriptions with real information')
    parser.add_argument('start_index', type=int, nargs='?', default=0, help='Starting index for processing experts')
    parser.add_argument('--force', action='store_true', help='Force update even if description exists')
    parser.add_argument('--max', type=int, default=5, help='Maximum number of experts to process')
    parser.add_argument('--file', type=str, default='expert_descriptions.json', help='File to store/load expert descriptions')
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
    
    # Limit the number of experts to process
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
            # Generate search query
            name = expert_details["name"]
            search_query = name
            if expert_details.get("affiliation"):
                search_query += f" {expert_details['affiliation']}"
            
            focus_areas = expert_details.get("focus_areas", [])
            if focus_areas:
                areas = " ".join([area.replace("_", " ") for area in focus_areas])
                search_query += f" {areas}"
            
            tags = expert_details.get("tags", [])
            if tags:
                search_query += f" {' '.join(tags[:2])}"  # Just use the first 2 tags to keep query focused
            
            search_query += " Ukraine expert biography"
            
            # Get web search results manually
            expert_info = {"id": expert_id, "name": name, "search_query": search_query}
            description = manual_web_search(expert_info)
            
            # If no description provided, generate a basic one
            if not description:
                description = generate_basic_description(expert_details)
                print(f"  Using basic description: {description}")
            
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