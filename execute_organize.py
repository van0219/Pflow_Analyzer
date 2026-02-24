#!/usr/bin/env python3

import subprocess
import sys
import os

# Change to the correct directory and execute
try:
    result = subprocess.run([
        "python", 
        "ReusableTools/IPA_ClientHandover/organize_by_sections.py",
        "Temp/MatchReport_Outbound_lpd_data.json",
        "Temp/MatchReport_spec_data.json", 
        "Temp/MatchReport_Outbound_wu_data.json",
        "Temp/MatchReport_Outbound"
    ], capture_output=True, text=True, cwd=".")
    
    print("Command output:")
    print(result.stdout)
    
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    print(f"Return code: {result.returncode}")
    
    # Check if files were created
    expected_files = [
        "Temp/MatchReport_Outbound_section_business.json",
        "Temp/MatchReport_Outbound_section_workflow.json", 
        "Temp/MatchReport_Outbound_section_configuration.json",
        "Temp/MatchReport_Outbound_section_activities.json",
        "Temp/MatchReport_Outbound_section_validation.json"
    ]
    
    print("\nFile verification:")
    for file_path in expected_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} - NOT FOUND")

except Exception as e:
    print(f"Error executing command: {e}")