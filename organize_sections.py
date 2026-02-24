#!/usr/bin/env python3

import subprocess
import sys
import os

def main():
    # Execute the organize by sections command
    cmd = [
        "python", 
        "ReusableTools/IPA_ClientHandover/organize_by_sections.py",
        "Temp/MatchReport_Outbound_lpd_data.json",
        "Temp/MatchReport_spec_data.json", 
        "Temp/MatchReport_Outbound_wu_data.json",
        "Temp/MatchReport_Outbound"
    ]
    
    print("Executing command:")
    print(" ".join(cmd))
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        # Verify output files were created
        expected_files = [
            "Temp/MatchReport_Outbound_section_business.json",
            "Temp/MatchReport_Outbound_section_workflow.json", 
            "Temp/MatchReport_Outbound_section_configuration.json",
            "Temp/MatchReport_Outbound_section_activities.json",
            "Temp/MatchReport_Outbound_section_validation.json"
        ]
        
        print("\nVerifying output files:")
        all_created = True
        for file_path in expected_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✓ {file_path} ({size} bytes)")
            else:
                print(f"✗ {file_path} - NOT FOUND")
                all_created = False
        
        if all_created:
            print("\n✅ All 5 section files created successfully!")
        else:
            print("\n❌ Some section files were not created")
            
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()