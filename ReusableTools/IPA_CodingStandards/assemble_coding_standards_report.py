#!/usr/bin/env python3
"""
IPA Coding Standards - Report Assembly
Merges all domain analysis JSONs and generates Excel report.

Usage:
    python assemble_coding_standards_report.py <client> <rice_item> <process_name>
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def load_json(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    if len(sys.argv) < 4:
        print("Usage: python assemble_coding_standards_report.py <client> <rice_item> <process_name>")
        sys.exit(1)
    
    client = sys.argv[1]
    rice_item = sys.argv[2]
    process_name = sys.argv[3]
    
    print("=" * 80)
    print("PHASE 6: REPORT ASSEMBLY")
    print("=" * 80)
    print()
    
    temp_dir = Path('Temp')
    
    # Load all analysis JSONs
    print("[1/4] Loading analysis results...")
    analyses = {}
    required_domains = ['naming', 'javascript', 'sql', 'errorhandling', 'structure']
    
    for domain in required_domains:
        analysis_file = temp_dir / f"{domain}_analysis.json"
        if not analysis_file.exists():
            print(f"   ❌ Missing: {domain}_analysis.json")
            print(f"   Run Phase {required_domains.index(domain) + 1} first")
            sys.exit(1)
        
        analyses[domain] = load_json(analysis_file)
        violation_count = len(analyses[domain].get('violations', []))
        print(f"   ✓ {domain}: {violation_count} violations")
    
    # Load metadata
    lpd_structure = load_json(temp_dir / 'lpd_structure.json')
    metrics_summary = load_json(temp_dir / 'metrics_summary.json')
    project_standards = load_json(temp_dir / 'project_standards.json')
    
    print()
    print("[2/4] Merging violations...")
    
    # Merge all violations
    all_violations = []
    for domain, analysis in analyses.items():
        violations = analysis.get('violations', [])
        for v in violations:
            v['domain'] = domain
            # Convert activities list to comma-separated string for template compatibility
            if isinstance(v.get('activities'), list):
                v['activities'] = ', '.join(v['activities'])
            all_violations.append(v)
    
    print(f"   ✓ Total violations: {len(all_violations)}")
    
    # Save merged violations
    merged_file = temp_dir / f"{process_name}_violations.json"
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(all_violations, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved: {merged_file.name}")
    
    print()
    print("[3/4] Building ipa_data structure...")
    
    # Import and use build_ipa_data_helper
    sys.path.insert(0, str(Path(__file__).parent))
    from build_ipa_data_helper import build_ipa_data_from_violations
    
    # Extract data from lpd_structure and metrics
    activities = lpd_structure.get('processes', [{}])[0].get('activities', [])
    activity_count = metrics_summary.get('total_activities', 0)
    process_type = lpd_structure.get('processes', [{}])[0].get('type', 'Interface Process')
    auto_restart = lpd_structure.get('processes', [{}])[0].get('autoRestart', '0')
    
    # Extract SQL queries from lpd_structure
    sql_queries_array = lpd_structure.get('processes', [{}])[0].get('sql_queries', [])
    
    # Calculate quality scores
    total_violations = len(all_violations)
    high_severity = len([v for v in all_violations if v.get('severity') == 'High'])
    medium_severity = len([v for v in all_violations if v.get('severity') == 'Medium'])
    low_severity = len([v for v in all_violations if v.get('severity') == 'Low'])
    
    quality_scores = {
        'overall': max(0, 100 - (high_severity * 10 + medium_severity * 5 + low_severity * 2)),
        'naming': 100 - len([v for v in all_violations if v['domain'] == 'naming']) * 10,
        'javascript': 100 - len([v for v in all_violations if v['domain'] == 'javascript']) * 10,
        'sql': 100,
        'error_handling': 100 - len([v for v in all_violations if v['domain'] == 'errorhandling']) * 10,
        'structure': 100
    }
    
    # Generate key findings
    key_findings = []
    if high_severity > 0:
        key_findings.append({
            'category': 'High Priority',
            'finding': f"{high_severity} high-severity violations require immediate attention",
            'status': 'Critical'
        })
    if medium_severity > 0:
        key_findings.append({
            'category': 'Medium Priority',
            'finding': f"{medium_severity} medium-severity issues impact code quality",
            'status': 'Warning'
        })
    if total_violations == 0:
        key_findings.append({
            'category': 'Quality',
            'finding': 'No violations found - process meets all coding standards',
            'status': 'Pass'
        })
    
    # Build ipa_data
    ipa_data = build_ipa_data_from_violations(
        violations=all_violations,
        client_name=client,
        rice_item=rice_item,
        process_name=process_name,
        process_type=process_type,
        activity_count=activity_count,
        activities=activities,
        quality_scores=quality_scores,
        key_findings=key_findings,
        auto_restart=auto_restart,
        sql_queries_array=sql_queries_array
    )
    
    ipa_data_file = temp_dir / f"{process_name}_ipa_data.json"
    with open(ipa_data_file, 'w', encoding='utf-8') as f:
        json.dump(ipa_data, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ Created: {ipa_data_file.name}")
    
    print()
    print("[4/4] Generating Excel report...")
    
    # Import and use enhanced template
    sys.path.insert(0, str(Path(__file__).parent))
    from ipa_coding_standards_template_enhanced import generate_report
    
    # Load ipa_data
    ipa_data = load_json(ipa_data_file)
    
    # Generate report
    output_filename = generate_report(ipa_data)
    
    # Move to results folder with proper naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f"Coding_Standards_Results/{client}_{rice_item}_{process_name}_CodingStandards_{timestamp}.xlsx"
    
    import shutil
    shutil.move(output_filename, final_filename)
    
    print(f"   ✓ Report generated: {final_filename}")
    
    print()
    print("=" * 80)
    print("PHASE 6 COMPLETE")
    print("=" * 80)
    print()
    print(f"Report: {final_filename}")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
