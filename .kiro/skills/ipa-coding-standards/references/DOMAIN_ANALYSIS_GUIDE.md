# Domain Analysis Guide

Domain-specific analysis patterns for IPA Coding Standards.

## External Knowledge Sources

For deep domain expertise, reference these steering files during analysis:

- **JavaScript ES5**: `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` (Section: JavaScript ES5 Compliance)
- **Compass SQL**: `.kiro/steering/06_Compass_SQL_CheatSheet.md` (Complete SQL dialect reference)
- **Process Patterns**: `.kiro/steering/04_Process_Patterns_Library.md` (450+ real-world examples)
- **FSM/Landmark**: `.kiro/steering/07_FSM_Business_Classes_and_API.md` (Business class patterns)

## Overview

The IPA Coding Standards skill analyzes 5 domains separately to prevent context overload and ensure comprehensive coverage.

## Domain 1: Naming Conventions

### What to Analyze

- **Filename format**: Must match process type pattern
- **Node captions**: Must be descriptive, not generic
- **Config set names**: Must include vendor/system name
- **Hardcoded values**: Should use ${ConfigSet.Variable} syntax

### Analysis Patterns

**Rule 1.1.1: Filename Format**

Approval Workflow: `<Prefix>_WF_<Description>.lpd`
Interface Process: `<Prefix>_INT_<Source>_<Dest>_<Description>.lpd`
Scheduled Process: `<Prefix>_SCH_<Description>.lpd`

**Rule 1.1.2: Node Naming**

Generic (violation): "Assign 1", "Branch 1", "WebRun 1"
Descriptive (compliant): "Calculate Total Amount", "Route to Manager", "Call Approval API"

**Rule 1.4.1: Config Set Naming**

Generic (violation): "Config", "Settings"
Vendor-specific (compliant): "Hyland_OnBase_Config", "Infor_FSM_Settings"

**Rule 1.4.3: Hardcoded Values**

Hardcoded (violation): `var apiUrl = "https://api.example.com"`
Config-based (compliant): `var apiUrl = "${API.BaseURL}"`

### Project Standards Override

If `project_standards.json` contains naming rules, they take precedence over steering defaults.

Example:
```json
{
  "rule_id": "1.1.1",
  "pattern": "<Client>_<Type>_<Description>.lpd",
  "severity": "High"
}
```

## Domain 2: JavaScript ES5 Compliance

### What to Analyze

- **ES6 features**: let, const, arrow functions, template literals, destructuring
- **Performance patterns**: Regex compilation in loops, string concatenation
- **Function order**: Functions declared before use
- **Variable scoping**: var keyword in Assign nodes, no var on Start node

### Analysis Patterns

**ES5 Compliance**

ES6 (violation):
```javascript
let x = 10;
const y = 20;
const add = (a, b) => a + b;
```

ES5 (compliant):
```javascript
var x = 10;
var y = 20;
function add(a, b) { return a + b; }
```

**Variable Scoping**

Start Node (compliant - no var keyword):
```javascript
vApproverList = "";
vTotalAmount = 0;
```

Assign Node (compliant - with var keyword):
```javascript
var tempArray = data.split(',');
var sum = 0;
```

Assign Node (violation - missing var):
```javascript
tempArray = data.split(',');  // Creates unintended global
```

**Performance Patterns**

Regex in loop (violation):
```javascript
for (var i = 0; i < items.length; i++) {
    if (items[i].match(/pattern/)) { }
}
```

Regex compiled once (compliant):
```javascript
var pattern = /pattern/;
for (var i = 0; i < items.length; i++) {
    if (pattern.test(items[i])) { }
}
```

### Project Standards Override

If `project_standards.json` contains JavaScript rules, they take precedence.

## Domain 3: SQL Queries

### What to Analyze

- **Pagination**: Required for queries returning >100 rows
- **Compass SQL**: Use Compass API, not direct SQL
- **SELECT ***: Avoid, specify columns
- **WHERE clauses**: Required for UPDATE/DELETE

### Analysis Patterns

**Rule 1.5.2: Pagination**

No pagination (violation):
```sql
SELECT * FROM APINVOICE
```

With pagination (compliant):
```sql
SELECT * FROM APINVOICE LIMIT 100 OFFSET 0
```

**Compass SQL**

Direct SQL (violation):
```sql
SELECT * FROM EMPLOYEE WHERE EMP_ID = '12345'
```

Compass API (compliant):
```javascript
var query = "Employee?filter=EmployeeId eq '12345'&select=EmployeeId,Name,Department";
```

**SELECT ***

SELECT * (violation):
```sql
SELECT * FROM APINVOICE
```

Specific columns (compliant):
```sql
SELECT INVOICE_NUM, VENDOR, AMOUNT FROM APINVOICE
```

### Project Standards Override

If `project_standards.json` contains SQL rules, they take precedence.

## Domain 4: Error Handling

### What to Analyze

- **OnError tabs**: Required for error-prone activities (WEBRN, WEBRUN, ACCFIL)
- **stopOnError flag**: Should be false for activities with OnError tabs
- **GetWorkUnitErrors**: Required activity node for error reporting
- **Error coverage**: Percentage of error-prone activities with error handling

### Analysis Patterns

**Rule 1.3.1: OnError Tabs**

No OnError tab (violation):
```xml
<activity type="WEBRN" stopOnError="true">
  <!-- No OnError tab -->
</activity>
```

With OnError tab (compliant):
```xml
<activity type="WEBRN" stopOnError="false">
  <onError>
    <!-- Error handling logic -->
  </onError>
</activity>
```

**Rule 1.3.2: GetWorkUnitErrors**

Missing (violation): No GetWorkUnitErrors activity in process

Present (compliant): GetWorkUnitErrors activity exists and is used

### Project Standards Override

If `project_standards.json` contains error handling rules, they take precedence.

## Domain 5: Process Structure

### What to Analyze

- **Auto-restart configuration**: Appropriate for process type
- **Process type**: Approval, Interface, Scheduled, etc.
- **Activity distribution**: Balance of activity types

### Analysis Patterns

**Auto-Restart Appropriateness**

Context-aware analysis:
- Approval workflows: Auto-restart usually NOT appropriate (user interaction)
- Interface processes: Auto-restart usually appropriate (automated)
- Scheduled processes: Auto-restart usually appropriate (automated)

**Process Type Determination**

Based on characteristics:
- User interaction activities → Approval Workflow
- File access + web services → Interface Process
- Timer activities → Scheduled Process

### Project Standards Override

If `project_standards.json` contains structure rules, they take precedence.

## Incremental Processing

For large processes, domains are processed in chunks:

- **Naming**: 50 nodes per chunk
- **JavaScript**: 20 JS blocks per chunk
- **SQL**: 30 queries per chunk
- **Error Handling**: 40 activities per chunk
- **Structure**: Direct analysis (small dataset)

Each chunk is analyzed separately, then results are merged.

## AI Output Format

Each domain analysis should return JSON array of violations:

```json
[
  {
    "rule_id": "1.1.1",
    "severity": "High",
    "finding": "Filename does not match approval workflow pattern",
    "current": "ProcessName.lpd",
    "recommendation": "Rename to <Prefix>_WF_<Description>.lpd",
    "activities": "N/A (filename)",
    "domain": "naming"
  }
]
```

---

For more information, see:
- [`CODING_STANDARDS_REFERENCE.md`](CODING_STANDARDS_REFERENCE.md) - Complete rules reference
- [`JSON_SCHEMAS.md`](JSON_SCHEMAS.md) - JSON structure details
