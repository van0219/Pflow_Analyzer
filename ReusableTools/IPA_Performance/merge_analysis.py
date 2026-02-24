#!/usr/bin/env python3
"""
Work Unit Analysis Merger

Purpose: Merge 4 area analysis files into master analysis
This tool does NOT analyze - it only merges analyzed data

Input: 4 analysis files from subagents
Output: Master analysis JSON

Usage:
    python merge_analysis.py <output_prefix>
    
Example:
    python merge_analysis.py Temp/CISOutbound
    
    Reads:
    - Temp/CISOutbound_analysis_activities.json
    - Temp/CISOutbound_analysis_errors.json
    - Temp/CISOutbound_analysis_performance.json
    - Temp/CISOutbound_analysis_code.json
    
    Outputs:
    - Temp/CISOutbound_master_analysis.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Import validator
sys.path.insert(0, str(Path(__file__).parent))
from validate_analysis_schema import SchemaValidator


class AnalysisMerger:
    """Merges area analysis files into master analysis."""
    
    def __init__(self, output_prefix: str):
        self.output_prefix = output_prefix
        self.areas = ['activities', 'errors', 'performance', 'code']
        self.analyses = {}
        
    def load_area_analysis(self, area: str) -> Dict[str, Any]:
        """Load and validate analysis for a specific area."""
        file_path = f"{self.output_prefix}_analysis_{area}.json"
        
        if not Path(file_path).exists():
            print(f"⚠ Warning: {file_path} not found, skipping")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                data = json.load(f)
            
            # Validate schema
            validator = SchemaValidator(area)
            is_valid = validator.validate(data)
            
            if not is_valid:
                print(f"⚠ Schema validation failed for {area}:")
                print(validator.get_report())
                print(f"⚠ Continuing with potentially incomplete data...")
            else:
                print(f"✓ Loaded {area} analysis (schema valid)")
            
            return data
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return {}
    
    def merge_all_analyses(self) -> Dict[str, Any]:
        """Merge all area analyses into master structure."""
        master = {
            'summary': {
                'areas_analyzed': [],
                'total_activities': 0,
                'total_errors': 0,
                'total_issues': 0
            },
            'activities_analysis': {},
            'errors_analysis': {},
            'performance_analysis': {},
            'code_analysis': {},
            'metadata': {}
        }
        
        # Load each area
        for area in self.areas:
            area_data = self.load_area_analysis(area)
            
            if not area_data:
                continue
            
            master['summary']['areas_analyzed'].append(area)
            
            # Store area analysis
            if area == 'activities':
                master['activities_analysis'] = area_data
                master['summary']['total_activities'] = area_data.get('statistics', {}).get('total_activities', 0)
            elif area == 'errors':
                master['errors_analysis'] = area_data
                master['summary']['total_errors'] = area_data.get('statistics', {}).get('total_errors', 0)
            elif area == 'performance':
                master['performance_analysis'] = area_data
            elif area == 'code':
                master['code_analysis'] = area_data
                master['summary']['total_issues'] = area_data.get('statistics', {}).get('total_issues', 0)
            
            # Merge metadata (first area wins)
            if 'metadata' in area_data and not master['metadata']:
                master['metadata'] = area_data['metadata']
        
        return master
    
    def save_master_analysis(self, master: Dict[str, Any]):
        """Save master analysis file."""
        output_path = f"{self.output_prefix}_master_analysis.json"
        
        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(master, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Master analysis saved: {output_path}")
        print(f"\nSummary:")
        print(f"  Areas analyzed: {', '.join(master['summary']['areas_analyzed'])}")
        print(f"  Total activities: {master['summary']['total_activities']}")
        print(f"  Total errors: {master['summary']['total_errors']}")
        print(f"  Total issues: {master['summary']['total_issues']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_analysis.py <output_prefix>")
        print("\nExample:")
        print("  python merge_analysis.py Temp/CISOutbound")
        sys.exit(1)
    
    output_prefix = sys.argv[1]
    
    print(f"Merging analyses for: {output_prefix}\n")
    
    merger = AnalysisMerger(output_prefix)
    master = merger.merge_all_analyses()
    merger.save_master_analysis(master)
    
    print(f"\n✓ Merge complete!")


if __name__ == "__main__":
    main()