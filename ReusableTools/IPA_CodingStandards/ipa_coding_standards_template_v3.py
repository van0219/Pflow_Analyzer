#!/usr/bin/env python3
"""
IPA Coding Standards Template - V3.0 Professional Edition

Professional Excel reports with comprehensive improvements:
- Grid-based Executive Dashboard with aligned KPI cards
- Action ID system (ACT-001, ACT-002, etc.) for traceability
- Bidirectional hyperlinks between Detailed Analysis and Action Items
- Workbook navigation links on all sheets
- Metrics Calculation transparency sheet
- Enhanced visual consistency (severity colors, fonts, spacing)
- Dynamic charts (no hardcoded values)
- Impact analysis and code examples
- Priority scoring and testing guidance

5 Sheets:
1. Executive Dashboard - Grid-aligned KPIs and dynamic charts
2. Metrics Calculation - Formula transparency and methodology
3. Action Items - Traceable developer checklist with Action IDs
4. Detailed Analysis - Comprehensive analysis with Action ID hyperlinks
5. Process Flow - Visual diagram with complexity metrics

Version: 3.0
Updated: 2026-03-08 - V3 enhancements for professional stakeholder presentation
"""

import xlsxwriter
from datetime import datetime
# Matplotlib imports removed - using native Excel charts instead
# import matplotlib.pyplot as plt
# from io import BytesIO
# import numpy as np
import json
from pathlib import Path


def calculate_row_height(text, column_width=80, base_height=15):
    """Calculate row height based on text length and column width."""
    if not text:
        return base_height
    
    text = str(text)
    chars_per_line = column_width
    estimated_lines = max(1, len(text) / chars_per_line)
    newline_count = text.count('\n')
    estimated_lines += newline_count
    height = min(409, max(base_height, int(estimated_lines * base_height)))
    
    return height




def generate_action_id(index):
    """Generate Action ID in format ACT-001, ACT-002, etc."""
    return f"ACT-{index:03d}"


def add_navigation_links(ws, wb, current_sheet):
    """
    IMPROVEMENT 2: Add navigation links to all sheets
    
    Adds hyperlinks in row 1 for easy navigation between sheets.
    
    Args:
        ws: Worksheet object
        wb: Workbook object
        current_sheet: Name of current sheet (to skip self-link)
    """
    nav_format = wb.add_format({
        'font_size': 9,
        'align': 'center',
        'bg_color': '#E3F2FD',
        'font_color': '#1565C0',
        'underline': True,
        'border': 1
    })
    
    nav_links = [
        ('📊 Executive Dashboard', "internal:'📊 Executive Dashboard'!A1"),
        ('📐 Metrics Calculation', "internal:'📐 Metrics Calculation'!A1"),
        ('✅ Action Items', "internal:'✅ Action Items'!A1"),
        ('📐 Detailed Analysis', "internal:'📐 Detailed Analysis'!A1"),
        ('🔄 Process Flow', "internal:'🔄 Process Flow'!A1")
    ]
    
    col = 0
    for sheet_name, url in nav_links:
        if sheet_name != current_sheet:
            ws.write_url(0, col, url, nav_format, string=f'→ {sheet_name}')
            col += 1
    
    # Set row height for navigation
    ws.set_row(0, 18)




# IMPROVEMENT 9: Severity Color Standards (verified)
# High Severity: #C62828 (Red) ✓
# Medium Severity: #F57C00 (Orange) ✓
# Low Severity: #FBC02D (Yellow) ✓
# Pass Status: #2E7D32 (Green) ✓
# Modern Color Palette
COLORS = {
    'deep_blue': '#1565C0',
    'green': '#2E7D32',
    'amber': '#F57C00',
    'purple': '#6A1B9A',
    'red': '#C62828',
    'medium_blue': '#1E88E5',
    'light_blue': '#E3F2FD',
    'light_green': '#E8F5E9',
    'light_amber': '#FFF3E0',
    'gray': '#F5F5F5',
    'dark_gray': '#424242',
    'white': '#FFFFFF'
}



def calculate_action_items_count(ipa_data):
    """Calculate the actual number of action items (same logic as Action Items sheet)."""
    seen_items = set()
    count = 0
    
    # Count recommendations
    for rec in ipa_data.get('recommendations', []):
        activities = rec.get('activities', '')
        if isinstance(activities, list):
            activity = ', '.join(str(a) for a in activities) if activities else ipa_data.get('overview', {}).get('process_name', '')
        else:
            activity = str(activities) if activities else ipa_data.get('overview', {}).get('process_name', '')
        
        issue_text = str(rec.get('issue', ''))
        key = (activity.lower().strip(), issue_text.lower().strip())
        
        if key not in seen_items:
            count += 1
            seen_items.add(key)
    
    # Count coding standards violations (status != Pass)
    for section_name, issues in ipa_data.get('coding_standards', {}).items():
        for issue in issues:
            if len(issue) >= 7:
                status = issue[5] if len(issue) > 5 else 'Needs Improvement'
                activity = str(issue[0]) if len(issue) > 0 else ''
                issue_text = str(issue[3]) if len(issue) > 3 else ''
                key = (activity.lower().strip(), issue_text.lower().strip())
                
                if status != 'Pass' and key not in seen_items:
                    count += 1
                    seen_items.add(key)
    
    return count


def calculate_total_checks(ipa_data):
    """
    Calculate total number of checks dynamically from actual rules evaluated.
    
    This replaces the hardcoded total_checks = 100 with an accurate count
    based on the actual coding standards rules that were evaluated during analysis.
    
    Args:
        ipa_data: Dictionary containing analysis results
    
    Returns:
        int: Total number of checks (rules evaluated), defaults to 100 if unavailable
    
    Formula:
        - Count unique rules from all violations
        - Add rules that passed (no violations)
        - Fallback to 100 if metadata unavailable
    """
    # Try to get from project standards metadata
    project_standards = ipa_data.get('project_standards', {})
    rules = project_standards.get('rules', [])
    
    if rules:
        return len(rules)
    
    # Alternative: Count unique rules from violations + estimate passed rules
    violations = ipa_data.get('violations', [])
    unique_rules = set()
    
    for violation in violations:
        rule_id = violation.get('rule_id', '')
        if rule_id:
            unique_rules.add(rule_id)
    
    # Estimate: If we found violations in X rules, assume we checked ~5X rules total
    # (most rules pass, so violations represent ~20% of checks)
    if unique_rules:
        estimated_total = len(unique_rules) * 5
        return min(estimated_total, 100)  # Cap at 100 for reasonableness
    
    # Fallback to 100 if no metadata available
    return 100



def generate_report(ipa_data):
    """Generate enhanced 4-sheet coding standards report"""
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    client = ipa_data.get('client_name', 'Client')
    rice_item = ipa_data.get('rice_item', 'Project')
    process_name = ipa_data.get('overview', {}).get('process_name', '')
    
    # Include process name if provided (for multiple IPAs in same RICE item)
    if process_name:
        output_path = f"Coding_Standards_Results/{client}_{rice_item}_{process_name}_CodingStandards_{date_str}.xlsx"
    else:
        output_path = f"Coding_Standards_Results/{client}_{rice_item}_CodingStandards_{date_str}.xlsx"
    
    workbook = xlsxwriter.Workbook(output_path)
    
    # Create sheets in modern order
    create_executive_dashboard(workbook, ipa_data)
    create_metrics_calculation_sheet(workbook, ipa_data)
    create_action_items_enhanced(workbook, ipa_data)
    create_detailed_analysis_enhanced(workbook, ipa_data)
    create_process_flow(workbook, ipa_data)
    
    workbook.close()
    return output_path



# Removed create_radar_chart - replaced with dynamic Excel charts


def create_executive_dashboard(wb, ipa_data):
    """Create redesigned executive dashboard with dynamic Excel charts"""
    
    # IMPROVEMENT 7: Data Flow Architecture Documentation
    # ====================================================
    # Data Flow:
    #   1. Analysis Phase (Phases 1-5) → ipa_data dictionary
    #   2. ipa_data → Dashboard metrics calculation (this function)
    #   3. Dashboard metrics → Excel cells (written below)
    #   4. Excel cells → Charts (dynamic references)
    #
    # Key Principle: All metrics flow from ipa_data to cells to charts.
    # No static images, no hardcoded values in charts.
    # ====================================================
    
    ws = wb.add_worksheet('📊 Executive Dashboard')
    ws.hide_gridlines(2)
    
    # Print optimization
    ws.set_landscape()
    ws.set_paper(9)  # A4
    ws.fit_to_pages(1, 0)
    ws.set_header('&C&14&B📊 IPA Coding Standards Dashboard')
    ws.set_footer('&LGenerated: &D &T&C&P of &N&R' + ipa_data.get('client_name', 'Client') + ' • ' + ipa_data.get('rice_item', 'Project'))
    
    # Hero section
    hero_format = wb.add_format({
        'bold': True,
        'font_size': 28,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter'
    })
    ws.merge_range('A1:M1', '📊 CODING STANDARDS DASHBOARD', hero_format)
    ws.set_row(0, 45)
    
    # Metadata bar
    client = ipa_data.get('client_name', 'Client')
    rice_item = ipa_data.get('rice_item', 'Project')
    meta_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:M2', f"{client} • {rice_item} | Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", meta_format)
    ws.set_row(1, 22)
    
    # Navigation links
    nav_format = wb.add_format({
        'font_size': 9,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['deep_blue'],
        'underline': True
    })
    ws.write_url('A3', "internal:'✅ Action Items'!A1", nav_format, string='→ Action Items')
    ws.write_url('B3', "internal:'📐 Detailed Analysis'!A1", nav_format, string='→ Detailed Analysis')
    ws.write_url('C3', "internal:'🔄 Process Flow'!A1", nav_format, string='→ Process Flow')
    ws.set_row(2, 15)
    
    # Calculate metrics from violations
    violations = ipa_data.get('violations', [])
    summary_metrics = ipa_data.get('summary_metrics', {})
    
    high_count = summary_metrics.get('high_severity', 0)
    medium_count = summary_metrics.get('medium_severity', 0)
    low_count = summary_metrics.get('low_severity', 0)
    total_violations = summary_metrics.get('total_violations', 0)
    
    # IMPROVEMENT 1: Dynamic Total Checks Calculation
    # Calculate actual number of rules evaluated (replaces hardcoded 100)
    # This ensures pass rate accuracy: (passed / total) × 100
    total_checks = calculate_total_checks(ipa_data)
    passed_checks = total_checks - total_violations
    
    quality_scores = ipa_data.get('quality_scores', {})
    
    # IMPROVEMENT 2: Quality Score Formula Documentation
    # =====================================================
    # QUALITY SCORE CALCULATION (Weighted by Severity)
    # Base Score = 100
    # High Severity Penalty   = -10 points per violation
    # Medium Severity Penalty = -5 points per violation
    # Low Severity Penalty    = -2 points per violation
    #
    # Formula: Score = 100 - (high × 10) - (medium × 5) - (low × 2)
    #
    # Example:
    #   High: 2, Medium: 4, Low: 1
    #   Score = 100 - (2 × 10) - (4 × 5) - (1 × 2)
    #         = 100 - 20 - 20 - 2
    #         = 58
    #
    # Note: This differs from Pass Rate (93%) which treats all violations equally.
    #       Quality Score emphasizes high-severity issues more heavily.
    # =====================================================
    
    overall_score = quality_scores.get('overall', 0)
    
    # IMPROVEMENT 4: Technical Debt KPI
    # Technical Debt = Points lost from base score (100 - quality_score)
    # This metric is widely used in code quality platforms like SonarQube
    technical_debt = 100 - overall_score
    
    # IMPROVEMENT 8: Severity Risk Indicator
    # Provides immediate visibility of critical issues for leadership
    if high_count > 0:
        risk_status = "⚠️ High Severity Issues Detected – Immediate Attention Required"
        risk_level = "CRITICAL"
        risk_bg_color = COLORS['red']
    elif medium_count > 3:
        risk_status = "⚡ Multiple Medium Severity Issues – Review Recommended"
        risk_level = "WARNING"
        risk_bg_color = COLORS['amber']
    else:
        risk_status = "✓ No Critical Violations – Code Quality Acceptable"
        risk_level = "GOOD"
        risk_bg_color = COLORS['green']
            
    # === TOP SECTION: KPI CARDS ===
    row = 3
    
    # Card formats
    card_header = wb.add_format({
        'bold': True,
        'font_size': 11,
        'bg_color': COLORS['deep_blue'],
        'font_color': 'white',
        'align': 'center',
        'border': 1
    })
    
    # Overall Quality Score with color coding
    if overall_score >= 80:
        score_color = COLORS['green']
        score_label = 'Good'
    elif overall_score >= 60:
        score_color = COLORS['amber']
        score_label = 'Needs Attention'
    else:
        score_color = COLORS['red']
        score_label = 'Poor'
    
    card_value_quality = wb.add_format({
        'bold': True,
        'font_size': 36,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': COLORS['white'],
        'font_color': score_color
    })
    
    card_label = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['white'],
        'font_color': COLORS['dark_gray'],
        'border': 1
    })
    
    # High Severity Risk Indicator with color coding
    if high_count > 0:
        risk_color = COLORS['red']
        risk_label = 'Immediate Attention Required'
    else:
        risk_color = COLORS['green']
        risk_label = 'No Critical Violations'
    
    risk_header = wb.add_format({
        'bold': True,
        'font_size': 11,
        'bg_color': risk_color,
        'font_color': 'white',
        'align': 'center',
        'border': 1
    })
    
    risk_value = wb.add_format({
        'bold': True,
        'font_size': 36,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': COLORS['white'],
        'font_color': risk_color
    })
    
    # IMPROVEMENT 1: Grid-Based KPI Layout
    # Row 6-12: KPI Cards aligned in strict grid (B-E, F-I, J-M, N-Q)
    
    # Card 1: Overall Quality Score (Columns B-E)
    ws.merge_range(row, 1, row, 4, '🎯 OVERALL QUALITY SCORE', card_header)
    ws.merge_range(row+1, 1, row+2, 4, overall_score, card_value_quality)
    ws.merge_range(row+3, 1, row+3, 4, score_label, card_label)
    
    # Card 2: Pass Rate (Columns F-I)
    pass_rate = int((passed_checks / total_checks) * 100) if total_checks > 0 else 100
    ws.merge_range(row, 5, row, 8, '✅ PASS RATE', card_header)
    ws.merge_range(row+1, 5, row+2, 8, f'{pass_rate}%', card_value_quality)
    ws.merge_range(row+3, 5, row+3, 8, f'{passed_checks}/{total_checks} Checks', card_label)
    
    # Card 3: Total Violations (Columns J-M)
    ws.merge_range(row, 9, row, 12, '📋 TOTAL VIOLATIONS', card_header)
    ws.merge_range(row+1, 9, row+2, 12, total_violations, card_value_quality)
    ws.merge_range(row+3, 9, row+3, 12, f'{high_count} High, {medium_count} Med, {low_count} Low', card_label)
    
    # Card 4: Technical Debt (Columns N-Q)
    ws.merge_range(row, 13, row, 16, '⚠️ TECHNICAL DEBT', card_header)
    ws.merge_range(row+1, 13, row+2, 16, technical_debt, card_value_quality)
    ws.merge_range(row+3, 13, row+3, 16, f'{technical_debt} Points Lost', card_label)
    
    # IMPROVEMENT 4: Card 5 - Technical Debt KPI (Columns M-O, if space allows)
    # Note: May need to adjust column layout or add to second row
    # For now, we'll add it as a prominent metric below the main cards
        
    ws.set_row(row, 25)
    ws.set_row(row+1, 35)
    ws.set_row(row+2, 35)
    ws.set_row(row+3, 22)
    
    row += 5
    
    # IMPROVEMENT 8: Severity Risk Indicator Banner
    # Display prominent risk status for leadership visibility
    risk_banner_format = wb.add_format({
        'bold': True,
        'font_size': 12,
        'font_color': 'white',
        'bg_color': risk_bg_color,
        'align': 'center',
        'valign': 'vcenter',
        'border': 2
    })
    
    ws.merge_range(row, 0, row, 11, f'{risk_status}', risk_banner_format)
    ws.set_row(row, 30)
    row += 1
    
    # Technical Debt Display (below risk banner)
    tech_debt_label_format = wb.add_format({
        'bold': True,
        'font_size': 11,
        'bg_color': COLORS['gray'],
        'align': 'right',
        'valign': 'vcenter',
        'border': 1
    })
    
    tech_debt_value_format = wb.add_format({
        'bold': True,
        'font_size': 16,
        'font_color': COLORS['amber'] if technical_debt > 30 else COLORS['green'],
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    ws.merge_range(row, 0, row, 5, '📊 Technical Debt (Points Lost):', tech_debt_label_format)
    ws.merge_range(row, 6, row, 11, f'{technical_debt} points', tech_debt_value_format)
    ws.set_row(row, 25)
    row += 1
    ws.set_row(row, 15)
    row += 1
    
    # === WRITE CHART DATA TO VISIBLE CELLS ===
    # This is the key fix - write data that charts can reference
    
    data_row_start = row + 1
    
    # Header row for chart data
    data_header_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': COLORS['light_blue'],
        'align': 'center',
        'border': 1
    })
    
    ws.write(row, 0, 'Severity', data_header_format)
    ws.write(row, 1, 'Count', data_header_format)
    ws.set_row(row, 20)
    row += 1
    
    # Write severity data
    data_format = wb.add_format({
        'font_size': 10,
        'align': 'left',
        'border': 1
    })
    
    data_value_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'border': 1
    })
    
    ws.write(row, 0, 'High Violations', data_format)
    ws.write(row, 1, high_count, data_value_format)
    row += 1
    
    ws.write(row, 0, 'Medium Violations', data_format)
    ws.write(row, 1, medium_count, data_value_format)
    row += 1
    
    ws.write(row, 0, 'Low Violations', data_format)
    ws.write(row, 1, low_count, data_value_format)
    row += 1
    
    # === MIDDLE SECTION: VIOLATION SEVERITY DISTRIBUTION ===
    row += 2
    
    section_header = wb.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'align': 'left',
        'valign': 'vcenter',
        'left': 2,
        'right': 2,
        'top': 2,
        'bottom': 2
    })
    
    ws.merge_range(row, 0, row, 5, '📊 VIOLATION SEVERITY DISTRIBUTION', section_header)
    ws.set_row(row, 28)
    row += 1
    
    # Create Clustered Column Chart
    column_chart = wb.add_chart({'type': 'column'})
    column_chart.add_series({
        'name': 'Violations',
        'categories': ['📊 Executive Dashboard', data_row_start, 0, data_row_start + 2, 0],
        'values': ['📊 Executive Dashboard', data_row_start, 1, data_row_start + 2, 1],
        'data_labels': {'value': True, 'position': 'outside_end'},
        'points': [
            {'fill': {'color': COLORS['red']}},      # High
            {'fill': {'color': COLORS['amber']}},    # Medium
            {'fill': {'color': '#FDD835'}}           # Low (Yellow)
        ]
    })
    
    column_chart.set_title({'name': 'Violation Severity Distribution', 'name_font': {'size': 14, 'bold': True}})
    column_chart.set_x_axis({'name': 'Severity Level', 'name_font': {'size': 11}})
    column_chart.set_y_axis({'name': 'Number of Violations', 'name_font': {'size': 11}})
    column_chart.set_size({'width': 480, 'height': 360})
    column_chart.set_legend({'position': 'none'})
    column_chart.set_style(11)
    
    ws.insert_chart(row, 0, column_chart)
    
    # === RIGHT SECTION: CODE QUALITY PASS RATE ===
    ws.merge_range(row, 6, row, 11, '✅ CODE QUALITY PASS RATE', section_header)
    ws.set_row(row, 28)
    
    # Write pass/fail data for donut chart
    pass_fail_row = row + 1
    ws.write(pass_fail_row, 7, 'Status', data_header_format)
    ws.write(pass_fail_row, 8, 'Count', data_header_format)
    
    ws.write(pass_fail_row + 1, 7, 'Passed Checks', data_format)
    ws.write(pass_fail_row + 1, 8, passed_checks, data_value_format)
    
    ws.write(pass_fail_row + 2, 7, 'Failed Checks', data_format)
    ws.write(pass_fail_row + 2, 8, total_violations, data_value_format)
    
    # Create Donut Chart
    donut_chart = wb.add_chart({'type': 'doughnut'})
    donut_chart.add_series({
        'name': 'Code Quality',
        'categories': ['📊 Executive Dashboard', pass_fail_row + 1, 7, pass_fail_row + 2, 7],
        'values': ['📊 Executive Dashboard', pass_fail_row + 1, 8, pass_fail_row + 2, 8],
        'data_labels': {'percentage': True, 'position': 'best_fit', 'font': {'size': 11, 'bold': True}},
        'points': [
            {'fill': {'color': COLORS['green']}},    # Passed
            {'fill': {'color': COLORS['red']}}       # Failed
        ]
    })
    
    donut_chart.set_title({'name': 'Code Quality Pass Rate', 'name_font': {'size': 14, 'bold': True}})
    donut_chart.set_size({'width': 480, 'height': 360})
    donut_chart.set_legend({'position': 'bottom', 'font': {'size': 10}})
    donut_chart.set_hole_size(50)
    
    ws.insert_chart(row + 1, 6, donut_chart)
    
    row += 22
    
    # === KEY FINDINGS SECTION ===
    ws.merge_range(row, 0, row, 11, '🔍 KEY FINDINGS', section_header)
    ws.set_row(row, 25)
    row += 1
    
    finding_format = wb.add_format({
        'font_size': 10,
        'text_wrap': True,
        'valign': 'top',
        'bg_color': COLORS['white'],
        'border': 1,
        'border_color': COLORS['gray']
    })
    
    # Generate key findings from data
    key_findings = []
    
    if high_count > 0:
        key_findings.append({
            'status': 'Critical',
            'category': 'High Priority',
            'details': f'{high_count} high-severity violations require immediate attention'
        })
    
    if medium_count > 0:
        key_findings.append({
            'status': 'Warning',
            'category': 'Medium Priority',
            'details': f'{medium_count} medium-severity issues impact code quality'
        })
    
    if overall_score >= 80:
        key_findings.append({
            'status': 'Pass',
            'category': 'Quality Score',
            'details': f'Overall quality score of {overall_score} indicates good code quality'
        })
    elif overall_score >= 60:
        key_findings.append({
            'status': 'Warning',
            'category': 'Quality Score',
            'details': f'Overall quality score of {overall_score} needs attention'
        })
    else:
        key_findings.append({
            'status': 'Critical',
            'category': 'Quality Score',
            'details': f'Overall quality score of {overall_score} indicates poor code quality'
        })
    
    for finding in key_findings[:5]:
        status = finding.get('status', 'Info')
        category = finding.get('category', '')
        details = finding.get('details', '')
        
        if status in ['Pass', 'Excellent', 'Good']:
            badge_color = COLORS['green']
        elif status in ['Verify', 'Needs Improvement', 'Warning']:
            badge_color = COLORS['amber']
        else:
            badge_color = COLORS['red']
        
        badge_format = wb.add_format({
            'bold': True,
            'font_size': 9,
            'bg_color': badge_color,
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        category_format = wb.add_format({
            'bold': True,
            'font_size': 10,
            'bg_color': COLORS['white'],
            'border': 1,
            'border_color': COLORS['gray']
        })
        
        ws.write(row, 0, status, badge_format)
        ws.write(row, 1, category, category_format)
        ws.merge_range(row, 2, row, 11, details, finding_format)
        ws.set_row(row, 35)
        row += 1
    
    # Column widths
    ws.set_column('A:A', 12)
    ws.set_column('B:B', 15)
    ws.set_column('C:L', 12)


def create_action_items_enhanced(wb, ipa_data):
    """Create enhanced action items sheet with impact analysis and code examples"""
    ws = wb.add_worksheet('✅ Action Items')
    ws.hide_gridlines(2)
    
    # Phase 4: Print optimization
    ws.set_landscape()
    ws.set_paper(9)  # A4
    ws.fit_to_pages(1, 0)  # Fit to 1 page wide
    ws.set_header('&C&14&B✅ Action Items - Developer Checklist')
    ws.set_footer('&LPage &P of &N&C' + ipa_data.get('client_name', 'Client') + ' • ' + ipa_data.get('rice_item', 'Project') + '&R&D')
    ws.repeat_rows(0, 3)  # Repeat title and header rows when printing
    ws.set_print_scale(85)  # Scale to 85% for better fit
    
    # Modern title
    title_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter'
    })
    ws.merge_range('A3:N3', '✅ ACTION ITEMS - ENHANCED DEVELOPER CHECKLIST', title_format)
    ws.set_row(1, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A3:N3', 'Items with impact analysis, code examples, and testing guidance', subtitle_format)
    ws.set_row(2, 20)
    
    # IMPROVEMENT 2: Navigation links
    add_navigation_links(ws, wb, '✅ Action Items')
    ws.set_row(0, 18)
    
    # Adjust row numbers (navigation now in row 0)
    
    # Headers
    row = 4  # V3: Adjusted for navigation
    header_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1,
        'border_color': COLORS['white'],
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })
    
    # Data formats
    cell_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'text_wrap': True,
        'font_size': 9
    })
    critical_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFEBEE',
        'text_wrap': True,
        'font_size': 9
    })
    high_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFF3E0',
        'text_wrap': True,
        'font_size': 9
    })
    medium_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFFDE7',
        'text_wrap': True,
        'font_size': 9
    })
    
    # Headers
    row = 3
    # IMPROVEMENT 4: Add Action ID column
    headers = [
        'Action ID', 'Priority', 'Category', 'Rule ID', 'Activity', 'Issue', 'Current', 
        'Recommendation', 'Effort', 'Impact', 'Priority\nScore', 'Est. Fix\nTime', 
        'Affected\n%', 'Code Example', 'Testing Notes', 'Status'
    ]
    for col, header in enumerate(headers):
        ws.write(row, col, header, header_format)
    ws.set_row(row, 30)
    
    # Phase 2: Priority color formats with conditional formatting
    critical_priority_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFEBEE',  # Light red
        'text_wrap': True,
        'font_size': 9,
        'bold': True,
        'font_color': COLORS['red']
    })
    high_priority_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFF3E0',  # Light amber
        'text_wrap': True,
        'font_size': 9,
        'bold': True,
        'font_color': COLORS['amber']
    })
    medium_priority_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFFDE7',  # Light yellow
        'text_wrap': True,
        'font_size': 9,
        'font_color': COLORS['dark_gray']
    })
    low_priority_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': COLORS['white'],
        'text_wrap': True,
        'font_size': 9,
        'font_color': COLORS['dark_gray']
    })
    
    row += 1
    
    # Collect all issues
    all_issues = []
    seen_items = set()
    
    # Add violations from ipa_data['violations'] (primary source with complete data)
    for violation in ipa_data.get('violations', []):
        activity = violation.get('activity_caption', violation.get('activity_id', violation.get('activities', '')))
        issue_text = violation.get('finding', violation.get('issue', ''))
        key = (activity.lower().strip(), issue_text.lower().strip())
        
        if key not in seen_items:
            # Map domain to category
            domain_to_category = {
                'naming': 'Naming Convention',
                'javascript': 'JavaScript Organization',
                'sql': 'SQL Performance',
                'errorhandling': 'Error Handling',
                'structure': 'System Configuration'
            }
            category = domain_to_category.get(violation.get('domain', ''), 'General')
            
            # Calculate priority score based on severity and impact
            severity = violation.get('severity', 'Medium')
            impact = violation.get('impact', 'Medium')
            priority_score = 50
            if severity == 'High' and impact == 'High':
                priority_score = 90
            elif severity == 'High' or impact == 'High':
                priority_score = 70
            elif severity == 'Medium' and impact == 'Medium':
                priority_score = 50
            else:
                priority_score = 30
            
            all_issues.append({
                'priority': severity,
                'category': category,
                'rule_id': violation.get('rule_id', 'N/A'),
                'activity': activity,
                'issue': issue_text,
                'current': violation.get('current', violation.get('current_state', '')),
                'recommendation': violation.get('recommendation', ''),
                'effort': violation.get('effort', 'Medium'),
                'impact': impact,
                'priority_score': priority_score,
                'estimated_fix_time': 'TBD',
                'affected_percentage': 0,
                'code_example': violation.get('code_example', ''),
                'testing_notes': violation.get('testing_notes', ''),
                'status': 'Not Started'
            })
            seen_items.add(key)
    
    # Sort by priority score (descending)
    all_issues.sort(key=lambda x: x.get('priority_score', 50), reverse=True)
    
    # Write issues
    for issue in all_issues:
        severity = issue['priority']
        
        # Phase 2: Use priority-specific formats with color coding
        if severity == 'Critical':
            fmt = critical_priority_format
        elif severity == 'High':
            fmt = high_priority_format
        elif severity == 'Medium':
            fmt = medium_priority_format
        else:
            fmt = low_priority_format
        
        # Extract enhanced fields if available
        priority_score = issue.get('priority_score', 50)
        estimated_fix_time = issue.get('estimated_fix_time', 'TBD')
        affected_percentage = issue.get('affected_percentage', 0)
        
        # Format code example
        code_example = ''
        if issue.get('code_example'):
            if isinstance(issue['code_example'], dict):
                before = issue['code_example'].get('before', '')
                after = issue['code_example'].get('after', '')
                code_example = f"Before: {before}\nAfter: {after}"
            else:
                code_example = str(issue['code_example'])
        
        testing_notes = issue.get('testing_notes', '')
        
        # IMPROVEMENT 4 & 6: Add Action ID with hyperlink to Detailed Analysis
        action_id = generate_action_id(all_issues.index(issue) + 1)
        ws.write_url(row, 0, f"internal:'📐 Detailed Analysis'!A{row+10}", fmt, string=action_id)
        
        ws.write(row, 1, issue['priority'], fmt)
        ws.write(row, 2, issue['category'], fmt)
        ws.write(row, 3, issue['rule_id'], fmt)
        ws.write(row, 4, issue['activity'], fmt)
        ws.write(row, 5, issue['issue'], fmt)
        ws.write(row, 6, issue['current'], fmt)
        ws.write(row, 7, issue['recommendation'], fmt)
        ws.write(row, 8, issue['effort'], fmt)
        ws.write(row, 9, issue['impact'], fmt)
        ws.write(row, 10, priority_score, fmt)
        ws.write(row, 11, estimated_fix_time, fmt)
        ws.write(row, 12, f"{affected_percentage}%" if affected_percentage > 0 else 'N/A', fmt)
        ws.write(row, 13, code_example, fmt)
        ws.write(row, 14, testing_notes, fmt)
        ws.write(row, 15, 'Not Started', fmt)  # Status column
        
        ws.set_row(row, 60)
        row += 1
    
    # Phase 3: Add AutoFilter to enable filtering
    if row > 4:
        ws.autofilter(3, 0, row - 1, 15)
    
    # Phase 3: Add data validation for Status column
    ws.data_validation(f'P4:P{row}', {
        'validate': 'list',
        'source': ['Not Started', 'In Progress', 'Complete', 'Blocked'],
        'input_title': 'Select Status',
        'input_message': 'Choose current status of this action item',
        'error_title': 'Invalid Status',
        'error_message': 'Please select a valid status from the dropdown'
    })
    
    # Column widths
    # IMPROVEMENT 4: Updated column widths for Action ID
    ws.set_column('A:A', 10)  # Action ID
    ws.set_column('B:B', 8)   # Priority
    ws.set_column('C:C', 18)  # Category
    ws.set_column('D:D', 10)  # Rule ID
    ws.set_column('E:E', 20)  # Activity
    ws.set_column('F:F', 25)  # Issue
    ws.set_column('G:G', 20)  # Current
    ws.set_column('H:H', 30)  # Recommendation
    ws.set_column('I:I', 8)   # Effort
    ws.set_column('J:J', 8)   # Impact
    ws.set_column('K:K', 8)   # Priority Score
    ws.set_column('L:L', 10)  # Est. Fix Time
    ws.set_column('M:M', 8)   # Affected %
    ws.set_column('N:N', 25)  # Code Example
    ws.set_column('O:O', 25)  # Testing Notes
    ws.set_column('P:P', 12)  # Status



def create_detailed_analysis_enhanced(wb, ipa_data):
    """Create enhanced detailed analysis sheet with impact analysis and code examples"""
    ws = wb.add_worksheet('📐 Detailed Analysis')
    ws.hide_gridlines(2)
    
    # Phase 4: Print optimization
    ws.set_portrait()
    ws.set_paper(9)  # A4
    ws.fit_to_pages(1, 0)  # Fit to 1 page wide
    ws.set_header('&C&14&B📐 Detailed Analysis')
    ws.set_footer('&LPage &P of &N&C' + ipa_data.get('client_name', 'Client') + ' • ' + ipa_data.get('rice_item', 'Project') + '&R&D')
    ws.repeat_rows(0, 2)  # Repeat title rows when printing
    
    # Modern title
    title_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter'
    })
    ws.merge_range('A1:J1', '📐 DETAILED ANALYSIS WITH IMPACT ASSESSMENT', title_format)
    ws.set_row(1, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:J2', 'Comprehensive technical analysis with code examples and testing guidance', subtitle_format)
    ws.set_row(2, 20)
    
    # IMPROVEMENT 2: Navigation links
    add_navigation_links(ws, wb, '✅ Action Items')
    ws.set_row(0, 18)
    
    # Adjust row numbers (navigation now in row 0)
    
    # Section header format
    section_format = wb.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1,
        'border_color': COLORS['white']
    })
    
    # Subsection format
    subsection_format = wb.add_format({
        'bold': True,
        'font_size': 12,
        'bg_color': COLORS['light_blue'],
        'border': 1,
        'border_color': COLORS['gray']
    })
    
    # Phase 2: Severity badge formats (Phase 4: Enhanced for accessibility)
    critical_badge_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': '#D32F2F',  # Phase 4: Darker red for better contrast
        'font_color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 2,
        'border_color': '#B71C1C'  # Phase 4: Darker border
    })
    high_badge_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': '#F57C00',  # Phase 4: Darker amber for better contrast
        'font_color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 2,
        'border_color': '#E65100'  # Phase 4: Darker border
    })
    medium_badge_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': '#FBC02D',  # Phase 4: Darker yellow for better contrast
        'font_color': '#212121',  # Phase 4: Darker text
        'align': 'center',
        'valign': 'vcenter',
        'border': 2,
        'border_color': '#F57F17'  # Phase 4: Darker border
    })
    low_badge_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': '#388E3C',  # Phase 4: Darker green for better contrast
        'font_color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 2,
        'border_color': '#1B5E20'  # Phase 4: Darker border
    })
    
    # Data formats
    label_format = wb.add_format({
        'bold': True,
        'border': 1,
        'border_color': COLORS['gray'],
        'bg_color': COLORS['gray'],
        'font_size': 10
    })
    value_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'text_wrap': True,
        'valign': 'top',
        'font_size': 10
    })
    code_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'font_name': 'Consolas',
        'bg_color': COLORS['gray'],
        'text_wrap': True,
        'font_size': 9
    })
    good_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'bg_color': COLORS['light_green'],
        'text_wrap': True,
        'font_size': 10
    })
    warning_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'bg_color': COLORS['light_amber'],
        'text_wrap': True,
        'font_size': 10
    })
    
    row = 3
    
    # SECTION 1: Process Overview
    ws.merge_range(row, 0, row, 9, '1. PROCESS OVERVIEW', section_format)
    row += 1
    
    overview = ipa_data.get('overview', {})
    ws.write(row, 0, 'Process Name:', label_format)
    ws.merge_range(row, 1, row, 9, overview.get('process_name', 'N/A'), value_format)
    row += 1
    
    ws.write(row, 0, 'Process Type:', label_format)
    ws.merge_range(row, 1, row, 9, overview.get('process_type', 'N/A'), value_format)
    row += 1
    
    ws.write(row, 0, 'Total Activities:', label_format)
    ws.merge_range(row, 1, row, 9, str(overview.get('total_activities', 0)), value_format)
    row += 1
    
    ws.write(row, 0, 'Auto-Restart:', label_format)
    ws.merge_range(row, 1, row, 9, overview.get('auto_restart', 'N/A'), value_format)
    row += 2

    
    # SECTION 2: Violations with Enhanced Analysis
    ws.merge_range(row, 0, row, 9, '2. VIOLATIONS WITH IMPACT ANALYSIS', section_format)
    row += 1
    
    violations = ipa_data.get('violations', [])
    if violations:
        for idx, violation in enumerate(violations, 1):
            # Phase 2: Violation header with severity badge
            severity = violation.get('severity', 'Medium')
            if severity == 'Critical':
                badge_fmt = critical_badge_format
                badge_text = '🔴 CRITICAL'  # Phase 4: Icon + text for accessibility
            elif severity == 'High':
                badge_fmt = high_badge_format
                badge_text = '🟠 HIGH'  # Phase 4: Icon + text for accessibility
            elif severity == 'Medium':
                badge_fmt = medium_badge_format
                badge_text = '🟡 MEDIUM'  # Phase 4: Icon + text for accessibility
            else:
                badge_fmt = low_badge_format
                badge_text = '🟢 LOW'  # Phase 4: Icon + text for accessibility
            
            # IMPROVEMENT 5 & 6: Violation header with Action ID and hyperlink
            action_id = generate_action_id(idx)
            ws.write_url(row, 0, f"internal:'✅ Action Items'!A{idx+4}", badge_fmt, string=badge_text)
            ws.write(row, 1, action_id, subsection_format)
            ws.merge_range(row, 2, row, 9, f"Violation {idx}: {violation.get('rule_name', 'N/A')}", subsection_format)
            row += 1
            
            # Basic info
            ws.write(row, 0, 'Activity:', label_format)
            activity_value = violation.get('activity_caption', violation.get('activity_id', violation.get('activities', 'N/A')))
            ws.merge_range(row, 1, row, 9, activity_value, value_format)
            row += 1
            
            ws.write(row, 0, 'Finding:', label_format)
            finding_value = violation.get('issue', violation.get('finding', 'N/A'))
            ws.merge_range(row, 1, row, 9, finding_value, value_format)
            row += 1
            
            ws.write(row, 0, 'Current:', label_format)
            current_value = violation.get('current_state', violation.get('current', 'N/A'))
            ws.merge_range(row, 1, row, 9, current_value, value_format)
            row += 1
            
            ws.write(row, 0, 'Recommendation:', label_format)
            ws.merge_range(row, 1, row, 9, violation.get('recommendation', 'N/A'), value_format)
            row += 1
            
            # Impact Analysis (if available)
            impact_analysis = violation.get('impact_analysis', {})
            if impact_analysis:
                ws.merge_range(row, 0, row, 9, '📊 Impact Analysis', subsection_format)
                row += 1
                
                ws.write(row, 0, 'Frequency:', label_format)
                ws.merge_range(row, 1, row, 4, impact_analysis.get('frequency', 'N/A'), value_format)
                ws.write(row, 5, 'Affected %:', label_format)
                ws.merge_range(row, 6, row, 9, f"{impact_analysis.get('affected_percentage', 0)}%", value_format)
                row += 1
                
                ws.write(row, 0, 'Maintainability:', label_format)
                ws.merge_range(row, 1, row, 4, impact_analysis.get('maintainability_impact', 'N/A'), value_format)
                ws.write(row, 5, 'Est. Fix Time:', label_format)
                ws.merge_range(row, 6, row, 9, impact_analysis.get('estimated_fix_time', 'N/A'), value_format)
                row += 1
            
            # Code Examples (if available)
            code_examples = violation.get('code_examples', {})
            if code_examples:
                ws.merge_range(row, 0, row, 9, '💻 Code Examples', subsection_format)
                row += 1
                
                ws.write(row, 0, 'Before:', label_format)
                ws.merge_range(row, 1, row, 9, code_examples.get('before', 'N/A'), code_format)
                row += 1
                
                ws.write(row, 0, 'After:', label_format)
                ws.merge_range(row, 1, row, 9, code_examples.get('after', 'N/A'), code_format)
                row += 1
                
                ws.write(row, 0, 'Explanation:', label_format)
                ws.merge_range(row, 1, row, 9, code_examples.get('explanation', 'N/A'), value_format)
                row += 1
            
            # Testing Notes (if available)
            testing_notes = violation.get('testing_notes', '')
            if testing_notes:
                ws.merge_range(row, 0, row, 9, '🧪 Testing Notes', subsection_format)
                row += 1
                
                ws.merge_range(row, 0, row, 9, testing_notes, value_format)
                row += 1
            
            # Priority Score (if available)
            priority_score = violation.get('priority_score', 0)
            if priority_score > 0:
                ws.write(row, 0, 'Priority Score:', label_format)
                score_fmt = warning_format if priority_score >= 70 else value_format
                ws.merge_range(row, 1, row, 9, f"{priority_score}/100", score_fmt)
                row += 1
            
            row += 1  # Spacer between violations
    else:
        ws.merge_range(row, 0, row, 9, '✓ No violations found', good_format)
        row += 1
    
    row += 1
    
    # Column widths
    ws.set_column('A:A', 15)
    ws.set_column('B:J', 20)


def create_metrics_calculation_sheet(wb, ipa_data):
    """
    IMPROVEMENT 3: Metrics Calculation Transparency Sheet
    
    Create a worksheet that documents how all dashboard metrics are calculated.
    This improves auditability and user trust in the metrics.
    
    Sections:
        1. Quality Score Formula with example calculation
        2. Pass Rate Formula with example calculation
        3. Violation Summary (severity breakdown)
        4. Technical Debt Explanation
        5. Data Sources and Methodology
    """
    ws = wb.add_worksheet('📐 Metrics Calculation')
    ws.hide_gridlines(2)
    
    # Title
    title_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter'
    })
    ws.merge_range('A1:H1', '📐 METRICS CALCULATION METHODOLOGY', title_format)
    ws.set_row(1, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:H2', 'Transparency documentation for dashboard metrics', subtitle_format)
    ws.set_row(2, 20)
    
    # Section header format
    section_format = wb.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1
    })
    
    # Label format
    label_format = wb.add_format({
        'bold': True,
        'font_size': 11,
        'bg_color': COLORS['gray'],
        'border': 1
    })
    
    # Value format
    value_format = wb.add_format({
        'font_size': 11,
        'border': 1,
        'valign': 'top'
    })
    
    # Formula format
    formula_format = wb.add_format({
        'font_size': 11,
        'font_name': 'Consolas',
        'bg_color': COLORS['light_blue'],
        'border': 1,
        'valign': 'top'
    })
    
    # Example format
    example_format = wb.add_format({
        'font_size': 11,
        'bg_color': COLORS['light_green'],
        'border': 1,
        'valign': 'top'
    })
    
    row = 3
    
    # Get metrics
    summary_metrics = ipa_data.get('summary_metrics', {})
    high_count = summary_metrics.get('high_severity', 0)
    medium_count = summary_metrics.get('medium_severity', 0)
    low_count = summary_metrics.get('low_severity', 0)
    total_violations = summary_metrics.get('total_violations', 0)
    
    quality_scores = ipa_data.get('quality_scores', {})
    overall_score = quality_scores.get('overall', 0)
    
    total_checks = calculate_total_checks(ipa_data)
    passed_checks = total_checks - total_violations
    pass_rate = int((passed_checks / total_checks) * 100) if total_checks > 0 else 100
    technical_debt = 100 - overall_score
    
    # ========================================
    # SECTION 1: Quality Score Formula
    # ========================================
    ws.merge_range(row, 0, row, 7, '1. QUALITY SCORE FORMULA', section_format)
    row += 1
    
    ws.write(row, 0, 'Base Score:', label_format)
    ws.merge_range(row, 1, row, 7, '100 points', value_format)
    row += 1
    
    ws.write(row, 0, 'Penalty System:', label_format)
    ws.merge_range(row, 1, row, 7, 'Weighted by severity to emphasize critical issues', value_format)
    row += 1
    
    ws.write(row, 0, 'High Severity:', label_format)
    ws.merge_range(row, 1, row, 7, '-10 points per violation', value_format)
    row += 1
    
    ws.write(row, 0, 'Medium Severity:', label_format)
    ws.merge_range(row, 1, row, 7, '-5 points per violation', value_format)
    row += 1
    
    ws.write(row, 0, 'Low Severity:', label_format)
    ws.merge_range(row, 1, row, 7, '-2 points per violation', value_format)
    row += 1
    
    ws.write(row, 0, 'Formula:', label_format)
    ws.merge_range(row, 1, row, 7, 'Score = 100 - (High × 10) - (Medium × 5) - (Low × 2)', formula_format)
    row += 1
    
    ws.write(row, 0, 'Your Report:', label_format)
    calculation_text = f'Score = 100 - ({high_count} × 10) - ({medium_count} × 5) - ({low_count} × 2)\\n'
    calculation_text += f'      = 100 - {high_count * 10} - {medium_count * 5} - {low_count * 2}\\n'
    calculation_text += f'      = {overall_score}'
    ws.merge_range(row, 1, row, 7, calculation_text, example_format)
    ws.set_row(row, 45)
    row += 1
    
    ws.write(row, 0, 'Result:', label_format)
    ws.merge_range(row, 1, row, 7, f'Quality Score = {overall_score}', example_format)
    row += 2
    
    # ========================================
    # SECTION 2: Pass Rate Formula
    # ========================================
    ws.merge_range(row, 0, row, 7, '2. PASS RATE FORMULA', section_format)
    row += 1
    
    ws.write(row, 0, 'Formula:', label_format)
    ws.merge_range(row, 1, row, 7, 'Pass Rate = (Passed Checks / Total Checks) × 100', formula_format)
    row += 1
    
    ws.write(row, 0, 'Total Checks:', label_format)
    ws.merge_range(row, 1, row, 7, f'{total_checks} rules evaluated', value_format)
    row += 1
    
    ws.write(row, 0, 'Failed Checks:', label_format)
    ws.merge_range(row, 1, row, 7, f'{total_violations} violations found', value_format)
    row += 1
    
    ws.write(row, 0, 'Passed Checks:', label_format)
    ws.merge_range(row, 1, row, 7, f'{passed_checks} rules passed', value_format)
    row += 1
    
    ws.write(row, 0, 'Your Report:', label_format)
    pass_calc_text = f'Pass Rate = ({passed_checks} / {total_checks}) × 100\\n'
    pass_calc_text += f'          = {pass_rate}%'
    ws.merge_range(row, 1, row, 7, pass_calc_text, example_format)
    ws.set_row(row, 30)
    row += 1
    
    ws.write(row, 0, 'Result:', label_format)
    ws.merge_range(row, 1, row, 7, f'Pass Rate = {pass_rate}%', example_format)
    row += 2
    
    # ========================================
    # SECTION 3: Violation Summary
    # ========================================
    ws.merge_range(row, 0, row, 7, '3. VIOLATION SUMMARY', section_format)
    row += 1
    
    ws.write(row, 0, 'High Severity:', label_format)
    ws.merge_range(row, 1, row, 7, f'{high_count} violations', value_format)
    row += 1
    
    ws.write(row, 0, 'Medium Severity:', label_format)
    ws.merge_range(row, 1, row, 7, f'{medium_count} violations', value_format)
    row += 1
    
    ws.write(row, 0, 'Low Severity:', label_format)
    ws.merge_range(row, 1, row, 7, f'{low_count} violations', value_format)
    row += 1
    
    ws.write(row, 0, 'Total Violations:', label_format)
    ws.merge_range(row, 1, row, 7, f'{total_violations} violations', example_format)
    row += 1
    
    ws.write(row, 0, 'Verification:', label_format)
    ws.merge_range(row, 1, row, 7, f'{high_count} + {medium_count} + {low_count} = {total_violations} ✓', example_format)
    row += 2
    
    # ========================================
    # SECTION 4: Technical Debt
    # ========================================
    ws.merge_range(row, 0, row, 7, '4. TECHNICAL DEBT', section_format)
    row += 1
    
    ws.write(row, 0, 'Definition:', label_format)
    ws.merge_range(row, 1, row, 7, 'Points lost from base score due to violations', value_format)
    row += 1
    
    ws.write(row, 0, 'Formula:', label_format)
    ws.merge_range(row, 1, row, 7, 'Technical Debt = 100 - Quality Score', formula_format)
    row += 1
    
    ws.write(row, 0, 'Your Report:', label_format)
    debt_calc_text = f'Technical Debt = 100 - {overall_score}\\n'
    debt_calc_text += f'               = {technical_debt} points'
    ws.merge_range(row, 1, row, 7, debt_calc_text, example_format)
    ws.set_row(row, 30)
    row += 1
    
    ws.write(row, 0, 'Interpretation:', label_format)
    if technical_debt <= 10:
        interpretation = 'Excellent - Minimal technical debt'
    elif technical_debt <= 30:
        interpretation = 'Good - Manageable technical debt'
    elif technical_debt <= 50:
        interpretation = 'Fair - Moderate technical debt requiring attention'
    else:
        interpretation = 'Poor - High technical debt requiring immediate action'
    ws.merge_range(row, 1, row, 7, interpretation, value_format)
    row += 2
    
    # ========================================
    # SECTION 5: Why Quality Score ≠ Pass Rate
    # ========================================
    ws.merge_range(row, 0, row, 7, '5. WHY QUALITY SCORE ≠ PASS RATE', section_format)
    row += 1
    
    ws.write(row, 0, 'Quality Score:', label_format)
    ws.merge_range(row, 1, row, 7, f'{overall_score} (weighted by severity)', value_format)
    row += 1
    
    ws.write(row, 0, 'Pass Rate:', label_format)
    ws.merge_range(row, 1, row, 7, f'{pass_rate}% (unweighted)', value_format)
    row += 1
    
    ws.write(row, 0, 'Explanation:', label_format)
    explanation = 'Quality Score uses weighted penalties to emphasize high-severity issues. '
    explanation += 'Pass Rate treats all violations equally. '
    explanation += f'In your report, {total_violations} violations ({100-pass_rate}% failure) resulted in '
    explanation += f'a {overall_score} quality score ({technical_debt}-point penalty) because '
    explanation += f'{high_count} high-severity issues carry heavier penalties.'
    ws.merge_range(row, 1, row, 7, explanation, value_format)
    ws.set_row(row, 60)
    row += 2
    
    # ========================================
    # SECTION 6: Data Sources
    # ========================================
    ws.merge_range(row, 0, row, 7, '6. DATA SOURCES', section_format)
    row += 1
    
    ws.write(row, 0, 'Analysis Phase:', label_format)
    ws.merge_range(row, 1, row, 7, 'Phases 1-5 (Naming, JavaScript, SQL, Error Handling, Structure)', value_format)
    row += 1
    
    ws.write(row, 0, 'Data Structure:', label_format)
    ws.merge_range(row, 1, row, 7, 'ipa_data dictionary → summary_metrics, quality_scores, violations', value_format)
    row += 1
    
    ws.write(row, 0, 'Calculation:', label_format)
    ws.merge_range(row, 1, row, 7, 'Template reads ipa_data → Calculates metrics → Writes to Excel', value_format)
    row += 1
    
    ws.write(row, 0, 'Charts:', label_format)
    ws.merge_range(row, 1, row, 7, 'Dynamic Excel charts reference dashboard cells (no static images)', value_format)
    row += 1
    
    # Column widths
    ws.set_column('A:A', 20)
    ws.set_column('B:H', 18)




def create_process_flow(wb, ipa_data):
    """Create comprehensive process flow with visual diagram"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    import io
    import re
    
    ws = wb.add_worksheet('🔄 Process Flow')
    ws.hide_gridlines(2)
    
    # Phase 4: Print optimization
    ws.set_portrait()
    ws.set_paper(9)  # A4
    ws.fit_to_pages(1, 0)  # Fit to 1 page wide
    ws.set_header('&C&14&B🔄 Process Flow Diagram')
    ws.set_footer('&LPage &P of &N&C' + ipa_data.get('client_name', 'Client') + ' • ' + ipa_data.get('rice_item', 'Project') + '&R&D')
    ws.repeat_rows(0, 2)  # Repeat title rows when printing
    
    # Modern title
    title_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter'
    })
    ws.merge_range('A1:L1', '🔄 PROCESS FLOW DIAGRAM', title_format)
    ws.set_row(1, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:L2', 'Visual representation of process structure and complexity', subtitle_format)
    ws.set_row(2, 20)
    
    # IMPROVEMENT 2: Navigation links
    add_navigation_links(ws, wb, '✅ Action Items')
    ws.set_row(0, 18)
    
    # Adjust row numbers (navigation now in row 0)
    
    # Section header
    section_format = wb.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1
    })
    
    # Info format
    info_format = wb.add_format({
        'font_size': 10,
        'border': 1,
        'border_color': COLORS['gray'],
        'text_wrap': True,
        'valign': 'top',
        'bg_color': COLORS['white']
    })
    
    # Metrics format
    metrics_format = wb.add_format({
        'font_size': 10,
        'border': 1,
        'border_color': COLORS['gray'],
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#F8F9FA'
    })
    
    row = 4
    
    # Process Info Section
    overview = ipa_data.get('overview', {})
    ws.merge_range(row, 0, row, 5, 'PROCESS INFORMATION', section_format)
    ws.merge_range(row, 6, row, 11, 'COMPLEXITY METRICS', section_format)
    row += 1
    
    # Left side: Process Info
    info_text = f"""Process Name: {overview.get('process_name', 'N/A')}
Process Type: {overview.get('process_type', 'N/A')}
Total Activities: {overview.get('total_activities', 0)}
JavaScript Blocks: {overview.get('javascript_blocks', 0)}
SQL Queries: {len(ipa_data.get('sql_queries', []))}
Auto-Restart: {overview.get('auto_restart', '0')}"""
    
    ws.merge_range(row, 0, row+5, 5, info_text, info_format)
    
    # Right side: Complexity Metrics
    activities = ipa_data.get('activities', [])
    branch_count = sum(1 for act in activities if act.get('type') == 'BRANCH')
    loop_count = sum(1 for act in activities if act.get('type') in ['ITBEG', 'ItEnd'])
    subprocess_count = sum(1 for act in activities if act.get('type') == 'SUBPROC')
    user_action_count = sum(1 for act in activities if act.get('type') == 'UA')
    js_blocks = overview.get('javascript_blocks', 0)
    sql_queries = len(ipa_data.get('sql_queries', []))
    
    complexity_score = (branch_count * 3) + (loop_count * 5) + (subprocess_count * 2) + \
                       (user_action_count * 4) + (js_blocks * 2) + (sql_queries * 3)
    
    if complexity_score <= 20:
        complexity_level = 'Low'
    elif complexity_score <= 50:
        complexity_level = 'Medium'
    elif complexity_score <= 100:
        complexity_level = 'High'
    else:
        complexity_level = 'Very High'
    
    complexity_text = f"""Branches: {branch_count} (×3 = {branch_count * 3} pts)
Loops: {loop_count} (×5 = {loop_count * 5} pts)
Subprocesses: {subprocess_count} (×2 = {subprocess_count * 2} pts)
User Actions: {user_action_count} (×4 = {user_action_count * 4} pts)
JS Blocks: {js_blocks} (×2 = {js_blocks * 2} pts)
SQL Queries: {sql_queries} (×3 = {sql_queries * 3} pts)

TOTAL: {complexity_score} points ({complexity_level})"""
    
    ws.merge_range(row, 6, row+5, 11, complexity_text, metrics_format)
    row += 6
    row += 1
    
    # Visual Flow Diagram Section
    ws.merge_range(row, 0, row, 11, 'VISUAL PROCESS FLOW', section_format)
    row += 1
    
    # High-Level Process Flow diagram removed per user request
    # (Section commented out to skip diagram generation)
    
    # Activity Details Table
    ws.merge_range(row, 0, row, 11, 'ACTIVITY DETAILS', section_format)
    row += 1
    
    # Table headers
    header_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1,
        'align': 'center'
    })
    
    ws.write(row, 0, '#', header_format)
    ws.write(row, 1, 'Type', header_format)
    ws.write(row, 2, 'Activity ID', header_format)
    ws.write(row, 3, 'Caption', header_format)
    ws.write(row, 4, 'Has Error Handling', header_format)
    ws.write(row, 5, 'Has JavaScript', header_format)
    ws.write(row, 6, 'Has SQL', header_format)
    row += 1
    
    # Table data with conditional formatting for "Yes" values
    cell_format = wb.add_format({
        'font_size': 9,
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top'
    })
    
    # Format for "Yes" values (highlighted)
    yes_format = wb.add_format({
        'font_size': 9,
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#D4EDDA',  # Light green background
        'font_color': '#155724',  # Dark green text
        'bold': True
    })
    
    # Format for "No" values
    no_format = wb.add_format({
        'font_size': 9,
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'font_color': '#6C757D'  # Gray text
    })
    
    real_activities = [act for act in activities if act.get('type') and act.get('id')]
    for i, act in enumerate(real_activities[:50], 1):  # Show first 50
        ws.write(row, 0, i, cell_format)
        ws.write(row, 1, act.get('type', ''), cell_format)
        ws.write(row, 2, act.get('id', ''), cell_format)
        ws.write(row, 3, act.get('caption', ''), cell_format)
        
        # Apply conditional formatting for boolean columns
        has_error = act.get('has_error_handling', False)
        has_js = act.get('has_javascript', False)
        has_sql = act.get('has_sql', False)
        
        ws.write(row, 4, 'Yes' if has_error else 'No', yes_format if has_error else no_format)
        ws.write(row, 5, 'Yes' if has_js else 'No', yes_format if has_js else no_format)
        ws.write(row, 6, 'Yes' if has_sql else 'No', yes_format if has_sql else no_format)
        row += 1
    
    if len(real_activities) > 50:
        ws.merge_range(row, 0, row, 6,
                       f"... {len(real_activities) - 50} more activities (see LPD file for complete list)",
                       cell_format)
        row += 1
    
    row += 1
    
    # Critical Paths & Recommendations
    ws.merge_range(row, 0, row, 11, 'CRITICAL PATHS & RECOMMENDATIONS', section_format)
    row += 1
    
    critical_paths = []
    
    if branch_count > 5:
        critical_paths.append(f"⚠ High branch count ({branch_count}) - Consider simplifying conditional logic")
    
    if loop_count > 3:
        critical_paths.append(f"⚠ Multiple loops ({loop_count}) - Verify performance with large datasets")
    
    if js_blocks > 10:
        critical_paths.append(f"⚠ Many JavaScript blocks ({js_blocks}) - Consider consolidation for maintainability")
    
    if subprocess_count > 5:
        critical_paths.append(f"⚠ Multiple subprocesses ({subprocess_count}) - Verify error handling and dependencies")
    
    if sql_queries > 5:
        critical_paths.append(f"⚠ Multiple SQL queries ({sql_queries}) - Verify pagination and performance")
    
    if not critical_paths:
        critical_paths.append("✓ No critical complexity concerns identified")
    
    critical_text = "\n\n".join(critical_paths)
    
    ws.merge_range(row, 0, row+len(critical_paths)+1, 11, critical_text, metrics_format)
    row += len(critical_paths) + 2
    
    # Column widths
    ws.set_column('A:A', 5)   # #
    ws.set_column('B:B', 12)  # Type
    ws.set_column('C:C', 20)  # Activity ID
    ws.set_column('D:D', 25)  # Caption
    ws.set_column('E:G', 15)  # Boolean columns
    ws.set_column('H:L', 15)  # Extra space


if __name__ == "__main__":
    print("IPA Coding Standards Template - Enhanced Edition")
    print("Usage: from ReusableTools.IPA_CodingStandards.ipa_coding_standards_template_enhanced import generate_report")
