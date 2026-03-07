#!/usr/bin/env python3
"""
Master Orchestrator for Incremental Client Handover Pipeline
Runs all phases with crash-safe incremental processing
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{'=' * 80}")
    print(f"{description}")
    print(f"{'=' * 80}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ FAILED: {description}")
        return False
    else:
        print(f"\n✓ SUCCESS: {description}")
        return True

def check_file_exists(filepath, description):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        size = path.stat().st_size
        print(f"   ✓ {description}: {filepath} ({size} bytes)")
        return True
    else:
        print(f"   ❌ {description}: {filepath} NOT FOUND")
        return False

def main():
    print("\n" + "=" * 80)
    print("INCREMENTAL CLIENT HANDOVER PIPELINE")
    print("Crash-Safe Architecture with Small AI Outputs")
    print("=" * 80)
    
    # Phase 2: Workflow Analysis (Incremental)
    print("\n\n### PHASE 2: WORKFLOW ANALYSIS (INCREMENTAL) ###\n")
    
    if not run_command("python Temp/build_workflow_analysis.py", 
                       "Phase 2.1: Extract workflow chunks"):
        return 1
    
    print("\n   → AI should now analyze workflow chunks")
    print("   → Each chunk analysis should be ~2-3 KB output")
    print("   → After AI analysis, run: python Temp/build_workflow_analysis.py merge")
    
    # Phase 3: Configuration Analysis (Incremental)
    print("\n\n### PHASE 3: CONFIGURATION ANALYSIS (INCREMENTAL) ###\n")
    
    if not run_command("python Temp/build_configuration_analysis.py",
                       "Phase 3.1: Extract configuration chunks"):
        return 1
    
    print("\n   → AI should now analyze configuration chunks")
    print("   → Each chunk analysis should be ~1-2 KB output")
    print("   → After AI analysis, run: python Temp/build_configuration_analysis.py merge")
    
    # Phase 4: Risk Assessment (Incremental)
    print("\n\n### PHASE 4: RISK ASSESSMENT (INCREMENTAL) ###\n")
    
    if not run_command("python Temp/build_risk_assessment.py",
                       "Phase 4.1: Extract risk chunks"):
        return 1
    
    print("\n   → AI should now analyze risk chunks")
    print("   → Each chunk analysis should be ~1-2 KB output (3-5 risks max)")
    print("   → After AI analysis, run: python Temp/build_risk_assessment.py merge")
    
    # Summary
    print("\n\n" + "=" * 80)
    print("PIPELINE SETUP COMPLETE")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. AI analyzes workflow chunks (11 chunks)")
    print("2. AI analyzes configuration chunks (5 categories)")
    print("3. AI analyzes risk chunks (5 categories)")
    print("4. Run merge commands for each phase")
    print("5. Run Phase 5: python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py BayCare APIA")
    print("\nKey Benefits:")
    print("✓ No large AI outputs (all <3 KB)")
    print("✓ No context accumulation")
    print("✓ Crash-safe execution")
    print("✓ Can resume from any point")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
