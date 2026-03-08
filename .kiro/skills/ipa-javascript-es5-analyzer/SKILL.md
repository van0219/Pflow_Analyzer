---
name: "ipa-javascript-es5-analyzer"
description: "Your JavaScript genius for IPA. Analyzes, reviews, optimizes, debugs, and writes ES5-compliant JavaScript. Handles code review, creation, troubleshooting, and best practices. Use for any JavaScript-related task in IPA."
---

# IPA JavaScript ES5 Genius

Your comprehensive JavaScript expert for IPA. Not just a code reviewer - a full-featured JavaScript assistant that analyzes, creates, optimizes, debugs, and teaches ES5-compliant JavaScript for IPA processes.

## What This Skill Does

This skill is your JavaScript genius that can:

1. **Analyze & Review** - Comprehensive code analysis for ES5 compliance, best practices, performance
2. **Create & Generate** - Write production-ready ES5 JavaScript from requirements
3. **Debug & Fix** - Troubleshoot runtime errors, identify root causes, provide fixes
4. **Optimize & Improve** - Enhance performance, refactor code, apply best practices
5. **Teach & Explain** - Answer JavaScript questions, explain concepts, provide examples
6. **Convert & Migrate** - Transform ES6+ code to ES5, modernize legacy code

## When to Use

**Code Review & Analysis:**

- Reviewing JavaScript before deployment
- Validating ES5 compliance
- Identifying performance issues
- Ensuring production readiness

**Code Creation:**

- Writing new IPA JavaScript from scratch
- Generating Assign node logic
- Creating data transformation functions
- Building validation routines

**Troubleshooting:**

- Debugging runtime errors
- Fixing "unexpected token" errors
- Resolving NULL/undefined issues
- Solving performance problems

**Learning & Questions:**

- Understanding ES5 constraints
- Learning IPA JavaScript patterns
- Getting code examples
- Best practices guidance

**Optimization:**

- Improving slow code
- Reducing complexity
- Enhancing readability
- Applying defensive patterns

## Critical ES5 Rules

**IPA JavaScript executes in ES5 environment. Modern syntax causes immediate runtime errors.**

### Forbidden ES6+ Features

| Feature | ES6+ (FORBIDDEN) | ES5 (REQUIRED) |
|---------|------------------|----------------|
| Variables | `let x = 1;` `const x = 1;` | `var x = 1;` |
| Functions | `() => {}` `async/await` | `function() {}` |
| Strings | `` `Hello ${name}` `` | `"Hello " + name` |
| Destructuring | `var {prop} = obj;` | `var prop = obj.prop;` |
| Default params | `function f(x = 1)` | Check inside function |
| Spread | `[...arr]` | `arr.slice()` |
| Classes | `class MyClass {}` | Constructor functions |
| Modules | `import/export` | Not supported |
| Promises | `new Promise()` | Not supported |
| Template literals | `` `text` `` | `"text"` |

### Allowed ES5 Features

- `var` declarations
- `function` keyword
- Traditional for loops
- `if/else`, `switch`, ternary operator
- Object literals: `{key: value}`
- Array literals: `[1, 2, 3]`
- String concatenation: `+`
- All ES5 built-in methods

## How to Use This Skill

### Quick Questions

Just ask! No code needed:

```text

User: How do I loop through an array in ES5?
User: What's the ES5 way to filter an array?
User: How do I handle NULL values safely?
User: Show me an IPA Assign node structure

```text

### Code Review (Paste in Chat)

For short code (< 100 lines), paste directly:

```text

User: Review this code:
var items = data.filter(x => x.status === "Active");
let count = items.length;

Skill: [Identifies ES6 violations and provides ES5 fix]

```text

### Code Review (File-Based)

For longer code, save to file:

```text

User: Analyze Temp/assign_node_code.js

Skill: [Reads file, performs comprehensive analysis]

```text

### Code Generation

Describe what you need:

```text

User: I need JavaScript to parse a CSV file, validate required fields, 
and calculate totals. It should handle empty lines and invalid numbers.

Skill: [Generates complete ES5-compliant code with error handling]

```text

### Troubleshooting

Share the error:

```text

User: My code is failing with "unexpected token" error on line 23

Skill: [Analyzes code, identifies ES6+ syntax, provides fix]

```text

### Learning & Examples

Ask for explanations:

```text

User: Explain the difference between var and let
User: Show me how to do pagination in IPA
User: What's the best way to handle floating point comparison?

Skill: [Provides detailed explanation with examples]

```text

## Activation Instructions

**CRITICAL**: When this skill is activated, the following steering files are automatically loaded:

1. **IPA Guide** (REQUIRED):

   ```text\n ---
name: "ipa-javascript-es5-analyzer"
description: "Your JavaScript genius for IPA. Analyzes, reviews, optimizes, debugs, and writes ES5-compliant JavaScript. Handles code review, creation, troubleshooting, and best practices. Use for any JavaScript-related task in IPA."
---

# IPA JavaScript ES5 Genius

Your comprehensive JavaScript expert for IPA. Not just a code reviewer - a full-featured JavaScript assistant that analyzes, creates, optimizes, debugs, and teaches ES5-compliant JavaScript for IPA processes.

## What This Skill Does

This skill is your JavaScript genius that can:

1. **Analyze & Review** - Comprehensive code analysis for ES5 compliance, best practices, performance
2. **Create & Generate** - Write production-ready ES5 JavaScript from requirements
3. **Debug & Fix** - Troubleshoot runtime errors, identify root causes, provide fixes
4. **Optimize & Improve** - Enhance performance, refactor code, apply best practices
5. **Teach & Explain** - Answer JavaScript questions, explain concepts, provide examples
6. **Convert & Migrate** - Transform ES6+ code to ES5, modernize legacy code

## When to Use

**Code Review & Analysis:**

- Reviewing JavaScript before deployment
- Validating ES5 compliance
- Identifying performance issues
- Ensuring production readiness

**Code Creation:**

- Writing new IPA JavaScript from scratch
- Generating Assign node logic
- Creating data transformation functions
- Building validation routines

**Troubleshooting:**

- Debugging runtime errors
- Fixing "unexpected token" errors
- Resolving NULL/undefined issues
- Solving performance problems

**Learning & Questions:**

- Understanding ES5 constraints
- Learning IPA JavaScript patterns
- Getting code examples
- Best practices guidance

**Optimization:**

- Improving slow code
- Reducing complexity
- Enhancing readability
- Applying defensive patterns

## Critical ES5 Rules

**IPA JavaScript executes in ES5 environment. Modern syntax causes immediate runtime errors.**

### Forbidden ES6+ Features

| Feature | ES6+ (FORBIDDEN) | ES5 (REQUIRED) |
|---------|------------------|----------------|
| Variables | `let x = 1;` `const x = 1;` | `var x = 1;` |
| Functions | `() => {}` `async/await` | `function() {}` |
| Strings | `` `Hello ${name}` `` | `"Hello " + name` |
| Destructuring | `var {prop} = obj;` | `var prop = obj.prop;` |
| Default params | `function f(x = 1)` | Check inside function |
| Spread | `[...arr]` | `arr.slice()` |
| Classes | `class MyClass {}` | Constructor functions |
| Modules | `import/export` | Not supported |
| Promises | `new Promise()` | Not supported |
| Template literals | `` `text` `` | `"text"` |

### Allowed ES5 Features

- `var` declarations
- `function` keyword
- Traditional for loops
- `if/else`, `switch`, ternary operator
- Object literals: `{key: value}`
- Array literals: `[1, 2, 3]`
- String concatenation: `+`
- All ES5 built-in methods

## How to Use This Skill

### Quick Questions

Just ask! No code needed:

```text

User: How do I loop through an array in ES5?
User: What's the ES5 way to filter an array?
User: How do I handle NULL values safely?
User: Show me an IPA Assign node structure

```text

### Code Review (Paste in Chat)

For short code (< 100 lines), paste directly:

```text

User: Review this code:
var items = data.filter(x => x.status === "Active");
let count = items.length;

Skill: [Identifies ES6 violations and provides ES5 fix]

```text

### Code Review (File-Based)

For longer code, save to file:

```text

User: Analyze Temp/assign_node_code.js

Skill: [Reads file, performs comprehensive analysis]

```text

### Code Generation

Describe what you need:

```text

User: I need JavaScript to parse a CSV file, validate required fields, 
and calculate totals. It should handle empty lines and invalid numbers.

Skill: [Generates complete ES5-compliant code with error handling]

```text

### Troubleshooting

Share the error:

```text

User: My code is failing with "unexpected token" error on line 23

Skill: [Analyzes code, identifies ES6+ syntax, provides fix]

```text

### Learning & Examples

Ask for explanations:

```text

User: Explain the difference between var and let
User: Show me how to do pagination in IPA
User: What's the best way to handle floating point comparison?

Skill: [Provides detailed explanation with examples]

```text

## Activation Instructions

**CRITICAL**: When this skill is activated, the following steering files are automatically loaded:

1. **IPA Guide** (REQUIRED):

   ```text\ndiscloseContext(name="ipa-ipd-guide")

   ```

   Loads `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` with:

- IPA JavaScript ES5 compliance rules
- Assign node structure
- Start node global variables
- Activity types and patterns

1. **Process Patterns** (for code generation):

   ```text\ndiscloseContext(name="process-patterns")

   ```

   Loads `.kiro/steering/04_Process_Patterns_Library.md` with:
   - 450+ analyzed IPA workflows
   - Common JavaScript patterns
   - Data transformation examples
   - Validation routines

2. **FSM Business Classes** (for API integration):

   ```text\ndiscloseContext(name="fsm-business-classes")

   ```

   Loads `.kiro/steering/07_FSM_Business_Classes_and_API.md` when working with:
   - WebRun activities
   - Landmark API calls
   - FSM business class operations

3. **Data Fabric** (for Compass SQL integration):

   ```text\ndiscloseContext(name="data-fabric-guide")

   ```

   Loads `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md` when working with:
   - Compass API JavaScript
   - Data Lake queries
   - JSON parsing from API responses

**The skill will automatically load relevant steering files based on the task context.**

The skill performs comprehensive analysis across 6 dimensions:

1. **ES5 Compliance**

   - No `let`/`const` (use `var`)
   - No arrow functions (use `function`)
   - No template literals (use string concatenation)
   - No destructuring (explicit property access)
   - No default parameters (check inside function)
   - No spread operator (use `.slice()`, `.concat()`)
   - No ES6+ methods (`.map()`, `.filter()`, `.find()`)

2. **Best Practices**

   - Defensive NULL/undefined checks
   - Input validation
   - Type checking before operations
   - Proper error handling
   - Meaningful variable names
   - Comments for complex logic

3. **Performance**

   - Efficient loops (avoid nested loops where possible)
   - String concatenation optimization
   - Array operations efficiency
   - Avoid redundant calculations
   - Memory-efficient patterns

4. **Production Readiness**

   - Edge case handling (empty strings, zero, NULL)
   - Floating point comparison (rounding)
   - Division by zero checks
   - Array bounds checking
   - Safe type conversions

5. **Code Quality**

   - Readability (formatting, indentation)
   - Maintainability (modularity, reusability)
   - Naming conventions (descriptive names)
   - Comment quality
   - Code organization

6. **IPA-Specific Patterns**

   - Assign node structure (function wrapper)
   - Global variable usage
   - Configuration at top of function
   - No top-level return statements
   - Function invocation at end

### Step 3: Recommendations

For each issue found, provides:

- **Severity**: Critical / High / Medium / Low
- **Category**: ES5 Compliance / Best Practices / Performance / Production Readiness
- **Explanation**: Why this matters
- **Fix**: Specific code changes
- **Example**: Before/after comparison

### Step 4: Improved Code

Generates refactored code with:

- All ES6+ features converted to ES5
- Best practices applied
- Performance optimizations
- Production-ready error handling
- Comments explaining changes

## Analysis Categories

### ES5 Compliance Issues

**Critical:**

- `let` or `const` declarations
- Arrow functions `() => {}`
- Template literals `` `${var}` ``
- `async`/`await`
- Destructuring `{prop} = obj`
- Spread operator `...arr`
- ES6+ methods (`.map()`, `.filter()`, `.find()`)

**High:**

- Default parameters `function(x = 1)`
- `class` keyword
- `import`/`export` statements
- `Promise` usage
- `for...of` loops

**Medium:**

- Object shorthand `{prop}` instead of `{prop: prop}`
- Computed property names `{[key]: value}`
- Method shorthand `{method() {}}`

### Best Practices Issues

**Critical:**

- No NULL/undefined checks before operations
- No input validation
- Missing error handling
- Unsafe type conversions

**High:**

- No defensive programming patterns
- Missing edge case handling
- Unclear variable names
- No comments for complex logic

**Medium:**

- Inconsistent naming conventions
- Poor code organization
- Redundant code
- Magic numbers without explanation

### Performance Issues

**Critical:**

- Nested loops with high complexity
- **String concatenation in loops** (O(n²) complexity - use array accumulation)
- Redundant calculations inside loops

**High:**

- Unnecessary array iterations
- Inefficient search patterns
- Memory-intensive operations

**Medium:**

- Suboptimal algorithm choices
- Unnecessary variable declarations
- Redundant type checks

### Production Readiness Issues

**Critical:**

- No division by zero checks
- No floating point rounding before comparison
- Missing NULL guards on critical operations

**High:**

- No empty string/array checks
- Missing array bounds validation
- Unsafe parseInt/parseFloat usage

**Medium:**

- No default value handling
- Missing type validation
- Insufficient error messages

## Common Patterns Analyzed

### Pattern 1: Variable Declarations

**Bad (ES6):**

```javascript

let count = 0;
const MAX_ITEMS = 100;

```text

**Good (ES5):**

```javascript

var count = 0;
var MAX_ITEMS = 100;

```text

### Pattern 2: Arrow Functions

**Bad (ES6):**

```javascript

var result = items.map(item => item.value);

```text

**Good (ES5):**

```javascript

var result = [];
for (var i = 0; i < items.length; i++) {
    result.push(items[i].value);
}

```text

### Pattern 3: Template Literals

**Bad (ES6):**

```javascript

var message = `Hello ${name}, you have ${count} items`;

```text

**Good (ES5):**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

### Pattern 4: Destructuring

**Bad (ES6):**

```javascript

var {firstName, lastName} = person;

```text

**Good (ES5):**

```javascript

var firstName = person.firstName;
var lastName = person.lastName;

```text

### Pattern 5: Default Parameters

**Bad (ES6):**

```javascript

function calculate(amount, rate = 0.05) {
    return amount * rate;
}

```text

**Good (ES5):**

```javascript

function calculate(amount, rate) {
    if (typeof rate === "undefined") {
        rate = 0.05;
    }
    return amount * rate;
}

```text

### Pattern 6: Spread Operator

**Bad (ES6):**

```javascript

var combined = [...array1, ...array2];

```text

**Good (ES5):**

```javascript

var combined = array1.concat(array2);

```text

### Pattern 7: Defensive NULL Checks

**Bad:**

```javascript

var total = parseFloat(amount);
if (total === 0) {
    // May fail if amount is NULL/undefined
}

```text

**Good:**

```javascript

if (!amount || typeof amount !== "string") {
    amount = "0";
}
var total = parseFloat(amount);
if (isNaN(total)) {
    total = 0;
}
if (total === 0) {
    // Safe comparison
}

```text

### Pattern 8: Floating Point Comparison

**Bad:**

```javascript

if (sumQty === 0) {
    // Unreliable for floating point
}

```text

**Good:**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var roundedSum = roundToDecimals(sumQty, 2);
if (roundedSum === 0) {
    // Safe comparison
}

```text

### Pattern 9: Division by Zero

**Bad:**

```javascript

var unitCost = extendedAmount / originalQuantity;

```

### Pattern 10: String Concatenation in Loops (CRITICAL PERFORMANCE)

**Bad (O(n²) complexity):**

```javascript
// Inside pagination loop (100+ iterations)
OutputRecords += GetResultOut + "

";
```

**Why It's Bad:**
- Strings are immutable in JavaScript
- Each `+=` creates a NEW string and copies ALL previous content
- 100 iterations = ~5MB copied for 100KB of data
- Performance degrades exponentially with data size

**Good (O(n) complexity):**

```javascript
// BEFORE the pagination loop
var OutputRecordsArray = [];

// INSIDE the pagination loop
while (hasMoreData) {
    // ... fetch and transform data ...
    
    // Push to array instead of string concatenation
    for (var i = 0; i < transformedLines.length; i++) {
        OutputRecordsArray.push(transformedLines[i]);
    }
    
    // ... pagination logic ...
    offset += limit;
}

// AFTER the loop completes - join once
var OutputRecords = OutputRecordsArray.join("

");
```

**Performance Comparison:**

| Approach | Complexity | 100 Iterations | 1000 Iterations |
|----------|-----------|----------------|-----------------|
| String += | O(n²) | ~5MB copied | ~500MB copied |
| Array.push() + join() | O(n) | ~100KB copied | ~1MB copied |
| **Speedup** | **Linear** | **50x faster** | **500x faster** |

**When to Use:**
- Any loop with 10+ iterations
- Pagination loops processing large datasets
- File processing with line-by-line accumulation
- Data transformation with result aggregationtext

**Good:**

```javascript

if (originalQuantity === 0) {
    exceptions.push({error: "Division by zero"});
    continue;
}
var unitCost = extendedAmount / originalQuantity;

```text

### Pattern 11: IPA Assign Node Structure

**Bad:**

```javascript

// Top-level code
var result = processData(input);
return result;  // ERROR: No top-level return

```text

**Good:**

```javascript

function transformData(inputData, fileName) {
    // Configuration variables
    var CONFIG_VALUE = "setting";
    
    // Validation
    if (!inputData || typeof inputData !== "string") {
        inputData = "";
    }
    
    // Processing logic
    var result = [];
    // ... transformation ...
    
    return result;
}

// Function invocation at end
transformData(ImportFile, FileName);

```

## Real-World Performance Scenarios

### Scenario 1: Compass API Pagination (Production)

**Context**: MatchReport_Outbound.lpd processing 50,000 GL transactions

**Bad Implementation (O(n²) - 45 minutes execution)**:

```javascript
// Global variable
var OutputRecords = "";

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        GetResultArr[i] = GetResultArr[i].replace(/,/g, "|");
    }
    GetResultOut = GetResultArr.join("
");
    
    // ❌ BAD: String concatenation in loop
    OutputRecords += GetResultOut + "
";  // O(n²) complexity
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}
```

**Performance Impact**:
- Iteration 1: Copy 10KB
- Iteration 100: Copy 1MB (100 × 10KB)
- Iteration 500: Copy 5MB (500 × 10KB)
- Total: ~1.25GB copied for 5MB of data
- Execution time: 45 minutes

**Good Implementation (O(n) - 54 seconds execution)**:

```javascript
// Global variable (array accumulator)
var OutputRecordsArray = [];

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        var line = GetResultArr[i];
        if (line && line.trim() !== "") {
            // ✅ GOOD: Push to array
            OutputRecordsArray.push(line.replace(/,/g, "|"));
        }
    }
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}

// Join once after loop completes
var OutputRecords = OutputRecordsArray.join("
");
```

**Performance Improvement**:
- Total: ~5MB copied (linear growth)
- Execution time: 54 seconds
- **Speedup: 50x faster**
- Memory efficiency: 250x less copying

### Scenario 2: File Processing with Validation

**Context**: Invoice import processing 10,000 lines with validation

**Bad Implementation (Multiple Issues)**:

```javascript
var validRecords = "";
var errorRecords = "";

for (var i = 0; i < lines.length; i++) {
    var fields = lines[i].split(",");
    
    // ❌ Issue 1: No NULL check
    var amount = parseFloat(fields[2]);
    
    // ❌ Issue 2: Floating point comparison without rounding
    if (amount === 0) {
        errorRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    } else {
        validRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    }
}
```

**Good Implementation (All Best Practices)**:

```javascript
var validRecordsArray = [];
var errorRecordsArray = [];

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    
    // ✅ Skip empty lines
    if (!line || line.trim() === "") {
        continue;
    }
    
    var fields = line.split(",");
    
    // ✅ Validate field count
    if (fields.length < 3) {
        errorRecordsArray.push(line + "|Missing fields");
        continue;
    }
    
    // ✅ NULL check and safe parsing
    var amountStr = fields[2] ? fields[2].trim() : "0";
    var amount = parseFloat(amountStr);
    
    // ✅ Validate numeric
    if (isNaN(amount)) {
        errorRecordsArray.push(line + "|Invalid amount: " + amountStr);
        continue;
    }
    
    // ✅ Round before comparison
    var roundedAmount = roundToDecimals(amount, 2);
    
    if (roundedAmount === 0) {
        errorRecordsArray.push(line + "|Zero amount");
    } else {
        validRecordsArray.push(line);
    }
}

// ✅ Join once at end
var validRecords = validRecordsArray.join("
");
var errorRecords = errorRecordsArray.join("
");
```

**Improvements**:
- Array accumulation (50x faster for large datasets)
- NULL safety (prevents runtime errors)
- Floating point rounding (prevents comparison bugs)
- Input validation (catches data quality issues)
- Empty line handling (cleaner output)

### Scenario 3: Nested Loop Optimization

**Context**: Matching 1,000 invoices against 5,000 PO lines

**Bad Implementation (O(n²) - 5 million comparisons)**:

```javascript
var matchedInvoices = [];

// ❌ Nested loop without optimization
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < poLines.length; j++) {
        if (invoices[i].poNumber === poLines[j].poNumber &&
            invoices[i].lineNumber === poLines[j].lineNumber) {
            matchedInvoices.push({
                invoice: invoices[i],
                poLine: poLines[j]
            });
            break;  // At least breaks after match
        }
    }
}
```

**Good Implementation (O(n) - 6,000 operations)**:

```javascript
// ✅ Build lookup map (O(n))
var poLookup = {};
for (var i = 0; i < poLines.length; i++) {
    var key = poLines[i].poNumber + "|" + poLines[i].lineNumber;
    poLookup[key] = poLines[i];
}

// ✅ Single loop with map lookup (O(n))
var matchedInvoices = [];
for (var i = 0; i < invoices.length; i++) {
    var key = invoices[i].poNumber + "|" + invoices[i].lineNumber;
    var poLine = poLookup[key];
    
    if (poLine) {
        matchedInvoices.push({
            invoice: invoices[i],
            poLine: poLine
        });
    }
}
```

**Performance Improvement**:
- Bad: 5,000,000 comparisons (1,000 × 5,000)
- Good: 6,000 operations (5,000 + 1,000)
- **Speedup: 833x faster**

## Performance Optimization Checklist

### Memory Optimization

**1. Array Accumulation vs String Concatenation**

```javascript
// ❌ BAD: O(n²) memory copying
var result = "";
for (var i = 0; i < 1000; i++) {
    result += data[i] + "
";  // Creates 1000 new strings
}

// ✅ GOOD: O(n) memory usage
var resultArray = [];
for (var i = 0; i < 1000; i++) {
    resultArray.push(data[i]);  // Reuses array memory
}
var result = resultArray.join("
");  // Single allocation
```

**2. Reuse Variables Instead of Creating New Ones**

```javascript
// ❌ BAD: Creates 1000 new variables
for (var i = 0; i < 1000; i++) {
    var temp = data[i].toUpperCase();
    var trimmed = temp.trim();
    var replaced = trimmed.replace(/,/g, "|");
    results.push(replaced);
}

// ✅ GOOD: Reuses single variable
var temp;
for (var i = 0; i < 1000; i++) {
    temp = data[i].toUpperCase().trim().replace(/,/g, "|");
    results.push(temp);
}
```

**3. Avoid Unnecessary Array Copies**

```javascript
// ❌ BAD: Creates new array on each iteration
for (var i = 0; i < items.length; i++) {
    var subset = items.slice(0, i);  // O(n²) total
    process(subset);
}

// ✅ GOOD: Process in place
for (var i = 0; i < items.length; i++) {
    process(items, i);  // Pass index instead
}
```

### Speed Optimization

**1. Hoist Invariant Calculations Outside Loops**

```javascript
// ❌ BAD: Calculates same value 1000 times
for (var i = 0; i < 1000; i++) {
    var multiplier = Math.pow(10, 2);  // Recalculated each iteration
    results.push(data[i] * multiplier);
}

// ✅ GOOD: Calculate once
var multiplier = Math.pow(10, 2);
for (var i = 0; i < 1000; i++) {
    results.push(data[i] * multiplier);
}
```

**2. Cache Array Length**

```javascript
// ❌ BAD: Accesses .length property 1000 times
for (var i = 0; i < items.length; i++) {
    process(items[i]);
}

// ✅ GOOD: Cache length (minor optimization, but good practice)
var len = items.length;
for (var i = 0; i < len; i++) {
    process(items[i]);
}
```

**3. Use Lookup Maps for Repeated Searches**

```javascript
// ❌ BAD: O(n²) - searches array repeatedly
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < vendors.length; j++) {
        if (invoices[i].vendorId === vendors[j].id) {
            invoices[i].vendorName = vendors[j].name;
            break;
        }
    }
}

// ✅ GOOD: O(n) - build map once, lookup is O(1)
var vendorMap = {};
for (var i = 0; i < vendors.length; i++) {
    vendorMap[vendors[i].id] = vendors[i].name;
}
for (var i = 0; i < invoices.length; i++) {
    invoices[i].vendorName = vendorMap[invoices[i].vendorId] || "";
}
```

**4. Compile Regex Outside Loops**

```javascript
// ❌ BAD: Compiles regex 1000 times
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(/[^0-9]/g, "");  // Regex compiled each time
    results.push(cleaned);
}

// ✅ GOOD: Compile once (ES5 doesn't have explicit compilation, but pattern is cached)
var digitPattern = /[^0-9]/g;
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(digitPattern, "");
    results.push(cleaned);
}
```

### Space Optimization

**1. Clear Large Variables After Use**

```javascript
// Process large dataset
var largeData = fetchLargeDataset();  // 10MB
var processed = processData(largeData);

// ✅ Clear reference to allow garbage collection
largeData = null;

// Continue with processed data
return processed;
```

**2. Process Data in Chunks**

```javascript
// ❌ BAD: Load entire file into memory
var allLines = fileContent.split("
");  // 100MB in memory
var results = [];
for (var i = 0; i < allLines.length; i++) {
    results.push(processLine(allLines[i]));
}

// ✅ GOOD: Process in chunks (if possible)
var CHUNK_SIZE = 1000;
var results = [];
var lines = fileContent.split("
");

for (var i = 0; i < lines.length; i += CHUNK_SIZE) {
    var chunk = lines.slice(i, i + CHUNK_SIZE);
    for (var j = 0; j < chunk.length; j++) {
        results.push(processLine(chunk[j]));
    }
    chunk = null;  // Clear chunk
}
```

## Performance Measurement Tips

### Timing Code Execution

```javascript
// Start timer
var startTime = new Date().getTime();

// Your code here
for (var i = 0; i < 10000; i++) {
    // ... processing ...
}

// End timer
var endTime = new Date().getTime();
var elapsedMs = endTime - startTime;

// Log result
console.log("Execution time: " + elapsedMs + "ms");
```

### Memory Usage Estimation

```javascript
// Estimate string memory usage
function estimateStringMemory(str) {
    // Each character is ~2 bytes in JavaScript
    return str.length * 2;
}

// Estimate array memory usage
function estimateArrayMemory(arr) {
    var total = 0;
    for (var i = 0; i < arr.length; i++) {
        if (typeof arr[i] === "string") {
            total += arr[i].length * 2;
        }
    }
    return total;
}

// Example usage
var data = "Large string data...";
var memoryBytes = estimateStringMemory(data);
var memoryMB = memoryBytes / (1024 * 1024);
console.log("Estimated memory: " + memoryMB.toFixed(2) + " MB");
```text

## Output Format

### Analysis Summary

```text

📊 IPA JAVASCRIPT ES5 ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code: [First 50 chars...]
Lines: 85
Complexity: Medium
Node Type: Assign

OVERALL ASSESSMENT: ⚠️ NEEDS IMPROVEMENT

Critical Issues: 3 (ES5 compliance violations)
High Priority: 5 (Missing NULL checks)
Medium Priority: 8 (Performance optimizations)
Low Priority: 2 (Code quality)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Issue Details

```text

🔴 CRITICAL: Arrow Function Usage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Category: ES5 Compliance
Impact: Runtime error in IPA (arrow functions not supported)
Line: 23

Issue:
Arrow function syntax is ES6+ and will cause immediate runtime error
in IPA's ES5 JavaScript environment.

Current Code:
var filtered = items.filter(item => item.status === "Active");

Recommended Fix:
var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

Explanation:
IPA JavaScript executes in ES5 environment. Use traditional for loops
and function keyword instead of arrow functions and array methods like
.filter(), .map(), .find().

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Improved Code

```text

✅ IMPROVED CODE (ES5 COMPLIANT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied:

1. Converted all let/const to var
2. Replaced arrow functions with function keyword
3. Replaced template literals with string concatenation
4. Added NULL/undefined checks
5. Added floating point rounding
6. Added division by zero checks

7. Improved error handling
8. Added descriptive comments

// IPA Assign Node: Transform Import Data
// Purpose: Parse and validate import file content
// Input: ImportFile (string), FileName (string)
// Output: Processed records array

function transformImportData(importFileContent, fileName) {
    // Configuration
    var ROUND_DECIMALS = 2;
    var REQUIRED_FIELDS = ["id", "amount", "quantity"];
    
    // Input validation
    if (!importFileContent || typeof importFileContent !== "string") {
        importFileContent = "";
    }
    
    if (!fileName || typeof fileName !== "string") {
        fileName = "unknown";
    }
    
    // Initialize result arrays
    var processedRecords = [];
    var exceptions = [];
    
    // Parse input (assuming CSV format)
    var lines = importFileContent.split("\n");
    
    // Process each line
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        
        // Skip empty lines
        if (!line || line.trim() === "") {
            continue;
        }
        
        var fields = line.split(",");
        
        // Validate required fields
        if (fields.length < REQUIRED_FIELDS.length) {
            exceptions.push({
                line: i + 1,
                error: "Missing required fields"
            });
            continue;
        }
        
        // Extract and validate fields
        var id = fields[0] ? fields[0].trim() : "";
        var amountStr = fields[1] ? fields[1].trim() : "0";
        var quantityStr = fields[2] ? fields[2].trim() : "0";
        
        // Parse numeric values with validation
        var amount = parseFloat(amountStr);
        if (isNaN(amount)) {
            exceptions.push({
                line: i + 1,
                field: "amount",
                error: "Invalid numeric value: " + amountStr
            });
            continue;
        }
        
        var quantity = parseFloat(quantityStr);
        if (isNaN(quantity)) {
            exceptions.push({
                line: i + 1,
                field: "quantity",
                error: "Invalid numeric value: " + quantityStr
            });
            continue;
        }
        
        // Division by zero check
        var unitPrice = 0;
        if (quantity === 0) {
            exceptions.push({
                line: i + 1,
                error: "Quantity is zero, cannot calculate unit price"
            });
            continue;
        } else {
            unitPrice = amount / quantity;
        }
        
        // Round for safe comparison
        var roundedAmount = roundToDecimals(amount, ROUND_DECIMALS);
        
        // Build result record
        var record = {
            id: id,
            amount: roundedAmount,
            quantity: quantity,
            unitPrice: roundToDecimals(unitPrice, ROUND_DECIMALS),
            fileName: fileName,
            lineNumber: i + 1
        };
        
        processedRecords.push(record);
    }
    
    // Helper function: Round to specified decimals
    function roundToDecimals(num, decimals) {
        var multiplier = Math.pow(10, decimals);
        return Math.round(num * multiplier) / multiplier;
    }
    
    // Return results
    return {
        records: processedRecords,
        exceptions: exceptions,
        totalProcessed: processedRecords.length,
        totalErrors: exceptions.length
    };
}

// Invoke function with IPA variables
transformImportData(ImportFile, FileName);

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

## Integration with IPA

### IPA Assign Node Structure

```javascript

// Entire script wrapped in function
function processData(inputData, configValue) {
    // Configuration variables INSIDE function
    var MAX_RECORDS = 1000;
    var DELIMITER = ",";
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing logic
    var results = [];
    // ... transformation ...
    
    return results;
}

// Function invocation at end (NO top-level return)
processData(InputVariable, ConfigVariable);

```text

### Global Variables (Start Node)

**CRITICAL**: Start node global variables are defined in the **Properties** tab, NOT as JavaScript code.

```text

Start Node Properties (NOT JavaScript):
queryID = ""
auth = ""
rowCount = 0
accessTokenResp = ""
OutputRecords = ""
offset = 0
limit = 1000

```text

These become global variables accessible throughout the process. No `var` keyword needed in Properties tab.

### Common IPA Patterns

**Pattern: Accumulator Loop**

```javascript

var allRecords = [];
var hasMoreData = true;
var offset = 0;
var limit = 1000;

while (hasMoreData) {
    // Fetch page of data
    var pageData = fetchData(offset, limit);
    
    // Append to accumulator
    allRecords = allRecords.concat(pageData);
    
    // Check if more data exists
    hasMoreData = (pageData.length === limit);
    offset += limit;
}

```text

**Pattern: Error Collection**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    try {
        processRecord(records[i]);
    } catch (e) {
        exceptions.push({
            record: i,
            error: e.message || "Unknown error"
        });
    }
}

```text

## Advanced Features

### Code Complexity Scoring

- **Simple**: Single loop, basic operations, < 50 lines
- **Medium**: Multiple loops, conditionals, 50-150 lines
- **Complex**: Nested loops, complex logic, 150-300 lines
- **Very Complex**: Deep nesting, multiple functions, > 300 lines

### Performance Estimation

- **Fast**: O(n) complexity, simple operations
- **Moderate**: O(n²) complexity, string operations
- **Slow**: O(n³) complexity, nested loops
- **Very Slow**: Exponential complexity, inefficient algorithms

### Production Readiness Score

Based on:

- NULL/undefined handling (30%)
- Error handling (25%)
- Edge case coverage (20%)
- Type validation (15%)
- Code quality (10%)

## Usage Examples

### Example 1: Quick Question

```text

User: How do I convert an array to uppercase in ES5?

Skill: In ES5, you need to use a for loop instead of .map():

var items = ["apple", "banana", "cherry"];
var uppercased = [];
for (var i = 0; i < items.length; i++) {
    uppercased.push(items[i].toUpperCase());
}
// Result: ["APPLE", "BANANA", "CHERRY"]

```text

### Example 2: Code Review (Pasted)

```text

User: Review this:
let items = data.filter(x => x.status === "Active");

Skill: [Identifies ES6 violations: let, arrow function, .filter()]
[Provides ES5-compliant alternative with for loop]

```text

### Example 3: Code Generation

```text

User: I need JavaScript to:

1. Parse CSV input
2. Validate required fields (id, amount, quantity)
3. Calculate unit price (amount / quantity)
4. Handle division by zero
5. Collect errors

Skill: [Generates complete ES5-compliant code with:

- Input validation
- CSV parsing
- Field validation
- Safe division
- Error collection
- Proper IPA Assign node structure]

```text

### Example 4: Troubleshooting

```text

User: This code fails with "unexpected token" on line 15:
const MAX_ITEMS = 100;

Skill: The error is caused by ES6 'const' keyword. IPA uses ES5 environment.

Fix:
var MAX_ITEMS = 100;

ES5 doesn't support 'const' or 'let'. Always use 'var' for all variable declarations.

```text

### Example 5: Optimization

```text

User: This code is slow, can you optimize it?
[Shows nested loop code]

Skill: [Analyzes O(n²) complexity]
[Provides O(n) solution using lookup map]
[Explains performance improvement]

```text

### Example 6: Learning

```text

User: Explain IPA Assign node structure

Skill: [Provides detailed explanation with example]
[Shows function wrapper pattern]
[Explains configuration placement]
[Demonstrates function invocation]

```text

## Code Generation Capabilities

### Data Transformation

**Request:**

```text

Transform JSON array to CSV format with specific columns

```text

**Generates:**

- Input validation
- JSON parsing
- Field extraction
- CSV formatting
- Error handling
- ES5-compliant code

### Validation Routines

**Request:**

```text

Validate order data: required fields, numeric amounts, date formats

```text

**Generates:**

- Field presence checks
- Type validation
- Format validation
- Error collection
- Descriptive error messages

### API Response Processing

**Request:**

```text

Parse Compass API response, extract records, handle pagination

```text

**Generates:**

- JSON parsing
- NULL safety
- Array handling
- Pagination logic
- Error handling

### File Processing

**Request:**

```text

Read CSV file, parse lines, validate data, transform to JSON

```text

**Generates:**

- File content validation
- Line-by-line parsing
- Field extraction
- Data transformation
- Error collection

### Calculation Logic

**Request:**

```text

Calculate totals, subtotals, tax, with rounding and validation

```text

**Generates:**

- Safe numeric parsing
- Floating point rounding
- Division by zero checks
- Accumulation logic
- Result formatting

### Error Handling Patterns

**Request:**

```text

Collect errors during processing, categorize by severity

```text

**Generates:**

- Try-catch blocks
- Error collection array
- Error categorization
- Descriptive messages
- Error summary

## Tips for Best Results

1. **Be Specific**: Describe requirements clearly
2. **Provide Context**: Mention node type, data source, expected output
3. **Share Errors**: Include full error messages
4. **Show Examples**: Provide sample input/output data
5. **Ask Questions**: No question is too basic
6. **Request Explanations**: Ask "why" for better understanding

## Quick Reference - Common Questions

### Variables & Declarations

**Q: How do I declare variables in ES5?**

```javascript

var name = "John";
var count = 0;
var isActive = true;

```text

**Q: Can I use let or const?**
No. IPA uses ES5 environment. Always use `var`.

### Arrays

**Q: How do I loop through an array?**

```javascript

for (var i = 0; i < items.length; i++) {
    var item = items[i];
    // Process item
}

```text

**Q: How do I filter an array?**

```javascript

var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

```text

**Q: How do I map an array?**

```javascript

var mapped = [];
for (var i = 0; i < items.length; i++) {
    mapped.push(items[i].value * 2);
}

```text

### Strings

**Q: How do I concatenate strings?**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

**Q: Can I use template literals?**
No. Use string concatenation with `+` operator.

**Q: How do I check if string contains substring?**

```javascript

if (str.indexOf("substring") !== -1) {
    // Found
}

```text

### Functions

**Q: How do I write a function?**

```javascript

function calculateTotal(items) {
    var total = 0;
    for (var i = 0; i < items.length; i++) {
        total += items[i].amount;
    }
    return total;
}

```text

**Q: Can I use arrow functions?**
No. Always use `function` keyword.

### NULL Safety

**Q: How do I check for NULL/undefined?**

```javascript

if (!value || typeof value !== "string") {
    value = "";  // Default
}

```text

**Q: How do I safely access object properties?**

```javascript

var name = "";
if (person && typeof person === "object") {
    name = person.firstName || "";
}

```text

### Numbers

**Q: How do I parse numbers safely?**

```javascript

var num = parseFloat(input);
if (isNaN(num)) {
    num = 0;  // Default
}

```text

**Q: How do I compare floating point numbers?**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var rounded = roundToDecimals(0.1 + 0.2, 2);
if (rounded === 0.3) {
    // Safe comparison
}

```text

**Q: How do I check for division by zero?**

```javascript

if (denominator === 0) {
    // Handle error
    return;
}
var result = numerator / denominator;

```text

### IPA-Specific

**Q: What's the IPA Assign node structure?**

```javascript

function processData(inputData) {
    // Configuration
    var MAX_RECORDS = 1000;
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing
    var results = [];
    // ... logic ...
    
    return results;
}

// Invoke function
processData(InputVariable);

```text

**Q: How do I define global variables?**
Define them in Start node Properties tab (NOT JavaScript):

```text

queryID = ""
rowCount = 0
offset = 0

```text

**Q: How do I collect errors?**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    if (!records[i].id) {
        exceptions.push({
            record: i,
            error: "Missing ID"
        });
        continue;
    }
}

```text

### Debugging

**Q: "unexpected token" error - what does it mean?**
Usually ES6+ syntax in ES5 environment. Check for:

- `let`/`const` (use `var`)
- Arrow functions `=>` (use `function`)
- Template literals `` `${}` `` (use `+`)

**Q: "Cannot read property of undefined" - how to fix?**
Add NULL checks:

```javascript

if (obj && obj.property) {
    // Safe to access
}

```text

**Q: Code works in browser but fails in IPA - why?**
Browser supports ES6+, IPA uses ES5. Convert modern syntax to ES5.

## Limitations

This skill analyzes JavaScript syntax and patterns but cannot:

- Execute code in IPA environment
- Access IPA global variables
- Test against live data
- Validate IPA-specific functions
- Measure actual execution time

For live validation, test in IPA Designer.

## Version History

- **1.2.0** (2026-03-09): Added real-world performance scenarios and optimization best practices
  - Real-world Scenario 1: Compass API pagination (50x speedup)
  - Real-world Scenario 2: File processing with validation
  - Real-world Scenario 3: Nested loop optimization (833x speedup)
  - Performance optimization checklist (memory, speed, space)
  - Performance measurement tips
- **1.1.0** (2026-03-09): Added string concatenation performance pattern
  - New Pattern 10: String Concatenation in Loops (O(n²) vs O(n) complexity)
  - Performance comparison table (50-500x speedup for large datasets)
  - Pagination loop optimization guidance
  - Array accumulation pattern for data aggregation
- **1.0.0** (2026-03-09): Initial release with comprehensive ES5 analysis
.Value -replace '```', '```text' 
   Loads `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` with:
   - IPA JavaScript ES5 compliance rules
   - Assign node structure
   - Start node global variables
   - Activity types and patterns

2. **Process Patterns** (for code generation):

   ```text\n ---
name: "ipa-javascript-es5-analyzer"
description: "Your JavaScript genius for IPA. Analyzes, reviews, optimizes, debugs, and writes ES5-compliant JavaScript. Handles code review, creation, troubleshooting, and best practices. Use for any JavaScript-related task in IPA."
---

# IPA JavaScript ES5 Genius

Your comprehensive JavaScript expert for IPA. Not just a code reviewer - a full-featured JavaScript assistant that analyzes, creates, optimizes, debugs, and teaches ES5-compliant JavaScript for IPA processes.

## What This Skill Does

This skill is your JavaScript genius that can:

1. **Analyze & Review** - Comprehensive code analysis for ES5 compliance, best practices, performance
2. **Create & Generate** - Write production-ready ES5 JavaScript from requirements
3. **Debug & Fix** - Troubleshoot runtime errors, identify root causes, provide fixes
4. **Optimize & Improve** - Enhance performance, refactor code, apply best practices
5. **Teach & Explain** - Answer JavaScript questions, explain concepts, provide examples
6. **Convert & Migrate** - Transform ES6+ code to ES5, modernize legacy code

## When to Use

**Code Review & Analysis:**

- Reviewing JavaScript before deployment
- Validating ES5 compliance
- Identifying performance issues
- Ensuring production readiness

**Code Creation:**

- Writing new IPA JavaScript from scratch
- Generating Assign node logic
- Creating data transformation functions
- Building validation routines

**Troubleshooting:**

- Debugging runtime errors
- Fixing "unexpected token" errors
- Resolving NULL/undefined issues
- Solving performance problems

**Learning & Questions:**

- Understanding ES5 constraints
- Learning IPA JavaScript patterns
- Getting code examples
- Best practices guidance

**Optimization:**

- Improving slow code
- Reducing complexity
- Enhancing readability
- Applying defensive patterns

## Critical ES5 Rules

**IPA JavaScript executes in ES5 environment. Modern syntax causes immediate runtime errors.**

### Forbidden ES6+ Features

| Feature | ES6+ (FORBIDDEN) | ES5 (REQUIRED) |
|---------|------------------|----------------|
| Variables | `let x = 1;` `const x = 1;` | `var x = 1;` |
| Functions | `() => {}` `async/await` | `function() {}` |
| Strings | `` `Hello ${name}` `` | `"Hello " + name` |
| Destructuring | `var {prop} = obj;` | `var prop = obj.prop;` |
| Default params | `function f(x = 1)` | Check inside function |
| Spread | `[...arr]` | `arr.slice()` |
| Classes | `class MyClass {}` | Constructor functions |
| Modules | `import/export` | Not supported |
| Promises | `new Promise()` | Not supported |
| Template literals | `` `text` `` | `"text"` |

### Allowed ES5 Features

- `var` declarations
- `function` keyword
- Traditional for loops
- `if/else`, `switch`, ternary operator
- Object literals: `{key: value}`
- Array literals: `[1, 2, 3]`
- String concatenation: `+`
- All ES5 built-in methods

## How to Use This Skill

### Quick Questions

Just ask! No code needed:

```text

User: How do I loop through an array in ES5?
User: What's the ES5 way to filter an array?
User: How do I handle NULL values safely?
User: Show me an IPA Assign node structure

```text

### Code Review (Paste in Chat)

For short code (< 100 lines), paste directly:

```text

User: Review this code:
var items = data.filter(x => x.status === "Active");
let count = items.length;

Skill: [Identifies ES6 violations and provides ES5 fix]

```text

### Code Review (File-Based)

For longer code, save to file:

```text

User: Analyze Temp/assign_node_code.js

Skill: [Reads file, performs comprehensive analysis]

```text

### Code Generation

Describe what you need:

```text

User: I need JavaScript to parse a CSV file, validate required fields, 
and calculate totals. It should handle empty lines and invalid numbers.

Skill: [Generates complete ES5-compliant code with error handling]

```text

### Troubleshooting

Share the error:

```text

User: My code is failing with "unexpected token" error on line 23

Skill: [Analyzes code, identifies ES6+ syntax, provides fix]

```text

### Learning & Examples

Ask for explanations:

```text

User: Explain the difference between var and let
User: Show me how to do pagination in IPA
User: What's the best way to handle floating point comparison?

Skill: [Provides detailed explanation with examples]

```text

## Activation Instructions

**CRITICAL**: When this skill is activated, the following steering files are automatically loaded:

1. **IPA Guide** (REQUIRED):

   ```text\ndiscloseContext(name="ipa-ipd-guide")

   ```

   Loads `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` with:

- IPA JavaScript ES5 compliance rules
- Assign node structure
- Start node global variables
- Activity types and patterns

1. **Process Patterns** (for code generation):

   ```text\ndiscloseContext(name="process-patterns")

   ```

   Loads `.kiro/steering/04_Process_Patterns_Library.md` with:
   - 450+ analyzed IPA workflows
   - Common JavaScript patterns
   - Data transformation examples
   - Validation routines

2. **FSM Business Classes** (for API integration):

   ```text\ndiscloseContext(name="fsm-business-classes")

   ```

   Loads `.kiro/steering/07_FSM_Business_Classes_and_API.md` when working with:
   - WebRun activities
   - Landmark API calls
   - FSM business class operations

3. **Data Fabric** (for Compass SQL integration):

   ```text\ndiscloseContext(name="data-fabric-guide")

   ```

   Loads `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md` when working with:
   - Compass API JavaScript
   - Data Lake queries
   - JSON parsing from API responses

**The skill will automatically load relevant steering files based on the task context.**

The skill performs comprehensive analysis across 6 dimensions:

1. **ES5 Compliance**

   - No `let`/`const` (use `var`)
   - No arrow functions (use `function`)
   - No template literals (use string concatenation)
   - No destructuring (explicit property access)
   - No default parameters (check inside function)
   - No spread operator (use `.slice()`, `.concat()`)
   - No ES6+ methods (`.map()`, `.filter()`, `.find()`)

2. **Best Practices**

   - Defensive NULL/undefined checks
   - Input validation
   - Type checking before operations
   - Proper error handling
   - Meaningful variable names
   - Comments for complex logic

3. **Performance**

   - Efficient loops (avoid nested loops where possible)
   - String concatenation optimization
   - Array operations efficiency
   - Avoid redundant calculations
   - Memory-efficient patterns

4. **Production Readiness**

   - Edge case handling (empty strings, zero, NULL)
   - Floating point comparison (rounding)
   - Division by zero checks
   - Array bounds checking
   - Safe type conversions

5. **Code Quality**

   - Readability (formatting, indentation)
   - Maintainability (modularity, reusability)
   - Naming conventions (descriptive names)
   - Comment quality
   - Code organization

6. **IPA-Specific Patterns**

   - Assign node structure (function wrapper)
   - Global variable usage
   - Configuration at top of function
   - No top-level return statements
   - Function invocation at end

### Step 3: Recommendations

For each issue found, provides:

- **Severity**: Critical / High / Medium / Low
- **Category**: ES5 Compliance / Best Practices / Performance / Production Readiness
- **Explanation**: Why this matters
- **Fix**: Specific code changes
- **Example**: Before/after comparison

### Step 4: Improved Code

Generates refactored code with:

- All ES6+ features converted to ES5
- Best practices applied
- Performance optimizations
- Production-ready error handling
- Comments explaining changes

## Analysis Categories

### ES5 Compliance Issues

**Critical:**

- `let` or `const` declarations
- Arrow functions `() => {}`
- Template literals `` `${var}` ``
- `async`/`await`
- Destructuring `{prop} = obj`
- Spread operator `...arr`
- ES6+ methods (`.map()`, `.filter()`, `.find()`)

**High:**

- Default parameters `function(x = 1)`
- `class` keyword
- `import`/`export` statements
- `Promise` usage
- `for...of` loops

**Medium:**

- Object shorthand `{prop}` instead of `{prop: prop}`
- Computed property names `{[key]: value}`
- Method shorthand `{method() {}}`

### Best Practices Issues

**Critical:**

- No NULL/undefined checks before operations
- No input validation
- Missing error handling
- Unsafe type conversions

**High:**

- No defensive programming patterns
- Missing edge case handling
- Unclear variable names
- No comments for complex logic

**Medium:**

- Inconsistent naming conventions
- Poor code organization
- Redundant code
- Magic numbers without explanation

### Performance Issues

**Critical:**

- Nested loops with high complexity
- **String concatenation in loops** (O(n²) complexity - use array accumulation)
- Redundant calculations inside loops

**High:**

- Unnecessary array iterations
- Inefficient search patterns
- Memory-intensive operations

**Medium:**

- Suboptimal algorithm choices
- Unnecessary variable declarations
- Redundant type checks

### Production Readiness Issues

**Critical:**

- No division by zero checks
- No floating point rounding before comparison
- Missing NULL guards on critical operations

**High:**

- No empty string/array checks
- Missing array bounds validation
- Unsafe parseInt/parseFloat usage

**Medium:**

- No default value handling
- Missing type validation
- Insufficient error messages

## Common Patterns Analyzed

### Pattern 1: Variable Declarations

**Bad (ES6):**

```javascript

let count = 0;
const MAX_ITEMS = 100;

```text

**Good (ES5):**

```javascript

var count = 0;
var MAX_ITEMS = 100;

```text

### Pattern 2: Arrow Functions

**Bad (ES6):**

```javascript

var result = items.map(item => item.value);

```text

**Good (ES5):**

```javascript

var result = [];
for (var i = 0; i < items.length; i++) {
    result.push(items[i].value);
}

```text

### Pattern 3: Template Literals

**Bad (ES6):**

```javascript

var message = `Hello ${name}, you have ${count} items`;

```text

**Good (ES5):**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

### Pattern 4: Destructuring

**Bad (ES6):**

```javascript

var {firstName, lastName} = person;

```text

**Good (ES5):**

```javascript

var firstName = person.firstName;
var lastName = person.lastName;

```text

### Pattern 5: Default Parameters

**Bad (ES6):**

```javascript

function calculate(amount, rate = 0.05) {
    return amount * rate;
}

```text

**Good (ES5):**

```javascript

function calculate(amount, rate) {
    if (typeof rate === "undefined") {
        rate = 0.05;
    }
    return amount * rate;
}

```text

### Pattern 6: Spread Operator

**Bad (ES6):**

```javascript

var combined = [...array1, ...array2];

```text

**Good (ES5):**

```javascript

var combined = array1.concat(array2);

```text

### Pattern 7: Defensive NULL Checks

**Bad:**

```javascript

var total = parseFloat(amount);
if (total === 0) {
    // May fail if amount is NULL/undefined
}

```text

**Good:**

```javascript

if (!amount || typeof amount !== "string") {
    amount = "0";
}
var total = parseFloat(amount);
if (isNaN(total)) {
    total = 0;
}
if (total === 0) {
    // Safe comparison
}

```text

### Pattern 8: Floating Point Comparison

**Bad:**

```javascript

if (sumQty === 0) {
    // Unreliable for floating point
}

```text

**Good:**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var roundedSum = roundToDecimals(sumQty, 2);
if (roundedSum === 0) {
    // Safe comparison
}

```text

### Pattern 9: Division by Zero

**Bad:**

```javascript

var unitCost = extendedAmount / originalQuantity;

```

### Pattern 10: String Concatenation in Loops (CRITICAL PERFORMANCE)

**Bad (O(n²) complexity):**

```javascript
// Inside pagination loop (100+ iterations)
OutputRecords += GetResultOut + "

";
```

**Why It's Bad:**
- Strings are immutable in JavaScript
- Each `+=` creates a NEW string and copies ALL previous content
- 100 iterations = ~5MB copied for 100KB of data
- Performance degrades exponentially with data size

**Good (O(n) complexity):**

```javascript
// BEFORE the pagination loop
var OutputRecordsArray = [];

// INSIDE the pagination loop
while (hasMoreData) {
    // ... fetch and transform data ...
    
    // Push to array instead of string concatenation
    for (var i = 0; i < transformedLines.length; i++) {
        OutputRecordsArray.push(transformedLines[i]);
    }
    
    // ... pagination logic ...
    offset += limit;
}

// AFTER the loop completes - join once
var OutputRecords = OutputRecordsArray.join("

");
```

**Performance Comparison:**

| Approach | Complexity | 100 Iterations | 1000 Iterations |
|----------|-----------|----------------|-----------------|
| String += | O(n²) | ~5MB copied | ~500MB copied |
| Array.push() + join() | O(n) | ~100KB copied | ~1MB copied |
| **Speedup** | **Linear** | **50x faster** | **500x faster** |

**When to Use:**
- Any loop with 10+ iterations
- Pagination loops processing large datasets
- File processing with line-by-line accumulation
- Data transformation with result aggregationtext

**Good:**

```javascript

if (originalQuantity === 0) {
    exceptions.push({error: "Division by zero"});
    continue;
}
var unitCost = extendedAmount / originalQuantity;

```text

### Pattern 11: IPA Assign Node Structure

**Bad:**

```javascript

// Top-level code
var result = processData(input);
return result;  // ERROR: No top-level return

```text

**Good:**

```javascript

function transformData(inputData, fileName) {
    // Configuration variables
    var CONFIG_VALUE = "setting";
    
    // Validation
    if (!inputData || typeof inputData !== "string") {
        inputData = "";
    }
    
    // Processing logic
    var result = [];
    // ... transformation ...
    
    return result;
}

// Function invocation at end
transformData(ImportFile, FileName);

```

## Real-World Performance Scenarios

### Scenario 1: Compass API Pagination (Production)

**Context**: MatchReport_Outbound.lpd processing 50,000 GL transactions

**Bad Implementation (O(n²) - 45 minutes execution)**:

```javascript
// Global variable
var OutputRecords = "";

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        GetResultArr[i] = GetResultArr[i].replace(/,/g, "|");
    }
    GetResultOut = GetResultArr.join("
");
    
    // ❌ BAD: String concatenation in loop
    OutputRecords += GetResultOut + "
";  // O(n²) complexity
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}
```

**Performance Impact**:
- Iteration 1: Copy 10KB
- Iteration 100: Copy 1MB (100 × 10KB)
- Iteration 500: Copy 5MB (500 × 10KB)
- Total: ~1.25GB copied for 5MB of data
- Execution time: 45 minutes

**Good Implementation (O(n) - 54 seconds execution)**:

```javascript
// Global variable (array accumulator)
var OutputRecordsArray = [];

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        var line = GetResultArr[i];
        if (line && line.trim() !== "") {
            // ✅ GOOD: Push to array
            OutputRecordsArray.push(line.replace(/,/g, "|"));
        }
    }
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}

// Join once after loop completes
var OutputRecords = OutputRecordsArray.join("
");
```

**Performance Improvement**:
- Total: ~5MB copied (linear growth)
- Execution time: 54 seconds
- **Speedup: 50x faster**
- Memory efficiency: 250x less copying

### Scenario 2: File Processing with Validation

**Context**: Invoice import processing 10,000 lines with validation

**Bad Implementation (Multiple Issues)**:

```javascript
var validRecords = "";
var errorRecords = "";

for (var i = 0; i < lines.length; i++) {
    var fields = lines[i].split(",");
    
    // ❌ Issue 1: No NULL check
    var amount = parseFloat(fields[2]);
    
    // ❌ Issue 2: Floating point comparison without rounding
    if (amount === 0) {
        errorRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    } else {
        validRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    }
}
```

**Good Implementation (All Best Practices)**:

```javascript
var validRecordsArray = [];
var errorRecordsArray = [];

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    
    // ✅ Skip empty lines
    if (!line || line.trim() === "") {
        continue;
    }
    
    var fields = line.split(",");
    
    // ✅ Validate field count
    if (fields.length < 3) {
        errorRecordsArray.push(line + "|Missing fields");
        continue;
    }
    
    // ✅ NULL check and safe parsing
    var amountStr = fields[2] ? fields[2].trim() : "0";
    var amount = parseFloat(amountStr);
    
    // ✅ Validate numeric
    if (isNaN(amount)) {
        errorRecordsArray.push(line + "|Invalid amount: " + amountStr);
        continue;
    }
    
    // ✅ Round before comparison
    var roundedAmount = roundToDecimals(amount, 2);
    
    if (roundedAmount === 0) {
        errorRecordsArray.push(line + "|Zero amount");
    } else {
        validRecordsArray.push(line);
    }
}

// ✅ Join once at end
var validRecords = validRecordsArray.join("
");
var errorRecords = errorRecordsArray.join("
");
```

**Improvements**:
- Array accumulation (50x faster for large datasets)
- NULL safety (prevents runtime errors)
- Floating point rounding (prevents comparison bugs)
- Input validation (catches data quality issues)
- Empty line handling (cleaner output)

### Scenario 3: Nested Loop Optimization

**Context**: Matching 1,000 invoices against 5,000 PO lines

**Bad Implementation (O(n²) - 5 million comparisons)**:

```javascript
var matchedInvoices = [];

// ❌ Nested loop without optimization
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < poLines.length; j++) {
        if (invoices[i].poNumber === poLines[j].poNumber &&
            invoices[i].lineNumber === poLines[j].lineNumber) {
            matchedInvoices.push({
                invoice: invoices[i],
                poLine: poLines[j]
            });
            break;  // At least breaks after match
        }
    }
}
```

**Good Implementation (O(n) - 6,000 operations)**:

```javascript
// ✅ Build lookup map (O(n))
var poLookup = {};
for (var i = 0; i < poLines.length; i++) {
    var key = poLines[i].poNumber + "|" + poLines[i].lineNumber;
    poLookup[key] = poLines[i];
}

// ✅ Single loop with map lookup (O(n))
var matchedInvoices = [];
for (var i = 0; i < invoices.length; i++) {
    var key = invoices[i].poNumber + "|" + invoices[i].lineNumber;
    var poLine = poLookup[key];
    
    if (poLine) {
        matchedInvoices.push({
            invoice: invoices[i],
            poLine: poLine
        });
    }
}
```

**Performance Improvement**:
- Bad: 5,000,000 comparisons (1,000 × 5,000)
- Good: 6,000 operations (5,000 + 1,000)
- **Speedup: 833x faster**

## Performance Optimization Checklist

### Memory Optimization

**1. Array Accumulation vs String Concatenation**

```javascript
// ❌ BAD: O(n²) memory copying
var result = "";
for (var i = 0; i < 1000; i++) {
    result += data[i] + "
";  // Creates 1000 new strings
}

// ✅ GOOD: O(n) memory usage
var resultArray = [];
for (var i = 0; i < 1000; i++) {
    resultArray.push(data[i]);  // Reuses array memory
}
var result = resultArray.join("
");  // Single allocation
```

**2. Reuse Variables Instead of Creating New Ones**

```javascript
// ❌ BAD: Creates 1000 new variables
for (var i = 0; i < 1000; i++) {
    var temp = data[i].toUpperCase();
    var trimmed = temp.trim();
    var replaced = trimmed.replace(/,/g, "|");
    results.push(replaced);
}

// ✅ GOOD: Reuses single variable
var temp;
for (var i = 0; i < 1000; i++) {
    temp = data[i].toUpperCase().trim().replace(/,/g, "|");
    results.push(temp);
}
```

**3. Avoid Unnecessary Array Copies**

```javascript
// ❌ BAD: Creates new array on each iteration
for (var i = 0; i < items.length; i++) {
    var subset = items.slice(0, i);  // O(n²) total
    process(subset);
}

// ✅ GOOD: Process in place
for (var i = 0; i < items.length; i++) {
    process(items, i);  // Pass index instead
}
```

### Speed Optimization

**1. Hoist Invariant Calculations Outside Loops**

```javascript
// ❌ BAD: Calculates same value 1000 times
for (var i = 0; i < 1000; i++) {
    var multiplier = Math.pow(10, 2);  // Recalculated each iteration
    results.push(data[i] * multiplier);
}

// ✅ GOOD: Calculate once
var multiplier = Math.pow(10, 2);
for (var i = 0; i < 1000; i++) {
    results.push(data[i] * multiplier);
}
```

**2. Cache Array Length**

```javascript
// ❌ BAD: Accesses .length property 1000 times
for (var i = 0; i < items.length; i++) {
    process(items[i]);
}

// ✅ GOOD: Cache length (minor optimization, but good practice)
var len = items.length;
for (var i = 0; i < len; i++) {
    process(items[i]);
}
```

**3. Use Lookup Maps for Repeated Searches**

```javascript
// ❌ BAD: O(n²) - searches array repeatedly
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < vendors.length; j++) {
        if (invoices[i].vendorId === vendors[j].id) {
            invoices[i].vendorName = vendors[j].name;
            break;
        }
    }
}

// ✅ GOOD: O(n) - build map once, lookup is O(1)
var vendorMap = {};
for (var i = 0; i < vendors.length; i++) {
    vendorMap[vendors[i].id] = vendors[i].name;
}
for (var i = 0; i < invoices.length; i++) {
    invoices[i].vendorName = vendorMap[invoices[i].vendorId] || "";
}
```

**4. Compile Regex Outside Loops**

```javascript
// ❌ BAD: Compiles regex 1000 times
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(/[^0-9]/g, "");  // Regex compiled each time
    results.push(cleaned);
}

// ✅ GOOD: Compile once (ES5 doesn't have explicit compilation, but pattern is cached)
var digitPattern = /[^0-9]/g;
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(digitPattern, "");
    results.push(cleaned);
}
```

### Space Optimization

**1. Clear Large Variables After Use**

```javascript
// Process large dataset
var largeData = fetchLargeDataset();  // 10MB
var processed = processData(largeData);

// ✅ Clear reference to allow garbage collection
largeData = null;

// Continue with processed data
return processed;
```

**2. Process Data in Chunks**

```javascript
// ❌ BAD: Load entire file into memory
var allLines = fileContent.split("
");  // 100MB in memory
var results = [];
for (var i = 0; i < allLines.length; i++) {
    results.push(processLine(allLines[i]));
}

// ✅ GOOD: Process in chunks (if possible)
var CHUNK_SIZE = 1000;
var results = [];
var lines = fileContent.split("
");

for (var i = 0; i < lines.length; i += CHUNK_SIZE) {
    var chunk = lines.slice(i, i + CHUNK_SIZE);
    for (var j = 0; j < chunk.length; j++) {
        results.push(processLine(chunk[j]));
    }
    chunk = null;  // Clear chunk
}
```

## Performance Measurement Tips

### Timing Code Execution

```javascript
// Start timer
var startTime = new Date().getTime();

// Your code here
for (var i = 0; i < 10000; i++) {
    // ... processing ...
}

// End timer
var endTime = new Date().getTime();
var elapsedMs = endTime - startTime;

// Log result
console.log("Execution time: " + elapsedMs + "ms");
```

### Memory Usage Estimation

```javascript
// Estimate string memory usage
function estimateStringMemory(str) {
    // Each character is ~2 bytes in JavaScript
    return str.length * 2;
}

// Estimate array memory usage
function estimateArrayMemory(arr) {
    var total = 0;
    for (var i = 0; i < arr.length; i++) {
        if (typeof arr[i] === "string") {
            total += arr[i].length * 2;
        }
    }
    return total;
}

// Example usage
var data = "Large string data...";
var memoryBytes = estimateStringMemory(data);
var memoryMB = memoryBytes / (1024 * 1024);
console.log("Estimated memory: " + memoryMB.toFixed(2) + " MB");
```text

## Output Format

### Analysis Summary

```text

📊 IPA JAVASCRIPT ES5 ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code: [First 50 chars...]
Lines: 85
Complexity: Medium
Node Type: Assign

OVERALL ASSESSMENT: ⚠️ NEEDS IMPROVEMENT

Critical Issues: 3 (ES5 compliance violations)
High Priority: 5 (Missing NULL checks)
Medium Priority: 8 (Performance optimizations)
Low Priority: 2 (Code quality)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Issue Details

```text

🔴 CRITICAL: Arrow Function Usage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Category: ES5 Compliance
Impact: Runtime error in IPA (arrow functions not supported)
Line: 23

Issue:
Arrow function syntax is ES6+ and will cause immediate runtime error
in IPA's ES5 JavaScript environment.

Current Code:
var filtered = items.filter(item => item.status === "Active");

Recommended Fix:
var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

Explanation:
IPA JavaScript executes in ES5 environment. Use traditional for loops
and function keyword instead of arrow functions and array methods like
.filter(), .map(), .find().

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Improved Code

```text

✅ IMPROVED CODE (ES5 COMPLIANT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied:

1. Converted all let/const to var
2. Replaced arrow functions with function keyword
3. Replaced template literals with string concatenation
4. Added NULL/undefined checks
5. Added floating point rounding
6. Added division by zero checks

7. Improved error handling
8. Added descriptive comments

// IPA Assign Node: Transform Import Data
// Purpose: Parse and validate import file content
// Input: ImportFile (string), FileName (string)
// Output: Processed records array

function transformImportData(importFileContent, fileName) {
    // Configuration
    var ROUND_DECIMALS = 2;
    var REQUIRED_FIELDS = ["id", "amount", "quantity"];
    
    // Input validation
    if (!importFileContent || typeof importFileContent !== "string") {
        importFileContent = "";
    }
    
    if (!fileName || typeof fileName !== "string") {
        fileName = "unknown";
    }
    
    // Initialize result arrays
    var processedRecords = [];
    var exceptions = [];
    
    // Parse input (assuming CSV format)
    var lines = importFileContent.split("\n");
    
    // Process each line
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        
        // Skip empty lines
        if (!line || line.trim() === "") {
            continue;
        }
        
        var fields = line.split(",");
        
        // Validate required fields
        if (fields.length < REQUIRED_FIELDS.length) {
            exceptions.push({
                line: i + 1,
                error: "Missing required fields"
            });
            continue;
        }
        
        // Extract and validate fields
        var id = fields[0] ? fields[0].trim() : "";
        var amountStr = fields[1] ? fields[1].trim() : "0";
        var quantityStr = fields[2] ? fields[2].trim() : "0";
        
        // Parse numeric values with validation
        var amount = parseFloat(amountStr);
        if (isNaN(amount)) {
            exceptions.push({
                line: i + 1,
                field: "amount",
                error: "Invalid numeric value: " + amountStr
            });
            continue;
        }
        
        var quantity = parseFloat(quantityStr);
        if (isNaN(quantity)) {
            exceptions.push({
                line: i + 1,
                field: "quantity",
                error: "Invalid numeric value: " + quantityStr
            });
            continue;
        }
        
        // Division by zero check
        var unitPrice = 0;
        if (quantity === 0) {
            exceptions.push({
                line: i + 1,
                error: "Quantity is zero, cannot calculate unit price"
            });
            continue;
        } else {
            unitPrice = amount / quantity;
        }
        
        // Round for safe comparison
        var roundedAmount = roundToDecimals(amount, ROUND_DECIMALS);
        
        // Build result record
        var record = {
            id: id,
            amount: roundedAmount,
            quantity: quantity,
            unitPrice: roundToDecimals(unitPrice, ROUND_DECIMALS),
            fileName: fileName,
            lineNumber: i + 1
        };
        
        processedRecords.push(record);
    }
    
    // Helper function: Round to specified decimals
    function roundToDecimals(num, decimals) {
        var multiplier = Math.pow(10, decimals);
        return Math.round(num * multiplier) / multiplier;
    }
    
    // Return results
    return {
        records: processedRecords,
        exceptions: exceptions,
        totalProcessed: processedRecords.length,
        totalErrors: exceptions.length
    };
}

// Invoke function with IPA variables
transformImportData(ImportFile, FileName);

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

## Integration with IPA

### IPA Assign Node Structure

```javascript

// Entire script wrapped in function
function processData(inputData, configValue) {
    // Configuration variables INSIDE function
    var MAX_RECORDS = 1000;
    var DELIMITER = ",";
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing logic
    var results = [];
    // ... transformation ...
    
    return results;
}

// Function invocation at end (NO top-level return)
processData(InputVariable, ConfigVariable);

```text

### Global Variables (Start Node)

**CRITICAL**: Start node global variables are defined in the **Properties** tab, NOT as JavaScript code.

```text

Start Node Properties (NOT JavaScript):
queryID = ""
auth = ""
rowCount = 0
accessTokenResp = ""
OutputRecords = ""
offset = 0
limit = 1000

```text

These become global variables accessible throughout the process. No `var` keyword needed in Properties tab.

### Common IPA Patterns

**Pattern: Accumulator Loop**

```javascript

var allRecords = [];
var hasMoreData = true;
var offset = 0;
var limit = 1000;

while (hasMoreData) {
    // Fetch page of data
    var pageData = fetchData(offset, limit);
    
    // Append to accumulator
    allRecords = allRecords.concat(pageData);
    
    // Check if more data exists
    hasMoreData = (pageData.length === limit);
    offset += limit;
}

```text

**Pattern: Error Collection**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    try {
        processRecord(records[i]);
    } catch (e) {
        exceptions.push({
            record: i,
            error: e.message || "Unknown error"
        });
    }
}

```text

## Advanced Features

### Code Complexity Scoring

- **Simple**: Single loop, basic operations, < 50 lines
- **Medium**: Multiple loops, conditionals, 50-150 lines
- **Complex**: Nested loops, complex logic, 150-300 lines
- **Very Complex**: Deep nesting, multiple functions, > 300 lines

### Performance Estimation

- **Fast**: O(n) complexity, simple operations
- **Moderate**: O(n²) complexity, string operations
- **Slow**: O(n³) complexity, nested loops
- **Very Slow**: Exponential complexity, inefficient algorithms

### Production Readiness Score

Based on:

- NULL/undefined handling (30%)
- Error handling (25%)
- Edge case coverage (20%)
- Type validation (15%)
- Code quality (10%)

## Usage Examples

### Example 1: Quick Question

```text

User: How do I convert an array to uppercase in ES5?

Skill: In ES5, you need to use a for loop instead of .map():

var items = ["apple", "banana", "cherry"];
var uppercased = [];
for (var i = 0; i < items.length; i++) {
    uppercased.push(items[i].toUpperCase());
}
// Result: ["APPLE", "BANANA", "CHERRY"]

```text

### Example 2: Code Review (Pasted)

```text

User: Review this:
let items = data.filter(x => x.status === "Active");

Skill: [Identifies ES6 violations: let, arrow function, .filter()]
[Provides ES5-compliant alternative with for loop]

```text

### Example 3: Code Generation

```text

User: I need JavaScript to:

1. Parse CSV input
2. Validate required fields (id, amount, quantity)
3. Calculate unit price (amount / quantity)
4. Handle division by zero
5. Collect errors

Skill: [Generates complete ES5-compliant code with:

- Input validation
- CSV parsing
- Field validation
- Safe division
- Error collection
- Proper IPA Assign node structure]

```text

### Example 4: Troubleshooting

```text

User: This code fails with "unexpected token" on line 15:
const MAX_ITEMS = 100;

Skill: The error is caused by ES6 'const' keyword. IPA uses ES5 environment.

Fix:
var MAX_ITEMS = 100;

ES5 doesn't support 'const' or 'let'. Always use 'var' for all variable declarations.

```text

### Example 5: Optimization

```text

User: This code is slow, can you optimize it?
[Shows nested loop code]

Skill: [Analyzes O(n²) complexity]
[Provides O(n) solution using lookup map]
[Explains performance improvement]

```text

### Example 6: Learning

```text

User: Explain IPA Assign node structure

Skill: [Provides detailed explanation with example]
[Shows function wrapper pattern]
[Explains configuration placement]
[Demonstrates function invocation]

```text

## Code Generation Capabilities

### Data Transformation

**Request:**

```text

Transform JSON array to CSV format with specific columns

```text

**Generates:**

- Input validation
- JSON parsing
- Field extraction
- CSV formatting
- Error handling
- ES5-compliant code

### Validation Routines

**Request:**

```text

Validate order data: required fields, numeric amounts, date formats

```text

**Generates:**

- Field presence checks
- Type validation
- Format validation
- Error collection
- Descriptive error messages

### API Response Processing

**Request:**

```text

Parse Compass API response, extract records, handle pagination

```text

**Generates:**

- JSON parsing
- NULL safety
- Array handling
- Pagination logic
- Error handling

### File Processing

**Request:**

```text

Read CSV file, parse lines, validate data, transform to JSON

```text

**Generates:**

- File content validation
- Line-by-line parsing
- Field extraction
- Data transformation
- Error collection

### Calculation Logic

**Request:**

```text

Calculate totals, subtotals, tax, with rounding and validation

```text

**Generates:**

- Safe numeric parsing
- Floating point rounding
- Division by zero checks
- Accumulation logic
- Result formatting

### Error Handling Patterns

**Request:**

```text

Collect errors during processing, categorize by severity

```text

**Generates:**

- Try-catch blocks
- Error collection array
- Error categorization
- Descriptive messages
- Error summary

## Tips for Best Results

1. **Be Specific**: Describe requirements clearly
2. **Provide Context**: Mention node type, data source, expected output
3. **Share Errors**: Include full error messages
4. **Show Examples**: Provide sample input/output data
5. **Ask Questions**: No question is too basic
6. **Request Explanations**: Ask "why" for better understanding

## Quick Reference - Common Questions

### Variables & Declarations

**Q: How do I declare variables in ES5?**

```javascript

var name = "John";
var count = 0;
var isActive = true;

```text

**Q: Can I use let or const?**
No. IPA uses ES5 environment. Always use `var`.

### Arrays

**Q: How do I loop through an array?**

```javascript

for (var i = 0; i < items.length; i++) {
    var item = items[i];
    // Process item
}

```text

**Q: How do I filter an array?**

```javascript

var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

```text

**Q: How do I map an array?**

```javascript

var mapped = [];
for (var i = 0; i < items.length; i++) {
    mapped.push(items[i].value * 2);
}

```text

### Strings

**Q: How do I concatenate strings?**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

**Q: Can I use template literals?**
No. Use string concatenation with `+` operator.

**Q: How do I check if string contains substring?**

```javascript

if (str.indexOf("substring") !== -1) {
    // Found
}

```text

### Functions

**Q: How do I write a function?**

```javascript

function calculateTotal(items) {
    var total = 0;
    for (var i = 0; i < items.length; i++) {
        total += items[i].amount;
    }
    return total;
}

```text

**Q: Can I use arrow functions?**
No. Always use `function` keyword.

### NULL Safety

**Q: How do I check for NULL/undefined?**

```javascript

if (!value || typeof value !== "string") {
    value = "";  // Default
}

```text

**Q: How do I safely access object properties?**

```javascript

var name = "";
if (person && typeof person === "object") {
    name = person.firstName || "";
}

```text

### Numbers

**Q: How do I parse numbers safely?**

```javascript

var num = parseFloat(input);
if (isNaN(num)) {
    num = 0;  // Default
}

```text

**Q: How do I compare floating point numbers?**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var rounded = roundToDecimals(0.1 + 0.2, 2);
if (rounded === 0.3) {
    // Safe comparison
}

```text

**Q: How do I check for division by zero?**

```javascript

if (denominator === 0) {
    // Handle error
    return;
}
var result = numerator / denominator;

```text

### IPA-Specific

**Q: What's the IPA Assign node structure?**

```javascript

function processData(inputData) {
    // Configuration
    var MAX_RECORDS = 1000;
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing
    var results = [];
    // ... logic ...
    
    return results;
}

// Invoke function
processData(InputVariable);

```text

**Q: How do I define global variables?**
Define them in Start node Properties tab (NOT JavaScript):

```text

queryID = ""
rowCount = 0
offset = 0

```text

**Q: How do I collect errors?**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    if (!records[i].id) {
        exceptions.push({
            record: i,
            error: "Missing ID"
        });
        continue;
    }
}

```text

### Debugging

**Q: "unexpected token" error - what does it mean?**
Usually ES6+ syntax in ES5 environment. Check for:

- `let`/`const` (use `var`)
- Arrow functions `=>` (use `function`)
- Template literals `` `${}` `` (use `+`)

**Q: "Cannot read property of undefined" - how to fix?**
Add NULL checks:

```javascript

if (obj && obj.property) {
    // Safe to access
}

```text

**Q: Code works in browser but fails in IPA - why?**
Browser supports ES6+, IPA uses ES5. Convert modern syntax to ES5.

## Limitations

This skill analyzes JavaScript syntax and patterns but cannot:

- Execute code in IPA environment
- Access IPA global variables
- Test against live data
- Validate IPA-specific functions
- Measure actual execution time

For live validation, test in IPA Designer.

## Version History

- **1.2.0** (2026-03-09): Added real-world performance scenarios and optimization best practices
  - Real-world Scenario 1: Compass API pagination (50x speedup)
  - Real-world Scenario 2: File processing with validation
  - Real-world Scenario 3: Nested loop optimization (833x speedup)
  - Performance optimization checklist (memory, speed, space)
  - Performance measurement tips
- **1.1.0** (2026-03-09): Added string concatenation performance pattern
  - New Pattern 10: String Concatenation in Loops (O(n²) vs O(n) complexity)
  - Performance comparison table (50-500x speedup for large datasets)
  - Pagination loop optimization guidance
  - Array accumulation pattern for data aggregation
- **1.0.0** (2026-03-09): Initial release with comprehensive ES5 analysis
.Value -replace '```', '```text' 
   Loads `.kiro/steering/04_Process_Patterns_Library.md` with:
   - 450+ analyzed IPA workflows
   - Common JavaScript patterns
   - Data transformation examples
   - Validation routines

3. **FSM Business Classes** (for API integration):

   ```text\n ---
name: "ipa-javascript-es5-analyzer"
description: "Your JavaScript genius for IPA. Analyzes, reviews, optimizes, debugs, and writes ES5-compliant JavaScript. Handles code review, creation, troubleshooting, and best practices. Use for any JavaScript-related task in IPA."
---

# IPA JavaScript ES5 Genius

Your comprehensive JavaScript expert for IPA. Not just a code reviewer - a full-featured JavaScript assistant that analyzes, creates, optimizes, debugs, and teaches ES5-compliant JavaScript for IPA processes.

## What This Skill Does

This skill is your JavaScript genius that can:

1. **Analyze & Review** - Comprehensive code analysis for ES5 compliance, best practices, performance
2. **Create & Generate** - Write production-ready ES5 JavaScript from requirements
3. **Debug & Fix** - Troubleshoot runtime errors, identify root causes, provide fixes
4. **Optimize & Improve** - Enhance performance, refactor code, apply best practices
5. **Teach & Explain** - Answer JavaScript questions, explain concepts, provide examples
6. **Convert & Migrate** - Transform ES6+ code to ES5, modernize legacy code

## When to Use

**Code Review & Analysis:**

- Reviewing JavaScript before deployment
- Validating ES5 compliance
- Identifying performance issues
- Ensuring production readiness

**Code Creation:**

- Writing new IPA JavaScript from scratch
- Generating Assign node logic
- Creating data transformation functions
- Building validation routines

**Troubleshooting:**

- Debugging runtime errors
- Fixing "unexpected token" errors
- Resolving NULL/undefined issues
- Solving performance problems

**Learning & Questions:**

- Understanding ES5 constraints
- Learning IPA JavaScript patterns
- Getting code examples
- Best practices guidance

**Optimization:**

- Improving slow code
- Reducing complexity
- Enhancing readability
- Applying defensive patterns

## Critical ES5 Rules

**IPA JavaScript executes in ES5 environment. Modern syntax causes immediate runtime errors.**

### Forbidden ES6+ Features

| Feature | ES6+ (FORBIDDEN) | ES5 (REQUIRED) |
|---------|------------------|----------------|
| Variables | `let x = 1;` `const x = 1;` | `var x = 1;` |
| Functions | `() => {}` `async/await` | `function() {}` |
| Strings | `` `Hello ${name}` `` | `"Hello " + name` |
| Destructuring | `var {prop} = obj;` | `var prop = obj.prop;` |
| Default params | `function f(x = 1)` | Check inside function |
| Spread | `[...arr]` | `arr.slice()` |
| Classes | `class MyClass {}` | Constructor functions |
| Modules | `import/export` | Not supported |
| Promises | `new Promise()` | Not supported |
| Template literals | `` `text` `` | `"text"` |

### Allowed ES5 Features

- `var` declarations
- `function` keyword
- Traditional for loops
- `if/else`, `switch`, ternary operator
- Object literals: `{key: value}`
- Array literals: `[1, 2, 3]`
- String concatenation: `+`
- All ES5 built-in methods

## How to Use This Skill

### Quick Questions

Just ask! No code needed:

```text

User: How do I loop through an array in ES5?
User: What's the ES5 way to filter an array?
User: How do I handle NULL values safely?
User: Show me an IPA Assign node structure

```text

### Code Review (Paste in Chat)

For short code (< 100 lines), paste directly:

```text

User: Review this code:
var items = data.filter(x => x.status === "Active");
let count = items.length;

Skill: [Identifies ES6 violations and provides ES5 fix]

```text

### Code Review (File-Based)

For longer code, save to file:

```text

User: Analyze Temp/assign_node_code.js

Skill: [Reads file, performs comprehensive analysis]

```text

### Code Generation

Describe what you need:

```text

User: I need JavaScript to parse a CSV file, validate required fields, 
and calculate totals. It should handle empty lines and invalid numbers.

Skill: [Generates complete ES5-compliant code with error handling]

```text

### Troubleshooting

Share the error:

```text

User: My code is failing with "unexpected token" error on line 23

Skill: [Analyzes code, identifies ES6+ syntax, provides fix]

```text

### Learning & Examples

Ask for explanations:

```text

User: Explain the difference between var and let
User: Show me how to do pagination in IPA
User: What's the best way to handle floating point comparison?

Skill: [Provides detailed explanation with examples]

```text

## Activation Instructions

**CRITICAL**: When this skill is activated, the following steering files are automatically loaded:

1. **IPA Guide** (REQUIRED):

   ```text\ndiscloseContext(name="ipa-ipd-guide")

   ```

   Loads `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` with:

- IPA JavaScript ES5 compliance rules
- Assign node structure
- Start node global variables
- Activity types and patterns

1. **Process Patterns** (for code generation):

   ```text\ndiscloseContext(name="process-patterns")

   ```

   Loads `.kiro/steering/04_Process_Patterns_Library.md` with:
   - 450+ analyzed IPA workflows
   - Common JavaScript patterns
   - Data transformation examples
   - Validation routines

2. **FSM Business Classes** (for API integration):

   ```text\ndiscloseContext(name="fsm-business-classes")

   ```

   Loads `.kiro/steering/07_FSM_Business_Classes_and_API.md` when working with:
   - WebRun activities
   - Landmark API calls
   - FSM business class operations

3. **Data Fabric** (for Compass SQL integration):

   ```text\ndiscloseContext(name="data-fabric-guide")

   ```

   Loads `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md` when working with:
   - Compass API JavaScript
   - Data Lake queries
   - JSON parsing from API responses

**The skill will automatically load relevant steering files based on the task context.**

The skill performs comprehensive analysis across 6 dimensions:

1. **ES5 Compliance**

   - No `let`/`const` (use `var`)
   - No arrow functions (use `function`)
   - No template literals (use string concatenation)
   - No destructuring (explicit property access)
   - No default parameters (check inside function)
   - No spread operator (use `.slice()`, `.concat()`)
   - No ES6+ methods (`.map()`, `.filter()`, `.find()`)

2. **Best Practices**

   - Defensive NULL/undefined checks
   - Input validation
   - Type checking before operations
   - Proper error handling
   - Meaningful variable names
   - Comments for complex logic

3. **Performance**

   - Efficient loops (avoid nested loops where possible)
   - String concatenation optimization
   - Array operations efficiency
   - Avoid redundant calculations
   - Memory-efficient patterns

4. **Production Readiness**

   - Edge case handling (empty strings, zero, NULL)
   - Floating point comparison (rounding)
   - Division by zero checks
   - Array bounds checking
   - Safe type conversions

5. **Code Quality**

   - Readability (formatting, indentation)
   - Maintainability (modularity, reusability)
   - Naming conventions (descriptive names)
   - Comment quality
   - Code organization

6. **IPA-Specific Patterns**

   - Assign node structure (function wrapper)
   - Global variable usage
   - Configuration at top of function
   - No top-level return statements
   - Function invocation at end

### Step 3: Recommendations

For each issue found, provides:

- **Severity**: Critical / High / Medium / Low
- **Category**: ES5 Compliance / Best Practices / Performance / Production Readiness
- **Explanation**: Why this matters
- **Fix**: Specific code changes
- **Example**: Before/after comparison

### Step 4: Improved Code

Generates refactored code with:

- All ES6+ features converted to ES5
- Best practices applied
- Performance optimizations
- Production-ready error handling
- Comments explaining changes

## Analysis Categories

### ES5 Compliance Issues

**Critical:**

- `let` or `const` declarations
- Arrow functions `() => {}`
- Template literals `` `${var}` ``
- `async`/`await`
- Destructuring `{prop} = obj`
- Spread operator `...arr`
- ES6+ methods (`.map()`, `.filter()`, `.find()`)

**High:**

- Default parameters `function(x = 1)`
- `class` keyword
- `import`/`export` statements
- `Promise` usage
- `for...of` loops

**Medium:**

- Object shorthand `{prop}` instead of `{prop: prop}`
- Computed property names `{[key]: value}`
- Method shorthand `{method() {}}`

### Best Practices Issues

**Critical:**

- No NULL/undefined checks before operations
- No input validation
- Missing error handling
- Unsafe type conversions

**High:**

- No defensive programming patterns
- Missing edge case handling
- Unclear variable names
- No comments for complex logic

**Medium:**

- Inconsistent naming conventions
- Poor code organization
- Redundant code
- Magic numbers without explanation

### Performance Issues

**Critical:**

- Nested loops with high complexity
- **String concatenation in loops** (O(n²) complexity - use array accumulation)
- Redundant calculations inside loops

**High:**

- Unnecessary array iterations
- Inefficient search patterns
- Memory-intensive operations

**Medium:**

- Suboptimal algorithm choices
- Unnecessary variable declarations
- Redundant type checks

### Production Readiness Issues

**Critical:**

- No division by zero checks
- No floating point rounding before comparison
- Missing NULL guards on critical operations

**High:**

- No empty string/array checks
- Missing array bounds validation
- Unsafe parseInt/parseFloat usage

**Medium:**

- No default value handling
- Missing type validation
- Insufficient error messages

## Common Patterns Analyzed

### Pattern 1: Variable Declarations

**Bad (ES6):**

```javascript

let count = 0;
const MAX_ITEMS = 100;

```text

**Good (ES5):**

```javascript

var count = 0;
var MAX_ITEMS = 100;

```text

### Pattern 2: Arrow Functions

**Bad (ES6):**

```javascript

var result = items.map(item => item.value);

```text

**Good (ES5):**

```javascript

var result = [];
for (var i = 0; i < items.length; i++) {
    result.push(items[i].value);
}

```text

### Pattern 3: Template Literals

**Bad (ES6):**

```javascript

var message = `Hello ${name}, you have ${count} items`;

```text

**Good (ES5):**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

### Pattern 4: Destructuring

**Bad (ES6):**

```javascript

var {firstName, lastName} = person;

```text

**Good (ES5):**

```javascript

var firstName = person.firstName;
var lastName = person.lastName;

```text

### Pattern 5: Default Parameters

**Bad (ES6):**

```javascript

function calculate(amount, rate = 0.05) {
    return amount * rate;
}

```text

**Good (ES5):**

```javascript

function calculate(amount, rate) {
    if (typeof rate === "undefined") {
        rate = 0.05;
    }
    return amount * rate;
}

```text

### Pattern 6: Spread Operator

**Bad (ES6):**

```javascript

var combined = [...array1, ...array2];

```text

**Good (ES5):**

```javascript

var combined = array1.concat(array2);

```text

### Pattern 7: Defensive NULL Checks

**Bad:**

```javascript

var total = parseFloat(amount);
if (total === 0) {
    // May fail if amount is NULL/undefined
}

```text

**Good:**

```javascript

if (!amount || typeof amount !== "string") {
    amount = "0";
}
var total = parseFloat(amount);
if (isNaN(total)) {
    total = 0;
}
if (total === 0) {
    // Safe comparison
}

```text

### Pattern 8: Floating Point Comparison

**Bad:**

```javascript

if (sumQty === 0) {
    // Unreliable for floating point
}

```text

**Good:**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var roundedSum = roundToDecimals(sumQty, 2);
if (roundedSum === 0) {
    // Safe comparison
}

```text

### Pattern 9: Division by Zero

**Bad:**

```javascript

var unitCost = extendedAmount / originalQuantity;

```

### Pattern 10: String Concatenation in Loops (CRITICAL PERFORMANCE)

**Bad (O(n²) complexity):**

```javascript
// Inside pagination loop (100+ iterations)
OutputRecords += GetResultOut + "

";
```

**Why It's Bad:**
- Strings are immutable in JavaScript
- Each `+=` creates a NEW string and copies ALL previous content
- 100 iterations = ~5MB copied for 100KB of data
- Performance degrades exponentially with data size

**Good (O(n) complexity):**

```javascript
// BEFORE the pagination loop
var OutputRecordsArray = [];

// INSIDE the pagination loop
while (hasMoreData) {
    // ... fetch and transform data ...
    
    // Push to array instead of string concatenation
    for (var i = 0; i < transformedLines.length; i++) {
        OutputRecordsArray.push(transformedLines[i]);
    }
    
    // ... pagination logic ...
    offset += limit;
}

// AFTER the loop completes - join once
var OutputRecords = OutputRecordsArray.join("

");
```

**Performance Comparison:**

| Approach | Complexity | 100 Iterations | 1000 Iterations |
|----------|-----------|----------------|-----------------|
| String += | O(n²) | ~5MB copied | ~500MB copied |
| Array.push() + join() | O(n) | ~100KB copied | ~1MB copied |
| **Speedup** | **Linear** | **50x faster** | **500x faster** |

**When to Use:**
- Any loop with 10+ iterations
- Pagination loops processing large datasets
- File processing with line-by-line accumulation
- Data transformation with result aggregationtext

**Good:**

```javascript

if (originalQuantity === 0) {
    exceptions.push({error: "Division by zero"});
    continue;
}
var unitCost = extendedAmount / originalQuantity;

```text

### Pattern 11: IPA Assign Node Structure

**Bad:**

```javascript

// Top-level code
var result = processData(input);
return result;  // ERROR: No top-level return

```text

**Good:**

```javascript

function transformData(inputData, fileName) {
    // Configuration variables
    var CONFIG_VALUE = "setting";
    
    // Validation
    if (!inputData || typeof inputData !== "string") {
        inputData = "";
    }
    
    // Processing logic
    var result = [];
    // ... transformation ...
    
    return result;
}

// Function invocation at end
transformData(ImportFile, FileName);

```

## Real-World Performance Scenarios

### Scenario 1: Compass API Pagination (Production)

**Context**: MatchReport_Outbound.lpd processing 50,000 GL transactions

**Bad Implementation (O(n²) - 45 minutes execution)**:

```javascript
// Global variable
var OutputRecords = "";

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        GetResultArr[i] = GetResultArr[i].replace(/,/g, "|");
    }
    GetResultOut = GetResultArr.join("
");
    
    // ❌ BAD: String concatenation in loop
    OutputRecords += GetResultOut + "
";  // O(n²) complexity
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}
```

**Performance Impact**:
- Iteration 1: Copy 10KB
- Iteration 100: Copy 1MB (100 × 10KB)
- Iteration 500: Copy 5MB (500 × 10KB)
- Total: ~1.25GB copied for 5MB of data
- Execution time: 45 minutes

**Good Implementation (O(n) - 54 seconds execution)**:

```javascript
// Global variable (array accumulator)
var OutputRecordsArray = [];

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        var line = GetResultArr[i];
        if (line && line.trim() !== "") {
            // ✅ GOOD: Push to array
            OutputRecordsArray.push(line.replace(/,/g, "|"));
        }
    }
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}

// Join once after loop completes
var OutputRecords = OutputRecordsArray.join("
");
```

**Performance Improvement**:
- Total: ~5MB copied (linear growth)
- Execution time: 54 seconds
- **Speedup: 50x faster**
- Memory efficiency: 250x less copying

### Scenario 2: File Processing with Validation

**Context**: Invoice import processing 10,000 lines with validation

**Bad Implementation (Multiple Issues)**:

```javascript
var validRecords = "";
var errorRecords = "";

for (var i = 0; i < lines.length; i++) {
    var fields = lines[i].split(",");
    
    // ❌ Issue 1: No NULL check
    var amount = parseFloat(fields[2]);
    
    // ❌ Issue 2: Floating point comparison without rounding
    if (amount === 0) {
        errorRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    } else {
        validRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    }
}
```

**Good Implementation (All Best Practices)**:

```javascript
var validRecordsArray = [];
var errorRecordsArray = [];

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    
    // ✅ Skip empty lines
    if (!line || line.trim() === "") {
        continue;
    }
    
    var fields = line.split(",");
    
    // ✅ Validate field count
    if (fields.length < 3) {
        errorRecordsArray.push(line + "|Missing fields");
        continue;
    }
    
    // ✅ NULL check and safe parsing
    var amountStr = fields[2] ? fields[2].trim() : "0";
    var amount = parseFloat(amountStr);
    
    // ✅ Validate numeric
    if (isNaN(amount)) {
        errorRecordsArray.push(line + "|Invalid amount: " + amountStr);
        continue;
    }
    
    // ✅ Round before comparison
    var roundedAmount = roundToDecimals(amount, 2);
    
    if (roundedAmount === 0) {
        errorRecordsArray.push(line + "|Zero amount");
    } else {
        validRecordsArray.push(line);
    }
}

// ✅ Join once at end
var validRecords = validRecordsArray.join("
");
var errorRecords = errorRecordsArray.join("
");
```

**Improvements**:
- Array accumulation (50x faster for large datasets)
- NULL safety (prevents runtime errors)
- Floating point rounding (prevents comparison bugs)
- Input validation (catches data quality issues)
- Empty line handling (cleaner output)

### Scenario 3: Nested Loop Optimization

**Context**: Matching 1,000 invoices against 5,000 PO lines

**Bad Implementation (O(n²) - 5 million comparisons)**:

```javascript
var matchedInvoices = [];

// ❌ Nested loop without optimization
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < poLines.length; j++) {
        if (invoices[i].poNumber === poLines[j].poNumber &&
            invoices[i].lineNumber === poLines[j].lineNumber) {
            matchedInvoices.push({
                invoice: invoices[i],
                poLine: poLines[j]
            });
            break;  // At least breaks after match
        }
    }
}
```

**Good Implementation (O(n) - 6,000 operations)**:

```javascript
// ✅ Build lookup map (O(n))
var poLookup = {};
for (var i = 0; i < poLines.length; i++) {
    var key = poLines[i].poNumber + "|" + poLines[i].lineNumber;
    poLookup[key] = poLines[i];
}

// ✅ Single loop with map lookup (O(n))
var matchedInvoices = [];
for (var i = 0; i < invoices.length; i++) {
    var key = invoices[i].poNumber + "|" + invoices[i].lineNumber;
    var poLine = poLookup[key];
    
    if (poLine) {
        matchedInvoices.push({
            invoice: invoices[i],
            poLine: poLine
        });
    }
}
```

**Performance Improvement**:
- Bad: 5,000,000 comparisons (1,000 × 5,000)
- Good: 6,000 operations (5,000 + 1,000)
- **Speedup: 833x faster**

## Performance Optimization Checklist

### Memory Optimization

**1. Array Accumulation vs String Concatenation**

```javascript
// ❌ BAD: O(n²) memory copying
var result = "";
for (var i = 0; i < 1000; i++) {
    result += data[i] + "
";  // Creates 1000 new strings
}

// ✅ GOOD: O(n) memory usage
var resultArray = [];
for (var i = 0; i < 1000; i++) {
    resultArray.push(data[i]);  // Reuses array memory
}
var result = resultArray.join("
");  // Single allocation
```

**2. Reuse Variables Instead of Creating New Ones**

```javascript
// ❌ BAD: Creates 1000 new variables
for (var i = 0; i < 1000; i++) {
    var temp = data[i].toUpperCase();
    var trimmed = temp.trim();
    var replaced = trimmed.replace(/,/g, "|");
    results.push(replaced);
}

// ✅ GOOD: Reuses single variable
var temp;
for (var i = 0; i < 1000; i++) {
    temp = data[i].toUpperCase().trim().replace(/,/g, "|");
    results.push(temp);
}
```

**3. Avoid Unnecessary Array Copies**

```javascript
// ❌ BAD: Creates new array on each iteration
for (var i = 0; i < items.length; i++) {
    var subset = items.slice(0, i);  // O(n²) total
    process(subset);
}

// ✅ GOOD: Process in place
for (var i = 0; i < items.length; i++) {
    process(items, i);  // Pass index instead
}
```

### Speed Optimization

**1. Hoist Invariant Calculations Outside Loops**

```javascript
// ❌ BAD: Calculates same value 1000 times
for (var i = 0; i < 1000; i++) {
    var multiplier = Math.pow(10, 2);  // Recalculated each iteration
    results.push(data[i] * multiplier);
}

// ✅ GOOD: Calculate once
var multiplier = Math.pow(10, 2);
for (var i = 0; i < 1000; i++) {
    results.push(data[i] * multiplier);
}
```

**2. Cache Array Length**

```javascript
// ❌ BAD: Accesses .length property 1000 times
for (var i = 0; i < items.length; i++) {
    process(items[i]);
}

// ✅ GOOD: Cache length (minor optimization, but good practice)
var len = items.length;
for (var i = 0; i < len; i++) {
    process(items[i]);
}
```

**3. Use Lookup Maps for Repeated Searches**

```javascript
// ❌ BAD: O(n²) - searches array repeatedly
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < vendors.length; j++) {
        if (invoices[i].vendorId === vendors[j].id) {
            invoices[i].vendorName = vendors[j].name;
            break;
        }
    }
}

// ✅ GOOD: O(n) - build map once, lookup is O(1)
var vendorMap = {};
for (var i = 0; i < vendors.length; i++) {
    vendorMap[vendors[i].id] = vendors[i].name;
}
for (var i = 0; i < invoices.length; i++) {
    invoices[i].vendorName = vendorMap[invoices[i].vendorId] || "";
}
```

**4. Compile Regex Outside Loops**

```javascript
// ❌ BAD: Compiles regex 1000 times
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(/[^0-9]/g, "");  // Regex compiled each time
    results.push(cleaned);
}

// ✅ GOOD: Compile once (ES5 doesn't have explicit compilation, but pattern is cached)
var digitPattern = /[^0-9]/g;
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(digitPattern, "");
    results.push(cleaned);
}
```

### Space Optimization

**1. Clear Large Variables After Use**

```javascript
// Process large dataset
var largeData = fetchLargeDataset();  // 10MB
var processed = processData(largeData);

// ✅ Clear reference to allow garbage collection
largeData = null;

// Continue with processed data
return processed;
```

**2. Process Data in Chunks**

```javascript
// ❌ BAD: Load entire file into memory
var allLines = fileContent.split("
");  // 100MB in memory
var results = [];
for (var i = 0; i < allLines.length; i++) {
    results.push(processLine(allLines[i]));
}

// ✅ GOOD: Process in chunks (if possible)
var CHUNK_SIZE = 1000;
var results = [];
var lines = fileContent.split("
");

for (var i = 0; i < lines.length; i += CHUNK_SIZE) {
    var chunk = lines.slice(i, i + CHUNK_SIZE);
    for (var j = 0; j < chunk.length; j++) {
        results.push(processLine(chunk[j]));
    }
    chunk = null;  // Clear chunk
}
```

## Performance Measurement Tips

### Timing Code Execution

```javascript
// Start timer
var startTime = new Date().getTime();

// Your code here
for (var i = 0; i < 10000; i++) {
    // ... processing ...
}

// End timer
var endTime = new Date().getTime();
var elapsedMs = endTime - startTime;

// Log result
console.log("Execution time: " + elapsedMs + "ms");
```

### Memory Usage Estimation

```javascript
// Estimate string memory usage
function estimateStringMemory(str) {
    // Each character is ~2 bytes in JavaScript
    return str.length * 2;
}

// Estimate array memory usage
function estimateArrayMemory(arr) {
    var total = 0;
    for (var i = 0; i < arr.length; i++) {
        if (typeof arr[i] === "string") {
            total += arr[i].length * 2;
        }
    }
    return total;
}

// Example usage
var data = "Large string data...";
var memoryBytes = estimateStringMemory(data);
var memoryMB = memoryBytes / (1024 * 1024);
console.log("Estimated memory: " + memoryMB.toFixed(2) + " MB");
```text

## Output Format

### Analysis Summary

```text

📊 IPA JAVASCRIPT ES5 ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code: [First 50 chars...]
Lines: 85
Complexity: Medium
Node Type: Assign

OVERALL ASSESSMENT: ⚠️ NEEDS IMPROVEMENT

Critical Issues: 3 (ES5 compliance violations)
High Priority: 5 (Missing NULL checks)
Medium Priority: 8 (Performance optimizations)
Low Priority: 2 (Code quality)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Issue Details

```text

🔴 CRITICAL: Arrow Function Usage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Category: ES5 Compliance
Impact: Runtime error in IPA (arrow functions not supported)
Line: 23

Issue:
Arrow function syntax is ES6+ and will cause immediate runtime error
in IPA's ES5 JavaScript environment.

Current Code:
var filtered = items.filter(item => item.status === "Active");

Recommended Fix:
var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

Explanation:
IPA JavaScript executes in ES5 environment. Use traditional for loops
and function keyword instead of arrow functions and array methods like
.filter(), .map(), .find().

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Improved Code

```text

✅ IMPROVED CODE (ES5 COMPLIANT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied:

1. Converted all let/const to var
2. Replaced arrow functions with function keyword
3. Replaced template literals with string concatenation
4. Added NULL/undefined checks
5. Added floating point rounding
6. Added division by zero checks

7. Improved error handling
8. Added descriptive comments

// IPA Assign Node: Transform Import Data
// Purpose: Parse and validate import file content
// Input: ImportFile (string), FileName (string)
// Output: Processed records array

function transformImportData(importFileContent, fileName) {
    // Configuration
    var ROUND_DECIMALS = 2;
    var REQUIRED_FIELDS = ["id", "amount", "quantity"];
    
    // Input validation
    if (!importFileContent || typeof importFileContent !== "string") {
        importFileContent = "";
    }
    
    if (!fileName || typeof fileName !== "string") {
        fileName = "unknown";
    }
    
    // Initialize result arrays
    var processedRecords = [];
    var exceptions = [];
    
    // Parse input (assuming CSV format)
    var lines = importFileContent.split("\n");
    
    // Process each line
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        
        // Skip empty lines
        if (!line || line.trim() === "") {
            continue;
        }
        
        var fields = line.split(",");
        
        // Validate required fields
        if (fields.length < REQUIRED_FIELDS.length) {
            exceptions.push({
                line: i + 1,
                error: "Missing required fields"
            });
            continue;
        }
        
        // Extract and validate fields
        var id = fields[0] ? fields[0].trim() : "";
        var amountStr = fields[1] ? fields[1].trim() : "0";
        var quantityStr = fields[2] ? fields[2].trim() : "0";
        
        // Parse numeric values with validation
        var amount = parseFloat(amountStr);
        if (isNaN(amount)) {
            exceptions.push({
                line: i + 1,
                field: "amount",
                error: "Invalid numeric value: " + amountStr
            });
            continue;
        }
        
        var quantity = parseFloat(quantityStr);
        if (isNaN(quantity)) {
            exceptions.push({
                line: i + 1,
                field: "quantity",
                error: "Invalid numeric value: " + quantityStr
            });
            continue;
        }
        
        // Division by zero check
        var unitPrice = 0;
        if (quantity === 0) {
            exceptions.push({
                line: i + 1,
                error: "Quantity is zero, cannot calculate unit price"
            });
            continue;
        } else {
            unitPrice = amount / quantity;
        }
        
        // Round for safe comparison
        var roundedAmount = roundToDecimals(amount, ROUND_DECIMALS);
        
        // Build result record
        var record = {
            id: id,
            amount: roundedAmount,
            quantity: quantity,
            unitPrice: roundToDecimals(unitPrice, ROUND_DECIMALS),
            fileName: fileName,
            lineNumber: i + 1
        };
        
        processedRecords.push(record);
    }
    
    // Helper function: Round to specified decimals
    function roundToDecimals(num, decimals) {
        var multiplier = Math.pow(10, decimals);
        return Math.round(num * multiplier) / multiplier;
    }
    
    // Return results
    return {
        records: processedRecords,
        exceptions: exceptions,
        totalProcessed: processedRecords.length,
        totalErrors: exceptions.length
    };
}

// Invoke function with IPA variables
transformImportData(ImportFile, FileName);

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

## Integration with IPA

### IPA Assign Node Structure

```javascript

// Entire script wrapped in function
function processData(inputData, configValue) {
    // Configuration variables INSIDE function
    var MAX_RECORDS = 1000;
    var DELIMITER = ",";
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing logic
    var results = [];
    // ... transformation ...
    
    return results;
}

// Function invocation at end (NO top-level return)
processData(InputVariable, ConfigVariable);

```text

### Global Variables (Start Node)

**CRITICAL**: Start node global variables are defined in the **Properties** tab, NOT as JavaScript code.

```text

Start Node Properties (NOT JavaScript):
queryID = ""
auth = ""
rowCount = 0
accessTokenResp = ""
OutputRecords = ""
offset = 0
limit = 1000

```text

These become global variables accessible throughout the process. No `var` keyword needed in Properties tab.

### Common IPA Patterns

**Pattern: Accumulator Loop**

```javascript

var allRecords = [];
var hasMoreData = true;
var offset = 0;
var limit = 1000;

while (hasMoreData) {
    // Fetch page of data
    var pageData = fetchData(offset, limit);
    
    // Append to accumulator
    allRecords = allRecords.concat(pageData);
    
    // Check if more data exists
    hasMoreData = (pageData.length === limit);
    offset += limit;
}

```text

**Pattern: Error Collection**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    try {
        processRecord(records[i]);
    } catch (e) {
        exceptions.push({
            record: i,
            error: e.message || "Unknown error"
        });
    }
}

```text

## Advanced Features

### Code Complexity Scoring

- **Simple**: Single loop, basic operations, < 50 lines
- **Medium**: Multiple loops, conditionals, 50-150 lines
- **Complex**: Nested loops, complex logic, 150-300 lines
- **Very Complex**: Deep nesting, multiple functions, > 300 lines

### Performance Estimation

- **Fast**: O(n) complexity, simple operations
- **Moderate**: O(n²) complexity, string operations
- **Slow**: O(n³) complexity, nested loops
- **Very Slow**: Exponential complexity, inefficient algorithms

### Production Readiness Score

Based on:

- NULL/undefined handling (30%)
- Error handling (25%)
- Edge case coverage (20%)
- Type validation (15%)
- Code quality (10%)

## Usage Examples

### Example 1: Quick Question

```text

User: How do I convert an array to uppercase in ES5?

Skill: In ES5, you need to use a for loop instead of .map():

var items = ["apple", "banana", "cherry"];
var uppercased = [];
for (var i = 0; i < items.length; i++) {
    uppercased.push(items[i].toUpperCase());
}
// Result: ["APPLE", "BANANA", "CHERRY"]

```text

### Example 2: Code Review (Pasted)

```text

User: Review this:
let items = data.filter(x => x.status === "Active");

Skill: [Identifies ES6 violations: let, arrow function, .filter()]
[Provides ES5-compliant alternative with for loop]

```text

### Example 3: Code Generation

```text

User: I need JavaScript to:

1. Parse CSV input
2. Validate required fields (id, amount, quantity)
3. Calculate unit price (amount / quantity)
4. Handle division by zero
5. Collect errors

Skill: [Generates complete ES5-compliant code with:

- Input validation
- CSV parsing
- Field validation
- Safe division
- Error collection
- Proper IPA Assign node structure]

```text

### Example 4: Troubleshooting

```text

User: This code fails with "unexpected token" on line 15:
const MAX_ITEMS = 100;

Skill: The error is caused by ES6 'const' keyword. IPA uses ES5 environment.

Fix:
var MAX_ITEMS = 100;

ES5 doesn't support 'const' or 'let'. Always use 'var' for all variable declarations.

```text

### Example 5: Optimization

```text

User: This code is slow, can you optimize it?
[Shows nested loop code]

Skill: [Analyzes O(n²) complexity]
[Provides O(n) solution using lookup map]
[Explains performance improvement]

```text

### Example 6: Learning

```text

User: Explain IPA Assign node structure

Skill: [Provides detailed explanation with example]
[Shows function wrapper pattern]
[Explains configuration placement]
[Demonstrates function invocation]

```text

## Code Generation Capabilities

### Data Transformation

**Request:**

```text

Transform JSON array to CSV format with specific columns

```text

**Generates:**

- Input validation
- JSON parsing
- Field extraction
- CSV formatting
- Error handling
- ES5-compliant code

### Validation Routines

**Request:**

```text

Validate order data: required fields, numeric amounts, date formats

```text

**Generates:**

- Field presence checks
- Type validation
- Format validation
- Error collection
- Descriptive error messages

### API Response Processing

**Request:**

```text

Parse Compass API response, extract records, handle pagination

```text

**Generates:**

- JSON parsing
- NULL safety
- Array handling
- Pagination logic
- Error handling

### File Processing

**Request:**

```text

Read CSV file, parse lines, validate data, transform to JSON

```text

**Generates:**

- File content validation
- Line-by-line parsing
- Field extraction
- Data transformation
- Error collection

### Calculation Logic

**Request:**

```text

Calculate totals, subtotals, tax, with rounding and validation

```text

**Generates:**

- Safe numeric parsing
- Floating point rounding
- Division by zero checks
- Accumulation logic
- Result formatting

### Error Handling Patterns

**Request:**

```text

Collect errors during processing, categorize by severity

```text

**Generates:**

- Try-catch blocks
- Error collection array
- Error categorization
- Descriptive messages
- Error summary

## Tips for Best Results

1. **Be Specific**: Describe requirements clearly
2. **Provide Context**: Mention node type, data source, expected output
3. **Share Errors**: Include full error messages
4. **Show Examples**: Provide sample input/output data
5. **Ask Questions**: No question is too basic
6. **Request Explanations**: Ask "why" for better understanding

## Quick Reference - Common Questions

### Variables & Declarations

**Q: How do I declare variables in ES5?**

```javascript

var name = "John";
var count = 0;
var isActive = true;

```text

**Q: Can I use let or const?**
No. IPA uses ES5 environment. Always use `var`.

### Arrays

**Q: How do I loop through an array?**

```javascript

for (var i = 0; i < items.length; i++) {
    var item = items[i];
    // Process item
}

```text

**Q: How do I filter an array?**

```javascript

var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

```text

**Q: How do I map an array?**

```javascript

var mapped = [];
for (var i = 0; i < items.length; i++) {
    mapped.push(items[i].value * 2);
}

```text

### Strings

**Q: How do I concatenate strings?**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

**Q: Can I use template literals?**
No. Use string concatenation with `+` operator.

**Q: How do I check if string contains substring?**

```javascript

if (str.indexOf("substring") !== -1) {
    // Found
}

```text

### Functions

**Q: How do I write a function?**

```javascript

function calculateTotal(items) {
    var total = 0;
    for (var i = 0; i < items.length; i++) {
        total += items[i].amount;
    }
    return total;
}

```text

**Q: Can I use arrow functions?**
No. Always use `function` keyword.

### NULL Safety

**Q: How do I check for NULL/undefined?**

```javascript

if (!value || typeof value !== "string") {
    value = "";  // Default
}

```text

**Q: How do I safely access object properties?**

```javascript

var name = "";
if (person && typeof person === "object") {
    name = person.firstName || "";
}

```text

### Numbers

**Q: How do I parse numbers safely?**

```javascript

var num = parseFloat(input);
if (isNaN(num)) {
    num = 0;  // Default
}

```text

**Q: How do I compare floating point numbers?**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var rounded = roundToDecimals(0.1 + 0.2, 2);
if (rounded === 0.3) {
    // Safe comparison
}

```text

**Q: How do I check for division by zero?**

```javascript

if (denominator === 0) {
    // Handle error
    return;
}
var result = numerator / denominator;

```text

### IPA-Specific

**Q: What's the IPA Assign node structure?**

```javascript

function processData(inputData) {
    // Configuration
    var MAX_RECORDS = 1000;
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing
    var results = [];
    // ... logic ...
    
    return results;
}

// Invoke function
processData(InputVariable);

```text

**Q: How do I define global variables?**
Define them in Start node Properties tab (NOT JavaScript):

```text

queryID = ""
rowCount = 0
offset = 0

```text

**Q: How do I collect errors?**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    if (!records[i].id) {
        exceptions.push({
            record: i,
            error: "Missing ID"
        });
        continue;
    }
}

```text

### Debugging

**Q: "unexpected token" error - what does it mean?**
Usually ES6+ syntax in ES5 environment. Check for:

- `let`/`const` (use `var`)
- Arrow functions `=>` (use `function`)
- Template literals `` `${}` `` (use `+`)

**Q: "Cannot read property of undefined" - how to fix?**
Add NULL checks:

```javascript

if (obj && obj.property) {
    // Safe to access
}

```text

**Q: Code works in browser but fails in IPA - why?**
Browser supports ES6+, IPA uses ES5. Convert modern syntax to ES5.

## Limitations

This skill analyzes JavaScript syntax and patterns but cannot:

- Execute code in IPA environment
- Access IPA global variables
- Test against live data
- Validate IPA-specific functions
- Measure actual execution time

For live validation, test in IPA Designer.

## Version History

- **1.2.0** (2026-03-09): Added real-world performance scenarios and optimization best practices
  - Real-world Scenario 1: Compass API pagination (50x speedup)
  - Real-world Scenario 2: File processing with validation
  - Real-world Scenario 3: Nested loop optimization (833x speedup)
  - Performance optimization checklist (memory, speed, space)
  - Performance measurement tips
- **1.1.0** (2026-03-09): Added string concatenation performance pattern
  - New Pattern 10: String Concatenation in Loops (O(n²) vs O(n) complexity)
  - Performance comparison table (50-500x speedup for large datasets)
  - Pagination loop optimization guidance
  - Array accumulation pattern for data aggregation
- **1.0.0** (2026-03-09): Initial release with comprehensive ES5 analysis
.Value -replace '```', '```text' 
   Loads `.kiro/steering/07_FSM_Business_Classes_and_API.md` when working with:
   - WebRun activities
   - Landmark API calls
   - FSM business class operations

4. **Data Fabric** (for Compass SQL integration):

   ```text\n ---
name: "ipa-javascript-es5-analyzer"
description: "Your JavaScript genius for IPA. Analyzes, reviews, optimizes, debugs, and writes ES5-compliant JavaScript. Handles code review, creation, troubleshooting, and best practices. Use for any JavaScript-related task in IPA."
---

# IPA JavaScript ES5 Genius

Your comprehensive JavaScript expert for IPA. Not just a code reviewer - a full-featured JavaScript assistant that analyzes, creates, optimizes, debugs, and teaches ES5-compliant JavaScript for IPA processes.

## What This Skill Does

This skill is your JavaScript genius that can:

1. **Analyze & Review** - Comprehensive code analysis for ES5 compliance, best practices, performance
2. **Create & Generate** - Write production-ready ES5 JavaScript from requirements
3. **Debug & Fix** - Troubleshoot runtime errors, identify root causes, provide fixes
4. **Optimize & Improve** - Enhance performance, refactor code, apply best practices
5. **Teach & Explain** - Answer JavaScript questions, explain concepts, provide examples
6. **Convert & Migrate** - Transform ES6+ code to ES5, modernize legacy code

## When to Use

**Code Review & Analysis:**

- Reviewing JavaScript before deployment
- Validating ES5 compliance
- Identifying performance issues
- Ensuring production readiness

**Code Creation:**

- Writing new IPA JavaScript from scratch
- Generating Assign node logic
- Creating data transformation functions
- Building validation routines

**Troubleshooting:**

- Debugging runtime errors
- Fixing "unexpected token" errors
- Resolving NULL/undefined issues
- Solving performance problems

**Learning & Questions:**

- Understanding ES5 constraints
- Learning IPA JavaScript patterns
- Getting code examples
- Best practices guidance

**Optimization:**

- Improving slow code
- Reducing complexity
- Enhancing readability
- Applying defensive patterns

## Critical ES5 Rules

**IPA JavaScript executes in ES5 environment. Modern syntax causes immediate runtime errors.**

### Forbidden ES6+ Features

| Feature | ES6+ (FORBIDDEN) | ES5 (REQUIRED) |
|---------|------------------|----------------|
| Variables | `let x = 1;` `const x = 1;` | `var x = 1;` |
| Functions | `() => {}` `async/await` | `function() {}` |
| Strings | `` `Hello ${name}` `` | `"Hello " + name` |
| Destructuring | `var {prop} = obj;` | `var prop = obj.prop;` |
| Default params | `function f(x = 1)` | Check inside function |
| Spread | `[...arr]` | `arr.slice()` |
| Classes | `class MyClass {}` | Constructor functions |
| Modules | `import/export` | Not supported |
| Promises | `new Promise()` | Not supported |
| Template literals | `` `text` `` | `"text"` |

### Allowed ES5 Features

- `var` declarations
- `function` keyword
- Traditional for loops
- `if/else`, `switch`, ternary operator
- Object literals: `{key: value}`
- Array literals: `[1, 2, 3]`
- String concatenation: `+`
- All ES5 built-in methods

## How to Use This Skill

### Quick Questions

Just ask! No code needed:

```text

User: How do I loop through an array in ES5?
User: What's the ES5 way to filter an array?
User: How do I handle NULL values safely?
User: Show me an IPA Assign node structure

```text

### Code Review (Paste in Chat)

For short code (< 100 lines), paste directly:

```text

User: Review this code:
var items = data.filter(x => x.status === "Active");
let count = items.length;

Skill: [Identifies ES6 violations and provides ES5 fix]

```text

### Code Review (File-Based)

For longer code, save to file:

```text

User: Analyze Temp/assign_node_code.js

Skill: [Reads file, performs comprehensive analysis]

```text

### Code Generation

Describe what you need:

```text

User: I need JavaScript to parse a CSV file, validate required fields, 
and calculate totals. It should handle empty lines and invalid numbers.

Skill: [Generates complete ES5-compliant code with error handling]

```text

### Troubleshooting

Share the error:

```text

User: My code is failing with "unexpected token" error on line 23

Skill: [Analyzes code, identifies ES6+ syntax, provides fix]

```text

### Learning & Examples

Ask for explanations:

```text

User: Explain the difference between var and let
User: Show me how to do pagination in IPA
User: What's the best way to handle floating point comparison?

Skill: [Provides detailed explanation with examples]

```text

## Activation Instructions

**CRITICAL**: When this skill is activated, the following steering files are automatically loaded:

1. **IPA Guide** (REQUIRED):

   ```text\ndiscloseContext(name="ipa-ipd-guide")

   ```

   Loads `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` with:

- IPA JavaScript ES5 compliance rules
- Assign node structure
- Start node global variables
- Activity types and patterns

1. **Process Patterns** (for code generation):

   ```text\ndiscloseContext(name="process-patterns")

   ```

   Loads `.kiro/steering/04_Process_Patterns_Library.md` with:
   - 450+ analyzed IPA workflows
   - Common JavaScript patterns
   - Data transformation examples
   - Validation routines

2. **FSM Business Classes** (for API integration):

   ```text\ndiscloseContext(name="fsm-business-classes")

   ```

   Loads `.kiro/steering/07_FSM_Business_Classes_and_API.md` when working with:
   - WebRun activities
   - Landmark API calls
   - FSM business class operations

3. **Data Fabric** (for Compass SQL integration):

   ```text\ndiscloseContext(name="data-fabric-guide")

   ```

   Loads `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md` when working with:
   - Compass API JavaScript
   - Data Lake queries
   - JSON parsing from API responses

**The skill will automatically load relevant steering files based on the task context.**

The skill performs comprehensive analysis across 6 dimensions:

1. **ES5 Compliance**

   - No `let`/`const` (use `var`)
   - No arrow functions (use `function`)
   - No template literals (use string concatenation)
   - No destructuring (explicit property access)
   - No default parameters (check inside function)
   - No spread operator (use `.slice()`, `.concat()`)
   - No ES6+ methods (`.map()`, `.filter()`, `.find()`)

2. **Best Practices**

   - Defensive NULL/undefined checks
   - Input validation
   - Type checking before operations
   - Proper error handling
   - Meaningful variable names
   - Comments for complex logic

3. **Performance**

   - Efficient loops (avoid nested loops where possible)
   - String concatenation optimization
   - Array operations efficiency
   - Avoid redundant calculations
   - Memory-efficient patterns

4. **Production Readiness**

   - Edge case handling (empty strings, zero, NULL)
   - Floating point comparison (rounding)
   - Division by zero checks
   - Array bounds checking
   - Safe type conversions

5. **Code Quality**

   - Readability (formatting, indentation)
   - Maintainability (modularity, reusability)
   - Naming conventions (descriptive names)
   - Comment quality
   - Code organization

6. **IPA-Specific Patterns**

   - Assign node structure (function wrapper)
   - Global variable usage
   - Configuration at top of function
   - No top-level return statements
   - Function invocation at end

### Step 3: Recommendations

For each issue found, provides:

- **Severity**: Critical / High / Medium / Low
- **Category**: ES5 Compliance / Best Practices / Performance / Production Readiness
- **Explanation**: Why this matters
- **Fix**: Specific code changes
- **Example**: Before/after comparison

### Step 4: Improved Code

Generates refactored code with:

- All ES6+ features converted to ES5
- Best practices applied
- Performance optimizations
- Production-ready error handling
- Comments explaining changes

## Analysis Categories

### ES5 Compliance Issues

**Critical:**

- `let` or `const` declarations
- Arrow functions `() => {}`
- Template literals `` `${var}` ``
- `async`/`await`
- Destructuring `{prop} = obj`
- Spread operator `...arr`
- ES6+ methods (`.map()`, `.filter()`, `.find()`)

**High:**

- Default parameters `function(x = 1)`
- `class` keyword
- `import`/`export` statements
- `Promise` usage
- `for...of` loops

**Medium:**

- Object shorthand `{prop}` instead of `{prop: prop}`
- Computed property names `{[key]: value}`
- Method shorthand `{method() {}}`

### Best Practices Issues

**Critical:**

- No NULL/undefined checks before operations
- No input validation
- Missing error handling
- Unsafe type conversions

**High:**

- No defensive programming patterns
- Missing edge case handling
- Unclear variable names
- No comments for complex logic

**Medium:**

- Inconsistent naming conventions
- Poor code organization
- Redundant code
- Magic numbers without explanation

### Performance Issues

**Critical:**

- Nested loops with high complexity
- **String concatenation in loops** (O(n²) complexity - use array accumulation)
- Redundant calculations inside loops

**High:**

- Unnecessary array iterations
- Inefficient search patterns
- Memory-intensive operations

**Medium:**

- Suboptimal algorithm choices
- Unnecessary variable declarations
- Redundant type checks

### Production Readiness Issues

**Critical:**

- No division by zero checks
- No floating point rounding before comparison
- Missing NULL guards on critical operations

**High:**

- No empty string/array checks
- Missing array bounds validation
- Unsafe parseInt/parseFloat usage

**Medium:**

- No default value handling
- Missing type validation
- Insufficient error messages

## Common Patterns Analyzed

### Pattern 1: Variable Declarations

**Bad (ES6):**

```javascript

let count = 0;
const MAX_ITEMS = 100;

```text

**Good (ES5):**

```javascript

var count = 0;
var MAX_ITEMS = 100;

```text

### Pattern 2: Arrow Functions

**Bad (ES6):**

```javascript

var result = items.map(item => item.value);

```text

**Good (ES5):**

```javascript

var result = [];
for (var i = 0; i < items.length; i++) {
    result.push(items[i].value);
}

```text

### Pattern 3: Template Literals

**Bad (ES6):**

```javascript

var message = `Hello ${name}, you have ${count} items`;

```text

**Good (ES5):**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

### Pattern 4: Destructuring

**Bad (ES6):**

```javascript

var {firstName, lastName} = person;

```text

**Good (ES5):**

```javascript

var firstName = person.firstName;
var lastName = person.lastName;

```text

### Pattern 5: Default Parameters

**Bad (ES6):**

```javascript

function calculate(amount, rate = 0.05) {
    return amount * rate;
}

```text

**Good (ES5):**

```javascript

function calculate(amount, rate) {
    if (typeof rate === "undefined") {
        rate = 0.05;
    }
    return amount * rate;
}

```text

### Pattern 6: Spread Operator

**Bad (ES6):**

```javascript

var combined = [...array1, ...array2];

```text

**Good (ES5):**

```javascript

var combined = array1.concat(array2);

```text

### Pattern 7: Defensive NULL Checks

**Bad:**

```javascript

var total = parseFloat(amount);
if (total === 0) {
    // May fail if amount is NULL/undefined
}

```text

**Good:**

```javascript

if (!amount || typeof amount !== "string") {
    amount = "0";
}
var total = parseFloat(amount);
if (isNaN(total)) {
    total = 0;
}
if (total === 0) {
    // Safe comparison
}

```text

### Pattern 8: Floating Point Comparison

**Bad:**

```javascript

if (sumQty === 0) {
    // Unreliable for floating point
}

```text

**Good:**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var roundedSum = roundToDecimals(sumQty, 2);
if (roundedSum === 0) {
    // Safe comparison
}

```text

### Pattern 9: Division by Zero

**Bad:**

```javascript

var unitCost = extendedAmount / originalQuantity;

```

### Pattern 10: String Concatenation in Loops (CRITICAL PERFORMANCE)

**Bad (O(n²) complexity):**

```javascript
// Inside pagination loop (100+ iterations)
OutputRecords += GetResultOut + "

";
```

**Why It's Bad:**
- Strings are immutable in JavaScript
- Each `+=` creates a NEW string and copies ALL previous content
- 100 iterations = ~5MB copied for 100KB of data
- Performance degrades exponentially with data size

**Good (O(n) complexity):**

```javascript
// BEFORE the pagination loop
var OutputRecordsArray = [];

// INSIDE the pagination loop
while (hasMoreData) {
    // ... fetch and transform data ...
    
    // Push to array instead of string concatenation
    for (var i = 0; i < transformedLines.length; i++) {
        OutputRecordsArray.push(transformedLines[i]);
    }
    
    // ... pagination logic ...
    offset += limit;
}

// AFTER the loop completes - join once
var OutputRecords = OutputRecordsArray.join("

");
```

**Performance Comparison:**

| Approach | Complexity | 100 Iterations | 1000 Iterations |
|----------|-----------|----------------|-----------------|
| String += | O(n²) | ~5MB copied | ~500MB copied |
| Array.push() + join() | O(n) | ~100KB copied | ~1MB copied |
| **Speedup** | **Linear** | **50x faster** | **500x faster** |

**When to Use:**
- Any loop with 10+ iterations
- Pagination loops processing large datasets
- File processing with line-by-line accumulation
- Data transformation with result aggregationtext

**Good:**

```javascript

if (originalQuantity === 0) {
    exceptions.push({error: "Division by zero"});
    continue;
}
var unitCost = extendedAmount / originalQuantity;

```text

### Pattern 11: IPA Assign Node Structure

**Bad:**

```javascript

// Top-level code
var result = processData(input);
return result;  // ERROR: No top-level return

```text

**Good:**

```javascript

function transformData(inputData, fileName) {
    // Configuration variables
    var CONFIG_VALUE = "setting";
    
    // Validation
    if (!inputData || typeof inputData !== "string") {
        inputData = "";
    }
    
    // Processing logic
    var result = [];
    // ... transformation ...
    
    return result;
}

// Function invocation at end
transformData(ImportFile, FileName);

```

## Real-World Performance Scenarios

### Scenario 1: Compass API Pagination (Production)

**Context**: MatchReport_Outbound.lpd processing 50,000 GL transactions

**Bad Implementation (O(n²) - 45 minutes execution)**:

```javascript
// Global variable
var OutputRecords = "";

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        GetResultArr[i] = GetResultArr[i].replace(/,/g, "|");
    }
    GetResultOut = GetResultArr.join("
");
    
    // ❌ BAD: String concatenation in loop
    OutputRecords += GetResultOut + "
";  // O(n²) complexity
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}
```

**Performance Impact**:
- Iteration 1: Copy 10KB
- Iteration 100: Copy 1MB (100 × 10KB)
- Iteration 500: Copy 5MB (500 × 10KB)
- Total: ~1.25GB copied for 5MB of data
- Execution time: 45 minutes

**Good Implementation (O(n) - 54 seconds execution)**:

```javascript
// Global variable (array accumulator)
var OutputRecordsArray = [];

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        var line = GetResultArr[i];
        if (line && line.trim() !== "") {
            // ✅ GOOD: Push to array
            OutputRecordsArray.push(line.replace(/,/g, "|"));
        }
    }
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}

// Join once after loop completes
var OutputRecords = OutputRecordsArray.join("
");
```

**Performance Improvement**:
- Total: ~5MB copied (linear growth)
- Execution time: 54 seconds
- **Speedup: 50x faster**
- Memory efficiency: 250x less copying

### Scenario 2: File Processing with Validation

**Context**: Invoice import processing 10,000 lines with validation

**Bad Implementation (Multiple Issues)**:

```javascript
var validRecords = "";
var errorRecords = "";

for (var i = 0; i < lines.length; i++) {
    var fields = lines[i].split(",");
    
    // ❌ Issue 1: No NULL check
    var amount = parseFloat(fields[2]);
    
    // ❌ Issue 2: Floating point comparison without rounding
    if (amount === 0) {
        errorRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    } else {
        validRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    }
}
```

**Good Implementation (All Best Practices)**:

```javascript
var validRecordsArray = [];
var errorRecordsArray = [];

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    
    // ✅ Skip empty lines
    if (!line || line.trim() === "") {
        continue;
    }
    
    var fields = line.split(",");
    
    // ✅ Validate field count
    if (fields.length < 3) {
        errorRecordsArray.push(line + "|Missing fields");
        continue;
    }
    
    // ✅ NULL check and safe parsing
    var amountStr = fields[2] ? fields[2].trim() : "0";
    var amount = parseFloat(amountStr);
    
    // ✅ Validate numeric
    if (isNaN(amount)) {
        errorRecordsArray.push(line + "|Invalid amount: " + amountStr);
        continue;
    }
    
    // ✅ Round before comparison
    var roundedAmount = roundToDecimals(amount, 2);
    
    if (roundedAmount === 0) {
        errorRecordsArray.push(line + "|Zero amount");
    } else {
        validRecordsArray.push(line);
    }
}

// ✅ Join once at end
var validRecords = validRecordsArray.join("
");
var errorRecords = errorRecordsArray.join("
");
```

**Improvements**:
- Array accumulation (50x faster for large datasets)
- NULL safety (prevents runtime errors)
- Floating point rounding (prevents comparison bugs)
- Input validation (catches data quality issues)
- Empty line handling (cleaner output)

### Scenario 3: Nested Loop Optimization

**Context**: Matching 1,000 invoices against 5,000 PO lines

**Bad Implementation (O(n²) - 5 million comparisons)**:

```javascript
var matchedInvoices = [];

// ❌ Nested loop without optimization
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < poLines.length; j++) {
        if (invoices[i].poNumber === poLines[j].poNumber &&
            invoices[i].lineNumber === poLines[j].lineNumber) {
            matchedInvoices.push({
                invoice: invoices[i],
                poLine: poLines[j]
            });
            break;  // At least breaks after match
        }
    }
}
```

**Good Implementation (O(n) - 6,000 operations)**:

```javascript
// ✅ Build lookup map (O(n))
var poLookup = {};
for (var i = 0; i < poLines.length; i++) {
    var key = poLines[i].poNumber + "|" + poLines[i].lineNumber;
    poLookup[key] = poLines[i];
}

// ✅ Single loop with map lookup (O(n))
var matchedInvoices = [];
for (var i = 0; i < invoices.length; i++) {
    var key = invoices[i].poNumber + "|" + invoices[i].lineNumber;
    var poLine = poLookup[key];
    
    if (poLine) {
        matchedInvoices.push({
            invoice: invoices[i],
            poLine: poLine
        });
    }
}
```

**Performance Improvement**:
- Bad: 5,000,000 comparisons (1,000 × 5,000)
- Good: 6,000 operations (5,000 + 1,000)
- **Speedup: 833x faster**

## Performance Optimization Checklist

### Memory Optimization

**1. Array Accumulation vs String Concatenation**

```javascript
// ❌ BAD: O(n²) memory copying
var result = "";
for (var i = 0; i < 1000; i++) {
    result += data[i] + "
";  // Creates 1000 new strings
}

// ✅ GOOD: O(n) memory usage
var resultArray = [];
for (var i = 0; i < 1000; i++) {
    resultArray.push(data[i]);  // Reuses array memory
}
var result = resultArray.join("
");  // Single allocation
```

**2. Reuse Variables Instead of Creating New Ones**

```javascript
// ❌ BAD: Creates 1000 new variables
for (var i = 0; i < 1000; i++) {
    var temp = data[i].toUpperCase();
    var trimmed = temp.trim();
    var replaced = trimmed.replace(/,/g, "|");
    results.push(replaced);
}

// ✅ GOOD: Reuses single variable
var temp;
for (var i = 0; i < 1000; i++) {
    temp = data[i].toUpperCase().trim().replace(/,/g, "|");
    results.push(temp);
}
```

**3. Avoid Unnecessary Array Copies**

```javascript
// ❌ BAD: Creates new array on each iteration
for (var i = 0; i < items.length; i++) {
    var subset = items.slice(0, i);  // O(n²) total
    process(subset);
}

// ✅ GOOD: Process in place
for (var i = 0; i < items.length; i++) {
    process(items, i);  // Pass index instead
}
```

### Speed Optimization

**1. Hoist Invariant Calculations Outside Loops**

```javascript
// ❌ BAD: Calculates same value 1000 times
for (var i = 0; i < 1000; i++) {
    var multiplier = Math.pow(10, 2);  // Recalculated each iteration
    results.push(data[i] * multiplier);
}

// ✅ GOOD: Calculate once
var multiplier = Math.pow(10, 2);
for (var i = 0; i < 1000; i++) {
    results.push(data[i] * multiplier);
}
```

**2. Cache Array Length**

```javascript
// ❌ BAD: Accesses .length property 1000 times
for (var i = 0; i < items.length; i++) {
    process(items[i]);
}

// ✅ GOOD: Cache length (minor optimization, but good practice)
var len = items.length;
for (var i = 0; i < len; i++) {
    process(items[i]);
}
```

**3. Use Lookup Maps for Repeated Searches**

```javascript
// ❌ BAD: O(n²) - searches array repeatedly
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < vendors.length; j++) {
        if (invoices[i].vendorId === vendors[j].id) {
            invoices[i].vendorName = vendors[j].name;
            break;
        }
    }
}

// ✅ GOOD: O(n) - build map once, lookup is O(1)
var vendorMap = {};
for (var i = 0; i < vendors.length; i++) {
    vendorMap[vendors[i].id] = vendors[i].name;
}
for (var i = 0; i < invoices.length; i++) {
    invoices[i].vendorName = vendorMap[invoices[i].vendorId] || "";
}
```

**4. Compile Regex Outside Loops**

```javascript
// ❌ BAD: Compiles regex 1000 times
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(/[^0-9]/g, "");  // Regex compiled each time
    results.push(cleaned);
}

// ✅ GOOD: Compile once (ES5 doesn't have explicit compilation, but pattern is cached)
var digitPattern = /[^0-9]/g;
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(digitPattern, "");
    results.push(cleaned);
}
```

### Space Optimization

**1. Clear Large Variables After Use**

```javascript
// Process large dataset
var largeData = fetchLargeDataset();  // 10MB
var processed = processData(largeData);

// ✅ Clear reference to allow garbage collection
largeData = null;

// Continue with processed data
return processed;
```

**2. Process Data in Chunks**

```javascript
// ❌ BAD: Load entire file into memory
var allLines = fileContent.split("
");  // 100MB in memory
var results = [];
for (var i = 0; i < allLines.length; i++) {
    results.push(processLine(allLines[i]));
}

// ✅ GOOD: Process in chunks (if possible)
var CHUNK_SIZE = 1000;
var results = [];
var lines = fileContent.split("
");

for (var i = 0; i < lines.length; i += CHUNK_SIZE) {
    var chunk = lines.slice(i, i + CHUNK_SIZE);
    for (var j = 0; j < chunk.length; j++) {
        results.push(processLine(chunk[j]));
    }
    chunk = null;  // Clear chunk
}
```

## Performance Measurement Tips

### Timing Code Execution

```javascript
// Start timer
var startTime = new Date().getTime();

// Your code here
for (var i = 0; i < 10000; i++) {
    // ... processing ...
}

// End timer
var endTime = new Date().getTime();
var elapsedMs = endTime - startTime;

// Log result
console.log("Execution time: " + elapsedMs + "ms");
```

### Memory Usage Estimation

```javascript
// Estimate string memory usage
function estimateStringMemory(str) {
    // Each character is ~2 bytes in JavaScript
    return str.length * 2;
}

// Estimate array memory usage
function estimateArrayMemory(arr) {
    var total = 0;
    for (var i = 0; i < arr.length; i++) {
        if (typeof arr[i] === "string") {
            total += arr[i].length * 2;
        }
    }
    return total;
}

// Example usage
var data = "Large string data...";
var memoryBytes = estimateStringMemory(data);
var memoryMB = memoryBytes / (1024 * 1024);
console.log("Estimated memory: " + memoryMB.toFixed(2) + " MB");
```text

## Output Format

### Analysis Summary

```text

📊 IPA JAVASCRIPT ES5 ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code: [First 50 chars...]
Lines: 85
Complexity: Medium
Node Type: Assign

OVERALL ASSESSMENT: ⚠️ NEEDS IMPROVEMENT

Critical Issues: 3 (ES5 compliance violations)
High Priority: 5 (Missing NULL checks)
Medium Priority: 8 (Performance optimizations)
Low Priority: 2 (Code quality)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Issue Details

```text

🔴 CRITICAL: Arrow Function Usage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Category: ES5 Compliance
Impact: Runtime error in IPA (arrow functions not supported)
Line: 23

Issue:
Arrow function syntax is ES6+ and will cause immediate runtime error
in IPA's ES5 JavaScript environment.

Current Code:
var filtered = items.filter(item => item.status === "Active");

Recommended Fix:
var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

Explanation:
IPA JavaScript executes in ES5 environment. Use traditional for loops
and function keyword instead of arrow functions and array methods like
.filter(), .map(), .find().

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Improved Code

```text

✅ IMPROVED CODE (ES5 COMPLIANT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied:

1. Converted all let/const to var
2. Replaced arrow functions with function keyword
3. Replaced template literals with string concatenation
4. Added NULL/undefined checks
5. Added floating point rounding
6. Added division by zero checks

7. Improved error handling
8. Added descriptive comments

// IPA Assign Node: Transform Import Data
// Purpose: Parse and validate import file content
// Input: ImportFile (string), FileName (string)
// Output: Processed records array

function transformImportData(importFileContent, fileName) {
    // Configuration
    var ROUND_DECIMALS = 2;
    var REQUIRED_FIELDS = ["id", "amount", "quantity"];
    
    // Input validation
    if (!importFileContent || typeof importFileContent !== "string") {
        importFileContent = "";
    }
    
    if (!fileName || typeof fileName !== "string") {
        fileName = "unknown";
    }
    
    // Initialize result arrays
    var processedRecords = [];
    var exceptions = [];
    
    // Parse input (assuming CSV format)
    var lines = importFileContent.split("\n");
    
    // Process each line
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        
        // Skip empty lines
        if (!line || line.trim() === "") {
            continue;
        }
        
        var fields = line.split(",");
        
        // Validate required fields
        if (fields.length < REQUIRED_FIELDS.length) {
            exceptions.push({
                line: i + 1,
                error: "Missing required fields"
            });
            continue;
        }
        
        // Extract and validate fields
        var id = fields[0] ? fields[0].trim() : "";
        var amountStr = fields[1] ? fields[1].trim() : "0";
        var quantityStr = fields[2] ? fields[2].trim() : "0";
        
        // Parse numeric values with validation
        var amount = parseFloat(amountStr);
        if (isNaN(amount)) {
            exceptions.push({
                line: i + 1,
                field: "amount",
                error: "Invalid numeric value: " + amountStr
            });
            continue;
        }
        
        var quantity = parseFloat(quantityStr);
        if (isNaN(quantity)) {
            exceptions.push({
                line: i + 1,
                field: "quantity",
                error: "Invalid numeric value: " + quantityStr
            });
            continue;
        }
        
        // Division by zero check
        var unitPrice = 0;
        if (quantity === 0) {
            exceptions.push({
                line: i + 1,
                error: "Quantity is zero, cannot calculate unit price"
            });
            continue;
        } else {
            unitPrice = amount / quantity;
        }
        
        // Round for safe comparison
        var roundedAmount = roundToDecimals(amount, ROUND_DECIMALS);
        
        // Build result record
        var record = {
            id: id,
            amount: roundedAmount,
            quantity: quantity,
            unitPrice: roundToDecimals(unitPrice, ROUND_DECIMALS),
            fileName: fileName,
            lineNumber: i + 1
        };
        
        processedRecords.push(record);
    }
    
    // Helper function: Round to specified decimals
    function roundToDecimals(num, decimals) {
        var multiplier = Math.pow(10, decimals);
        return Math.round(num * multiplier) / multiplier;
    }
    
    // Return results
    return {
        records: processedRecords,
        exceptions: exceptions,
        totalProcessed: processedRecords.length,
        totalErrors: exceptions.length
    };
}

// Invoke function with IPA variables
transformImportData(ImportFile, FileName);

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

## Integration with IPA

### IPA Assign Node Structure

```javascript

// Entire script wrapped in function
function processData(inputData, configValue) {
    // Configuration variables INSIDE function
    var MAX_RECORDS = 1000;
    var DELIMITER = ",";
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing logic
    var results = [];
    // ... transformation ...
    
    return results;
}

// Function invocation at end (NO top-level return)
processData(InputVariable, ConfigVariable);

```text

### Global Variables (Start Node)

**CRITICAL**: Start node global variables are defined in the **Properties** tab, NOT as JavaScript code.

```text

Start Node Properties (NOT JavaScript):
queryID = ""
auth = ""
rowCount = 0
accessTokenResp = ""
OutputRecords = ""
offset = 0
limit = 1000

```text

These become global variables accessible throughout the process. No `var` keyword needed in Properties tab.

### Common IPA Patterns

**Pattern: Accumulator Loop**

```javascript

var allRecords = [];
var hasMoreData = true;
var offset = 0;
var limit = 1000;

while (hasMoreData) {
    // Fetch page of data
    var pageData = fetchData(offset, limit);
    
    // Append to accumulator
    allRecords = allRecords.concat(pageData);
    
    // Check if more data exists
    hasMoreData = (pageData.length === limit);
    offset += limit;
}

```text

**Pattern: Error Collection**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    try {
        processRecord(records[i]);
    } catch (e) {
        exceptions.push({
            record: i,
            error: e.message || "Unknown error"
        });
    }
}

```text

## Advanced Features

### Code Complexity Scoring

- **Simple**: Single loop, basic operations, < 50 lines
- **Medium**: Multiple loops, conditionals, 50-150 lines
- **Complex**: Nested loops, complex logic, 150-300 lines
- **Very Complex**: Deep nesting, multiple functions, > 300 lines

### Performance Estimation

- **Fast**: O(n) complexity, simple operations
- **Moderate**: O(n²) complexity, string operations
- **Slow**: O(n³) complexity, nested loops
- **Very Slow**: Exponential complexity, inefficient algorithms

### Production Readiness Score

Based on:

- NULL/undefined handling (30%)
- Error handling (25%)
- Edge case coverage (20%)
- Type validation (15%)
- Code quality (10%)

## Usage Examples

### Example 1: Quick Question

```text

User: How do I convert an array to uppercase in ES5?

Skill: In ES5, you need to use a for loop instead of .map():

var items = ["apple", "banana", "cherry"];
var uppercased = [];
for (var i = 0; i < items.length; i++) {
    uppercased.push(items[i].toUpperCase());
}
// Result: ["APPLE", "BANANA", "CHERRY"]

```text

### Example 2: Code Review (Pasted)

```text

User: Review this:
let items = data.filter(x => x.status === "Active");

Skill: [Identifies ES6 violations: let, arrow function, .filter()]
[Provides ES5-compliant alternative with for loop]

```text

### Example 3: Code Generation

```text

User: I need JavaScript to:

1. Parse CSV input
2. Validate required fields (id, amount, quantity)
3. Calculate unit price (amount / quantity)
4. Handle division by zero
5. Collect errors

Skill: [Generates complete ES5-compliant code with:

- Input validation
- CSV parsing
- Field validation
- Safe division
- Error collection
- Proper IPA Assign node structure]

```text

### Example 4: Troubleshooting

```text

User: This code fails with "unexpected token" on line 15:
const MAX_ITEMS = 100;

Skill: The error is caused by ES6 'const' keyword. IPA uses ES5 environment.

Fix:
var MAX_ITEMS = 100;

ES5 doesn't support 'const' or 'let'. Always use 'var' for all variable declarations.

```text

### Example 5: Optimization

```text

User: This code is slow, can you optimize it?
[Shows nested loop code]

Skill: [Analyzes O(n²) complexity]
[Provides O(n) solution using lookup map]
[Explains performance improvement]

```text

### Example 6: Learning

```text

User: Explain IPA Assign node structure

Skill: [Provides detailed explanation with example]
[Shows function wrapper pattern]
[Explains configuration placement]
[Demonstrates function invocation]

```text

## Code Generation Capabilities

### Data Transformation

**Request:**

```text

Transform JSON array to CSV format with specific columns

```text

**Generates:**

- Input validation
- JSON parsing
- Field extraction
- CSV formatting
- Error handling
- ES5-compliant code

### Validation Routines

**Request:**

```text

Validate order data: required fields, numeric amounts, date formats

```text

**Generates:**

- Field presence checks
- Type validation
- Format validation
- Error collection
- Descriptive error messages

### API Response Processing

**Request:**

```text

Parse Compass API response, extract records, handle pagination

```text

**Generates:**

- JSON parsing
- NULL safety
- Array handling
- Pagination logic
- Error handling

### File Processing

**Request:**

```text

Read CSV file, parse lines, validate data, transform to JSON

```text

**Generates:**

- File content validation
- Line-by-line parsing
- Field extraction
- Data transformation
- Error collection

### Calculation Logic

**Request:**

```text

Calculate totals, subtotals, tax, with rounding and validation

```text

**Generates:**

- Safe numeric parsing
- Floating point rounding
- Division by zero checks
- Accumulation logic
- Result formatting

### Error Handling Patterns

**Request:**

```text

Collect errors during processing, categorize by severity

```text

**Generates:**

- Try-catch blocks
- Error collection array
- Error categorization
- Descriptive messages
- Error summary

## Tips for Best Results

1. **Be Specific**: Describe requirements clearly
2. **Provide Context**: Mention node type, data source, expected output
3. **Share Errors**: Include full error messages
4. **Show Examples**: Provide sample input/output data
5. **Ask Questions**: No question is too basic
6. **Request Explanations**: Ask "why" for better understanding

## Quick Reference - Common Questions

### Variables & Declarations

**Q: How do I declare variables in ES5?**

```javascript

var name = "John";
var count = 0;
var isActive = true;

```text

**Q: Can I use let or const?**
No. IPA uses ES5 environment. Always use `var`.

### Arrays

**Q: How do I loop through an array?**

```javascript

for (var i = 0; i < items.length; i++) {
    var item = items[i];
    // Process item
}

```text

**Q: How do I filter an array?**

```javascript

var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

```text

**Q: How do I map an array?**

```javascript

var mapped = [];
for (var i = 0; i < items.length; i++) {
    mapped.push(items[i].value * 2);
}

```text

### Strings

**Q: How do I concatenate strings?**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

**Q: Can I use template literals?**
No. Use string concatenation with `+` operator.

**Q: How do I check if string contains substring?**

```javascript

if (str.indexOf("substring") !== -1) {
    // Found
}

```text

### Functions

**Q: How do I write a function?**

```javascript

function calculateTotal(items) {
    var total = 0;
    for (var i = 0; i < items.length; i++) {
        total += items[i].amount;
    }
    return total;
}

```text

**Q: Can I use arrow functions?**
No. Always use `function` keyword.

### NULL Safety

**Q: How do I check for NULL/undefined?**

```javascript

if (!value || typeof value !== "string") {
    value = "";  // Default
}

```text

**Q: How do I safely access object properties?**

```javascript

var name = "";
if (person && typeof person === "object") {
    name = person.firstName || "";
}

```text

### Numbers

**Q: How do I parse numbers safely?**

```javascript

var num = parseFloat(input);
if (isNaN(num)) {
    num = 0;  // Default
}

```text

**Q: How do I compare floating point numbers?**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var rounded = roundToDecimals(0.1 + 0.2, 2);
if (rounded === 0.3) {
    // Safe comparison
}

```text

**Q: How do I check for division by zero?**

```javascript

if (denominator === 0) {
    // Handle error
    return;
}
var result = numerator / denominator;

```text

### IPA-Specific

**Q: What's the IPA Assign node structure?**

```javascript

function processData(inputData) {
    // Configuration
    var MAX_RECORDS = 1000;
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing
    var results = [];
    // ... logic ...
    
    return results;
}

// Invoke function
processData(InputVariable);

```text

**Q: How do I define global variables?**
Define them in Start node Properties tab (NOT JavaScript):

```text

queryID = ""
rowCount = 0
offset = 0

```text

**Q: How do I collect errors?**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    if (!records[i].id) {
        exceptions.push({
            record: i,
            error: "Missing ID"
        });
        continue;
    }
}

```text

### Debugging

**Q: "unexpected token" error - what does it mean?**
Usually ES6+ syntax in ES5 environment. Check for:

- `let`/`const` (use `var`)
- Arrow functions `=>` (use `function`)
- Template literals `` `${}` `` (use `+`)

**Q: "Cannot read property of undefined" - how to fix?**
Add NULL checks:

```javascript

if (obj && obj.property) {
    // Safe to access
}

```text

**Q: Code works in browser but fails in IPA - why?**
Browser supports ES6+, IPA uses ES5. Convert modern syntax to ES5.

## Limitations

This skill analyzes JavaScript syntax and patterns but cannot:

- Execute code in IPA environment
- Access IPA global variables
- Test against live data
- Validate IPA-specific functions
- Measure actual execution time

For live validation, test in IPA Designer.

## Version History

- **1.2.0** (2026-03-09): Added real-world performance scenarios and optimization best practices
  - Real-world Scenario 1: Compass API pagination (50x speedup)
  - Real-world Scenario 2: File processing with validation
  - Real-world Scenario 3: Nested loop optimization (833x speedup)
  - Performance optimization checklist (memory, speed, space)
  - Performance measurement tips
- **1.1.0** (2026-03-09): Added string concatenation performance pattern
  - New Pattern 10: String Concatenation in Loops (O(n²) vs O(n) complexity)
  - Performance comparison table (50-500x speedup for large datasets)
  - Pagination loop optimization guidance
  - Array accumulation pattern for data aggregation
- **1.0.0** (2026-03-09): Initial release with comprehensive ES5 analysis
.Value -replace '```', '```text' 
   Loads `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md` when working with:
   - Compass API JavaScript
   - Data Lake queries
   - JSON parsing from API responses

**The skill will automatically load relevant steering files based on the task context.**

The skill performs comprehensive analysis across 6 dimensions:

1. **ES5 Compliance**

   - No `let`/`const` (use `var`)
   - No arrow functions (use `function`)
   - No template literals (use string concatenation)
   - No destructuring (explicit property access)
   - No default parameters (check inside function)
   - No spread operator (use `.slice()`, `.concat()`)
   - No ES6+ methods (`.map()`, `.filter()`, `.find()`)

2. **Best Practices**

   - Defensive NULL/undefined checks
   - Input validation
   - Type checking before operations
   - Proper error handling
   - Meaningful variable names
   - Comments for complex logic

3. **Performance**

   - Efficient loops (avoid nested loops where possible)
   - String concatenation optimization
   - Array operations efficiency
   - Avoid redundant calculations
   - Memory-efficient patterns

4. **Production Readiness**

   - Edge case handling (empty strings, zero, NULL)
   - Floating point comparison (rounding)
   - Division by zero checks
   - Array bounds checking
   - Safe type conversions

5. **Code Quality**

   - Readability (formatting, indentation)
   - Maintainability (modularity, reusability)
   - Naming conventions (descriptive names)
   - Comment quality
   - Code organization

6. **IPA-Specific Patterns**

   - Assign node structure (function wrapper)
   - Global variable usage
   - Configuration at top of function
   - No top-level return statements
   - Function invocation at end

### Step 3: Recommendations

For each issue found, provides:

- **Severity**: Critical / High / Medium / Low
- **Category**: ES5 Compliance / Best Practices / Performance / Production Readiness
- **Explanation**: Why this matters
- **Fix**: Specific code changes
- **Example**: Before/after comparison

### Step 4: Improved Code

Generates refactored code with:

- All ES6+ features converted to ES5
- Best practices applied
- Performance optimizations
- Production-ready error handling
- Comments explaining changes

## Analysis Categories

### ES5 Compliance Issues

**Critical:**

- `let` or `const` declarations
- Arrow functions `() => {}`
- Template literals `` `${var}` ``
- `async`/`await`
- Destructuring `{prop} = obj`
- Spread operator `...arr`
- ES6+ methods (`.map()`, `.filter()`, `.find()`)

**High:**

- Default parameters `function(x = 1)`
- `class` keyword
- `import`/`export` statements
- `Promise` usage
- `for...of` loops

**Medium:**

- Object shorthand `{prop}` instead of `{prop: prop}`
- Computed property names `{[key]: value}`
- Method shorthand `{method() {}}`

### Best Practices Issues

**Critical:**

- No NULL/undefined checks before operations
- No input validation
- Missing error handling
- Unsafe type conversions

**High:**

- No defensive programming patterns
- Missing edge case handling
- Unclear variable names
- No comments for complex logic

**Medium:**

- Inconsistent naming conventions
- Poor code organization
- Redundant code
- Magic numbers without explanation

### Performance Issues

**Critical:**

- Nested loops with high complexity
- **String concatenation in loops** (O(n²) complexity - use array accumulation)
- Redundant calculations inside loops

**High:**

- Unnecessary array iterations
- Inefficient search patterns
- Memory-intensive operations

**Medium:**

- Suboptimal algorithm choices
- Unnecessary variable declarations
- Redundant type checks

### Production Readiness Issues

**Critical:**

- No division by zero checks
- No floating point rounding before comparison
- Missing NULL guards on critical operations

**High:**

- No empty string/array checks
- Missing array bounds validation
- Unsafe parseInt/parseFloat usage

**Medium:**

- No default value handling
- Missing type validation
- Insufficient error messages

## Common Patterns Analyzed

### Pattern 1: Variable Declarations

**Bad (ES6):**

```javascript

let count = 0;
const MAX_ITEMS = 100;

```text

**Good (ES5):**

```javascript

var count = 0;
var MAX_ITEMS = 100;

```text

### Pattern 2: Arrow Functions

**Bad (ES6):**

```javascript

var result = items.map(item => item.value);

```text

**Good (ES5):**

```javascript

var result = [];
for (var i = 0; i < items.length; i++) {
    result.push(items[i].value);
}

```text

### Pattern 3: Template Literals

**Bad (ES6):**

```javascript

var message = `Hello ${name}, you have ${count} items`;

```text

**Good (ES5):**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

### Pattern 4: Destructuring

**Bad (ES6):**

```javascript

var {firstName, lastName} = person;

```text

**Good (ES5):**

```javascript

var firstName = person.firstName;
var lastName = person.lastName;

```text

### Pattern 5: Default Parameters

**Bad (ES6):**

```javascript

function calculate(amount, rate = 0.05) {
    return amount * rate;
}

```text

**Good (ES5):**

```javascript

function calculate(amount, rate) {
    if (typeof rate === "undefined") {
        rate = 0.05;
    }
    return amount * rate;
}

```text

### Pattern 6: Spread Operator

**Bad (ES6):**

```javascript

var combined = [...array1, ...array2];

```text

**Good (ES5):**

```javascript

var combined = array1.concat(array2);

```text

### Pattern 7: Defensive NULL Checks

**Bad:**

```javascript

var total = parseFloat(amount);
if (total === 0) {
    // May fail if amount is NULL/undefined
}

```text

**Good:**

```javascript

if (!amount || typeof amount !== "string") {
    amount = "0";
}
var total = parseFloat(amount);
if (isNaN(total)) {
    total = 0;
}
if (total === 0) {
    // Safe comparison
}

```text

### Pattern 8: Floating Point Comparison

**Bad:**

```javascript

if (sumQty === 0) {
    // Unreliable for floating point
}

```text

**Good:**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var roundedSum = roundToDecimals(sumQty, 2);
if (roundedSum === 0) {
    // Safe comparison
}

```text

### Pattern 9: Division by Zero

**Bad:**

```javascript

var unitCost = extendedAmount / originalQuantity;

```

### Pattern 10: String Concatenation in Loops (CRITICAL PERFORMANCE)

**Bad (O(n²) complexity):**

```javascript
// Inside pagination loop (100+ iterations)
OutputRecords += GetResultOut + "

";
```

**Why It's Bad:**
- Strings are immutable in JavaScript
- Each `+=` creates a NEW string and copies ALL previous content
- 100 iterations = ~5MB copied for 100KB of data
- Performance degrades exponentially with data size

**Good (O(n) complexity):**

```javascript
// BEFORE the pagination loop
var OutputRecordsArray = [];

// INSIDE the pagination loop
while (hasMoreData) {
    // ... fetch and transform data ...
    
    // Push to array instead of string concatenation
    for (var i = 0; i < transformedLines.length; i++) {
        OutputRecordsArray.push(transformedLines[i]);
    }
    
    // ... pagination logic ...
    offset += limit;
}

// AFTER the loop completes - join once
var OutputRecords = OutputRecordsArray.join("

");
```

**Performance Comparison:**

| Approach | Complexity | 100 Iterations | 1000 Iterations |
|----------|-----------|----------------|-----------------|
| String += | O(n²) | ~5MB copied | ~500MB copied |
| Array.push() + join() | O(n) | ~100KB copied | ~1MB copied |
| **Speedup** | **Linear** | **50x faster** | **500x faster** |

**When to Use:**
- Any loop with 10+ iterations
- Pagination loops processing large datasets
- File processing with line-by-line accumulation
- Data transformation with result aggregationtext

**Good:**

```javascript

if (originalQuantity === 0) {
    exceptions.push({error: "Division by zero"});
    continue;
}
var unitCost = extendedAmount / originalQuantity;

```text

### Pattern 11: IPA Assign Node Structure

**Bad:**

```javascript

// Top-level code
var result = processData(input);
return result;  // ERROR: No top-level return

```text

**Good:**

```javascript

function transformData(inputData, fileName) {
    // Configuration variables
    var CONFIG_VALUE = "setting";
    
    // Validation
    if (!inputData || typeof inputData !== "string") {
        inputData = "";
    }
    
    // Processing logic
    var result = [];
    // ... transformation ...
    
    return result;
}

// Function invocation at end
transformData(ImportFile, FileName);

```

## Real-World Performance Scenarios

### Scenario 1: Compass API Pagination (Production)

**Context**: MatchReport_Outbound.lpd processing 50,000 GL transactions

**Bad Implementation (O(n²) - 45 minutes execution)**:

```javascript
// Global variable
var OutputRecords = "";

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        GetResultArr[i] = GetResultArr[i].replace(/,/g, "|");
    }
    GetResultOut = GetResultArr.join("
");
    
    // ❌ BAD: String concatenation in loop
    OutputRecords += GetResultOut + "
";  // O(n²) complexity
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}
```

**Performance Impact**:
- Iteration 1: Copy 10KB
- Iteration 100: Copy 1MB (100 × 10KB)
- Iteration 500: Copy 5MB (500 × 10KB)
- Total: ~1.25GB copied for 5MB of data
- Execution time: 45 minutes

**Good Implementation (O(n) - 54 seconds execution)**:

```javascript
// Global variable (array accumulator)
var OutputRecordsArray = [];

// Pagination loop (500 iterations, 100 records each)
while (hasMoreData) {
    // Fetch page from Compass API
    var GetResultOut = /* API call returns 100 records */;
    
    // Transform CSV data
    var GetResultArr = GetResultOut.trim().split("
");
    for (var i = 0; i < GetResultArr.length; i++) {
        var line = GetResultArr[i];
        if (line && line.trim() !== "") {
            // ✅ GOOD: Push to array
            OutputRecordsArray.push(line.replace(/,/g, "|"));
        }
    }
    
    offset += limit;
    hasMoreData = (GetResultArr.length === limit);
}

// Join once after loop completes
var OutputRecords = OutputRecordsArray.join("
");
```

**Performance Improvement**:
- Total: ~5MB copied (linear growth)
- Execution time: 54 seconds
- **Speedup: 50x faster**
- Memory efficiency: 250x less copying

### Scenario 2: File Processing with Validation

**Context**: Invoice import processing 10,000 lines with validation

**Bad Implementation (Multiple Issues)**:

```javascript
var validRecords = "";
var errorRecords = "";

for (var i = 0; i < lines.length; i++) {
    var fields = lines[i].split(",");
    
    // ❌ Issue 1: No NULL check
    var amount = parseFloat(fields[2]);
    
    // ❌ Issue 2: Floating point comparison without rounding
    if (amount === 0) {
        errorRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    } else {
        validRecords += lines[i] + "
";  // ❌ Issue 3: String concatenation
    }
}
```

**Good Implementation (All Best Practices)**:

```javascript
var validRecordsArray = [];
var errorRecordsArray = [];

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    
    // ✅ Skip empty lines
    if (!line || line.trim() === "") {
        continue;
    }
    
    var fields = line.split(",");
    
    // ✅ Validate field count
    if (fields.length < 3) {
        errorRecordsArray.push(line + "|Missing fields");
        continue;
    }
    
    // ✅ NULL check and safe parsing
    var amountStr = fields[2] ? fields[2].trim() : "0";
    var amount = parseFloat(amountStr);
    
    // ✅ Validate numeric
    if (isNaN(amount)) {
        errorRecordsArray.push(line + "|Invalid amount: " + amountStr);
        continue;
    }
    
    // ✅ Round before comparison
    var roundedAmount = roundToDecimals(amount, 2);
    
    if (roundedAmount === 0) {
        errorRecordsArray.push(line + "|Zero amount");
    } else {
        validRecordsArray.push(line);
    }
}

// ✅ Join once at end
var validRecords = validRecordsArray.join("
");
var errorRecords = errorRecordsArray.join("
");
```

**Improvements**:
- Array accumulation (50x faster for large datasets)
- NULL safety (prevents runtime errors)
- Floating point rounding (prevents comparison bugs)
- Input validation (catches data quality issues)
- Empty line handling (cleaner output)

### Scenario 3: Nested Loop Optimization

**Context**: Matching 1,000 invoices against 5,000 PO lines

**Bad Implementation (O(n²) - 5 million comparisons)**:

```javascript
var matchedInvoices = [];

// ❌ Nested loop without optimization
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < poLines.length; j++) {
        if (invoices[i].poNumber === poLines[j].poNumber &&
            invoices[i].lineNumber === poLines[j].lineNumber) {
            matchedInvoices.push({
                invoice: invoices[i],
                poLine: poLines[j]
            });
            break;  // At least breaks after match
        }
    }
}
```

**Good Implementation (O(n) - 6,000 operations)**:

```javascript
// ✅ Build lookup map (O(n))
var poLookup = {};
for (var i = 0; i < poLines.length; i++) {
    var key = poLines[i].poNumber + "|" + poLines[i].lineNumber;
    poLookup[key] = poLines[i];
}

// ✅ Single loop with map lookup (O(n))
var matchedInvoices = [];
for (var i = 0; i < invoices.length; i++) {
    var key = invoices[i].poNumber + "|" + invoices[i].lineNumber;
    var poLine = poLookup[key];
    
    if (poLine) {
        matchedInvoices.push({
            invoice: invoices[i],
            poLine: poLine
        });
    }
}
```

**Performance Improvement**:
- Bad: 5,000,000 comparisons (1,000 × 5,000)
- Good: 6,000 operations (5,000 + 1,000)
- **Speedup: 833x faster**

## Performance Optimization Checklist

### Memory Optimization

**1. Array Accumulation vs String Concatenation**

```javascript
// ❌ BAD: O(n²) memory copying
var result = "";
for (var i = 0; i < 1000; i++) {
    result += data[i] + "
";  // Creates 1000 new strings
}

// ✅ GOOD: O(n) memory usage
var resultArray = [];
for (var i = 0; i < 1000; i++) {
    resultArray.push(data[i]);  // Reuses array memory
}
var result = resultArray.join("
");  // Single allocation
```

**2. Reuse Variables Instead of Creating New Ones**

```javascript
// ❌ BAD: Creates 1000 new variables
for (var i = 0; i < 1000; i++) {
    var temp = data[i].toUpperCase();
    var trimmed = temp.trim();
    var replaced = trimmed.replace(/,/g, "|");
    results.push(replaced);
}

// ✅ GOOD: Reuses single variable
var temp;
for (var i = 0; i < 1000; i++) {
    temp = data[i].toUpperCase().trim().replace(/,/g, "|");
    results.push(temp);
}
```

**3. Avoid Unnecessary Array Copies**

```javascript
// ❌ BAD: Creates new array on each iteration
for (var i = 0; i < items.length; i++) {
    var subset = items.slice(0, i);  // O(n²) total
    process(subset);
}

// ✅ GOOD: Process in place
for (var i = 0; i < items.length; i++) {
    process(items, i);  // Pass index instead
}
```

### Speed Optimization

**1. Hoist Invariant Calculations Outside Loops**

```javascript
// ❌ BAD: Calculates same value 1000 times
for (var i = 0; i < 1000; i++) {
    var multiplier = Math.pow(10, 2);  // Recalculated each iteration
    results.push(data[i] * multiplier);
}

// ✅ GOOD: Calculate once
var multiplier = Math.pow(10, 2);
for (var i = 0; i < 1000; i++) {
    results.push(data[i] * multiplier);
}
```

**2. Cache Array Length**

```javascript
// ❌ BAD: Accesses .length property 1000 times
for (var i = 0; i < items.length; i++) {
    process(items[i]);
}

// ✅ GOOD: Cache length (minor optimization, but good practice)
var len = items.length;
for (var i = 0; i < len; i++) {
    process(items[i]);
}
```

**3. Use Lookup Maps for Repeated Searches**

```javascript
// ❌ BAD: O(n²) - searches array repeatedly
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < vendors.length; j++) {
        if (invoices[i].vendorId === vendors[j].id) {
            invoices[i].vendorName = vendors[j].name;
            break;
        }
    }
}

// ✅ GOOD: O(n) - build map once, lookup is O(1)
var vendorMap = {};
for (var i = 0; i < vendors.length; i++) {
    vendorMap[vendors[i].id] = vendors[i].name;
}
for (var i = 0; i < invoices.length; i++) {
    invoices[i].vendorName = vendorMap[invoices[i].vendorId] || "";
}
```

**4. Compile Regex Outside Loops**

```javascript
// ❌ BAD: Compiles regex 1000 times
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(/[^0-9]/g, "");  // Regex compiled each time
    results.push(cleaned);
}

// ✅ GOOD: Compile once (ES5 doesn't have explicit compilation, but pattern is cached)
var digitPattern = /[^0-9]/g;
for (var i = 0; i < 1000; i++) {
    var cleaned = data[i].replace(digitPattern, "");
    results.push(cleaned);
}
```

### Space Optimization

**1. Clear Large Variables After Use**

```javascript
// Process large dataset
var largeData = fetchLargeDataset();  // 10MB
var processed = processData(largeData);

// ✅ Clear reference to allow garbage collection
largeData = null;

// Continue with processed data
return processed;
```

**2. Process Data in Chunks**

```javascript
// ❌ BAD: Load entire file into memory
var allLines = fileContent.split("
");  // 100MB in memory
var results = [];
for (var i = 0; i < allLines.length; i++) {
    results.push(processLine(allLines[i]));
}

// ✅ GOOD: Process in chunks (if possible)
var CHUNK_SIZE = 1000;
var results = [];
var lines = fileContent.split("
");

for (var i = 0; i < lines.length; i += CHUNK_SIZE) {
    var chunk = lines.slice(i, i + CHUNK_SIZE);
    for (var j = 0; j < chunk.length; j++) {
        results.push(processLine(chunk[j]));
    }
    chunk = null;  // Clear chunk
}
```

## Performance Measurement Tips

### Timing Code Execution

```javascript
// Start timer
var startTime = new Date().getTime();

// Your code here
for (var i = 0; i < 10000; i++) {
    // ... processing ...
}

// End timer
var endTime = new Date().getTime();
var elapsedMs = endTime - startTime;

// Log result
console.log("Execution time: " + elapsedMs + "ms");
```

### Memory Usage Estimation

```javascript
// Estimate string memory usage
function estimateStringMemory(str) {
    // Each character is ~2 bytes in JavaScript
    return str.length * 2;
}

// Estimate array memory usage
function estimateArrayMemory(arr) {
    var total = 0;
    for (var i = 0; i < arr.length; i++) {
        if (typeof arr[i] === "string") {
            total += arr[i].length * 2;
        }
    }
    return total;
}

// Example usage
var data = "Large string data...";
var memoryBytes = estimateStringMemory(data);
var memoryMB = memoryBytes / (1024 * 1024);
console.log("Estimated memory: " + memoryMB.toFixed(2) + " MB");
```text

## Output Format

### Analysis Summary

```text

📊 IPA JAVASCRIPT ES5 ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code: [First 50 chars...]
Lines: 85
Complexity: Medium
Node Type: Assign

OVERALL ASSESSMENT: ⚠️ NEEDS IMPROVEMENT

Critical Issues: 3 (ES5 compliance violations)
High Priority: 5 (Missing NULL checks)
Medium Priority: 8 (Performance optimizations)
Low Priority: 2 (Code quality)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Issue Details

```text

🔴 CRITICAL: Arrow Function Usage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Category: ES5 Compliance
Impact: Runtime error in IPA (arrow functions not supported)
Line: 23

Issue:
Arrow function syntax is ES6+ and will cause immediate runtime error
in IPA's ES5 JavaScript environment.

Current Code:
var filtered = items.filter(item => item.status === "Active");

Recommended Fix:
var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

Explanation:
IPA JavaScript executes in ES5 environment. Use traditional for loops
and function keyword instead of arrow functions and array methods like
.filter(), .map(), .find().

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

### Improved Code

```text

✅ IMPROVED CODE (ES5 COMPLIANT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied:

1. Converted all let/const to var
2. Replaced arrow functions with function keyword
3. Replaced template literals with string concatenation
4. Added NULL/undefined checks
5. Added floating point rounding
6. Added division by zero checks

7. Improved error handling
8. Added descriptive comments

// IPA Assign Node: Transform Import Data
// Purpose: Parse and validate import file content
// Input: ImportFile (string), FileName (string)
// Output: Processed records array

function transformImportData(importFileContent, fileName) {
    // Configuration
    var ROUND_DECIMALS = 2;
    var REQUIRED_FIELDS = ["id", "amount", "quantity"];
    
    // Input validation
    if (!importFileContent || typeof importFileContent !== "string") {
        importFileContent = "";
    }
    
    if (!fileName || typeof fileName !== "string") {
        fileName = "unknown";
    }
    
    // Initialize result arrays
    var processedRecords = [];
    var exceptions = [];
    
    // Parse input (assuming CSV format)
    var lines = importFileContent.split("\n");
    
    // Process each line
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        
        // Skip empty lines
        if (!line || line.trim() === "") {
            continue;
        }
        
        var fields = line.split(",");
        
        // Validate required fields
        if (fields.length < REQUIRED_FIELDS.length) {
            exceptions.push({
                line: i + 1,
                error: "Missing required fields"
            });
            continue;
        }
        
        // Extract and validate fields
        var id = fields[0] ? fields[0].trim() : "";
        var amountStr = fields[1] ? fields[1].trim() : "0";
        var quantityStr = fields[2] ? fields[2].trim() : "0";
        
        // Parse numeric values with validation
        var amount = parseFloat(amountStr);
        if (isNaN(amount)) {
            exceptions.push({
                line: i + 1,
                field: "amount",
                error: "Invalid numeric value: " + amountStr
            });
            continue;
        }
        
        var quantity = parseFloat(quantityStr);
        if (isNaN(quantity)) {
            exceptions.push({
                line: i + 1,
                field: "quantity",
                error: "Invalid numeric value: " + quantityStr
            });
            continue;
        }
        
        // Division by zero check
        var unitPrice = 0;
        if (quantity === 0) {
            exceptions.push({
                line: i + 1,
                error: "Quantity is zero, cannot calculate unit price"
            });
            continue;
        } else {
            unitPrice = amount / quantity;
        }
        
        // Round for safe comparison
        var roundedAmount = roundToDecimals(amount, ROUND_DECIMALS);
        
        // Build result record
        var record = {
            id: id,
            amount: roundedAmount,
            quantity: quantity,
            unitPrice: roundToDecimals(unitPrice, ROUND_DECIMALS),
            fileName: fileName,
            lineNumber: i + 1
        };
        
        processedRecords.push(record);
    }
    
    // Helper function: Round to specified decimals
    function roundToDecimals(num, decimals) {
        var multiplier = Math.pow(10, decimals);
        return Math.round(num * multiplier) / multiplier;
    }
    
    // Return results
    return {
        records: processedRecords,
        exceptions: exceptions,
        totalProcessed: processedRecords.length,
        totalErrors: exceptions.length
    };
}

// Invoke function with IPA variables
transformImportData(ImportFile, FileName);

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text

## Integration with IPA

### IPA Assign Node Structure

```javascript

// Entire script wrapped in function
function processData(inputData, configValue) {
    // Configuration variables INSIDE function
    var MAX_RECORDS = 1000;
    var DELIMITER = ",";
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing logic
    var results = [];
    // ... transformation ...
    
    return results;
}

// Function invocation at end (NO top-level return)
processData(InputVariable, ConfigVariable);

```text

### Global Variables (Start Node)

**CRITICAL**: Start node global variables are defined in the **Properties** tab, NOT as JavaScript code.

```text

Start Node Properties (NOT JavaScript):
queryID = ""
auth = ""
rowCount = 0
accessTokenResp = ""
OutputRecords = ""
offset = 0
limit = 1000

```text

These become global variables accessible throughout the process. No `var` keyword needed in Properties tab.

### Common IPA Patterns

**Pattern: Accumulator Loop**

```javascript

var allRecords = [];
var hasMoreData = true;
var offset = 0;
var limit = 1000;

while (hasMoreData) {
    // Fetch page of data
    var pageData = fetchData(offset, limit);
    
    // Append to accumulator
    allRecords = allRecords.concat(pageData);
    
    // Check if more data exists
    hasMoreData = (pageData.length === limit);
    offset += limit;
}

```text

**Pattern: Error Collection**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    try {
        processRecord(records[i]);
    } catch (e) {
        exceptions.push({
            record: i,
            error: e.message || "Unknown error"
        });
    }
}

```text

## Advanced Features

### Code Complexity Scoring

- **Simple**: Single loop, basic operations, < 50 lines
- **Medium**: Multiple loops, conditionals, 50-150 lines
- **Complex**: Nested loops, complex logic, 150-300 lines
- **Very Complex**: Deep nesting, multiple functions, > 300 lines

### Performance Estimation

- **Fast**: O(n) complexity, simple operations
- **Moderate**: O(n²) complexity, string operations
- **Slow**: O(n³) complexity, nested loops
- **Very Slow**: Exponential complexity, inefficient algorithms

### Production Readiness Score

Based on:

- NULL/undefined handling (30%)
- Error handling (25%)
- Edge case coverage (20%)
- Type validation (15%)
- Code quality (10%)

## Usage Examples

### Example 1: Quick Question

```text

User: How do I convert an array to uppercase in ES5?

Skill: In ES5, you need to use a for loop instead of .map():

var items = ["apple", "banana", "cherry"];
var uppercased = [];
for (var i = 0; i < items.length; i++) {
    uppercased.push(items[i].toUpperCase());
}
// Result: ["APPLE", "BANANA", "CHERRY"]

```text

### Example 2: Code Review (Pasted)

```text

User: Review this:
let items = data.filter(x => x.status === "Active");

Skill: [Identifies ES6 violations: let, arrow function, .filter()]
[Provides ES5-compliant alternative with for loop]

```text

### Example 3: Code Generation

```text

User: I need JavaScript to:

1. Parse CSV input
2. Validate required fields (id, amount, quantity)
3. Calculate unit price (amount / quantity)
4. Handle division by zero
5. Collect errors

Skill: [Generates complete ES5-compliant code with:

- Input validation
- CSV parsing
- Field validation
- Safe division
- Error collection
- Proper IPA Assign node structure]

```text

### Example 4: Troubleshooting

```text

User: This code fails with "unexpected token" on line 15:
const MAX_ITEMS = 100;

Skill: The error is caused by ES6 'const' keyword. IPA uses ES5 environment.

Fix:
var MAX_ITEMS = 100;

ES5 doesn't support 'const' or 'let'. Always use 'var' for all variable declarations.

```text

### Example 5: Optimization

```text

User: This code is slow, can you optimize it?
[Shows nested loop code]

Skill: [Analyzes O(n²) complexity]
[Provides O(n) solution using lookup map]
[Explains performance improvement]

```text

### Example 6: Learning

```text

User: Explain IPA Assign node structure

Skill: [Provides detailed explanation with example]
[Shows function wrapper pattern]
[Explains configuration placement]
[Demonstrates function invocation]

```text

## Code Generation Capabilities

### Data Transformation

**Request:**

```text

Transform JSON array to CSV format with specific columns

```text

**Generates:**

- Input validation
- JSON parsing
- Field extraction
- CSV formatting
- Error handling
- ES5-compliant code

### Validation Routines

**Request:**

```text

Validate order data: required fields, numeric amounts, date formats

```text

**Generates:**

- Field presence checks
- Type validation
- Format validation
- Error collection
- Descriptive error messages

### API Response Processing

**Request:**

```text

Parse Compass API response, extract records, handle pagination

```text

**Generates:**

- JSON parsing
- NULL safety
- Array handling
- Pagination logic
- Error handling

### File Processing

**Request:**

```text

Read CSV file, parse lines, validate data, transform to JSON

```text

**Generates:**

- File content validation
- Line-by-line parsing
- Field extraction
- Data transformation
- Error collection

### Calculation Logic

**Request:**

```text

Calculate totals, subtotals, tax, with rounding and validation

```text

**Generates:**

- Safe numeric parsing
- Floating point rounding
- Division by zero checks
- Accumulation logic
- Result formatting

### Error Handling Patterns

**Request:**

```text

Collect errors during processing, categorize by severity

```text

**Generates:**

- Try-catch blocks
- Error collection array
- Error categorization
- Descriptive messages
- Error summary

## Tips for Best Results

1. **Be Specific**: Describe requirements clearly
2. **Provide Context**: Mention node type, data source, expected output
3. **Share Errors**: Include full error messages
4. **Show Examples**: Provide sample input/output data
5. **Ask Questions**: No question is too basic
6. **Request Explanations**: Ask "why" for better understanding

## Quick Reference - Common Questions

### Variables & Declarations

**Q: How do I declare variables in ES5?**

```javascript

var name = "John";
var count = 0;
var isActive = true;

```text

**Q: Can I use let or const?**
No. IPA uses ES5 environment. Always use `var`.

### Arrays

**Q: How do I loop through an array?**

```javascript

for (var i = 0; i < items.length; i++) {
    var item = items[i];
    // Process item
}

```text

**Q: How do I filter an array?**

```javascript

var filtered = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        filtered.push(items[i]);
    }
}

```text

**Q: How do I map an array?**

```javascript

var mapped = [];
for (var i = 0; i < items.length; i++) {
    mapped.push(items[i].value * 2);
}

```text

### Strings

**Q: How do I concatenate strings?**

```javascript

var message = "Hello " + name + ", you have " + count + " items";

```text

**Q: Can I use template literals?**
No. Use string concatenation with `+` operator.

**Q: How do I check if string contains substring?**

```javascript

if (str.indexOf("substring") !== -1) {
    // Found
}

```text

### Functions

**Q: How do I write a function?**

```javascript

function calculateTotal(items) {
    var total = 0;
    for (var i = 0; i < items.length; i++) {
        total += items[i].amount;
    }
    return total;
}

```text

**Q: Can I use arrow functions?**
No. Always use `function` keyword.

### NULL Safety

**Q: How do I check for NULL/undefined?**

```javascript

if (!value || typeof value !== "string") {
    value = "";  // Default
}

```text

**Q: How do I safely access object properties?**

```javascript

var name = "";
if (person && typeof person === "object") {
    name = person.firstName || "";
}

```text

### Numbers

**Q: How do I parse numbers safely?**

```javascript

var num = parseFloat(input);
if (isNaN(num)) {
    num = 0;  // Default
}

```text

**Q: How do I compare floating point numbers?**

```javascript

function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var rounded = roundToDecimals(0.1 + 0.2, 2);
if (rounded === 0.3) {
    // Safe comparison
}

```text

**Q: How do I check for division by zero?**

```javascript

if (denominator === 0) {
    // Handle error
    return;
}
var result = numerator / denominator;

```text

### IPA-Specific

**Q: What's the IPA Assign node structure?**

```javascript

function processData(inputData) {
    // Configuration
    var MAX_RECORDS = 1000;
    
    // Validation
    if (!inputData) {
        inputData = "";
    }
    
    // Processing
    var results = [];
    // ... logic ...
    
    return results;
}

// Invoke function
processData(InputVariable);

```text

**Q: How do I define global variables?**
Define them in Start node Properties tab (NOT JavaScript):

```text

queryID = ""
rowCount = 0
offset = 0

```text

**Q: How do I collect errors?**

```javascript

var exceptions = [];

for (var i = 0; i < records.length; i++) {
    if (!records[i].id) {
        exceptions.push({
            record: i,
            error: "Missing ID"
        });
        continue;
    }
}

```text

### Debugging

**Q: "unexpected token" error - what does it mean?**
Usually ES6+ syntax in ES5 environment. Check for:

- `let`/`const` (use `var`)
- Arrow functions `=>` (use `function`)
- Template literals `` `${}` `` (use `+`)

**Q: "Cannot read property of undefined" - how to fix?**
Add NULL checks:

```javascript

if (obj && obj.property) {
    // Safe to access
}

```text

**Q: Code works in browser but fails in IPA - why?**
Browser supports ES6+, IPA uses ES5. Convert modern syntax to ES5.

## Limitations

This skill analyzes JavaScript syntax and patterns but cannot:

- Execute code in IPA environment
- Access IPA global variables
- Test against live data
- Validate IPA-specific functions
- Measure actual execution time

For live validation, test in IPA Designer.

## Version History

- **1.2.0** (2026-03-09): Added real-world performance scenarios and optimization best practices
  - Real-world Scenario 1: Compass API pagination (50x speedup)
  - Real-world Scenario 2: File processing with validation
  - Real-world Scenario 3: Nested loop optimization (833x speedup)
  - Performance optimization checklist (memory, speed, space)
  - Performance measurement tips
- **1.1.0** (2026-03-09): Added string concatenation performance pattern
  - New Pattern 10: String Concatenation in Loops (O(n²) vs O(n) complexity)
  - Performance comparison table (50-500x speedup for large datasets)
  - Pagination loop optimization guidance
  - Array accumulation pattern for data aggregation
- **1.0.0** (2026-03-09): Initial release with comprehensive ES5 analysis
