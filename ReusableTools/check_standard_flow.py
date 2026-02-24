#!/usr/bin/env python3
"""
Check if an IPA process is a standard flow that should not be modified.

Usage:
    from ReusableTools.check_standard_flow import check_standard_flow
    
    result = check_standard_flow('MatchReport_Outbound.lpd')
    if result['is_standard']:
        print(f"WARNING: {result['flow_name']} is a standard flow!")
"""

import csv
import os


def check_standard_flow(lpd_filename, csv_path='Application+Defined+Processes.csv'):
    """
    Check if an LPD file is a standard flow.
    
    Args:
        lpd_filename: Name of the LPD file (e.g., 'MatchReport_Outbound.lpd')
        csv_path: Path to the standard flows CSV file
        
    Returns:
        dict: {
            'is_standard': bool,
            'flow_name': str or None,
            'description': str or None,
            'message': str
        }
    """
    # Remove .lpd extension for comparison
    base_name = lpd_filename.replace('.lpd', '')
    
    # Check if CSV file exists
    if not os.path.exists(csv_path):
        return {
            'is_standard': False,
            'flow_name': None,
            'description': None,
            'message': f'Standard flows CSV not found: {csv_path}'
        }
    
    # Read CSV and check for match
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Check PfiFlowDefinition column
                flow_def = row.get('PfiFlowDefinition', '').strip()
                
                if flow_def and flow_def == base_name:
                    return {
                        'is_standard': True,
                        'flow_name': flow_def,
                        'description': row.get('PfiFlowDescription', '').strip(),
                        'message': f'⚠️ WARNING: "{base_name}" is a STANDARD FLOW and should NOT be modified. Copy and rename if customization is needed.'
                    }
        
        # Not found in standard flows
        return {
            'is_standard': False,
            'flow_name': None,
            'description': None,
            'message': f'✓ "{base_name}" is a custom flow (not in standard flows list)'
        }
        
    except Exception as e:
        return {
            'is_standard': False,
            'flow_name': None,
            'description': None,
            'message': f'Error reading CSV: {str(e)}'
        }


def check_multiple_flows(lpd_files, csv_path='Application+Defined+Processes.csv'):
    """
    Check multiple LPD files against standard flows.
    
    Args:
        lpd_files: List of LPD filenames
        csv_path: Path to the standard flows CSV file
        
    Returns:
        dict: {
            'standard_flows': list of dicts,
            'custom_flows': list of dicts,
            'summary': str
        }
    """
    standard_flows = []
    custom_flows = []
    
    for lpd_file in lpd_files:
        result = check_standard_flow(lpd_file, csv_path)
        
        if result['is_standard']:
            standard_flows.append({
                'filename': lpd_file,
                'flow_name': result['flow_name'],
                'description': result['description']
            })
        else:
            custom_flows.append({
                'filename': lpd_file,
                'message': result['message']
            })
    
    # Build summary
    summary_lines = []
    if standard_flows:
        summary_lines.append(f'⚠️ Found {len(standard_flows)} STANDARD FLOW(S) - DO NOT MODIFY:')
        for flow in standard_flows:
            summary_lines.append(f'  - {flow["filename"]} ({flow["description"]})')
    
    if custom_flows:
        summary_lines.append(f'✓ Found {len(custom_flows)} custom flow(s):')
        for flow in custom_flows:
            summary_lines.append(f'  - {flow["filename"]}')
    
    return {
        'standard_flows': standard_flows,
        'custom_flows': custom_flows,
        'summary': '\n'.join(summary_lines)
    }


if __name__ == '__main__':
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print('Usage: python check_standard_flow.py <lpd_filename>')
        print('Example: python check_standard_flow.py MatchReport_Outbound.lpd')
        sys.exit(1)
    
    lpd_file = sys.argv[1]
    result = check_standard_flow(lpd_file)
    
    print(result['message'])
    
    if result['is_standard']:
        print(f'\nFlow Name: {result["flow_name"]}')
        print(f'Description: {result["description"]}')
        sys.exit(1)  # Exit with error code for standard flows
    else:
        sys.exit(0)  # Success for custom flows
