#!/usr/bin/env python3
"""
Work Unit Data Organizer by Analysis Areas

Purpose: Organize extracted WU data into 4 focused analysis areas
This tool does NOT analyze - it only organizes data for specialized analyzers

Input: Temp/<ProcessName>_wu_data.json (from extract_wu_log.py)
Output: 4 area files for specialized analysis

Usage:
    python organize_by_areas.py <wu_data_json> <output_prefix>
    
Example:
    python organize_by_areas.py Temp/CISOutbound_wu_data.json Temp/CISOutbound
    
    Creates:
    - Temp/CISOutbound_area_activities.json
    - Temp/CISOutbound_area_errors.json
    - Temp/CISOutbound_area_performance.json
    - Temp/CISOutbound_area_code.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class WUDataOrganizer:
    """Organizes WU data into analysis areas."""
    
    def __init__(self, wu_data_file: str, output_prefix: str):
        self.wu_data_file = wu_data_file
        self.output_prefix = output_prefix
        self.wu_data = {}
        
    def load_wu_data(self):
        """Load extracted WU data."""
        print(f"Loading WU data from {self.wu_data_file}...")
        
        with open(self.wu_data_file, 'r', encoding='utf-8', errors='replace') as f:
            self.wu_data = json.load(f)
        
        print(f"✓ Loaded WU data")
        print(f"  - Work Unit: {self.wu_data.get('metadata', {}).get('work_unit_number', 'Unknown')}")
        print(f"  - Activities: {len(self.wu_data.get('activities', []))}")
        print(f"  - Errors: {len(self.wu_data.get('errors', []))}")
    
    def organize_activities(self) -> Dict[str, Any]:
        """Organize activity timeline data."""
        return {
            'metadata': self.wu_data.get('metadata', {}),
            'activities': self.wu_data.get('activities', []),
            'statistics': {
                'total_activities': len(self.wu_data.get('activities', [])),
                'activity_types': self._count_activity_types()
            }
        }
    
    def organize_errors(self) -> Dict[str, Any]:
        """Organize error data."""
        return {
            'metadata': self.wu_data.get('metadata', {}),
            'errors': self.wu_data.get('errors', []),
            'activities': self.wu_data.get('activities', []),  # For context
            'statistics': {
                'total_errors': len(self.wu_data.get('errors', [])),
                'error_activities': self._identify_error_activities()
            }
        }
    
    def organize_performance(self) -> Dict[str, Any]:
        """Organize performance metrics data."""
        return {
            'metadata': self.wu_data.get('metadata', {}),
            'activities': self.wu_data.get('activities', []),
            'variables': self.wu_data.get('variables', {}),
            'statistics': {
                'total_duration_ms': self.wu_data.get('metadata', {}).get('duration_ms'),
                'activity_durations': self._extract_activity_durations(),
                'slow_activities': self._identify_slow_activities()
            }
        }
    
    def organize_code(self) -> Dict[str, Any]:
        """Organize code review data (JavaScript/SQL)."""
        return {
            'metadata': self.wu_data.get('metadata', {}),
            'activities': self.wu_data.get('activities', []),
            'variables': self.wu_data.get('variables', {}),
            'errors': self.wu_data.get('errors', []),  # For JS/SQL error context
            'statistics': {
                'total_activities': len(self.wu_data.get('activities', []))
            }
        }
    
    def _count_activity_types(self) -> Dict[str, int]:
        """Count activities by type."""
        type_counts = {}
        for activity in self.wu_data.get('activities', []):
            activity_type = activity.get('type', 'Unknown')
            type_counts[activity_type] = type_counts.get(activity_type, 0) + 1
        return type_counts
    
    def _identify_error_activities(self) -> List[str]:
        """Identify activities that had errors."""
        error_activities = []
        # This is a placeholder - actual error-activity mapping would need log parsing
        return error_activities
    
    def _extract_activity_durations(self) -> List[Dict[str, Any]]:
        """Extract duration data for all activities."""
        durations = []
        for activity in self.wu_data.get('activities', []):
            if 'duration_ms' in activity and activity['duration_ms'] is not None:
                durations.append({
                    'name': activity.get('name', 'Unknown'),
                    'type': activity.get('type', 'Unknown'),
                    'duration_ms': activity['duration_ms']
                })
        return durations
    
    def _identify_slow_activities(self, threshold_ms: int = 5000) -> List[Dict[str, Any]]:
        """Identify activities slower than threshold."""
        slow = []
        for activity in self.wu_data.get('activities', []):
            duration = activity.get('duration_ms')
            if duration and duration > threshold_ms:
                slow.append({
                    'name': activity.get('name', 'Unknown'),
                    'type': activity.get('type', 'Unknown'),
                    'duration_ms': duration
                })
        return slow
    
    def save_area(self, area_name: str, data: Dict[str, Any]):
        """Save area data to JSON file."""
        output_file = f"{self.output_prefix}_area_{area_name}.json"
        
        with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {area_name} area: {output_file}")
    
    def organize_all(self):
        """Organize all areas."""
        print("\nOrganizing WU data by analysis areas...\n")
        
        # Area 1: Activities
        activities_data = self.organize_activities()
        self.save_area('activities', activities_data)
        
        # Area 2: Errors
        errors_data = self.organize_errors()
        self.save_area('errors', errors_data)
        
        # Area 3: Performance
        performance_data = self.organize_performance()
        self.save_area('performance', performance_data)
        
        # Area 4: Code
        code_data = self.organize_code()
        self.save_area('code', code_data)
        
        print(f"\n✓ Organization complete! Created 4 area files.")


def main():
    if len(sys.argv) < 3:
        print("Usage: python organize_by_areas.py <wu_data_json> <output_prefix>")
        print("\nExample:")
        print("  python organize_by_areas.py Temp/CISOutbound_wu_data.json Temp/CISOutbound")
        sys.exit(1)
    
    wu_data_file = sys.argv[1]
    output_prefix = sys.argv[2]
    
    if not Path(wu_data_file).exists():
        print(f"❌ Error: {wu_data_file} not found")
        sys.exit(1)
    
    organizer = WUDataOrganizer(wu_data_file, output_prefix)
    organizer.load_wu_data()
    organizer.organize_all()


if __name__ == "__main__":
    main()