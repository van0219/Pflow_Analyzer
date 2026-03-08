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
    
    # Phase 4: Print optimization
    ws.set_landscape()
    ws.set_paper(9)  # A4
    ws.fit_to_pages(1, 0)  # Fit to 1 page wide
    ws.set_header('&C&14&B📊 IPA Coding Standards Dashboard')
    ws.set_footer('&LGenerated: &D &T&C&P of &N&R' + ipa_data.get('client_name', 'Client') + ' • ' + ipa_data.get('rice_item', 'Project'))
    ws.repeat_rows(0, 1)  # Repeat title rows when printing
    
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
    
    # Phase 3: Navigation links
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
    
    ws.set_row(2, 15)  # Spacer
    
    # KPI Cards Row - 4 cards in single row
    row = 3
    quality_scores = ipa_data.get('quality_scores', {})
    overall_score = quality_scores.get('overall', 0)
    overview = ipa_data.get('overview', {})
    process_count = overview.get('process_count', 0)
    activity_count = overview.get('activity_count', 0)
    
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

    # Calculate complexity for Card 4
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
    
    action_count = calculate_action_items_count(ipa_data)
    
    # Card 1: Overall Quality (Columns A-C)
    ws.merge_range(row, 0, row, 2, '🎯 OVERALL QUALITY', card_header)
    ws.merge_range(row+1, 0, row+2, 2, overall_score, card_value)
    ws.merge_range(row+3, 0, row+3, 2, 'Quality Score', card_label)
    
    # Card 2: Processes (Columns D-F)
    ws.merge_range(row, 3, row, 5, '📋 PROCESSES', card_header)
    ws.merge_range(row+1, 3, row+2, 5, process_count, card_value)
    ws.merge_range(row+3, 3, row+3, 5, f'{activity_count} Activities', card_label)
    
    # Card 3: Complexity (Columns G-I)
    ws.merge_range(row, 6, row, 8, '⚙️ COMPLEXITY', card_header)
    ws.merge_range(row+1, 6, row+2, 8, complexity_score, complexity_value_format)
    ws.merge_range(row+3, 6, row+3, 8, complexity_level, card_label)
    
    # Card 4: Action Items (Columns J-L)
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

    
    # Charts Section - Side by side layout
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
    
    charts_start_row = row
    
    # Left side: Radar Chart (Columns A-F)
    if quality_scores:
        chart_img = create_radar_chart(quality_scores)
        ws.insert_image(row, 0, 'radar_chart.png', {'image_data': chart_img, 'x_scale': 0.9, 'y_scale': 0.9})
    
    # Right side: Bar Chart (Columns G-L)
    if quality_scores:
        # Prepare data for chart (exclude 'overall' score)
        chart_categories = []
        chart_values = []
        for key, value in quality_scores.items():
            if key != 'overall':
                chart_categories.append(key.replace('_', ' ').title())
                chart_values.append(value)
        
        # Write data to hidden cells for chart
        data_start_row = row + 25
        for idx, (cat, val) in enumerate(zip(chart_categories, chart_values)):
            ws.write(data_start_row + idx, 6, cat)
            ws.write(data_start_row + idx, 7, val)
        
        # Create bar chart
        chart = wb.add_chart({'type': 'bar'})
        chart.add_series({
            'name': 'Quality Score',
            'categories': ['📊 Executive Dashboard', data_start_row, 6, data_start_row + len(chart_categories) - 1, 6],
            'values': ['📊 Executive Dashboard', data_start_row, 7, data_start_row + len(chart_categories) - 1, 7],
            'fill': {'color': COLORS['deep_blue']},
            'data_labels': {'value': True, 'position': 'outside_end'}
        })
        
        chart.set_title({'name': 'Quality Scores by Category', 'name_font': {'size': 12, 'bold': True}})
        chart.set_x_axis({'name': 'Score (0-100)', 'min': 0, 'max': 100})
        chart.set_y_axis({'name': 'Category'})
        chart.set_size({'width': 480, 'height': 360})
        chart.set_legend({'position': 'none'})
        
        ws.insert_chart(row, 6, chart)
    
    row += 20
    
    # Severity Breakdown Chart - Full width below
    ws.merge_range(row, 0, row, 11, '📊 SEVERITY BREAKDOWN', section_header)
    ws.set_row(row, 28)
    row += 1
    
    # Calculate severity counts
    all_violations = []
    for rec in ipa_data.get('recommendations', []):
        all_violations.append(rec.get('priority', 'Medium'))
    for section_name, issues in ipa_data.get('coding_standards', {}).items():
        for issue in issues:
            if len(issue) >= 6 and issue[5] != 'Pass':
                all_violations.append(issue[2] if len(issue) > 2 else 'Medium')
    
    severity_counts = {
        'Critical': all_violations.count('Critical'),
        'High': all_violations.count('High'),
        'Medium': all_violations.count('Medium'),
        'Low': all_violations.count('Low')
    }
    
    # Write severity data for chart (Columns A-B, hidden below)
    data_start_row = row + 20
    severity_labels = ['Critical', 'High', 'Medium', 'Low']
    severity_colors = [COLORS['red'], COLORS['amber'], '#FDD835', COLORS['green']]
    
    for idx, label in enumerate(severity_labels):
        ws.write(data_start_row + idx, 0, label)
        ws.write(data_start_row + idx, 1, severity_counts.get(label, 0))
    
    # Create pie chart for severity breakdown (Left side: Columns A-E)
    severity_chart = wb.add_chart({'type': 'pie'})
    severity_chart.add_series({
        'name': 'Violations by Severity',
        'categories': ['📊 Executive Dashboard', data_start_row, 0, data_start_row + 3, 0],
        'values': ['📊 Executive Dashboard', data_start_row, 1, data_start_row + 3, 1],
        'data_labels': {'value': True, 'category': True, 'position': 'best_fit'},
        'points': [
            {'fill': {'color': severity_colors[0]}},
            {'fill': {'color': severity_colors[1]}},
            {'fill': {'color': severity_colors[2]}},
            {'fill': {'color': severity_colors[3]}}
        ]
    })
    
    severity_chart.set_title({'name': 'Violations by Severity', 'name_font': {'size': 12, 'bold': True}})
    severity_chart.set_size({'width': 400, 'height': 300})
    severity_chart.set_legend({'position': 'right', 'font': {'size': 9}})
    
    ws.insert_chart(row, 0, severity_chart)
    
    # Key Findings (Right side: Columns F-L)
    findings_header = wb.add_format({
        'bold': True,
        'font_size': 12,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'align': 'left',
        'valign': 'vcenter',
        'border': 1
    })
    ws.merge_range(row, 6, row, 11, '🔍 KEY FINDINGS', findings_header)
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
    
    key_findings = ipa_data.get('key_findings', [])
    for finding in key_findings[:5]:
        # Handle both dict and string formats
        if isinstance(finding, dict):
            category = finding.get('category', '')
            status = finding.get('status', '')
            details = finding.get('finding', finding.get('details', ''))
        else:
            # String format - treat as details
            category = 'Finding'
            status = 'Info'
            details = str(finding)
        
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
        
        ws.write(row, 6, status, badge_format)
        ws.write(row, 7, category, wb.add_format({
            'bold': True,
            'font_size': 10,
            'bg_color': COLORS['white'],
            'border': 1,
            'border_color': COLORS['gray']
        }))
        ws.merge_range(row, 8, row, 11, details, finding_format)
        ws.set_row(row, 35)
        row += 1
    
    row += 15  # Space for pie chart
    
    ws.set_column('A:A', 12)
    ws.set_column('B:C', 15)
    ws.set_column('D:L', 12)



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
    
    # Phase 3: Back to Dashboard link
    back_format = wb.add_format({
        'font_size': 9,
        'align': 'left',
        'bg_color': COLORS['white'],
        'font_color': COLORS['deep_blue'],
        'underline': True
    })
    ws.write_url('A3', "internal:'📊 Executive Dashboard'!A1", back_format, string='← Back to Dashboard')
    ws.set_row(2, 18)
    
    # Headers
    row = 4  # Phase 3: Adjusted for navigation link
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
        ws.write(row, 14, 'Not Started', fmt)  # Phase 3: Status column with default value
        
        ws.set_row(row, 60)
        row += 1
    
    # Phase 3: Add AutoFilter to enable filtering
    if row > 4:
        ws.autofilter(3, 0, row - 1, 14)
    
    # Phase 3: Add data validation for Status column
    ws.data_validation(f'O4:O{row}', {
        'validate': 'list',
        'source': ['Not Started', 'In Progress', 'Complete', 'Blocked'],
        'input_title': 'Select Status',
        'input_message': 'Choose current status of this action item',
        'error_title': 'Invalid Status',
        'error_message': 'Please select a valid status from the dropdown'
    })
    
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
    ws.set_column('O:O', 12)  # Phase 3: Status column



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
    
    # Phase 3: Back to Dashboard link
    back_format = wb.add_format({
        'font_size': 9,
        'align': 'left',
        'bg_color': COLORS['white'],
        'font_color': COLORS['deep_blue'],
        'underline': True
    })
    ws.write_url('A3', "internal:'📊 Executive Dashboard'!A1", back_format, string='← Back to Dashboard')
    ws.set_row(2, 18)
    
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
            
            # Violation header with severity badge
            ws.write(row, 0, badge_text, badge_fmt)
            ws.merge_range(row, 1, row, 9, f"Violation {idx}: {violation.get('rule_name', 'N/A')}", subsection_format)
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
    ws.set_row(0, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:L2', 'Visual representation of process structure and complexity', subtitle_format)
    ws.set_row(1, 20)
    
    # Phase 3: Back to Dashboard link
    back_format = wb.add_format({
        'font_size': 9,
        'align': 'left',
        'bg_color': COLORS['white'],
        'font_color': COLORS['deep_blue'],
        'underline': True
    })
    ws.write_url('A3', "internal:'📊 Executive Dashboard'!A1", back_format, string='← Back to Dashboard')
    ws.set_row(2, 18)
    
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
    
    # Generate simplified high-level phase diagram
    try:
        # Filter real activities (exclude empty connectors)
        real_activities = [act for act in activities if act.get('type') and act.get('id')]
        
        # Try to load AI-generated flow phases JSON
        process_name = overview.get('process_name', 'Unknown')
        flow_phases_file = Path('Temp') / f"{process_name}_flow_phases.json"
        
        phases = []
        if flow_phases_file.exists():
            # Use AI-generated phases
            try:
                with open(flow_phases_file, 'r', encoding='utf-8') as f:
                    flow_data = json.load(f)
                    phases = flow_data.get('phases', [])
            except Exception as e:
                print(f"Warning: Could not load flow phases JSON: {e}")
                phases = []
        
        # Fallback to generic phases if JSON not found or empty
        if not phases:
            phases = [
                {'name': 'Start', 'color': '#28a745', 'activities': 1, 'description': 'Process initialization'},
                {'name': 'Processing', 'color': '#17a2b8', 'activities': len(real_activities) - 2, 'description': 'Main process logic'},
                {'name': 'End', 'color': '#dc3545', 'activities': 1, 'description': 'Process completion'}
            ]
        
        # Create horizontal swimlane diagram
        fig, ax = plt.subplots(figsize=(14, max(6, len(phases) * 1.2)))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, max(6, len(phases) * 1.2))
        ax.axis('off')
        
        # Draw phases as horizontal boxes
        y_pos = max(5.5, len(phases) * 1.1)
        x_start = 1
        box_width = 11
        box_height = 0.8
        
        for i, phase in enumerate(phases):
            # Draw phase box
            box = mpatches.FancyBboxPatch((x_start, y_pos - box_height/2), box_width, box_height,
                                          boxstyle="round,pad=0.05",
                                          facecolor=phase['color'],
                                          edgecolor='black',
                                          linewidth=2,
                                          alpha=0.8)
            ax.add_patch(box)
            
            # Add phase name (left side)
            ax.text(x_start + 0.3, y_pos, phase['name'],
                   ha='left', va='center', fontsize=12, weight='bold',
                   color='white')
            
            # Add activity count (right side)
            ax.text(x_start + box_width - 0.3, y_pos, f"{phase['activities']} activities",
                   ha='right', va='center', fontsize=9,
                   color='white', style='italic')
            
            # Add description below box
            ax.text(x_start + box_width/2, y_pos - box_height/2 - 0.15, phase['description'],
                   ha='center', va='top', fontsize=8,
                   color='#495057', style='italic')
            
            # Draw arrow to next phase
            if i < len(phases) - 1:
                arrow = FancyArrowPatch((x_start + box_width/2, y_pos - box_height/2 - 0.3),
                                       (x_start + box_width/2, y_pos - box_height/2 - 0.7),
                                       arrowstyle='->', mutation_scale=20,
                                       color='#495057', linewidth=2)
                ax.add_patch(arrow)
            
            y_pos -= 1.2
        
        # Add title
        ax.text(7, max(6.5, len(phases) * 1.2 + 0.5), 'High-Level Process Flow',
               ha='center', va='top', fontsize=16, weight='bold',
               color='#212529')
        
        # Add branch/loop indicators if present
        if branch_count > 0 or loop_count > 0:
            indicators_y = 0.5
            indicators_text = []
            if branch_count > 0:
                indicators_text.append(f"Decision Points: {branch_count}")
            if loop_count > 0:
                indicators_text.append(f"Loops: {loop_count}")
            
            ax.text(7, indicators_y, " | ".join(indicators_text),
                   ha='center', va='center', fontsize=10,
                   color='#6c757d', style='italic',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#dee2e6'))
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        plt.close()
        
        # Insert image into Excel
        ws.insert_image(row, 0, 'flowchart.png',
                       {'image_data': img_buffer, 'x_scale': 0.8, 'y_scale': 0.8})
        
        # Reserve space for image (adjust based on phase count)
        row += max(25, len(phases) * 4 + 5)
        
    except Exception as e:
        # Fallback to text if diagram fails
        error_format = wb.add_format({
            'font_size': 10,
            'font_color': COLORS['red'],
            'italic': True
        })
        ws.merge_range(row, 0, row, 11,
                       f"Visual diagram generation failed: {str(e)}\nFalling back to text representation.",
                       error_format)
        row += 2
    
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
    
    # Table data
    cell_format = wb.add_format({
        'font_size': 9,
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top'
    })
    
    real_activities = [act for act in activities if act.get('type') and act.get('id')]
    for i, act in enumerate(real_activities[:50], 1):  # Show first 50
        ws.write(row, 0, i, cell_format)
        ws.write(row, 1, act.get('type', ''), cell_format)
        ws.write(row, 2, act.get('id', ''), cell_format)
        ws.write(row, 3, act.get('caption', ''), cell_format)
        ws.write(row, 4, 'Yes' if act.get('has_error_handling') else 'No', cell_format)
        ws.write(row, 5, 'Yes' if act.get('has_javascript') else 'No', cell_format)
        ws.write(row, 6, 'Yes' if act.get('has_sql') else 'No', cell_format)
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
