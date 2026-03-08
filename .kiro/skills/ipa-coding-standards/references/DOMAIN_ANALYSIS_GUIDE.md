# Domain Analysis Guide

Domain-specific analysis patterns for IPA Coding Standards.

## External Knowledge Sources

**CRITICAL**: Before performing domain analysis, load relevant steering files for deep domain expertise.

### Required Steering Files

Load these steering files BEFORE analyzing their respective domains:

**Phase 2 (JavaScript Analysis)**:
```
discloseContext(name="ipa-ipd-guide")
```
- Contains: IPA JavaScript ES5 compliance rules, Start node global variables pattern, function declaration order

**Phase 3 (SQL Analysis)**:
```
discloseContext(name="compass-sql")
discloseContext(name="data-fabric-guide")
```
- Contains: Compass SQL dialect, Data Fabric API patterns, pagination patterns (limit/offset in URLs)

**Phase 4 (Error Handling Analysis)**:
```
discloseContext(name="ipa-ipd-guide")
```
- Contains: OnError tab requirements, GetWorkUnitErrors pattern, error-prone activity types

**Phase 5 (Structure Analysis)**:
```
discloseContext(name="process-patterns")
```
- Contains: 450+ real-world process patterns, auto-restart appropriateness by process type

### Why Load Steering Files?

Steering files contain:
- Real-world patterns from 450+ analyzed processes
- IPA-specific implementation details (Start node properties, Compass API)
- Client-specific variations and edge cases
- Production-validated best practices

**Without steering files**: Analysis relies on generic patterns and may miss IPA-specific nuances.

**With steering files**: Analysis uses production-validated patterns and catches real issues.

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

**CRITICAL: Check Start Node Properties FIRST**

Before flagging missing global variables, ALWAYS check Start node properties:

```json
{
  "id": "Start",
  "type": "START",
  "properties": {
    "queryID": "\"\"",
    "auth": "\"\"",
    "rowCount": "0"
  }
}
```

Variables defined in Start node properties are AUTOMATICALLY global (no var keyword needed).

**Variable Scoping Rules**

1. **Start Node Properties** (global variables):
   - Defined in Properties tab, NOT as JavaScript code
   - No `var` keyword needed
   - Accessible throughout entire process
   - Example: `queryID = ""`, `rowCount = 0`

2. **Assign Node WITHOUT var** (modifies global):
   - Valid IF variable exists in Start node properties
   - Invalid IF variable NOT in Start node properties (creates unintended global)

3. **Assign Node WITH var** (local variable):
   - Creates local variable scoped to that Assign node
   - Example: `var tempArray = data.split(',');`

**Analysis Workflow**:
1. Load lpd_structure.json
2. Find Start node and extract properties
3. Build list of global variables from Start node properties
4. When analyzing Assign nodes:
   - If variable assignment WITHOUT var → Check if in Start node properties
   - If in Start node properties → COMPLIANT (modifying global)
   - If NOT in Start node properties → VIOLATION (unintended global)

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

**Performance Patterns**

**CRITICAL: Verify Regex Actually Exists**

Before flagging regex compilation issues, verify the code ACTUALLY contains regex patterns:
- Look for `/pattern/` syntax
- Look for `new RegExp()` calls
- Do NOT flag string operations (`.split()`, `.replace()`, `.substring()`) as regex

Example - NO REGEX (false positive):
```javascript
function formatDate(dt) {
    var d = new Date(dt);
    var padMonth = (d.getMonth()+1).toString().length == 1 ? '0' + (d.getMonth()+1).toString() : (d.getMonth()+1).toString();
    return year + padMonth + padDay;
}
```

Example - HAS REGEX (valid violation):
```javascript
for (var i = 0; i < items.length; i++) {
    if (items[i].match(/pattern/)) { }  // Regex compiled in loop
}
```

Regex compiled once (compliant):
```javascript
var pattern = /pattern/;
for (var i = 0; i < items.length; i++) {
    if (pattern.test(items[i])) { }
}
```

### Best Practice Suggestions (Low Severity)

**CRITICAL**: Even when code is ES5 compliant and has no violations, ALWAYS provide improvement suggestions.

**Analysis Approach**:
1. Review ALL JavaScript blocks for improvement opportunities
2. Flag suggestions as "Low" severity (not violations)
3. Focus on code quality, maintainability, and performance
4. Provide specific examples and recommendations

**Categories for Suggestions**:

**1. Code Organization and Readability**

Look for:
- Long functions (>50 lines) that could be split
- Complex nested conditionals that could be simplified
- Magic numbers without explanation
- Inconsistent formatting or indentation
- Poor variable naming (single letters, abbreviations)

Example suggestion:
```json
{
  "rule_id": "2.9.1",
  "severity": "Low",
  "finding": "Function formatDate2 is 65 lines long and handles multiple responsibilities",
  "current": "Single function handles date formatting, padding, and validation",
  "recommendation": "Consider splitting into smaller functions: padNumber(), validateDate(), formatDate()",
  "activities": "Assign1540",
  "domain": "javascript"
}
```

**2. Performance Optimizations**

Look for:
- String concatenation in loops (use array.join())
- Repeated property access (cache in variable)
- Inefficient array operations
- Unnecessary type conversions

Example suggestion:
```json
{
  "rule_id": "2.9.2",
  "severity": "Low",
  "finding": "String concatenation using += operator in loop",
  "current": "for (var i=0; i<arr.length; i++) { result += arr[i]; }",
  "recommendation": "Use array.join() for better performance: result = arr.join('')",
  "activities": "Assign7960",
  "domain": "javascript"
}
```

**3. Error Handling Patterns**

Look for:
- Missing try-catch blocks for JSON.parse()
- No validation before accessing object properties
- Silent failures without logging

Example suggestion:
```json
{
  "rule_id": "2.9.3",
  "severity": "Low",
  "finding": "JSON.parse() without error handling",
  "current": "var obj = JSON.parse(InitQuery_result);",
  "recommendation": "Add try-catch: try { var obj = JSON.parse(InitQuery_result); } catch(e) { /* handle error */ }",
  "activities": "Assign4580",
  "domain": "javascript"
}
```

**4. Code Maintainability**

Look for:
- Duplicate code blocks (DRY principle)
- Hardcoded values that should be constants
- Complex expressions that need comments
- Inconsistent patterns across similar operations

Example suggestion:
```json
{
  "rule_id": "2.9.4",
  "severity": "Low",
  "finding": "Duplicate date formatting logic across multiple activities",
  "current": "formatDate() and formatDate2() have similar logic with slight variations",
  "recommendation": "Consolidate into single function with parameters for format type",
  "activities": "Assign1540, Filename",
  "domain": "javascript"
}
```

**5. Modern ES5 Patterns**

Look for:
- Opportunities to use Array methods (map, filter, reduce) instead of loops
- Better use of ternary operators for simple conditionals
- Improved use of logical operators for default values

Example suggestion:
```json
{
  "rule_id": "2.9.5",
  "severity": "Low",
  "finding": "Manual array iteration could use Array.filter()",
  "current": "for loop with if condition to filter array",
  "recommendation": "Use arr.filter(function(item) { return condition; }) for cleaner code",
  "activities": "Assign7960",
  "domain": "javascript"
}
```

**When to Generate Suggestions**:
- ALWAYS generate 3-5 suggestions per process (even if ES5 compliant)
- Focus on most impactful improvements first
- Provide specific code examples in recommendations
- Reference actual activity IDs where improvements apply

**When NOT to Generate Suggestions**:
- Don't suggest ES6 features (arrow functions, let/const, template literals)
- Don't flag intentional design choices without clear benefit
- Don't suggest changes that would break IPA compatibility

### Project Standards Override

If `project_standards.json` contains JavaScript rules, they take precedence.

## Domain 3: SQL Queries

### What to Analyze

- **Pagination**: Required for queries returning >100 rows
- **Compass SQL**: Use Compass API, not direct SQL
- **SELECT ***: Avoid, specify columns
- **WHERE clauses**: Required for UPDATE/DELETE

### Analysis Patterns

**CRITICAL: Recognize Compass API Pagination Pattern**

Compass API uses a two-step pattern:
1. **InitQuery** (or similar): POST to `/jobs/` - Creates query job, returns queryID
2. **GetResult** (or similar): GET to `/jobs/{queryID}/result?limit=X&offset=Y` - Retrieves paginated results

**Analysis Workflow**:
1. Check if process uses Compass API (look for `/DATAFABRIC/compass/` in URLs)
2. If Compass API:
   - Find the activity that retrieves results (usually GET to `/jobs/{queryID}/result`)
   - Check if URL contains `limit=` and `offset=` parameters
   - If YES → Pagination EXISTS (compliant)
   - If NO → Pagination MISSING (violation)
3. If direct SQL (not Compass API):
   - Check for LIMIT/OFFSET in SQL query
   - If YES → Pagination EXISTS (compliant)
   - If NO → Pagination MISSING (violation)

**Example - Compass API WITH Pagination (COMPLIANT)**:

InitQuery activity (creates job):
```javascript
// POST to /DATAFABRIC/compass/v2/jobs/
// Body contains SQL query
```

GetResult activity (retrieves results):
```javascript
// GET to /DATAFABRIC/compass/v2/jobs/{queryID}/result?limit=<!limit>&offset=<!offset>
// Pagination in URL parameters
```

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

### Best Practice Suggestions (Low Severity)

**CRITICAL**: Even when SQL queries are compliant, ALWAYS provide improvement suggestions based on Compass SQL best practices.

**MUST LOAD**: Before analyzing SQL, load steering file 06 (Compass SQL CheatSheet) for correct syntax and patterns.

**Analysis Approach**:
1. Review ALL SQL queries for optimization opportunities
2. Flag suggestions as "Low" severity (not violations)
3. Reference Compass SQL CheatSheet for correct syntax
4. Provide specific examples with Compass SQL syntax

**Categories for Suggestions**:

**1. Query Optimization**

Look for:
- Missing indexes on WHERE clause columns
- Inefficient JOIN patterns
- Unnecessary DISTINCT operations
- Complex subqueries that could be CTEs

Example suggestion:
```json
{
  "rule_id": "3.9.1",
  "severity": "Low",
  "finding": "Complex query could benefit from Common Table Expression (CTE)",
  "current": "Single large query with multiple aggregations and joins",
  "recommendation": "Use WITH clause to break into logical steps: WITH RecentOrders AS (...) SELECT ...",
  "activities": "InitQuery",
  "domain": "sql"
}
```

**2. Column Selection Specificity**

Look for:
- Selecting more columns than needed
- Redundant column selections
- Missing column aliases for clarity

Example suggestion:
```json
{
  "rule_id": "3.9.2",
  "severity": "Low",
  "finding": "Query selects columns that may not be used in output",
  "current": "SELECT includes 15 columns but output file only uses 8",
  "recommendation": "Remove unused columns to improve query performance and reduce data transfer",
  "activities": "InitQuery",
  "domain": "sql"
}
```

**3. CAST Operations with NULL Checks**

Look for:
- CAST operations without NULL validation
- Missing COALESCE for default values
- Type conversions that could fail silently

Example suggestion:
```json
{
  "rule_id": "3.9.3",
  "severity": "Low",
  "finding": "CAST operation without NULL check",
  "current": "CAST(SUM(NetTransactionAmount) AS DECIMAL(18,2))",
  "recommendation": "Add NULL handling: COALESCE(CAST(SUM(NetTransactionAmount) AS DECIMAL(18,2)), 0.00)",
  "activities": "InitQuery",
  "domain": "sql"
}
```

**4. Compass SQL Specific Patterns**

Look for:
- Opportunities to use Compass SQL functions
- Better use of CONCAT vs string operations
- Proper use of RPAD/LPAD for formatting
- Efficient use of CASE statements

Example suggestion:
```json
{
  "rule_id": "3.9.4",
  "severity": "Low",
  "finding": "Complex CASE statement could be simplified",
  "current": "CASE WHEN ISNULL(field,'0000') = '' THEN '0000' ELSE ISNULL(field,'0000') END",
  "recommendation": "Simplify to: COALESCE(NULLIF(field, ''), '0000')",
  "activities": "InitQuery",
  "domain": "sql"
}
```

**5. Query Readability**

Look for:
- Missing comments for complex logic
- Inconsistent formatting
- Unclear column aliases
- Complex expressions without explanation

Example suggestion:
```json
{
  "rule_id": "3.9.5",
  "severity": "Low",
  "finding": "Complex CONCAT expression without explanation",
  "current": "CONCAT(FinanceDimension1,FinanceDimension3, FinanceDimension4)",
  "recommendation": "Add comment explaining business logic: -- Combines Cost Center + Department + Location",
  "activities": "InitQuery",
  "domain": "sql"
}
```

**6. Aggregation Patterns**

Look for:
- GROUP BY with many columns (could use subquery)
- Missing HAVING clauses for filtered aggregations
- Inefficient COUNT(*) vs COUNT(column)

Example suggestion:
```json
{
  "rule_id": "3.9.6",
  "severity": "Low",
  "finding": "GROUP BY clause repeats complex expressions",
  "current": "GROUP BY with 5 complex CONCAT/RPAD expressions",
  "recommendation": "Use subquery or CTE to calculate expressions once, then GROUP BY aliases",
  "activities": "InitQuery",
  "domain": "sql"
}
```

**When to Generate Suggestions**:
- ALWAYS generate 2-4 suggestions per SQL query (even if compliant)
- Focus on Compass SQL specific optimizations
- Reference steering file 06 for correct Compass SQL syntax
- Provide specific code examples in recommendations

**When NOT to Generate Suggestions**:
- Don't suggest standard SQL features not supported by Compass SQL
- Don't flag Compass API pagination patterns as missing LIMIT clause
- Don't suggest DML operations (INSERT/UPDATE/DELETE) - Compass SQL is read-only

**CRITICAL**: Always verify suggestions against Compass SQL CheatSheet (steering file 06) to ensure compatibility.

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
