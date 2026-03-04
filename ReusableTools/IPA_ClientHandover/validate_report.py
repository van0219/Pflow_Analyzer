#!/usr/bin/env python3
"""
Validate Client Handover Report Completeness

This script validates that all sheets in the generated client handover report
contain the expected data and are not blank.
"""

import sys
import pandas as pd
from pathlib import Path


def validate_report(report_path):
    """
    Validate client handover report completeness.
    
    Returns:
        dict: Validation results with status and issues
    """
    results = {
        'valid': True,
        'issues': [],
        'warnings': [],
        'sheet_status': {}
    }
    
    try:
        xl = pd.ExcelFile(report_path)
        sheet_names = xl.sheet_names
        
        print(f"\n{'='*80}")
        print(f"VALIDATING CLIENT HANDOVER REPORT")
        print(f"{'='*80}\n")
        print(f"Report: {report_path}")
        print(f"Total Sheets: {len(sheet_names)}\n")
        
        # Expected sheets and their minimum row requirements
        expected_sheets = {
            '📊 Executive Summary': {'min_rows': 10, 'critical': True},
            '📋 Business Requirements': {'min_rows': 5, 'critical': True},
            '✅ Production Validation': {'min_rows': 10, 'critical': False},
            '⚙️ System Configuration': {'min_rows': 10, 'critical': True},
            '📚 Activity Node Guide': {'min_rows': 5, 'critical': True},
            '🔧 Maintenance Guide': {'min_rows': 10, 'critical': True}
        }
        
        # Validate each expected sheet
        for sheet_name, requirements in expected_sheets.items():
            if sheet_name not in sheet_names:
                issue = f"❌ Missing sheet: {sheet_name}"
                results['issues'].append(issue)
                results['valid'] = False
                results['sheet_status'][sheet_name] = 'MISSING'
                print(issue)
                continue
            
            # Read sheet and check row count
            df = pd.read_excel(report_path, sheet_name=sheet_name, header=None)
            row_count = len(df)
            non_empty_rows = df.dropna(how='all').shape[0]
            
            # Check if sheet has minimum required rows
            if non_empty_rows < requirements['min_rows']:
                severity = "❌" if requirements['critical'] else "⚠️"
                issue = f"{severity} {sheet_name}: Only {non_empty_rows} non-empty rows (expected >= {requirements['min_rows']})"
                
                if requirements['critical']:
                    results['issues'].append(issue)
                    results['valid'] = False
                    results['sheet_status'][sheet_name] = 'INCOMPLETE'
                else:
                    results['warnings'].append(issue)
                    results['sheet_status'][sheet_name] = 'WARNING'
                
                print(issue)
            else:
                results['sheet_status'][sheet_name] = 'OK'
                print(f"✓ {sheet_name}: {non_empty_rows} rows")
        
        # Check for Process sheets (should have at least one)
        process_sheets = [s for s in sheet_names if s.startswith('⚙️ Process_')]
        if not process_sheets:
            issue = "❌ No Process sheets found"
            results['issues'].append(issue)
            results['valid'] = False
            print(f"\n{issue}")
        else:
            print(f"\n✓ Found {len(process_sheets)} Process sheet(s)")
            for process_sheet in process_sheets:
                df = pd.read_excel(report_path, sheet_name=process_sheet, header=None)
                non_empty_rows = df.dropna(how='all').shape[0]
                if non_empty_rows < 10:
                    issue = f"⚠️ {process_sheet}: Only {non_empty_rows} rows"
                    results['warnings'].append(issue)
                    print(f"  {issue}")
                else:
                    print(f"  ✓ {process_sheet}: {non_empty_rows} rows")
        
        # Specific content validation
        print(f"\n{'='*80}")
        print("CONTENT VALIDATION")
        print(f"{'='*80}\n")
        
        # Validate Business Requirements has actual requirements
        if '📋 Business Requirements' in sheet_names:
            df = pd.read_excel(report_path, sheet_name='📋 Business Requirements', header=None)
            # Check for "Total Requirements:" text and extract the number
            total_req_text = df.astype(str).apply(lambda x: x.str.contains('Total Requirements:', case=False).any(), axis=1)
            if total_req_text.any():
                req_row_idx = total_req_text.idxmax()
                req_row = str(df.iloc[req_row_idx, 0])
                # Extract number from "Total Requirements: N"
                import re
                match = re.search(r'Total Requirements:\s*(\d+)', req_row)
                if match:
                    req_count = int(match.group(1))
                    if req_count == 0:
                        issue = "❌ Business Requirements sheet shows 'Total Requirements: 0'"
                        results['issues'].append(issue)
                        results['valid'] = False
                        print(issue)
                    else:
                        print(f"✓ Business Requirements has {req_count} requirements")
                else:
                    print("⚠️ Could not parse Business Requirements count")
            else:
                print("⚠️ Could not verify Business Requirements count")
        
        # Validate System Configuration has config variables
        if '⚙️ System Configuration' in sheet_names:
            df = pd.read_excel(report_path, sheet_name='⚙️ System Configuration', header=None)
            # Look for OAuth or Interface config variables
            has_config = df.astype(str).apply(lambda x: x.str.contains('Interface\\.|OAuth|API_AuthCred', case=False).any(), axis=1).any()
            if has_config:
                config_count = df.astype(str).apply(lambda x: x.str.contains('Interface\\.|API_AuthCred', case=False).any(), axis=1).sum()
                print(f"✓ System Configuration has {config_count} configuration variables")
            else:
                issue = "❌ System Configuration appears to be empty"
                results['issues'].append(issue)
                results['valid'] = False
                print(issue)
        
        # Validate Production Validation (if present)
        if '✅ Production Validation' in sheet_names:
            df = pd.read_excel(report_path, sheet_name='✅ Production Validation', header=None)
            has_test_results = df.astype(str).apply(lambda x: x.str.contains('Test Case|Pass|Fail', case=False).any(), axis=1).any()
            if has_test_results:
                print("✓ Production Validation has test results")
            else:
                warning = "⚠️ Production Validation may be incomplete (no test results found)"
                results['warnings'].append(warning)
                print(warning)
        
        # Summary
        print(f"\n{'='*80}")
        print("VALIDATION SUMMARY")
        print(f"{'='*80}\n")
        
        if results['valid']:
            print("✅ REPORT IS VALID - All critical sections have data")
        else:
            print("❌ REPORT HAS ISSUES - See details above")
        
        if results['issues']:
            print(f"\nCritical Issues ({len(results['issues'])}):")
            for issue in results['issues']:
                print(f"  {issue}")
        
        if results['warnings']:
            print(f"\nWarnings ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"  {warning}")
        
        print()
        
    except Exception as e:
        results['valid'] = False
        results['issues'].append(f"Error reading report: {str(e)}")
        print(f"\n❌ ERROR: {str(e)}\n")
    
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_report.py <report_path>")
        sys.exit(1)
    
    report_path = sys.argv[1]
    
    if not Path(report_path).exists():
        print(f"Error: Report file not found: {report_path}")
        sys.exit(1)
    
    results = validate_report(report_path)
    
    # Exit with appropriate code
    sys.exit(0 if results['valid'] else 1)


if __name__ == "__main__":
    main()
