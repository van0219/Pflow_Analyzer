#!/usr/bin/env python3
"""
Validate Kiro hook files - Check JSON validity and structure

Usage:
    python validate_hooks.py                          # Validate all hooks in .kiro/hooks/
    python validate_hooks.py <hook_file>              # Validate specific hook
    python validate_hooks.py <hook1> <hook2> ...      # Validate multiple hooks
    python validate_hooks.py --all                    # Validate all hooks (explicit)
"""

import json
import sys
import glob
from pathlib import Path

def validate_hook(filepath, verbose=True):
    """
    Validate a single hook file
    
    Args:
        filepath: Path to hook file
        verbose: Print detailed output
        
    Returns:
        tuple: (is_valid, hook_data or None)
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"Validating: {filepath}")
        print('='*60)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Required fields
        required_fields = ['enabled', 'name', 'when', 'then']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            if verbose:
                print(f"✗ Missing required fields: {', '.join(missing_fields)}")
            return False, None
        
        if verbose:
            print("✓ Valid JSON structure")
            print(f"✓ Name: {data.get('name', 'N/A')}")
            print(f"✓ Version: {data.get('version', 'N/A')}")
            print(f"✓ Type: {data.get('when', {}).get('type', 'N/A')}")
            print(f"✓ Action: {data.get('then', {}).get('type', 'N/A')}")
            
            # Check prompt if exists
            prompt = data.get('then', {}).get('prompt', '')
            if prompt:
                print(f"✓ Prompt length: {len(prompt)} characters")
            
            command = data.get('then', {}).get('command', '')
            if command:
                print(f"✓ Command length: {len(command)} characters")
        
        return True, data
        
    except json.JSONDecodeError as e:
        if verbose:
            print(f"✗ INVALID JSON: {e}")
        return False, None
    except FileNotFoundError:
        if verbose:
            print(f"✗ FILE NOT FOUND: {filepath}")
        return False, None
    except Exception as e:
        if verbose:
            print(f"✗ ERROR: {e}")
        return False, None

def find_all_hooks(hooks_dir='.kiro/hooks'):
    """Find all .kiro.hook files in directory"""
    hook_files = glob.glob(f"{hooks_dir}/*.kiro.hook")
    return sorted(hook_files)

def main():
    """Main validation function"""
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == '--all'):
        # Validate all hooks
        hooks = find_all_hooks()
        if not hooks:
            print("No hook files found in .kiro/hooks/")
            sys.exit(1)
    else:
        # Validate specified hooks
        hooks = sys.argv[1:]
    
    print(f"Validating {len(hooks)} hook file(s)...")
    
    results = {}
    for hook in hooks:
        is_valid, data = validate_hook(hook, verbose=True)
        results[hook] = is_valid
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    valid_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for hook, is_valid in results.items():
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:12} {hook}")
    
    print(f"\n{valid_count}/{total_count} hooks valid")
    
    if valid_count == total_count:
        print("\n✓ ALL HOOKS VALID")
        sys.exit(0)
    else:
        print("\n✗ SOME HOOKS HAVE ERRORS")
        sys.exit(1)

if __name__ == "__main__":
    main()
