#!/usr/bin/env python3
"""
IPA Client Handover Report Generator

Automatically loads consolidated documentation and generates the client handover report.
Handles both single and multiple processes (backward compatible).

Usage:
    python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py <rice_item> <client_name> <rice_item>

Example (single process):
    python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py MatchReport FPI MatchReport

Example (multiple processes):
    python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py APIA BayCare APIA
"""

import sys
import json
import os

def generate_report(rice_item, client_name, rice_item_name):
    """
    Generate client handover report from consolidated documentation.
    Handles both single and multiple processes (backward compatible).
    
    Args:
        rice_item: RICE item name (e.g., 'MatchReport' or 'APIA')
        client_name: Client name (e.g., 'FPI' or 'BayCare')
        rice_item_name: RICE item name (same as rice_item, for compatibility)
    
    Returns:
        Path to generated report
    """
    
    # Add workspace root to path for template import
    sys.path.insert(0, '.')
    
    try:
        from ipa_client_handover_template import generate_report as generate_excel_report
    except ImportError:
        print("❌ Error: Could not import ipa_client_handover_template")
        print("   Make sure you're running from workspace root")
        sys.exit(1)
    
    # Load consolidated documentation
    temp_dir = 'Temp'
    consolidated_path = f'{temp_dir}/{rice_item}_consolidated_documentation.json'
    
    if not os.path.exists(consolidated_path):
        print(f"❌ Error: Consolidated documentation not found: {consolidated_path}")
        print("   Run consolidate_processes.py first")
        sys.exit(1)
    
    try:
        with open(consolidated_path, 'r', encoding='utf-8') as f:
            consolidated = json.load(f)
        print(f"✓ Loaded: {consolidated_path}")
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing {consolidated_path}: {e}")
        print(f"   File may be incomplete or corrupted")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading {consolidated_path}: {e}")
        sys.exit(1)
    
    # Build ipa_data structure for template
    # Extract process details for template
    processes = []
    for process in consolidated.get('processes', []):
        process_data = {
            'name': process.get('name', 'Unknown'),
            'file': f"{process.get('name', 'Unknown')}.lpd",
            'activity_count': process.get('activity_count', 0),
            'activities': process.get('activity_guide', {}).get('activities', []),
            'config_variables': process.get('configuration', {}).get('config_variables', [])
        }
        processes.append(process_data)
    
    # Build ipa_data with consolidated information
    # For single process, use process-level validation and config
    # For multiple processes, aggregate from all processes
    process_list = consolidated.get('processes', [])
    
    # Get validation data (prefer process-level if available)
    if len(process_list) == 1 and process_list[0].get('validation'):
        production_validation = process_list[0].get('validation', {})
    else:
        production_validation = consolidated.get('validation', {})
    
    # Get configuration variables (prefer process-level if available)
    if len(process_list) == 1 and process_list[0].get('configuration', {}).get('config_variables'):
        config_variables = process_list[0].get('configuration', {}).get('config_variables', [])
    else:
        config_variables = consolidated.get('configuration', {}).get('config_variables', [])
    
    ipa_data = {
        'client_name': client_name,
        'process_group': rice_item_name,
        'processes': processes,
        'business_requirements': consolidated.get('business_requirements', {}),
        'production_validation': production_validation,
        'config_variables': config_variables,
        'maintenance_guide': {
            'configuration': consolidated.get('configuration', {}),
            'activity_guide': consolidated.get('activity_guide', {})
        },
        'workflow_steps': consolidated.get('workflow', {}).get('processes', [{}])[0].get('workflow_steps', []) if consolidated.get('workflow', {}).get('processes') else []
    }
    
    # Add process details for executive summary
    ipa_data['process_details'] = {
        'RICE Item': rice_item_name,
        'Client': client_name,
        'Process Count': len(processes),
        'Total Activities': consolidated.get('metadata', {}).get('total_activities', 0),
        'Documentation Date': consolidated.get('metadata', {}).get('generated_date', 'N/A')
    }
    
    # Add key features (extract from business requirements or use defaults)
    business_req = consolidated.get('business_requirements', {})
    if 'requirements' in business_req and business_req['requirements']:
        requirements_list = business_req['requirements']
        if isinstance(requirements_list[0], dict):
            # New format: extract titles from structured requirements
            ipa_data['key_features'] = [req.get('title', 'Feature') for req in requirements_list[:5]]
        else:
            # Old format: use as-is
            ipa_data['key_features'] = [req[0] if isinstance(req, (list, tuple)) else req for req in requirements_list[:5]]
    else:
        ipa_data['key_features'] = [
            'Automated data processing',
            'Real-time validation',
            'Error handling and recovery',
            'Audit trail and logging'
        ]
    
    # Add requirements for Business Requirements sheet
    # Pass structured requirements directly to template (no transformation)
    if 'requirements' in business_req:
        ipa_data['requirements'] = business_req['requirements']
    else:
        ipa_data['requirements'] = []
    
    # Generate report
    try:
        output_path = generate_excel_report(ipa_data)
        print(f"\n✓ Report generated successfully: {output_path}")
        print(f"  Processes documented: {len(processes)}")
        print(f"  Total activities: {consolidated.get('metadata', {}).get('total_activities', 0)}")
        return output_path
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py <rice_item> <client_name> <rice_item>")
        print("\nExample (single process):")
        print("  python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py MatchReport FPI MatchReport")
        print("\nExample (multiple processes):")
        print("  python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py APIA BayCare APIA")
        sys.exit(1)
    
    rice_item = sys.argv[1]
    client_name = sys.argv[2]
    rice_item_name = sys.argv[3]
    
    generate_report(rice_item, client_name, rice_item_name)
