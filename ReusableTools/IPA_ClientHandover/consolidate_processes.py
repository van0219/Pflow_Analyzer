#!/usr/bin/env python3
"""
IPA Client Handover - Consolidate Multiple Processes

Consolidates multiple process documentation files into a single RICE-level documentation file.
Handles both single and multiple processes (backward compatible).

Usage:
    python consolidate_processes.py <rice_item> <process_name1> [<process_name2> ...]
    
    Arguments:
        rice_item: RICE item name (e.g., "MatchReport")
        process_name1, process_name2, ...: Process names to consolidate
    
    Expects these files to exist for each process:
        Temp/<process_name>_master_documentation.json
    
    Creates:
        Temp/<rice_item>_consolidated_documentation.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_process_documentation(process_name):
    """Load master documentation for a process"""
    file_path = f"Temp/{process_name}_master_documentation.json"
    
    if not Path(file_path).exists():
        print(f"✗ Error: {file_path} not found")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        print(f"✓ Loaded: {file_path}")
        return data
    except Exception as e:
        print(f"✗ Error loading {file_path}: {e}")
        return None


def consolidate_business_requirements(process_docs):
    """
    Consolidate business requirements across processes.
    Since business requirements come from the spec (RICE-level), they should be the same.
    Use the first process's business requirements.
    """
    if not process_docs:
        return {}
    
    # Use first process's business requirements (they're RICE-level from spec)
    return process_docs[0].get('business_requirements', {})


def consolidate_validation(process_docs):
    """
    Consolidate validation data across processes.
    Aggregate metrics and combine test results.
    """
    if not process_docs:
        return {}
    
    consolidated = {
        'has_wu_log': False,
        'processes_validated': [],
        'total_tests': 0,
        'total_passed': 0,
        'aggregate_performance': {}
    }
    
    for doc in process_docs:
        validation = doc.get('validation', {})
        process_name = doc.get('metadata', {}).get('process_name', 'Unknown')
        
        if validation.get('has_wu_log', False):
            consolidated['has_wu_log'] = True
            consolidated['processes_validated'].append({
                'process_name': process_name,
                'test_summary': validation.get('test_summary', {}),
                'performance': validation.get('performance', {})
            })
            
            # Aggregate counts
            test_summary = validation.get('test_summary', {})
            consolidated['total_tests'] += test_summary.get('total_tests', 0)
            consolidated['total_passed'] += test_summary.get('passed', 0)
    
    # Calculate aggregate pass rate
    if consolidated['total_tests'] > 0:
        consolidated['pass_rate'] = f"{(consolidated['total_passed'] / consolidated['total_tests'] * 100):.1f}%"
    else:
        consolidated['pass_rate'] = 'N/A'
    
    return consolidated


def consolidate_configuration(process_docs):
    """
    Consolidate configuration across processes.
    Combine all config variables from all processes.
    """
    if not process_docs:
        return {}
    
    consolidated = {
        'config_variables': [],
        'processes': []
    }
    
    for doc in process_docs:
        config = doc.get('configuration', {})
        process_name = doc.get('metadata', {}).get('process_name', 'Unknown')
        
        # Add process-specific config
        consolidated['processes'].append({
            'process_name': process_name,
            'config_variables': config.get('config_variables', [])
        })
        
        # Add to consolidated list (with process name prefix)
        for var in config.get('config_variables', []):
            var_with_process = var.copy() if isinstance(var, dict) else var
            if isinstance(var_with_process, dict):
                var_with_process['process'] = process_name
            consolidated['config_variables'].append(var_with_process)
    
    return consolidated


def consolidate_activity_guide(process_docs):
    """
    Consolidate activity guides across processes.
    Keep separate activity lists per process.
    """
    if not process_docs:
        return {}
    
    consolidated = {
        'processes': []
    }
    
    for doc in process_docs:
        activity_guide = doc.get('activity_guide', {})
        process_name = doc.get('metadata', {}).get('process_name', 'Unknown')
        
        consolidated['processes'].append({
            'process_name': process_name,
            'activities': activity_guide.get('activities', []),
            'activity_groups': activity_guide.get('activity_groups', [])
        })
    
    return consolidated


def consolidate_workflow(process_docs):
    """
    Consolidate workflow information across processes.
    Keep separate workflows per process.
    """
    if not process_docs:
        return {}
    
    consolidated = {
        'processes': []
    }
    
    for doc in process_docs:
        workflow = doc.get('workflow', {})
        process_name = doc.get('metadata', {}).get('process_name', 'Unknown')
        
        consolidated['processes'].append({
            'process_name': process_name,
            'workflow_steps': workflow.get('workflow_steps', []),
            'approval_paths': workflow.get('approval_paths', []),
            'decision_points': workflow.get('decision_points', [])
        })
    
    return consolidated


def consolidate_processes(rice_item, process_names):
    """
    Consolidate multiple process documentation files into one RICE-level file.
    
    Args:
        rice_item: RICE item name
        process_names: List of process names to consolidate
    
    Returns:
        Path to consolidated documentation file
    """
    
    print("Consolidating process documentation...")
    print("=" * 60)
    print(f"RICE Item: {rice_item}")
    print(f"Processes: {', '.join(process_names)}")
    print("=" * 60)
    
    # Load all process documentation
    process_docs = []
    for process_name in process_names:
        doc = load_process_documentation(process_name)
        if doc is None:
            print(f"✗ Failed to load documentation for {process_name}")
            sys.exit(1)
        process_docs.append(doc)
    
    print("=" * 60)
    print(f"✓ Loaded {len(process_docs)} process documentation files")
    print("=" * 60)
    
    # Consolidate sections
    print("Consolidating sections...")
    
    consolidated = {
        'metadata': {
            'rice_item': rice_item,
            'process_count': len(process_names),
            'process_names': process_names,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_activities': sum(doc.get('metadata', {}).get('activity_count', 0) for doc in process_docs)
        },
        'business_requirements': consolidate_business_requirements(process_docs),
        'validation': consolidate_validation(process_docs),
        'configuration': consolidate_configuration(process_docs),
        'activity_guide': consolidate_activity_guide(process_docs),
        'workflow': consolidate_workflow(process_docs),
        'processes': []
    }
    
    # Add individual process data for detailed sheets
    for doc in process_docs:
        process_name = doc.get('metadata', {}).get('process_name', 'Unknown')
        consolidated['processes'].append({
            'name': process_name,
            'activity_count': doc.get('metadata', {}).get('activity_count', 0),
            'business_requirements': doc.get('business_requirements', {}),
            'workflow': doc.get('workflow', {}),
            'configuration': doc.get('configuration', {}),
            'activity_guide': doc.get('activity_guide', {}),
            'validation': doc.get('validation', {})
        })
    
    # Save consolidated documentation
    output_path = f"Temp/{rice_item}_consolidated_documentation.json"
    with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"✓ Consolidated documentation created: {output_path}")
    print(f"  RICE Item: {rice_item}")
    print(f"  Processes: {len(process_names)}")
    print(f"  Total Activities: {consolidated['metadata']['total_activities']}")
    print(f"  Has Spec: {bool(consolidated['business_requirements'])}")
    print(f"  Has WU Logs: {consolidated['validation'].get('has_wu_log', False)}")
    print(f"  File size: {len(json.dumps(consolidated))} bytes")
    print("=" * 60)
    
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python consolidate_processes.py <rice_item> <process_name1> [<process_name2> ...]")
        print("\nExample:")
        print("  python consolidate_processes.py APIA InvoiceApproval_APIA_NONPOROUTING InvoiceApproval_APIA_NONPOROUTING_Reject")
        sys.exit(1)
    
    rice_item = sys.argv[1]
    process_names = sys.argv[2:]
    
    try:
        output_path = consolidate_processes(rice_item, process_names)
        print(f"\n✓ Success! Consolidated documentation ready for report generation.")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
