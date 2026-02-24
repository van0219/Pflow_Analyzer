#!/usr/bin/env python3
"""
IPA Coding Standards Template - Enhanced Edition with Subagent Analysis

Professional Excel reports with enhanced analysis from specialized subagents:
- Impact analysis (frequency, affected %, maintainability, fix time)
- Code examples (before/after with explanations)
- Testing notes (testing requirements, deployment considerations)
- Priority scores (0-100 objective scoring)
- Process flow visualization

4 Sheets:
1. Executive Dashboard - Visual KPIs and quality metrics
2. Action Items - Enhanced developer checklist with impact analysis
3. Detailed Analysis - Comprehensive analysis with code examples
4. Process Flow - Text-based flow diagram with complexity metrics

Updated: 2026-02-22 - Enhanced with subagent analysis fields
"""

import xlsxwriter
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np


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
            activity = ', '.join(activities) if activities else ipa_data.get('overview', {}).get('process_name', '')
        else:
            activity = activities if activities else ipa_data.get('overview', {}).get('process_name', '')
        
        issue_text = rec.get('issue', '')
        key = (activity.lower().strip(), issue_text.lower().strip())
        
        if key not in seen_items:
            count += 1
            seen_items.add(key)
    
    # Count coding standards violations (status != Pass)
    for section_name, issues in ipa_data.get('coding_standards', {}).items():
        for issue in issues:
            if len(issue) >= 7:
                status = issue[5] if len(issue) > 5 else 'Needs Improvement'
                activity = issue[0] if len(issue) > 0 else ''
                issue_text = issue[3] if len(issue) > 3 else ''
                key = (activity.lower().strip(), issue_text.lower().strip())
                
                if status != 'Pass' and key not in seen_items:
                    count += 1
                    seen_items.add(key)
    
    return count


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
    create_action_items_enhanced(workbook, ipa_data)
    create_detailed_analysis_enhanced(workbook, ipa_data)
    create_process_flow(workbook, ipa_data)
    
    workbook.close()
    return output_path



def create_radar_chart(quality_scores):
    """Create modern radar chart for quality scores"""
    categories = [k.replace('_', ' ').title() for k in quality_scores.keys() if k != 'overall']
    values = [v for k, v in quality_scores.items() if k != 'overall']
    
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    values_plot = values + values[:1]
    angles_plot = angles + angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')
    
    ax.plot(angles_plot, values_plot, 'o-', linewidth=3, color=COLORS['deep_blue'], label='Current')
    ax.fill(angles_plot, values_plot, alpha=0.25, color=COLORS['deep_blue'])
    
    target = [100] * (N + 1)
    ax.plot(angles_plot, target, '--', linewidth=2, color=COLORS['green'], alpha=0.5, label='Target')
    
    ax.set_ylim(0, 100)
    ax.set_xticks(angles)
    ax.set_xticklabels(categories, size=9)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], size=8, color='gray')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=9)
    
    plt.title('Quality Metrics', size=12, weight='bold', pad=15)
    
    img_data = BytesIO()
    plt.savefig(img_data, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    img_data.seek(0)
    plt.close()
    
    return img_data


def create_executive_dashboard(wb, ipa_data):
    """Create modern executive dashboard with visual KPIs (reused from original)"""
    ws = wb.add_worksheet('📊 Executive Dashboard')
    ws.hide_gridlines(2)
    
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
    
    ws.set_row(2, 15)  # Spacer
    
    # KPI Cards Row
    row = 3
    quality_scores = ipa_data.get('quality_scores', {})
    overall_score = quality_scores.get('overall', 0)
    
    # Card formats
    card_header = wb.add_format({
        'bold': True,
        'font_size': 11,
        'bg_color': COLORS['deep_blue'],
        'font_color': 'white',
        'align': 'center',
        'border': 1,
        'border_color': COLORS['gray']
    })
    card_value = wb.add_format({
        'bold': True,
        'font_size': 36,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': COLORS['white'],
        'font_color': COLORS['green'] if overall_score >= 90 else COLORS['amber'] if overall_score >= 70 else COLORS['red']
    })
    card_label = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['white'],
        'font_color': COLORS['dark_gray'],
        'border': 1,
        'border_color': COLORS['gray']
    })

    
    # Card 1: Overall Score
    ws.merge_range(row, 0, row, 2, '🎯 OVERALL QUALITY', card_header)
    ws.merge_range(row+1, 0, row+2, 2, overall_score, card_value)
    ws.merge_range(row+3, 0, row+3, 2, 'Quality Score', card_label)
    
    # Card 2: Process Count
    overview = ipa_data.get('overview', {})
    process_count = overview.get('process_count', 0)
    activity_count = overview.get('activity_count', 0)
    
    ws.merge_range(row, 3, row, 5, '📋 PROCESSES', card_header)
    ws.merge_range(row+1, 3, row+2, 5, process_count, card_value)
    ws.merge_range(row+3, 3, row+3, 5, f'{activity_count} Activities', card_label)
    
    # Card 3: Complexity Score
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
        complexity_color = COLORS['green']
    elif complexity_score <= 50:
        complexity_level = 'Medium'
        complexity_color = COLORS['amber']
    elif complexity_score <= 100:
        complexity_level = 'High'
        complexity_color = COLORS['amber']
    else:
        complexity_level = 'Very High'
        complexity_color = COLORS['red']
    
    complexity_value_format = wb.add_format({
        'bold': True,
        'font_size': 36,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': COLORS['white'],
        'font_color': complexity_color
    })
    
    ws.merge_range(row, 6, row, 8, '⚙️ COMPLEXITY', card_header)
    ws.merge_range(row+1, 6, row+2, 8, complexity_score, complexity_value_format)
    ws.merge_range(row+3, 6, row+3, 8, complexity_level, card_label)
    
    # Card 4: Action Items
    action_count = calculate_action_items_count(ipa_data)
    
    ws.merge_range(row, 9, row, 11, '✅ ACTION ITEMS', card_header)
    ws.merge_range(row+1, 9, row+2, 11, action_count, card_value)
    ws.merge_range(row+3, 9, row+3, 11, 'Items to Address', card_label)
    
    ws.set_row(row, 25)
    ws.set_row(row+1, 35)
    ws.set_row(row+2, 35)
    ws.set_row(row+3, 22)
    
    row += 5
    ws.set_row(row, 15)
    row += 1

    
    # Charts Section
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
    
    ws.merge_range(row, 0, row, 11, '📈 QUALITY METRICS VISUALIZATION', section_header)
    ws.set_row(row, 28)
    row += 1
    
    if quality_scores:
        chart_img = create_radar_chart(quality_scores)
        ws.insert_image(row, 0, 'radar_chart.png', {'image_data': chart_img, 'x_scale': 1.0, 'y_scale': 1.0})
    
    row += 25
    ws.merge_range(row, 0, row, 11, '🔍 KEY FINDINGS', section_header)
    ws.set_row(row, 28)
    row += 1
    
    finding_format = wb.add_format({
        'font_size': 10,
        'text_wrap': True,
        'valign': 'top',
        'bg_color': COLORS['white'],
        'border': 1,
        'border_color': COLORS['gray']
    })
    
    key_findings = ipa_data.get('key_findings', [])
    for finding in key_findings[:5]:
        category = finding.get('category', '')
        status = finding.get('status', '')
        details = finding.get('details', '')
        
        if status in ['Pass', 'Excellent', 'Good']:
            badge_color = COLORS['green']
        elif status in ['Verify', 'Needs Improvement']:
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
        
        ws.write(row, 0, status, badge_format)
        ws.merge_range(row, 1, row, 2, category, wb.add_format({
            'bold': True,
            'font_size': 10,
            'bg_color': COLORS['white'],
            'border': 1,
            'border_color': COLORS['gray']
        }))
        ws.merge_range(row, 3, row, 11, details, finding_format)
        ws.set_row(row, 35)
        row += 1
    
    ws.set_column('A:A', 12)
    ws.set_column('B:C', 15)
    ws.set_column('D:L', 12)



def create_action_items_enhanced(wb, ipa_data):
    """Create enhanced action items sheet with impact analysis and code examples"""
    ws = wb.add_worksheet('✅ Action Items')
    ws.hide_gridlines(2)
    
    # Modern title
    title_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter'
    })
    ws.merge_range('A1:N1', '✅ ACTION ITEMS - ENHANCED DEVELOPER CHECKLIST', title_format)
    ws.set_row(0, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:N2', 'Items with impact analysis, code examples, and testing guidance', subtitle_format)
    ws.set_row(1, 20)
    
    # Header format
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
    headers = [
        'Priority', 'Category', 'Rule ID', 'Activity', 'Issue', 'Current', 
        'Recommendation', 'Effort', 'Impact', 'Priority\nScore', 'Est. Fix\nTime', 
        'Affected\n%', 'Code Example', 'Testing Notes'
    ]
    for col, header in enumerate(headers):
        ws.write(row, col, header, header_format)
    ws.set_row(row, 30)
    
    row += 1
    
    # Collect all issues
    all_issues = []
    seen_items = set()
    
    # Add recommendations
    for rec in ipa_data.get('recommendations', []):
        activities = rec.get('activities', '')
        if isinstance(activities, list):
            activity = ', '.join(activities) if activities else ipa_data.get('overview', {}).get('process_name', '')
        else:
            activity = activities if activities else ipa_data.get('overview', {}).get('process_name', '')
        
        issue_text = rec.get('issue', '')
        key = (activity.lower().strip(), issue_text.lower().strip())
        
        if key not in seen_items:
            all_issues.append({
                'priority': rec.get('priority', 'Medium'),
                'category': rec.get('category', 'General'),
                'rule_id': rec.get('rule_id', 'AI Analysis'),
                'activity': activity,
                'issue': issue_text,
                'current': rec.get('current', ''),
                'recommendation': rec.get('recommendation', ''),
                'effort': rec.get('effort', 'Medium'),
                'impact': rec.get('impact', 'Medium'),
                'priority_score': rec.get('priority_score', 50),
                'estimated_fix_time': rec.get('estimated_fix_time', 'TBD'),
                'affected_percentage': rec.get('affected_percentage', 0),
                'code_example': rec.get('code_example', ''),
                'testing_notes': rec.get('testing_notes', ''),
                'status': rec.get('status', 'Needs Improvement')
            })
            seen_items.add(key)

    
    # Add coding standards violations
    import re
    for section_name, issues in ipa_data.get('coding_standards', {}).items():
        for issue in issues:
            if len(issue) >= 7:
                status = issue[5] if len(issue) > 5 else 'Needs Improvement'
                category = section_name.replace('_', ' ').title()
                activity = issue[0] if len(issue) > 0 else ''
                issue_text = issue[3] if len(issue) > 3 else ''
                key = (activity.lower().strip(), issue_text.lower().strip())
                
                if status in ['Verify', 'Needs Improvement'] and key not in seen_items:
                    rule_name = issue[1] if len(issue) > 1 else ''
                    rule_id_match = re.search(r'\(([A-Z]+\s+[\d.]+)\)', rule_name)
                    rule_id = rule_id_match.group(1) if rule_id_match else 'Best Practice'
                    
                    all_issues.append({
                        'priority': issue[2] if len(issue) > 2 else 'Medium',
                        'category': category,
                        'rule_id': rule_id,
                        'activity': activity,
                        'issue': issue_text,
                        'current': issue[4] if len(issue) > 4 else '',
                        'recommendation': issue[6] if len(issue) > 6 else '',
                        'effort': 'Low',
                        'impact': 'Medium',
                        'priority_score': 50,
                        'estimated_fix_time': 'TBD',
                        'affected_percentage': 0,
                        'code_example': '',
                        'testing_notes': '',
                        'status': status
                    })
                    seen_items.add(key)
    
    # Sort by priority score (descending)
    all_issues.sort(key=lambda x: x.get('priority_score', 50), reverse=True)
    
    # Write issues
    for issue in all_issues:
        severity = issue['priority']
        fmt = critical_format if severity == 'Critical' else high_format if severity == 'High' else medium_format if severity == 'Medium' else cell_format
        
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
        
        ws.write(row, 0, issue['priority'], fmt)
        ws.write(row, 1, issue['category'], fmt)
        ws.write(row, 2, issue['rule_id'], fmt)
        ws.write(row, 3, issue['activity'], fmt)
        ws.write(row, 4, issue['issue'], fmt)
        ws.write(row, 5, issue['current'], fmt)
        ws.write(row, 6, issue['recommendation'], fmt)
        ws.write(row, 7, issue['effort'], fmt)
        ws.write(row, 8, issue['impact'], fmt)
        ws.write(row, 9, priority_score, fmt)
        ws.write(row, 10, estimated_fix_time, fmt)
        ws.write(row, 11, f"{affected_percentage}%" if affected_percentage > 0 else 'N/A', fmt)
        ws.write(row, 12, code_example, fmt)
        ws.write(row, 13, testing_notes, fmt)
        
        ws.set_row(row, 60)
        row += 1
    
    # Column widths
    ws.set_column('A:A', 8)
    ws.set_column('B:B', 18)
    ws.set_column('C:C', 10)
    ws.set_column('D:D', 20)
    ws.set_column('E:E', 25)
    ws.set_column('F:F', 20)
    ws.set_column('G:G', 30)
    ws.set_column('H:H', 8)
    ws.set_column('I:I', 8)
    ws.set_column('J:J', 8)
    ws.set_column('K:K', 10)
    ws.set_column('L:L', 8)
    ws.set_column('M:M', 25)
    ws.set_column('N:N', 25)



def create_detailed_analysis_enhanced(wb, ipa_data):
    """Create enhanced detailed analysis sheet with impact analysis and code examples"""
    ws = wb.add_worksheet('📐 Detailed Analysis')
    ws.hide_gridlines(2)
    
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
    ws.set_row(0, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:J2', 'Comprehensive technical analysis with code examples and testing guidance', subtitle_format)
    ws.set_row(1, 20)
    
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
            # Violation header
            ws.merge_range(row, 0, row, 9, f"Violation {idx}: {violation.get('rule_name', 'N/A')}", subsection_format)
            row += 1
            
            # Basic info
            ws.write(row, 0, 'Activity:', label_format)
            ws.merge_range(row, 1, row, 9, violation.get('activities', 'N/A'), value_format)
            row += 1
            
            ws.write(row, 0, 'Finding:', label_format)
            ws.merge_range(row, 1, row, 9, violation.get('finding', 'N/A'), value_format)
            row += 1
            
            ws.write(row, 0, 'Current:', label_format)
            ws.merge_range(row, 1, row, 9, violation.get('current', 'N/A'), value_format)
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



def create_process_flow(wb, ipa_data):
    """Create text-based process flow diagram with complexity metrics"""
    ws = wb.add_worksheet('🔄 Process Flow')
    ws.hide_gridlines(2)
    
    # Modern title
    title_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter'
    })
    ws.merge_range('A1:H1', '🔄 PROCESS FLOW DIAGRAM', title_format)
    ws.set_row(0, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:H2', 'Visual representation of process structure and complexity', subtitle_format)
    ws.set_row(1, 20)
    
    # Section header
    section_format = wb.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1
    })
    
    # Flow text format
    flow_format = wb.add_format({
        'font_name': 'Consolas',
        'font_size': 10,
        'border': 1,
        'border_color': COLORS['gray'],
        'text_wrap': False,
        'valign': 'top'
    })
    
    # Metrics format
    metrics_format = wb.add_format({
        'font_size': 10,
        'border': 1,
        'border_color': COLORS['gray'],
        'text_wrap': True,
        'valign': 'top'
    })
    
    row = 3
    
    # Process Info
    overview = ipa_data.get('overview', {})
    ws.merge_range(row, 0, row, 7, 'PROCESS INFORMATION', section_format)
    row += 1
    
    info_text = f"""Process: {overview.get('process_name', 'N/A')}
Type: {overview.get('process_type', 'N/A')}
Activities: {overview.get('total_activities', 0)}
JavaScript Blocks: {overview.get('javascript_blocks', 0)}
SQL Queries: {len(ipa_data.get('sql_queries', []))}"""
    
    ws.merge_range(row, 0, row+4, 7, info_text, metrics_format)
    row += 5
    row += 1
    
    # Complexity Breakdown
    ws.merge_range(row, 0, row, 7, 'COMPLEXITY BREAKDOWN', section_format)
    row += 1
    
    activities = ipa_data.get('activities', [])
    branch_count = sum(1 for act in activities if act.get('type') == 'BRANCH')
    loop_count = sum(1 for act in activities if act.get('type') in ['ITBEG', 'ItEnd'])
    subprocess_count = sum(1 for act in activities if act.get('type') == 'SUBPROC')
    user_action_count = sum(1 for act in activities if act.get('type') == 'UA')
    js_blocks = overview.get('javascript_blocks', 0)
    sql_queries = len(ipa_data.get('sql_queries', []))
    
    complexity_score = (branch_count * 3) + (loop_count * 5) + (subprocess_count * 2) + \
                       (user_action_count * 4) + (js_blocks * 2) + (sql_queries * 3)
    
    complexity_text = f"""Branches: {branch_count} (×3 = {branch_count * 3} points)
Loops: {loop_count} (×5 = {loop_count * 5} points)
Subprocesses: {subprocess_count} (×2 = {subprocess_count * 2} points)
User Actions: {user_action_count} (×4 = {user_action_count * 4} points)
JavaScript Blocks: {js_blocks} (×2 = {js_blocks * 2} points)
SQL Queries: {sql_queries} (×3 = {sql_queries * 3} points)

TOTAL COMPLEXITY: {complexity_score} points"""
    
    if complexity_score <= 20:
        complexity_level = 'Low'
    elif complexity_score <= 50:
        complexity_level = 'Medium'
    elif complexity_score <= 100:
        complexity_level = 'High'
    else:
        complexity_level = 'Very High'
    
    complexity_text += f"\nLevel: {complexity_level}"
    
    ws.merge_range(row, 0, row+8, 7, complexity_text, metrics_format)
    row += 9
    row += 1

    
    # Activity Flow
    ws.merge_range(row, 0, row, 7, 'ACTIVITY FLOW', section_format)
    row += 1
    
    # Build simplified flow diagram
    flow_lines = []
    flow_lines.append("PROCESS FLOW:")
    flow_lines.append("=" * 50)
    flow_lines.append("")
    
    # Group activities by type for summary
    activity_types = {}
    for act in activities[:20]:  # Show first 20 activities
        act_type = act.get('type', 'UNKNOWN')
        caption = act.get('caption', act.get('id', 'N/A'))
        
        if act_type == 'START':
            flow_lines.append("├─ START")
        elif act_type == 'BRANCH':
            flow_lines.append(f"├─ BRANCH: {caption}")
        elif act_type == 'ITBEG':
            flow_lines.append(f"├─ LOOP START: {caption}")
        elif act_type == 'ItEnd':
            flow_lines.append(f"│  └─ LOOP END")
        elif act_type == 'SUBPROC':
            flow_lines.append(f"├─ SUBPROCESS: {caption}")
        elif act_type == 'UA':
            flow_lines.append(f"├─ USER ACTION: {caption}")
        elif act_type == 'SCRIPT':
            flow_lines.append(f"├─ JAVASCRIPT: {caption}")
        elif act_type == 'SQL':
            flow_lines.append(f"├─ SQL QUERY: {caption}")
        elif act_type == 'END':
            flow_lines.append("└─ END")
        else:
            flow_lines.append(f"├─ {act_type}: {caption}")
    
    if len(activities) > 20:
        flow_lines.append(f"... ({len(activities) - 20} more activities)")
    
    flow_text = "\n".join(flow_lines)
    
    # Calculate row height based on number of lines
    num_lines = len(flow_lines)
    ws.merge_range(row, 0, row+num_lines-1, 7, flow_text, flow_format)
    row += num_lines
    row += 1
    
    # Critical Paths
    ws.merge_range(row, 0, row, 7, 'CRITICAL PATHS & RECOMMENDATIONS', section_format)
    row += 1
    
    critical_paths = []
    
    if branch_count > 5:
        critical_paths.append(f"⚠ High branch count ({branch_count}) - Consider simplifying logic")
    
    if loop_count > 3:
        critical_paths.append(f"⚠ Multiple loops ({loop_count}) - Verify performance with large datasets")
    
    if js_blocks > 10:
        critical_paths.append(f"⚠ Many JavaScript blocks ({js_blocks}) - Consider consolidation")
    
    if subprocess_count > 5:
        critical_paths.append(f"⚠ Multiple subprocesses ({subprocess_count}) - Verify error handling")
    
    if not critical_paths:
        critical_paths.append("✓ No critical complexity concerns identified")
    
    critical_text = "\n\n".join(critical_paths)
    
    ws.merge_range(row, 0, row+len(critical_paths), 7, critical_text, metrics_format)
    row += len(critical_paths) + 1
    
    # Column widths
    ws.set_column('A:H', 25)


if __name__ == "__main__":
    print("IPA Coding Standards Template - Enhanced Edition")
    print("Usage: from ReusableTools.IPA_CodingStandards.ipa_coding_standards_template_enhanced import generate_report")
