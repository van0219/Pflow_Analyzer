# IPA JavaScript Best Practices

## Production Safety Patterns

### 1. Floating Point Comparison

**Problem**: Direct comparison of floating point numbers is unreliable.

**Bad:**
```javascript
var sumQty = 0.1 + 0.2;  // Actually 0.30000000000000004
if (sumQty === 0.3) {
    // May not execute
}
```

**Good:**
```javascript
function roundToDecimals(num, decimals) {
    var multiplier = Math.pow(10, decimals);
    return Math.round(num * multiplier) / multiplier;
}

var sumQty = 0.1 + 0.2;
var roundedSum = roundToDecimals(sumQty, 2);
if (roundedSum === 0.3) {
    // Reliable comparison
}
```

### 2. NULL/Undefined Guards

**Problem**: Operations on NULL/undefined cause runtime errors.

**Bad:**
```javascript
var total = parseFloat(amount);
if (total === 0) {
    // Fails if amount is NULL/undefined
}
```

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
```

### 3. Division by Zero

**Problem**: Division by zero returns Infinity or NaN.

**Bad:**
```javascript
var unitCost = extendedAmount / originalQuantity;
```

**Good:**
```javascript
if (originalQuantity === 0) {
    exceptions.push({error: "Division by zero"});
    continue;
}
var unitCost = extendedAmount / originalQuantity;
```

### 4. Array Bounds Checking

**Problem**: Accessing array index out of bounds returns undefined.

**Bad:**
```javascript
var firstItem = items[0];
var value = firstItem.property;  // Error if items is empty
```

**Good:**
```javascript
if (!items || items.length === 0) {
    // Handle empty array
    return;
}
var firstItem = items[0];
var value = firstItem.property;
```

### 5. Type Validation

**Problem**: Operations on wrong types cause errors.

**Bad:**
```javascript
var result = value.toUpperCase();  // Error if value is not string
```

**Good:**
```javascript
if (typeof value !== "string") {
    value = String(value);
}
var result = value.toUpperCase();
```

### 6. Safe parseInt/parseFloat

**Problem**: parseInt/parseFloat return NaN for invalid input.

**Bad:**
```javascript
var num = parseInt(input);
var result = num + 10;  // NaN + 10 = NaN
```

**Good:**
```javascript
var num = parseInt(input, 10);
if (isNaN(num)) {
    num = 0;  // Default value
}
var result = num + 10;
```

### 7. Empty String Checks

**Problem**: Empty strings can cause logic errors.

**Bad:**
```javascript
if (status) {
    // Executes for empty string ""
}
```

**Good:**
```javascript
if (status && status !== "") {
    // Only executes for non-empty strings
}

// Or more defensive:
if (status && typeof status === "string" && status.trim() !== "") {
    // Robust check
}
```

### 8. Object Property Access

**Problem**: Accessing properties on NULL/undefined causes errors.

**Bad:**
```javascript
var name = person.firstName;  // Error if person is NULL
```

**Good:**
```javascript
var name = "";
if (person && typeof person === "object") {
    name = person.firstName || "";
}
```

## IPA-Specific Patterns

### 1. Assign Node Structure

**Required Pattern:**
```javascript
function transformData(inputData, fileName) {
    // Configuration variables INSIDE function
    var CONFIG_VALUE = "setting";
    var MAX_RECORDS = 1000;
    
    // Input validation
    if (!inputData || typeof inputData !== "string") {
        inputData = "";
    }
    
    // Processing logic
    var results = [];
    // ... transformation ...
    
    return results;
}

// Function invocation at end (NO top-level return)
transformData(ImportFile, FileName);
```

**Key Rules:**
- Entire script wrapped in function
- Configuration variables inside function
- No top-level return statements
- Function invoked at end with IPA variables

### 2. Start Node Global Variables

**CRITICAL**: Start node variables are defined in Properties tab, NOT as JavaScript.

**Properties Tab (NOT JavaScript):**
```
queryID = ""
auth = ""
rowCount = 0
tempCount = 0
accessTokenResp = ""
OutputRecords = ""
offset = 0
limit = 1000
```

**Common Mistake:**
```javascript
// WRONG - Don't define globals in Start node JavaScript
var queryID = "";
var auth = "";
```

These properties automatically become global variables accessible throughout the process.

### 3. Error Collection Pattern

**Pattern:**
```javascript
var exceptions = [];

for (var i = 0; i < records.length; i++) {
    try {
        // Validation
        if (!records[i].id) {
            exceptions.push({
                record: i,
                field: "id",
                error: "Missing required field"
            });
            continue;
        }
        
        // Processing
        processRecord(records[i]);
        
    } catch (e) {
        exceptions.push({
            record: i,
            error: e.message || "Unknown error"
        });
    }
}

// Return or store exceptions for error handling
return {
    processed: records.length - exceptions.length,
    errors: exceptions
};
```

### 4. Pagination Loop Pattern

**Pattern:**
```javascript
var allRecords = [];
var hasMoreData = true;
var offset = 0;
var limit = 1000;

while (hasMoreData) {
    // Fetch page of data (via WebRun or other source)
    var pageData = fetchDataPage(offset, limit);
    
    // Validate response
    if (!pageData || !Array.isArray(pageData)) {
        hasMoreData = false;
        break;
    }
    
    // Append to accumulator
    allRecords = allRecords.concat(pageData);
    
    // Check if more data exists
    hasMoreData = (pageData.length === limit);
    offset += limit;
    
    // Safety: Prevent infinite loops
    if (offset > 1000000) {
        break;
    }
}
```

### 5. Configuration at Top

**Pattern:**
```javascript
function processData(input) {
    // Configuration section at top
    var ROUND_DECIMALS = 2;
    var MAX_RECORDS = 10000;
    var REQUIRED_FIELDS = ["id", "amount", "date"];
    var DEFAULT_STATUS = "Pending";
    var ERROR_THRESHOLD = 0.05;  // 5% error rate
    
    // Processing logic below
    // ...
}
```

**Benefits:**
- Easy to modify settings
- Clear separation of config and logic
- Maintainable code

## Performance Optimization

### 1. Avoid Nested Loops

**Bad (O(n²)):**
```javascript
for (var i = 0; i < items.length; i++) {
    for (var j = 0; j < categories.length; j++) {
        if (items[i].category === categories[j].id) {
            // Match found
        }
    }
}
```

**Good (O(n)):**
```javascript
// Build lookup map first
var categoryMap = {};
for (var i = 0; i < categories.length; i++) {
    categoryMap[categories[i].id] = categories[i];
}

// Single loop with O(1) lookup
for (var i = 0; i < items.length; i++) {
    var category = categoryMap[items[i].category];
    if (category) {
        // Match found
    }
}
```

### 2. String Concatenation in Loops

**Bad:**
```javascript
var result = "";
for (var i = 0; i < items.length; i++) {
    result += items[i] + ",";  // Creates new string each iteration
}
```

**Good:**
```javascript
var parts = [];
for (var i = 0; i < items.length; i++) {
    parts.push(items[i]);
}
var result = parts.join(",");  // Single concatenation
```

### 3. Cache Array Length

**Bad:**
```javascript
for (var i = 0; i < items.length; i++) {
    // items.length evaluated every iteration
}
```

**Good:**
```javascript
for (var i = 0, len = items.length; i < len; i++) {
    // Length cached
}
```

### 4. Avoid Redundant Calculations

**Bad:**
```javascript
for (var i = 0; i < items.length; i++) {
    var taxRate = getTaxRate();  // Called every iteration
    var tax = items[i].amount * taxRate;
}
```

**Good:**
```javascript
var taxRate = getTaxRate();  // Called once
for (var i = 0; i < items.length; i++) {
    var tax = items[i].amount * taxRate;
}
```

## Code Quality

### 1. Meaningful Variable Names

**Bad:**
```javascript
var x = 100;
var y = x * 0.05;
var z = x + y;
```

**Good:**
```javascript
var orderAmount = 100;
var taxAmount = orderAmount * 0.05;
var totalAmount = orderAmount + taxAmount;
```

### 2. Comments for Complex Logic

**Bad:**
```javascript
var r = a * Math.pow(1 + b, c);
```

**Good:**
```javascript
// Calculate compound interest: Principal * (1 + rate)^periods
var futureValue = principal * Math.pow(1 + interestRate, periods);
```

### 3. Function Modularity

**Bad:**
```javascript
function processEverything(data) {
    // 500 lines of code doing everything
}
```

**Good:**
```javascript
function processData(data) {
    var validated = validateData(data);
    var transformed = transformData(validated);
    var enriched = enrichData(transformed);
    return enriched;
}

function validateData(data) {
    // Focused validation logic
}

function transformData(data) {
    // Focused transformation logic
}

function enrichData(data) {
    // Focused enrichment logic
}
```

### 4. Consistent Naming Conventions

**Pattern:**
```javascript
// Variables: camelCase
var firstName = "John";
var orderTotal = 100;

// Constants: UPPER_SNAKE_CASE
var MAX_RECORDS = 1000;
var DEFAULT_STATUS = "Pending";

// Functions: camelCase, verb-based
function calculateTotal(items) {
    // ...
}

function validateInput(data) {
    // ...
}
```

### 5. Error Messages

**Bad:**
```javascript
throw new Error("Error");
```

**Good:**
```javascript
throw new Error("Invalid order amount: expected positive number, got " + amount);
```

## Testing Patterns

### 1. Edge Case Testing

**Test Cases:**
```javascript
// Test with empty input
var result1 = processData("");

// Test with NULL
var result2 = processData(null);

// Test with undefined
var result3 = processData(undefined);

// Test with zero
var result4 = processData("0");

// Test with negative
var result5 = processData("-100");

// Test with very large number
var result6 = processData("999999999");

// Test with special characters
var result7 = processData("!@#$%");
```

### 2. Boundary Testing

**Test Cases:**
```javascript
// Test array boundaries
var emptyArray = [];
var singleItem = [1];
var maxItems = new Array(10000);

// Test string boundaries
var emptyString = "";
var singleChar = "a";
var longString = new Array(10001).join("x");

// Test numeric boundaries
var zero = 0;
var negative = -1;
var maxInt = 2147483647;
var minInt = -2147483648;
```

## Common Anti-Patterns to Avoid

### 1. Magic Numbers

**Bad:**
```javascript
if (status === 2) {
    // What does 2 mean?
}
```

**Good:**
```javascript
var STATUS_ACTIVE = 2;
if (status === STATUS_ACTIVE) {
    // Clear meaning
}
```

### 2. Deep Nesting

**Bad:**
```javascript
if (condition1) {
    if (condition2) {
        if (condition3) {
            if (condition4) {
                // Code buried 4 levels deep
            }
        }
    }
}
```

**Good:**
```javascript
if (!condition1) return;
if (!condition2) return;
if (!condition3) return;
if (!condition4) return;

// Code at top level
```

### 3. Modifying Loop Variable

**Bad:**
```javascript
for (var i = 0; i < items.length; i++) {
    if (condition) {
        i++;  // Skips items unpredictably
    }
}
```

**Good:**
```javascript
for (var i = 0; i < items.length; i++) {
    if (condition) {
        continue;  // Skip this iteration
    }
}
```

### 4. Implicit Type Coercion

**Bad:**
```javascript
if (value == "0") {
    // Matches 0, "0", false, etc.
}
```

**Good:**
```javascript
if (value === "0") {
    // Only matches string "0"
}
```

