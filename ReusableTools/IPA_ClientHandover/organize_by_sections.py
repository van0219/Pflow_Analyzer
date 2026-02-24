#!/usr/bin/env python3
"""
IPA Client Handover - Organize by Documentation Sections

Splits extracted IPA data into 5 documentation section files for parallel analysis.

Sections:
1. Business Requirements - What and why (from functional spec)
2. Workflow - How it flows (from LPD activities)
3. Configuration - What can be changed (from LPD config variables)
4. Activity Guide - Reference documentation (from LPD activities)
5. Validation - Production proof (from WU logs)

Usage:
    python organize_by_sections.py <lpd_json> <spec_json> <wu_json> <output_prefix>
    
    Arguments:
        lpd_json: Path to extracted LPD data JSON
        spec_json: Path to extracted spec data JSON (or "none" if not available)
        wu_json: Path to extracted WU log JSON (or "none" if not available)
        output_prefix: Output file prefix (e.g., "Temp/ProcessName")
"""

import json
import sys
from pathlib import Path


def extract_integrations(activities):
    """Extract integration points (APIs, files, etc.)"""
    integrations = []
    
    for activity in activities:
        activity_type = activity.get('type', '')
        
        # API integrations
        if activity_type in ['WEBRN', 'WEBRUN']:
            integrations.append({
                'type': 'API',
                'activity_id': activity.get('id'),
                'caption': activity.get('caption'),
                'details': 'REST API call'
            })
        
        # File integrations
        elif activity_type in ['ACCFIL', 'FILEIN', 'FILEOUT']:
            integrations.append({
                'type': 'File',
                'activity_id': activity.get('id'),
                'caption': activity.get('caption'),
                'details': 'File processing'
            })
        
        # Database integrations
        elif activity_type == 'QUERY':
            integrations.append({
                'type': 'Database',
                'activity_id': activity.get('id'),
                'caption': activity.get('caption'),
                'details': 'SQL query'
            })
    
    return integrations


def build_flow_sequence(activities):
    """Build sequential flow of activities"""
    sequence = []
    
    for i, activity in enumerate(activities):
        sequence.append({
            'order': i + 1,
            'id': activity.get('id'),
            'type': activity.get('type'),
            'caption': activity.get('caption'),
            'is_user_action': activity.get('type') == 'USERACTION',
            'is_branch': activity.get('type') == 'BRANCH',
            'is_loop': activity.get('type') in ['LOOP', 'WHILE']
        })
    
    return sequence


def extract_system_settings(activities):
    """Extract system configuration references"""
    settings = []
    
    for activity in activities:
        # Look for config variable references in JavaScript
        if activity.get('type') == 'ASSIGN':
            code = activity.get('code', '')
            if '${' in code:
                # Extract config variable names
                import re
                config_vars = re.findall(r'\$\{([^}]+)\}', code)
                for var in config_vars:
                    if var not in [s['name'] for s in settings]:
                        settings.append({
                            'name': var,
                            'activity_id': activity.get('id'),
                            'activity_caption': activity.get('caption')
                        })
    
    return settings


def extract_email_config(activities):
    """Extract email configuration"""
    email_config = []
    
    for activity in activities:
        if activity.get('type') == 'EMAIL':
            email_config.append({
                'activity_id': activity.get('id'),
                'caption': activity.get('caption'),
                'to': activity.get('to', ''),
                'subject': activity.get('subject', ''),
                'body_template': activity.get('body', '')
            })
    
    return email_config


def extract_approval_matrix(activities):
    """Extract approval matrix from user actions"""
    approval_matrix = []
    
    user_actions = [a for a in activities if a.get('type') == 'USERACTION']
    
    for ua in user_actions:
        approval_matrix.append({
            'level': len(approval_matrix) + 1,
            'activity_id': ua.get('id'),
            'caption': ua.get('caption'),
            'actor': ua.get('actor', ''),
            'timeout': ua.get('timeout', ''),
            'description': f"Approval level {len(approval_matrix) + 1}"
        })
    
    return approval_matrix


def group_by_type(activities):
    """Group activities by type"""
    groups = {}
    
    for activity in activities:
        activity_type = activity.get('type', 'UNKNOWN')
        if activity_type not in groups:
            groups[activity_type] = []
        groups[activity_type].append(activity)
    
    return groups


def build_dependencies(activities):
    """Build activity dependencies (simplified)"""
    dependencies = []
    
    # For now, just sequential dependencies
    for i in range(len(activities) - 1):
        dependencies.append({
            'from': activities[i].get('id'),
            'to': activities[i + 1].get('id'),
            'type': 'sequential'
        })
    
    return dependencies


def generate_descriptions(activities):
    """Generate activity descriptions"""
    descriptions = {}
    
    for activity in activities:
        activity_id = activity.get('id')
        activity_type = activity.get('type')
        caption = activity.get('caption', '')
        
        # Generate description based on type
        if activity_type == 'START':
            desc = "Initializes process variables and begins workflow"
        elif activity_type == 'USERACTION':
            desc = f"Waits for user approval: {caption}"
        elif activity_type == 'BRANCH':
            desc = f"Decision point: {caption}"
        elif activity_type == 'ASSIGN':
            desc = f"Executes JavaScript: {caption}"
        elif activity_type == 'EMAIL':
            desc = f"Sends email notification: {caption}"
        elif activity_type == 'WEBRN' or activity_type == 'WEBRUN':
            desc = f"Calls REST API: {caption}"
        elif activity_type == 'QUERY':
            desc = f"Executes SQL query: {caption}"
        elif activity_type == 'END':
            desc = "Completes process execution"
        else:
            desc = f"{activity_type} activity: {caption}"
        
        descriptions[activity_id] = desc
    
    return descriptions


def extract_test_results(wu_data):
    """Extract test results from WU log data"""
    if not wu_data:
        return None
    
    return {
        'total_executions': wu_data.get('total_executions', 0),
        'successful': wu_data.get('successful_executions', 0),
        'failed': wu_data.get('failed_executions', 0),
        'success_rate': wu_data.get('success_rate', 0)
    }


def extract_performance(wu_data):
    """Extract performance metrics from WU log data"""
    if not wu_data:
        return None
    
    return {
        'avg_duration': wu_data.get('avg_duration', 'N/A'),
        'min_duration': wu_data.get('min_duration', 'N/A'),
        'max_duration': wu_data.get('max_duration', 'N/A')
    }


def validate_error_handling(lpd_data, wu_data):
    """Validate error handling from LPD and WU log"""
    if not lpd_data:
        return False
    
    # Check if process has error handling configured
    process = lpd_data.get('processes', [{}])[0]
    error_handling = process.get('error_handling_analysis', {})
    
    has_error_config = error_handling.get('nodes_with_error_config', [])
    
    return len(has_error_config) > 0


def organize_by_sections(lpd_path, spec_path, wu_path, output_prefix):
    """
    Organize extracted data into 5 documentation section files.
    
    Args:
        lpd_path: Path to LPD data JSON
        spec_path: Path to spec data JSON (or "none")
        wu_path: Path to WU log data JSON (or "none")
        output_prefix: Output file prefix
    
    Returns:
        List of created file paths
    """
    
    # Load LPD data (required)
    with open(lpd_path, 'r', encoding='utf-8', errors='replace') as f:
        lpd_data = json.load(f)
    
    # Load spec data (optional)
    spec_data = {}
    if spec_path != "none" and Path(spec_path).exists():
        with open(spec_path, 'r', encoding='utf-8', errors='replace') as f:
            spec_data = json.load(f)
    
    # Load WU log data (optional)
    wu_data = {}
    if wu_path != "none" and Path(wu_path).exists():
        with open(wu_path, 'r', encoding='utf-8', errors='replace') as f:
            wu_data = json.load(f)
    
    # Get process data
    process = lpd_data.get('processes', [{}])[0]
    activities = process.get('activities', [])
    
    # Section 1: Business Requirements
    business = {
        'requirements': spec_data.get('requirements', []),
        'objectives': spec_data.get('objectives', []),
        'stakeholders': spec_data.get('stakeholders', []),
        'scope': spec_data.get('scope', {}),
        'process_overview': {
            'name': process.get('name', ''),
            'file': process.get('file', ''),
            'activity_count': len(activities),
            'description': spec_data.get('description', '')
        }
    }
    
    # Section 2: Workflow
    workflow = {
        'activities': activities,
        'user_actions': [a for a in activities if a.get('type') == 'USERACTION'],
        'branches': [a for a in activities if a.get('type') == 'BRANCH'],
        'integrations': extract_integrations(activities),
        'flow_sequence': build_flow_sequence(activities)
    }
    
    # Section 3: Configuration
    configuration = {
        'config_variables': process.get('config_variables', []),
        'config_sets': process.get('config_sets', []),
        'system_settings': extract_system_settings(activities),
        'email_config': extract_email_config(activities),
        'approval_matrix': extract_approval_matrix(activities)
    }
    
    # Section 4: Activity Guide
    activities_guide = {
        'all_activities': activities,
        'activity_types': group_by_type(activities),
        'activity_dependencies': build_dependencies(activities),
        'activity_descriptions': generate_descriptions(activities)
    }
    
    # Section 5: Validation
    validation = {
        'wu_log_data': wu_data,
        'test_results': extract_test_results(wu_data),
        'performance_metrics': extract_performance(wu_data),
        'error_handling_validated': validate_error_handling(lpd_data, wu_data),
        'has_wu_log': bool(wu_data)
    }
    
    # Save all sections
    output_files = []
    
    sections = {
        'business': business,
        'workflow': workflow,
        'configuration': configuration,
        'activities': activities_guide,
        'validation': validation
    }
    
    for section_name, section_data in sections.items():
        output_path = f"{output_prefix}_section_{section_name}.json"
        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(section_data, f, indent=2, ensure_ascii=False)
        output_files.append(output_path)
        print(f"✓ Created: {output_path} ({len(json.dumps(section_data))} bytes)")
    
    return output_files


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python organize_by_sections.py <lpd_json> <spec_json> <wu_json> <output_prefix>")
        print("  Use 'none' for spec_json or wu_json if not available")
        sys.exit(1)
    
    lpd_path = sys.argv[1]
    spec_path = sys.argv[2]
    wu_path = sys.argv[3]
    output_prefix = sys.argv[4]
    
    try:
        output_files = organize_by_sections(lpd_path, spec_path, wu_path, output_prefix)
        print(f"\n✓ Successfully created {len(output_files)} section files")
        print(f"  Output prefix: {output_prefix}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
