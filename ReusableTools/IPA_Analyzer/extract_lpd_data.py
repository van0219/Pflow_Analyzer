#!/usr/bin/env python3
"""
LPD Data Extraction Tool

Purpose: Extract structured data from LPD files for Kiro to analyze
This tool does NOT analyze - it only extracts and organizes data

Output: JSON file with activities, JavaScript blocks, config variables
"""

import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
from urllib.parse import unquote


def extract_lpd_data(lpd_files: List[str], output_file: str = None) -> dict:
    """
    Extract structured data from LPD files
    
    Args:
        lpd_files: List of LPD file paths
        output_file: Optional output JSON file path
    
    Returns:
        Dictionary with extracted data
    """
    results = {
        'processes': [],
        'summary': {
            'total_processes': 0,
            'total_activities': 0,
            'total_javascript_blocks': 0
        }
    }
    
    for lpd_file in lpd_files:
        print(f"Extracting data from {Path(lpd_file).name}...")
        process_data = extract_single_lpd(lpd_file)
        results['processes'].append(process_data)
        
        # Update summary
        results['summary']['total_activities'] += len(process_data['activities'])
        results['summary']['total_javascript_blocks'] += len(process_data['javascript_blocks'])
    
    results['summary']['total_processes'] = len(results['processes'])
    results['summary']['total_sql_queries'] = sum(len(p.get('sql_queries', [])) for p in results['processes'])
    
    # Save to JSON if output file specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(results, f, indent=2)
        print(f"✓ Data saved to {output_file}")
    
    return results


def extract_single_lpd(lpd_file: str) -> dict:
    """Extract data from a single LPD file"""
    with open(lpd_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Parse XML
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        return {
            'file': Path(lpd_file).name,
            'error': f'XML parse error: {str(e)}',
            'activities': [],
            'javascript_blocks': [],
            'config_variables': [],
            'system_configuration_usage': {}
        }
    
    # Extract process metadata
    process_name = root.get('name', Path(lpd_file).stem)
    auto_restart = root.get('autoRestart', '0')
    
    # Extract activities
    activities = []
    javascript_blocks = []
    sql_queries = []
    config_variables = []
    
    for activity in root.findall('.//activity'):
        act_type = activity.get('activityType', '')
        act_id = activity.get('id', '')
        act_caption = activity.get('caption', '')
        
        # Skip ItEnd (auto-generated partners of LM nodes)
        if act_type == 'ItEnd':
            continue
        
        # Extract activity data
        act_data = {
            'id': act_id,
            'type': act_type,
            'caption': act_caption,
            'properties': {}
        }
        
        # For BRANCH nodes, extract branch conditions as a list
        if act_type == 'BRANCH':
            act_data['branch_conditions'] = []
            
            # Extract branch conditions (naam, btexe, expr appear in sequence)
            props = activity.findall('.//prop')
            i = 0
            while i < len(props):
                prop = props[i]
                prop_name = prop.get('name', '')
                
                # When we find 'naam', collect the next btexe and expr
                if prop_name == 'naam':
                    anydata = prop.find('anyData')
                    branch_name = anydata.text if anydata is not None and anydata.text else (prop.text or '')
                    
                    # Look ahead for btexe and expr
                    branch_to = ''
                    branch_expr = ''
                    
                    if i + 1 < len(props) and props[i + 1].get('name') == 'btexe':
                        anydata = props[i + 1].find('anyData')
                        branch_to = anydata.text if anydata is not None and anydata.text else (props[i + 1].text or '')
                    
                    if i + 2 < len(props) and props[i + 2].get('name') == 'expr':
                        anydata = props[i + 2].find('anyData')
                        branch_expr = anydata.text if anydata is not None and anydata.text else (props[i + 2].text or '')
                    
                    act_data['branch_conditions'].append({
                        'name': branch_name,
                        'branch_to': branch_to,
                        'expression': branch_expr
                    })
                    
                    # Skip the btexe and expr we just processed
                    i += 3
                    continue
                
                i += 1
        
        # Extract properties
        for prop in activity.findall('.//prop'):
            prop_name = prop.get('name', '')
            
            # Get property value from anyData CDATA or text
            anydata = prop.find('anyData')
            if anydata is not None and anydata.text:
                prop_value = anydata.text
            else:
                prop_value = prop.text or ''
            
            # ONLY extract JavaScript from ASSGN (Assign) nodes
            if act_type == 'ASSGN':
                # Detect JavaScript blocks in Assign nodes
                # 1. Properties named "expression" (standard)
                # 2. Properties named "ReplacingTheEmptyNameWithJavaScript*" (IPA Designer naming)
                # 3. Properties with URL-encoded content (contains %0D%0A, %2B, etc.)
                is_javascript = False
                
                if prop_name == 'expression' and prop_value.strip():
                    is_javascript = True
                elif 'javascript' in prop_name.lower() and prop_value.strip():
                    is_javascript = True
                elif prop_value and len(prop_value) > 20 and ('%0D%0A' in prop_value or '%2B' in prop_value or '%3D' in prop_value):
                    # URL-encoded content detected (likely JavaScript)
                    is_javascript = True
                
                if is_javascript and prop_value.strip():
                    # Decode URL-encoded JavaScript
                    decoded_code = unquote(prop_value)
                    
                    javascript_blocks.append({
                        'activity_id': act_id,
                        'activity_type': act_type,
                        'activity_caption': act_caption,
                        'property_name': prop_name,
                        'code': decoded_code,
                        'line_count': decoded_code.count('\n') + 1
                    })
                    continue  # Don't store in properties
            
            # Extract SQL from multiple node types
            # SQL can appear in: WEBRN/WEBRUN (API calls), ASSGN (variable construction), 
            # MSGBD (message formatting), ACCFIL (file content)
            if act_type in ['WEBRUN', 'WEBRN', 'ASSGN', 'MSGBD', 'ACCFIL']:
                # Check if property might contain SQL
                # Common property names: requestBody, callString, expression, fileContent, message, body
                is_sql_property = (
                    'request' in prop_name.lower() or 
                    'body' in prop_name.lower() or 
                    'query' in prop_name.lower() or 
                    'call' in prop_name.lower() or
                    'expression' in prop_name.lower() or
                    'content' in prop_name.lower() or
                    'message' in prop_name.lower() or
                    'sql' in prop_name.lower()
                )
                
                if is_sql_property and prop_value and len(prop_value) > 20:
                    decoded_value = unquote(prop_value) if '%' in prop_value else prop_value
                    
                    # Check if it looks like SQL (expanded keyword list)
                    sql_keywords = [
                        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE',
                        'CREATE', 'ALTER', 'DROP', 'TRUNCATE',  # DDL
                        'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',  # Joins
                        'GROUP BY', 'ORDER BY', 'HAVING',  # Clauses
                        'UNION', 'INTERSECT', 'EXCEPT'  # Set operations
                    ]
                    
                    if any(keyword in decoded_value.upper() for keyword in sql_keywords):
                        # For ASSGN nodes, check if it's JavaScript constructing SQL (not just using SQL keywords in comments)
                        if act_type == 'ASSGN':
                            # Look for SQL variable assignments or string concatenation patterns
                            # Examples: var sql = "SELECT...", query = "SELECT...", sql += "FROM..."
                            has_sql_pattern = (
                                'sql' in decoded_value.lower() or
                                'query' in decoded_value.lower() or
                                '"SELECT' in decoded_value or
                                "'SELECT" in decoded_value or
                                '= "' in decoded_value or
                                "= '" in decoded_value
                            )
                            
                            if not has_sql_pattern:
                                # Skip if it's just JavaScript code mentioning SQL keywords
                                continue
                        
                        sql_queries.append({
                            'activity_id': act_id,
                            'activity_type': act_type,
                            'activity_caption': act_caption,
                            'property_name': prop_name,
                            'query': decoded_value,
                            'line_count': decoded_value.count('\n') + 1
                        })
                        
                        # Only skip storing in properties for non-ASSGN nodes
                        # ASSGN nodes need their full JavaScript code preserved
                        if act_type != 'ASSGN':
                            continue
            
            # Store all other properties
            act_data['properties'][prop_name] = prop_value
        
        activities.append(act_data)
    
    # Extract START node variables (config variables)
    start_node = root.find('.//activity[@activityType="START"]')
    if start_node is not None:
        for prop in start_node.findall('.//prop[@name="expression"]'):
            code = prop.text or ''
            # Extract variable assignments
            var_pattern = r'(?:var|let|const)\s+(\w+)\s*=\s*([^;]+);'
            for match in re.finditer(var_pattern, code):
                var_name = match.group(1)
                var_value = match.group(2).strip()
                config_variables.append({
                    'name': var_name,
                    'value': var_value
                })
    
    # Analyze System Configuration usage across all JavaScript blocks
    config_usage = analyze_system_configuration(javascript_blocks)
    
    # Analyze error handling configuration
    error_handling = analyze_error_handling(activities, javascript_blocks)
    
    return {
        'file': Path(lpd_file).name,
        'process_name': process_name,
        'auto_restart': auto_restart,
        'activity_count': len(activities),
        'activities': activities,
        'javascript_blocks': javascript_blocks,
        'sql_queries': sql_queries,
        'config_variables': config_variables,
        'system_configuration_usage': config_usage,
        'error_handling_analysis': error_handling
    }


def analyze_system_configuration(javascript_blocks):
    """
    Analyze System Configuration usage to identify configuration set names
    
    Returns dict with:
    - config_references: List of all _configuration references found
    - config_sets: Unique configuration set names (needs verification)
    - generic_names: Config sets with potentially generic names
    """
    config_references = []
    config_sets = set()
    generic_names = []
    
    # Common generic terms that should be flagged for verification
    GENERIC_TERMS = {
        'interface', 'integration', 'config', 'configuration', 'settings',
        'system', 'general', 'common', 'shared', 'global', 'default',
        'process', 'workflow', 'data', 'file', 'api', 'service'
    }
    
    for block in javascript_blocks:
        code = block['code']
        
        # Find all _configuration references
        # Pattern: _configuration.<ConfigSetName>.<PropertyName>
        config_pattern = r'_configuration\.(\w+)\.(\w+)'
        matches = re.finditer(config_pattern, code)
        
        for match in matches:
            config_set = match.group(1)
            property_name = match.group(2)
            full_reference = f'_configuration.{config_set}.{property_name}'
            
            config_references.append({
                'activity_id': block['activity_id'],
                'config_set': config_set,
                'property_name': property_name,
                'full_reference': full_reference
            })
            
            config_sets.add(config_set)
            
            # Check if config set name is generic
            if config_set.lower() in GENERIC_TERMS:
                if config_set not in [g['config_set'] for g in generic_names]:
                    generic_names.append({
                        'config_set': config_set,
                        'reason': f'"{config_set}" is a generic term - should be vendor-specific per coding standard 1.4.1',
                        'recommendation': 'Verify this is the correct vendor-specific configuration set name'
                    })
    
    return {
        'config_references': config_references,
        'config_sets': sorted(list(config_sets)),
        'generic_names': generic_names,
        'total_references': len(config_references),
        'unique_sets': len(config_sets)
    }


def analyze_error_handling(activities, javascript_blocks):
    """
    Analyze error handling configuration across all activities
    
    Returns dict with:
    - nodes_with_error_config: Activities with stopOnError or overrideError
    - error_messages: Activities with ErrMsg assignments
    - nodes_without_error_handling: Activities that should have error handling but don't
    - summary: Overall error handling assessment
    """
    # Node types that support OnError tab (all except START, END, ASSGN, BRANCH)
    SUPPORTS_ONERROR = {'WEBRN', 'WEBRUN', 'ACCFIL', 'Timer', 'SUBPROC', 'MSGBD', 'ITBEG'}
    
    nodes_with_error_config = []
    nodes_without_error_handling = []
    error_messages = []
    
    # Analyze activities
    for activity in activities:
        act_type = activity['type']
        act_id = activity['id']
        props = activity.get('properties', {})
        
        # Check if node type supports OnError tab
        if act_type in SUPPORTS_ONERROR:
            stop_on_error = props.get('stopOnError', 'true')
            override_error = props.get('overrideError', 'false')
            
            # Node has error configuration
            if stop_on_error == 'false' or override_error == 'true':
                nodes_with_error_config.append({
                    'activity_id': act_id,
                    'activity_type': act_type,
                    'stopOnError': stop_on_error,
                    'overrideError': override_error,
                    'has_error_handling': True
                })
            else:
                # Node supports OnError but doesn't have it configured
                nodes_without_error_handling.append({
                    'activity_id': act_id,
                    'activity_type': act_type,
                    'stopOnError': stop_on_error,
                    'note': 'Supports OnError tab but stopOnError=true (will stop on error)'
                })
    
    # Find ErrMsg assignments in JavaScript
    for block in javascript_blocks:
        if block['property_name'] == 'ErrMsg':
            error_messages.append({
                'activity_id': block['activity_id'],
                'message': block['code'][:100]  # First 100 chars
            })
    
    # Summary
    total_supporting_onerror = len([a for a in activities if a['type'] in SUPPORTS_ONERROR])
    configured_count = len(nodes_with_error_config)
    unconfigured_count = len(nodes_without_error_handling)
    
    return {
        'nodes_with_error_config': nodes_with_error_config,
        'nodes_without_error_handling': nodes_without_error_handling,
        'error_messages': error_messages,
        'summary': {
            'total_nodes_supporting_onerror': total_supporting_onerror,
            'nodes_with_error_config': configured_count,
            'nodes_without_error_config': unconfigured_count,
            'error_message_count': len(error_messages),
            'coverage_percentage': round((configured_count / total_supporting_onerror * 100) if total_supporting_onerror > 0 else 0, 1)
        }
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_lpd_data.py <lpd_file1> [lpd_file2] ...")
        sys.exit(1)
    
    lpd_files = sys.argv[1:]
    output_file = 'Temp/lpd_data.json'
    
    result = extract_lpd_data(lpd_files, output_file)
    print(f"\nExtracted:")
    print(f"  - {result['summary']['total_processes']} processes")
    print(f"  - {result['summary']['total_activities']} activities")
    print(f"  - {result['summary']['total_javascript_blocks']} JavaScript blocks")
    print(f"  - {result['summary']['total_sql_queries']} SQL queries")
