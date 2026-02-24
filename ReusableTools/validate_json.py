#!/usr/bin/env python3
"""
Generic JSON validator with hook-specific validation.

Usage:
    python ReusableTools/validate_json.py <file.json>
    python ReusableTools/validate_json.py <file.kiro.hook>
    
Auto-detects hook files and applies additional validation rules.
"""

import json
import sys
import os
from pathlib import Path


def is_hook_file(filepath):
    """Check if file is a Kiro hook based on extension or location."""
    path = Path(filepath)
    return (
        path.suffix == '.hook' or 
        '.kiro.hook' in path.name or
        '.kiro/hooks' in str(path)
    )


def validate_json_syntax(filepath):
    """Validate basic JSON syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, {
            'type': 'JSONDecodeError',
            'message': str(e),
            'line': e.lineno,
            'column': e.colno,
            'detail': e.msg
        }
    except Exception as e:
        return False, None, {
            'type': type(e).__name__,
            'message': str(e)
        }


def validate_hook_structure(data):
    """Validate hook-specific requirements."""
    errors = []
    warnings = []
    
    # Required fields
    required_fields = ['name', 'when', 'then']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
    
    # Version field type check (CRITICAL - IDE requirement)
    if 'version' in data:
        if not isinstance(data['version'], str):
            errors.append(
                f"Field 'version' must be a string, not {type(data['version']).__name__}. "
                f"Current value: {data['version']} (IDE will not recognize this hook)"
            )
    
    # Enabled field type check
    if 'enabled' in data:
        if not isinstance(data['enabled'], bool):
            warnings.append(
                f"Field 'enabled' should be boolean, not {type(data['enabled']).__name__}"
            )
    
    # When structure
    if 'when' in data:
        if not isinstance(data['when'], dict):
            errors.append("Field 'when' must be an object/dict")
        elif 'type' not in data['when']:
            errors.append("Field 'when.type' is required")
        else:
            valid_when_types = [
                'fileEdited', 'fileCreated', 'fileDeleted', 
                'userTriggered', 'promptSubmit', 'agentStop',
                'preToolUse', 'postToolUse', 'preTaskExecution', 'postTaskExecution'
            ]
            if data['when']['type'] not in valid_when_types:
                warnings.append(
                    f"Unknown when.type: '{data['when']['type']}'. "
                    f"Valid types: {', '.join(valid_when_types)}"
                )
    
    # Then structure
    if 'then' in data:
        if not isinstance(data['then'], dict):
            errors.append("Field 'then' must be an object/dict")
        elif 'type' not in data['then']:
            errors.append("Field 'then.type' is required")
        else:
            valid_then_types = ['askAgent', 'runCommand']
            if data['then']['type'] not in valid_then_types:
                errors.append(
                    f"Invalid then.type: '{data['then']['type']}'. "
                    f"Valid types: {', '.join(valid_then_types)}"
                )
            
            # Check for required fields based on then.type
            if data['then']['type'] == 'askAgent' and 'prompt' not in data['then']:
                errors.append("Field 'then.prompt' is required for askAgent hooks")
            elif data['then']['type'] == 'runCommand' and 'command' not in data['then']:
                errors.append("Field 'then.command' is required for runCommand hooks")
    
    return errors, warnings


def print_validation_report(filepath, is_hook, json_valid, data, json_error, hook_errors, hook_warnings):
    """Print formatted validation report."""
    print("=" * 70)
    print(f"JSON VALIDATION REPORT: {filepath}")
    print("=" * 70)
    
    # File type
    file_type = "Kiro Hook" if is_hook else "JSON File"
    print(f"\nFILE TYPE: {file_type}")
    
    # JSON syntax validation
    if json_valid:
        print("\n✓ JSON SYNTAX: VALID")
        print(f"  File size: {os.path.getsize(filepath)} bytes")
        if data:
            print(f"  Top-level type: {type(data).__name__}")
            if isinstance(data, dict):
                print(f"  Keys: {', '.join(data.keys())}")
    else:
        print("\n❌ JSON SYNTAX: INVALID")
        if json_error:
            print(f"  Error type: {json_error['type']}")
            print(f"  Message: {json_error['message']}")
            if 'line' in json_error:
                print(f"  Location: Line {json_error['line']}, Column {json_error['column']}")
            if 'detail' in json_error:
                print(f"  Detail: {json_error['detail']}")
        return  # Stop here if JSON is invalid
    
    # Hook-specific validation
    if is_hook:
        print("\n" + "=" * 70)
        print("HOOK-SPECIFIC VALIDATION")
        print("=" * 70)
        
        if hook_errors:
            print(f"\n❌ ERRORS ({len(hook_errors)}):")
            for i, error in enumerate(hook_errors, 1):
                print(f"  {i}. {error}")
        else:
            print("\n✓ No errors found")
        
        if hook_warnings:
            print(f"\n⚠️  WARNINGS ({len(hook_warnings)}):")
            for i, warning in enumerate(hook_warnings, 1):
                print(f"  {i}. {warning}")
        else:
            print("\n✓ No warnings")
        
        # Overall status
        print("\n" + "=" * 70)
        if not hook_errors:
            print("✓ HOOK STATUS: VALID (IDE should recognize this hook)")
        else:
            print("❌ HOOK STATUS: INVALID (IDE will NOT recognize this hook)")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✓ STATUS: Valid JSON file")
        print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_json.py <file.json>")
        print("\nValidates JSON syntax for any file.")
        print("Auto-detects hook files and applies additional validation.")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    
    # Detect file type
    is_hook = is_hook_file(filepath)
    
    # Validate JSON syntax
    json_valid, data, json_error = validate_json_syntax(filepath)
    
    # Validate hook structure if applicable
    hook_errors = []
    hook_warnings = []
    if is_hook and json_valid and data:
        hook_errors, hook_warnings = validate_hook_structure(data)
    
    # Print report
    print_validation_report(
        filepath, is_hook, json_valid, data, 
        json_error, hook_errors, hook_warnings
    )
    
    # Exit code
    if not json_valid or (is_hook and hook_errors):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
