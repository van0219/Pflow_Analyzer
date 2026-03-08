#!/usr/bin/env python3
"""
Batch Coding Standards Analysis
Runs complete coding standards workflow for multiple LPD files sequentially.

Usage:
    python batch_coding_standards.py <client> <rice> <lpd1> <lpd2> <lpd3> ...
    
Example:
    python batch_coding_standards.py BayCare APIA *.lpd
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


def run_single_process(client, rice, lpd_path):
    """Run complete coding standards workflow for a single LPD file."""
    lpd_file = Path(lpd_path)
    process_name = lpd_file.stem
    
    print("\n" + "=" * 80)
    print(f"PROCESSING: {lpd_file.name}")
    print("=" * 80)
    
    try:
        # Phase 0: Preprocessing
        print("\n→ Phase 0: Preprocessing...")
        result = subprocess.run(
            ["python", "ReusableTools/IPA_CodingStandards/preprocess_coding_standards.py", 
             str(lpd_file), client],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Phase 0 failed: {result.stderr}")
            return False
        print("✓ Phase 0 complete")
        
        # Note: Phases 1-5 are AI-driven and should be handled by the agent
        # This script only handles the Python preprocessing and assembly
        
        # Phase 6: Report Assembly
        print("\n→ Phase 6: Report Assembly...")
        result = subprocess.run(
            ["python", "ReusableTools/IPA_CodingStandards/assemble_coding_standards_report.py",
             client, rice, process_name],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Phase 6 failed: {result.stderr}")
            return False
        
        # Extract report path from output
        for line in result.stdout.split('\n'):
            if 'Report:' in line or '.xlsx' in line:
                print(f"✓ {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {lpd_file.name}: {e}")
        return False


def main():
    if len(sys.argv) < 4:
        print("Usage: python batch_coding_standards.py <client> <rice> <lpd1> <lpd2> ...")
        print("\nExample:")
        print("  python batch_coding_standards.py BayCare APIA Projects/BayCare/APIA/*.lpd")
        sys.exit(1)
    
    client = sys.argv[1]
    rice = sys.argv[2]
    lpd_files = sys.argv[3:]
    
    print("=" * 80)
    print("BATCH CODING STANDARDS ANALYSIS")
    print("=" * 80)
    print(f"\nClient: {client}")
    print(f"RICE: {rice}")
    print(f"Processes: {len(lpd_files)}")
    print(f"Estimated time: ~{len(lpd_files) * 10} minutes")
    
    start_time = datetime.now()
    results = []
    
    for i, lpd_file in enumerate(lpd_files, 1):
        print(f"\n\n{'=' * 80}")
        print(f"PROCESS {i} of {len(lpd_files)}")
        print(f"{'=' * 80}")
        
        success = run_single_process(client, rice, lpd_file)
        results.append((Path(lpd_file).name, success))
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 80)
    print(f"\nTotal time: {duration}")
    print(f"Successful: {sum(1 for _, s in results if s)}/{len(results)}")
    
    print("\nResults:")
    for lpd_name, success in results:
        status = "✓" if success else "❌"
        print(f"  {status} {lpd_name}")
    
    # Exit with error code if any failed
    if not all(s for _, s in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
