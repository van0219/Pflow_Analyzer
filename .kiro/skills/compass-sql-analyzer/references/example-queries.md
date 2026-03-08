# Compass SQL Example Queries

Real-world examples demonstrating good and bad patterns for Compass SQL queries.

## Table of Contents

- [Good Examples](#good-examples)
- [Bad Examples](#bad-examples)
- [Before/After Refactoring](#beforeafter-refactoring)
- [Performance Comparison](#performance-comparison)

## Good Examples

### Example 1: Transaction Query with API Pagination

**Use Case**: Fetch transaction history with Compass API pagination for large datasets

```sql
-- Purpose: Fetch transaction history
-- Parameters: startDate, endDate
-- Pagination: Handled by Compass API offset/limit parameters
-- Expected Rows: Up to 100,000 per API call
-- Estimated Execution: < 5 seconds per page

SELECT 
  t.transactionId,
  CAST(t.transactionDate AS date) AS trans_date,
  CAST(t.amount AS decimal) AS amount_decimal,
  t.transactionType,
  t.status,
  c.customerName,
  c.customerEmail
FROM TransactionHistory t
INNER JOIN Customers c ON t.customerId = c.customerId
WHERE CAST(t.transactionDate AS date) IS NOT NULL
  AND CAST(t.transactionDate AS date) >= ?  -- Parameter: startDate
  AND CAST(t.transactionDate AS date) < ?   -- Parameter: endDate
  AND CAST(t.amount AS decimal) IS NOT NULL
  AND t.status IN ('Completed', 'Pending')
ORDER BY t.transactionDate DESC, t.transactionId;
-- No LIMIT/OFFSET in SQL - handled by Compass API
```

**IPA Pagination Implementation**:

```text
1. Submit query: POST /compass/v2/jobs/ with SQL above
2. Poll status: GET /jobs/{queryId}/status/ until FINISHED
3. Retrieve page 1: GET /jobs/{queryId}/result/?offset=0&limit=100000
4. Retrieve page 2: GET /jobs/{queryId}/result/?offset=100000&limit=100000
5. Continue until no more data returned
```

**Why This Is Good**:

- ✅ Pagination handled by Compass API (offset/limit parameters)
- ✅ NULL checks after CAST operations
- ✅ Parameterized values (dates)
- ✅ Selective WHERE clause (date range, status filter)
- ✅ Proper JOIN with ON condition
- ✅ Documented purpose and parameters
- ✅ Deterministic ordering (date + ID)

---

### Example 2: Aggregation with CTE

**Use Case**: Monthly sales summary with customer segmentation

```sql
-- Purpose: Generate monthly sales summary by customer segment
-- Parameters: startDate, endDate
-- Expected Rows: ~12 months × 3 segments = 36 rows
-- Estimated Execution: < 10 seconds

WITH CustomerSegments AS (
  SELECT 
    customerId,
    CASE 
      WHEN totalSpent >= 10000 THEN 'Premium'
      WHEN totalSpent >= 1000 THEN 'Standard'
      ELSE 'Basic'
    END AS segment
  FROM (
    SELECT 
      customerId,
      SUM(CAST(amount AS decimal)) AS totalSpent
    FROM Orders
    WHERE CAST(orderDate AS date) >= ?  -- Parameter: segmentStartDate
    GROUP BY customerId
  ) customer_totals
),
MonthlySales AS (
  SELECT 
    DATE_TRUNC('month', CAST(orderDate AS date)) AS sales_month,
    customerId,
    COUNT(*) AS order_count,
    SUM(CAST(amount AS decimal)) AS monthly_total
  FROM Orders
  WHERE CAST(orderDate AS date) IS NOT NULL
    AND CAST(orderDate AS date) >= ?  -- Parameter: startDate
    AND CAST(orderDate AS date) < ?   -- Parameter: endDate
    AND CAST(amount AS decimal) IS NOT NULL
  GROUP BY DATE_TRUNC('month', CAST(orderDate AS date)), customerId
)
SELECT 
  ms.sales_month,
  cs.segment,
  COUNT(DISTINCT ms.customerId) AS customer_count,
  SUM(ms.order_count) AS total_orders,
  SUM(ms.monthly_total) AS total_revenue,
  AVG(ms.monthly_total) AS avg_revenue_per_customer
FROM MonthlySales ms
INNER JOIN CustomerSegments cs ON ms.customerId = cs.customerId
GROUP BY ms.sales_month, cs.segment
ORDER BY ms.sales_month DESC, cs.segment;
```

**Why This Is Good**:

- ✅ Modular CTEs for complex logic
- ✅ NULL safety throughout
- ✅ Parameterized date ranges
- ✅ Bounded result set (aggregated data)
- ✅ Clear business logic (customer segmentation)
- ✅ Efficient aggregation strategy
- ✅ Well-documented purpose

---

### Example 3: Cross-Format Join (JSON + DSV)

**Use Case**: Join JSON customer data with DSV order data

```sql
-- Purpose: Combine customer profile (JSON) with order history (DSV)
-- Parameters: startDate, customerId (optional)
-- Expected Rows: 100-1000 per customer
-- Estimated Execution: < 3 seconds

SELECT 
  cust.customerId,
  cust.customerName,
  cust.customerEmail,
  cust.customerTier,
  ord.orderId,
  CAST(ord.orderDate AS date) AS order_date,
  CAST(ord.orderTotal AS decimal) AS order_total,
  ord.orderStatus
FROM CustomerProfileJson cust
INNER JOIN OrderHistoryDsv ord 
  ON cust.customerId = ord.customerId
WHERE CAST(ord.orderDate AS date) IS NOT NULL
  AND CAST(ord.orderDate AS date) >= ?  -- Parameter: startDate
  AND CAST(ord.orderTotal AS decimal) IS NOT NULL
  AND (? IS NULL OR cust.customerId = ?)  -- Optional filter: customerId
ORDER BY cust.customerId, ord.orderDate DESC
-- Pagination handled by Compass API offset/limit parameters
```

**Why This Is Good**:

- ✅ Joins different object formats (JSON + DSV)
- ✅ Optional parameter handling (customerId)
- ✅ NULL safety after CAST
- ✅ Pagination for large results
- ✅ Clear naming conventions

---

## Bad Examples

### Example 1: Missing Pagination

**Problem**: No result limiting or API pagination on large table

```sql
-- ❌ BAD: Will timeout on large datasets
SELECT * FROM TransactionHistory
WHERE transactionDate >= '2024-01-01'
ORDER BY transactionDate DESC;
```

**Issues**:

- ❌ No result limiting (SELECT TOP/LIMIT) or API pagination
- ❌ Hardcoded date
- ❌ No CAST on date column
- ❌ SELECT * (inefficient)

**Impact**: Query will timeout or return millions of rows, causing memory issues.

---

### Example 2: Unsafe CAST

**Problem**: CAST in WHERE without NULL check

```sql
-- ❌ BAD: Missing NULL check after CAST
SELECT 
  orderId,
  CAST(orderDate AS date) AS order_date,
  CAST(amount AS decimal) AS amount_decimal
FROM Orders
WHERE CAST(orderDate AS date) > '2024-01-01'
  AND CAST(amount AS decimal) > 100.00;
```

**Issues**:

- ❌ No NULL check after CAST (data loss)
- ❌ Hardcoded values (date, amount)
- ❌ Multiple CAST on same column (inefficient)

**Impact**: Rows with invalid dates/amounts are silently excluded (data loss).

---

### Example 3: Cartesian Product

**Problem**: Missing JOIN condition

```sql
-- ❌ BAD: Cartesian product
SELECT * FROM Orders o
CROSS JOIN Customers c
WHERE o.customerId = c.customerId;
```

**Issues**:

- ❌ CROSS JOIN instead of INNER JOIN
- ❌ JOIN condition in WHERE (inefficient)
- ❌ SELECT * (inefficient)

**Impact**: Generates N×M rows before filtering, causing timeout.

---

### Example 4: Non-Selective Filter

**Problem**: WHERE clause filters too few rows

```sql
-- ❌ BAD: Non-selective filter
SELECT * FROM Orders
WHERE status <> 'Cancelled';  -- Filters only 5% of rows
```

**Issues**:

- ❌ Non-selective filter (scans 95% of table)
- ❌ No pagination
- ❌ SELECT * (inefficient)

**Impact**: Scans entire table, slow performance.

---

### Example 5: Hardcoded Values

**Problem**: No parameterization

```sql
-- ❌ BAD: Hardcoded values everywhere
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'
  AND orderDate < '2024-02-01'
  AND status = 'Active'
  AND customerId = 12345
LIMIT 1000;
```

**Issues**:

- ❌ Hardcoded dates (not reusable)
- ❌ Hardcoded status (not flexible)
- ❌ Hardcoded customerId (single-use)
- ❌ Hardcoded limit (not configurable)

**Impact**: Requires code changes for different parameters.

---

## Before/After Refactoring

### Refactoring 1: Add Pagination and NULL Safety

**Before**:
```sql
SELECT * FROM Orders
WHERE CAST(orderDate AS date) > '2024-01-01'
ORDER BY orderDate DESC;
```

**After**:
```sql
-- Purpose: Fetch orders with pagination and NULL safety
-- Parameters: startDate
-- Pagination: Compass API offset/limit parameters
SELECT 
  orderId,
  CAST(orderDate AS date) AS order_date,
  CAST(amount AS decimal) AS amount_decimal,
  status,
  customerId
FROM Orders
WHERE CAST(orderDate AS date) IS NOT NULL
  AND CAST(orderDate AS date) > ?  -- Parameter: startDate
  AND CAST(amount AS decimal) IS NOT NULL
ORDER BY orderDate DESC, orderId
-- Pagination handled by Compass API
```

**Changes**:

1. Added NULL checks after CAST
2. Parameterized startDate
3. Added API pagination (Compass API offset/limit parameters)
4. Removed SELECT * (explicit columns)
5. Added deterministic ordering (date + ID)
6. Added documentation

---

### Refactoring 2: Fix Cartesian Product

**Before**:
```sql
SELECT * FROM Orders o, Customers c
WHERE o.customerId = c.customerId
  AND o.orderDate >= '2024-01-01';
```

**After**:
```sql
-- Purpose: Fetch orders with customer details
-- Parameters: startDate
SELECT 
  o.orderId,
  CAST(o.orderDate AS date) AS order_date,
  CAST(o.amount AS decimal) AS amount_decimal,
  c.customerName,
  c.customerEmail
FROM Orders o
INNER JOIN Customers c ON o.customerId = c.customerId
WHERE CAST(o.orderDate AS date) IS NOT NULL
  AND CAST(o.orderDate AS date) >= ?  -- Parameter: startDate
ORDER BY o.orderDate DESC
-- Pagination handled by Compass API offset/limit parameters
```

**Changes**:

1. Changed to INNER JOIN with ON clause
2. Added NULL safety
3. Parameterized date
4. Added pagination
5. Explicit column selection
6. Added documentation

---

### Refactoring 3: Optimize Aggregation

**Before**:
```sql
SELECT 
  customerId,
  COUNT(*) AS order_count,
  SUM(amount) AS total_spent
FROM Orders
GROUP BY customerId;
```

**After**:
```sql
-- Purpose: Customer order summary with date range filter
-- Parameters: startDate, endDate, minOrders
-- Expected Rows: ~1000 active customers
WITH FilteredOrders AS (
  SELECT 
    customerId,
    CAST(amount AS decimal) AS amount_decimal
  FROM Orders
  WHERE CAST(orderDate AS date) IS NOT NULL
    AND CAST(orderDate AS date) >= ?  -- Parameter: startDate
    AND CAST(orderDate AS date) < ?   -- Parameter: endDate
    AND CAST(amount AS decimal) IS NOT NULL
)
SELECT 
  customerId,
  COUNT(*) AS order_count,
  SUM(amount_decimal) AS total_spent,
  AVG(amount_decimal) AS avg_order_value
FROM FilteredOrders
GROUP BY customerId
HAVING COUNT(*) >= ?  -- Parameter: minOrders
ORDER BY total_spent DESC
LIMIT 100;
```

**Changes**:

1. Added date range filter (reduces aggregation scope)
2. Added NULL safety
3. Used CTE for clarity
4. Added HAVING clause for filtering
5. Added pagination (LIMIT)
6. Parameterized values
7. Added documentation

---

## Performance Comparison

### Scenario: Fetch 100K rows from 10M row table

| Query Pattern | Execution Time | Memory Usage | Timeout Risk |
|---------------|----------------|--------------|--------------|
| No pagination | 45+ minutes | 2+ GB | HIGH |
| LIMIT 100000 | 30 minutes | 500 MB | MEDIUM |
| LIMIT 1000 (paginated) | 5 seconds/page | 10 MB/page | LOW |
| Filtered + paginated | 2 seconds/page | 5 MB/page | VERY LOW |

**Recommendation**: Always use pagination with selective filters for production queries.

---

## Common Mistakes Summary

| Mistake | Impact | Fix |
|---------|--------|-----|
| No pagination | Timeout, memory issues | Use Compass API offset/limit |
| Missing NULL check after CAST | Data loss | Add IS NOT NULL |
| Hardcoded values | Not reusable | Parameterize |
| Cartesian product | Exponential rows | Use INNER JOIN |
| Non-selective WHERE | Full table scan | Add date/status filters |
| SELECT * | Inefficient | Explicit columns |
| Missing ORDER BY | Non-deterministic pagination | Add ORDER BY |

---

## Additional Resources

- **Compass SQL Syntax**: `.kiro/steering/06_Compass_SQL_CheatSheet.md`
- **Data Fabric Guide**: `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md`
- **Analysis Rules**: `references/analysis-rules.md`
