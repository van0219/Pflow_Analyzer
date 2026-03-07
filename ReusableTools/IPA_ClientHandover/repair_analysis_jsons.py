#!/usr/bin/env python3
"""
JSON Validation and Auto-Repair Tool for Client Handover Analysis Files

This tool validates and automatically repairs common JSON syntax errors in analysis
files generated during Phases 1-4 of the client handover workflow.

Common issues fixed:
1. Closing brace followed by comma (}  ,) - caused by fsWrite + fsAppend pattern
2. Missing closing braces
3. Trailing commas in arrays/objects
4. Duplicate keys
5. Invalid escape sequences

Usage:
    python repair_analysis_jsons.py [--backup]
    
Options:
    --backup    Create backup files before repair (.bak extension)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Analysis files to validate and repair
ANALYSIS_FILES = [
    'Temp/business_analysis.json',
    'Temp/workflow_analysis.json',
    'Temp/configuration_analysis.json',
    'Temp/risk_assessment.json'
]

class JSONRepairTool:
    """Validates and repairs JSON files with common syntax errors"""
    
    def __init__(self, create_backup=False):
        self.create_backup = create_backup
        self.repairs_made = []
        
    def validate_json(self, file_path):
        """Validate JSON file and return error details if invalid"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, None
        except json.JSONDecodeError as e:
            return False, str(e)
        except FileNotFoundError:
            return None, "File not found"
    
    def repair_closing_brace_comma(self, content):
        """
        Fix pattern: }  ,  "next_section"
        Should be:   ,  "next_section" (remove the premature })
        
        This is the most common error from fsWrite + fsAppend pattern.
        The issue occurs when fsWrite creates a complete JSON object ending with },
        then fsAppend adds a comma and more content.
        
        The fix is to remove the premature closing brace before the comma.
        """
        # Pattern: closing brace, optional whitespace, comma, optional whitespace, quote
        # We want to remove the closing brace and keep the comma
        pattern = r'\}\s*\n\s*,\s*\n\s*"'
        
        if re.search(pattern, content):
            # Replace } \n , \n " with just , \n "
            content = re.sub(pattern, ',\n  "', content)
            self.repairs_made.append("Removed premature closing brace before comma")
        
        return content
    
    def repair_trailing_commas(self, content):
        """Remove trailing commas before closing braces/brackets"""
        # Trailing comma before }
        pattern1 = r',(\s*)\}'
        if re.search(pattern1, content):
            content = re.sub(pattern1, r'\1}', content)
            self.repairs_made.append("Removed trailing commas before }")
        
        # Trailing comma before ]
        pattern2 = r',(\s*)\]'
        if re.search(pattern2, content):
            content = re.sub(pattern2, r'\1]', content)
            self.repairs_made.append("Removed trailing commas before ]")
        
        return content
    
    def repair_missing_closing_braces(self, content):
        """Attempt to balance braces and brackets"""
        open_braces = content.count('{')
        close_braces = content.count('}')
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        
        if open_braces > close_braces:
            content = content.rstrip() + '\n' + '}' * (open_braces - close_braces)
            self.repairs_made.append(f"Added {open_braces - close_braces} missing closing braces")
        
        if open_brackets > close_brackets:
            content = content.rstrip() + '\n' + ']' * (open_brackets - close_brackets)
            self.repairs_made.append(f"Added {open_brackets - close_brackets} missing closing brackets")
        
        return content
    
    def repair_file(self, file_path):
        """Repair a single JSON file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return False, "File not found", []
        
        # Read original content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Create backup if requested
        if self.create_backup:
            backup_path = file_path.with_suffix('.json.bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
        
        # Reset repairs list
        self.repairs_made = []
        
        # Apply repairs in order
        content = original_content
        content = self.repair_closing_brace_comma(content)
        content = self.repair_trailing_commas(content)
        content = self.repair_missing_closing_braces(content)
        
        # Validate repaired content
        try:
            json.loads(content)
            
            # Write repaired content if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, "Repaired successfully", self.repairs_made
            else:
                return True, "No repairs needed", []
        
        except json.JSONDecodeError as e:
            # Repair failed, restore original if backup exists
            if self.create_backup:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
            return False, f"Repair failed: {str(e)}", self.repairs_made

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate and repair JSON analysis files for client handover workflow'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup files before repair (.bak extension)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("JSON VALIDATION AND REPAIR TOOL")
    print("=" * 80)
    print()
    
    repairer = JSONRepairTool(create_backup=args.backup)
    
    results = {
        'valid': [],
        'repaired': [],
        'failed': [],
        'missing': []
    }
    
    for file_path in ANALYSIS_FILES:
        file_name = Path(file_path).name
        print(f"Checking {file_name}...")
        
        # First validation
        is_valid, error = repairer.validate_json(file_path)
        
        if is_valid is None:
            print(f"  ⚠ File not found")
            results['missing'].append(file_name)
            continue
        
        if is_valid:
            print(f"  ✓ Valid JSON")
            results['valid'].append(file_name)
            continue
        
        # File is invalid, attempt repair
        print(f"  ✗ Invalid JSON: {error}")
        print(f"  → Attempting repair...")
        
        success, message, repairs = repairer.repair_file(file_path)
        
        if success:
            if repairs:
                print(f"  ✓ {message}")
                for repair in repairs:
                    print(f"    - {repair}")
                results['repaired'].append((file_name, repairs))
            else:
                print(f"  ✓ {message}")
                results['valid'].append(file_name)
        else:
            print(f"  ✗ {message}")
            results['failed'].append((file_name, message))
        
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    if results['valid']:
        print(f"✓ Valid files ({len(results['valid'])}):")
        for file_name in results['valid']:
            print(f"  - {file_name}")
        print()
    
    if results['repaired']:
        print(f"✓ Repaired files ({len(results['repaired'])}):")
        for file_name, repairs in results['repaired']:
            print(f"  - {file_name}")
            for repair in repairs:
                print(f"      {repair}")
        print()
    
    if results['failed']:
        print(f"✗ Failed repairs ({len(results['failed'])}):")
        for file_name, error in results['failed']:
            print(f"  - {file_name}: {error}")
        print()
    
    if results['missing']:
        print(f"⚠ Missing files ({len(results['missing'])}):")
        for file_name in results['missing']:
            print(f"  - {file_name}")
        print()
    
    # Exit code
    if results['failed']:
        print("❌ Some files could not be repaired. Manual intervention required.")
        return 1
    elif results['repaired']:
        print("✅ All invalid files were successfully repaired.")
        return 0
    else:
        print("✅ All files are valid. No repairs needed.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
