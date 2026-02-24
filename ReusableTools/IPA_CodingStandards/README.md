# IPA Coding Standards Analyzer

Automated code quality analysis for Infor Process Automation (IPA) processes using domain-segmented AI analysis with specialized subagents.

## Overview

This tool analyzes IPA processes against coding standards and generates comprehensive Excel reports with visual dashboards, action items, and process flow diagrams.

## Architecture

**Domain-Segmented Analysis**: Prevents context overload by analyzing one domain at a time instead of everything together.

**5 Specialized Subagents** (run in parallel):
1. `ipa-naming-analyzer` - Filenames, node captions, config sets
2. `ipa-javascript-analyzer` - ES5 compliance, performance
3. `ipa-sql-analyzer` - Compass SQL, pagination
4. `ipa-error-handling-analyzer` - OnError tabs, coverage
5. `ipa-structure-analyzer` - Auto-restart, process type

**Workflow**:
1. Python extracts data → JSON
2. Python organizes by domain → 5 domain files
3. AI analyzes each domain (parallel) → Violations per domain
4. Python merges violations → Master file
5. Python generates report → ONE Excel

## Files

### Core Scripts

- `extract_lpd_data.py` - Extracts data from LPD files
- `organize_by_domain.py` - Organizes extracted data by domain
- `merge_violations.py` - Merges domain violations into master file
- `analyze_coding_standards.py` - Programmatic analyzer (optional)

### Templates

- `ipa_coding_standards_template_enhanced.py` - **Current** (v2.0 - Enhanced Edition)
  - 4 sheets: Executive Dashboard, Action Items, Detailed Analysis, Process Flow
  - Enhanced columns: Priority Score, Est. Fix Time, Affected %, Code Examples, Testing Notes
  - Backward compatible with old data format
  
- `ipa_coding_standards_template.py` - Legacy (v1.0)
  - 3 sheets: Executive Dashboard, Action Items, Detailed Analysis
  - Superseded by enhanced template

### Helpers

- `build_ipa_data_helper.py` - Builds ipa_data from violations (prevents duplicates)
- `check_standard_flow.py` - Checks if process is a standard flow

### Documentation

- `README.md` - This file
- `ENHANCEMENT_PLAN.md` - Enhancement roadmap and status
- `ARCHITECTURE.md` - Detailed architecture documentation

## Usage

### Via Hook (Recommended)

Trigger the "Coding Standards" hook (v34) which automates the entire workflow.

### Manual Usage

```python
import sys
sys.path.insert(0, '.')

# Step 1: Extract data
from ReusableTools.IPA_Analyzer.extract_lpd_data import extract_lpd_data
extract_lpd_data(['path/to/process.lpd'], 'Temp/ProcessName_lpd_data.json')

# Step 2: Organize by domain
# Run: python ReusableTools/IPA_CodingStandards/organize_by_domain.py Temp/ProcessName_lpd_data.json Temp/ProcessName

# Step 3: Analyze each domain (use subagents or manual analysis)

# Step 4: Merge violations
# Run: python ReusableTools/IPA_CodingStandards/merge_violations.py Temp/ProcessName

# Step 5: Build ipa_data and generate report
from ReusableTools.IPA_CodingStandards.build_ipa_data_helper import build_ipa_data_from_violations
from ReusableTools.IPA_CodingStandards.ipa_coding_standards_template_enhanced import generate_report

ipa_data = build_ipa_data_from_violations(
    violations=violations,
    client_name='Client',
    rice_item='Project',
    process_name='ProcessName',
    process_type='Interface Process',
    activity_count=78,
    activities=activities_array,
    quality_scores=quality_scores_dict,
    key_findings=key_findings_array
)

output_path = generate_report(ipa_data)
print(f'Report generated: {output_path}')
```

## Report Structure

### Executive Dashboard
- KPI cards: Overall Quality, Processes, Complexity, Action Items
- Radar chart: Quality metrics visualization
- Key findings: Top 5 findings with status badges

### Action Items (Enhanced)
14 columns:
1. Priority
2. Category
3. Rule ID
4. Activity
5. Issue
6. Current
7. Recommendation
8. Effort
9. Impact
10. **Priority Score** (0-100)
11. **Est. Fix Time**
12. **Affected %**
13. **Code Example** (before/after)
14. **Testing Notes**

### Detailed Analysis (Enhanced)
- Process Overview
- Violations with Impact Analysis:
  - Impact Analysis (frequency, affected %, maintainability, fix time)
  - Code Examples (before, after, explanation)
  - Testing Notes
  - Priority Score

### Process Flow (NEW)
- Process information
- Complexity breakdown with scoring
- Activity flow diagram
- Critical paths and recommendations

## Enhanced Fields

The enhanced template (v2.0) supports additional fields for richer analysis:

```python
{
    # Standard fields
    'rule_id': 'FPI 1.1.1',
    'severity': 'Medium',
    'finding': 'Description',
    'current': 'Current state',
    'recommendation': 'How to fix',
    'activities': 'Affected activities',
    'domain': 'naming',
    
    # Enhanced fields (optional)
    'impact_analysis': {
        'frequency': 'Every execution',
        'affected_percentage': 75,
        'maintainability_impact': 'High',
        'estimated_fix_time': '2-3 hours'
    },
    'code_examples': {
        'before': 'old code',
        'after': 'new code',
        'explanation': 'why better'
    },
    'testing_notes': 'what to test',
    'priority_score': 85
}
```

**Backward Compatibility**: Template works without enhanced fields (shows defaults).

## Subagents

Located in `.kiro/agents/`:

- `ipa-naming-analyzer.md`
- `ipa-javascript-analyzer.md`
- `ipa-sql-analyzer.md`
- `ipa-error-handling-analyzer.md`
- `ipa-structure-analyzer.md`

Each subagent:
- Has read-only tools (safe for analysis)
- Auto-loads relevant steering files
- Returns structured JSON violations array
- Runs in parallel with other subagents

## Performance

- Extraction: ~1s per 12K lines
- Organization: ~2s
- AI analysis (5 subagents in parallel): ~30-60s
- Report generation: <10s
- **Total: ~1-2 min per process** (70-80% faster than sequential)

## Version History

### v2.0 (2026-02-22) - Enhanced Edition
- Added Process Flow sheet
- Enhanced Action Items with 4 new columns
- Enhanced Detailed Analysis with impact sections
- Backward compatible with v1.0 data

### v1.0 (2026-02-08) - Initial Release
- 3-sheet report (Dashboard, Action Items, Detailed Analysis)
- Domain-segmented analysis
- Parallel subagent execution

## Related Documentation

- `.kiro/steering/00_Kiro_General_Rules.md` - General workflow rules
- `.kiro/steering/10_IPA_Report_Generation.md` - Report generation guide
- `.kiro/hooks/coding-standards.kiro.hook` - Automated workflow hook (v34)

## Support

For issues or questions, refer to:
- `ENHANCEMENT_PLAN.md` - Feature roadmap
- `ARCHITECTURE.md` - Technical details
- `.kiro/steering/` - Comprehensive guides
