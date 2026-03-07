---
inclusion: auto
name: wu-report-generation
description: Work unit log analysis and Excel report generation. Use when analyzing WU logs, generating WU reports, or working with wu_master_template.py.
---

# Work Unit Report Generation

## Table of Contents

- [Purpose](#purpose)
- [Quick Reference](#quick-reference)
- [Architecture](#architecture)
- [wu_data Dictionary Structure](#wu_data-dictionary-structure)
- [Excel Report Standards](#excel-report-standards)
- [Sheet-Specific Details](#sheet-specific-details)
- [Python Script Template](#python-script-template)
- [JavaScript Analysis Requirements](#javascript-analysis-requirements)
- [SQL Analysis Requirements](#sql-analysis-requirements)
- [Technical Analysis Requirements](#technical-analysis-requirements)
- [Recommendations Requirements](#recommendations-requirements)
- [Process Pattern Examples](#process-pattern-examples)

## Purpose

Standards for generating Excel reports from work unit (WU) log analysis. This guide covers WU analysis reports for internal technical analysis of IPA runtime execution.

**Core Principle**: AI analyzes data and builds structured dictionaries. Python templates format pre-analyzed data into Excel reports.

**Scope Distinction**:

- This guide: WU runtime execution analysis (logs, performance, errors)
- `10_IPA_Report_Generation.md`: IPA source code analysis and client handover documentation

## Quick Reference

### Automatic Report Generation Workflow

**When user says**: "Read WU 12345", "Analyze WU 12345", or "Generate WU report for 12345"

**CRITICAL EXECUTION RULES**:

- Generate report automatically without asking for confirmation
- Use "N/A" for missing optional fields (RICE ID, Developer, Peer Reviewer, Tenant)
- Do NOT prompt user for missing metadata
- Proceed immediately with available data

**Standard Workflow**:

1. **Locate log file**: Search `WU_Logs/` for file containing WU number (format: `<number>_log.txt`)
2. **Analyze log**: Extract activities, errors, JavaScript code, SQL queries, performance metrics
3. **Build wu_data dictionary**: Structure analyzed data according to schema (see below)
4. **Generate report**: Execute `wu_master_template.py` with wu_data
5. **Save output**: `WU_Report_Results/WU_<ProcessName>_Report_YYYYMMDD.xlsx`
6. **Inform user**: Report location and key findings summary

## Architecture

### Separation of Concerns

**AI Responsibilities**:

- Read and parse work unit log files
- Extract activities, timestamps, errors, JavaScript code, SQL queries
- Analyze performance metrics, memory usage, execution patterns
- Identify issues, root causes, and recommendations
- Build structured `wu_data` dictionary with pre-analyzed data

**Template Responsibilities** (`wu_master_template.py`):

- Format pre-analyzed data into Excel workbook
- Apply styling, colors, conditional formatting
- Generate charts and visualizations
- NO analysis logic (all analysis done by AI)

**File Locations**:

- Template: `wu_master_template.py` (workspace root)
- Output: `WU_Report_Results/WU_<ProcessName>_Report_YYYYMMDD.xlsx`
- Temp scripts: `Temp/` folder (disposable generation scripts)

**Critical Rule**: Template receives fully analyzed data. Do NOT put analysis logic in template code.

## wu_data Dictionary Structure

### Complete Schema

The `wu_data` dictionary MUST follow this exact structure for compatibility with `wu_master_template.py`:

```python
wu_data = {
    # ===== BASIC INFO (Required) =====
    'work_unit_id': str,           # "636228"
    'process_name': str,           # "CISOutboundIntegration"
    'status': str,                 # "SUCCESS" or "FAILED"
    
    # ===== DASHBOARD DATA =====
    'info_data': [                 # List of [Metric, Value, Status, Rating]
        ["Total Duration", "18.5s", "✅ Pass", "Excellent"],
        ["Memory Usage", "45.2 MiB", "✅ Pass", "Good"],
        ["CPU Time", "12.3s", "✅ Pass", "Good"],
        ["Error Count", "0", "✅ Pass", "Excellent"],
    ],
    
    'chart_data': {                # Dictionary of chart datasets
        'status': [                # Pie chart: (label, count)
            ("Success", 1), 
            ("Failed", 0)
        ],
        'memory_by_activity': [    # Bar chart: (activity, memory_mib)
            ("Activity1", 100.5), 
            ("Activity2", 45.2)
        ]
    },
    
    # ===== ACTIVITY TIMELINE =====
    'activities': [                # List of activity dictionaries
        {
            'name': str,           # "ProcessInvoice"
            'type': str,           # START, LM, ASSGN, BRANCH, UA, EMAIL, etc.
            'start_time': str,     # ISO timestamp "2024-01-15T10:30:45"
            'end_time': str,       # ISO timestamp or "N/A" if not completed
            'duration': str,       # "1.2s", "45ms", "N/A"
            'status': str          # "Completed", "Error", "In Progress"
        }
    ],
    
    # ===== PERFORMANCE METRICS =====
    'metrics': {
        'duration_ms': int,        # Total execution time in milliseconds
        'memory_mib': float,       # Peak memory usage in MiB
        'cpu_time_ms': int,        # CPU time in milliseconds
        'user_time_ms': int        # User time in milliseconds
    },
    
    # ===== ERROR ANALYSIS =====
    'errors': [                    # List of error dictionaries
        {
            'activity': str,       # Activity where error occurred
            'type': str,           # "JavaScript Error", "FSM Error", "Timeout"
            'message': str,        # Full error message
            'severity': str,       # "Critical", "High", "Medium", "Low"
            'impact': str          # Business impact description
        }
    ],
    
    # ===== JAVASCRIPT REVIEW (10 columns) =====
    'js_issues': [                 # List of lists (10 columns each)
        [
            work_unit_id,          # str: "636228"
            activity,              # str: "ProcessData"
            block,                 # str: "Block 1"
            issue_type,            # str: "ES5 Compliance"
            severity,              # str: "High"
            line,                  # str: "15"
            code_snippet,          # str: "const x = 5;"
            root_cause,            # str: "ES6 const not supported"
            specific_fix_es5,      # str: "var x = 5;"
            prevention             # str: "Use var for all variables"
        ]
    ],
    
    # ===== SQL REVIEW (10 columns) =====
    'sql_issues': [                # List of lists (10 columns each)
        [
            work_unit_id,          # str: "636228"
            activity,              # str: "QueryData"
            query_type,            # str: "SELECT"
            sql_snippet,           # str: "SELECT * FROM table"
            severity,              # str: "Medium"
            issue,                 # str: "SELECT * inefficient"
            root_cause,            # str: "Retrieves unnecessary columns"
            recommendation,        # str: "Specify column names"
            compass_compatible,    # str: "Yes"
            performance_impact     # str: "Medium"
        ]
    ],
    
    # ===== MEMORY ANALYSIS (7 columns) =====
    'memory_analysis': [           # List of lists (7 columns each)
        [
            work_unit_id,          # str: "636228"
            activity,              # str: "ProcessData"
            type,                  # str: "LM" or "ASSGN"
            memory_mib,            # float: 45.2
            duration_ms,           # int: 1200
            efficiency,            # float: 35.4 (percentage)
            rating                 # str: "Good"
        ]
    ],
    
    # ===== RECOMMENDATIONS (10 columns) =====
    'recommendations': [           # List of lists (10 columns each)
        [
            priority,              # str: "High"
            category,              # str: "Performance"
            issue_description,     # str: "Slow query execution"
            affected_wus,          # str: "636228, 636229"
            root_cause,            # str: "Missing index on lookup field"
            specific_fix,          # str: "Add index to field X"
            code_example_es5,      # str: ES5 code example
            testing_steps,         # str: "1. Deploy index 2. Test query"
            effort,                # str: "Low"
            impact                 # str: "High"
        ]
    ],
    
    # ===== TECHNICAL ANALYSIS (3-column tables) =====
    'architecture_analysis': [     # List of [Aspect, Value, Assessment]
        ["Aspect", "Value", "Assessment"],  # Header row
        ["Design Pattern", "File Processing", "Standard pattern for batch processing"],
        ["Service Classification", "Integration", "Connects external systems"],
    ],
    
    'js_quality_analysis': [       # List of [Metric, Score, Assessment]
        ["Metric", "Score", "Assessment"],  # Header row
        ["ES5 Compliance", "85", "Good - minor issues with ternary operators"],
        ["Security Score", "90", "Excellent - no critical vulnerabilities"],
    ],
    
    'business_impact': [           # List of [Factor, Value, Assessment]
        ["Factor", "Value", "Assessment"],  # Header row
        ["Failure Impact", "High", "Blocks downstream GL posting"],
        ["Recovery Time", "15 min", "Manual intervention required"],
    ]
}
```

### ES5 JavaScript Requirements

**CRITICAL**: IPA executes JavaScript in ES5 environment. All fix recommendations MUST use ES5 syntax.

| Feature | ES5 (Required) | ES6+ (Forbidden) |
|---------|----------------|------------------|
| Variables | `var x = 1;` | `let x = 1;` `const x = 1;` |
| Functions | `function f() {}` | `() => {}` `async/await` |
| Strings | `"Hello " + name` | `` `Hello ${name}` `` |
| Null checks | `typeof x !== "undefined"` | Optional chaining `x?.prop` |
| Arrays | `Array.prototype.slice.call(args)` | Spread `...args` |
| Objects | `{key: value}` | Shorthand `{key}` |
| Loops | `for (var i = 0; i < n; i++)` | `for...of` `arr.forEach()` |

**Example ES5 Fix**:

```javascript
// ❌ WRONG (ES6)
const processData = (items) => {
    return items.filter(x => x.active);
};

// ✅ CORRECT (ES5)
var processData = function(items) {
    var result = [];
    for (var i = 0; i < items.length; i++) {
        if (items[i].active) {
            result.push(items[i]);
        }
    }
    return result;
};
```

## Excel Report Standards

### Technology Stack

**Required Libraries**:

- `openpyxl`: Excel file manipulation
- `pandas`: Data frame operations (10-50x faster than manual cell writes)

**Performance**: Use pandas DataFrames for bulk data writes, openpyxl for styling.

### Standard Report Structure (9 Sheets)

All WU analysis reports MUST include these sheets in order:

1. **Summary Dashboard** - Executive overview with key metrics and charts
2. **Activity Timeline** - Chronological execution log (7 columns)
3. **Performance Metrics** - Duration, memory, CPU analysis (7 columns)
4. **Error Analysis** - Errors, severity, and impact (6 columns)
5. **JavaScript Review** - ES5 compliance and code quality (10 columns)
6. **SQL Review** - Data Fabric/Compass SQL queries (10 columns)
7. **Memory Analysis** - Memory usage by activity (7 columns)
8. **Recommendations** - Actionable fixes with code examples (10 columns)
9. **Technical Analysis** - Architecture, JS quality, business impact (3-column tables)

### Formatting Standards

**Header Styling**:

- Background: Infor blue (#0066CC)
- Font: White, bold
- Alignment: Center

**Status Color Coding**:

| Status | Background | Font | Use Case |
|--------|------------|------|----------|
| Success/Pass | Green (#C6EFCE) | Black | Metrics within threshold |
| Warning | Yellow (#FFEB9C) | Black | Approaching threshold |
| Error/Critical | Red (#FFC7CE) | White | Exceeds threshold or errors |

**Cell Reference Syntax**: Always use `cell(row=X, column=Y)` format (NOT `ws['A1']`)

**Column Widths**: Auto-adjust based on content (minimum 12, maximum 50)

**Additional Features**:

- Sortable headers (freeze top row)
- Conditional formatting for thresholds
- Text wrapping for long content
- Borders for table structure

### Color Thresholds

**Memory Usage**:

- Green: <70,000 MiB
- Yellow: 70,000-90,000 MiB
- Red: >90,000 MiB (white font)

**Duration**:

- Green: ≤60 seconds
- Yellow: 60-300 seconds
- Red: >300 seconds (white font)

**Priority Levels**:

- Critical: Red background, white font
- High: Orange background, black font
- Medium: Yellow background, black font
- Low: Green background, black font

## Sheet-Specific Details

### 1. Summary Dashboard

**Layout Structure**:

- Key Info: A3:D15 (Process name, WU ID, status, timestamps, metrics)
- Charts: F3:K15 (Pie chart at F4, Bar chart at I4)
- Analysis Tables: A17:K25 (Architecture, JS quality, business impact)

**Required Charts**:

1. **Pie Chart** (F4): Process Status distribution
   - Data: Success count vs Failed count
   - Colors: Green for success, Red for failed

2. **Bar Chart** (I4): Memory by Activity
   - Data: Activity names vs Memory (MiB)
   - Sorted by memory descending

**Tenant Display**: Show full tenant ID (e.g., "VWF68LHJUP5D6NUB-TRN")

**Outlier Detection**: Use IQR (Interquartile Range) method for identifying performance outliers

### 2. Activity Timeline (7 columns)

**Column Structure**:

1. Work Unit ID (str)
2. Activity (str)
3. Type (str) - START, LM, ASSGN, BRANCH, UA, EMAIL, etc.
4. Start Time (ISO timestamp)
5. End Time (ISO timestamp or "N/A")
6. Duration (str) - "1.2s", "45ms", "N/A"
7. Status (str) - "Completed", "Error", "In Progress"

**Critical Rules**:

- End time: Use actual timestamp if available, otherwise "N/A"
- Status: Extract from log context (look for error indicators)
- Duration: Calculate from timestamps, format with appropriate unit

### 3. Performance Metrics (7 columns)

**Column Structure**:

1. Work Unit ID
2. Metric Name
3. Value
4. Unit
5. Threshold
6. Status (Pass/Warning/Fail)
7. Rating (Excellent/Good/Fair/Poor)

**Display Requirements**:

- Memory: Always in MiB (not bytes)
- CPU/User time: Show actual values from metrics (not calculated)
- Include comparison to baseline/threshold

### 4. Error Analysis (6 columns)

**Column Structure**:

1. Work Unit ID
2. Activity
3. Error Type
4. Message
5. Severity
6. Impact

**Conditional Formatting**:

- Red highlighting: Only when FSM error count >0
- Font: White on red background for critical errors
- Yellow: Warnings and medium severity
- No highlighting: Informational messages

### 5. JavaScript Review (10 columns)

**Column Structure**:

1. Work Unit ID
2. Activity
3. Block (e.g., "Block 1", "Block 2")
4. Issue Type (ES5 Compliance, Performance, Security, Code Quality)
5. Severity (Critical, High, Medium, Low)
6. Line Number
7. Code Snippet (problematic code)
8. Root Cause (why it's an issue)
9. Specific Fix (ES5) (exact replacement code)
10. Prevention (how to avoid in future)

**Critical Requirements**:

- All fixes MUST be ES5-compliant
- Include line numbers for traceability
- Show before/after code snippets
- Explain WHY the issue matters

### 6. SQL Review (10 columns)

**Column Structure**:

1. Work Unit ID
2. Activity
3. Query Type (SELECT, INSERT, UPDATE, DELETE)
4. SQL Snippet (first 100 chars)
5. Severity
6. Issue
7. Root Cause
8. Recommendation
9. Compass Compatible (Yes/No)
10. Performance Impact (High/Medium/Low)

**Special Considerations**:

- Show consolidated query count per WU
- Recognize Data Fabric CSV-based API processes positively
- Flag non-Compass SQL syntax
- Identify missing indexes, inefficient joins

### 7. Memory Analysis (7 columns)

**Column Structure**:

1. Work Unit ID
2. Activity
3. Type (LM, ASSGN, etc.)
4. Memory (MiB)
5. Duration (ms)
6. Efficiency (%)
7. Rating

**Calculations**:

- Efficiency: `(1 - memory_used/70000) * 100`
- Rating: Node-type specific thresholds
  - LM nodes: >50 MiB = Poor
  - ASSGN nodes: >30 MiB = Poor

**Display Requirements**:

- Show actual peak memory node (e.g., "Assign8560")
- Sort by memory descending
- Highlight inefficient activities

### 8. Recommendations (10 columns)

**Column Structure**:

1. Priority (Critical/High/Medium/Low)
2. Category (Performance/Security/Code Quality/Architecture)
3. Issue Description (what's wrong)
4. Affected Work Units (comma-separated IDs)
5. Root Cause Analysis (WHY it's happening)
6. Specific Fix Required (exact implementation steps)
7. Code Examples (before/after ES5 code)
8. Testing Steps (validation procedures)
9. Effort (Low/Medium/High)
10. Impact (Critical/High/Medium/Low)

**Formatting**:

- Enable text wrap for columns 3, 5, 6, 7, 8
- Color-code priority column
- Sort by priority (Critical first)

**Recommendation Labels**:

- ✅ RECOMMENDED: Keep current implementation (best practice)
- 🔍 OPTIONAL: Monitoring/infrastructure improvements
- ⚠️ CONSIDER: Evaluate business need, then implement if justified

### 9. Technical Analysis (3-column tables)

**Three Separate Tables**:

1. **Process Architecture** (3 columns: Aspect, Value, Assessment)
   - Design patterns used
   - Service classification
   - Auto-restart compliance
   - Activity count
   - Flow patterns
   - Configuration dependencies

2. **JavaScript Code Quality Scores** (3 columns: Metric, Score, Assessment)
   - ES5 Compliance Score (0-100)
   - Security Score (0-100)
   - Performance Score (0-100)
   - Code Quality Score (0-100)

3. **Business Impact** (3 columns: Factor, Value, Assessment)
   - Process purpose
   - Failure impact
   - Downstream systems
   - Data integrity
   - Recovery time
   - Business continuity

**Color Coding**:

- Red: Critical issues or non-compliance
- Yellow: Warnings or areas for improvement
- Green: Compliant or best practices followed

## Python Script Template

### Standard Script Structure

All WU report generation scripts MUST follow this template:

```python
#!/usr/bin/env python3
"""
Work Unit Report Generation Script
Analyzes WU log and generates Excel report using wu_master_template.py
"""

import sys
import openpyxl
import pandas as pd
from pathlib import Path

# Add workspace root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from wu_master_template import generate_report

def analyze_wu_log(log_path):
    """
    Analyze work unit log file and extract data
    
    Args:
        log_path: Path to WU log file
        
    Returns:
        wu_data dictionary with analyzed data
    """
    # Read and parse log file
    with open(log_path, 'r', encoding='utf-8') as f:
        log_content = f.read()
    
    # Extract and analyze data
    wu_data = {
        'work_unit_id': '12345',
        'process_name': 'ProcessName',
        'status': 'SUCCESS',
        # ... build complete wu_data structure
    }
    
    return wu_data

def main():
    """Main execution function"""
    # Analyze log
    wu_data = analyze_wu_log('WU_Logs/12345_log.txt')
    
    # Generate report
    output_path = generate_report(wu_data)
    
    print(f"✓ Report generated: {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Script Requirements

**Mandatory Elements**:

1. Shebang: `#!/usr/bin/env python3`
2. Docstring: Module-level description
3. Import resolution: `sys.path.append()` for workspace root
4. Main guard: `if __name__ == "__main__":`
5. Exit code: `sys.exit(main())`

**File Location**: Create in `Temp/` folder only (disposable scripts)

**Naming Convention**: `generate_wu_<process_name>_report.py`

## JavaScript Analysis Requirements

### Comprehensive Analysis Categories

**1. ES5 Compliance** (15 points penalty per issue)

Detect and flag these ES6+ features:

- `let` / `const` declarations
- Arrow functions `() => {}`
- Template literals `` `${var}` ``
- Classes `class MyClass {}`
- Spread operator `...args`
- Destructuring `{prop} = obj`
- Default parameters `function(x = 1)`
- Object shorthand `{prop}` instead of `{prop: prop}`

**2. Performance Issues** (10 points penalty per issue)

- `for...in` loops (use `for` loop instead)
- Nested loops (>2 levels)
- JSON parsing frequency (parse once, reuse)
- String concatenation in loops (3+ operations)
- Repeated function calls (cache results)
- Regex without optimization
- Nested conditionals (4+ levels)

**3. Code Quality Issues** (5 points penalty per issue)

- `==` instead of `===`
- Variable hoisting issues
- Unused variables
- Magic strings/numbers (use named constants)
- High function complexity (>10 branches)
- Poor naming conventions
- Missing semicolons
- Boolean string comparisons (`if (x == "true")`)

**4. Security Issues** (20 points penalty per issue)

- `eval()` usage
- `Function` constructor
- `innerHTML` manipulation
- `document.write()`
- `setTimeout` with string arguments
- Dynamic property access without validation
- Global variable pollution
- Unsafe regex patterns
- Missing input validation

**5. Best Practices**

- Missing try-catch blocks
- No default values for parameters
- Missing type checking
- Improper variable scope
- Magic numbers (use named constants)

### Analysis Output Requirements

**Overall Assessment**:

- Grade: A (90-100), B (80-89), C (70-79), D (<70)
- Total issues count
- Critical issues count (security + ES5 compliance)
- Score calculation: Start at 100, subtract penalties

**Issue Tracking**:

- Line-level tracking with exact line numbers
- Code snippets (before and after)
- Severity classification (Critical/High/Medium/Low)
- Block-by-block analysis (if multiple JS blocks)

**Error Detection**:

When runtime errors found in log:

- Classify as Critical severity
- Extract error type (ReferenceError, TypeError, SyntaxError)
- Identify exact variable/function name causing error
- Provide specific fix with correct variable name
- Include root cause analysis

**Example Error Analysis**:

```javascript
// Log shows: ReferenceError: totalAmount is not defined

// Root Cause: Variable 'totalAmount' used before declaration
// Specific Fix: Declare variable before use
var totalAmount = 0;  // Add this line before usage
```

## SQL Analysis Requirements

### Compass SQL Compliance

**Critical Rules**:

- Verify Compass SQL dialect compatibility
- Flag non-standard SQL syntax
- Check for Data Fabric specific functions
- Validate table/column naming conventions

### Performance Analysis

**Query Optimization Checks**:

1. **SELECT * usage**: Flag and recommend specific columns
2. **Missing indexes**: Identify lookup fields without indexes
3. **Inefficient joins**: Check join conditions and order
4. **Subquery optimization**: Suggest JOIN alternatives
5. **LIKE patterns**: Flag leading wildcards `LIKE '%value'`
6. **Function usage**: Identify non-sargable predicates

### Data Fabric Integration

**Positive Recognition**:

- CSV-based API processes (efficient pattern)
- Proper pagination implementation
- Timestamp-based filtering
- Batch processing patterns

**Issue Detection**:

- Missing pagination for large datasets
- Inefficient filtering
- Unnecessary data retrieval
- Missing error handling

### SQL Review Output

**10-Column Structure** (see wu_data schema above)

**Severity Classification**:

- Critical: Query will fail or cause data corruption
- High: Significant performance impact (>5s delay)
- Medium: Moderate performance impact (1-5s delay)
- Low: Minor optimization opportunity

## Technical Analysis Requirements

### Process Architecture Analysis

**Required Assessments**:

1. **Design Patterns**:
   - File processing, API integration, batch processing, real-time
   - Pattern appropriateness for use case

2. **Service Classification**:
   - Integration, transformation, notification, reporting
   - Alignment with IPA best practices

3. **Auto-Restart Compliance**:
   - Check if auto-restart is enabled
   - Validate appropriateness (disabled for financial transactions)

4. **Activity Count**:
   - Total activities in process
   - Complexity assessment (Simple <10, Moderate 10-30, Complex >30)

5. **Flow Patterns**:
   - Linear, branching, looping, parallel
   - Error handling paths

6. **Configuration Dependencies**:
   - OAuth requirements
   - External system dependencies
   - Environment-specific settings

### JavaScript Code Quality Scores

**Four Scoring Dimensions** (0-100 scale):

1. **ES5 Compliance Score**:
   - Start at 100
   - Subtract 15 points per ES6+ feature
   - Minimum score: 0

2. **Security Score**:
   - Start at 100
   - Subtract 20 points per security issue
   - Critical issues: eval, Function constructor, innerHTML
   - Minimum score: 0

3. **Performance Score**:
   - Start at 100
   - Subtract 10 points per performance issue
   - Consider: loops, string ops, JSON parsing, regex
   - Minimum score: 0

4. **Code Quality Score**:
   - Start at 100
   - Subtract 5 points per quality issue
   - Consider: naming, complexity, unused vars, magic numbers
   - Minimum score: 0

**Assessment Labels**:

- 90-100: Excellent
- 80-89: Good
- 70-79: Fair
- 60-69: Poor
- <60: Critical

### Business Impact Analysis

**Required Assessments**:

1. **Process Purpose**: Clear description of business function
2. **Failure Impact**: What happens if process fails (High/Medium/Low)
3. **Downstream Systems**: Systems depending on this process
4. **Data Integrity**: Risk to data consistency
5. **Recovery Time**: Time to manually recover from failure
6. **Business Continuity**: Impact on business operations

**Color Coding**:

- Red: Critical impact, immediate attention required
- Yellow: Moderate impact, plan remediation
- Green: Low impact, monitor only

## Recommendations Requirements

### 10-Column Structure

See wu_data schema for exact column definitions.

### Recommendation Quality Standards

**Priority Classification**:

- **Critical**: Security vulnerabilities, data corruption risks, process failures
- **High**: Performance issues causing >5s delays, ES5 compliance blocking deployment
- **Medium**: Code quality issues, minor performance optimizations
- **Low**: Style improvements, documentation updates

**Root Cause Analysis**:

- Explain WHY the issue exists
- Identify contributing factors
- Reference specific code locations

**Specific Fix Requirements**:

- Exact implementation steps (not vague suggestions)
- Include variable names, function names, line numbers
- Provide complete code examples
- Specify configuration changes if needed

**Code Examples**:

- Show before/after code
- MUST be ES5-compliant
- Include comments explaining changes
- Test that examples are syntactically correct

**Testing Steps**:

- Specific validation procedures
- Expected outcomes
- Rollback procedures if needed

**Effort Estimation**:

- Low: <1 hour, simple code change
- Medium: 1-4 hours, moderate refactoring
- High: >4 hours, significant redesign

**Impact Assessment**:

- Critical: Prevents failures, fixes security issues
- High: Significant performance improvement (>50%)
- Medium: Moderate improvement (10-50%)
- Low: Minor improvement (<10%)

### Recommendation Labels

**✅ RECOMMENDED**: Keep current implementation

- Used when code follows best practices
- No changes needed
- Acknowledge good patterns

**🔍 OPTIONAL**: Monitoring/infrastructure improvements

- Non-critical enhancements
- Infrastructure changes (logging, monitoring)
- Nice-to-have optimizations

**⚠️ CONSIDER**: Evaluate business need, then implement

- Requires business decision
- Cost/benefit analysis needed
- May have trade-offs

## Process Pattern Examples

### Purpose

Reference patterns from real-world IPA processes to guide analysis and set benchmarks.

### GLAgriBankInterface

**Process Type**: Agricultural banking GL transaction interface

**Key Characteristics**:

- **Input**: File-based processing from `/InProgress` directory
- **Organization**: Multi-entity (FCIL organization structure)
- **Transaction Types**: Loans, payments, fees, accruals
- **GL Integration**: Real-time GL creation and posting
- **Auto-Restart**: Disabled (financial integrity requirement)
- **JavaScript**: ES5-compliant with OAuth2 authentication

**Performance Benchmarks**:

- Processing speed: 2-10 MB/s
- GL records created: 171 records per run
- File size: ~201 KB processed in ~1 second
- Error rate: 0% (production stable)

**Analysis Insights**:

- Auto-restart disabled is CORRECT for financial transactions
- OAuth2 implementation follows best practices
- File processing pattern is standard and efficient

### Currency Exchange Rate Export

**Process Type**: GEOSYNTEC_INT_N-0004_DailyCurrencyExchangeRateExport_Outbound

**Key Characteristics**:

- **Schedule**: Daily automated export
- **Pagination**: 30 records per page
- **Output Format**: CSV with quoted fields
- **Currency Pairs**: 15+ pairs supported
- **Notifications**: Email notifications on completion
- **Filtering**: Timestamp-based incremental export

**Performance Benchmarks**:

- Query time per page: 48-85ms
- Processing time per record: 2-16ms
- Total rates exported: 90+ rates
- Error rate: 0% (production stable)

**Analysis Insights**:

- Pagination prevents memory issues with large datasets
- Timestamp filtering ensures incremental updates
- CSV format with quoting handles special characters

### EmPowerGLInterface

**Process Type**: Empower GL journal entry processing

**Key Characteristics**:

- **Authentication**: OAuth2 with CloudSuite
- **Routing**: Dynamic FEG (Financial Entity Group) routing
- **Input Parsing**: CSV parsing with regex validation
- **Processing**: JSON batch processing
- **Transaction Types**: ACH disbursements and receipts
- **Multi-Entity**: Dynamic credentials per entity

**Performance Benchmarks**:

- OAuth2 token acquisition: Fast (<500ms)
- Regex parsing: Efficient pattern matching
- JSON processing: Optimized batch operations
- Cleanup: Automatic file cleanup after processing

**Analysis Insights**:

- OAuth2 implementation is production-ready
- Dynamic routing pattern is reusable
- Regex validation prevents malformed data
- Automatic cleanup prevents disk space issues

### Using Pattern Examples

**When analyzing WU logs**:

1. **Identify pattern**: Match process to similar pattern above
2. **Compare benchmarks**: Evaluate performance against reference
3. **Apply insights**: Use pattern-specific best practices
4. **Flag deviations**: Note significant differences from pattern

**Example Analysis**:

```text
Process: GLInterface_NewClient
Pattern Match: GLAgriBankInterface (financial transaction interface)

Comparison:
- Auto-restart: Enabled ⚠️ (should be disabled for financial)
- Processing speed: 0.5 MB/s ⚠️ (below 2-10 MB/s benchmark)
- Error rate: 2% ⚠️ (above 0% benchmark)

Recommendations:
1. Disable auto-restart (financial integrity)
2. Investigate slow processing (50% below benchmark)
3. Review error handling (2% error rate unacceptable)
```
