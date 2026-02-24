#!/usr/bin/env python3
"""
WU Analysis Schema Validator

Purpose: Validate subagent JSON outputs match expected schema
Ensures uniform structure across different runs

Usage:
    python validate_analysis_schema.py <analysis_file> <schema_type>
    
Example:
    python validate_analysis_schema.py Temp/Process_analysis_activities.json activities
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List


# Schema definitions for each analysis type
SCHEMAS = {
    'activities': {
        'required_fields': ['metadata', 'statistics', 'activities', 'activity_type_summary', 'execution_pattern'],
        'metadata_fields': ['work_unit_number', 'process_name', 'status', 'total_duration_ms', 'total_duration_readable'],
        'statistics_fields': ['total_activities', 'total_duration_ms', 'average_duration_ms', 'slow_activities_count'],
        'activity_fields': ['name', 'type', 'duration_ms', 'duration_readable', 'status', 'is_slow'],
        'execution_pattern_fields': ['linear', 'has_loops', 'has_branches', 'complexity']
    },
    'errors': {
        'required_fields': ['metadata', 'statistics', 'errors', 'error_summary'],
        'metadata_fields': ['work_unit_number', 'process_name'],
        'statistics_fields': ['total_errors', 'critical', 'high', 'medium', 'low'],
        'error_fields': ['activity', 'type', 'message', 'severity', 'impact'],
        'error_summary_fields': ['most_common_type', 'affected_activities', 'process_impact']
    },
    'performance': {
        'required_fields': ['metadata', 'statistics', 'performance_metrics', 'bottlenecks', 'memory_analysis', 'efficiency_assessment'],
        'metadata_fields': ['work_unit_number', 'process_name', 'total_duration_ms', 'total_duration_readable'],
        'statistics_fields': ['total_duration_ms', 'total_duration_readable', 'efficiency_rating', 'bottleneck_count'],
        'performance_metrics_fields': ['duration_ms', 'throughput'],
        'bottleneck_fields': ['activity', 'type', 'duration_ms', 'percentage_of_total', 'severity', 'recommendation'],
        'memory_analysis_fields': ['work_unit_id', 'activity', 'type', 'duration_ms', 'efficiency', 'rating'],
        'efficiency_assessment_fields': ['overall_rating', 'strengths', 'weaknesses']
    },
    'code': {
        'required_fields': ['metadata', 'statistics', 'js_issues', 'sql_issues', 'code_summary'],
        'metadata_fields': ['work_unit_number', 'process_name'],
        'statistics_fields': ['total_issues', 'js_issues', 'sql_issues'],
        'code_summary_fields': ['js_compliance', 'sql_compliance', 'overall_assessment']
    }
}


class SchemaValidator:
    """Validates JSON analysis files against expected schemas."""
    
    def __init__(self, schema_type: str):
        if schema_type not in SCHEMAS:
            raise ValueError(f"Unknown schema type: {schema_type}. Valid types: {list(SCHEMAS.keys())}")
        self.schema = SCHEMAS[schema_type]
        self.schema_type = schema_type
        self.errors = []
        self.warnings = []
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate data against schema. Returns True if valid."""
        self.errors = []
        self.warnings = []
        
        # Check required top-level fields
        for field in self.schema['required_fields']:
            if field not in data:
                self.errors.append(f"Missing required field: {field}")
        
        # Validate metadata
        if 'metadata' in data:
            self._validate_fields(data['metadata'], self.schema['metadata_fields'], 'metadata')
        
        # Validate statistics
        if 'statistics' in data:
            self._validate_fields(data['statistics'], self.schema['statistics_fields'], 'statistics')
        
        # Schema-specific validations
        if self.schema_type == 'activities':
            self._validate_activities(data)
        elif self.schema_type == 'errors':
            self._validate_errors(data)
        elif self.schema_type == 'performance':
            self._validate_performance(data)
        elif self.schema_type == 'code':
            self._validate_code(data)
        
        return len(self.errors) == 0
    
    def _validate_fields(self, obj: Dict, required_fields: List[str], context: str):
        """Validate object has required fields."""
        for field in required_fields:
            if field not in obj:
                self.warnings.append(f"{context}: Missing recommended field '{field}'")
    
    def _validate_activities(self, data: Dict):
        """Validate activities-specific structure."""
        if 'activities' in data and data['activities']:
            # Check first activity has required fields
            first_activity = data['activities'][0]
            self._validate_fields(first_activity, self.schema['activity_fields'], 'activities[0]')
        
        if 'execution_pattern' in data:
            self._validate_fields(data['execution_pattern'], self.schema['execution_pattern_fields'], 'execution_pattern')
    
    def _validate_errors(self, data: Dict):
        """Validate errors-specific structure."""
        if 'errors' in data and data['errors']:
            # Check first error has required fields
            first_error = data['errors'][0]
            self._validate_fields(first_error, self.schema['error_fields'], 'errors[0]')
        
        if 'error_summary' in data:
            self._validate_fields(data['error_summary'], self.schema['error_summary_fields'], 'error_summary')
    
    def _validate_performance(self, data: Dict):
        """Validate performance-specific structure."""
        if 'performance_metrics' in data:
            self._validate_fields(data['performance_metrics'], self.schema['performance_metrics_fields'], 'performance_metrics')
        
        if 'bottlenecks' in data and data['bottlenecks']:
            first_bottleneck = data['bottlenecks'][0]
            self._validate_fields(first_bottleneck, self.schema['bottleneck_fields'], 'bottlenecks[0]')
        
        if 'memory_analysis' in data and data['memory_analysis']:
            first_mem = data['memory_analysis'][0]
            self._validate_fields(first_mem, self.schema['memory_analysis_fields'], 'memory_analysis[0]')
        
        if 'efficiency_assessment' in data:
            self._validate_fields(data['efficiency_assessment'], self.schema['efficiency_assessment_fields'], 'efficiency_assessment')
    
    def _validate_code(self, data: Dict):
        """Validate code-specific structure."""
        if 'code_summary' in data:
            self._validate_fields(data['code_summary'], self.schema['code_summary_fields'], 'code_summary')
        
        # Validate js_issues and sql_issues are arrays
        if 'js_issues' in data and not isinstance(data['js_issues'], list):
            self.errors.append("js_issues must be an array")
        
        if 'sql_issues' in data and not isinstance(data['sql_issues'], list):
            self.errors.append("sql_issues must be an array")
    
    def get_report(self) -> str:
        """Get validation report."""
        report = []
        
        if self.errors:
            report.append("❌ VALIDATION ERRORS:")
            for error in self.errors:
                report.append(f"  - {error}")
        
        if self.warnings:
            report.append("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                report.append(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            report.append("✓ Validation passed - schema is correct")
        
        return "\n".join(report)


def validate_file(file_path: str, schema_type: str) -> bool:
    """Validate a JSON file against schema."""
    print(f"Validating {file_path} against '{schema_type}' schema...")
    
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON: {e}")
        return False
    
    validator = SchemaValidator(schema_type)
    is_valid = validator.validate(data)
    
    print(validator.get_report())
    
    return is_valid


def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_analysis_schema.py <analysis_file> <schema_type>")
        print("\nSchema types: activities, errors, performance, code")
        print("\nExample:")
        print("  python validate_analysis_schema.py Temp/Process_analysis_activities.json activities")
        sys.exit(1)
    
    file_path = sys.argv[1]
    schema_type = sys.argv[2]
    
    is_valid = validate_file(file_path, schema_type)
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
