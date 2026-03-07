#!/usr/bin/env python3
"""
Incremental Configuration Analysis Builder
Extracts configuration data in chunks to avoid context overload
"""

import json
import sys
from pathlib import Path

def load_process_structures():
    """Load all LPD process structures"""
    processes = []
    for i in range(1, 4):
        lpd_file = Path(f"Temp/lpd_process_{i}.json")
        if lpd_file.exists():
            with open(lpd_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                processes.append(data)
    return processes

def extract_configuration_chunks(processes):
    """Extract configuration data organized by category"""
    chunks = {
        "file_channels": [],
        "web_services": [],
        "process_variables": [],
        "security_roles": [],
        "config_dependencies": []
    }
    
    for proc_idx, process_data in enumerate(processes, 1):
        # Handle nested structure
        if 'processes' in process_data:
            process_list = process_data['processes']
        else:
            process_list = [process_data]
        
        for process in process_list:
            proc_name = process.get('process_name', process.get('name', f'Process_{proc_idx}'))
            
            # Extract file channels from ACCFIL activities
            activities = process.get('activities', [])
            for activity in activities:
                if activity.get('type') == 'ACCFIL':
                    file_channel = activity.get('properties', {}).get('fileChannel', '')
                    if file_channel:
                        chunks["file_channels"].append({
                            'activity_id': activity.get('id'),
                            'file_channel': file_channel,
                            'process_name': proc_name
                        })
                
                # Extract web services from WEBRN activities
                if activity.get('type') == 'WEBRN':
                    web_service = activity.get('properties', {}).get('webService', '')
                    if web_service:
                        chunks["web_services"].append({
                            'activity_id': activity.get('id'),
                            'web_service': web_service,
                            'process_name': proc_name
                        })
            
            # Extract START activity variables
            activities = process.get('activities', [])
            for activity in activities:
                if activity.get('type') == 'START':
                    properties = activity.get('properties', {})
                    # Extract variables that reference _configuration
                    for var_name, var_value in properties.items():
                        if isinstance(var_value, str) and '_configuration' in var_value:
                            chunks["process_variables"].append({
                                'variable': var_name,
                                'value': var_value,
                                'process_name': proc_name
                            })
            
            # Extract security roles
            security = process.get('security', {})
            roles = security.get('roles', [])
            for role in roles:
                role['process_name'] = proc_name
                chunks["security_roles"].append(role)
            
            # Extract config set dependencies
            config_sets = process.get('config_sets', [])
            for cs in config_sets:
                cs['process_name'] = proc_name
                chunks["config_dependencies"].append(cs)
    
    return chunks

def main():
    print("=" * 80)
    print("CONFIGURATION ANALYSIS BUILDER - INCREMENTAL MODE")
    print("=" * 80)
    
    # Load all process structures
    print("\n[1/3] Loading process structures...")
    processes = load_process_structures()
    print(f"   ✓ Loaded {len(processes)} processes")
    
    # Extract configuration chunks
    print("\n[2/3] Extracting configuration data by category...")
    chunks = extract_configuration_chunks(processes)
    
    # Save each chunk
    for category, data in chunks.items():
        if data:
            chunk_file = Path(f"Temp/config_chunk_{category}.json")
            with open(chunk_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "category": category,
                    "count": len(data),
                    "items": data
                }, f, indent=2)
            print(f"   ✓ {category}: {len(data)} items → {chunk_file.name}")
        else:
            print(f"   - {category}: 0 items (skipped)")
    
    print(f"\n[3/3] Configuration chunks ready for AI analysis")
    print(f"\n   Next steps:")
    print(f"   1. AI analyzes each config_chunk_*.json file")
    print(f"   2. AI returns analysis for each category")
    print(f"   3. Run: python Temp/build_configuration_analysis.py merge")
    
    return 0

def merge_chunks():
    """Merge analyzed chunks into final configuration_analysis.json"""
    print("=" * 80)
    print("MERGING CONFIGURATION ANALYSIS CHUNKS")
    print("=" * 80)
    
    configuration_analysis = {
        "file_channel_config": [],
        "web_service_config": [],
        "process_variables": [],
        "security_roles": [],
        "configuration_dependencies": [],
        "modification_instructions": {}
    }
    
    categories = ["file_channels", "web_services", "process_variables", 
                  "security_roles", "config_dependencies"]
    
    for category in categories:
        analyzed_file = Path(f"Temp/config_chunk_{category}_analyzed.json")
        if analyzed_file.exists():
            print(f"\n   Merging {category}...")
            with open(analyzed_file, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)
            
            # Map to output structure
            if category == "file_channels":
                configuration_analysis["file_channel_config"] = chunk_data.get("analysis", [])
            elif category == "web_services":
                configuration_analysis["web_service_config"] = chunk_data.get("analysis", [])
            elif category == "process_variables":
                configuration_analysis["process_variables"] = chunk_data.get("analysis", [])
            elif category == "security_roles":
                configuration_analysis["security_roles"] = chunk_data.get("analysis", [])
            elif category == "config_dependencies":
                configuration_analysis["configuration_dependencies"] = chunk_data.get("analysis", [])
            
            # Merge modification instructions
            if "modification_instructions" in chunk_data:
                configuration_analysis["modification_instructions"].update(
                    chunk_data["modification_instructions"]
                )
            
            print(f"   ✓ {category} merged")
        else:
            print(f"   - {category} not found (skipped)")
    
    # Save final output
    output_file = Path("Temp/configuration_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(configuration_analysis, f, indent=2)
    
    print(f"\n   ✓ Written: {output_file}")
    print("\n" + "=" * 80)
    print("PHASE 3 COMPLETE")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "merge":
        sys.exit(merge_chunks())
    else:
        sys.exit(main())
