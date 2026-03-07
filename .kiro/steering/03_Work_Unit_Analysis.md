---
inclusion: auto
name: work-unit-analysis
description: Work unit log analysis, error patterns, IPA process execution, activity logs, approval workflows. Use when analyzing work unit logs, troubleshooting IPA process failures, generating work unit reports, or conducting peer reviews.
---

# Work Unit Analysis Guide

## Table of Contents

- [Quick Reference](#quick-reference)
- [Critical Timestamp Format](#critical-timestamp-format)
- [Work Unit Types](#work-unit-types)
- [Log Structure](#log-structure)
- [Error Pattern Quick Reference](#error-pattern-quick-reference)
- [Detailed Error Patterns](#detailed-error-patterns)
- [Success Patterns](#success-patterns)
- [Performance Analysis](#performance-analysis)
- [JavaScript Engine (ES5)](#javascript-engine-es5)
- [Analysis Tools](#analysis-tools)
- [Bulk Data Processing](#bulk-data-processing)
- [Analysis Methodology](#analysis-methodology)
- [Data Tracing](#data-tracing)
- [Automated Log Collection](#automated-log-collection)

## Quick Reference

### Common Analysis Tasks

| Task                        | Tool/Approach                                    |
|-----------------------------|--------------------------------------------------|
| Extract performance metrics | `ReusableTools/IPA_Analyzer/extract_wu_log.py`  |
| Generate Excel report       | `wu_master_template.py`                          |
| Identify error patterns     | Search for error signatures in log               |
| Calculate activity duration | Parse timestamps with `%m/%d/%Y %I:%M:%S.%f %p`  |
| Check ES5 compliance        | Review JavaScript blocks for ES6+ features       |

### Error Signature Quick Lookup

| Error Signature                         | Pattern #          | Severity    |
|-----------------------------------------|--------------------|-------------|
| `No valid users [] or tasks []`         | #1, #9, #10, #13   | Critical    |
| `Row not found: Unable to lock row`     | #2, #14            | High        |
| `ReferenceError: "..." is not defined`  | #6, #7, #12        | Medium-High |
| `Source file(s)/folder(s) do not exist` | #11                | High        |
| `Access denied for ... on ...`          | #15                | High        |
| `All branch conditions false`           | #16                | Medium      |
| `client is closed`                      | #5                 | Medium      |
| `Timeout escalation`                    | #4                 | Medium      |
| `Error occurred while reading input file` | #18              | High        |

## Critical Timestamp Format

**MANDATORY**: IPA logs use `MM/DD/YYYY HH:MM:SS.mmm AM/PM` format for ALL timestamps.

**Correct Parsing**:

```python
from datetime import datetime

start_dt = datetime.strptime(start_time, '%m/%d/%Y %I:%M:%S.%f %p')
end_dt = datetime.strptime(end_time, '%m/%d/%Y %I:%M:%S.%f %p')
duration_ms = int((end_dt - start_dt).total_seconds() * 1000)
```

**Example**:

- Start: `08/26/2025 05:27:56.919 AM`
- End: `08/26/2025 05:27:56.920 AM`
- Duration: 1ms

**Common Mistake**: Assuming different formats for start vs end times - they are IDENTICAL.

## Work Unit Types

### FSM (Infor Financials and Supply Management)

**Characteristics**:

- Complex approval workflows with multi-level user interactions
- Financial data processing with detailed business logic
- Extensive JavaScript for calculations and data transformation
- Longer execution times (minutes to hours including user wait time)
- Rich logging with detailed activity flows

**Common Processes**:

- Approval workflows: `FPI_JournalEntryApproval`, `FPICashLedgerPaymentApproval`
- Data exports: `MatchReport_Outbound`, `GEOSYNTEC_INT_N-0004_DailyCurrencyExchangeRateExport_Outbound`
- GL interfaces: `GLAgriBankInterface`, `RepSetGLSetup_Extract`, `GeoSyntec_INT_VirtualCard_GLInterface`

### GHR (Infor Global Human Resources)

**Characteristics**:

- Simpler execution patterns with minimal logging
- Timeout-driven processes (system-initiated actions)
- Employee data operations with delta change tracking
- Shorter, more automated flows
- OAuth-based API integrations
- Security proxy configuration dependencies

**Common Processes**: `HRMEmployeeExport`, `ImmediateApprve`, `Infor-IMS-SmokeTest-Currency`

**Typical GHR Errors**:

- Timeout escalations (system dispatch for hanging processes)
- Security proxy configuration issues
- Empty OAuth/JSON service account data
- HTTP 400 errors from malformed API requests
- SMTP connectivity failures

## Log Structure

### Header Format

```text
Workunit [ID] started @ [DateTime]
    Landmark version: [Version]
    Process name: [ProcessName]
    Auto Restart: [Enabled/Disabled]
```

### Activity Structure

**Pattern**: Activities have start and completion markers with full execution details between them.

**Start Marker**: `Activity name:ActivityName type:TYPE id:N started @ [timestamp]`

**End Marker**: `Activity name:ActivityName id:N completed @ [timestamp]`

**Activity Types**:

- `START` - Process initialization
- `LM` - Landmark transaction (database operations)
- `ASSGN` - Assignment (JavaScript, variable operations)
- `BRANCH` - Conditional routing
- `UA` - User Action (approval, manual task)
- `WEBRN` - Web Run (external API calls)
- `ACCFIL` - File Access (read/write operations)
- `END` - Process completion

**Extraction Regex**:

```python
pattern = r'Activity name:([^\s]+)\s+type:(\w+)\s+id:(\d+)\s+started @ ([^\n]+)\n(.*?)(?=Activity name:|\Z)'
```

**Status Detection**: Extract from completion patterns showing "Completed", "Error", "Failed", etc.

## Error Pattern Quick Reference

| #  | Error Type           | Signature                                  | Root Cause                  | Fix Priority |
|----|----------------------|--------------------------------------------|-----------------------------|--------------|
| 1  | User Assignment      | `No valid users [] or tasks []`            | Empty actor variables       | Critical     |
| 2  | Record Not Found     | `Row not found: Unable to lock row`        | Record deleted/missing      | High         |
| 3  | JSON Parsing         | `Invalid JSON passed to JSON.parse()`      | Malformed JSON config       | Medium       |
| 4  | Timeout              | `Timeout escalation: Dispatch Action`      | Process hanging             | Medium       |
| 5  | SFTP                 | `client is closed`                         | Network connectivity        | Medium       |
| 6  | JavaScript Runtime   | `Error evaluating expression`              | Syntax/type errors          | Medium-High  |
| 7  | Undefined Variable   | `"variableName" is not defined`            | Missing variable            | Medium       |
| 8  | ES5 Compliance       | Modern JS syntax                           | ES6+ features used          | Medium       |
| 9  | Approval Config      | Empty approval actors                      | Workflow misconfiguration   | Critical     |
| 10 | JSON Approval        | Empty ActorList arrays                     | JSON config incomplete      | Critical     |
| 11 | File Transfer        | `Source file(s)/folder(s) do not exist`    | Path mismatch               | High         |
| 12 | Non-Critical JS      | ReferenceError but process continues       | Optional variables          | Low          |
| 13 | Team Approval        | Empty team member list                     | Team not populated          | Critical     |
| 14 | Record Deletion      | Row not found during approval              | Timing issue                | High         |
| 15 | Security Access      | `Access denied for ... on ...`             | Missing permissions         | High         |
| 16 | Branch Logic         | `All branch conditions false`              | Null/undefined values       | Medium       |
| 17 | Data Extraction      | Invalid lookup keys                        | Data format issues          | Medium       |
| 18 | DBImport CSV Error   | `Error occurred while reading input file`  | Malformed source CSV        | High         |

## Detailed Error Patterns

### Pattern #1: User Assignment Configuration Error (CRITICAL)

**Signature**: `UserActionConfigException: No valid users [] or tasks [] with valid users were found for assignment`

**Root Cause**: Empty actor variables in UserAction activities - CSV user list resolves to empty values (`,,,`)

**Analysis Steps**:

1. Identify the failing UserAction activity name
2. Check all actor variables:
   - `CurrentApproverActor` (individual)
   - `CurrentApproverActorList` (list)
   - `CurrentTeamActorList` (team)
   - `CurrentPositionActorList` (position)
3. Verify ApprovalProcessor configuration
4. Check approval level and escalation settings

**Resolution**: Configure proper user assignments or team membership in approval workflow.

**Example** (WU 408156): `<!CurrentApproverActor>,<!CurrentApproverActorList>,<!CurrentTeamActorList>,<!CurrentPositionActorList>` → `,,,`

### Pattern #2: Database Record Not Found

**Signature**: `Row not found: Unable to lock row. Entry with key values [KeyValues] not found`

**Root Cause**: Record deleted or missing between process steps

**Resolution**:

- Add record existence validation before operations
- Review data retention policies
- Implement graceful handling for missing records

### Pattern #3: JSON Parsing Issues

**Signature**: `Invalid JSON passed to JSON.parse()` or `SyntaxError: Empty JSON string`

**Root Cause**: Malformed JSON configuration or empty JSON strings

**Resolution**:

- Validate JSON syntax (trailing commas, quotes)
- Check for empty/null JSON variables before parsing
- Add try-catch around JSON.parse() calls

### Pattern #4: Timeout Escalation (GHR)

**Signature**: `Timeout escalation: Dispatch Action taken by system for [ID]`

**Characteristics**: Minimal log content, system-initiated action

**Root Cause**: Process execution exceeding timeout thresholds

**Resolution**:

- Optimize process performance
- Implement timeout handling
- Add monitoring and alerts

### Pattern #5: SFTP Connection Errors

**Signature**: `FileTransfer: Execution error java.io.IOException: client is closed`

**Root Cause**: Network connectivity issues during file transfer

**Resolution**:

- Implement retry logic with exponential backoff
- Add connection health checks
- Verify network/firewall configuration

### Pattern #6-8: JavaScript Errors

**Signatures**:

- `Error evaluating expression`
- `ReferenceError: "variableName" is not defined`
- `TypeError`, `SyntaxError`
- Modern JS syntax (ES6+) in ES5 environment

**Root Causes**:

- Undefined variables
- Incorrect syntax
- Type mismatches
- ES6+ features not supported

**Analysis Required**:

- Exact activity name and expression
- Specific variable names
- Root cause explanation
- Multiple fix options with code examples

**Resolution**:

- Define missing variables
- Fix syntax errors
- Convert ES6+ to ES5 (see JavaScript Engine section)
- Add null/undefined checks

### Pattern #9-10: Approval Configuration Errors

**Signature**: `UserActionConfigException` with JSON approval data

**Root Cause**: Empty arrays in JSON approval configuration

**JSON Issues**:

```json
{
  "ActorList": [],
  "TeamActorList": [],
  "Actor": "",
  "ApprovalTeam": ""
}
```

**Resolution**:

1. Review `DerivedRoutingApprovalJSON` structure
2. Populate ActorList arrays with valid user IDs
3. Configure ApprovalTeam and TeamActorList
4. Validate JSON syntax and completeness
5. Test approval routing

### Pattern #11: File Transfer Source Missing

**Signature**: `FileTransfer: Source error - Source file(s)/folder(s) do not exist`

**Root Cause**: File path mismatch between FileAccess and FTP activities

**Common Issues**:

- Mismatched file paths
- Incorrect storage location
- File naming inconsistencies
- Temporary file cleanup before transfer
- Permission issues

**Resolution**:

1. Verify FileAccess output path matches FTP source path
2. Check file naming variables for consistency
3. Validate storage location configuration
4. Add file existence validation before transfer
5. Implement retry logic

### Pattern #12: Non-Critical JavaScript Errors

**Signature**: `ReferenceError` in Start activity but process continues

**Root Cause**: Optional variables referenced but not critical to execution

**Resolution**:

- Define missing variables with defaults
- Add null/undefined checks
- Remove unused variable references
- Use try-catch for optional variables

**Note**: These errors don't prevent process completion but should be cleaned up.

### Pattern #13: Team-Based Approval Errors

**Signature**: `UserActionConfigException` with team assignment

**Root Cause**: Team name configured but `DerivedCurrentTeamActorList` is empty

**Resolution**:

1. Verify team exists and has active members
2. Check team membership derivation logic
3. Validate team membership assignments
4. Consider fallback to individual approver if team empty
5. Implement team membership validation

### Pattern #14: Record Deletion During Approval

**Signature**: `Row not found` during approval completion (after successful assignment)

**Root Cause**: Business record deleted between approval assignment and completion

**Timing Issue**: Long approval cycles allow time for record cleanup

**Resolution**:

1. Add record existence validation before approval completion
2. Implement graceful handling of missing records
3. Review data retention policies
4. Add logging for record deletion events
5. Consider approval workflow timeout policies
6. Implement record locking during approval

### Pattern #15: Security Access Denied

**Signature**: `Access denied for [ActionName] on [BusinessClass] for actor [ActorName]`

**Root Cause**: User lacks security permissions for approval action

**Resolution**:

1. Identify required security permissions
2. Grant business class permissions to approval users
3. Configure security roles for workflow participants
4. Test approval actions with assigned users
5. Consider elevated security context for processes
6. Add error handling for access denied scenarios

### Pattern #16: Branch Logic Null/Undefined Errors

**Signature**: `Branch [BranchName]: All branch conditions false` with undefined operations

**Root Cause**: Branch conditions evaluate undefined/null values from empty query results

**Resolution**:

1. Add null/undefined validation in JavaScript
2. Implement default values for empty results
3. Add branch conditions for empty/null scenarios
4. Use try-catch for variable operations
5. Validate data existence before processing

### Pattern #17: Data Extraction Key Validation Errors

**Signature**: `DoesNotExistException: [BusinessClass] does not exist` with invalid keys

**Root Cause**: Fixed-width data extraction produces invalid key values (spaces, wrong format)

**Resolution**:

1. Add data validation before lookup operations
2. Trim extracted values
3. Validate key format
4. Add error handling for invalid keys
5. Log extraction issues for debugging

### Pattern #18: DBImport File Reading Error (HIGH)

**Signature**: `Error occurred while reading input file; DBImport halted` with error code 32

**Root Cause**: Malformed CSV in source file - typically missing closing quotes on field values causing CSV parser failure

**Critical Troubleshooting Methodology**:

1. **ALWAYS check source file FIRST** - Do NOT assume IPA processing is the issue
2. Identify which record number failed (e.g., "Importing 5" means record 5)
3. Search source file for that record number
4. Look for CSV format issues:
   - Missing closing quotes: `"value|"nextfield"` instead of `"value"|"nextfield"`
   - Embedded delimiters without proper escaping
   - Unescaped quotes within quoted fields
   - Line breaks within quoted fields

**Common Mistake**: Assuming the IPA JavaScript or FileAccess activity is creating bad data, when the source file itself is corrupted.

**Example** (WU 2526):
- Error: `PayablesInvoiceImport Importing 5 Error occurred while reading input file`
- Source file line 30: `"Header"|"82784260224|"2026-02-23T09:49:25-05:00"`
- Issue: Missing closing quote after `82784260224`
- Should be: `"Header"|"82784260224"|"2026-02-23T09:49:25-05:00"`

**Resolution**:

1. Fix source system export (Coupa, external API, etc.)
2. Add CSV validation before processing
3. Consider adding CSV repair logic for known issues
4. Log source file content for debugging

**Prevention**:

- Validate source file format before IPA processing
- Add file format checks in ReadFile activity
- Implement CSV linting/validation step
- Monitor source system export quality

## Success Patterns

### Successful Approval Workflow

1. Initial Setup → Data retrieval and validation
2. User Action Created → Notification sent
3. User Response → Action received
4. Level Update → Approval advanced
5. Final Approval → Transaction completed

### Successful Data Export

1. Initialization with JavaScript functions
2. Database queries with filtering/pagination
3. Data transformation (CSV formatting)
4. File operations
5. Multi-page retrieval for large datasets
6. Clean completion

### Successful GL Interface

1. Variable initialization and file path setup
2. OAuth configuration and date formatting
3. File validation and routing
4. Data extraction from directory
5. GL transaction creation and posting
6. Clean completion

## Performance Analysis

### Activity Duration Benchmarks

- Database queries: 200ms - 2s (pagination: 48-85ms)
- User actions: Indefinite (human wait time)
- JavaScript processing: 10-50ms (data transformation: 2-16ms/record)
- File operations: 100-500ms

### Memory Thresholds

- Work Unit Limit: 100,000 MiB maximum
- Critical: >90,000 MiB
- Warning: >70,000 MiB
- Normal: <70,000 MiB

### Node-Level Thresholds

- Critical: >1,000 MiB
- Warning: >500 MiB
- Normal: <500 MiB

### Typical Memory Consumption

- Landmark activities: 100-800 MiB (highest)
- JavaScript assignments: 5-10 MiB (moderate)

## JavaScript Engine (ES5)

**Engine**: Mozilla Rhino 1.7R4 (JavaScript 1.7 with partial ES5)

**Verified**: `C:\IPDesigner\2025120460\lib\thirdParty\js.jar`

### Supported Features ✅

```javascript
// Variables
var x = 5;                    // ✅ Recommended
const y = 10;                 // ✅ Works but doesn't enforce immutability

// Functions
function myFunc() { }         // ✅ Required syntax

// Strings
var msg = 'Hello ' + name;    // ✅ Concatenation required
```

### NOT Supported ❌

```javascript
// Arrow functions
() => {}                      // ❌ Use function() {}

// Template literals
`Hello ${name}`               // ❌ Use 'Hello ' + name

// Spread operator
[...array]                    // ❌ Use Array.prototype methods

// ES6 Classes
class MyClass {}              // ❌ Use function constructors

// Destructuring
const {x, y} = obj;           // ❌ Use explicit property access
```

### Important: `const` Behavior

Rhino 1.7R4 supports `const` syntax but does NOT enforce immutability:

- ✅ Declaration works: `const x = 5;`
- ❌ Does NOT prevent reassignment
- ❌ Does NOT require initialization
- ❌ Does NOT prevent object/array modification

**Recommendation**: Use `var` for clarity about actual behavior.

**Evidence**: BayCare APIA WU 339 used `const` 4 times successfully in production.

### Common Violations to Fix

| Issue              | Wrong                  | Correct                                  |
|--------------------|------------------------|------------------------------------------|
| Arrow functions    | `() => {}`             | `function() {}`                          |
| Template literals  | `` `Hello ${name}` ``  | `'Hello ' + name`                        |
| Spread operator    | `[...arr]`             | `Array.prototype.slice.call(arr)`        |
| for...of loops     | `for (let x of arr)`   | `for (var i=0; i<arr.length; i++)`       |

### Performance Best Practices

- Prefer `for` loops over `for...in` for arrays
- Minimize `JSON.parse()` calls, cache results
- Combine `var` declarations at function top
- Use `===` for strict comparison
- Implement `try-catch` for error handling
- Use `typeof` for undefined checks

## Analysis Tools

### IPA Analyzer (`ReusableTools/IPA_Analyzer/`)

**Purpose**: Extract data from work unit logs for AI analysis

**Tools**:

- `extract_wu_log.py` - Extracts performance metrics, variables, errors → JSON
- `extract_lpd_data.py` - Extracts activities, JavaScript, config → JSON
- `extract_spec.py` - Extracts requirements from ANA-050 docs → JSON

**Workflow**:

1. Python extracts data → organized JSON files
2. Kiro reads JSON and performs analysis
3. Kiro builds analysis results
4. Python template formats results → Excel report

**Performance**: Fast extraction (~1s per 12K lines)

### WU Master Template (`wu_master_template.py`)

**Purpose**: Generate Excel reports from work unit analysis

**Features**:

- Multi-sheet reports (Summary, Activities, Performance, Errors)
- Professional formatting with color coding
- Activity timeline visualization
- Error pattern identification
- Performance metrics analysis

**Usage**:

```python
from wu_master_template import generate_report

wu_data = {
    'work_unit_id': '12345',
    'process_name': 'InvoiceApproval',
    'activities': [...],
    'errors': [...],
    'performance': {...}
}

output_path = generate_report(wu_data)
```

## Bulk Data Processing

### CIS Integration Pattern

**Challenge**: Work unit logs with millions of data records (100MB+ files)

**Solution**: Line-by-line pre-filtering during file read

**Preserved Content**:

- Activity markers (start/completion)
- Metrics sections
- Error messages
- Performance data
- Node information

**Removed Content**:

- XML/JSON data blocks
- Large result sets
- Repetitive records (10+ consecutive)
- Large parameter blocks (>1000 chars)

**Implementation**:

```python
def filter_line(line):
    # Preserve activity markers
    if 'Activity name:' in line:
        return True
    # Preserve metrics
    if '[Metrics' in line:
        return True
    # Skip data records
    if line.startswith('Record ') or line.startswith('Row '):
        return False
    return True
```

**Performance**: Reduces 100MB files to 5-10MB while preserving analysis-critical data.

## Analysis Methodology

### Step-by-Step Approach

1. **Initial Assessment**
   - Check work unit status (SUCCESS/FAILED)
   - Identify process type (FSM vs GHR)
   - Review memory usage vs 100,000 MiB limit
   - Note auto-restart configuration

2. **Activity Flow Analysis**
   - Follow chronological sequence
   - Note branch decisions and routing
   - Identify bottlenecks and delays
   - Check user action patterns

3. **Error Pattern Matching**
   - Compare with known error signatures (see Quick Reference table)
   - Identify root cause category
   - Assess impact and severity
   - Check for cascading failures

4. **Performance Analysis**
   - Review metrics section
   - Identify memory-intensive activities (>800 MiB)
   - Analyze database query performance
   - Check JavaScript execution times

5. **JavaScript Code Review**
   - Check ES5 compliance
   - Identify undefined variables
   - Review error handling
   - Assess performance patterns

6. **Root Cause Determination**
   - Correlate errors with activity flow
   - Identify configuration issues
   - Check data quality problems
   - Determine fix priority

7. **Recommendation Generation**
   - Provide specific code fixes
   - Suggest configuration changes
   - Recommend process improvements
   - Include testing requirements

## Data Tracing

### When to Use

Investigating data quality issues (zeros, nulls, missing values) in BIFSM API + Compass API data extraction processes.

### Complete Data Flow Pattern

```text
1. GLTOT Cube (d/EPM)     → Source GL balance data
2. BIFSM_LoadApi          → Loads to Infor Data Lake (IDL Object)
3. Compass API InitQuery  → Submits SQL query to Data Lake
4. GetStatus (polling)    → Waits for query completion
5. GetResult              → Retrieves query results
6. Assign (raw)           → Stores API response (quoted CSV)
7. Assign (processed)     → Cleans data (unquoted CSV)
8. WriteFile              → Writes CSV file
9. SFTP                   → Transfers to client
```

### Tracing Steps

1. **Check raw API response** (quoted format: `"FCE","value"`)
   - Count zeros in target column
   - If zeros exist here → **source data issue**

2. **Check processed data** (unquoted format: `FCE,value`)
   - Count zeros in target column
   - Compare with raw zero count

3. **Verify BIFSM_LoadApi success**
   - Look for `"Data Successfully Loaded into IDL Object"`
   - Check HTTP 200 status

4. **Identify affected period**
   - Group zeros by period column
   - Compare with known-good files

5. **Determine root cause location**
   - Raw = Processed zeros → **Source data (cube) issue**
   - Processed > Raw zeros → **IPA processing issue**
   - Client file > Processed → **Client merge issue**

### Python Analysis Pattern

```python
def count_zeros_in_column(lines, column_index, is_quoted=False):
    """Count zero values in specific column."""
    zero_count = 0
    for line in lines:
        if is_quoted:
            parts = parse_quoted_csv(line)
        else:
            parts = line.split(',')

        if len(parts) > column_index:
            value = float(parts[column_index])
            if value == 0.0:
                zero_count += 1

    return zero_count
```

## Automated Log Collection

**Tool**: `Process_Flow_Analyzer.py` - GUI application for bulk work unit log collection

**Features**:

- FSM authentication with credential management
- Process filtering and selection
- Bulk download (up to 10 work units per process)
- Organized storage with session tracking
- Real-time status logging
- Error handling and recovery

**Architecture**:

- Modular design (browser, download, database, UI components)
- Chrome WebDriver automation
- SQLite session tracking
- Professional tkinter GUI

**Use Case**: Collect multiple work unit logs per IPA process for comprehensive pattern analysis.
