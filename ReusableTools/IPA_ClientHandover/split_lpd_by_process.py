#!/usr/bin/env python3
"""
Split combined LPD structure into individual process files for Phase 2 analysis.

This enables per-process activity description generation, preventing context
overload when analyzing multiple large processes.

Usage:
    python split_lpd_by_process.py
    
Output:
    Temp/lpd_process_1.json
    Temp/lpd_process_2.json
    Temp/lpd_process_3.json
"""

import json
from pathlib import Path

def split_lpd_by_process(input_file="Temp/lpd_structure.json", output_dir="Temp"):
    """Split combined LPD structure into individual process files"""
    
    # Load combined structure
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    processes = data.get('processes', [])
    
    if not processes:
        print("⚠ No processes found in lpd_structure.json")
        return []
    
    output_files = []
    
    for i, process in enumerate(processes, 1):
        # Create individual process file
        process_data = {
            "processes": [process],
            "summary": {
                "total_processes": 1,
                "total_activities": process.get('activity_count', 0),
                "total_javascript_blocks": len(process.get('javascript_blocks', [])),
                "total_sql_queries": len(process.get('sql_queries', []))
            }
        }
        
        output_file = f"{output_dir}/lpd_process_{i}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(process_data, f, indent=2, ensure_ascii=False)
        
        output_files.append(output_file)
        
        print(f"✓ Process {i}: {process.get('process_name', 'Unknown')}")
        print(f"  Activities: {process.get('activity_count', 0)}")
        print(f"  Output: {output_file}")
    
    return output_files

if __name__ == "__main__":
    print("=" * 80)
    print("SPLITTING LPD STRUCTURE BY PROCESS")
    print("=" * 80)
    print()
    
    output_files = split_lpd_by_process()
    
    print()
    print("=" * 80)
    print(f"SPLIT COMPLETE - {len(output_files)} process files created")
    print("=" * 80)
    print()
    print("Next step: Run Phase 2 analysis on each process file individually")
