---
name: "compass-sql-analyzer"
description: "Analyze Compass SQL queries for syntax, performance, durability, and flexibility. Provides recommendations and improved code. Use when reviewing SQL queries, optimizing performance, or validating Compass SQL compliance."
---

# Compass SQL Analyzer

Comprehensive analysis tool for Compass SQL queries with focus on syntax validation, performance optimization, durability for large datasets, and code flexibility.

## What This Skill Does

Analyzes Compass SQL queries and provides:

1. **Syntax Validation** - Compass SQL compliance, reserved words, quoting rules
2. **Performance Analysis** - Pagination, indexing hints, JOIN optimization, CAST usage
3. **Durability Assessment** - Handling datasets from 1K to millions of rows
4. **Flexibility Review** - Parameterization, reusability, maintainability
5. **Best Practices** - Compass SQL patterns, error handling, NULL safety
6. **Code Improvements** - Refactored queries with explanations

## When to Use

- Reviewing SQL queries before deployment
- Optimizing slow-running queries
- Validating Compass SQL syntax compliance
- Ensuring queries scale from small to large datasets
- Preparing queries for production use
- Code review and quality assurance
- Troubleshooting query failures

## Analysis Workflow

### Step 1: Query Input

**For short queries** (< 50 lines):
- Paste directly in chat

**For long queries** (> 50 lines):
- Save to `Temp/query_to_analyze.sql`
- Reference file path in chat

### Step 2: Automated Analysis

The skill performs comprehensive analysis across 6 dimensions:

1. **Syntax Validation**
   - Compass SQL compliance (no DML/DDL)
   - Object/property naming rules
   - Quote usage (double quotes for problematic names)
   - Reserved word conflicts
   - CAST/CONVERT syntax

2. **Performance Analysis**
   - Result limiting strategy (context-dependent)
   - Pagination strategy (Compass API offset/limit parameters for IPA)
   - JOIN efficiency (order, type, conditions)
   - CAST placement (WHERE vs SELECT)
   - Subquery optimization
   - Aggregation efficiency

3. **Durability Assessment**
   - Timeout risk (60-minute limit)
   - Memory usage patterns
   - Scalability from 1K to millions of rows
   - Result set size management
   - API pagination compliance

4. **Flexibility Review**
   - Hardcoded values vs parameters
   - Reusability across environments
   - Maintainability (comments, structure)
   - Error handling (NULL checks)
   - Configuration externalization

5. **Best Practices**
   - NULL safety after CAST
   - Defensive programming patterns
   - Compass SQL idioms
   - Common anti-patterns
   - Production readiness

6. **Code Quality**
   - Readability (formatting, indentation)
   - Naming conventions
   - Comment quality
   - Modularity
   - Documentation

### Step 3: Recommendations

For each issue found, provides:

- **Severity**: Critical / High / Medium / Low
- **Impact**: Performance / Correctness / Maintainability
- **Explanation**: Why this matters
- **Fix**: Specific code changes
- **Example**: Before/after comparison

### Step 4: Improved Code

Generates refactored query with:

- All issues fixed
- Optimizations applied
- Comments explaining changes
- Production-ready structure
- Parameterization where appropriate

## Analysis Categories

### Syntax Issues

**Critical:**
- DML/DDL statements (INSERT, UPDATE, DELETE, CREATE)
- Invalid CAST types
- Malformed JOIN syntax
- Missing required clauses

**High:**
- Unquoted problematic names (spaces, hyphens, numbers)
- Reserved word conflicts
- Case sensitivity violations
- Invalid function usage

**Medium:**
- Inconsistent quoting style
- Unclear operator precedence
- Missing table aliases

### Performance Issues

**Critical:**
- Missing WHERE clause on large tables (unbounded queries)
- Cartesian products (missing JOIN conditions)
- CAST in WHERE without NULL check
- Inefficient subqueries

**High:**
- Non-selective WHERE clauses
- Multiple CAST operations on same column
- Inefficient JOIN order
- Missing aggregation filters (HAVING)

**Medium:**
- Redundant DISTINCT
- Unnecessary sorting
- Overly complex CTEs

**Note on LIMIT clauses**: In IPA implementations, LIMIT clauses are typically NOT used in SQL queries. Pagination is handled at the Compass API level using offset/limit parameters. When reviewing user code for IPA, do NOT suggest adding LIMIT clauses.

### Durability Issues

**Critical:**
- No timeout protection (queries > 60 minutes)
- Unbounded result sets without WHERE filtering
- Memory-intensive operations without proper filtering

**High:**
- Large IN clauses (> 1000 values)
- Unoptimized aggregations on large datasets
- Missing ORDER BY for consistent pagination

**Medium:**
- No result size estimation
- Inefficient data type conversions

**Note on pagination**: In IPA implementations, pagination is handled at the Compass API level (offset/limit parameters), not with SQL LIMIT clauses. Focus on WHERE clause filtering for data reduction.

### Flexibility Issues

**High:**
- Hardcoded dates, IDs, or values
- Environment-specific object names
- No parameterization strategy
- Brittle string matching

**Medium:**
- Magic numbers without explanation
- Hardcoded LIMIT values
- No configuration externalization
- Poor reusability

## Common Patterns Analyzed

### Pattern 1: Pagination

**IMPORTANT FOR IPA IMPLEMENTATIONS:**

In IPA contexts, SQL queries typically do NOT include LIMIT clauses. Data filtering is done through WHERE, GROUP BY, and HAVING clauses. Pagination is handled at the Compass API level using offset/limit parameters in the API calls, not in the SQL query itself.

**IPA Pattern (typical - no LIMIT in SQL):**

```sql
-- SQL Query (no LIMIT clause)
SELECT * FROM LargeTable
WHERE status = 'Active'
ORDER BY id;

-- Pagination handled by Compass API in IPA WebRun loop:
-- GET /jobs/{queryId}/result/?offset=0&limit=100000
-- GET /jobs/{queryId}/result/?offset=100000&limit=100000
```

**For testing/exploration only** (not typical IPA usage):

```sql
-- Option 1: SELECT TOP (SQL Server style)
SELECT TOP 1000 * FROM LargeTable
ORDER BY id;

-- Option 2: SELECT LIMIT (Apache Spark style)
SELECT * FROM LargeTable
ORDER BY id
LIMIT 1000;

-- Note: OFFSET is NOT supported in Compass SQL
```

### Pattern 2: CAST Safety

**Bad:**
```sql
SELECT * FROM Orders
WHERE CAST(orderDate AS date) > '2024-01-01';  -- No NULL check
```

**Good:**
```sql
SELECT * FROM Orders
WHERE CAST(orderDate AS date) IS NOT NULL
  AND CAST(orderDate AS date) > '2024-01-01';
```

### Pattern 3: JOIN Optimization

**Bad:**
```sql
SELECT * FROM Orders o
CROSS JOIN Customers c  -- Cartesian product
WHERE o.customerId = c.customerId;
```

**Good:**
```sql
SELECT * FROM Orders o
INNER JOIN Customers c ON o.customerId = c.customerId;
```

### Pattern 4: Parameterization

**Bad:**
```sql
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'  -- Hardcoded
  AND status = 'Active';
```

**Good:**
```sql
-- Use IPA variables: startDate, statusFilter
SELECT * FROM Orders
WHERE orderDate >= ?  -- Parameter placeholder
  AND status = ?;
```

## Output Format

### Analysis Summary

```text
📊 COMPASS SQL ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query: [First 50 chars...]
Lines: 45
Complexity: Medium
Estimated Rows: 10K - 100K

OVERALL ASSESSMENT: ⚠️ NEEDS IMPROVEMENT

Critical Issues: 2
High Priority: 3
Medium Priority: 5
Low Priority: 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Issue Details

```text
🔴 CRITICAL: Unbounded Query Without Filtering
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Category: Durability
Impact: Query may timeout or return excessive rows
Line: 15

Issue:
Query lacks WHERE clause filtering on a large transactional table.
When querying Data Lake tables with millions of rows, this will cause:
- API timeout (60-minute limit)
- Memory exhaustion
- Slow response times

Current Code:
SELECT * FROM TransactionHistory
ORDER BY transDate DESC;

Recommended Fix:
SELECT * FROM TransactionHistory
WHERE transDate >= '2024-01-01'  -- Add filtering
ORDER BY transDate DESC;

-- Pagination handled by Compass API in IPA:
-- GET /jobs/{queryId}/result/?offset=0&limit=100000
-- GET /jobs/{queryId}/result/?offset=100000&limit=100000

Explanation:
In IPA implementations, use WHERE clauses to filter data. Pagination
is handled at the Compass API level using offset/limit parameters in
the API calls, not with SQL LIMIT clauses. Focus on reducing the
dataset through effective WHERE conditions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Improved Code

```text
✅ IMPROVED QUERY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied:
1. Added WHERE clause filtering
2. Added NULL checks after CAST
3. Parameterized hardcoded values
4. Optimized JOIN order
5. Added defensive error handling

-- Improved Compass SQL Query (IPA Context)
-- Purpose: Fetch transaction history with API-level pagination
-- Parameters: startDate
-- Pagination: Handled by Compass API offset/limit parameters
-- Expected Rows: Variable (filtered by WHERE clause)

SELECT 
  t.transactionId,
  t.transactionDate,
  CAST(t.amount AS decimal) AS amount_decimal,
  c.customerName
FROM TransactionHistory t
INNER JOIN Customers c ON t.customerId = c.customerId
WHERE CAST(t.transactionDate AS date) IS NOT NULL
  AND CAST(t.transactionDate AS date) >= '<!startDate>'  -- IPA parameter
  AND CAST(t.amount AS decimal) IS NOT NULL
ORDER BY t.transactionDate DESC;

-- IPA Implementation Notes:
-- 1. Initialize: limit = 100000, offset = 0
-- 2. Submit query via Compass API POST /jobs/
-- 3. Poll status: GET /jobs/{queryId}/status/ until FINISHED
-- 4. Loop: GET /jobs/{queryId}/result/?offset=X&limit=100000
-- 5. Increment offset by limit after each page
-- 6. Exit: When result count < limit
-- 7. Error Handling: Check for NULL after CAST operations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Integration with IPA

When analyzing SQL for IPA WebRun activities:

1. **Variable Substitution**: Identifies hardcoded values that should be IPA variables
2. **Pagination Loop**: Provides IPA JavaScript pattern for pagination
3. **Error Handling**: Suggests GetWorkUnitErrors integration
4. **Performance**: Estimates execution time and memory usage

**Example IPA Pattern:**

```javascript
// IPA Assign Node: Initialize Pagination
var limit = 1000;
var offset = 0;
var allResults = [];
var hasMoreData = true;

// IPA Branch Node: Check hasMoreData
// IPA WebRun Node: Execute query with limit/offset
// IPA Assign Node: Process results
var results = JSON.parse(WebRunResponse);
allResults = allResults.concat(results.data);
offset += limit;
hasMoreData = (results.data.length === limit);
```

## Advanced Features

### Query Complexity Scoring

- **Simple**: Single table, basic WHERE, < 10 lines
- **Medium**: JOINs, aggregations, CTEs, 10-50 lines
- **Complex**: Multiple CTEs, subqueries, > 50 lines
- **Very Complex**: Nested subqueries, UNION, > 100 lines

### Performance Estimation

- **Row Count**: Estimated based on table size and filters
- **Execution Time**: Rough estimate based on complexity
- **Memory Usage**: Based on result set size and operations
- **Timeout Risk**: Probability of exceeding 60-minute limit

### Scalability Analysis

Tests query behavior across dataset sizes:

- **1K rows**: Should complete in < 1 second
- **10K rows**: Should complete in < 5 seconds
- **100K rows**: Should complete in < 30 seconds
- **1M rows**: Requires pagination, < 5 minutes per page
- **10M+ rows**: Must use pagination, consider incremental processing

## Usage Examples

### Example 1: Quick Analysis

```text
User: Analyze this SQL:
SELECT * FROM Orders WHERE orderDate > '2024-01-01'

Kiro: [Performs analysis, identifies missing pagination and CAST]
```

### Example 2: File-Based Analysis

```text
User: Analyze Temp/complex_query.sql

Kiro: [Reads file, performs comprehensive analysis]
```

### Example 3: Performance Context

```text
User: This query is timing out on our production Data Lake. It queries GLTransaction table with millions of rows.

Kiro: [Analyzes with performance and scalability recommendations]
```

## Activation Instructions

**CRITICAL**: When this skill is activated, you MUST immediately load the Compass SQL steering file:

```
discloseContext(name="compass-sql")
```

This loads `.kiro/steering/06_Compass_SQL_CheatSheet.md` which contains comprehensive Compass SQL documentation including:

- All supported functions (string, math, aggregation, datetime, conversion, analytic)
- Complete operator reference
- Query structure and clauses
- CAST behavior and NULL handling
- Critical rules (UTC timestamps, case sensitivity, 60-minute timeout)
- Common patterns and best practices
- Limitations and constraints

**OPTIONAL**: For queries involving pagination or IPA implementation, also load:

```
discloseContext(name="data-fabric-guide")
```

This loads `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md` which contains:

- Compass API pagination (offset/limit query parameters)
- IPA WebRun implementation patterns
- Rate limits and timeouts
- Critical distinction: offset/limit are API parameters, NOT SQL syntax

**DO NOT proceed with analysis without loading the Compass SQL steering file first.**

## References

### Primary References (Load via discloseContext)

- **Compass SQL Syntax**: `.kiro/steering/06_Compass_SQL_CheatSheet.md`
  - **MUST load via**: `discloseContext(name="compass-sql")`
  - **Contains**: Complete SQL syntax, functions, operators, critical rules
  - **When to use**: Every Compass SQL analysis (REQUIRED)

- **Data Fabric Guide**: `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md`
  - **Load via**: `discloseContext(name="data-fabric-guide")`
  - **Contains**: Compass API pagination, IPA implementation patterns, rate limits, timeouts
  - **When to use**: When analyzing pagination, API integration, or IPA WebRun activities
  - **Critical for**: Understanding offset/limit are API parameters, not SQL syntax

### Skill-Specific References

- **Analysis Rules**: `references/analysis-rules.md`
- **Example Queries**: `references/example-queries.md`

### Official Documentation

- **Infor Data Fabric User Guide**: `Infor_Data_Fabric_User_Guide.pdf` (Chapter 11: Compass SQL Reference)

## Limitations

This skill analyzes SQL syntax and patterns but cannot:

- Execute queries against live Data Fabric
- Validate object/property names exist in Data Catalog
- Measure actual execution time
- Access query execution plans
- Validate data types match source schema

For live validation, use Compass Query Editor in Infor OS Portal.

## Tips for Best Results

1. **Provide Context**: Mention table sizes, expected row counts, use case
2. **Include Comments**: Existing comments help understand intent
3. **Specify Environment**: Production vs development considerations
4. **Share Errors**: Include any error messages from failed queries
5. **Mention Performance**: Note if query is slow or timing out
6. **Dataset Size**: Indicate if querying transactional tables with millions of rows

## Version History

- **1.0.0** (2026-03-08): Initial release with comprehensive analysis
