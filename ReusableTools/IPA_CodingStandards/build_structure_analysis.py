#!/usr/bin/env python3
"""
IPA Coding Standards - Structure Analysis Builder
Direct analysis script for process structure domain (no chunking needed).

Usage:
    python build_structure_analysis.py
"""

import json
import sys
from pathlib import Path

def load_json(filepath):
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """Save JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    """Analyze structure domain data"""
    print("=" * 80)
    print("PHASE 5: STRUCTURE ANALYSIS")
    print("=" * 80)
    print()
    
    temp_dir = Path('Temp')
    
    # Check if analysis already exists (AI has completed it)
    output_file = temp_dir / 'structure_analysis.json'
    if output_file.exists():
        print("[1/2] Structure analysis found, adding rule_name...")
        
        # Load existing analysis
        analysis = load_json(output_file)
        
        # Load project standards for rule_name mapping
        standards_file = temp_dir / 'project_standards.json'
        rule_map = {}
        if standards_file.exists():
            project_standards = load_json(standards_file)
            rule_map = {std['Rule_ID']: std['Rule_Name'] for std in project_standards}
        
        # Add rule_name to all violations
        violations = analysis.get('violations', [])
        for v in violations:
            if 'rule_name' not in v:  # Only add if missing
                rule_id = v.get('rule_id', 'Custom')
                if rule_id in rule_map:
                    v['rule_name'] = f"{rule_id}: {rule_map[rule_id]}"
                else:
                    v['rule_name'] = f"{rule_id}: {v.get('category', 'Custom Rule')}"
        
        print(f"   ✓ Added rule_name to {len(violations)} violations")
        
        # Save updated analysis
        print(f"[2/2] Saving updated analysis...")
        save_json(analysis, output_file)
        print(f"   ✓ {output_file}")
        
        print()
        print("=" * 80)
        print("PHASE 5 COMPLETE")
        print("=" * 80)
        print()
        
        return 0
    
    # If analysis doesn't exist, prepare data for AI
    domain_files = list(temp_dir.glob('*_domain_structure.json'))
    
    if not domain_files:
        print("❌ Error: No structure domain file found")
        sys.exit(1)
    
    domain_file = domain_files[0]
    print(f"[1/3] Loading structure domain data: {domain_file.name}")
    structure_data = load_json(domain_file)
    
    standards_file = temp_dir / 'project_standards.json'
    print(f"[2/3] Loading project standards: {standards_file.name}")
    project_standards = load_json(standards_file)
    
    metrics_file = temp_dir / 'metrics_summary.json'
    print(f"[3/3] Loading metrics summary: {metrics_file.name}")
    metrics = load_json(metrics_file)
    
    print()
    print("Structure data ready for AI analysis")
    print("AI should analyze and create structure_analysis.json")
    print()
    
    # Create placeholder
    analysis = {
        'domain': 'structure',
        'violations': [],
        'notes': 'AI analysis required for structure domain'
    }
    
    save_json(analysis, output_file)
    print(f"✓ Placeholder created: {output_file.name}")
    
    print()
    print("=" * 80)
    print("PHASE 5 READY")
    print("=" * 80)
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
