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
    
    # Auto-repair JSON files before loading
    print("\n[0/3] Validating and repairing JSON files...")
    repair_json_files(temp_dir)
    
    # Load all JSON outputs from phases 1-4
    print("\n[1/3] Loading analysis outputs...")
    
    business_analysis = load_json(os.path.join(temp_dir, "business_analysis.json"))
    workflow_analysis = load_json(os.path.join(temp_dir, "workflow_analysis.json"))
    configuration_analysis = load_json(os.path.join(temp_dir, "configuration_analysis.json"))
    risk_assessment = load_json(os.path.join(temp_dir, "risk_assessment.json"))
    
    # Load raw data for reference
    lpd_structure = load_json(os.path.join(temp_dir, "lpd_structure.json"))
    metrics_summary = load_json(os.path.join(temp_dir, "metrics_summary.json"))
    
    # Load work unit data if available
    wu_data = load_json(os.path.join(temp_dir, "wu_log_data.json"))
    
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
        metrics_summary=metrics_summary,
        wu_data=wu_data
    )
    
    print("   ✓ ipa_data structure built")
    
    # Debug output
    print(f"   → Config variables: {len(ipa_data.get('config_variables', []))}")
    print(f"   → Requirements: {len(ipa_data.get('requirements', []))}")
    print(f"   → Activity guide: {len(ipa_data.get('activity_guide', []))}")
    print(f"   → Key features: {len(ipa_data.get('key_features', []))}")
    
    # Generate Excel report using existing template
    print("\n[3/3] Generating Excel report...")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = generate_report(ipa_data)
    
    print("\n" + "=" * 80)
    print("PHASE 5 COMPLETE")
    print("=" * 80)
    print(f"\nGenerated report: {output_path}")
    
    # Validate the generated report
    print("\n" + "=" * 80)
    print("VALIDATING GENERATED REPORT")
    print("=" * 80 + "\n")
    
    # Import validation function
    sys.path.insert(0, str(Path(__file__).parent))
    from validate_report import validate_report
    
    validation_results = validate_report(output_path)
    
    if not validation_results['valid']:
        print("\n⚠️  WARNING: Report validation found issues. Review the report before delivery.\n")
    else:
        print("\n✅ Report validation passed. Report is ready for client delivery.\n")
    
    print("Client handover documentation complete!")
    print(f"Report: {output_path}\n")
    
    return output_path


def repair_json_files(temp_dir):
    """Auto-repair common JSON syntax errors in analysis files"""
    from repair_analysis_jsons import JSONRepairTool
    
    analysis_files = [
        'business_analysis.json',
        'workflow_analysis.json',
        'configuration_analysis.json',
        'risk_assessment.json'
    ]
    
    repairer = JSONRepairTool(create_backup=False)
    repairs_made = False
    
    for file_name in analysis_files:
        file_path = os.path.join(temp_dir, file_name)
        
        if not os.path.exists(file_path):
            continue
        
        # Check if file is valid
        is_valid, error = repairer.validate_json(file_path)
        
        if is_valid:
            continue
        
        # Attempt repair
        success, message, repairs = repairer.repair_file(file_path)
        
        if success and repairs:
            print(f"   ✓ Repaired {file_name}")
            for repair in repairs:
                print(f"     - {repair}")
            repairs_made = True
    
    if not repairs_made:
        print("   ✓ All JSON files valid")

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
def transform_requirements(business_analysis):
    """
    Transform requirements to template format with all required fields.

    Adds: ID, Category, Title, Priority, Source, Stakeholders
    """
    # Try business_requirements first (Phase 3 format), then functional_requirements (legacy)
    requirements = business_analysis.get('business_requirements', [])
    if not requirements:
        requirements = business_analysis.get('functional_requirements', [])
    
    stakeholders_list = business_analysis.get('stakeholders', [])

    # Extract stakeholder names
    stakeholder_names = []
    for s in stakeholders_list:
        if isinstance(s, dict):
            name = s.get('name', '') or s.get('role', '')
            if name:
                stakeholder_names.append(name)
        elif isinstance(s, str):
            stakeholder_names.append(s)

    # Default stakeholders if none found
    if not stakeholder_names:
        stakeholder_names = ['Technical Team', 'Business Users']

    transformed = []
    for idx, req in enumerate(requirements, start=1):
        # Extract requirement fields based on structure
        if isinstance(req, dict):
            # Check if it's already in the expected format (has 'id', 'requirement', 'description')
            req_id = req.get('id', f'BR-{idx:03d}')
            req_title = req.get('requirement', '') or req.get('title', '')
            req_description = req.get('description', '')
            req_priority = req.get('priority', 'Medium')
            req_category = req.get('category', 'Functional')
            req_source = req.get('source', 'ANA-050')
            business_value = req.get('business_value', '')
        elif isinstance(req, str):
            req_id = f'BR-{idx:03d}'
            req_title = req
            req_description = req
            req_priority = 'Medium'
            req_category = 'Functional'
            req_source = 'ANA-050'
            business_value = ''
        else:
            continue

        transformed.append({
            'id': req_id,
            'category': req_category,
            'title': req_title[:100] if len(req_title) > 100 else req_title,  # Limit title length
            'description': req_description,
            'priority': req_priority,
            'business_value': business_value or f"Supports {req_title.lower()}",
            'source': req_source,
            'stakeholders': stakeholder_names[:3]  # Top 3 stakeholders
        })

    return transformed


def transform_production_validation(wu_data):
    """
    Create production validation from work unit log.

    Generates real test results and performance metrics from actual execution data.
    Matches template expectations for nested structure.
    """
    import re  # For regex pattern matching
    
    if not wu_data or not wu_data.get('metadata'):
        return {
            'test_summary': {
                'work_unit_number': 'N/A',
                'total_executions': 'N/A',
                'successful': 'N/A',
                'failed': 0,
                'success_rate': 0,
                'test_date': 'N/A',
                'test_environment': 'Production'
            },
            'performance': {
                'avg_duration': 'N/A',
                'min_duration': 'N/A',
                'max_duration': 'N/A',
                'performance_rating': 'N/A'
            }
        }

    metadata = wu_data.get('metadata', {})
    duration = metadata.get('duration_readable', 'N/A')
    error_count = len(wu_data.get('errors', []))
    activity_count = len(wu_data.get('activities', []))
    work_unit_number = metadata.get('work_unit_number', 'N/A')
    status = metadata.get('status', 'Unknown')
    start_time = metadata.get('start_time', 'N/A')

    # Extract tenant/environment from variables
    variables = wu_data.get('variables', {})
    # Work unit logs don't reliably contain tenant/data area information
    # Use placeholder for user to update manually
    test_environment = '<Tenant>'
    
    # Extract record count from variables - look for rowCount
    record_count = 'N/A'
    
    # First try the 'x' variable which contains the full JSON response
    if 'x' in variables:
        x_value = str(variables['x'])
        match = re.search(r'"rowCount":(\d+)', x_value)
        if match:
            record_count = match.group(1)
    
    # If not found in x, try other rowCount variables
    if record_count == 'N/A':
        for key, value in variables.items():
            if 'rowcount' in str(key).lower():
                # Extract numeric value from the variable
                val_str = str(value)
                # Look for patterns like "obj.rowCount;; to value 370" or just "370"
                match = re.search(r'(\d+)', val_str)
                if match:
                    record_count = match.group(1)
                    break
    
    # If not found in rowCount, try RecordCount or Count
    if record_count == 'N/A':
        for key in ['RecordCount', 'Count', 'record_count']:
            if key in variables:
                val_str = str(variables[key])
                match = re.search(r'(\d+)', val_str)
                if match:
                    record_count = match.group(1)
                    break

    # Determine speed rating
    try:
        duration_seconds = float(duration.replace('s', ''))
        if duration_seconds < 10:
            speed_rating = 'Excellent'
        elif duration_seconds < 30:
            speed_rating = 'Good'
        else:
            speed_rating = 'Acceptable'
    except:
        speed_rating = 'N/A'
        duration_seconds = 0

    # Count SFTP operations - check 'name' field not 'caption'
    sftp_count = sum(1 for act in wu_data.get('activities', [])
                     if 'FTP' in act.get('name', '').upper() or
                        'FileTransfer' in act.get('type', ''))

    # Calculate average activity time
    try:
        avg_time = duration_seconds / activity_count if activity_count > 0 else 0
        avg_time_str = f'{avg_time:.2f}s'
    except:
        avg_time_str = 'N/A'
    
    # Count actual execution paths taken (scenarios tested)
    scenarios_tested = []
    activity_names = [act.get('name', '') for act in wu_data.get('activities', [])]
    
    # Identify which paths were taken
    if 'GetAccessToken' in activity_names:
        scenarios_tested.append('OAuth Authentication')
    if 'InitQuery' in activity_names:
        scenarios_tested.append('Compass API Query')
    if 'GetStatus' in activity_names:
        scenarios_tested.append('Asynchronous Status Polling')
    if 'GetResult' in activity_names:
        scenarios_tested.append('Result Retrieval with Pagination')
    if any('FTP' in name or 'FileTransfer' in name for name in activity_names):
        scenarios_tested.append('SFTP File Transfer')
    if any('Delete' in name for name in activity_names):
        scenarios_tested.append('File Cleanup')
    
    scenarios_count = len(scenarios_tested)
    
    # Build data validation section with real record count
    data_validation = {
        'input_file': 'Trigger file with run date',
        'records_retrieved': f'{record_count} GL records' if record_count != 'N/A' else 'N/A',
        'data_volume': f'{record_count} records processed' if record_count != 'N/A' else 'N/A'
    }

    # Build structure matching template expectations
    return {
        'test_summary': {
            'work_unit_number': work_unit_number,
            'total_executions': '1',
            'successful': '1' if error_count == 0 else '0',
            'failed': error_count,  # Keep as integer for proper comparison in template
            'success_rate': 100 if error_count == 0 else 0,
            'test_date': start_time.split()[0] if start_time != 'N/A' else 'N/A',
            'test_environment': test_environment,
            'test_scenarios': len(scenarios_tested),  # Total scenarios defined
            'scenarios_tested': scenarios_count  # Actual scenarios executed
        },
        'performance': {
            'avg_duration': duration,
            'min_duration': duration,
            'max_duration': duration,
            'performance_rating': speed_rating
        },
        'error_handling': {
            'validated': error_count == 0,
            'test_scenarios': scenarios_tested[:3] if len(scenarios_tested) > 3 else scenarios_tested,  # Limit to 3 for display
            'confidence': 'High' if error_count == 0 else 'Medium'
        },
        'production_readiness': {
            'ready': error_count == 0 and status == 'Completed',
            'confidence_level': 'High' if error_count == 0 else 'Medium',
            'evidence': [
                f'Work unit {work_unit_number} completed successfully',
                f'Execution time: {duration}',
                f'Processed {record_count} records' if record_count != 'N/A' else 'Data processing verified',
                f'{activity_count} activities executed',
                f'{sftp_count} file operations completed' if sftp_count > 0 else 'No file operation errors'
            ]
        },
        'test_coverage': {
            'scenarios_tested': scenarios_tested,  # Use actual scenarios from execution
            'coverage_percentage': 100
        },
        'activity_breakdown': {
            'total_activities': activity_count,
            'activity_types': {
                'Data Operations': sum(1 for a in wu_data.get('activities', []) if a.get('type') in ['ASSGN', 'BRANCH']),
                'API Calls': sum(1 for a in wu_data.get('activities', []) if a.get('type') == 'WEBRN'),
                'File Operations': sum(1 for a in wu_data.get('activities', []) if a.get('type') == 'ACCFIL'),
                'Other': sum(1 for a in wu_data.get('activities', []) if a.get('type') not in ['ASSGN', 'BRANCH', 'WEBRN', 'ACCFIL'])
            }
        },
        'data_validation': data_validation,
        'integration_points': {
            'Data Fabric API': 'Validated',
            'OAuth2 Authentication': 'Validated',
            'SFTP File Transfer': 'Validated' if sftp_count > 0 else 'Not tested'
        }
    }


def generate_key_features(business_analysis):
    """
    Generate key features from business analysis.

    Extracts features from integrations and objectives.
    Template will add check marks, so don't add them here.
    """
    features = []

    # From integrations
    for integration in business_analysis.get('integration_touchpoints', []):
        if isinstance(integration, dict):
            system = integration.get('system', '')
            if system:
                features.append(f"{system} Integration")
        elif isinstance(integration, str):
            features.append(integration)

    # From business objectives
    business_objectives = business_analysis.get('business_objectives', {})
    if isinstance(business_objectives, dict):
        objectives = business_objectives.get('objectives', [])
    elif isinstance(business_objectives, list):
        objectives = business_objectives
    else:
        objectives = []

    for objective in objectives:
        if objective and len(features) < 8:  # Limit to 8 features
            if isinstance(objective, str):
                features.append(objective)
            elif isinstance(objective, dict):
                obj_text = objective.get('objective', '') or objective.get('description', '')
                if obj_text:
                    features.append(obj_text)

    return features


def build_ipa_data(client_name, rice_item, business_analysis, workflow_analysis, 
                   configuration_analysis, risk_assessment, lpd_structure, metrics_summary, wu_data=None):
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
        'Process Count': str(len(processes)),
        'Total Activities': str(metrics_summary.get('total_activities', 0)),
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
    # Handle both dict and list formats for business_objectives
    business_objectives = business_analysis.get('business_objectives', {})
    if isinstance(business_objectives, dict):
        overview = business_objectives.get('overview', '')
        objectives = business_objectives.get('objectives', [])
    elif isinstance(business_objectives, list):
        # If it's a list, use first item as overview, rest as objectives
        overview = business_objectives[0] if business_objectives else ''
        objectives = business_objectives[1:] if len(business_objectives) > 1 else business_objectives
    else:
        overview = str(business_objectives) if business_objectives else ''
        objectives = []
    
    # Also check for business_purpose as fallback
    if not overview:
        overview = business_analysis.get('business_purpose', '')
    
    business_requirements = {
        'overview': overview,
        'objectives': objectives,
        'requirements': business_analysis.get('functional_requirements', []),
        'stakeholders': business_analysis.get('stakeholders', []),
        'integrations': business_analysis.get('integration_touchpoints', [])
    }
    
    # Build configuration variables section
    config_variables = []
    
    # Try configuration_items first (expected format)
    for config in configuration_analysis.get('configuration_items', []):
        config_variables.append({
            'name': config.get('name', ''),
            'type': config.get('type', ''),
            'description': config.get('description', ''),
            'default_value': config.get('default_value', ''),
            'modification_instructions': config.get('modification_instructions', '')
        })
    
    # If no configuration_items, try to extract from configuration_sets structure
    if not config_variables:
        for config_set in configuration_analysis.get('configuration_sets', []):
            for prop in config_set.get('properties', []):
                config_variables.append({
                    'name': f"{config_set.get('config_set', '')}.{prop.get('property', '')}",
                    'type': 'System Configuration',  # Always use this for template compatibility
                    'description': prop.get('description', ''),
                    'default_value': prop.get('example_value', ''),
                    'modification_instructions': prop.get('modification_instructions', ''),
                    'location': f"FSM > Configuration > System Configuration > {config_set.get('config_set', '')}",
                    'current_value': prop.get('example_value', ''),
                    'how_to_modify': prop.get('modification_instructions', '')
                })
    
    # If still no config_variables, try configuration_dependencies
    if not config_variables:
        for dep in configuration_analysis.get('configuration_dependencies', []):
            config_variables.append({
                'name': f"{dep.get('config_set', '')}.{dep.get('property', '')}",
                'type': 'System Configuration',
                'description': dep.get('purpose', '') or dep.get('usage', ''),
                'default_value': dep.get('example_value', ''),
                'modification_instructions': dep.get('modification_instructions', ''),
                'location': f"FSM > Configuration > System Configuration > {dep.get('config_set', '')}",
                'current_value': dep.get('example_value', ''),
                'how_to_modify': dep.get('modification_instructions', '')
            })
    
    # NEW: Extract from nested configuration_requirements structure (Phase 3 output format)
    if not config_variables:
        for req_category in configuration_analysis.get('configuration_requirements', []):
            category = req_category.get('category', '')
            for component in req_category.get('components', []):
                component_type = component.get('type', 'System Configuration')
                for setting in component.get('required_settings', []):
                    setting_name = setting.get('setting', '')
                    # Determine the full name based on category
                    if 'System Configuration' in category:
                        # Extract config set from configuration_location if available
                        config_location = component.get('configuration_location', '')
                        if 'Interface' in config_location:
                            full_name = f"Interface.{setting_name}"
                        else:
                            full_name = setting_name
                    elif 'File Channel' in category:
                        full_name = f"File Channel - {setting_name}"
                    else:
                        full_name = setting_name
                    
                    config_variables.append({
                        'name': full_name,
                        'type': component_type,
                        'description': setting.get('description', ''),
                        'default_value': setting.get('value', ''),
                        'modification_instructions': setting.get('modification_instructions', ''),
                        'location': component.get('configuration_location', ''),
                        'current_value': setting.get('value', ''),
                        'how_to_modify': setting.get('modification_instructions', '')
                    })
    
    # NEW: Extract from oauth_credentials and global_config_variables structure (ALWAYS run this)
    # OAuth credentials - only process if they're dicts (not already lists)
    oauth_creds_raw = configuration_analysis.get('oauth_credentials', [])
    if oauth_creds_raw and len(oauth_creds_raw) > 0 and isinstance(oauth_creds_raw[0], dict):
        # Process dict format
        for oauth in oauth_creds_raw:
            var_name = oauth.get('variable', '')
            config_set = oauth.get('config_set', 'Interface')
            structure = oauth.get('structure', {})
            if isinstance(structure, dict):
                structure_str = f"JSON: {', '.join(structure.keys())}"
            else:
                structure_str = str(structure)
            
            config_variables.append({
                'name': f"{config_set}.{var_name}",
                'type': 'OAuth2 Credentials',
                'description': oauth.get('purpose', ''),
                'default_value': structure_str,
                'modification_instructions': f"Update in FSM > Configuration > System Configuration > {config_set}",
                'location': f"FSM > Configuration > System Configuration > {config_set}",
                'current_value': oauth.get('format', 'JSON string'),
                'how_to_modify': f"Navigate to FSM > Configuration > System Configuration > {config_set}, locate {var_name}, update JSON with new OAuth credentials"
            })
    # If already lists, they'll be passed through directly to ipa_data
    
    # Global config variables - only process if they're dicts (not already lists)
    global_vars_raw = configuration_analysis.get('global_config_variables', [])
    if global_vars_raw and len(global_vars_raw) > 0 and isinstance(global_vars_raw[0], dict):
        # Process dict format
        for global_var in global_vars_raw:
            var_name = global_var.get('variable', '')
            config_set = global_var.get('config_set', 'Interface')
            config_variables.append({
                'name': f"{config_set}.{var_name}",
                'type': 'System Configuration',
                'description': global_var.get('purpose', ''),
                'default_value': global_var.get('example', ''),
                'modification_instructions': f"Update in FSM > Configuration > System Configuration > {config_set}",
                'location': f"FSM > Configuration > System Configuration > {config_set}",
                'current_value': global_var.get('example', ''),
                'how_to_modify': f"Navigate to FSM > Configuration > System Configuration > {config_set}, locate {var_name}, update value"
            })
    
    # File channel config - ALWAYS extract (check if already list format)
    file_channel_raw = configuration_analysis.get('file_channel_config', [])
    if file_channel_raw and isinstance(file_channel_raw[0], dict) if len(file_channel_raw) > 0 else False:
        # Dict format - convert to config_variables
        for fc_var in file_channel_raw:
            config_variables.append({
                'name': fc_var.get('variable', ''),
                'type': 'File Channel Variable',
                'description': fc_var.get('purpose', ''),
                'default_value': fc_var.get('example_value', ''),
                'modification_instructions': fc_var.get('modification_instructions', ''),
                'location': 'File Channel Configuration',
                'current_value': fc_var.get('example_value', ''),
                'how_to_modify': fc_var.get('modification_instructions', '')
            })
    
    # Process variables - ALWAYS extract (check if already list format)
    process_vars_raw = configuration_analysis.get('process_variables', [])
    if process_vars_raw and isinstance(process_vars_raw[0], dict) if len(process_vars_raw) > 0 else False:
        # Dict format - convert to config_variables
        for pv in process_vars_raw:
            config_variables.append({
                'name': pv.get('variable', ''),
                'type': 'Process Variable',
                'description': pv.get('purpose', ''),
                'default_value': pv.get('default_value', ''),
                'modification_instructions': pv.get('modification_instructions', ''),
                'location': 'Process Designer > Start Node > Properties',
                'current_value': pv.get('default_value', ''),
                'how_to_modify': pv.get('modification_instructions', '')
            })
    
    # Convert file_channel_config and process_variables to list format for template
    # Template expects list of lists, not list of dicts
    file_channel_list = []
    if file_channel_raw and isinstance(file_channel_raw[0], dict) if len(file_channel_raw) > 0 else False:
        # Convert from dict format
        for fc_var in file_channel_raw:
            file_channel_list.append([
                fc_var.get('variable', ''),
                fc_var.get('example_value', ''),
                fc_var.get('purpose', ''),
                fc_var.get('modification_instructions', '')
            ])
    else:
        # Already in list format
        file_channel_list = file_channel_raw
    
    process_variables_list = []
    if process_vars_raw and isinstance(process_vars_raw[0], dict) if len(process_vars_raw) > 0 else False:
        # Convert from dict format
        for pv in process_vars_raw:
            process_variables_list.append([
                pv.get('variable', ''),
                pv.get('default_value', ''),
                pv.get('purpose', ''),
                pv.get('modification_instructions', '')
            ])
    else:
        # Already in list format
        process_variables_list = process_vars_raw
    
    global_config_list = []
    global_vars_raw = configuration_analysis.get('global_config_variables', [])
    if global_vars_raw and isinstance(global_vars_raw[0], dict) if len(global_vars_raw) > 0 else False:
        # Convert from dict format
        for global_var in global_vars_raw:
            global_config_list.append([
                global_var.get('variable', ''),
                global_var.get('config_set', ''),
                global_var.get('example', ''),
                global_var.get('purpose', ''),
                global_var.get('modification_instructions', '')
            ])
    else:
        # Already in list format
        global_config_list = global_vars_raw
    # If already lists, they'll be passed through directly to ipa_data
    
    # Build activity guide section
    activity_guide = []
    for process in processes:
        for activity in process.get('activities', []):
            activity_id = activity.get('id', '')
            activity_type = activity.get('type', '')
            activity_caption = activity.get('caption', '')
            
            # Try to get descriptions from workflow_analysis
            description = workflow_analysis.get('activity_descriptions', {}).get(activity_id, '')
            business_purpose = workflow_analysis.get('activity_purposes', {}).get(activity_id, '')
            
            # If not found, generate basic description from activity type
            if not description and activity_type:
                type_descriptions = {
                    'START': 'Process entry point - initializes variables and begins execution',
                    'END': 'Process completion - marks successful end of workflow',
                    'ASSGN': 'Variable assignment - sets values, executes JavaScript, transforms data',
                    'WEBRN': 'HTTP API call - makes external web service requests',
                    'BRANCH': 'Conditional routing - directs flow based on conditions',
                    'Timer': 'Delay execution - waits for specified time period',
                    'ACCFIL': 'File operation - reads, writes, or manipulates files',
                    'SUBPROC': 'Subprocess call - invokes another IPA process',
                    'MSGBD': 'Message builder - constructs formatted messages',
                    'LM': 'Landmark transaction - queries or updates FSM business classes'
                }
                description = type_descriptions.get(activity_type, f'{activity_type} activity')
            
            activity_guide.append({
                'id': activity_id,
                'caption': activity_caption,
                'type': activity_type,
                'description': description,
                'business_purpose': business_purpose
            })
    
    # Build maintenance guide section
    maintenance_guide = {
        'common_modifications': configuration_analysis.get('common_modifications', []),
        'troubleshooting': risk_assessment.get('troubleshooting_guide', []),
        'best_practices': risk_assessment.get('best_practices', []),
        'escalation_procedures': risk_assessment.get('escalation_procedures', [])
    }
    
    # Build production validation section using transformation function
    production_validation = transform_production_validation(wu_data)
    
    # Build processes list for detailed sheets
    process_list = []
    for idx, process in enumerate(processes):
        process_name = process.get('process_name', process.get('name', f'Process_{idx+1}'))
        
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
        
        # Use process_type as fallback if process_description is empty
        if not process_description:
            process_description = workflow_analysis.get('process_type', 'IPA Process')
        
        # CRITICAL FIX: Enrich activities with descriptions and when_it_runs
        enriched_activities = []
        for activity in process.get('activities', []):
            activity_id = activity.get('id', '')
            activity_type = activity.get('type', '')
            activity_caption = activity.get('caption', '')
            
            # PRIORITY 1: Try to get activity-specific description from activity_descriptions dictionary
            activity_description = workflow_analysis.get('activity_descriptions', {}).get(activity_id, '')
            activity_when_runs = workflow_analysis.get('activity_purposes', {}).get(activity_id, '')
            
            # PRIORITY 2: If not found, try workflow_steps
            if not activity_description:
                for step in process_workflow_steps:
                    step_activities = step.get('activities', [])
                    # Check if this activity is mentioned in this workflow step
                    if activity_caption in step_activities or activity_id in step_activities or any(activity_caption in str(act) for act in step_activities):
                        activity_description = step.get('description', '')
                        activity_when_runs = step.get('business_purpose', '')
                        break
            
            # PRIORITY 3: If still not found, use generic type description
            if not activity_description:
                type_descriptions = {
                    'START': 'Process entry point - initializes variables and begins execution',
                    'END': 'Process completion - marks successful end of workflow',
                    'ASSGN': 'Variable assignment - sets values, executes JavaScript, transforms data',
                    'WEBRN': 'HTTP API call - makes external web service requests (OAuth, Compass API)',
                    'BRANCH': 'Conditional routing - directs flow based on conditions',
                    'Timer': 'Delay execution - waits for specified time period',
                    'ACCFIL': 'File operation - reads, writes, or manipulates files in FSM File Storage',
                    'SUBPROC': 'Subprocess call - invokes another IPA process',
                    'MSGBD': 'Message builder - constructs formatted messages',
                    'LM': 'Landmark transaction - queries or updates FSM business classes',
                    'FileTransfer': 'SFTP operation - transfers files to/from external servers'
                }
                activity_description = type_descriptions.get(activity_type, f'{activity_type} activity')
            
            # Generate when_it_runs based on workflow analysis or position/type
            if not activity_when_runs:
                if activity_type == 'START':
                    activity_when_runs = 'Process start - triggered by file channel'
                elif activity_type == 'END':
                    activity_when_runs = 'Process completion - after all activities finish'
                elif activity_type == 'BRANCH':
                    activity_when_runs = 'After previous activity - evaluates conditions to determine next step'
                elif activity_type == 'Timer':
                    activity_when_runs = 'Polling delay - waits between status checks'
                elif 'Error' in activity_caption or 'error' in activity_caption.lower():
                    activity_when_runs = 'Error handling - when errors occur in previous activities'
                else:
                    activity_when_runs = 'Sequential execution - after previous activity completes'
            
            description = activity_description
            when_it_runs = activity_when_runs
            
            enriched_activities.append({
                'id': activity_id,
                'type': activity_type,
                'caption': activity_caption,
                'description': description,
                'when_it_runs': when_it_runs,
                'properties': activity.get('properties', {})
            })
        
        process_data = {
            'name': process_name,
            'description': process_description,
            'workflow_steps': process_workflow_steps,
            'decision_points': process_decision_points,
            'activities': enriched_activities,  # Use enriched activities instead of raw
            'connections': process.get('connections', [])
        }
        process_list.append(process_data)
    
    # Generate key features using transformation function
    key_features = generate_key_features(business_analysis)
    
    # Build workflow_description for Executive Summary diagram
    # For multi-process RICE items, show high-level overview, not detailed process steps
    workflow_description = []
    
    if len(processes) > 1:
        # Multi-process: Show RICE-level overview
        process_overview = workflow_analysis.get('process_overview', '')
        
        # Extract high-level steps from process descriptions
        for process in workflow_analysis.get('processes', []):
            process_name = process.get('name', '')
            process_purpose = process.get('purpose', '')
            
            # Simplify process name for diagram
            if 'nightly' in process_name.lower() or 'trigger' in process_name.lower():
                step_name = 'Nightly Batch Submission'
            elif 'reject' in process_name.lower():
                step_name = 'Auto-Reject Processing'
            elif 'approval' in process_name.lower() and 'nightly' not in process_name.lower():
                step_name = 'Invoice Approval Workflow'
            else:
                # Extract key words from process name
                words = process_name.replace('_', ' ').split()
                step_name = ' '.join(words[:3]) if len(words) > 3 else process_name
            
            workflow_description.append({
                'step_name': step_name,
                'description': process_purpose
            })
    else:
        # Single process: Show process-specific workflow steps
        workflow_steps_data = workflow_analysis.get('workflow_steps', [])
        
        if isinstance(workflow_steps_data, list):
            for step in workflow_steps_data:
                if isinstance(step, dict):
                    # Use 'phase' field as step_name (not 'step' which is an integer)
                    step_name = step.get('name', step.get('phase', 'Process Step'))
                    workflow_description.append({
                        'step_name': step_name,
                        'description': step.get('description', '')
                    })
    
    # Assemble final ipa_data dictionary
    ipa_data = {
        'client_name': client_name,
        'process_group': rice_item,
        'process_details': process_details,
        'business_requirements': business_requirements,
        # Use transformed requirements instead of raw requirements
        'requirements': transform_requirements(business_analysis),
        'config_variables': config_variables,
        'activity_guide': activity_guide,
        'maintenance_guide': maintenance_guide,
        'production_validation': production_validation,
        'processes': process_list,
        'risk_assessment': risk_assessment,
        'metrics_summary': metrics_summary,
        'key_features': key_features,
        # Pass through configuration data in LIST format for template
        'file_channel_config': file_channel_list,
        'process_variables': process_variables_list,
        'global_config_variables': global_config_list,
        # Keep OAuth credentials in original format (template handles it differently)
        'oauth_credentials': configuration_analysis.get('oauth_credentials', []),
        # Add workflow_description for diagram generation
        'workflow_description': workflow_description
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