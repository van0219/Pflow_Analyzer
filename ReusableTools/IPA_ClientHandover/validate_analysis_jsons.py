#!/usr/bin/env python3
"""
Validate Client Handover Analysis JSON Files

This script validates that all required JSON files exist and have the correct structure
before attempting to assemble the client handover report.

Usage:
    python validate_analysis_jsons.py [temp_dir]

Returns:
    Exit code 0 if all validations pass
    Exit code 1 if any validation fails
"""

import sys
import json
import os
from pathlib import Path


def validate_file_exists(filepath):
    """Check if file exists"""
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    return True, f"✓ File exists: {filepath}"


def validate_json_parseable(filepath):
    """Check if file contains valid JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, f"✓ Valid JSON: {filepath}", data
    except json.JSONDecodeError as e:
        return False, f"✗ Invalid JSON in {filepath}: {e}", None
    except Exception as e:
        return False, f"✗ Error reading {filepath}: {e}", None


def validate_lpd_structure(data, filepath):
    """Validate lpd_structure.json"""
    issues = []
    
    if 'processes' not in data:
        issues.append("Missing 'processes' field")
    elif not isinstance(data['processes'], list):
        issues.append("'processes' must be an array")
    
    if issues:
        return False, f"✗ {filepath} structure issues: {', '.join(issues)}"
    return True, f"✓ {filepath} structure valid"


def validate_metrics_summary(data, filepath):
    """Validate metrics_summary.json"""
    issues = []
    
    if 'total_activities' not in data:
        issues.append("Missing 'total_activities' field")
    elif not isinstance(data['total_activities'], (int, float)):
        issues.append("'total_activities' must be a number")
    
    if issues:
        return False, f"✗ {filepath} structure issues: {', '.join(issues)}"
    return True, f"✓ {filepath} structure valid"


def validate_business_analysis(data, filepath):
    """Validate business_analysis.json"""
    issues = []
    warnings = []
    
    # Flexible validation - check for at least one expected field
    expected_fields = [
        'business_requirements', 'business_objectives', 'stakeholders',
        'business_objective', 'rice_item', 'integrations'
    ]
    
    has_content = any(field in data for field in expected_fields)
    
    if not has_content:
        return False, f"✗ {filepath} missing expected fields (need at least one of: {', '.join(expected_fields)})"
    
    # Check business_objectives structure (recommended format)
    if 'business_objectives' in data:
        bo = data['business_objectives']
        if isinstance(bo, dict):
            if 'overview' not in bo:
                warnings.append("business_objectives.overview missing (recommended)")
            if 'objectives' not in bo:
                warnings.append("business_objectives.objectives missing (recommended)")
        elif isinstance(bo, list):
            warnings.append("business_objectives is a list (dict format recommended)")
        else:
            warnings.append(f"business_objectives has unexpected type: {type(bo).__name__}")
    
    # Check for recommended fields
    if 'stakeholders' not in data:
        warnings.append("stakeholders field missing (recommended)")
    if 'functional_requirements' not in data and 'business_requirements' not in data:
        warnings.append("functional_requirements or business_requirements missing (recommended)")
    
    msg = f"✓ {filepath} structure valid"
    if warnings:
        msg += f"\n  ⚠ Warnings: {'; '.join(warnings)}"
    
    return True, msg


def validate_workflow_analysis(data, filepath):
    """Validate workflow_analysis.json"""
    # Flexible validation - check for at least one expected field
    expected_fields = [
        'decision_points', 'workflow_steps', 'workflow_phases',
        'process_name', 'process_type'
    ]
    
    has_content = any(field in data for field in expected_fields)
    
    if not has_content:
        return False, f"✗ {filepath} missing expected fields (need at least one of: {', '.join(expected_fields)})"
    return True, f"✓ {filepath} structure valid"


def validate_configuration_analysis(data, filepath):
    """Validate configuration_analysis.json"""
    # Flexible validation - check for at least one expected field
    expected_fields = [
        'configuration_dependencies', 'configuration_items', 'configuration_sets',
        'file_channels', 'file_channel_configuration',
        'web_services', 'sql_queries', 'sql_query_configuration',
        'hardcoded_values', 'environment_specific_settings'
    ]
    
    has_content = any(field in data for field in expected_fields)
    
    if not has_content:
        return False, f"✗ {filepath} missing expected fields (need at least one of: {', '.join(expected_fields)})"
    return True, f"✓ {filepath} structure valid"


def validate_risk_assessment(data, filepath):
    """Validate risk_assessment.json"""
    # Flexible validation - check for at least one expected field
    expected_fields = [
        'technical_risks', 'maintenance_risks', 'scalability_concerns',
        'compliance_requirements', 'disaster_recovery'
    ]
    
    has_content = any(field in data for field in expected_fields)
    
    if not has_content:
        return False, f"✗ {filepath} missing expected fields (need at least one of: {', '.join(expected_fields)})"
    return True, f"✓ {filepath} structure valid"


def validate_all(temp_dir="Temp"):
    """Validate all required JSON files"""
    print("=" * 80)
    print("CLIENT HANDOVER JSON VALIDATION")
    print("=" * 80)
    
    all_valid = True
    
    # Define required files and their validators
    files_to_validate = [
        ('lpd_structure.json', validate_lpd_structure),
        ('metrics_summary.json', validate_metrics_summary),
        ('business_analysis.json', validate_business_analysis),
        ('workflow_analysis.json', validate_workflow_analysis),
        ('configuration_analysis.json', validate_configuration_analysis),
        ('risk_assessment.json', validate_risk_assessment)
    ]
    
    print(f"\nValidating files in: {temp_dir}/\n")
    
    for filename, validator in files_to_validate:
        filepath = os.path.join(temp_dir, filename)
        
        # Check file exists
        exists, msg = validate_file_exists(filepath)
        print(msg)
        if not exists:
            all_valid = False
            continue
        
        # Check JSON is parseable
        parseable, msg, data = validate_json_parseable(filepath)
        print(msg)
        if not parseable:
            all_valid = False
            continue
        
        # Validate structure
        valid, msg = validator(data, filename)
        print(msg)
        if not valid:
            all_valid = False
        
        print()  # Blank line between files
    
    print("=" * 80)
    if all_valid:
        print("✓ ALL VALIDATIONS PASSED")
        print("=" * 80)
        print("\nReady to run Phase 5 (Report Assembly)")
        return 0
    else:
        print("✗ VALIDATION FAILED")
        print("=" * 80)
        print("\nFix the issues above before running Phase 5")
        return 1


if __name__ == "__main__":
    temp_dir = sys.argv[1] if len(sys.argv) > 1 else "Temp"
    exit_code = validate_all(temp_dir)
    sys.exit(exit_code)
