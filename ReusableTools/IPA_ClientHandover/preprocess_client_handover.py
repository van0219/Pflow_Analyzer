#!/usr/bin/env python3
"""
Phase 0: Client Handover Preprocessing
Stateless pipeline architecture - Extract and structure data for AI analysis phases.

This script performs deterministic data extraction with NO AI reasoning:
- Extract ANA-050 content
- Extract LPD process structure
- Segment LPD by domain
- Pre-calculate metrics

Output: Structured JSON files for subsequent analysis phases
"""

import sys
import json
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from IPA_Analyzer.extract_lpd_data import extract_lpd_data
from IPA_Analyzer.extract_spec import extract_spec


def preprocess_client_handover(lpd_file, spec_file, wu_log_file=None, output_dir="Temp"):
    """
    Phase 0: Preprocessing for client handover generation.
    
    Args:
        lpd_file: Path to LPD file
        spec_file: Path to ANA-050 specification document
        wu_log_file: Path to work unit log file (optional)
        output_dir: Output directory for JSON files
    
    Returns:
        dict: Paths to generated JSON files
    """
    print("=" * 80)
    print("PHASE 0: CLIENT HANDOVER PREPROCESSING")
    print("=" * 80)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    output_files = {}
    
    # Step 1: Extract ANA-050 content
    print("\n[1/3] Extracting ANA-050 specification content...")
    spec_raw_path = os.path.join(output_dir, "spec_raw.json")
    spec_data = extract_spec(spec_file)
    
    with open(spec_raw_path, 'w', encoding='utf-8') as f:
        json.dump(spec_data, f, indent=2, ensure_ascii=False)
    
    output_files['spec_raw'] = spec_raw_path
    print(f"   ✓ Written: {spec_raw_path}")
    
    # Step 2: Extract LPD structure
    print("\n[2/4] Extracting LPD process structure...")
    lpd_structure_path = os.path.join(output_dir, "lpd_structure.json")
    lpd_data = extract_lpd_data([lpd_file])
    
    with open(lpd_structure_path, 'w', encoding='utf-8') as f:
        json.dump(lpd_data, f, indent=2, ensure_ascii=False)
    
    output_files['lpd_structure'] = lpd_structure_path
    print(f"   ✓ Written: {lpd_structure_path}")
    
    # Step 3: Calculate metrics summary
    print("\n[3/4] Calculating metrics summary...")
    metrics_summary_path = os.path.join(output_dir, "metrics_summary.json")
    metrics = calculate_metrics(lpd_data)
    
    with open(metrics_summary_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    output_files['metrics_summary'] = metrics_summary_path
    print(f"   ✓ Written: {metrics_summary_path}")
    
    # Step 4: Extract WU log (optional)
    if wu_log_file and os.path.exists(wu_log_file):
        print(f"\n[4/4] Extracting work unit log from {os.path.basename(wu_log_file)}...")
        try:
            from IPA_Analyzer.extract_wu_log import extract_wu_log
            wu_log_path = os.path.join(output_dir, "wu_log_data.json")
            wu_data = extract_wu_log(wu_log_file)
            
            with open(wu_log_path, 'w', encoding='utf-8') as f:
                json.dump(wu_data, f, indent=2, ensure_ascii=False)
            
            output_files['wu_log'] = wu_log_path
            print(f"   ✓ Written: {wu_log_path}")
        except Exception as e:
            print(f"   ⚠ Warning: Could not extract WU log: {e}")
    elif wu_log_file:
        print(f"\n[4/4] WU log file not found: {wu_log_file}")
        print("   ⚠ Skipping work unit log extraction")
    else:
        print("\n[4/4] No work unit log provided - skipping")
    
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
        'script_lengths': {},
        'es6_patterns_detected': [],
        'sql_statements': [],
        'external_integrations': [],
        'file_channels': [],
        'web_services': [],
        'data_fabric_usage': False,
        'idm_integration': False
    }
    
    for process in lpd_data.get('processes', []):
        activities = process.get('activities', [])
        metrics['total_activities'] += len(activities)
        
        for activity in activities:
            # Count activity types
            activity_type = activity.get('type', 'Unknown')
            metrics['activity_types'][activity_type] = metrics['activity_types'].get(activity_type, 0) + 1
            
            # Analyze scripts
            script = activity.get('script', '')
            if script:
                script_length = len(script)
                activity_id = activity.get('id', 'Unknown')
                metrics['script_lengths'][activity_id] = script_length
                
                # Detect ES6 patterns
                es6_patterns = detect_es6_patterns(script)
                if es6_patterns:
                    metrics['es6_patterns_detected'].append({
                        'activity': activity_id,
                        'patterns': es6_patterns
                    })
            
            # Detect SQL statements
            if 'SELECT' in script.upper() or 'INSERT' in script.upper() or 'UPDATE' in script.upper():
                metrics['sql_statements'].append({
                    'activity': activity.get('id', 'Unknown'),
                    'caption': activity.get('caption', 'Unknown')
                })
            
            # Detect external integrations
            if activity_type in ['WebServiceActivity', 'RestActivity']:
                metrics['external_integrations'].append({
                    'activity': activity.get('id', 'Unknown'),
                    'type': activity_type,
                    'caption': activity.get('caption', 'Unknown')
                })
                metrics['web_services'].append(activity.get('caption', 'Unknown'))
            
            # Detect file channels
            if 'FileChannel' in str(activity.get('properties', {})):
                metrics['file_channels'].append({
                    'activity': activity.get('id', 'Unknown'),
                    'caption': activity.get('caption', 'Unknown')
                })
            
            # Detect Data Fabric usage
            if 'DataFabric' in script or 'Compass' in script:
                metrics['data_fabric_usage'] = True
            
            # Detect IDM integration
            if 'IDM' in script or 'ContentDocument' in script:
                metrics['idm_integration'] = True
    
    return metrics


def detect_es6_patterns(script):
    """
    Detect ES6 patterns in JavaScript code.
    
    Args:
        script: JavaScript code string
    
    Returns:
        list: Detected ES6 patterns
    """
    patterns = []
    
    # Check for let/const
    if 'let ' in script or 'const ' in script:
        patterns.append('let/const declarations')
    
    # Check for arrow functions
    if '=>' in script:
        patterns.append('arrow functions')
    
    # Check for template literals
    if '`' in script:
        patterns.append('template literals')
    
    # Check for destructuring
    if 'const {' in script or 'let {' in script or 'const [' in script or 'let [' in script:
        patterns.append('destructuring')
    
    # Check for spread operator
    if '...' in script:
        patterns.append('spread operator')
    
    # Check for class syntax
    if 'class ' in script:
        patterns.append('class syntax')
    
    return patterns


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python preprocess_client_handover.py <lpd_file> <spec_file> [wu_log_file] [output_dir]")
        print("\nArguments:")
        print("  lpd_file      : Path to LPD file (required)")
        print("  spec_file     : Path to ANA-050 specification (required)")
        print("  wu_log_file   : Path to work unit log file (optional)")
        print("  output_dir    : Output directory for JSON files (optional, defaults to 'Temp')")
        print("\nExamples:")
        print("  python preprocess_client_handover.py process.lpd spec.docx")
        print("  python preprocess_client_handover.py process.lpd spec.docx wu_log.txt")
        print("  python preprocess_client_handover.py process.lpd spec.docx wu_log.txt Output")
        sys.exit(1)
    
    lpd_file = sys.argv[1]
    spec_file = sys.argv[2]
    
    # Parse optional arguments
    wu_log_file = None
    output_dir = "Temp"
    
    if len(sys.argv) > 3:
        # Check if third argument is a file (WU log) or directory (output_dir)
        third_arg = sys.argv[3]
        if os.path.isfile(third_arg) or third_arg.endswith('.txt') or third_arg.endswith('.log'):
            wu_log_file = third_arg
            if len(sys.argv) > 4:
                output_dir = sys.argv[4]
        else:
            # Third argument is output_dir
            output_dir = third_arg
    
    output_files = preprocess_client_handover(lpd_file, spec_file, wu_log_file, output_dir)
    
    print("\nNext steps:")
    print("  Phase 1: Business Requirements Analysis")
    print(f"    Input: {output_files['spec_raw']}")
    print("  Phase 2: Workflow Architecture Analysis")
    print(f"    Input: {output_files['lpd_structure']}")
    print("  Phase 3: Configuration & Technical Components")
    print(f"    Input: {output_files['lpd_structure']}, {output_files['metrics_summary']}")
    if 'wu_log' in output_files:
        print("  Phase 4: Production Validation")
        print(f"    Input: {output_files['wu_log']}")
