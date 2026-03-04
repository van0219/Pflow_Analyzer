#!/usr/bin/env python3
"""
Review Client Handover Report

This script reviews a generated client handover Excel report to verify data completeness.
It checks each sheet for content and warns about empty or minimal data.

Usage:
    python review_client_handover_report.py <report_file>
    python review_client_handover_report.py Client_Handover_Results/FPI_MatchReport.xlsx

Returns:
    Exit code 0 if all sheets have content
    Exit code 1 if any sheet has minimal data
"""

import sys
import os
import pandas as pd
from pathlib import Path


def review_report(report_path):
    """Review client handover report for data completeness"""
    
    if not os.path.exists(report_path):
        print(f"❌ Error: Report file not found: {report_path}")
        return 1
    
    print("=" * 80)
    print("CLIENT HANDOVER REPORT REVIEW")
    print("=" * 80)
    print(f"\nReport: {report_path}")
    print()
    
    try:
        xl = pd.ExcelFile(report_path)
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return 1
    
    all_good = True
    warnings = []
    
    for i, sheet_name in enumerate(xl.sheet_names):
        try:
            df = pd.read_excel(report_path, sheet_name=i)
            row_count = len(df)
            col_count = len(df.columns)
            
            print(f"{i+1}. {sheet_name}")
            print(f"   Rows: {row_count}, Columns: {col_count}")
            
            # Check for empty sheets (only headers or minimal data)
            if row_count <= 3:
                print(f"   ⚠️  WARNING: Sheet appears to have minimal data")
                warnings.append(f"{sheet_name}: Only {row_count} rows")
                all_good = False
            else:
                print(f"   ✓ Sheet has content")
            print()
            
        except Exception as e:
            print(f"   ❌ Error reading sheet: {e}")
            warnings.append(f"{sheet_name}: Read error")
            all_good = False
            print()
    
    print("=" * 80)
    
    if all_good:
        print("✅ ALL SHEETS HAVE CONTENT")
        print("=" * 80)
        print("\nReport is ready for client delivery.")
        return 0
    else:
        print("⚠️  SOME SHEETS HAVE MINIMAL DATA")
        print("=" * 80)
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")
        print("\nRecommended actions:")
        print("  1. Check Phase 5 debug output for data counts")
        print("  2. Inspect analysis JSONs for missing fields")
        print("  3. Run validation script: python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py")
        print("  4. Fix data structure issues in analysis JSONs")
        print("  5. Regenerate report")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python review_client_handover_report.py <report_file>")
        print("\nExample:")
        print("  python review_client_handover_report.py Client_Handover_Results/FPI_MatchReport.xlsx")
        sys.exit(1)
    
    report_path = sys.argv[1]
    exit_code = review_report(report_path)
    sys.exit(exit_code)
