#!/usr/bin/env python3
"""
IPA Coding Standards Template - matplotlib chart edition

Professional Excel reports with matplotlib chart images:
- Matplotlib charts rendered as PNG images
- Guaranteed visibility (no Excel chart rendering issues)
- Modern color schemes and formatting
- Professional typography
- Dashboard-style layouts

3 Sheets:
1. Summary & Guide - Compliance scorecard with chart, severity breakdown
2. Action Items - Developer checklist (placeholder)
3. Detailed Analysis - Comprehensive analysis (placeholder)

Updated: 2026-02-07 - Using matplotlib for reliable chart rendering
"""

import xlsxwriter
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np


def calculate_row_height(text, column_width=80, base_height=15):
    """
    Calculate row height based on text length and column width.
    
    Args:
        text: The text content
        column_width: Width of the column in characters (default 80)
        base_height: Base height per line (default 15)
    
    Returns:
        Calculated row height
    """
    if not text:
        return base_height
    
    # Convert to string if not already
    text = str(text)
    
    # Estimate number of lines based on text length and column width
    # Average character width is ~1.2 units in Excel
    chars_per_line = column_width
    estimated_lines = max(1, len(text) / chars_per_line)
    
    # Add extra lines for newlines in text
    newline_count = text.count('\n')
    estimated_lines += newline_count
    
    # Calculate height (minimum 15, maximum 409 which is Excel's max)
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
    """
    Calculate the actual number of action items (same logic as Action Items sheet).
    Counts recommendations + coding standards violations (excluding Pass status).
    Deduplicates by (activity, issue) key.
    """
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
    """Generate modern 2026-style 3-sheet coding standards report"""
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
    create_executive_dashboard(workbook, ipa_data)  # Modern visual dashboard
    create_action_items(workbook, ipa_data)
    create_detailed_analysis(workbook, ipa_data)
    
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
    """Create modern executive dashboard with visual KPIs"""
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
    # Calculate complexity based on process characteristics
    activities = ipa_data.get('activities', [])
    branch_count = sum(1 for act in activities if act.get('type') == 'BRANCH')
    loop_count = sum(1 for act in activities if act.get('type') in ['ITBEG', 'ItEnd'])  # Iterator loops
    subprocess_count = sum(1 for act in activities if act.get('type') == 'SUBPROC')
    user_action_count = sum(1 for act in activities if act.get('type') == 'UA')
    js_blocks = overview.get('javascript_blocks', 0)
    sql_queries = len(ipa_data.get('sql_queries', []))
    
    # Complexity formula
    complexity_score = (branch_count * 3) + (loop_count * 5) + (subprocess_count * 2) + \
                       (user_action_count * 4) + (js_blocks * 2) + (sql_queries * 3)
    
    # Determine complexity level and color
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
    
    # Card 4: Action Items (count ALL action items, not just recommendations)
    action_count = calculate_action_items_count(ipa_data)
    
    ws.merge_range(row, 9, row, 11, '✅ ACTION ITEMS', card_header)
    ws.merge_range(row+1, 9, row+2, 11, action_count, card_value)
    ws.merge_range(row+3, 9, row+3, 11, 'Items to Address', card_label)
    
    ws.set_row(row, 25)
    ws.set_row(row+1, 35)
    ws.set_row(row+2, 35)
    ws.set_row(row+3, 22)
    
    # Spacer
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
    
    # Insert radar chart
    if quality_scores:
        chart_img = create_radar_chart(quality_scores)
        ws.insert_image(row, 0, 'radar_chart.png', {'image_data': chart_img, 'x_scale': 1.0, 'y_scale': 1.0})
    
    # Key Findings Section
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
    for finding in key_findings[:5]:  # Top 5 findings
        category = finding.get('category', '')
        status = finding.get('status', '')
        details = finding.get('details', '')
        
        # Status badge color
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
    
    # Column widths
    ws.set_column('A:A', 12)
    ws.set_column('B:C', 15)
    ws.set_column('D:L', 12)


def create_summary_and_guide(wb, ipa_data):
    """Create professional dashboard-style summary"""
    ws = wb.add_worksheet('📋 Summary & Guide')
    
    # Hide gridlines for cleaner look
    ws.hide_gridlines(2)
    
    # Title section with gradient effect
    hero_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'center',
        'valign': 'vcenter',
        'border': 0
    })
    ws.merge_range('A1:L1', 'IPA CODING STANDARDS REVIEW', hero_format)
    ws.set_row(0, 35)
    
    # Subtitle with metadata
    client = ipa_data.get('client_name', 'Client')
    rice_item = ipa_data.get('rice_item', 'Project')
    process_name = ipa_data.get('overview', {}).get('process_name', 'N/A')
    
    subtitle_format = wb.add_format({
        'font_size': 10,
        'font_color': '#666666',
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'border': 0
    })
    ws.merge_range('A2:L2', f"{client} • {rice_item} • {process_name} | {datetime.now().strftime('%B %d, %Y')}", subtitle_format)
    ws.set_row(1, 20)
    
    # Spacer
    ws.set_row(2, 10)
    
    # === KEY METRICS CARDS ===
    row = 3
    
    # Card styling
    card_title_format = wb.add_format({
        'bold': True,
        'font_size': 10,
        'font_color': '#666666',
        'align': 'center',
        'valign': 'vcenter',
        'top': 2,
        'left': 2,
        'right': 2,
        'top_color': COLORS['deep_blue'],
        'left_color': COLORS['deep_blue'],
        'right_color': COLORS['deep_blue']
    })
    
    overall_score = ipa_data.get('quality_scores', {}).get('overall', 85)
    score_color = COLORS['green'] if overall_score >= 90 else COLORS['amber'] if overall_score >= 70 else COLORS['red']
    
    # Card 1: Overall Score
    ws.merge_range(row, 0, row, 3, 'OVERALL QUALITY', card_title_format)
    
    score_value_format = wb.add_format({
        'bold': True,
        'font_size': 48,
        'font_color': score_color,
        'align': 'center',
        'valign': 'vcenter',
        'left': 2,
        'right': 2,
        'bottom': 2,
        'left_color': COLORS['deep_blue'],
        'right_color': COLORS['deep_blue'],
        'bottom_color': COLORS['deep_blue']
    })
    ws.merge_range(row + 1, 0, row + 2, 3, overall_score, score_value_format)
    
    # Card 2: Total Issues
    ws.merge_range(row, 4, row, 7, 'ISSUES FOUND', card_title_format)
    
    # Count all actionable issues (JS violations + non-passing coding standards + recommendations)
    js_issues = ipa_data.get('javascript_issues', [])
    coding_standards_issues = sum(1 for items in ipa_data.get('coding_standards', {}).values() 
                                   for item in items if len(item) > 5 and item[5] != 'Pass')
    recommendations = ipa_data.get('recommendations', [])
    
    # Total = JS issues + coding standards issues + recommendations (avoiding double-counting)
    total_issues = len(js_issues) + coding_standards_issues + len(recommendations)
    
    issues_value_format = wb.add_format({
        'bold': True,
        'font_size': 48,
        'font_color': COLORS['amber'] if total_issues > 0 else COLORS['green'],
        'align': 'center',
        'valign': 'vcenter',
        'left': 2,
        'right': 2,
        'bottom': 2,
        'left_color': COLORS['deep_blue'],
        'right_color': COLORS['deep_blue'],
        'bottom_color': COLORS['deep_blue']
    })
    ws.merge_range(row + 1, 4, row + 2, 7, total_issues, issues_value_format)
    
    # Card 3: Status
    ws.merge_range(row, 8, row, 11, 'COMPLIANCE STATUS', card_title_format)
    
    status = 'PASS' if overall_score >= 80 else 'REVIEW'
    status_icon = '✓' if overall_score >= 80 else '⚠'
    
    status_value_format = wb.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': 'white',
        'bg_color': COLORS['green'] if overall_score >= 80 else COLORS['amber'],
        'align': 'center',
        'valign': 'vcenter',
        'left': 2,
        'right': 2,
        'bottom': 2,
        'left_color': COLORS['deep_blue'],
        'right_color': COLORS['deep_blue'],
        'bottom_color': COLORS['deep_blue']
    })
    ws.merge_range(row + 1, 8, row + 2, 11, f"{status_icon} {status}", status_value_format)
    
    ws.set_row(row, 18)
    ws.set_row(row + 1, 35)
    ws.set_row(row + 2, 35)
    
    row += 4
    ws.set_row(row, 10)  # Spacer
    row += 1
    
    # === QUALITY BREAKDOWN CHART ===
    section_header = wb.add_format({
        'bold': True,
        'font_size': 14,
        'font_color': 'white',
        'bg_color': COLORS['deep_blue'],
        'align': 'left',
        'valign': 'vcenter',
        'left': 2,
        'right': 2,
        'top': 2,
        'bottom': 2,
        'left_color': COLORS['deep_blue'],
        'right_color': COLORS['deep_blue'],
        'top_color': COLORS['deep_blue'],
        'bottom_color': COLORS['deep_blue']
    })
    ws.merge_range(row, 0, row, 11, '  📊 QUALITY BREAKDOWN BY SECTION', section_header)
    ws.set_row(row, 25)
    row += 1
    
    chart_start_row = row
    
    # Create matplotlib chart with modern styling
    quality_scores = ipa_data.get('quality_scores', {})
    sections = [
        ('JavaScript ES5', quality_scores.get('javascript_es5', 100)),
        ('1.1 Naming', quality_scores.get('naming_convention', 100)),
        ('1.2 IPA Rules', quality_scores.get('ipa_rules', 100)),
        ('1.3 Error Handling', quality_scores.get('error_handling', 100)),
        ('1.4 Configuration', quality_scores.get('configuration', 100)),
        ('1.5 Performance', quality_scores.get('performance', 100))
    ]
    
    valid_sections = [(name, score) for name, score in sections if score is not None]
    section_names = [s[0] for s in valid_sections]
    scores = [s[1] for s in valid_sections]
    
    # Create modern horizontal bar chart
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor='white')
    
    # Color bars based on score
    colors = [COLORS['green'] if s >= 90 else COLORS['amber'] if s >= 70 else COLORS['red'] for s in scores]
    
    y_pos = range(len(section_names))
    bars = ax.barh(y_pos, scores, color=colors, height=0.7, edgecolor='white', linewidth=2)
    
    # Add value labels inside bars
    for i, (bar, score) in enumerate(zip(bars, scores)):
        label_color = 'white' if score > 30 else COLORS['dark_gray']
        x_pos = score - 8 if score > 30 else score + 3
        ha = 'right' if score > 30 else 'left'
        ax.text(x_pos, i, f'{score}%', 
                va='center', ha=ha, color=label_color, fontweight='bold', fontsize=11)
    
    # Styling
    ax.set_yticks(y_pos)
    ax.set_yticklabels(section_names, fontsize=11, fontweight='500')
    ax.set_xlim(0, 105)
    ax.set_xlabel('Quality Score (%)', fontsize=11, fontweight='500', color=COLORS['dark_gray'])
    ax.set_axisbelow(True)
    
    # Remove spines
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    
    # Grid
    ax.grid(axis='x', alpha=0.2, linestyle='-', linewidth=0.8, color='#CCCCCC')
    ax.set_facecolor('white')
    
    # Add reference lines
    ax.axvline(x=90, color=COLORS['green'], linestyle='--', linewidth=1, alpha=0.3)
    ax.axvline(x=70, color=COLORS['amber'], linestyle='--', linewidth=1, alpha=0.3)
    
    plt.tight_layout(pad=1.5)
    
    # Save to BytesIO
    img_data = BytesIO()
    plt.savefig(img_data, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    img_data.seek(0)
    plt.close()
    
    # Insert image
    ws.insert_image(chart_start_row, 0, '', {
        'image_data': img_data,
        'x_offset': 10,
        'y_offset': 10
    })
    
    # Move row pointer past chart (chart is ~300 pixels = ~20 rows)
    row = chart_start_row + 20
    ws.set_row(row, 10)  # Spacer
    row += 1
    
    # === KEY FINDINGS SECTION ===
    ws.merge_range(row, 0, row, 11, '  🔍 KEY FINDINGS', section_header)
    ws.set_row(row, 25)
    row += 1
    
    # Findings table
    finding_header = wb.add_format({
        'bold': True,
        'font_size': 10,
        'bg_color': COLORS['gray'],
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    
    pass_format = wb.add_format({
        'border': 1,
        'bg_color': COLORS['light_green'],
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'font_color': COLORS['green']
    })
    
    excellent_format = wb.add_format({
        'border': 1,
        'bg_color': COLORS['light_blue'],
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'font_color': COLORS['deep_blue']
    })
    
    verify_format = wb.add_format({
        'border': 1,
        'bg_color': COLORS['light_amber'],
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'font_color': COLORS['amber']
    })
    
    needs_improvement_format = wb.add_format({
        'border': 1,
        'bg_color': COLORS['light_amber'],
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'font_color': COLORS['amber']
    })
    
    finding_detail = wb.add_format({
        'border': 1,
        'text_wrap': True,
        'valign': 'top'
    })
    
    ws.merge_range(row, 0, row, 3, 'Category', finding_header)
    ws.write(row, 4, 'Status', finding_header)
    ws.merge_range(row, 5, row, 11, 'Details', finding_header)
    ws.set_row(row, 20)
    row += 1
    
    key_findings = ipa_data.get('key_findings', [])
    for finding in key_findings:
        category = finding.get('category', '')
        status = finding.get('status', '')
        details = finding.get('details', '')
        
        # Map status to appropriate format
        if status == 'Pass':
            status_fmt = pass_format
        elif status == 'Excellent':
            status_fmt = excellent_format
        elif status == 'Verify':
            status_fmt = verify_format
        elif status == 'Needs Improvement':
            status_fmt = needs_improvement_format
        else:
            status_fmt = verify_format  # Default to verify format
        
        ws.merge_range(row, 0, row, 3, category, finding_detail)
        ws.write(row, 4, status, status_fmt)
        ws.merge_range(row, 5, row, 11, details, finding_detail)
        ws.set_row(row, 30)
        row += 1
    
    # Column widths
    ws.set_column('A:D', 15)
    ws.set_column('E:E', 10)
    ws.set_column('F:L', 18)


def create_action_items(wb, ipa_data):
    """Create modern action items sheet"""
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
    ws.merge_range('A1:K1', '✅ ACTION ITEMS - DEVELOPER CHECKLIST', title_format)
    ws.set_row(0, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:K2', 'Items requiring attention or team verification', subtitle_format)
    ws.set_row(1, 20)
    
    # Modern header format
    header_format = wb.add_format({
        'bold': True,
        'font_size': 11,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1,
        'border_color': COLORS['white'],
        'align': 'center',
        'valign': 'vcenter'
    })
    
    # Modern data formats
    cell_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'text_wrap': True,
        'font_size': 10
    })
    critical_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFEBEE',
        'text_wrap': True,
        'font_size': 10
    })
    high_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFF3E0',
        'text_wrap': True,
        'font_size': 10
    })
    medium_format = wb.add_format({
        'border': 1,
        'border_color': COLORS['gray'],
        'valign': 'top',
        'bg_color': '#FFFDE7',
        'text_wrap': True,
        'font_size': 10
    })
    
    # Headers
    row = 3
    ws.write(row, 0, 'Priority', header_format)
    ws.write(row, 1, 'Category', header_format)
    ws.write(row, 2, 'Rule ID', header_format)
    ws.write(row, 3, 'File/Activity', header_format)
    ws.write(row, 4, 'Issue', header_format)
    ws.write(row, 5, 'Current State', header_format)
    ws.write(row, 6, 'Recommendation', header_format)
    ws.write(row, 7, 'Effort', header_format)
    ws.write(row, 8, 'Impact', header_format)
    ws.write(row, 9, 'Status', header_format)
    ws.set_row(row, 25)
    
    row += 1
    
    # Collect all issues (avoid duplicates by checking activity + issue content)
    all_issues = []
    seen_items = set()  # Track (activity, issue) pairs to avoid duplicates
    
    # Add SQL recommendations from sql_queries array (if they have actionable recommendations)
    for sql_query in ipa_data.get('sql_queries', []):
        recommendations = sql_query.get('recommendations', '')
        if recommendations and recommendations.strip() and not recommendations.lower().startswith('none'):
            activity = sql_query.get('activity_id', 'SQL Query')
            issue_text = recommendations
            key = (activity.lower().strip(), issue_text.lower().strip())
            
            if key not in seen_items:
                # Determine priority based on keywords
                priority = 'Low'  # Default for SQL optimizations
                if any(word in recommendations.lower() for word in ['critical', 'missing', 'required']):
                    priority = 'High'
                elif any(word in recommendations.lower() for word in ['should', 'important']):
                    priority = 'Medium'
                
                all_issues.append({
                    'priority': priority,
                    'category': 'SQL Performance',
                    'rule_id': 'Best Practice',
                    'activity': activity,
                    'issue': f"SQL optimization opportunity in {sql_query.get('query_type', 'query')}",
                    'current': sql_query.get('assessment', ''),
                    'recommendation': recommendations,
                    'effort': 'Low',
                    'impact': 'Low',
                    'status': 'Needs Improvement'
                })
                seen_items.add(key)
    
    # Add recommendations (these are the primary action items)
    for rec in ipa_data.get('recommendations', []):
        category = rec.get('category', 'General')
        activities = rec.get('activities', '')
        # Handle both string and list formats for activities
        if isinstance(activities, list):
            activity = ', '.join(activities) if activities else ipa_data.get('overview', {}).get('process_name', '')
        else:
            activity = activities if activities else ipa_data.get('overview', {}).get('process_name', '')
        
        issue_text = rec.get('issue', '')
        # Create unique key based on activity AND issue content (not category)
        key = (activity.lower().strip(), issue_text.lower().strip())
        
        if key not in seen_items:
            # Recommendations default to "Needs Improvement" (actionable items from AI analysis)
            # Only use "Pending" if explicitly set in the recommendation
            default_status = rec.get('status', 'Needs Improvement')
            
            all_issues.append({
                'priority': rec.get('priority', 'Medium'),
                'category': category,
                'rule_id': rec.get('rule_id', 'AI Analysis'),  # Default to AI Analysis for recommendations
                'activity': activity,
                'issue': issue_text,
                'current': rec.get('current', ''),
                'recommendation': rec.get('recommendation', ''),
                'effort': rec.get('effort', 'Medium'),
                'impact': rec.get('impact', 'Medium'),
                'status': default_status
            })
            seen_items.add(key)
    
    # Only add coding standards issues if they're NOT already covered by recommendations
    for section_name, issues in ipa_data.get('coding_standards', {}).items():
        for issue in issues:
            if len(issue) >= 7:
                status = issue[5] if len(issue) > 5 else 'Needs Improvement'
                category = section_name.replace('_', ' ').title()
                activity = issue[0] if len(issue) > 0 else ''
                issue_text = issue[3] if len(issue) > 3 else ''
                # Create unique key based on activity AND issue content
                key = (activity.lower().strip(), issue_text.lower().strip())
                
                # Only add if status requires action (Verify or Needs Improvement) AND not already added
                # Exclude: Pass, Excellent, Good, N/A (these don't need action items)
                if status in ['Verify', 'Needs Improvement'] and key not in seen_items:
                    # Extract rule_id from issue[1] which contains rule name like "Config set naming (FPI 1.1.3)"
                    rule_name = issue[1] if len(issue) > 1 else ''
                    # Try to extract rule ID from parentheses
                    import re
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
                        'status': status
                    })
                    seen_items.add(key)
    
    # Sort by priority
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    all_issues.sort(key=lambda x: priority_order.get(x['priority'], 4))
    
    # Write issues
    for issue in all_issues:
        severity = issue['priority']
        fmt = critical_format if severity == 'Critical' else high_format if severity == 'High' else medium_format if severity == 'Medium' else cell_format
        
        ws.write(row, 0, issue['priority'], fmt)
        ws.write(row, 1, issue['category'], fmt)
        ws.write(row, 2, issue.get('rule_id', 'AI Analysis'), fmt)
        ws.write(row, 3, issue['activity'], fmt)
        ws.write(row, 4, issue['issue'], fmt)
        ws.write(row, 5, issue['current'], fmt)
        ws.write(row, 6, issue['recommendation'], fmt)
        ws.write(row, 7, issue['effort'], fmt)
        ws.write(row, 8, issue['impact'], fmt)
        ws.write(row, 9, issue['status'], fmt)
        row += 1
    
    # Column widths
    ws.set_column('A:A', 10)
    ws.set_column('B:B', 20)
    ws.set_column('C:C', 12)
    ws.set_column('D:D', 25)
    ws.set_column('E:E', 30)
    ws.set_column('F:F', 25)
    ws.set_column('G:G', 35)
    ws.set_column('H:H', 10)
    ws.set_column('I:I', 10)
    ws.set_column('J:J', 12)


def create_detailed_analysis(wb, ipa_data):
    """Create modern detailed analysis sheet"""
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
    ws.merge_range('A1:J1', '📐 DETAILED ANALYSIS & CONTEXT', title_format)
    ws.set_row(0, 35)
    
    # Subtitle
    subtitle_format = wb.add_format({
        'font_size': 10,
        'align': 'center',
        'bg_color': COLORS['light_blue'],
        'font_color': COLORS['dark_gray']
    })
    ws.merge_range('A2:J2', 'Comprehensive technical analysis and recommendations', subtitle_format)
    ws.set_row(1, 20)
    
    # Modern section header format
    section_format = wb.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': COLORS['medium_blue'],
        'font_color': 'white',
        'border': 1,
        'border_color': COLORS['white']
    })
    
    # Modern subsection format
    subsection_format = wb.add_format({
        'bold': True,
        'font_size': 12,
        'bg_color': COLORS['light_blue'],
        'border': 1,
        'border_color': COLORS['gray']
    })
    
    # Modern data formats
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
    row += 1
    
    ws.write(row, 0, 'Assessment:', label_format)
    ws.merge_range(row, 1, row, 9, overview.get('auto_restart_assessment', 'N/A'), good_format)
    row += 2
    
    # SECTION 2: JavaScript ES5 Violations
    ws.merge_range(row, 0, row, 9, '2. JAVASCRIPT ES5 COMPLIANCE', section_format)
    row += 1
    
    js_issues = ipa_data.get('javascript_issues', [])
    if js_issues:
        ws.write(row, 0, 'Activity', subsection_format)
        ws.write(row, 1, 'Line', subsection_format)
        ws.write(row, 2, 'Issue Type', subsection_format)
        ws.write(row, 3, 'Severity', subsection_format)
        ws.merge_range(row, 4, row, 6, 'Code Snippet', subsection_format)
        ws.merge_range(row, 7, row, 9, 'Recommendation', subsection_format)
        row += 1
        
        for issue in js_issues:
            ws.write(row, 0, issue[1] if len(issue) > 1 else '', value_format)
            ws.write(row, 1, issue[2] if len(issue) > 2 else '', value_format)
            ws.write(row, 2, issue[3] if len(issue) > 3 else '', value_format)
            ws.write(row, 3, issue[4] if len(issue) > 4 else '', warning_format)
            ws.merge_range(row, 4, row, 6, issue[6] if len(issue) > 6 else '', code_format)
            ws.merge_range(row, 7, row, 9, issue[5] if len(issue) > 5 else '', value_format)
            row += 1
    else:
        ws.merge_range(row, 0, row, 9, '✓ No ES6 violations found - All JavaScript code is ES5 compliant', good_format)
        row += 1
    
    row += 1
    
    # SECTION 3: SQL Review
    ws.merge_range(row, 0, row, 9, '3. SQL REVIEW', section_format)
    row += 1
    
    sql_queries = ipa_data.get('sql_queries', [])
    if sql_queries:
        for query in sql_queries:
            ws.write(row, 0, 'Activity:', label_format)
            activity_text = query.get('activity_id', '')
            ws.merge_range(row, 1, row, 9, activity_text, value_format)
            ws.set_row(row, calculate_row_height(activity_text, column_width=100))
            row += 1
            
            ws.write(row, 0, 'Type:', label_format)
            type_text = query.get('query_type', 'Compass SQL')
            ws.merge_range(row, 1, row, 9, type_text, value_format)
            ws.set_row(row, calculate_row_height(type_text, column_width=100))
            row += 1
            
            ws.write(row, 0, 'Query:', label_format)
            row += 1
            query_text = query.get('query', '')
            ws.merge_range(row, 0, row, 9, query_text, code_format)
            ws.set_row(row, calculate_row_height(query_text, column_width=100, base_height=12))
            row += 1
            
            if 'assessment' in query:
                ws.write(row, 0, 'Assessment:', label_format)
                assessment_text = query.get('assessment', '')
                ws.merge_range(row, 1, row, 9, assessment_text, value_format)
                ws.set_row(row, calculate_row_height(assessment_text, column_width=100))
                row += 1
            
            if 'recommendations' in query:
                ws.write(row, 0, 'Recommendations:', label_format)
                rec_text = query.get('recommendations', '')
                ws.merge_range(row, 1, row, 9, rec_text, value_format)
                ws.set_row(row, calculate_row_height(rec_text, column_width=100))
                row += 1
            
            row += 1
    else:
        ws.merge_range(row, 0, row, 9, 'ℹ️ No SQL queries found in this process', value_format)
        row += 1
    
    row += 1
    
    # SECTION 4: Coding Standards Breakdown (1.1-1.5)
    ws.merge_range(row, 0, row, 9, '4. CODING STANDARDS BREAKDOWN', section_format)
    row += 1
    
    standards = ipa_data.get('coding_standards', {})
    standard_sections = [
        ('naming_convention', '1.1 Naming Convention'),
        ('ipa_rules', '1.2 IPA Rules'),
        ('error_handling', '1.3 Error Handling'),
        ('system_configuration', '1.4 System Configuration'),
        ('performance', '1.5 Performance Consideration')
    ]
    
    for key, title in standard_sections:
        ws.merge_range(row, 0, row, 9, title, subsection_format)
        row += 1
        
        items = standards.get(key, [])
        if items:
            for item in items:
                status = item[5] if len(item) > 5 else 'Needs Improvement'
                fmt = good_format if status == 'Pass' else warning_format
                
                ws.write(row, 0, 'Item:', label_format)
                item_text = item[1] if len(item) > 1 else ''
                ws.merge_range(row, 1, row, 9, item_text, value_format)
                ws.set_row(row, calculate_row_height(item_text, column_width=100))
                row += 1
                
                ws.write(row, 0, 'Finding:', label_format)
                finding_text = item[3] if len(item) > 3 else ''
                ws.merge_range(row, 1, row, 9, finding_text, value_format)
                ws.set_row(row, calculate_row_height(finding_text, column_width=100))
                row += 1
                
                ws.write(row, 0, 'Current:', label_format)
                current_text = item[4] if len(item) > 4 else ''
                ws.merge_range(row, 1, row, 9, current_text, value_format)
                ws.set_row(row, calculate_row_height(current_text, column_width=100))
                row += 1
                
                ws.write(row, 0, 'Status:', label_format)
                ws.merge_range(row, 1, row, 9, status, fmt)
                row += 1
                
                ws.write(row, 0, 'Action:', label_format)
                action_text = item[6] if len(item) > 6 else ''
                ws.merge_range(row, 1, row, 9, action_text, value_format)
                ws.set_row(row, calculate_row_height(action_text, column_width=100))
                row += 2
        else:
            ws.merge_range(row, 0, row, 9, 'No items to review', value_format)
            row += 2
    
    # SECTION 5: Best Practices
    ws.merge_range(row, 0, row, 9, '5. BEST PRACTICES ASSESSMENT', section_format)
    row += 1
    
    best_practices = ipa_data.get('best_practices', [])
    for practice in best_practices:
        ws.write(row, 0, 'Category:', label_format)
        category_text = practice.get('category', '')
        ws.merge_range(row, 1, row, 9, category_text, value_format)
        ws.set_row(row, calculate_row_height(category_text, column_width=100))
        row += 1
        
        ws.write(row, 0, 'Status:', label_format)
        status = practice.get('status', '')
        fmt = good_format if 'Excellent' in status or 'Good' in status else warning_format
        ws.merge_range(row, 1, row, 9, status, fmt)
        row += 1
        
        ws.write(row, 0, 'Details:', label_format)
        details_text = practice.get('details', '')
        ws.merge_range(row, 1, row, 9, details_text, value_format)
        ws.set_row(row, calculate_row_height(details_text, column_width=100))
        row += 1
        
        if 'code_example' in practice:
            ws.write(row, 0, 'Example:', label_format)
            example_text = practice.get('code_example', '')
            ws.merge_range(row, 1, row, 9, example_text, code_format)
            ws.set_row(row, calculate_row_height(example_text, column_width=100, base_height=12))
            row += 1
        
        row += 1
    
    # SECTION 6: Technical Architecture
    ws.merge_range(row, 0, row, 9, '6. TECHNICAL ARCHITECTURE', section_format)
    row += 1
    
    tech = ipa_data.get('technical_deep_dive', {})
    arch = tech.get('architecture', {})
    
    ws.write(row, 0, 'Pattern:', label_format)
    ws.merge_range(row, 1, row, 9, arch.get('pattern', ''), value_format)
    row += 1
    
    ws.write(row, 0, 'Components:', label_format)
    row += 1
    for component in arch.get('components', []):
        ws.merge_range(row, 1, row, 9, f'• {component}', value_format)
        row += 1
    
    row += 1
    ws.write(row, 0, 'Strengths:', label_format)
    row += 1
    for strength in arch.get('strengths', []):
        ws.merge_range(row, 1, row, 9, f'✓ {strength}', good_format)
        row += 1
    
    row += 1
    ws.write(row, 0, 'Weaknesses:', label_format)
    row += 1
    for weakness in arch.get('weaknesses', []):
        ws.merge_range(row, 1, row, 9, f'⚠ {weakness}', warning_format)
        row += 1
    
    row += 1
    
    # SECTION 7: Recommendations Summary
    ws.merge_range(row, 0, row, 9, '7. RECOMMENDATIONS SUMMARY', section_format)
    row += 1
    
    recommendations = ipa_data.get('recommendations', [])
    for rec in recommendations:
        priority = rec.get('priority', 'Medium')
        fmt = warning_format if priority in ['Critical', 'High'] else value_format
        
        ws.write(row, 0, 'Priority:', label_format)
        ws.merge_range(row, 1, row, 9, priority, fmt)
        row += 1
        
        ws.write(row, 0, 'Category:', label_format)
        ws.merge_range(row, 1, row, 9, rec.get('category', ''), value_format)
        row += 1
        
        ws.write(row, 0, 'Issue:', label_format)
        ws.merge_range(row, 1, row, 9, rec.get('issue', ''), value_format)
        row += 1
        
        ws.write(row, 0, 'Recommendation:', label_format)
        ws.merge_range(row, 1, row, 9, rec.get('recommendation', ''), value_format)
        row += 1
        
        ws.write(row, 0, 'Effort:', label_format)
        ws.write(row, 1, rec.get('effort', ''), value_format)
        ws.write(row, 2, 'Impact:', label_format)
        ws.merge_range(row, 3, row, 9, rec.get('impact', ''), value_format)
        row += 1
        
        ws.write(row, 0, 'Testing:', label_format)
        ws.merge_range(row, 1, row, 9, rec.get('testing', ''), value_format)
        row += 2
    
    # Column widths
    ws.set_column('A:A', 15)
    ws.set_column('B:J', 20)


if __name__ == "__main__":
    print("IPA Coding Standards Template - matplotlib edition")
    print("Usage: from ReusableTools.IPA_CodingStandards.ipa_coding_standards_template import generate_report")
