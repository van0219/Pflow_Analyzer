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


def preprocess_client_handover(lpd_file, spec_file, output_dir="Temp"):
    """
    Phase 0: Preprocessing for client handover generation.
    
    Args:
        lpd_file: Path to LPD file
        spec_file: Path to ANA-050 specification document
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
    print("\n[2/3] Extracting LPD process structure...")
    lpd_structure_path = os.path.join(output_dir, "lpd_structure.json")
    lpd_data = extract_lpd_data([lpd_file])
    
    with open(lpd_structure_path, 'w', encoding='utf-8') as f:
        json.dump(lpd_data, f, indent=2, ensure_ascii=False)
    
    output_files['lpd_structure'] = lpd_structure_path
    print(f"   ✓ Written: {lpd_structure_path}")
    
    # Step 3: Calculate metrics summary
    print("\n[3/3] Calculating metrics summary...")
    metrics_summary_path = os.path.join(output_dir, "metrics_summary.json")
    metrics = calculate_metrics(lpd_data)
    
    with open(metrics_summary_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    output_files['metrics_summary'] = metrics_summary_path
    print(f"   ✓ Written: {metrics_summary_path}")
    
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
        print("Usage: python preprocess_client_handover.py <lpd_file> <spec_file> [output_dir]")
        sys.exit(1)
    
    lpd_file = sys.argv[1]
    spec_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "Temp"
    
    output_files = preprocess_client_handover(lpd_file, spec_file, output_dir)
    
    print("\nNext steps:")
    print("  Phase 1: Business Requirements Analysis")
    print(f"    Input: {output_files['spec_raw']}")
    print("  Phase 2: Workflow Architecture Analysis")
    print(f"    Input: {output_files['lpd_structure']}")
    print("  Phase 3: Configuration & Technical Components")
    print(f"    Input: {output_files['lpd_structure']}, {output_files['metrics_summary']}")
