#!/usr/bin/env python3
"""
IPA Coding Standards Analyzer
Programmatically analyzes extracted LPD data against coding standards rules.
Outputs structured analysis JSON for AI review.

Usage:
    python analyze_coding_standards.py <lpd_data.json> <project_standards.xlsx> [output.json]
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from ReusableTools.excel_reader import read_excel
    import pandas as pd
except ImportError as e:
    print(f"Error: Required libraries not found. Install: pip install pandas openpyxl")
    sys.exit(1)


class IPACodingStandardsAnalyzer:
    """Analyzes IPA processes against coding standards."""
    
    def __init__(self, lpd_data_path: str, project_standards_path: str = None):
        """Initialize analyzer with data paths."""
        self.lpd_data_path = lpd_data_path
        self.project_standards_path = project_standards_path
        self.lpd_data = None
        self.project_standards = None
        self.analysis = {
            'metadata': {},
            'overview': {},
            'naming_violations': [],
            'ipa_rule_violations': [],
            'error_handling_issues': [],
            'config_issues': [],
            'performance_issues': [],
            'javascript_issues': [],
            'sql_queries': [],
            'generic_nodes': [],
            'statistics': {}
        }
    
    def load_data(self) -> bool:
        """Load LPD data and project standards."""
        try:
            # Load LPD data
            with open(self.lpd_data_path, 'r', encoding='utf-8', errors='replace') as f:
                self.lpd_data = json.load(f)
            
            # Load project standards if provided
            if self.project_standards_path and Path(self.project_standards_path).exists():
                df = read_excel(self.project_standards_path, sheet_name='Standards')
                self.project_standards = df.to_dict('records')
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze(self) -> Dict[str, Any]:
        """Run all analysis checks."""
        if not self.lpd_data:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Extract metadata
        self._extract_metadata()
        
        # Run analysis checks
        self._analyze_naming_convention()
        self._analyze_ipa_rules()
        self._analyze_error_handling()
        self._analyze_configuration()
        self._analyze_performance()
        self._analyze_javascript()
        self._extract_sql_queries()
        self._identify_generic_nodes()
        
        # Calculate statistics
        self._calculate_statistics()
        
        return self.analysis
    
    def _extract_metadata(self):
        """Extract process metadata."""
        process = self.lpd_data.get('processes', [{}])[0]
        
        self.analysis['metadata'] = {
            'process_name': process.get('name', 'Unknown'),
            'file_path': process.get('file_path', ''),
            'auto_restart': process.get('auto_restart', 'Unknown'),
            'activity_count': len(process.get('activities', [])),
            'javascript_count': len(process.get('javascript_blocks', [])),
            'sql_count': 0  # Will be calculated
        }
        
        self.analysis['overview'] = {
            'process_name': process.get('name', 'Unknown').replace('.lpd', ''),
            'process_type': self._determine_process_type(process),
            'activity_count': len(process.get('activities', [])),
            'total_activities': len(process.get('activities', [])),
            'javascript_blocks': len(process.get('javascript_blocks', [])),
            'sql_queries': 0,  # Will be updated
            'auto_restart': process.get('auto_restart', 'Unknown'),
            'auto_restart_assessment': self._assess_auto_restart(process),
            'description': process.get('description', ''),
            'process_count': 1
        }
    
    def _determine_process_type(self, process: Dict) -> str:
        """Determine process type from activities and structure."""
        activities = process.get('activities', [])
        name = process.get('name', '').lower()
        
        # Check for approval workflow indicators
        has_user_action = any(a.get('type') == 'USRACT' for a in activities)
        has_approval = 'approv' in name or any('approv' in str(a.get('caption', '')).lower() for a in activities)
        
        if has_user_action or has_approval:
            return 'Approval Workflow'
        
        # Check for interface indicators
        has_webservice = any(a.get('type') in ['WEBRN', 'WEBRUN'] for a in activities)
        has_file_access = any(a.get('type') == 'ACCFIL' for a in activities)
        
        if 'inbound' in name or 'import' in name:
            return 'Inbound Interface'
        elif 'outbound' in name or 'export' in name:
            return 'Outbound Interface'
        elif has_webservice or has_file_access:
            return 'Interface Process'
        
        # Check for conversion indicators
        if 'conversion' in name or 'migrate' in name:
            return 'Data Conversion'
        
        # Check for enhancement indicators
        if 'enhance' in name or 'custom' in name:
            return 'Enhancement'
        
        return 'IPA Process'
    
    def _assess_auto_restart(self, process: Dict) -> str:
        """Assess if auto_restart setting is appropriate."""
        auto_restart = process.get('auto_restart', 'Unknown')
        process_type = self._determine_process_type(process)
        
        if 'Approval' in process_type or 'User' in process_type:
            if auto_restart == '0':
                return 'Correctly set to 0 for approval workflow (requires user interaction)'
            else:
                return 'Should be 0 for approval workflows (requires user interaction)'
        elif 'Interface' in process_type:
            if auto_restart == '0':
                return 'Correctly set to 0 for interface (prevents duplicate processing)'
            else:
                return 'Should be 0 for interfaces (prevents duplicate processing)'
        else:
            return f'Set to {auto_restart} - verify appropriateness for {process_type}'
    
    def _analyze_naming_convention(self):
        """Check filename naming convention."""
        process = self.lpd_data.get('processes', [{}])[0]
        filename = process.get('name', '')
        
        # Expected format: <ProjectPrefix>_<INT>_<Source>_<Destination>_<ShortDescription>.lpd
        # Example: FPI_INT_MatchReport_SFTP_Outbound.lpd
        
        parts = filename.replace('.lpd', '').split('_')
        
        issues = []
        if len(parts) < 4:
            issues.append('Filename has fewer than 4 parts (expected: Prefix_INT_Source_Destination_Description)')
        
        if len(parts) >= 2 and parts[1] != 'INT':
            issues.append(f'Second part should be "INT" but found "{parts[1]}"')
        
        if issues:
            self.analysis['naming_violations'].append({
                'file': filename,
                'rule': 'Filename format (1.1.1)',
                'severity': 'High',
                'issues': issues,
                'current': filename,
                'recommendation': 'Follow format: <ProjectPrefix>_INT_<Source>_<Destination>_<Description>.lpd'
            })
    
    def _analyze_ipa_rules(self):
        """Check IPA-specific rules."""
        process = self.lpd_data.get('processes', [{}])[0]
        activities = process.get('activities', [])
        js_blocks = process.get('javascript_blocks', [])
        
        # Rule 1.2.1: Global variables on Start node
        start_nodes = [a for a in activities if a.get('type') == 'START']
        if start_nodes:
            start_node = start_nodes[0]
            start_js = [js for js in js_blocks if js.get('activity_id') == start_node.get('id')]
            
            # Check if global variables are declared on Start
            has_global_vars = any('var ' in js.get('code', '') for js in start_js)
            
            if not has_global_vars and len(js_blocks) > 0:
                self.analysis['ipa_rule_violations'].append({
                    'rule': 'Global variables on Start node (1.2.1)',
                    'severity': 'Medium',
                    'finding': 'No global variable declarations found on Start node',
                    'recommendation': 'Declare all global variables on Start node for clarity'
                })
        
        # Rule 1.2.3: Functions declared early
        for js in js_blocks:
            code = js.get('code', '')
            lines = code.split('\n')
            
            function_lines = []
            other_code_lines = []
            
            for i, line in enumerate(lines):
                if re.search(r'^\s*function\s+\w+', line):
                    function_lines.append(i)
                elif line.strip() and not line.strip().startswith('//') and not line.strip().startswith('/*'):
                    if 'var' not in line and '=' in line:
                        other_code_lines.append(i)
            
            # Check if functions come after other code
            if function_lines and other_code_lines:
                if min(function_lines) > min(other_code_lines):
                    self.analysis['ipa_rule_violations'].append({
                        'activity': js.get('activity_id'),
                        'rule': 'Functions declared early (1.2.3)',
                        'severity': 'Low',
                        'finding': 'Function declarations found after executable code',
                        'recommendation': 'Move function declarations to top of script'
                    })
    
    def _analyze_error_handling(self):
        """Check error handling implementation."""
        process = self.lpd_data.get('processes', [{}])[0]
        activities = process.get('activities', [])
        
        # Node types that should have error handling
        error_handling_types = ['WEBRN', 'WEBRUN', 'ACCFIL', 'Timer', 'SUBPROC', 'ITBEG']
        
        nodes_needing_error_handling = [a for a in activities if a.get('type') in error_handling_types]
        nodes_with_error_handling = [a for a in nodes_needing_error_handling if a.get('stopOnError') == 'false']
        
        missing_error_handling = len(nodes_needing_error_handling) - len(nodes_with_error_handling)
        
        if missing_error_handling > 0:
            missing_nodes = [a.get('id') for a in nodes_needing_error_handling if a.get('stopOnError') != 'false']
            self.analysis['error_handling_issues'].append({
                'rule': 'On Error tab implementation (1.3.1)',
                'severity': 'High',
                'count': missing_error_handling,
                'nodes': missing_nodes[:10],  # Limit to first 10
                'recommendation': 'Add On Error tab with stopOnError=false for graceful error handling'
            })
        
        # Check for GetWorkUnitErrors activity
        has_get_wu_errors = any('GetWorkUnitErrors' in a.get('caption', '') for a in activities)
        
        if not has_get_wu_errors:
            self.analysis['error_handling_issues'].append({
                'rule': 'GetWorkUnitErrors activity node (1.3.2)',
                'severity': 'Medium',
                'finding': 'No GetWorkUnitErrors activity found',
                'recommendation': 'Add GetWorkUnitErrors activity node to capture and log all errors'
            })
    
    def _analyze_configuration(self):
        """Check system configuration."""
        process = self.lpd_data.get('processes', [{}])[0]
        config_vars = process.get('config_variables', [])
        
        # Check for generic configuration set names
        generic_names = ['Interface', 'Config', 'System', 'Settings']
        
        for config in config_vars:
            config_set = config.get('config_set', '')
            if config_set in generic_names:
                self.analysis['config_issues'].append({
                    'config_set': config_set,
                    'rule': 'Config set naming (1.4.1)',
                    'severity': 'Medium',
                    'finding': f'Generic configuration set name: {config_set}',
                    'recommendation': 'Use vendor-specific configuration set names (e.g., VendorName_Interface)'
                })
            
            # Check for hardcoded values
            value = config.get('value', '')
            if value and not value.startswith('${'):
                # Check if it looks like a hardcoded path, URL, or credential
                if any(indicator in value.lower() for indicator in ['http://', 'https://', 'c:\\', '/home/', 'password', 'user=']):
                    self.analysis['config_issues'].append({
                        'variable': config.get('name', ''),
                        'rule': 'No hardcoded values (1.4.3)',
                        'severity': 'High',
                        'finding': f'Hardcoded value detected: {value[:50]}...',
                        'recommendation': 'Move to configuration set variable'
                    })
    
    def _analyze_performance(self):
        """Check performance best practices."""
        process = self.lpd_data.get('processes', [{}])[0]
        activities = process.get('activities', [])
        js_blocks = process.get('javascript_blocks', [])
        
        # Check for pagination in large dataset queries
        webrn_activities = [a for a in activities if a.get('type') in ['WEBRN', 'WEBRUN']]
        
        for activity in webrn_activities:
            # Check if it's a query activity
            caption = activity.get('caption', '').lower()
            if 'query' in caption or 'get' in caption or 'fetch' in caption:
                # Look for pagination indicators
                has_pagination = any(
                    keyword in str(activity.get('properties', {})).lower()
                    for keyword in ['limit', 'top', 'pagesize', 'maxrecords', 'offset', 'skip']
                )
                
                if not has_pagination:
                    self.analysis['performance_issues'].append({
                        'activity': activity.get('id'),
                        'rule': 'Pagination for large datasets (1.5.2)',
                        'severity': 'High',
                        'finding': 'Query activity without pagination',
                        'recommendation': 'Implement pagination for queries returning >1000 records'
                    })
        
        # Check JavaScript performance issues
        for js in js_blocks:
            code = js.get('code', '')
            activity_id = js.get('activity_id')
            
            # Check for regex in loops
            if re.search(r'for\s*\(.*\)\s*\{[^}]*new\s+RegExp', code, re.DOTALL):
                self.analysis['performance_issues'].append({
                    'activity': activity_id,
                    'rule': 'Performance optimization',
                    'severity': 'High',
                    'finding': 'RegExp compiled inside loop',
                    'recommendation': 'Pre-compile regex outside loop'
                })
            
            # Check for string concatenation in loops
            if re.search(r'for\s*\(.*\)\s*\{[^}]*\w+\s*\+=\s*["\']', code, re.DOTALL):
                self.analysis['performance_issues'].append({
                    'activity': activity_id,
                    'rule': 'Performance optimization',
                    'severity': 'Medium',
                    'finding': 'String concatenation in loop (O(n²) complexity)',
                    'recommendation': 'Use array accumulation with join()'
                })
    
    def _analyze_javascript(self):
        """Analyze JavaScript code for ES5 compliance and quality."""
        process = self.lpd_data.get('processes', [{}])[0]
        js_blocks = process.get('javascript_blocks', [])
        
        es6_patterns = {
            'let': r'\blet\s+\w+',
            'const': r'\bconst\s+\w+',
            'arrow_function': r'=>',
            'template_literal': r'`[^`]*\$\{',
            'spread_operator': r'\.\.\.',
            'class': r'\bclass\s+\w+',
            'destructuring': r'(?:const|let|var)\s*\{[^}]+\}\s*='
        }
        
        for js in js_blocks:
            code = js.get('code', '')
            activity_id = js.get('activity_id')
            
            for feature, pattern in es6_patterns.items():
                if re.search(pattern, code):
                    self.analysis['javascript_issues'].append([
                        process.get('name', ''),
                        activity_id,
                        'N/A',  # Line number
                        f'ES6 {feature}',
                        'High',
                        'Use ES5 equivalent',
                        code[:100] + '...' if len(code) > 100 else code,
                        'No',
                        self._get_es5_fix(feature)
                    ])
    
    def _get_es5_fix(self, feature: str) -> str:
        """Get ES5 fix recommendation for ES6 feature."""
        fixes = {
            'let': 'Use var instead',
            'const': 'Use var instead',
            'arrow_function': 'Use function() {} instead',
            'template_literal': 'Use string concatenation with + instead',
            'spread_operator': 'Use Array.prototype.concat() or manual iteration',
            'class': 'Use function constructor with prototype',
            'destructuring': 'Use explicit variable assignment'
        }
        return fixes.get(feature, 'Convert to ES5 syntax')
    
    def _extract_sql_queries(self):
        """Extract all SQL queries from activities."""
        process = self.lpd_data.get('processes', [{}])[0]
        activities = process.get('activities', [])
        
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
        
        for activity in activities:
            activity_id = activity.get('id')
            activity_type = activity.get('type')
            properties = activity.get('properties', {})
            
            # Check various property fields for SQL
            sql_fields = ['requestBody', 'callString', 'expression', 'query', 'sql']
            
            for field in sql_fields:
                value = properties.get(field, '')
                if value and any(keyword in value.upper() for keyword in sql_keywords):
                    self.analysis['sql_queries'].append({
                        'activity': activity_id,
                        'type': activity_type,
                        'query': value,
                        'assessment': 'Requires review',
                        'recommendations': []
                    })
        
        # Update count
        self.analysis['overview']['sql_queries'] = len(self.analysis['sql_queries'])
        self.analysis['metadata']['sql_count'] = len(self.analysis['sql_queries'])
    
    def _identify_generic_nodes(self):
        """Identify nodes with generic names."""
        process = self.lpd_data.get('processes', [{}])[0]
        activities = process.get('activities', [])
        
        generic_patterns = [
            r'^Assign\d*$',
            r'^Branch\d*$',
            r'^Wait\d*$',
            r'^MsgBuilder\d*$',
            r'^WebRun\d*$',
            r'^Timer\d*$'
        ]
        
        for activity in activities:
            caption = activity.get('caption', '')
            activity_id = activity.get('id')
            activity_type = activity.get('type')
            
            # Skip START and END nodes
            if activity_type in ['START', 'END']:
                continue
            
            # Check if caption matches generic pattern
            is_generic = any(re.match(pattern, caption) for pattern in generic_patterns)
            
            if is_generic:
                self.analysis['generic_nodes'].append({
                    'id': activity_id,
                    'caption': caption,
                    'type': activity_type,
                    'recommendation': self._suggest_node_name(activity, activities)
                })
    
    def _suggest_node_name(self, activity: Dict, all_activities: List[Dict]) -> str:
        """Suggest a descriptive name for a node based on context."""
        activity_type = activity.get('type')
        properties = activity.get('properties', {})
        
        # Type-specific suggestions
        if activity_type == 'ASSGN':
            return 'Describe what is being assigned (e.g., BuildRequestPayload, SetApprovalStatus)'
        elif activity_type == 'BRANCH':
            return 'Describe the condition (e.g., CheckInvoiceAmount, ValidateVendor)'
        elif activity_type == 'WEBRN' or activity_type == 'WEBRUN':
            return 'Describe the API call (e.g., QueryInvoices, UpdateApprovalStatus)'
        elif activity_type == 'MSGBD':
            return 'Describe the message purpose (e.g., BuildErrorEmail, FormatApprovalNotification)'
        else:
            return f'Use descriptive name for {activity_type} activity'
    
    def _calculate_statistics(self):
        """Calculate summary statistics."""
        self.analysis['statistics'] = {
            'total_violations': (
                len(self.analysis['naming_violations']) +
                len(self.analysis['ipa_rule_violations']) +
                len(self.analysis['error_handling_issues']) +
                len(self.analysis['config_issues']) +
                len(self.analysis['performance_issues'])
            ),
            'javascript_issues_count': len(self.analysis['javascript_issues']),
            'generic_nodes_count': len(self.analysis['generic_nodes']),
            'sql_queries_count': len(self.analysis['sql_queries']),
            'high_severity_count': sum(
                1 for item in (
                    self.analysis['naming_violations'] +
                    self.analysis['ipa_rule_violations'] +
                    self.analysis['error_handling_issues'] +
                    self.analysis['config_issues'] +
                    self.analysis['performance_issues']
                ) if item.get('severity') == 'High'
            )
        }
    
    def save_analysis(self, output_path: str):
        """Save analysis to JSON file."""
        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(self.analysis, f, indent=2, ensure_ascii=False)
        print(f"Analysis saved to: {output_path}")


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python analyze_coding_standards.py <lpd_data.json> <project_standards.xlsx> [output.json]")
        sys.exit(1)
    
    lpd_data_path = sys.argv[1]
    project_standards_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else lpd_data_path.replace('.json', '_analysis.json')
    
    print(f"Analyzing: {lpd_data_path}")
    print(f"Project standards: {project_standards_path}")
    
    analyzer = IPACodingStandardsAnalyzer(lpd_data_path, project_standards_path)
    
    if not analyzer.load_data():
        sys.exit(1)
    
    print("Running analysis...")
    analysis = analyzer.analyze()
    
    print(f"\nAnalysis Summary:")
    print(f"  Total violations: {analysis['statistics']['total_violations']}")
    print(f"  High severity: {analysis['statistics']['high_severity_count']}")
    print(f"  JavaScript issues: {analysis['statistics']['javascript_issues_count']}")
    print(f"  Generic nodes: {analysis['statistics']['generic_nodes_count']}")
    print(f"  SQL queries: {analysis['statistics']['sql_queries_count']}")
    
    analyzer.save_analysis(output_path)
    print(f"\n✓ Analysis complete!")


if __name__ == "__main__":
    main()
