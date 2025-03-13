#!/usr/bin/env python3
import requests
import json
import time
import random
import sys
import subprocess
import re
import argparse

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

def perform_web_search(query):
    """
    Use the web browser to search for expert information.
    This function will prompt the user to copy/paste information from search results.
    """
    print("\n" + "="*80)
    print(f"SEARCHING: {query}")
    print("="*80)
    
    print("Please search the web for information about this expert and enter it below.")
    print("Enter a blank line when done or type 'skip' to use a basic description.")
    
    lines = []
    while True:
        line = input("Description: ")
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

def main():
    parser = argparse.ArgumentParser(description='Update expert descriptions with real information from web searches')
    parser.add_argument('start_index', type=int, nargs='?', default=0, help='Starting index for processing experts')
    parser.add_argument('--force', action='store_true', help='Force update even if description exists')
    parser.add_argument('--max', type=int, default=5, help='Maximum number of experts to process')
    args = parser.parse_args()
    
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
        
        # Generate search query
        name = expert_details["name"]
        query = name
        if expert_details.get("affiliation"):
            query += f" {expert_details['affiliation']}"
        
        focus_areas = expert_details.get("focus_areas", [])
        if focus_areas:
            areas = " ".join([area.replace("_", " ") for area in focus_areas])
            query += f" {areas}"
        
        tags = expert_details.get("tags", [])
        if tags:
            query += f" {' '.join(tags[:2])}"  # Just use the first 2 tags to keep query focused
        
        query += " Ukraine expert biography"
        
        # Get web search results
        description = perform_web_search(query)
        
        # If no description provided, generate a basic one
        if not description:
            description = generate_basic_description(expert_details)
            print(f"  Using basic description: {description}")
        
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