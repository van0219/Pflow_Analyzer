#!/usr/bin/env python3
"""
Phase 0: Coding Standards Preprocessing
Stateless pipeline architecture - Extract and structure data for AI analysis phases.

This script performs deterministic data extraction with NO AI reasoning:
- Extract LPD process structure
- Calculate metrics
- Load project standards (if available)
- Organize data by domain

Output: Structured JSON files for subsequent analysis phases
"""

import sys
import json
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from IPA_Analyzer.extract_lpd_data import extract_lpd_data
from IPA_CodingStandards.organize_by_domain import DomainOrganizer


def preprocess_coding_standards(lpd_file, client_name, output_dir="Temp"):
    """
    Phase 0: Preprocessing for coding standards analysis.
    
    Args:
        lpd_file: Path to LPD file
        client_name: Client name (for project standards lookup)
        output_dir: Output directory for JSON files
    
    Returns:
        dict: Paths to generated JSON files
    """
    print("=" * 80)
    print("PHASE 0: CODING STANDARDS PREPROCESSING")
    print("=" * 80)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean up old analysis files from previous runs (keep .gitkeep)
    print("\n[0/4] Cleaning up previous analysis files...")
    for file in Path(output_dir).glob("*"):
        if file.is_file() and file.name != ".gitkeep":
            try:
                file.unlink()
            except Exception as e:
                print(f"   Warning: Could not delete {file.name}: {e}")
    print("   ✓ Temp folder cleaned")
    
    output_files = {}
    
    # Step 1: Extract LPD structure
    print("\n[1/4] Extracting LPD process structure...")
    lpd_structure_path = os.path.join(output_dir, "lpd_structure.json")
    lpd_data = extract_lpd_data([lpd_file])
    
    with open(lpd_structure_path, 'w', encoding='utf-8') as f:
        json.dump(lpd_data, f, indent=2, ensure_ascii=False)
    
    output_files['lpd_structure'] = lpd_structure_path
    print(f"   ✓ Written: {lpd_structure_path}")
    
    # Step 2: Calculate metrics summary
    print("\n[2/4] Calculating metrics summary...")
    metrics_summary_path = os.path.join(output_dir, "metrics_summary.json")
    metrics = calculate_metrics(lpd_data)
    
    with open(metrics_summary_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    output_files['metrics_summary'] = metrics_summary_path
    print(f"   ✓ Written: {metrics_summary_path}")
    
    # Step 3: Load project standards (if available)
    print(f"\n[3/4] Loading project standards for {client_name}...")
    project_standards_path = os.path.join(output_dir, "project_standards.json")
    
    standards_file = f"Projects/{client_name}/project_standards_{client_name}.xlsx"
    if os.path.exists(standards_file):
        print(f"   Found: {standards_file}")
        try:
            # Use excel_reader to load standards
            from excel_reader import read_excel
            standards_df = read_excel(standards_file, sheet_name='Standards')
            
            # Convert to list of dicts
            standards = standards_df.to_dict('records')
            
            with open(project_standards_path, 'w', encoding='utf-8') as f:
                json.dump(standards, f, indent=2, ensure_ascii=False)
            
            output_files['project_standards'] = project_standards_path
            print(f"   ✓ Written: {project_standards_path} ({len(standards)} rules)")
        except Exception as e:
            print(f"   ⚠ Warning: Could not load project standards: {e}")
            # Create empty standards file
            with open(project_standards_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)
            output_files['project_standards'] = project_standards_path
            print(f"   ✓ Written: {project_standards_path} (empty - using steering defaults)")
    else:
        print(f"   No project standards file found at: {standards_file}")
        # Create empty standards file
        with open(project_standards_path, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)
        output_files['project_standards'] = project_standards_path
        print(f"   ✓ Written: {project_standards_path} (empty - using steering defaults)")
    
    # Step 4: Organize by domain
    print("\n[4/4] Organizing data by domain...")
    process_name = os.path.splitext(os.path.basename(lpd_file))[0]
    output_prefix = os.path.join(output_dir, process_name)
    
    organizer = DomainOrganizer(lpd_structure_path, output_prefix)
    if organizer.organize_all_domains():
        output_files['domain_naming'] = f"{output_prefix}_domain_naming.json"
        output_files['domain_javascript'] = f"{output_prefix}_domain_javascript.json"
        output_files['domain_sql'] = f"{output_prefix}_domain_sql.json"
        output_files['domain_errorhandling'] = f"{output_prefix}_domain_errorhandling.json"
        output_files['domain_structure'] = f"{output_prefix}_domain_structure.json"
    else:
        print("   ⚠ Warning: Domain organization failed")
    
    print("\n" + "=" * 80)
    print("PHASE 0 COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")
    for key, path in output_files.items():
        print(f"  - {key}: {path}")
    
    return output_files


def calculate_metrics(lpd_data):
    """
    Calculate pre-computed metrics from LPD data.
    
    Args:
        lpd_data: Extracted LPD data structure
    
    Returns:
        dict: Metrics summary
    """
    metrics = {
        'process_count': len(lpd_data.get('processes', [])),
        'total_activities': 0,
        'activity_types': {},
        'javascript_block_count': 0,
        'sql_query_count': 0,
        'error_prone_activity_count': 0,
        'es6_patterns_detected': [],
        'generic_names_detected': [],
        'sql_types_detected': []
    }
    
    for process in lpd_data.get('processes', []):
        activities = process.get('activities', [])
        metrics['total_activities'] += len(activities)
        
        # Count JavaScript blocks
        js_blocks = process.get('javascript_blocks', [])
        metrics['javascript_block_count'] += len(js_blocks)
        
        # Detect ES6 patterns
        for js in js_blocks:
            code = js.get('code', '')
            if 'let ' in code or 'const ' in code:
                metrics['es6_patterns_detected'].append('let/const')
            if '=>' in code:
                metrics['es6_patterns_detected'].append('arrow_function')
            if '`' in code:
                metrics['es6_patterns_detected'].append('template_literal')
        
        # Count activity types
        for activity in activities:
            activity_type = activity.get('type', 'Unknown')
            metrics['activity_types'][activity_type] = metrics['activity_types'].get(activity_type, 0) + 1
            
            # Count error-prone activities
            if activity_type in ['WEBRN', 'WEBRUN', 'ACCFIL', 'Timer', 'SUBPROC', 'ITBEG']:
                metrics['error_prone_activity_count'] += 1
            
            # Detect generic names
            caption = activity.get('caption', '')
            if any(pattern in caption for pattern in ['Assign 1', 'Branch 1', 'WebRun 1', 'Wait 1']):
                metrics['generic_names_detected'].append(caption)
            
            # Detect SQL queries
            properties = activity.get('properties', {})
            for field in ['requestBody', 'callString', 'expression', 'query', 'sql']:
                value = properties.get(field, '')
                if value and any(keyword in value.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                    metrics['sql_query_count'] += 1
                    # Detect SQL type
                    for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']:
                        if keyword in value.upper():
                            metrics['sql_types_detected'].append(keyword)
                            break
                    break
    
    # Deduplicate lists
    metrics['es6_patterns_detected'] = list(set(metrics['es6_patterns_detected']))
    metrics['sql_types_detected'] = list(set(metrics['sql_types_detected']))
    
    return metrics


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python preprocess_coding_standards.py <lpd_file> <client_name> [output_dir]")
        print("\nArguments:")
        print("  lpd_file      : Path to LPD file (required)")
        print("  client_name   : Client name for project standards lookup (required)")
        print("  output_dir    : Output directory for JSON files (optional, defaults to 'Temp')")
        print("\nExamples:")
        print("  python preprocess_coding_standards.py process.lpd BayCare")
        print("  python preprocess_coding_standards.py process.lpd FPI Temp")
        sys.exit(1)
    
    lpd_file = sys.argv[1]
    client_name = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "Temp"
    
    output_files = preprocess_coding_standards(lpd_file, client_name, output_dir)
    
    print("\nNext steps:")
    print("  Phase 1: Naming Analysis")
    print(f"    Input: {output_files.get('domain_naming', 'N/A')}, {output_files['project_standards']}")
    print("  Phase 2: JavaScript Analysis")
    print(f"    Input: {output_files.get('domain_javascript', 'N/A')}, {output_files['project_standards']}")
    print("  Phase 3: SQL Analysis")
    print(f"    Input: {output_files.get('domain_sql', 'N/A')}, {output_files['project_standards']}")
    print("  Phase 4: Error Handling Analysis")
    print(f"    Input: {output_files.get('domain_errorhandling', 'N/A')}, {output_files['project_standards']}")
    print("  Phase 5: Structure Analysis")
    print(f"    Input: {output_files.get('domain_structure', 'N/A')}, {output_files['metrics_summary']}, {output_files['project_standards']}")
