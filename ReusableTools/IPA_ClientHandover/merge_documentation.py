#!/usr/bin/env python3
"""
IPA Client Handover - Merge Documentation Sections

Merges 5 analyzed documentation files into a single master documentation file.

Usage:
    python merge_documentation.py <output_prefix>
    
    Arguments:
        output_prefix: File prefix used by subagents (e.g., "Temp/ProcessName")
    
    Expects these files to exist:
        <output_prefix>_doc_business.json
        <output_prefix>_doc_workflow.json
        <output_prefix>_doc_configuration.json
        <output_prefix>_doc_activities.json
        <output_prefix>_doc_validation.json
    
    Creates:
        <output_prefix>_master_documentation.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_doc_file(output_prefix, doc_name):
    """Load a documentation file created by subagents, return empty dict if not found"""
    file_path = f"{output_prefix}_doc_{doc_name}.json"
    
    if not Path(file_path).exists():
        print(f"⚠️  Warning: {file_path} not found, using empty data")
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        print(f"✓ Loaded: {file_path} ({len(json.dumps(data))} bytes)")
        return data
    except Exception as e:
        print(f"✗ Error loading {file_path}: {e}")
        return {}


def merge_documentation(output_prefix):
    """
    Merge 5 analyzed documentation files into master documentation file.
    
    Args:
        output_prefix: File prefix for documentation files
    
    Returns:
        Path to master documentation file
    """
    
    print("Merging analyzed documentation files...")
    print("=" * 60)
    
    # Load all analyzed documentation files
    business = load_doc_file(output_prefix, 'business')
    workflow = load_doc_file(output_prefix, 'workflow')
    configuration = load_doc_file(output_prefix, 'configuration')
    activities = load_doc_file(output_prefix, 'activities')
    validation = load_doc_file(output_prefix, 'validation')
    
    # Extract process name from output_prefix
    # output_prefix format: "Temp/ProcessName" or "ProcessName"
    process_name = Path(output_prefix).name  # Gets "ProcessName" from "Temp/ProcessName"
    
    # Extract metadata from analyzed documentation
    activity_count = len(activities.get('activities', []))
    
    # Build master documentation
    master = {
        'metadata': {
            'process_name': process_name,
            'activity_count': activity_count,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sections_analyzed': 5,
            'has_spec': bool(business.get('requirements')),
            'has_wu_log': validation.get('has_wu_log', False)
        },
        'business_requirements': business,
        'workflow': workflow,
        'configuration': configuration,
        'activity_guide': activities,
        'validation': validation
    }
    
    # Save master documentation
    output_path = f"{output_prefix}_master_documentation.json"
    with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"✓ Master documentation created: {output_path}")
    print(f"  Process: {process_name}")
    print(f"  Activities: {activity_count}")
    print(f"  Has Spec: {master['metadata']['has_spec']}")
    print(f"  Has WU Log: {master['metadata']['has_wu_log']}")
    print(f"  File size: {len(json.dumps(master))} bytes")
    
    return output_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python merge_documentation.py <output_prefix>")
        print("  Example: python merge_documentation.py Temp/ProcessName")
        sys.exit(1)
    
    output_prefix = sys.argv[1]
    
    try:
        output_path = merge_documentation(output_prefix)
        print(f"\n✓ Success! Master documentation ready for analysis.")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)