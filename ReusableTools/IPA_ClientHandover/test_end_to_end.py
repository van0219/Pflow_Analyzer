#!/usr/bin/env python3
"""
End-to-End Integration Test for Client Handover Generation

This script tests the complete stateless pipeline workflow to ensure
all phases work together correctly.

Usage:
    python test_end_to_end.py

Requirements:
    - Test LPD file in Projects/FPI/MatchReport/
    - Test spec file in Projects/FPI/MatchReport/
"""

import sys
import os
import subprocess
import json
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*80}")
    print(f"TEST: {description}")
    print(f"{'='*80}")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✓ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Exit code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ {description} - ERROR: {e}")
        return False


def check_file_exists(filepath, description):
    """Check if a file exists"""
    print(f"\nChecking: {filepath}")
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✓ {description} exists ({size} bytes)")
        return True
    else:
        print(f"✗ {description} missing")
        return False


def validate_json_file(filepath, required_fields):
    """Validate JSON file has required fields"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        missing = [field for field in required_fields if field not in data]
        if missing:
            print(f"✗ {filepath} missing fields: {missing}")
            return False
        
        print(f"✓ {filepath} has all required fields")
        return True
    except Exception as e:
        print(f"✗ Error validating {filepath}: {e}")
        return False


def test_end_to_end():
    """Run complete end-to-end test"""
    print("="*80)
    print("CLIENT HANDOVER END-TO-END INTEGRATION TEST")
    print("="*80)
    
    test_results = []
    
    # Test data
    lpd_file = "Projects/FPI/MatchReport/MatchReport_Outbound.lpd"
    spec_file = "Projects/FPI/MatchReport/ANA-050_Analysis_Outgoing_Match_Report.docx"
    temp_dir = "Temp"
    client = "FPI"
    rice = "MatchReport"
    
    # Phase 0: Preprocessing
    success = run_command(
        ["python", "ReusableTools/IPA_ClientHandover/preprocess_client_handover.py", 
         lpd_file, spec_file, temp_dir],
        "Phase 0: Preprocessing"
    )
    test_results.append(("Phase 0", success))
    
    if not success:
        print("\n✗ Phase 0 failed - cannot continue")
        return False
    
    # Verify Phase 0 outputs
    phase0_files = [
        (f"{temp_dir}/lpd_structure.json", "LPD Structure", ['processes']),
        (f"{temp_dir}/metrics_summary.json", "Metrics Summary", ['total_activities']),
        (f"{temp_dir}/spec_raw.json", "Spec Raw Data", ['metadata'])
    ]
    
    for filepath, desc, required_fields in phase0_files:
        exists = check_file_exists(filepath, desc)
        test_results.append((f"Phase 0 Output: {desc}", exists))
        if exists:
            valid = validate_json_file(filepath, required_fields)
            test_results.append((f"Phase 0 Validation: {desc}", valid))
    
    # Note: Phases 1-4 are manual AI analysis steps in current implementation
    # For testing, we'll use the existing analysis JSONs if they exist
    
    print(f"\n{'='*80}")
    print("NOTE: Phases 1-4 (AI Analysis) are manual steps")
    print("Checking if analysis JSONs exist from previous run...")
    print(f"{'='*80}")
    
    analysis_files = [
        f"{temp_dir}/business_analysis.json",
        f"{temp_dir}/workflow_analysis.json",
        f"{temp_dir}/configuration_analysis.json",
        f"{temp_dir}/risk_assessment.json"
    ]
    
    all_analysis_exist = all(os.path.exists(f) for f in analysis_files)
    
    if not all_analysis_exist:
        print("\n⚠ Analysis JSONs not found - skipping Phase 5 test")
        print("Run Phases 1-4 manually to complete the test")
        test_results.append(("Phases 1-4 Analysis JSONs", False))
    else:
        print("\n✓ All analysis JSONs found")
        test_results.append(("Phases 1-4 Analysis JSONs", True))
        
        # Validate analysis JSONs
        success = run_command(
            ["python", "ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py", temp_dir],
            "Validate Analysis JSONs"
        )
        test_results.append(("JSON Validation", success))
        
        # Phase 5: Report Assembly
        success = run_command(
            ["python", "ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py",
             client, rice, temp_dir],
            "Phase 5: Report Assembly"
        )
        test_results.append(("Phase 5", success))
        
        # Verify report generated
        report_path = f"Client_Handover_Results/{client}_{rice}.xlsx"
        exists = check_file_exists(report_path, "Final Report")
        test_results.append(("Final Report", exists))
    
    # Print summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}\n")
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*80}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*80}")
    
    return passed == total


if __name__ == "__main__":
    success = test_end_to_end()
    sys.exit(0 if success else 1)
