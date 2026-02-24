---
inclusion: auto
name: wu-report-generation
description: Work unit log analysis and Excel report generation. Use when analyzing WU logs, generating WU reports, or working with wu_master_template.py.
---

# Work Unit Report Generation

## Purpose

Standards for generating Excel reports from work unit (WU) log analysis. This guide covers WU analysis reports for internal technical analysis of IPA runtime execution.

**Core Principle**: AI analyzes data and builds structured dictionaries. Python templates format pre-analyzed data into Excel reports.

**Note**: For IPA source code analysis and client handover documentation, see `10_IPA_Report_Generation.md`.

## Quick Reference

**When user says**: "Read WU 12345" or "Analyze WU 12345"

1. Search `WU_Logs/` for file containing WU number
2. Read and analyze log (activities, errors, JavaScript, metrics)
3. Build `wu_data` dictionary with analyzed data
4. Generate report automatically using `wu_master_template.py`
5. Save to `WU_Report_Results/WU_<ProcessName>_Report_YYYYMMDD.xlsx`
6. Inform user of report location

**CRITICAL**: Always generate report automatically. Do NOT ask for confirmation. Use "N/A" for missing optional fields (RICE ID, Developer, Peer Reviewer, Tenant).

## Architecture

**Separation of Concerns**:

- **AI Role**: Read logs, analyze data, build `wu_data` dictionary
- **Template Role**: Format pre-analyzed data into Excel (NO analysis logic)
- **Template File**: `wu_master_template.py` (workspace root)
- **Output Location**: `WU_Report_Results/WU_<ProcessName>_Report_YYYYMMDD.xlsx`
- **Temp Scripts**: `Temp/` folder for disposable generation scripts

## wu_data Dictionary Structure

**Required structure for WU analysis reports**:

```python
wu_data = {
    # Basic Info (required)
    'work_unit_id': str,           # "636228"
    'process_name': str,           # "CISOutboundIntegration"
    'status': str,                 # "SUCCESS" or "FAILED"
    
    # Dashboard Data
    'info_data': [                 # Metrics: ["Metric", "Value", "Status", "Rating"]
        ["Total Duration", "18.5s", "✅ Pass", "Excellent"],
        ["Memory Usage", "45.2 MiB", "✅ Pass", "Good"],
    ],
    'chart_data': {
        'status': [("Success", 1), ("Failed", 0)],
        'memory_by_activity': [("Activity1", 100.5), ("Activity2", 45.2)]
    },
    
    # Activity Timeline
    'activities': [
        {
            'name': str,           # Activity name
            'type': str,           # START, LM, ASSGN, BRANCH, UA, EMAIL, etc.
            'start_time': str,     # ISO timestamp
            'end_time': str,       # ISO timestamp or "N/A"
            'duration': str,       # "1.2s", "45ms", "N/A"
            'status': str          # "Completed", "Error", "In Progress"
        }
    ],
    
    # Performance Metrics
    'metrics': {
        'duration_ms': int,
        'memory_mib': float,
        'cpu_time_ms': int,
        'user_time_ms': int
    },
    
    # Error Analysis
    'errors': [
        {
            'activity': str,
            'type': str,           # "JavaScript Error", "FSM Error", "Timeout"
            'message': str,
            'severity': str,       # "Critical", "High", "Medium", "Low"
            'impact': str
        }
    ],
    
    # JavaScript Review (10 columns as list of lists)
    'js_issues': [
        [work_unit_id, activity, block, issue_type, severity, 
         line, code_snippet, root_cause, specific_fix_es5, prevention]
    ],
    
    # SQL Review (10 columns as list of lists)
    'sql_issues': [
        [work_unit_id, activity, query_type, sql_snippet, severity,
         issue, root_cause, recommendation, compass_compatible, performance_impact]
    ],
    
    # Memory Analysis (7 columns as list of lists)
    'memory_analysis': [
        [work_unit_id, activity, type, memory_mib, duration_ms, efficiency, rating]
    ],
    
    # Recommendations (10 columns as list of lists)
    'recommendations': [
        [priority, category, issue_description, affected_wus, root_cause,
         specific_fix, code_example_es5, testing_steps, effort, impact]
    ],
    
    # Technical Analysis (3 columns as list of lists)
    'architecture_analysis': [
        ["Aspect", "Value", "Assessment"],
        ["Design Pattern", "File Processing", "Standard pattern for batch processing"]
    ],
    'js_quality_analysis': [
        ["Metric", "Score", "Assessment"],
        ["ES5 Compliance", "85", "Good - minor issues with ternary operators"]
    ],
    'business_impact': [
        ["Factor", "Value", "Assessment"],
        ["Failure Impact", "High", "Blocks downstream GL posting"]
    ]
}
```

**ES5 JavaScript Requirements**:

IPA uses ES5 JavaScript. All fix recommendations MUST use ES5 syntax:

- `var` (NOT `let` or `const`)
- `typeof varName !== "undefined"` for null checks
- `function()` (NOT arrow functions `=>`)
- String concatenation with `+` (NOT template literals)
- `Array.prototype.slice.call()` (NOT spread operator `...`)

## Excel Report Standards

**Libraries**: `openpyxl` + `pandas` for 10-50x faster generation

**9 Standard Sheets** (WU Analysis):

1. Summary Dashboard - Executive overview with charts
2. Activity Timeline - Chronological execution (7 columns)
3. Performance Metrics - Duration, memory, CPU (7 columns)
4. Error Analysis - Errors and impact (6 columns)
5. JavaScript Review - ES5 compliance (10 columns)
6. SQL Review - Data Fabric/Compass queries (10 columns)
7. Memory Analysis - Memory by activity (7 columns)
8. Recommendations - Actionable fixes (10 columns)
9. Technical Analysis - Architecture, JS quality, business impact

**Formatting Standards**:

- Headers: Infor blue (#0066CC) with white text
- Color coding: Green (C6EFCE), Yellow (FFEB9C), Red (FFC7CE)
- Cell syntax: `cell(row=X, column=Y)` format
- Auto-adjust column widths
- Sortable headers, conditional formatting

**Color Thresholds**:

- Memory: Green <70K MiB, Yellow 70K-90K, Red >90K (white font)
- Duration: Green ≤1min, Yellow 1-5min, Red >5min (white font)
- Priority: Critical=Red, High=Orange, Medium=Yellow, Low=Green

## Sheet-Specific Details

### Summary Dashboard

- Layout: Key Info (A3:D15), Charts (F3:K15), Analysis (A17:K25)
- Charts: Pie (Process Status) at F4, Bar (Memory by Activity) at I4
- Display tenant ID (e.g., VWF68LHJUP5D6NUB-TRN)
- Use IQR method for outlier detection

### Activity Timeline (7 columns)

- Columns: Work Unit ID, Activity, Type, Start, End, Duration, Status
- End time: Actual timestamp or "N/A"
- Status: Extract from log (Completed/Error)

### Performance Metrics (7 columns)

- Display memory in MiB
- Show actual CPU/User time from metrics

### Error Analysis (6 columns)

- Red highlighting only when FSM error count >0
- White font on red background

### JavaScript Review (10 columns)

- Work Unit ID, Activity, Block, Issue Type, Severity, Line, Code Snippet, Root Cause, Specific Fix (ES5), Prevention

### SQL Review (10 columns)

- Work Unit ID, Activity, Query Type, SQL Snippet, Severity, Issue, Root Cause, Recommendation, Compass Compatible, Performance Impact
- Show consolidated query count per WU
- Recognize Data Fabric CSV-based API processes positively

### Memory Analysis (7 columns)

- Show actual peak memory node (e.g., "Assign8560")
- Efficiency: `(1 - memory_used/70K) * 100`
- Rating: Node-type specific thresholds

### Recommendations (10 columns)

- Priority, Category, Issue Description, Affected WUs, Root Cause, Specific Fix, Code Examples, Testing Steps, Effort, Impact
- Enable text wrap for detailed columns

### Technical Analysis (3-column tables)

- Process Architecture: Design patterns, service classification, auto-restart, activity count
- JS Code Quality: ES5/Security/Performance/Code Quality scores (0-100)
- Configuration: OAuth, variables, URLs, email, environment
- Business Impact: Purpose, failure impact, downstream systems, data integrity

## Python Script Template

```python
#!/usr/bin/env python3

import sys
import openpyxl
import pandas as pd
from wu_master_template import generate_report

def main():
    # Build wu_data dictionary
    wu_data = {
        'work_unit_id': '12345',
        'process_name': 'ProcessName',
        # ... rest of structure
    }
    
    # Generate report
    output_path = generate_report(wu_data)
    print(f"Report saved: {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Rules**:

- Shebang: `#!/usr/bin/env python3`
- Use `if __name__ == "__main__":` guard
- Use `sys.exit(main())` pattern
- Create in `Temp/` folder only

## JavaScript Analysis Requirements

**Comprehensive Analysis Categories**:

1. **ES5 Compliance** (15 pts penalty/issue): let/const, arrow functions, template literals, classes, spread, destructuring, default params, object shorthand

2. **Performance** (10 pts penalty/issue): for...in loops, nested loops, JSON parsing frequency, string concatenation (3+), repeated calls, regex optimization, nested conditionals (4+ levels)

3. **Code Quality** (5 pts penalty/issue): === vs ==, hoisting, unused vars, magic strings, function complexity, naming, semicolons, boolean string comparisons

4. **Security** (20 pts penalty/issue): eval(), Function constructor, innerHTML, document.write, setTimeout with strings, dynamic property access, global pollution, unsafe regex, input validation

5. **Best Practices**: try-catch, default values, type checking, variable scope, named constants

**Output Requirements**:

- Overall grade (A-D)
- Total issues count, critical issues
- Line-level tracking with code snippets
- Severity classification
- Block-by-block analysis

**Error Detection**:

- Detect runtime errors (ReferenceError, TypeError, SyntaxError)
- Classify as Critical severity
- Provide specific recommendations with exact variable names
- Include root cause analysis

## Technical Analysis Requirements

**Process Architecture**:

- Design patterns, service classification, auto-restart compliance, activity count, flow patterns, configuration dependencies

**JavaScript Code Quality Scores** (0-100):

- ES5 Compliance Score
- Security Score
- Performance Score
- Code Quality Score

**Configuration Analysis**:

- OAuth, variables, URLs, email, environment settings, process variables

**Business Impact**:

- Process purpose, failure impact, downstream systems, data integrity, recovery time, business continuity

**Color Coding**: Red=critical, Yellow=warning, Green=compliant

## Recommendations Requirements

**10-Column Structure**:

1. Priority (Critical/High/Medium/Low)
2. Category
3. Issue Description
4. Affected Work Units
5. Root Cause Analysis (WHY)
6. Specific Fix Required (exact implementation)
7. Code Examples (before/after ES5)
8. Testing Steps (validation procedures)
9. Effort (Low/Medium/High)
10. Impact (Critical/High/Medium/Low)

**Labels**:

- ✅ RECOMMENDED: Keep current implementation
- 🔍 OPTIONAL: Monitoring/infrastructure changes
- ⚠️ CONSIDER: Evaluate business need, then implement

## Process Pattern Examples

### GLAgriBankInterface

**Type**: Agricultural banking GL transaction interface

**Key Characteristics**:

- File-based from /InProgress directory
- Multi-entity (FCIL organization)
- Transaction types: loans, payments, fees, accruals
- Real-time GL creation and posting
- Auto-restart disabled (financial integrity)
- ES5-compliant with OAuth

**Benchmarks**: 2-10MB/s processing, 171 GL records, ~1s for 201KB, 0% error rate

### Currency Exchange Rate Export

**Type**: GEOSYNTEC_INT_N-0004_DailyCurrencyExchangeRateExport_Outbound

**Key Characteristics**:

- Daily automated export
- Pagination (30 records/page)
- CSV with quoted fields
- 15+ currency pairs
- Email notifications
- Timestamp-based filtering

**Benchmarks**: 48-85ms query/page, 2-16ms/record, 90+ rates, 0% error rate

### EmPowerGLInterface

**Type**: Empower GL journal entry processing

**Key Characteristics**:

- OAuth2 with CloudSuite
- Dynamic FEG routing
- CSV parsing with regex
- JSON batch processing
- ACH disbursements/receipts
- Multi-entity with dynamic credentials

**Benchmarks**: Fast OAuth2, efficient regex, optimized JSON, automatic cleanup
