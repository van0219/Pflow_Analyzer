#!/usr/bin/env python3
"""
IPA Domain Organizer
Splits extracted LPD data into domain-specific datasets for segmented AI analysis.
Solves context overload by allowing AI to analyze one domain at a time.

Domains:
1. Naming - Filenames, node captions, config sets
2. JavaScript - Code blocks, ES6 patterns, performance patterns
3. SQL - Queries, Compass SQL patterns
4. Error Handling - OnError tabs, GetWorkUnitErrors, stopOnError flags
5. Structure - Process metadata, activity counts, flow statistics

Usage:
    python organize_by_domain.py <lpd_data.json> <output_prefix>
    
Example:
    python organize_by_domain.py Temp/Process_lpd_data.json Temp/Process
    
    Outputs:
    - Temp/Process_domain_naming.json
    - Temp/Process_domain_javascript.json
    - Temp/Process_domain_sql.json
    - Temp/Process_domain_errorhandling.json
    - Temp/Process_domain_structure.json
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any


class DomainOrganizer:
    """Organizes IPA data into domain-specific datasets."""
    
    def __init__(self, lpd_data_path: str, output_prefix: str):
        self.lpd_data_path = lpd_data_path
        self.output_prefix = output_prefix
        self.lpd_data = None
        self.process = None
        
    def load_data(self) -> bool:
        """Load LPD data."""
        try:
            with open(self.lpd_data_path, 'r', encoding='utf-8', errors='replace') as f:
                self.lpd_data = json.load(f)
            self.process = self.lpd_data.get('processes', [{}])[0]
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def organize_naming_domain(self) -> Dict[str, Any]:
        """Organize naming-related data."""
        activities = self.process.get('activities', [])
        config_vars = self.process.get('config_variables', [])
        
        # Extract node captions
        node_captions = []
        for activity in activities:
            node_captions.append({
                'id': activity.get('id'),
                'caption': activity.get('caption'),
                'type': activity.get('type')
            })
        
        # Detect generic patterns
        generic_patterns = [
            r'^Assign\d*$',
            r'^Branch\d*$',
            r'^Wait\d*$',
            r'^MsgBuilder\d*$',
            r'^WebRun\d*$',
            r'^Timer\d*$'
        ]
        
        generic_nodes = []
        for node in node_captions:
            if node['type'] in ['START', 'END']:
                continue
            caption = node['caption']
            if any(re.match(pattern, caption) for pattern in generic_patterns):
                generic_nodes.append(node)
        
        # Extract config set names
        config_sets = {}
        for var in config_vars:
            config_set = var.get('config_set', '')
            if config_set not in config_sets:
                config_sets[config_set] = []
            config_sets[config_set].append(var.get('name'))
        
        # Detect generic config set names
        generic_config_names = ['Interface', 'Config', 'System', 'Settings']
        generic_config_sets = [
            name for name in config_sets.keys() 
            if name in generic_config_names
        ]
        
        # Detect hardcoded values in config
        hardcoded_values = []
        for var in config_vars:
            value = var.get('value', '')
            if value and not value.startswith('${'):
                # Check for suspicious patterns
                suspicious_indicators = [
                    'http://', 'https://', 'ftp://',
                    'c:\\', 'd:\\', '/home/', '/usr/',
                    'password', 'pwd', 'user=', 'username=',
                    'jdbc:', 'mongodb:', 'redis:',
                    '.com', '.net', '.org'
                ]
                if any(indicator in value.lower() for indicator in suspicious_indicators):
                    hardcoded_values.append({
                        'variable': var.get('name'),
                        'value': value[:50] + '...' if len(value) > 50 else value,
                        'config_set': var.get('config_set')
                    })
        
        # Determine process type from filename patterns
        filename = self.process.get('file', '') or self.process.get('name', '')
        process_type = 'Unknown'
        
        # Pattern matching for process type
        if any(keyword in filename.lower() for keyword in ['approval', 'workflow', 'wf_']):
            process_type = 'Approval Workflow'
        elif any(keyword in filename.lower() for keyword in ['interface', 'int_', 'inbound', 'outbound']):
            process_type = 'Interface Process'
        elif any(keyword in filename.lower() for keyword in ['trigger', 'scheduler', 'timer']):
            process_type = 'Scheduled Process'
        elif any(keyword in filename.lower() for keyword in ['report', 'rpt_']):
            process_type = 'Report Process'
        
        return {
            'filename': filename,
            'process_type': process_type,  # ADDED: Process type for correct naming recommendations
            'total_nodes': len(node_captions),
            'node_captions': node_captions,
            'generic_nodes': generic_nodes,
            'generic_node_count': len(generic_nodes),
            'generic_node_percentage': round(len(generic_nodes) / len(node_captions) * 100, 1) if node_captions else 0,
            'config_sets': config_sets,
            'generic_config_sets': generic_config_sets,
            'hardcoded_values': hardcoded_values,
            'hardcoded_values_count': len(hardcoded_values),
            'statistics': {
                'total_activities': len(activities),
                'nodes_with_generic_names': len(generic_nodes),
                'config_sets_count': len(config_sets),
                'generic_config_sets_count': len(generic_config_sets),
                'hardcoded_values_count': len(hardcoded_values)
            }
        }
    
    def organize_javascript_domain(self) -> Dict[str, Any]:
        """Organize JavaScript-related data."""
        js_blocks = self.process.get('javascript_blocks', [])
        activities = self.process.get('activities', [])
        
        # Find START node
        start_nodes = [a for a in activities if a.get('type') == 'START']
        start_node_id = start_nodes[0].get('id') if start_nodes else None
        
        # Check if START node has global variables
        # In IPA, Start node global variables are defined in PROPERTIES, not JavaScript code
        # Check both: properties (correct way) and JavaScript blocks (legacy check)
        has_global_vars_on_start = False
        start_node_global_vars = []
        if start_nodes:
            start_node = start_nodes[0]
            properties = start_node.get('properties', {})
            # Check if Start node has properties (excluding system properties)
            system_props = ['_activityCheckPoint', 'Checkpoint', 'variableType']
            user_props = [k for k in properties.keys() if k not in system_props]
            has_global_vars_on_start = len(user_props) > 0
            start_node_global_vars = user_props  # List of global variable names
            
            # Also check for JavaScript blocks (legacy approach)
            if not has_global_vars_on_start:
                start_node_js = [js for js in js_blocks if js.get('activity_id') == start_node_id]
                if start_node_js:
                    code = start_node_js[0].get('code', '')
                    has_global_vars_on_start = 'var ' in code or len(code.strip()) > 0
        
        # ES6 patterns to detect
        es6_patterns = {
            'let': r'\blet\s+\w+',
            'const': r'\bconst\s+\w+',
            'arrow_function': r'=>',
            'template_literal': r'`[^`]*\$\{',
            'spread_operator': r'\.\.\.',
            'class': r'\bclass\s+\w+',
            'destructuring': r'(?:const|let|var)\s*\{[^}]+\}\s*='
        }
        
        # Performance patterns to detect
        performance_patterns = {
            # Matches both new RegExp() and /pattern/g inside loops
            'regex_in_loop': r'for\s*\([^)]*\)\s*\{[^}]*(?:new\s+RegExp|/[^/\n]+/[gim]*)',
            # Matches string concatenation with += inside loops (any value, not just literals)
            'string_concat_in_loop': r'for\s*\([^)]*\)\s*\{[^}]*\w+\s*\+=',
            # Matches string concatenation with += outside loops (potential O(n²) if used repeatedly)
            'string_concat_repeated': r'\w+\s*\+=\s*(?:\w+|["\'])',
            # Matches regex compilation that could be pre-compiled
            'regex_not_precompiled': r'/[^/\n]+/[gim]*'
        }
        
        js_analysis = []
        for js in js_blocks:
            code = js.get('code', '')
            activity_id = js.get('activity_id')
            
            # Detect ES6 features
            es6_detected = {}
            for feature, pattern in es6_patterns.items():
                matches = re.findall(pattern, code)
                if matches:
                    es6_detected[feature] = {
                        'count': len(matches),
                        'examples': matches[:3]  # First 3 examples
                    }
            
            # Detect performance issues with context
            perf_detected = {}
            for issue, pattern in performance_patterns.items():
                matches = re.findall(pattern, code, re.DOTALL)
                if matches:
                    perf_detected[issue] = {
                        'count': len(matches),
                        'found': True
                    }
                    # Add specific examples for critical issues
                    if issue == 'regex_in_loop' and matches:
                        # Extract the actual regex pattern
                        regex_matches = re.findall(r'/([^/\n]+)/[gim]*', code)
                        if regex_matches:
                            perf_detected[issue]['examples'] = regex_matches[:2]  # First 2 patterns
                    elif issue == 'string_concat_repeated' and len(matches) > 3:
                        # Only flag if used more than 3 times (likely in a loop or repeated operation)
                        perf_detected[issue]['likely_performance_issue'] = True
                    elif issue == 'string_concat_in_loop':
                        # This is always a performance issue
                        perf_detected[issue]['severity'] = 'high'
            
            # Function declarations
            function_declarations = re.findall(r'function\s+(\w+)', code)
            
            # Check function declaration order
            lines = code.split('\n')
            function_lines = [i for i, line in enumerate(lines) if re.search(r'^\s*function\s+\w+', line)]
            code_lines = [i for i, line in enumerate(lines) 
                         if line.strip() 
                         and not line.strip().startswith('//') 
                         and not line.strip().startswith('/*')
                         and 'var' not in line 
                         and '=' in line]
            
            functions_declared_late = False
            if function_lines and code_lines:
                functions_declared_late = min(function_lines) > min(code_lines)
            
            # Variable declarations
            var_declarations = len(re.findall(r'\bvar\s+\w+', code))
            
            js_analysis.append({
                'activity_id': activity_id,
                'code_length': len(code),
                'line_count': code.count('\n') + 1,
                'es6_features_detected': es6_detected,
                'performance_patterns_detected': perf_detected,
                'function_declarations': function_declarations,
                'functions_declared_late': functions_declared_late,
                'var_declaration_count': var_declarations,
                'code_snippet': code[:200] + '...' if len(code) > 200 else code
            })
        
        return {
            'total_js_blocks': len(js_blocks),
            'start_node_has_global_vars': has_global_vars_on_start,
            'start_node_id': start_node_id,
            'start_node_global_vars': start_node_global_vars,  # List of global variable names
            'js_blocks': js_analysis,
            'statistics': {
                'blocks_with_es6': sum(1 for js in js_analysis if js['es6_features_detected']),
                'blocks_with_performance_issues': sum(1 for js in js_analysis if js['performance_patterns_detected']),
                'blocks_with_late_functions': sum(1 for js in js_analysis if js['functions_declared_late']),
                'total_functions': sum(len(js['function_declarations']) for js in js_analysis),
                'total_lines': sum(js['line_count'] for js in js_analysis)
            }
        }
    
    def organize_sql_domain(self) -> Dict[str, Any]:
        """Organize SQL-related data using pre-extracted queries."""
        # Use pre-extracted SQL queries from lpd_structure
        sql_queries_raw = self.process.get('sql_queries', [])
        activities = self.process.get('activities', [])
        
        # Check for Compass API pagination pattern
        # Compass API uses: POST /jobs/ (create) → GET /jobs/{id}/result?limit=X&offset=Y (retrieve)
        compass_api_activities = []
        for activity in activities:
            activity_type = activity.get('type')
            if activity_type in ['WEBRN', 'WEBRUN']:
                properties = activity.get('properties', {})
                program_name = properties.get('programName', '')
                call_string = properties.get('callString', '')
                
                # Check if this is a Compass API call
                is_compass_api = '/DATAFABRIC/compass/' in program_name or '/DATAFABRIC/compass/' in call_string
                
                if is_compass_api:
                    # Check if URL has limit/offset parameters
                    has_pagination_params = ('limit=' in program_name or 'limit=' in call_string) and \
                                          ('offset=' in program_name or 'offset=' in call_string)
                    
                    compass_api_activities.append({
                        'activity_id': activity.get('id'),
                        'activity_caption': activity.get('caption'),
                        'activity_type': activity_type,
                        'program_name': program_name,
                        'has_pagination': has_pagination_params,
                        'is_result_retrieval': '/result' in program_name or '/result' in call_string
                    })
        
        # Enrich with pattern detection
        sql_queries = []
        for query_data in sql_queries_raw:
            query_text = query_data.get('query', '')
            query_type = query_data.get('query_type', 'Unknown')
            
            # Detect Compass SQL patterns
            is_compass = 'compass' in query_text.lower() or 'DATAFABRIC' in query_text or 'FPI_FSM' in query_text
            
            # Detect potential issues
            has_select_star = 'SELECT *' in query_text.upper() or 'SELECT*' in query_text.upper()
            has_where = 'WHERE' in query_text.upper()
            has_limit = any(keyword in query_text.upper() for keyword in ['LIMIT', 'TOP', 'FETCH'])
            has_pagination = any(keyword in query_text.upper() for keyword in ['LIMIT', 'TOP', 'OFFSET', 'FETCH', 'PAGESIZE', 'MAXRECORDS'])
            
            sql_queries.append({
                'activity_id': query_data.get('activity_id'),
                'activity_type': query_data.get('activity_type'),
                'activity_caption': query_data.get('activity_caption'),
                'property_name': query_data.get('property_name'),
                'query_type': query_type,
                'query': query_text,
                'query_length': len(query_text),
                'line_count': query_data.get('line_count', 0),
                'is_compass_sql': is_compass,
                'patterns_detected': {
                    'select_star': has_select_star,
                    'has_where_clause': has_where,
                    'has_limit': has_limit,
                    'has_pagination': has_pagination
                }
            })
        
        return {
            'total_sql_queries': len(sql_queries),
            'sql_queries': sql_queries,
            'compass_api_activities': compass_api_activities,  # NEW: Compass API pagination info
            'statistics': {
                'compass_sql_count': sum(1 for q in sql_queries if q['is_compass_sql']),
                'compass_api_count': len(compass_api_activities),
                'compass_api_with_pagination': sum(1 for a in compass_api_activities if a['has_pagination']),
                'select_queries': sum(1 for q in sql_queries if q['query_type'] == 'SELECT'),
                'insert_queries': sum(1 for q in sql_queries if q['query_type'] == 'INSERT'),
                'update_queries': sum(1 for q in sql_queries if q['query_type'] == 'UPDATE'),
                'queries_with_select_star': sum(1 for q in sql_queries if q['patterns_detected']['select_star']),
                'queries_without_where': sum(1 for q in sql_queries if not q['patterns_detected']['has_where_clause'] and q['query_type'] in ['SELECT', 'UPDATE', 'DELETE']),
                'queries_without_limit': sum(1 for q in sql_queries if not q['patterns_detected']['has_limit'] and q['query_type'] == 'SELECT'),
                'queries_without_pagination': sum(1 for q in sql_queries if not q['patterns_detected']['has_pagination'] and q['query_type'] == 'SELECT')
            }
        }
    
    def organize_errorhandling_domain(self) -> Dict[str, Any]:
        """Organize error handling-related data."""
        activities = self.process.get('activities', [])
        
        # Get error handling analysis from extractor
        error_handling_data = self.process.get('error_handling_analysis', {})
        nodes_with_error_config = error_handling_data.get('nodes_with_error_config', [])
        
        # Create lookup for error handling status
        error_handling_lookup = {
            node['activity_id']: node.get('has_error_handling', False)
            for node in nodes_with_error_config
        }
        
        # Node types that should have error handling
        error_handling_types = ['WEBRN', 'WEBRUN', 'ACCFIL', 'Timer', 'SUBPROC', 'ITBEG']
        
        nodes_analysis = []
        for activity in activities:
            activity_id = activity.get('id')
            activity_type = activity.get('type')
            caption = activity.get('caption', '')
            
            # Check if node should have error handling
            should_have_error_handling = activity_type in error_handling_types
            
            if should_have_error_handling:
                # Get error handling status from extractor data
                has_error_handling = error_handling_lookup.get(activity_id, False)
                
                # Get stopOnError from extractor data
                stop_on_error = 'unknown'
                for node in nodes_with_error_config:
                    if node['activity_id'] == activity_id:
                        stop_on_error = node.get('stopOnError', 'true')
                        break
                
                nodes_analysis.append({
                    'activity_id': activity_id,
                    'activity_type': activity_type,
                    'caption': caption,
                    'stop_on_error': stop_on_error,
                    'has_error_handling': has_error_handling,
                    'missing_error_handling': not has_error_handling
                })
        
        # Check for GetWorkUnitErrors activity
        has_get_wu_errors = any(
            'GetWorkUnitErrors' in activity.get('caption', '')
            for activity in activities
        )
        
        return {
            'total_nodes_requiring_error_handling': len(nodes_analysis),
            'nodes_with_error_handling': sum(1 for n in nodes_analysis if n['has_error_handling']),
            'nodes_missing_error_handling': sum(1 for n in nodes_analysis if n['missing_error_handling']),
            'has_get_work_unit_errors': has_get_wu_errors,
            'nodes_analysis': nodes_analysis,
            'statistics': {
                'error_handling_coverage_percentage': round(
                    sum(1 for n in nodes_analysis if n['has_error_handling']) / len(nodes_analysis) * 100, 1
                ) if nodes_analysis else 100,
                'nodes_with_stop_on_error_true': sum(1 for n in nodes_analysis if n['stop_on_error'] == 'true'),
                'nodes_with_stop_on_error_false': sum(1 for n in nodes_analysis if n['stop_on_error'] == 'false')
            }
        }
    
    def organize_structure_domain(self) -> Dict[str, Any]:
        """Organize structure and metadata."""
        activities = self.process.get('activities', [])
        
        # Count by activity type
        activity_types = {}
        for activity in activities:
            activity_type = activity.get('type')
            activity_types[activity_type] = activity_types.get(activity_type, 0) + 1
        
        # Determine process type
        has_user_action = 'USRACT' in activity_types
        has_approval = any('approv' in str(a.get('caption', '')).lower() for a in activities)
        has_webservice = any(t in activity_types for t in ['WEBRN', 'WEBRUN'])
        has_file_access = 'ACCFIL' in activity_types
        
        process_name = self.process.get('name', '')
        if has_user_action or has_approval:
            process_type = 'Approval Workflow'
        elif 'inbound' in process_name.lower() or 'import' in process_name.lower():
            process_type = 'Inbound Interface'
        elif 'outbound' in process_name.lower() or 'export' in process_name.lower():
            process_type = 'Outbound Interface'
        elif has_webservice or has_file_access:
            process_type = 'Interface Process'
        else:
            process_type = 'IPA Process'
        
        # Auto-restart assessment
        auto_restart = self.process.get('auto_restart', 'Unknown')
        if 'Approval' in process_type or 'User' in process_type:
            auto_restart_appropriate = auto_restart == '0'
            auto_restart_reason = 'Should be 0 for approval workflows (requires user interaction)'
        elif 'Interface' in process_type:
            auto_restart_appropriate = auto_restart == '0'
            auto_restart_reason = 'Should be 0 for interfaces (prevents duplicate processing)'
        else:
            auto_restart_appropriate = None
            auto_restart_reason = f'Verify appropriateness for {process_type}'
        
        return {
            'process_name': process_name,
            'process_type': process_type,
            'auto_restart': auto_restart,
            'auto_restart_appropriate': auto_restart_appropriate,
            'auto_restart_reason': auto_restart_reason,
            'activity_types': activity_types,
            'total_activities': len(activities),
            'statistics': {
                'total_activities': len(activities),
                'unique_activity_types': len(activity_types),
                'has_user_interaction': has_user_action,
                'has_webservice_calls': has_webservice,
                'has_file_access': has_file_access
            }
        }
    
    def organize_all_domains(self):
        """Organize data into all domain files."""
        if not self.load_data():
            return False
        
        domains = {
            'naming': self.organize_naming_domain(),
            'javascript': self.organize_javascript_domain(),
            'sql': self.organize_sql_domain(),
            'errorhandling': self.organize_errorhandling_domain(),
            'structure': self.organize_structure_domain()
        }
        
        # Save each domain to separate file
        for domain_name, domain_data in domains.items():
            output_path = f"{self.output_prefix}_domain_{domain_name}.json"
            with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
                json.dump(domain_data, f, indent=2, ensure_ascii=False)
            print(f"✓ {domain_name.capitalize()} domain: {output_path}")
        
        print(f"\n✓ All domains organized successfully!")
        return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python organize_by_domain.py <lpd_data.json> <output_prefix>")
        print("\nExample:")
        print("  python organize_by_domain.py Temp/Process_lpd_data.json Temp/Process")
        sys.exit(1)
    
    lpd_data_path = sys.argv[1]
    output_prefix = sys.argv[2]
    
    print(f"Organizing: {lpd_data_path}")
    print(f"Output prefix: {output_prefix}\n")
    
    organizer = DomainOrganizer(lpd_data_path, output_prefix)
    
    if not organizer.organize_all_domains():
        sys.exit(1)


if __name__ == "__main__":
    main()
