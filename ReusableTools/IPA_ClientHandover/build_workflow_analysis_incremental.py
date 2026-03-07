#!/usr/bin/env python3
"""
Build workflow_analysis.json incrementally for large processes.
Processes activities in chunks to avoid context overload.

Supports both single-process and multi-process RICE items:
- Single process: Reads lpd_structure.json directly
- Multi-process: Reads lpd_structure.json with multiple processes

Usage:
    # Single process (1 LPD file)
    python build_workflow_analysis_incremental.py
    
    # Multi-process (N LPD files)
    python build_workflow_analysis_incremental.py
    
Output:
    Single process:
        - Temp/workflow_chunk_1.json
        - Temp/workflow_chunk_2.json
        - ...
    
    Multi-process:
        - Temp/workflow_chunk_ProcessName1_1.json
        - Temp/workflow_chunk_ProcessName1_2.json
        - Temp/workflow_chunk_ProcessName2_1.json
        - ...
    
    Final merged output:
        - Temp/workflow_analysis.json (contains all processes)
"""

import json
import sys
from pathlib import Path

def load_lpd_structure():
    """Load the LPD structure file"""
    lpd_path = Path('Temp/lpd_structure.json')
    with open(lpd_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_real_activities(activities):
    """Filter out empty connector activities"""
    return [act for act in activities 
            if act.get('id') and act.get('type') and act.get('type') != 'CONNECTOR']

def save_chunk_for_analysis(chunk_num, activities_chunk, js_blocks, sql_queries, process_name=None, output_dir='Temp'):
    """Save a chunk of activities with their code for AI analysis"""
    if process_name:
        output_path = Path(output_dir) / f'workflow_chunk_{process_name}_{chunk_num}.json'
    else:
        output_path = Path(output_dir) / f'workflow_chunk_{chunk_num}.json'
    
    # Create lookup dictionaries
    js_lookup = {block['activity_id']: block for block in js_blocks}
    sql_lookup = {query['activity_id']: query for query in sql_queries}
    
    chunk_data = []
    for activity in activities_chunk:
        activity_id = activity['id']
        activity_data = {
            'id': activity_id,
            'type': activity.get('type', ''),
            'caption': activity.get('caption', ''),
            'javascript': js_lookup.get(activity_id, {}).get('code', ''),
            'sql': sql_lookup.get(activity_id, {}).get('query', ''),
            'branch_condition': activity.get('branch_condition', '')
        }
        chunk_data.append(activity_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunk_data, f, indent=2)
    
    return output_path

def merge_chunk_results(chunk_num, descriptions, purposes, process_name=None, output_file='Temp/workflow_analysis.json'):
    """Merge chunk analysis results into workflow_analysis.json"""
    output_path = Path(output_file)
    
    # Load existing data or create new
    if output_path.exists():
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            'activity_descriptions': {},
            'activity_purposes': {}
        }
    
    # Merge new descriptions and purposes
    data['activity_descriptions'].update(descriptions)
    data['activity_purposes'].update(purposes)
    
    # Save updated data
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    if process_name:
        print(f"✓ Merged {process_name} chunk {chunk_num}: {len(descriptions)} activities")
    else:
        print(f"✓ Merged chunk {chunk_num}: {len(descriptions)} activities")
    print(f"  Total activities analyzed: {len(data['activity_descriptions'])}")

def main():
    """Main workflow for incremental analysis"""
    print("Loading LPD structure...")
    lpd_data = load_lpd_structure()
    
    processes = lpd_data.get('processes', [])
    if not processes:
        print("ERROR: No processes found in lpd_structure.json")
        sys.exit(1)
    
    num_processes = len(processes)
    print(f"Found {num_processes} process(es) to analyze")
    
    # Process each LPD file
    for process_idx, process in enumerate(processes, 1):
        process_name = process.get('process_name', f'Process{process_idx}')
        activities = process.get('activities', [])
        js_blocks = process.get('javascript_blocks', [])
        sql_queries = process.get('sql_queries', [])
        
        # Filter real activities
        real_activities = get_real_activities(activities)
        total_activities = len(real_activities)
        
        print(f"\n{'='*60}")
        print(f"PROCESS {process_idx}/{num_processes}: {process_name}")
        print(f"{'='*60}")
        print(f"Total activities to analyze: {total_activities}")
        print(f"JavaScript blocks: {len(js_blocks)}")
        print(f"SQL queries: {len(sql_queries)}")
        
        # Split into chunks of 10 activities
        chunk_size = 10
        num_chunks = (total_activities + chunk_size - 1) // chunk_size
        
        print(f"\nSplitting into {num_chunks} chunks of {chunk_size} activities each")
        
        for chunk_num in range(num_chunks):
            start_idx = chunk_num * chunk_size
            end_idx = min(start_idx + chunk_size, total_activities)
            chunk = real_activities[start_idx:end_idx]
            
            # Save chunk for AI analysis
            chunk_file = save_chunk_for_analysis(
                chunk_num + 1, 
                chunk, 
                js_blocks, 
                sql_queries,
                process_name if num_processes > 1 else None
            )
            print(f"\n✓ Chunk {chunk_num + 1}/{num_chunks} saved: {chunk_file}")
            print(f"  Activities {start_idx + 1}-{end_idx} of {total_activities}")
            print(f"  Ready for AI analysis")
    
    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    if num_processes == 1:
        print(f"1. Analyze each chunk file (workflow_chunk_1.json to workflow_chunk_N.json)")
        print("2. For each chunk, generate activity_descriptions and activity_purposes")
        print("3. Call merge_chunk_results(chunk_num, descriptions, purposes)")
    else:
        print(f"1. Analyze each chunk file (workflow_chunk_<ProcessName>_N.json)")
        print("2. For each chunk, generate activity_descriptions and activity_purposes")
        print("3. Call merge_chunk_results(chunk_num, descriptions, purposes, process_name='<ProcessName>')")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
