#!/usr/bin/env python3
"""
Incremental Workflow Analysis Builder for Multi-Process RICE Items
Processes activities in chunks to avoid context overload
"""

import json
import sys
from pathlib import Path

def load_process_structures():
    """Load all three LPD process structures"""
    processes = []
    for i in range(1, 4):
        lpd_file = Path(f"Temp/lpd_process_{i}.json")
        if lpd_file.exists():
            with open(lpd_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                processes.append(data)
        else:
            print(f"Warning: {lpd_file} not found")
    return processes

def extract_activities_chunk(processes, start_idx, chunk_size=50):
    """Extract a chunk of activities from all processes"""
    all_activities = []
    
    for proc_idx, process_data in enumerate(processes, 1):
        # Handle nested structure: {"processes": [{"process_name": "...", "activities": [...]}]}
        if 'processes' in process_data:
            process_list = process_data['processes']
        else:
            process_list = [process_data]
        
        for process in process_list:
            proc_name = process.get('process_name', process.get('name', f'Process_{proc_idx}'))
            activities = process.get('activities', [])
            
            for activity in activities:
                activity['process_name'] = proc_name
                activity['process_index'] = proc_idx
                all_activities.append(activity)
    
    # Return chunk
    end_idx = min(start_idx + chunk_size, len(all_activities))
    chunk = all_activities[start_idx:end_idx]
    
    return chunk, len(all_activities)

def main():
    print("=" * 80)
    print("WORKFLOW ANALYSIS BUILDER - INCREMENTAL MODE")
    print("=" * 80)
    
    # Load all process structures
    print("\n[1/4] Loading process structures...")
    processes = load_process_structures()
    print(f"   ✓ Loaded {len(processes)} processes")
    
    # Count total activities
    total_activities = 0
    for p in processes:
        if 'processes' in p:
            for proc in p['processes']:
                total_activities += len(proc.get('activities', []))
        else:
            total_activities += len(p.get('activities', []))
    print(f"   ✓ Total activities: {total_activities}")
    
    # Initialize output structure
    workflow_analysis = {
        "activity_descriptions": {},
        "activity_purposes": {},
        "workflow_steps": [],
        "approval_paths": [],
        "exception_handling": []
    }
    
    # Process in chunks
    chunk_size = 50
    current_idx = 0
    chunk_num = 1
    
    print(f"\n[2/4] Processing activities in chunks of {chunk_size}...")
    
    while current_idx < total_activities:
        chunk, total = extract_activities_chunk(processes, current_idx, chunk_size)
        
        if not chunk:
            break
        
        print(f"\n   Chunk {chunk_num}: Activities {current_idx + 1} to {current_idx + len(chunk)}")
        print(f"   Saving chunk data to: Temp/workflow_chunk_{chunk_num}.json")
        
        # Save chunk for AI analysis
        chunk_file = Path(f"Temp/workflow_chunk_{chunk_num}.json")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            json.dump({
                "chunk_number": chunk_num,
                "start_index": current_idx,
                "end_index": current_idx + len(chunk),
                "total_activities": total,
                "activities": chunk
            }, f, indent=2)
        
        print(f"   ✓ Chunk {chunk_num} ready for AI analysis")
        print(f"   → AI should analyze this chunk and return descriptions")
        
        current_idx += len(chunk)
        chunk_num += 1
    
    print(f"\n[3/4] Created {chunk_num - 1} chunks for analysis")
    print(f"\n[4/4] Next steps:")
    print(f"   1. AI analyzes each chunk file (workflow_chunk_N.json)")
    print(f"   2. AI returns activity_descriptions and activity_purposes for each chunk")
    print(f"   3. This script merges all chunks into workflow_analysis.json")
    print(f"\n   Run: python Temp/build_workflow_analysis.py merge")
    
    return 0

def merge_chunks():
    """Merge analyzed chunks into final workflow_analysis.json"""
    print("=" * 80)
    print("MERGING WORKFLOW ANALYSIS CHUNKS")
    print("=" * 80)
    
    workflow_analysis = {
        "activity_descriptions": {},
        "activity_purposes": {},
        "workflow_steps": [],
        "approval_paths": [],
        "exception_handling": []
    }
    
    chunk_num = 1
    merged_count = 0
    
    while True:
        chunk_file = Path(f"Temp/workflow_chunk_{chunk_num}_analyzed.json")
        if not chunk_file.exists():
            break
        
        print(f"\n   Merging chunk {chunk_num}...")
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
        
        # Merge descriptions and purposes
        if 'activity_descriptions' in chunk_data:
            workflow_analysis['activity_descriptions'].update(chunk_data['activity_descriptions'])
            merged_count += len(chunk_data['activity_descriptions'])
        
        if 'activity_purposes' in chunk_data:
            workflow_analysis['activity_purposes'].update(chunk_data['activity_purposes'])
        
        chunk_num += 1
    
    print(f"\n   ✓ Merged {chunk_num - 1} chunks")
    print(f"   ✓ Total activity descriptions: {merged_count}")
    
    # Save final output
    output_file = Path("Temp/workflow_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow_analysis, f, indent=2)
    
    print(f"\n   ✓ Written: {output_file}")
    print("\n" + "=" * 80)
    print("PHASE 2 COMPLETE")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "merge":
        sys.exit(merge_chunks())
    else:
        sys.exit(main())
