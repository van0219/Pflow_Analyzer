#!/usr/bin/env python3
"""
Violation Merger
Merges domain-specific violation files into a single master violations file.

Usage:
    python merge_violations.py <output_prefix>
    
Example:
    python merge_violations.py Temp/Process
    
    Reads:
    - Temp/Process_violations_naming.json
    - Temp/Process_violations_javascript.json
    - Temp/Process_violations_sql.json
    - Temp/Process_violations_errorhandling.json
    - Temp/Process_violations_structure.json
    
    Outputs:
    - Temp/Process_master_violations.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class ViolationMerger:
    """Merges domain-specific violations into master file."""
    
    def __init__(self, output_prefix: str):
        self.output_prefix = output_prefix
        self.domains = ['naming', 'javascript', 'sql', 'errorhandling', 'structure']
        self.violations = {}
        
    def load_domain_violations(self, domain: str) -> Dict[str, Any]:
        """Load violations for a specific domain."""
        file_path = f"{self.output_prefix}_violations_{domain}.json"
        
        if not Path(file_path).exists():
            print(f"⚠ Warning: {file_path} not found, skipping")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                data = json.load(f)
            print(f"✓ Loaded {domain} violations")
            return data
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return {}
    
    def merge_all_violations(self) -> Dict[str, Any]:
        """Merge all domain violations into master structure."""
        master = {
            'summary_metrics': {
                'total_violations': 0,
                'high_severity': 0,
                'medium_severity': 0,
                'low_severity': 0,
                'domains_analyzed': []
            },
            'violations_by_domain': {},
            'violations_by_severity': {
                'high': [],
                'medium': [],
                'low': []
            },
            'all_violations': [],
            'statistics': {},
            'metadata': {}
        }
        
        # Load each domain
        for domain in self.domains:
            domain_data = self.load_domain_violations(domain)
            
            if not domain_data:
                continue
            
            master['summary_metrics']['domains_analyzed'].append(domain)
            
            # Handle both formats: direct array or dictionary with 'violations' key
            if isinstance(domain_data, list):
                # Direct array format
                violations = domain_data
                master['violations_by_domain'][domain] = violations
            elif isinstance(domain_data, dict):
                # Dictionary format
                violations = domain_data.get('violations', [])
                master['violations_by_domain'][domain] = violations
                
                # Merge statistics if present
                if 'statistics' in domain_data:
                    master['statistics'][domain] = domain_data['statistics']
                
                # Merge metadata if present (first domain wins)
                if 'metadata' in domain_data and not master['metadata']:
                    master['metadata'] = domain_data['metadata']
            else:
                print(f"⚠ Warning: Unexpected format for {domain}, skipping")
                continue
            
            # Extract violations list (now guaranteed to be a list)
            # Extract violations list (now guaranteed to be a list)
            
            # Count by severity
            for violation in violations:
                severity = violation.get('severity', 'Low').lower()
                master['summary_metrics']['total_violations'] += 1
                
                if severity == 'high':
                    master['summary_metrics']['high_severity'] += 1
                    master['violations_by_severity']['high'].append(violation)
                elif severity == 'medium':
                    master['summary_metrics']['medium_severity'] += 1
                    master['violations_by_severity']['medium'].append(violation)
                else:
                    master['summary_metrics']['low_severity'] += 1
                    master['violations_by_severity']['low'].append(violation)
                
                # Add to all violations with domain tag
                violation_with_domain = violation.copy()
                violation_with_domain['domain'] = domain
                master['all_violations'].append(violation_with_domain)
        
        return master
    
    def save_master_violations(self, master: Dict[str, Any]):
        """Save master violations file."""
        output_path = f"{self.output_prefix}_master_violations.json"
        
        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(master, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Master violations saved: {output_path}")
        print(f"\nSummary:")
        print(f"  Total violations: {master['summary_metrics']['total_violations']}")
        print(f"  High severity: {master['summary_metrics']['high_severity']}")
        print(f"  Medium severity: {master['summary_metrics']['medium_severity']}")
        print(f"  Low severity: {master['summary_metrics']['low_severity']}")
        print(f"  Domains analyzed: {', '.join(master['summary_metrics']['domains_analyzed'])}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_violations.py <output_prefix>")
        print("\nExample:")
        print("  python merge_violations.py Temp/Process")
        sys.exit(1)
    
    output_prefix = sys.argv[1]
    
    print(f"Merging violations for: {output_prefix}\n")
    
    merger = ViolationMerger(output_prefix)
    master = merger.merge_all_violations()
    merger.save_master_violations(master)
    
    print(f"\n✓ Merge complete!")


if __name__ == "__main__":
    main()
