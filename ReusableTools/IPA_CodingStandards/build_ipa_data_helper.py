#!/usr/bin/env python3
"""
IPA Data Builder Helper - Prevents Duplicate Action Items

This helper ensures that recommendations and coding_standards use EXACT same text
from violations array, preventing duplicate action items in the report.

Usage:
    from ReusableTools.IPA_CodingStandards.build_ipa_data_helper import build_ipa_data_from_violations
    
    violations = [...]  # Your violations array
    ipa_data = build_ipa_data_from_violations(
        violations=violations,
        client_name='FPI',
        rice_item='MatchReport',
        process_name='MatchReport_Outbound',
        process_type='Interface Process',
        activity_count=78,
        activities=activities_array,
        quality_scores=quality_scores_dict,
        key_findings=key_findings_array
    )
"""


def build_ipa_data_from_violations(
    violations,
    client_name,
    rice_item,
    process_name,
    process_type,
    activity_count,
    activities,
    quality_scores,
    key_findings,
    javascript_blocks=0,
    sql_queries_array=None,
    auto_restart='0',
    auto_restart_assessment='',
    best_practices=None,
    technical_deep_dive=None
):
    """
    Build complete ipa_data structure from violations array.
    
    This ensures recommendations and coding_standards use EXACT same text,
    preventing duplicate action items.
    
    Args:
        violations: List of violation dicts with keys:
            - rule_id, rule_name, severity, finding, current, recommendation, activities, domain
        client_name: Client name (e.g., 'FPI')
        rice_item: RICE item name (e.g., 'MatchReport')
        process_name: Process name
        process_type: Process type (e.g., 'Interface Process')
        activity_count: Total activities
        activities: Activities array for complexity calculation
        quality_scores: Quality scores dict
        key_findings: Key findings array
        javascript_blocks: Number of JS blocks (default 0)
        sql_queries_array: SQL queries array (default [])
        auto_restart: Auto-restart value (default '0')
        auto_restart_assessment: Auto-restart assessment text
        best_practices: Best practices array (default [])
        technical_deep_dive: Technical deep dive dict (default {})
    
    Returns:
        Complete ipa_data dict ready for generate_report()
    """
    
    if sql_queries_array is None:
        sql_queries_array = []
    if best_practices is None:
        best_practices = []
    if technical_deep_dive is None:
        technical_deep_dive = {'architecture': {'pattern': '', 'components': [], 'strengths': [], 'weaknesses': []}}
    
    # Calculate summary metrics
    summary_metrics = {
        'total_violations': len(violations),
        'high_severity': sum(1 for v in violations if v['severity'] == 'High'),
        'medium_severity': sum(1 for v in violations if v['severity'] == 'Medium'),
        'low_severity': sum(1 for v in violations if v['severity'] == 'Low'),
        'compliance_percentage': round((activity_count - len(violations)) / activity_count * 100, 1) if activity_count > 0 else 100.0
    }
    
    # Build recommendations FROM violations (ensures exact text match)
    recommendations = []
    for v in violations:
        # Map severity to priority (they're the same in our case)
        priority = v['severity']
        
        # Map domain to category
        domain_to_category = {
            'naming': 'Naming Convention',
            'javascript': 'JavaScript Organization',
            'errorhandling': 'Error Handling',
            'sql': 'SQL Performance',
            'structure': 'System Configuration'
        }
        category = domain_to_category.get(v['domain'], v['domain'].replace('_', ' ').title())
        
        # Determine effort and impact based on severity
        if priority == 'High':
            effort = 'Medium'
            impact = 'High'
        elif priority == 'Medium':
            effort = 'Low'
            impact = 'Medium'
        else:  # Low
            effort = 'Low'
            impact = 'Low'
        
        rec = {
            'priority': priority,
            'category': category,
            'rule_id': v['rule_id'],
            'issue': v['finding'],  # EXACT COPY - DO NOT RETYPE
            'current': v['current'],
            'recommendation': v['recommendation'],
            'effort': effort,
            'impact': impact,
            'activities': v['activities']
        }
        
        # Preserve enhanced fields if present
        if 'impact_analysis' in v:
            impact_analysis = v['impact_analysis']
            rec['priority_score'] = v.get('priority_score', 50)
            rec['estimated_fix_time'] = impact_analysis.get('estimated_fix_time', 'TBD')
            rec['affected_percentage'] = impact_analysis.get('affected_percentage', 0)
        
        if 'code_examples' in v:
            rec['code_example'] = v['code_examples']
        
        if 'testing_notes' in v:
            rec['testing_notes'] = v['testing_notes']
        
        recommendations.append(rec)
    
    # Build coding_standards FROM violations (ensures exact text match)
    coding_standards = {
        'naming_convention': [],
        'ipa_rules': [],
        'error_handling': [],
        'system_configuration': [],
        'performance': []
    }
    
    domain_to_section = {
        'naming': 'naming_convention',
        'javascript': 'ipa_rules',
        'errorhandling': 'error_handling',
        'sql': 'performance',
        'structure': 'system_configuration'
    }
    
    for v in violations:
        section = domain_to_section.get(v['domain'], 'ipa_rules')
        coding_standards[section].append([
            v['activities'],           # Column 0: Activity
            v['rule_name'],           # Column 1: Rule Name (with ID)
            v['severity'],            # Column 2: Severity
            v['finding'],             # Column 3: Finding (EXACT COPY)
            v['current'],             # Column 4: Current
            'Needs Improvement',      # Column 5: Status
            v['recommendation']       # Column 6: Action
        ])
    
    # Build complete ipa_data
    ipa_data = {
        'client_name': client_name,
        'rice_item': rice_item,
        
        'overview': {
            'process_name': process_name,
            'process_type': process_type,
            'activity_count': activity_count,
            'total_activities': activity_count,
            'process_count': 1,
            'javascript_blocks': javascript_blocks,
            'sql_queries': len(sql_queries_array),
            'auto_restart': auto_restart,
            'auto_restart_assessment': auto_restart_assessment
        },
        
        'summary_metrics': summary_metrics,
        'quality_scores': quality_scores,
        'activities': activities,
        'violations': violations,
        'key_findings': key_findings,
        'recommendations': recommendations,
        'sql_queries': sql_queries_array,
        'javascript_issues': [],  # Empty - no ES6 violations
        'coding_standards': coding_standards,
        'best_practices': best_practices,
        'technical_deep_dive': technical_deep_dive,
        'statistics': {}
    }
    
    return ipa_data


if __name__ == '__main__':
    print("IPA Data Builder Helper")
    print("Usage: from ReusableTools.IPA_CodingStandards.build_ipa_data_helper import build_ipa_data_from_violations")
    print()
    print("This helper ensures recommendations and coding_standards use EXACT same text,")
    print("preventing duplicate action items in the report.")
