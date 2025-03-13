#!/usr/bin/env python3
import sys
import os
import json
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the database utilities
import db_utils

def export_all_data():
    """Export all data from the database to JSON files."""
    # Create export directory if it doesn't exist
    export_dir = os.path.join(os.path.dirname(__file__), '..', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    # Get timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Export cities
    cities = db_utils.get_all_cities()
    with open(os.path.join(export_dir, f'cities_{timestamp}.json'), 'w') as f:
        json.dump(cities, f, indent=2)
    print(f"Exported {len(cities)} cities")
    
    # Export all experts
    all_experts = []
    for city in cities:
        experts = db_utils.get_experts_by_city(city['id'])
        all_experts.extend(experts)
    
    with open(os.path.join(export_dir, f'experts_{timestamp}.json'), 'w') as f:
        json.dump(all_experts, f, indent=2)
    print(f"Exported {len(all_experts)} experts")
    
    # Export organizations with key figures
    organizations = db_utils.get_organizations_with_key_figures()
    with open(os.path.join(export_dir, f'organizations_{timestamp}.json'), 'w') as f:
        json.dump(organizations, f, indent=2)
    print(f"Exported {len(organizations)} organizations with key figures")
    
    # Export diaspora organizations
    diaspora_orgs = db_utils.get_diaspora_organizations()
    with open(os.path.join(export_dir, f'diaspora_organizations_{timestamp}.json'), 'w') as f:
        json.dump(diaspora_orgs, f, indent=2)
    print(f"Exported {len(diaspora_orgs)} diaspora organizations")
    
    # Export statistics
    stats = db_utils.get_statistics()
    with open(os.path.join(export_dir, f'statistics_{timestamp}.json'), 'w') as f:
        json.dump(stats, f, indent=2)
    print("Exported database statistics")
    
    # Export detailed expert information
    detailed_experts = []
    for expert in all_experts:
        detailed = db_utils.get_expert_details(expert['id'])
        detailed_experts.append(detailed)
    
    with open(os.path.join(export_dir, f'detailed_experts_{timestamp}.json'), 'w') as f:
        json.dump(detailed_experts, f, indent=2)
    print(f"Exported detailed information for {len(detailed_experts)} experts")
    
    print(f"\nAll data exported to {export_dir}")

if __name__ == "__main__":
    print("Exporting data from the Ukraine Experts Database...")
    export_all_data()
    print("\nData export completed successfully!") 