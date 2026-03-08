# Compass SQL Analysis Rules

Comprehensive ruleset for analyzing Compass SQL queries across 6 dimensions.

## Table of Contents

- [Syntax Validation Rules](#syntax-validation-rules)
- [Performance Analysis Rules](#performance-analysis-rules)
- [Durability Assessment Rules](#durability-assessment-rules)
- [Flexibility Review Rules](#flexibility-review-rules)
- [Best Practices Rules](#best-practices-rules)
- [Code Quality Rules](#code-quality-rules)

## Syntax Validation Rules

### Rule S1: No DML/DDL Statements

**Severity**: Critical  
**Category**: Syntax

**Check**: Query contains INSERT, UPDATE, DELETE, CREATE, ALTER, DROP

**Rationale**: Compass SQL is read-only. DML/DDL statements will fail.

**Fix**: Remove DML/DDL statements. Use Compass API for read operations only.

**Example**:
```sql
-- ❌ BAD
INSERT INTO Orders VALUES (1, '2024-01-01', 100.00);

-- ✅ GOOD
SELECT * FROM Orders WHERE orderId = 1;
```

---

### Rule S2: Quote Problematic Names

**Severity**: High  
**Category**: Syntax

**Check**: Object/property names with spaces, hyphens, starting with numbers, or reserved words without double quotes

**Rationale**: Compass SQL requires double quotes for problematic names.

**Fix**: Add double quotes around problematic names.

**Example**:
```sql
-- ❌ BAD
SELECT Order Date, Customer-ID FROM 2024_Orders;

-- ✅ GOOD
SELECT "Order Date", "Customer-ID" FROM "2024_Orders";
```

---

### Rule S3: Valid CAST Types

**Severity**: Critical  
**Category**: Syntax

**Check**: CAST uses unsupported types

**Supported Types**: varchar, date, datetime, datetime2, decimal, integer, bigint

**Fix**: Use supported CAST types only.

**Example**:
```sql
-- ❌ BAD
SELECT CAST(amount AS money) FROM Orders;

-- ✅ GOOD
SELECT CAST(amount AS decimal) FROM Orders;
```

---

### Rule S4: Proper JOIN Syntax

**Severity**: Critical  
**Category**: Syntax

**Check**: JOIN without ON clause, invalid JOIN type

**Fix**: Use proper JOIN syntax with ON conditions.

**Example**:
```sql
-- ❌ BAD
SELECT * FROM Orders o, Customers c WHERE o.customerId = c.customerId;

-- ✅ GOOD
SELECT * FROM Orders o
INNER JOIN Customers c ON o.customerId = c.customerId;
```

---

### Rule S5: Reserved Word Conflicts

**Severity**: High  
**Category**: Syntax

**Check**: Unquoted reserved words (SELECT, FROM, WHERE, etc.) used as names

**Fix**: Quote reserved words with double quotes.

**Example**:
```sql
-- ❌ BAD
SELECT SELECT, FROM FROM Orders;

-- ✅ GOOD
SELECT "SELECT", "FROM" FROM Orders;
```

---

## Performance Analysis Rules

### Rule P1: Result Limiting and API Pagination Required

**Severity**: Critical  
**Category**: Performance, Durability

**Check**: Query lacks result limiting or Compass API pagination on tables with > 10K rows

**Rationale**: Unbounded queries cause timeouts and memory issues. OFFSET is NOT supported in Compass SQL syntax.

**Fix**: Use SELECT TOP or SELECT LIMIT for result limiting. Implement Compass API pagination with offset/limit query parameters.

**Example**:
```sql
-- ❌ BAD: No result limiting
SELECT * FROM LargeTable ORDER BY id;

-- ✅ GOOD: Result limiting in SQL
SELECT TOP 100000 * FROM LargeTable ORDER BY id;

-- ✅ BEST: Compass API pagination
-- SQL Query (no OFFSET in SQL):
SELECT * FROM LargeTable ORDER BY id;

-- IPA Implementation (Compass API):
-- 1. POST /jobs/ with SQL query
-- 2. GET /jobs/{queryId}/status/ until FINISHED
-- 3. GET /jobs/{queryId}/result/?offset=0&limit=100000
-- 4. GET /jobs/{queryId}/result/?offset=100000&limit=100000
-- 5. Continue until no more data
```

---

### Rule P2: CAST in WHERE with NULL Check

**Severity**: High  
**Category**: Performance, Correctness

**Check**: CAST in WHERE clause without NULL check

**Rationale**: CAST returns NULL on failure. Missing NULL check causes incorrect results.

**Fix**: Add NULL check after CAST.

**Example**:
```sql
-- ❌ BAD
SELECT * FROM Orders
WHERE CAST(orderDate AS date) > '2024-01-01';

-- ✅ GOOD
SELECT * FROM Orders
WHERE CAST(orderDate AS date) IS NOT NULL
  AND CAST(orderDate AS date) > '2024-01-01';
```

---

### Rule P3: Avoid Cartesian Products

**Severity**: Critical  
**Category**: Performance

**Check**: CROSS JOIN or missing JOIN condition

**Rationale**: Cartesian products cause exponential row growth and timeouts.

**Fix**: Use proper JOIN with ON condition.

**Example**:
```sql
-- ❌ BAD
SELECT * FROM Orders o
CROSS JOIN Customers c
WHERE o.customerId = c.customerId;

-- ✅ GOOD
SELECT * FROM Orders o
INNER JOIN Customers c ON o.customerId = c.customerId;
```

---

### Rule P4: Selective WHERE Clauses

**Severity**: High  
**Category**: Performance

**Check**: WHERE clause filters < 10% of rows

**Rationale**: Non-selective filters scan entire table.

**Fix**: Add more selective filters (dates, status, IDs).

**Example**:
```sql
-- ❌ BAD (filters 90% of rows)
SELECT * FROM Orders WHERE status <> 'Cancelled';

-- ✅ GOOD (filters to specific date range)
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'
  AND orderDate < '2024-02-01'
  AND status = 'Active';
```

---

### Rule P5: Efficient JOIN Order

**Severity**: Medium  
**Category**: Performance

**Check**: Large table joined before small table

**Rationale**: JOIN order affects performance. Join smaller tables first.

**Fix**: Reorder JOINs to start with smallest table.

**Example**:
```sql
-- ❌ BAD (large table first)
SELECT * FROM Orders o  -- 10M rows
INNER JOIN Customers c ON o.customerId = c.customerId  -- 100K rows
INNER JOIN Products p ON o.productId = p.productId;  -- 1K rows

-- ✅ GOOD (small table first)
SELECT * FROM Products p  -- 1K rows
INNER JOIN Orders o ON p.productId = o.productId  -- 10M rows
INNER JOIN Customers c ON o.customerId = c.customerId;  -- 100K rows
```

---

### Rule P6: Redundant DISTINCT

**Severity**: Medium  
**Category**: Performance

**Check**: DISTINCT used when not needed (unique key in SELECT)

**Rationale**: DISTINCT adds sorting overhead.

**Fix**: Remove DISTINCT if results are already unique.

**Example**:
```sql
-- ❌ BAD (orderId is unique)
SELECT DISTINCT orderId, orderDate FROM Orders;

-- ✅ GOOD
SELECT orderId, orderDate FROM Orders;
```

---

## Durability Assessment Rules

### Rule D1: Timeout Protection

**Severity**: Critical  
**Category**: Durability

**Check**: Query estimated to exceed 60-minute timeout

**Rationale**: Compass SQL has 60-minute query timeout.

**Fix**: Add pagination, reduce scope, or split into multiple queries.

**Example**:
```sql
-- ❌ BAD (scans 100M rows)
SELECT * FROM HugeTable;

-- ✅ GOOD (paginated)
SELECT TOP 10000 * FROM HugeTable
ORDER BY id;
-- Or use Compass API pagination for larger datasets
```

---

### Rule D2: Bounded Result Sets

**Severity**: High  
**Category**: Durability

**Check**: Query returns > 100K rows without pagination

**Rationale**: Large result sets cause memory issues and slow processing.

**Fix**: Add LIMIT or filter to reduce result size.

**Example**:
```sql
-- ❌ BAD (returns millions of rows)
SELECT * FROM TransactionHistory;

-- ✅ GOOD (bounded to 1000 rows)
SELECT * FROM TransactionHistory
WHERE transDate >= '2024-01-01'
LIMIT 1000;
```

---

### Rule D3: Scalable Aggregations

**Severity**: High  
**Category**: Durability

**Check**: Aggregation without GROUP BY on large tables

**Rationale**: Full table aggregations are slow on large datasets.

**Fix**: Add GROUP BY or filter to reduce aggregation scope.

**Example**:
```sql
-- ❌ BAD (aggregates 10M rows)
SELECT COUNT(*), SUM(amount) FROM Orders;

-- ✅ GOOD (aggregates by month)
SELECT 
  DATE_TRUNC('month', orderDate) AS month,
  COUNT(*) AS order_count,
  SUM(amount) AS total_amount
FROM Orders
WHERE orderDate >= '2024-01-01'
GROUP BY DATE_TRUNC('month', orderDate);
```

---

### Rule D4: Memory-Intensive Operations

**Severity**: High  
**Category**: Durability

**Check**: Large IN clauses (> 1000 values), multiple CTEs, complex subqueries

**Rationale**: Memory-intensive operations can cause failures on large datasets.

**Fix**: Simplify query, use JOINs instead of IN, limit CTE complexity.

**Example**:
```sql
-- ❌ BAD (large IN clause)
SELECT * FROM Orders
WHERE customerId IN (1, 2, 3, ..., 5000);

-- ✅ GOOD (use JOIN)
SELECT o.* FROM Orders o
INNER JOIN CustomerList cl ON o.customerId = cl.customerId;
```

---

## Flexibility Review Rules

### Rule F1: Parameterize Hardcoded Values

**Severity**: High  
**Category**: Flexibility

**Check**: Hardcoded dates, IDs, status values, limits

**Rationale**: Hardcoded values reduce reusability and require code changes.

**Fix**: Replace with parameters (? placeholders for IPA variables).

**Example**:
```sql
-- ❌ BAD (hardcoded)
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'
  AND status = 'Active'
LIMIT 1000;

-- ✅ GOOD (parameterized)
SELECT * FROM Orders
WHERE orderDate >= ?  -- Parameter: startDate
  AND status = ?      -- Parameter: statusFilter
LIMIT ?;              -- Parameter: pageSize
```

---

### Rule F2: Environment-Agnostic Names

**Severity**: Medium  
**Category**: Flexibility

**Check**: Environment-specific object names (DEV_, PROD_, TEST_)

**Rationale**: Environment-specific names break portability.

**Fix**: Use generic names, configure environment externally.

**Example**:
```sql
-- ❌ BAD (environment-specific)
SELECT * FROM PROD_Orders;

-- ✅ GOOD (generic)
SELECT * FROM Orders;  -- Configure schema/prefix externally
```

---

### Rule F3: Configuration Externalization

**Severity**: Medium  
**Category**: Flexibility

**Check**: Magic numbers, hardcoded limits, business rules in SQL

**Rationale**: Configuration in SQL requires code changes.

**Fix**: Move configuration to IPA variables or config files.

**Example**:
```sql
-- ❌ BAD (magic numbers)
SELECT * FROM Orders
WHERE amount > 1000  -- What is 1000?
LIMIT 500;           -- Why 500?

-- ✅ GOOD (documented parameters)
SELECT * FROM Orders
WHERE amount > ?  -- Parameter: minAmount (default: 1000)
LIMIT ?;          -- Parameter: pageSize (default: 500)
```

---

### Rule F4: Reusable Query Structure

**Severity**: Medium  
**Category**: Flexibility

**Check**: Query structure is brittle, tightly coupled to specific use case

**Rationale**: Reusable queries reduce maintenance and duplication.

**Fix**: Generalize query structure, use CTEs for modularity.

**Example**:
```sql
-- ❌ BAD (specific use case)
SELECT orderId, orderDate, amount
FROM Orders
WHERE customerId = 12345
  AND orderDate = '2024-01-15';

-- ✅ GOOD (reusable)
WITH FilteredOrders AS (
  SELECT orderId, orderDate, amount, customerId
  FROM Orders
  WHERE orderDate >= ?  -- Parameter: startDate
    AND orderDate < ?   -- Parameter: endDate
)
SELECT * FROM FilteredOrders
WHERE customerId = ?;   -- Parameter: customerId
```

---

## Best Practices Rules

### Rule B1: NULL Safety After CAST

**Severity**: High  
**Category**: Best Practices, Correctness

**Check**: CAST without NULL check or COALESCE

**Rationale**: CAST returns NULL on failure. Missing NULL handling causes data loss.

**Fix**: Add NULL check or COALESCE with default value.

**Example**:
```sql
-- ❌ BAD (no NULL handling)
SELECT CAST(amount AS decimal) AS amount_decimal
FROM Orders;

-- ✅ GOOD (NULL check)
SELECT CAST(amount AS decimal) AS amount_decimal
FROM Orders
WHERE CAST(amount AS decimal) IS NOT NULL;

-- ✅ GOOD (default value)
SELECT COALESCE(CAST(amount AS decimal), 0.00) AS amount_decimal
FROM Orders;
```

---

### Rule B2: Defensive Programming

**Severity**: Medium  
**Category**: Best Practices

**Check**: Missing error handling, no validation, assumes data quality

**Rationale**: Production data has quality issues. Defensive code prevents failures.

**Fix**: Add validation, NULL checks, data quality filters.

**Example**:
```sql
-- ❌ BAD (assumes data quality)
SELECT 
  orderId,
  CAST(orderDate AS date) AS order_date,
  CAST(amount AS decimal) AS amount_decimal
FROM Orders;

-- ✅ GOOD (defensive)
SELECT 
  orderId,
  CAST(orderDate AS date) AS order_date,
  CAST(amount AS decimal) AS amount_decimal
FROM Orders
WHERE orderId IS NOT NULL
  AND orderDate IS NOT NULL
  AND amount IS NOT NULL
  AND CAST(orderDate AS date) IS NOT NULL
  AND CAST(amount AS decimal) IS NOT NULL
  AND CAST(amount AS decimal) > 0;  -- Business rule validation
```

---

### Rule B3: Consistent Formatting

**Severity**: Low  
**Category**: Best Practices, Code Quality

**Check**: Inconsistent indentation, capitalization, spacing

**Rationale**: Consistent formatting improves readability and maintainability.

**Fix**: Apply consistent formatting rules.

**Example**:
```sql
-- ❌ BAD (inconsistent)
select orderId,orderDate,amount from Orders where status='Active'and orderDate>='2024-01-01'order by orderDate desc;

-- ✅ GOOD (consistent)
SELECT 
  orderId,
  orderDate,
  amount
FROM Orders
WHERE status = 'Active'
  AND orderDate >= '2024-01-01'
ORDER BY orderDate DESC;
```

---

### Rule B4: Meaningful Comments

**Severity**: Low  
**Category**: Best Practices, Code Quality

**Check**: Missing comments, unclear purpose, no documentation

**Rationale**: Comments explain intent and business logic.

**Fix**: Add comments for purpose, parameters, business rules, edge cases.

**Example**:
```sql
-- ❌ BAD (no comments)
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'
  AND status = 'Active'
LIMIT 1000;

-- ✅ GOOD (documented)
-- Purpose: Fetch active orders for monthly reporting
-- Parameters: startDate (default: first day of current month)
-- Expected Rows: 1000 per page
-- Business Rule: Only include orders with 'Active' status
SELECT 
  orderId,
  orderDate,
  amount,
  customerId
FROM Orders
WHERE orderDate >= ?  -- Parameter: startDate
  AND status = 'Active'
ORDER BY orderDate DESC;
-- Pagination: Compass API offset/limit parameters
```

---

### Rule B5: Compass SQL Idioms

**Severity**: Medium  
**Category**: Best Practices

**Check**: Non-idiomatic patterns, verbose syntax, anti-patterns

**Rationale**: Compass SQL has specific idioms for common operations.

**Fix**: Use Compass SQL idioms and patterns.

**Example**:
```sql
-- ❌ BAD (verbose)
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'
  AND orderDate < '2024-02-01'
  AND (status = 'Active' OR status = 'Pending');

-- ✅ GOOD (idiomatic)
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'
  AND orderDate < '2024-02-01'
  AND status IN ('Active', 'Pending');
```

---

## Code Quality Rules

### Rule Q1: Readable Structure

**Severity**: Low  
**Category**: Code Quality

**Check**: Long lines (> 80 chars), nested subqueries, complex expressions

**Rationale**: Readable code is maintainable code.

**Fix**: Break long lines, use CTEs for subqueries, simplify expressions.

**Example**:
```sql
-- ❌ BAD (unreadable)
SELECT o.orderId, o.orderDate, o.amount, c.customerName, c.customerEmail, p.productName, p.productCategory FROM Orders o INNER JOIN Customers c ON o.customerId = c.customerId INNER JOIN Products p ON o.productId = p.productId WHERE o.orderDate >= '2024-01-01' AND o.status = 'Active' ORDER BY o.orderDate DESC LIMIT 1000;

-- ✅ GOOD (readable)
SELECT 
  o.orderId,
  o.orderDate,
  o.amount,
  c.customerName,
  c.customerEmail,
  p.productName,
  p.productCategory
FROM Orders o
INNER JOIN Customers c ON o.customerId = c.customerId
INNER JOIN Products p ON o.productId = p.productId
WHERE o.orderDate >= '2024-01-01'
  AND o.status = 'Active'
ORDER BY o.orderDate DESC
LIMIT 1000;
```

---

### Rule Q2: Descriptive Aliases

**Severity**: Low  
**Category**: Code Quality

**Check**: Single-letter aliases, unclear abbreviations

**Rationale**: Descriptive aliases improve readability.

**Fix**: Use meaningful aliases (2-4 characters).

**Example**:
```sql
-- ❌ BAD (unclear)
SELECT a.x, b.y, c.z
FROM Orders a
INNER JOIN Customers b ON a.id = b.id
INNER JOIN Products c ON a.pid = c.pid;

-- ✅ GOOD (descriptive)
SELECT 
  ord.orderId,
  cust.customerName,
  prod.productName
FROM Orders ord
INNER JOIN Customers cust ON ord.customerId = cust.customerId
INNER JOIN Products prod ON ord.productId = prod.productId;
```

---

### Rule Q3: Modular CTEs

**Severity**: Low  
**Category**: Code Quality

**Check**: Complex query without CTEs, repeated subqueries

**Rationale**: CTEs improve modularity and reusability.

**Fix**: Extract subqueries into CTEs.

**Example**:
```sql
-- ❌ BAD (repeated subquery)
SELECT 
  (SELECT COUNT(*) FROM Orders WHERE status = 'Active') AS active_count,
  (SELECT SUM(amount) FROM Orders WHERE status = 'Active') AS active_total
FROM dual;

-- ✅ GOOD (CTE)
WITH ActiveOrders AS (
  SELECT * FROM Orders WHERE status = 'Active'
)
SELECT 
  COUNT(*) AS active_count,
  SUM(amount) AS active_total
FROM ActiveOrders;
```

---

## Rule Priority Matrix

| Severity | Impact | Action |
|----------|--------|--------|
| Critical | Correctness, Durability | MUST FIX before production |
| High | Performance, Flexibility | SHOULD FIX before production |
| Medium | Maintainability, Best Practices | RECOMMENDED to fix |
| Low | Code Quality | OPTIONAL improvement |

## Analysis Workflow

1. **Parse Query**: Extract structure, identify components
2. **Apply Rules**: Check each rule against query
3. **Prioritize Issues**: Sort by severity and impact
4. **Generate Report**: Format findings with examples
5. **Provide Fixes**: Refactor query with improvements
6. **Validate**: Ensure fixes don't introduce new issues

## Custom Rules

Projects can define custom rules in `.kiro/steering/` files:

```markdown
## Custom Compass SQL Rules

### Rule C1: Company-Specific Naming

All queries must use company-specific prefixes:
- Tables: `COMP_TableName`
- Columns: `comp_column_name`
```

These custom rules are automatically included in analysis.
