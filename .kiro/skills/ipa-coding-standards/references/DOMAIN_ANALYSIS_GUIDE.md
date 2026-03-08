# Domain Analysis Guide - IPA Coding Standards

**CRITICAL**: This guide MUST be read BEFORE analyzing ANY domain chunk in Phases 1-5.

## Core Principle: You Are The Analyst

**Python preprocessing is a HELPER, not a CONSTRAINT.**

- Python flags potential issues using regex patterns
- YOU are the final authority on what's a violation
- YOU must read and understand the actual code
- YOU must create violations for ANY issues you find, whether Python flagged them or not

## Analysis Workflow (ALL Domains)

### Step 1: Read Project Standards FIRST

```text
BEFORE analyzing any chunk, read project_standards.json completely.
```

Project standards OVERRIDE steering file defaults. Know the rules before you judge.

### Step 2: Read The Actual Code/Data

```text
DO NOT rely solely on Python's pre-computed flags.
READ the actual code snippets, SQL queries, node captions, etc.
```

**Example - JavaScript Analysis:**

```json
{
  "activity_id": "Assign7960",
  "code_snippet": "for(var i=0; i<arr.length; i++) {\n  arr[i] = arr[i].replace(/pattern/g, val);\n}\noutput += result;",
  "performance_patterns_detected": {}  // EMPTY - Python missed it!
}
```

**Your job:**

1. Read the code_snippet
2. Spot the regex `/pattern/g` being compiled inside the loop
3. Spot the `output +=` string concatenation
4. CREATE violations for BOTH issues, even though Python didn't flag them

### Step 3: Apply Domain-Specific Rules

Each domain has specific things to look for. See domain sections below.

### Step 4: Consolidate Similar Violations

If you find 25 nodes with generic captions, create ONE violation with count and examples, not 25 individual violations.

### Step 5: Write Complete Violation Objects

Every violation MUST have:

- `rule_id`: From project standards or steering defaults
- `activity_id`: Specific node or "Multiple" for consolidated
- `activity_caption`: Node caption or descriptive summary
- `issue`: Clear description of the problem
- `current_state`: What the code/config looks like now
- `recommendation`: How to fix it (be specific)
- `severity`: High, Medium, or Low
- `code_example`: Before/after comparison (for code violations)

## Domain 1: Naming Analysis

### What Python Provides

- Filename
- List of nodes with captions
- Config set names
- Hardcoded value detection (basic)

### What YOU Must Do

**1. Filename Format (Rule 1.1.1)**

- Check against project standards format
- Interface: `<Prefix>_INT_<Source>_<Destination>_<Description>.lpd`
- Workflow: `<Prefix>_WF_<Description>.lpd`
- Flag if doesn't match

**2. Node Captions (Rule 1.1.4)**

- Read EVERY node caption in the chunk
- Identify generic names: "Assign", "Branch", "Wait", "WebRun"
- Consolidate into ONE violation if multiple found
- Count affected nodes and list examples

**3. Config Set Names (Rule 1.1.3)**

- Check if names are vendor-specific or generic
- "Interface" is generic - should be "VendorName_Purpose"
- Flag generic names

**4. Hardcoded Values (Rule 1.4.2)**

- Look for URLs, credentials, environment-specific values in code
- Python's detection is basic - YOU must read the code
- Check JavaScript blocks for hardcoded strings

### Common Mistakes to Avoid

- ❌ Creating 25 individual violations for 25 generic captions
- ✅ Create 1 consolidated violation with count and examples

## Domain 2: JavaScript Analysis

### What Python Provides

- ES6 feature detection (let/const, arrow functions, template literals)
- Performance pattern hints (regex_in_loop, string_concat_in_loop, etc.)
- Function declaration detection
- Code snippets (truncated to ~200 chars)

### What YOU Must Do

**CRITICAL: Python's performance detection is INCOMPLETE. You MUST read the code yourself.**

**1. ES5 Compliance (Rule 1.2.3)**

- Check Python's `es6_features_detected`
- BUT ALSO read code snippets for:
  - Destructuring: `const {prop} = obj`
  - Spread operators: `...array`
  - Default parameters: `function f(x = 1)`
  - async/await: `async function` or `await`

**2. Performance Issues (Rules 1.5.4, 1.5.5)**

**Rule 1.5.4: Regex Compilation**

- Python looks for: `new RegExp` or `/pattern/` inside loops
- YOU must also check:
  - Is the regex complex? (nested groups, lookaheads)
  - Is it used in pagination logic? (high iteration count)
  - Could it be pre-compiled outside the loop?

**Example violation:**

```javascript
// CURRENT (BAD):
for(var i=0; i<arr.length; i++) {
    arr[i] = arr[i].replace(/,(?=(?:(?:[^\"]*\"){2})*[^\"]*$)/g, delimiter);
}

// RECOMMENDED (GOOD):
var commaRegex = /,(?=(?:(?:[^\"]*\"){2})*[^\"]*$)/g;
for(var i=0; i<arr.length; i++) {
    arr[i] = arr[i].replace(commaRegex, delimiter);
}
```

**Rule 1.5.5: String Concatenation**

- Python looks for: `variable +=` inside loops
- YOU must also check:
  - Is `+=` used repeatedly in pagination logic?
  - Is it building large strings? (CSV output, file content)
  - Would array.join() be better?

**Example violation for string concatenation:**

```javascript
// CURRENT (BAD - O(n²) complexity):
OutputRecords += GetResultOut + "\r\n";  // Called in pagination loop

// RECOMMENDED (GOOD - O(n) complexity):
var recordsArray = [];
// In loop:
recordsArray.push(GetResultOut);
// After loop:
OutputRecords = recordsArray.join("\r\n");
```

**3. Function Declaration Order (Rule 1.2.2)**

- Check Python's `functions_declared_late` flag
- BUT ALSO read the code to understand context
- Functions should be declared at the top of the script
- Executable code should come after function declarations

**4. Variable Scoping (Rule 1.2.1)**

- Check if variables are properly scoped
- Global variables should be on Start node (no `var` keyword)
- Local variables should use `var` in Assign nodes
- Look for accidental globals (missing `var`)

### Common Mistakes to Avoid

- ❌ Only flagging issues Python detected
- ✅ Read the actual code and find issues Python missed
- ❌ Ignoring performance issues because Python didn't flag them
- ✅ Understand the business logic (pagination, file processing) and assess performance impact

## Domain 3: SQL Analysis

### What Python Provides

- SQL query text
- Query type detection (SELECT, INSERT, UPDATE, DELETE)
- Basic pattern detection (SELECT *, LIMIT clause)

### What YOU Must Do

**CRITICAL: Understand Compass API pagination vs SQL LIMIT clause**

**1. Pagination (Rule 1.5.2)**

**Compass API Pattern (CORRECT - not a violation):**

```javascript
// Start node has: limit = 5000, offset = 0
// InitQuery: SELECT ... (no LIMIT clause)
// Loop: GetResult with ?limit=<!limit>&offset=<!offset>
// Increment: offset += parseInt(limit)
```

This is CORRECT pagination. The LIMIT is in the API call, not the SQL query.

**SQL LIMIT Pattern (CORRECT):**

```sql
SELECT * FROM table WHERE condition LIMIT 1000
```

**Missing Pagination (VIOLATION):**

```sql
SELECT * FROM large_table WHERE condition
-- No LIMIT clause AND no Compass API pagination loop
```

**How to verify:**

1. Read the COMPLETE `lpd_structure.json` (not just the SQL chunk)
2. Check Start node for `limit` and `offset` variables
3. Look for GetResult activity with limit/offset parameters
4. Look for offset increment logic: `offset += parseInt(limit)`
5. If Compass API pagination exists, DO NOT flag missing LIMIT clause

**2. SELECT * (Performance)**

- Flag if SELECT * is used
- Recommend specifying only needed columns
- Exception: Small lookup tables (<100 rows)

**3. Compass SQL Compliance (Rule 1.5.2)**

- Check for Compass-specific syntax
- Verify proper use of Data Fabric tables
- Check for proper filtering (WHERE clauses)

### Common Mistakes to Avoid

- ❌ Flagging Compass API queries for missing LIMIT clause
- ✅ Verify pagination implementation before flagging
- ❌ Assuming all queries need LIMIT in the SQL
- ✅ Understand the difference between SQL LIMIT and API pagination

## Domain 4: Error Handling Analysis

### What Python Provides

- List of error-prone activities (WEBRN, ACCFIL, Timer, SUBPROC, etc.)
- stopOnError property values
- has_error_handling flags

### What YOU Must Do

**1. OnError Tab Coverage (Rule 1.3.1)**

- Check if error-prone activities have OnError tabs
- Required for: WEBRN, WEBRUN, ACCFIL, Timer, SUBPROC, ITBEG
- Not required for: START, END, ASSGN, BRANCH, MSGBD

**2. GetWorkUnitErrors Subprocess (Rule 1.3.2)**

- Check if process has a SUBPROC node for centralized error logging
- This is a best practice, not always required
- Flag as Medium severity if missing

**3. stopOnError Property (Rule 1.3.3)**

- Should be "false" for nodes with OnError tabs
- Allows graceful error handling
- Flag if "true" when OnError exists

### Common Mistakes to Avoid

- ❌ Flagging ASSGN or BRANCH nodes for missing OnError
- ✅ Only flag activity types that support OnError tabs
- ❌ Treating GetWorkUnitErrors as Critical
- ✅ It's a Medium severity best practice

## Domain 5: Structure Analysis

### What Python Provides

- Process type (Interface, Workflow, etc.)
- Auto-restart value
- Activity type distribution
- Complexity metrics

### What YOU Must Do

**1. Auto-Restart Configuration (Rule 1.4.3)**

- Interface/Outbound: Should be 0 (prevents duplicate processing)
- Approval/Inbound: Should be 1 (allows retry on failure)
- Check if current value matches process type

**2. Process Type Validation**

- Verify process type matches filename convention
- Interface processes should have INT in filename
- Workflow processes should have WF in filename

**3. Complexity Assessment**

- Review activity distribution
- Flag if process is overly complex (>100 activities)
- Recommend splitting into subprocesses if needed

### Common Mistakes to Avoid

- ❌ Flagging auto-restart without understanding process type
- ✅ Context-aware assessment based on interface vs workflow
- ❌ Treating all large processes as violations
- ✅ Assess if complexity is justified by business requirements

## Output Format

Each analysis phase MUST output a JSON file with this structure:

```json
{
  "chunk_id": 1,
  "violations": [
    {
      "rule_id": "1.5.4",
      "activity_id": "Assign7960",
      "activity_caption": "Assign",
      "issue": "Complex regex pattern compiled inside loop causing O(n) regex compilations",
      "current_state": "Regex /,(?=(?:(?:[^\"]*\"){2})*[^\"]*$)/g compiled on every iteration of pagination loop",
      "recommendation": "Pre-compile regex outside loop and reuse the compiled pattern",
      "severity": "High",
      "code_example": "Current:\nfor(var i=0; i<arr.length; i++) {\n  arr[i] = arr[i].replace(/,(?=(?:(?:[^\"]*\"){2})*[^\"]*$)/g, delimiter);\n}\n\nExpected:\nvar commaRegex = /,(?=(?:(?:[^\"]*\"){2})*[^\"]*$)/g;\nfor(var i=0; i<arr.length; i++) {\n  arr[i] = arr[i].replace(commaRegex, delimiter);\n}",
      "affected_nodes": ["Assign7960"]
    }
  ]
}
```

## Final Checklist (Before Saving Analysis)

- [ ] Read project standards completely
- [ ] Read ALL code snippets/data in the chunk (not just Python flags)
- [ ] Identified ALL violations (not just what Python flagged)
- [ ] Consolidated similar violations (not 25 individual items)
- [ ] Wrote complete violation objects (all required fields)
- [ ] Provided specific code examples (before/after)
- [ ] Assessed severity based on production impact
- [ ] Verified rule_id matches project standards or steering defaults

## Remember

**You are a senior code reviewer, not a script executor.**

- Python helps you find issues faster
- YOU make the final judgment calls
- YOUR analysis determines report quality
- YOUR recommendations guide developers

**If Python missed something obvious, that's a Python bug - but it's YOUR responsibility to catch it anyway.**
