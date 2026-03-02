#!/usr/bin/env python3
"""
Phase 5: Client Handover Report Assembly
Stateless pipeline architecture - Merge JSON outputs and generate Excel report.

This script:
- Merges all analysis phase JSON outputs
- Prepares ipa_data dictionary for template
- Calls existing template to generate Excel report
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ipa_client_handover_template import generate_report


def assemble_client_handover_report(client_name, rice_item, temp_dir="Temp", output_dir="Client_Handover_Results"):
    """
    Phase 5: Assemble client handover report from analysis JSON files.
    
    Args:
        client_name: Client name (e.g., "FPI")
        rice_item: RICE item name (e.g., "MatchReport")
        temp_dir: Directory containing JSON files from phases 1-4
        output_dir: Output directory for Excel report
    
    Returns:
        str: Path to generated Excel report
    """
    print("=" * 80)
    print("PHASE 5: CLIENT HANDOVER REPORT ASSEMBLY")
    print("=" * 80)
    
    # Load all JSON outputs from phases 1-4
    print("\n[1/3] Loading analysis outputs...")
    
    business_analysis = load_json(os.path.join(temp_dir, "business_analysis.json"))
    workflow_analysis = load_json(os.path.join(temp_dir, "workflow_analysis.json"))
    configuration_analysis = load_json(os.path.join(temp_dir, "configuration_analysis.json"))
    risk_assessment = load_json(os.path.join(temp_dir, "risk_assessment.json"))
    
    # Load raw data for reference
    lpd_structure = load_json(os.path.join(temp_dir, "lpd_structure.json"))
    metrics_summary = load_json(os.path.join(temp_dir, "metrics_summary.json"))
    
    print("   ✓ All analysis files loaded")
    
    # Build ipa_data dictionary for template
    print("\n[2/3] Building ipa_data structure...")
    ipa_data = build_ipa_data(
        client_name=client_name,
        rice_item=rice_item,
        business_analysis=business_analysis,
        workflow_analysis=workflow_analysis,
        configuration_analysis=configuration_analysis,
        risk_assessment=risk_assessment,
        lpd_structure=lpd_structure,
        metrics_summary=metrics_summary
    )
    
    print("   ✓ ipa_data structure built")
    
    # Generate Excel report using existing template
    print("\n[3/3] Generating Excel report...")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = generate_report(ipa_data)
    
    print("\n" + "=" * 80)
    print("PHASE 5 COMPLETE")
    print("=" * 80)
    print(f"\nGenerated report: {output_path}")
    
    return output_path


def load_json(filepath):
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"   ⚠ Warning: {filepath} not found, using empty dict")
        return {}
    except json.JSONDecodeError as e:
        print(f"   ⚠ Warning: {filepath} has invalid JSON: {e}")
        return {}


def build_ipa_data(client_name, rice_item, business_analysis, workflow_analysis, 
                   configuration_analysis, risk_assessment, lpd_structure, metrics_summary):
    """
    Build ipa_data dictionary for template.
    
    This function transforms the stateless pipeline outputs into the format
    expected by the existing ipa_client_handover_template.py
    """
    
    # Extract process information from LPD structure
    processes = lpd_structure.get('processes', [])
    
    # Build process details for executive summary
    process_details = {
        'Client': client_name,
        'RICE Item': rice_item,
        'Process Count': len(processes),
        'Total Activities': metrics_summary.get('total_activities', 0),
        'Report Date': datetime.now().strftime('%B %d, %Y')
    }
    
    # Add integration details if available
    if metrics_summary.get('data_fabric_usage'):
        process_details['Data Fabric'] = 'Yes'
    if metrics_summary.get('idm_integration'):
        process_details['IDM Integration'] = 'Yes'
    if metrics_summary.get('web_services'):
        process_details['Web Services'] = len(metrics_summary['web_services'])
    
    # Build business requirements section
    business_requirements = {
        'overview': business_analysis.get('business_objectives', {}).get('overview', ''),
        'objectives': business_analysis.get('business_objectives', {}).get('objectives', []),
        'requirements': business_analysis.get('functional_requirements', []),
        'stakeholders': business_analysis.get('stakeholders', []),
        'integrations': business_analysis.get('integration_touchpoints', [])
    }
    
    # Build configuration variables section
    config_variables = []
    for config in configuration_analysis.get('configuration_items', []):
        config_variables.append({
            'name': config.get('name', ''),
            'type': config.get('type', ''),
            'description': config.get('description', ''),
            'default_value': config.get('default_value', ''),
            'modification_instructions': config.get('modification_instructions', '')
        })
    
    # Build activity guide section
    activity_guide = []
    for process in processes:
        for activity in process.get('activities', []):
            activity_guide.append({
                'id': activity.get('id', ''),
                'caption': activity.get('caption', ''),
                'type': activity.get('type', ''),
                'description': workflow_analysis.get('activity_descriptions', {}).get(activity.get('id', ''), ''),
                'business_purpose': workflow_analysis.get('activity_purposes', {}).get(activity.get('id', ''), '')
            })
    
    # Build maintenance guide section
    maintenance_guide = {
        'common_modifications': configuration_analysis.get('common_modifications', []),
        'troubleshooting': risk_assessment.get('troubleshooting_guide', []),
        'best_practices': risk_assessment.get('best_practices', []),
        'escalation_procedures': risk_assessment.get('escalation_procedures', [])
    }
    
    # Build production validation section (if available)
    production_validation = {
        'validation_status': 'Not Available',
        'test_results': [],
        'performance_metrics': {}
    }
    
    # Build processes list for detailed sheets
    process_list = []
    for idx, process in enumerate(processes):
        process_name = process.get('name', f'Process_{idx+1}')
        
        # Handle workflow_analysis.decision_points - can be dict or list
        decision_points_data = workflow_analysis.get('decision_points', [])
        if isinstance(decision_points_data, dict):
            # Expected structure: {'ProcessName': [decision_points]}
            process_decision_points = decision_points_data.get(process_name, [])
        elif isinstance(decision_points_data, list):
            # Alternative structure: [{decision_point_objects}] - use all
            process_decision_points = decision_points_data
        else:
            process_decision_points = []
        
        # Handle workflow_analysis.workflow_steps - can be dict or list
        workflow_steps_data = workflow_analysis.get('workflow_steps', [])
        if isinstance(workflow_steps_data, dict):
            # Expected structure: {'ProcessName': [steps]}
            process_workflow_steps = workflow_steps_data.get(process_name, [])
        elif isinstance(workflow_steps_data, list):
            # Alternative structure: [step_objects] - use all
            process_workflow_steps = workflow_steps_data
        else:
            process_workflow_steps = []
        
        # Handle workflow_analysis.process_descriptions - can be dict or string
        process_descriptions_data = workflow_analysis.get('process_descriptions', {})
        if isinstance(process_descriptions_data, dict):
            process_description = process_descriptions_data.get(process_name, '')
        elif isinstance(process_descriptions_data, str):
            process_description = process_descriptions_data
        else:
            process_description = ''
        
        process_data = {
            'name': process_name,
            'description': process_description,
            'workflow_steps': process_workflow_steps,
            'decision_points': process_decision_points,
            'activities': process.get('activities', []),
            'connections': process.get('connections', [])
        }
        process_list.append(process_data)
    
    # Assemble final ipa_data dictionary
    ipa_data = {
        'client_name': client_name,
        'process_group': rice_item,
        'process_details': process_details,
        'business_requirements': business_requirements,
        'config_variables': config_variables,
        'activity_guide': activity_guide,
        'maintenance_guide': maintenance_guide,
        'production_validation': production_validation,
        'processes': process_list,
        'risk_assessment': risk_assessment,
        'metrics_summary': metrics_summary
    }
    
    return ipa_data


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python assemble_client_handover_report.py <client_name> <rice_item> [temp_dir] [output_dir]")
        print("\nExample:")
        print("  python assemble_client_handover_report.py FPI MatchReport")
        print("\nNote: Use positional arguments, NOT named arguments (--client, --rice)")
        sys.exit(1)
    
    client_name = sys.argv[1]
    rice_item = sys.argv[2]
    temp_dir = sys.argv[3] if len(sys.argv) > 3 else "Temp"
    output_dir = sys.argv[4] if len(sys.argv) > 4 else "Client_Handover_Results"
    
    # Validate inputs to prevent garbage filenames
    if client_name.startswith('-'):
        print(f"ERROR: Invalid client_name '{client_name}'")
        print("Client name cannot start with '-' (looks like a command-line flag)")
        print("\nDid you mean to use positional arguments instead of named arguments?")
        print("  ✅ CORRECT: python assemble_client_handover_report.py FPI MatchReport")
        print("  ❌ WRONG:   python assemble_client_handover_report.py --client FPI --rice MatchReport")
        sys.exit(1)
    
    if rice_item.startswith('-'):
        print(f"ERROR: Invalid rice_item '{rice_item}'")
        print("RICE item cannot start with '-' (looks like a command-line flag)")
        print("\nDid you mean to use positional arguments instead of named arguments?")
        print("  ✅ CORRECT: python assemble_client_handover_report.py FPI MatchReport")
        print("  ❌ WRONG:   python assemble_client_handover_report.py --client FPI --rice MatchReport")
        sys.exit(1)
    
    # Validate client_name and rice_item are not empty
    if not client_name.strip():
        print("ERROR: client_name cannot be empty")
        sys.exit(1)
    
    if not rice_item.strip():
        print("ERROR: rice_item cannot be empty")
        sys.exit(1)
    
    # Validate no special characters that would create invalid filenames
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        if char in client_name:
            print(f"ERROR: client_name contains invalid character '{char}'")
            print(f"Invalid characters for filenames: {' '.join(invalid_chars)}")
            sys.exit(1)
        if char in rice_item:
            print(f"ERROR: rice_item contains invalid character '{char}'")
            print(f"Invalid characters for filenames: {' '.join(invalid_chars)}")
            sys.exit(1)
    
    output_path = assemble_client_handover_report(client_name, rice_item, temp_dir, output_dir)
    
    print("\nClient handover documentation complete!")
    print(f"Report: {output_path}")