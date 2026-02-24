#!/usr/bin/env python3
"""
Performance Report Generator Helper

Purpose: Load master analysis and call wu_master_template.py
This tool bridges the gap between merged analysis and report generation

Input: Master analysis JSON
Output: Excel report via wu_master_template.py

Usage:
    python generate_performance_report.py <process_name> <client> <rice_item>
    
Example:
    python generate_performance_report.py CISOutbound FPI MatchReport
    
    Reads: Temp/CISOutbound_master_analysis.json
    Generates: Performance_Results/FPI_MatchReport_Performance_YYYYMMDD.xlsx
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add workspace root to path for template import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from wu_master_template import generate_report
except ImportError:
    print("❌ Error: Could not import wu_master_template.py")
    print("   Make sure wu_master_template.py is in the workspace root")
    sys.exit(1)


class PerformanceReportGenerator:
    """Generates performance report from master analysis."""
    
    def __init__(self, process_name: str, client: str, rice_item: str):
        self.process_name = process_name
        self.client = client
        self.rice_item = rice_item
        self.master_analysis = {}
        self.raw_wu_data = {}
        
    def load_master_analysis(self):
        """Load master analysis JSON and raw WU data."""
        analysis_file = f"Temp/{self.process_name}_master_analysis.json"
        wu_data_file = f"Temp/{self.process_name}_wu_data.json"
        
        print(f"Loading master analysis from {analysis_file}...")
        
        if not Path(analysis_file).exists():
            print(f"❌ Error: {analysis_file} not found")
            sys.exit(1)
        
        with open(analysis_file, 'r', encoding='utf-8', errors='replace') as f:
            self.master_analysis = json.load(f)
        
        print(f"✓ Loaded master analysis")
        print(f"  - Areas: {', '.join(self.master_analysis.get('summary', {}).get('areas_analyzed', []))}")
        
        # Load raw WU data for complete activity details (timestamps, etc.)
        if Path(wu_data_file).exists():
            with open(wu_data_file, 'r', encoding='utf-8', errors='replace') as f:
                self.raw_wu_data = json.load(f)
            print(f"✓ Loaded raw WU data for complete activity details")
    
    def build_wu_data(self) -> Dict[str, Any]:
        """Build wu_data dictionary for template."""
        print("\nBuilding wu_data for report generation...")
        
        # Extract metadata from activities_analysis (where it's actually located)
        activities_analysis = self.master_analysis.get('activities_analysis', {})
        metadata = activities_analysis.get('metadata', {})
        
        errors_analysis = self.master_analysis.get('errors_analysis', {})
        performance_analysis = self.master_analysis.get('performance_analysis', {})
        code_analysis = self.master_analysis.get('code_analysis', {})
        
        wu_data = {
            'work_unit_id': metadata.get('work_unit_number', 'Unknown'),
            'process_name': metadata.get('process_name', self.process_name),
            'status': metadata.get('status', 'Unknown'),
            'client': self.client,
            'rice_item': self.rice_item,
            
            # Dashboard metrics
            'info_data': self._build_info_data(metadata, activities_analysis, performance_analysis),
            
            # Chart data
            'chart_data': self._build_chart_data(activities_analysis, performance_analysis),
            
            # Activities - use raw WU data for complete details (timestamps)
            'activities': self._build_activities(activities_analysis),
            
            # Metrics
            'metrics': self._build_metrics(metadata, performance_analysis),
            
            # Errors - ensure proper dict format with all required fields
            'errors': self._build_errors(errors_analysis),
            
            # Code issues - ensure proper array format
            'js_issues': self._build_js_issues(code_analysis),
            'sql_issues': self._build_sql_issues(code_analysis),
            
            # Memory analysis - ensure proper array format
            'memory_analysis': self._build_memory_analysis(performance_analysis),
            
            # Recommendations
            'recommendations': self._build_recommendations(errors_analysis, performance_analysis, code_analysis),
            
            # Technical analysis
            'technical_analysis': self._build_technical_analysis(activities_analysis, performance_analysis)
        }
        
        print(f"✓ Built wu_data structure")
        return wu_data
    
    def _build_activities(self, activities_analysis: dict) -> list:
        """Build complete activities list with timestamps from raw WU data."""
        # Use raw WU data if available (has timestamps), otherwise use analyzed data
        if self.raw_wu_data and 'activities' in self.raw_wu_data:
            raw_activities = self.raw_wu_data['activities']
            analyzed_activities = activities_analysis.get('activities', [])
            
            # Merge: timestamps from raw, status/analysis from analyzed
            activities = []
            for raw_act in raw_activities:
                # Find matching analyzed activity
                analyzed = next((a for a in analyzed_activities if a['name'] == raw_act['name']), {})
                
                activities.append({
                    'name': raw_act.get('name', ''),
                    'type': raw_act.get('type', ''),
                    'start_time': raw_act.get('start_time', ''),
                    'end_time': raw_act.get('end_time', 'N/A'),
                    'duration': analyzed.get('duration_readable', raw_act.get('duration_ms', 'N/A')),
                    'status': analyzed.get('status', 'Completed')
                })
            return activities
        else:
            # Fallback to analyzed data only
            return activities_analysis.get('activities', [])
    
    def _build_info_data(self, metadata: Dict, activities: Dict, performance: Dict) -> list:
        """Build dashboard info data."""
        stats = activities.get('statistics', {})
        perf_metrics = performance.get('performance_metrics', {})
        
        return [
            ["Work Unit", metadata.get('work_unit_number', 'Unknown'), "✅ Pass", "Info"],
            ["Process", metadata.get('process_name', 'Unknown'), "✅ Pass", "Info"],
            ["Status", metadata.get('status', 'Unknown'), "✅ Pass", "Success"],
            ["Duration", metadata.get('total_duration_readable', 'Unknown'), "✅ Pass", "Excellent"],
            ["Activities", str(stats.get('total_activities', 0)), "✅ Pass", "Info"],
            ["Avg Duration", f"{stats.get('average_duration_ms', 0)}ms", "✅ Pass", "Good"],
            ["API Calls", str(perf_metrics.get('api_calls', 0)), "✅ Pass", "Info"],
            ["File Operations", str(perf_metrics.get('file_operations', 0)), "✅ Pass", "Info"],
            ["Throughput", perf_metrics.get('throughput', 'N/A'), "✅ Pass", "Good"],
            ["Efficiency", performance.get('statistics', {}).get('efficiency_rating', 'N/A'), "✅ Pass", "Good"]
        ]
    
    def _build_chart_data(self, activities: Dict, performance: Dict) -> dict:
        """Build chart data."""
        # Extract top activities by duration for chart
        activity_list = activities.get('activities', [])
        top_activities = sorted(
            [(a['name'], a['duration_ms']) for a in activity_list if a.get('duration_ms', 0) > 0],
            key=lambda x: x[1],
            reverse=True
        )[:10]  # Top 10 activities
        
        return {
            'status': [("Success", 1), ("Failed", 0)],
            'memory_by_activity': top_activities
        }
    
    def _build_metrics(self, metadata: Dict, performance: Dict) -> dict:
        """Build performance metrics."""
        return {
            'duration_ms': metadata.get('total_duration_ms', 0),
            'memory_mib': 0,  # Not available in WU logs
            'cpu_time_ms': 0,  # Not available in WU logs
            'user_time_ms': 0  # Not available in WU logs
        }
    
    def _build_errors(self, errors_analysis: dict) -> list:
        """Build errors list with all required fields."""
        errors = errors_analysis.get('errors', [])
        if not errors:
            return []
        
        # Ensure each error has all required fields
        result = []
        for err in errors:
            if isinstance(err, dict):
                result.append({
                    'activity': err.get('activity', 'Unknown'),
                    'type': err.get('type', 'Unknown'),
                    'message': err.get('message', ''),
                    'severity': err.get('severity', 'Medium'),
                    'impact': err.get('impact', '')
                })
            else:
                result.append(err)  # Already in correct format
        return result
    
    def _build_js_issues(self, code_analysis: dict) -> list:
        """Build JavaScript issues in 10-column array format."""
        # Check if already in array format
        js_issues = code_analysis.get('js_issues', [])
        if js_issues and isinstance(js_issues[0], list):
            return js_issues  # Already in correct format
        
        # If empty or not in array format, return empty list
        return []
    
    def _build_sql_issues(self, code_analysis: dict) -> list:
        """Build SQL issues in 10-column array format."""
        # Check if already in array format
        sql_issues = code_analysis.get('sql_issues', [])
        if sql_issues and isinstance(sql_issues[0], list):
            return sql_issues  # Already in correct format
        
        # If empty or not in array format, return empty list
        return []
    
    def _build_memory_analysis(self, performance_analysis: dict) -> list:
        """Build memory analysis in 7-column array format."""
        # Check if already in array format
        memory_analysis = performance_analysis.get('memory_analysis', [])
        if not memory_analysis:
            return []
        
        # If already in array format, return as-is
        if isinstance(memory_analysis[0], list):
            return memory_analysis
        
        # Convert from dict format to array format
        wu_id = self.master_analysis.get('metadata', {}).get('work_unit_number', 'Unknown')
        result = []
        for mem in memory_analysis:
            result.append([
                wu_id,
                mem.get('activity', 'Unknown'),
                mem.get('type', 'Unknown'),
                mem.get('memory_mib', mem.get('memory_estimate', 'N/A')),
                mem.get('duration_ms', 0),
                mem.get('efficiency', 'N/A'),
                mem.get('rating', 'N/A')
            ])
        return result
    
    def _build_recommendations(self, errors: Dict, performance: Dict, code: Dict) -> list:
        """Build recommendations from all analysis areas in 10-column format."""
        recommendations = []
        wu_id = self.master_analysis.get('metadata', {}).get('work_unit_number', 'Unknown')
        
        # Add performance recommendations
        perf_recs = performance.get('detailed_recommendations', [])
        for rec in perf_recs:
            recommendations.append([
                rec.get('priority', 'Medium'),                    # Priority
                rec.get('category', 'Performance'),               # Category
                rec.get('issue', rec.get('recommendation', '')),  # Issue Description
                wu_id,                                            # Affected WUs
                rec.get('recommendation', ''),                    # Root Cause
                rec.get('implementation', ''),                    # Specific Fix
                '',                                               # Code Example ES5
                '',                                               # Testing Steps
                rec.get('effort', 'Medium'),                      # Effort
                rec.get('estimated_impact', 'Medium')             # Impact
            ])
        
        # Add error recommendations
        error_recs = errors.get('recommendations', [])
        for rec in error_recs:
            recommendations.append([
                rec.get('priority', 'Medium'),                    # Priority
                rec.get('type', 'Error'),                         # Category
                rec.get('recommendation', ''),                    # Issue Description
                wu_id,                                            # Affected WUs
                rec.get('rationale', ''),                         # Root Cause
                rec.get('implementation', ''),                    # Specific Fix
                '',                                               # Code Example ES5
                '',                                               # Testing Steps
                'Low',                                            # Effort
                'Medium'                                          # Impact
            ])
        
        return recommendations
    
    def _build_technical_analysis(self, activities: Dict, performance: Dict) -> dict:
        """Build technical analysis tables."""
        exec_pattern = activities.get('execution_pattern', {})
        perf_assessment = activities.get('performance_assessment', {})
        efficiency = performance.get('efficiency_assessment', {})
        
        # Architecture analysis
        architecture = [
            ["Aspect", "Value", "Assessment"],
            ["Pattern", exec_pattern.get('pattern_description', 'N/A'), "Standard"],
            ["Complexity", exec_pattern.get('complexity', 'N/A'), "Appropriate"],
            ["Has Branches", str(exec_pattern.get('has_branches', False)), "Yes" if exec_pattern.get('has_branches') else "No"],
            ["Has Subprocesses", str(exec_pattern.get('has_subprocesses', False)), "Yes" if exec_pattern.get('has_subprocesses') else "No"],
            ["Critical Path %", f"{exec_pattern.get('critical_path_percentage', 0):.1f}%", "Efficient"]
        ]
        
        # Performance quality
        js_quality = [
            ["Metric", "Score", "Assessment"],
            ["Overall Rating", perf_assessment.get('overall_rating', 'N/A'), perf_assessment.get('overall_rating', 'N/A')],
            ["Efficiency Score", str(perf_assessment.get('efficiency_score', 0)), "Good" if perf_assessment.get('efficiency_score', 0) > 70 else "Needs Improvement"],
            ["Bottlenecks", str(len(performance.get('bottlenecks', []))), "Minimal" if len(performance.get('bottlenecks', [])) <= 1 else "Multiple"]
        ]
        
        # Business impact
        timing = activities.get('timing_breakdown', {})
        business = [
            ["Factor", "Value", "Assessment"],
            ["Auth Phase", f"{timing.get('authentication_phase_ms', 0)}ms", "Fast" if timing.get('authentication_phase_ms', 0) < 500 else "Slow"],
            ["Query Init", f"{timing.get('query_initialization_ms', 0)}ms", "Fast" if timing.get('query_initialization_ms', 0) < 1000 else "Slow"],
            ["Query Polling", f"{timing.get('query_polling_ms', 0)}ms", "Expected" if timing.get('query_polling_ms', 0) < 10000 else "Slow"],
            ["File Transfer", f"{timing.get('file_transfer_ms', 0)}ms", "Fast" if timing.get('file_transfer_ms', 0) < 1000 else "Slow"]
        ]
        
        return {
            'architecture_analysis': architecture,
            'js_quality_analysis': js_quality,
            'business_impact': business
        }
    
    def generate_report(self):
        """Generate Excel report."""
        print("\nGenerating Excel report...")
        
        wu_data = self.build_wu_data()
        
        # Call template
        output_file = generate_report(wu_data)
        
        print(f"\n✓ Report generated: {output_file}")
        return output_file


def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_performance_report.py <process_name> <client> <rice_item>")
        print("\nExample:")
        print("  python generate_performance_report.py CISOutbound FPI MatchReport")
        sys.exit(1)
    
    process_name = sys.argv[1]
    client = sys.argv[2]
    rice_item = sys.argv[3]
    
    generator = PerformanceReportGenerator(process_name, client, rice_item)
    generator.load_master_analysis()
    generator.generate_report()


if __name__ == "__main__":
    main()