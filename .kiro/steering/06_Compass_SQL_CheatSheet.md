---
inclusion: auto
name: compass-sql
description: Compass SQL dialect, Data Fabric queries, Data Lake operations, SQL syntax, JDBC connections. Use when writing Compass SQL queries, querying Data Fabric, or working with Infor OS data.
---

# Compass SQL CheatSheet

## Table of Contents

- [Critical Rules for AI](#critical-rules-for-ai)
- [Quick Reference](#quick-reference)
- [Object and Property Naming](#object-and-property-naming)
- [Query Structure](#query-structure)
- [SELECT Clauses](#select-clauses)
- [Joins and Subqueries](#joins-and-subqueries)
- [Expressions and Comparison Functions](#expressions-and-comparison-functions)
- [Logical and Comparison Operators](#logical-and-comparison-operators)
- [String Functions](#string-functions)
- [Mathematical Functions](#mathematical-functions)
- [Aggregation Functions](#aggregation-functions)
- [Datetime Functions](#datetime-functions)
- [Conversion Functions](#conversion-functions)
- [Analytic Functions](#analytic-functions)
- [Views](#views)
- [Common Query Patterns](#common-query-patterns)
- [Limitations](#limitations)
- [Connectivity](#connectivity)
- [AI Assistant Guidelines](#ai-assistant-guidelines)

## Critical Rules for AI

**MUST KNOW UPFRONT:**

- **READ-ONLY**: No `INSERT`, `UPDATE`, `DELETE`, or `CREATE TABLE` statements (only CREATE VIEW supported)
- **Case Rules**: Object names are NOT case-sensitive, property names ARE case-sensitive, data values ARE case-sensitive
- **CAST Failures**: Return `NULL` instead of errors (always check for NULL after CAST)
- **Timeout**: 60-minute query timeout limit
- **Quote Names**: Use double quotes for names with spaces, hyphens, starting with numbers, or reserved words
- **UTC Timestamps**: All Data Lake timestamps are in UTC timezone
- **Variation Handling**: By default, queries retrieve the highest variation of a record not tagged as deleted

**DO:**

- Use `CAST(column AS type)` for type conversions (returns NULL on failure)
- Use double quotes for problematic object/property names: `"Order Date"`
- Check for NULL after CAST operations in WHERE clauses
- Use `SELECT TOP` or `SELECT LIMIT` for result limiting (OFFSET not supported in SQL)
- Use Compass API `offset` and `limit` query parameters for pagination
- Join JSON and DSV objects freely
- Use `infor.lastModified()` for incremental data loads
- Use locale() function for localized property values

**DON'T:**

- Generate `INSERT`, `UPDATE`, `DELETE` statements
- Assume CAST will error on failure (it returns NULL)
- Use single quotes for object names (use double quotes)
- Create duplicate property names differing only by case
- Use `=''` or `=' '` to evaluate NULL conditions (unreliable)
- Use wildcard characters `[ ]` and `[^ ]` (not supported)

## Quick Reference

**Most Common Operations:**

```sql
-- Basic SELECT with filtering (IPA context - no LIMIT needed)
SELECT column1, column2
FROM ObjectName
WHERE column1 = 'value'
ORDER BY column2 DESC;

-- Type conversion (returns NULL on failure)
SELECT CAST(dateColumn AS date) AS converted_date
FROM ObjectName
WHERE CAST(amountColumn AS decimal) IS NOT NULL
  AND CAST(amountColumn AS decimal) > 100.00;

-- JOIN across object types
SELECT o1.property1, o2.property2
FROM JsonObject o1
INNER JOIN DsvObject o2 ON o1.key = o2.key;

-- Aggregation
SELECT category, COUNT(*) AS count, SUM(amount) AS total
FROM Sales
GROUP BY category
HAVING COUNT(*) > 10
ORDER BY total DESC;

-- Incremental data load (IPA context - no LIMIT needed)
SELECT * FROM Orders
WHERE infor.lastModified() >= '2024-01-01T00:00:00.000Z'
ORDER BY id;

-- Note: In IPA implementations, pagination is handled by Compass API
-- offset/limit parameters, not SQL LIMIT clauses
```

## Object and Property Naming

**Case Sensitivity Rules:**

- **Object names**: NOT case-sensitive (`Customer`, `CUSTOMER`, `customer` are the same)
- **Property names**: CASE-SENSITIVE (`ProductID`, `productid`, `PRODUCTID` are different)
- **Data values**: CASE-SENSITIVE (`'Smith'` and `'SMITH'` are different)

**When to Use Double Quotes:**

```sql
-- Names with spaces
SELECT "Order Date", "Customer Name" FROM Orders;

-- Names starting with numbers
SELECT "2024_Sales" FROM "2024_Data";

-- Reserved words
SELECT "SELECT", "FROM" FROM ReservedWordTable;

-- Names with hyphens or special characters
SELECT "order-id" FROM "customer-orders";
```

**Valid Characters:**

- Object names: A-Z, a-z, 0-9, underscore `_`
- Property names: A-Z, a-z, 0-9, underscore `_`, period `.`, space

**Aliases:**

- Enclose aliases in double quotes or square brackets
- Double quotes recommended (supported for all names)
- Square brackets not supported for names with special characters, reserved words, or starting with digits

## Query Structure

**Basic Structure:**

```sql
SELECT one or more properties, expressions, or literals
FROM object
WHERE filter condition(s)
GROUP BY expression
HAVING filter condition(s)
ORDER BY expression [ ASC | DESC ]
```

**FROM Clause:**

- Specify data objects or subquery from which values are derived
- Can include data from more than one object (JOINs)
- Supports JSON and DSV objects

**WHERE Clause:**

- Filter conditions to limit query results
- Most queries should include WHERE to limit results
- Use `infor.lastModified()` for incremental data loads
- Queries through Compass API do not limit results by default (returns all data)
- Queries through Compass UI limit results to 10,000 rows

**GROUP BY:**

- Group results by properties or expressions
- Expression in GROUP BY must also be in SELECT clause
- Does not support aggregation or window expressions
- Must use property names (aliases cannot be used)

**HAVING:**

- Filter aggregated results
- Commonly used with SELECT for aggregated result sets

**ORDER BY:**

- Sort result set columns
- Use ASC or DESC for ascending/descending order
- Property names and aliases may be used
- String values are case-sensitive (affects sort order)

## SELECT Clauses

**SELECT ALL:**

```sql
SELECT * FROM object
```

Retrieves all properties from data objects. Not recommended as object properties may change over time.

**SELECT DISTINCT:**

```sql
SELECT DISTINCT property1 FROM object
```

Removes duplicate values. Note: Values are case-sensitive, so 'ABC' and 'abc' are different.

**SELECT TOP:**

```sql
SELECT TOP 100 * FROM object
```

Limits number of rows. TOP PERCENT and TOP WITH TIES not supported.

**SELECT LIMIT:**

```sql
SELECT * FROM object LIMIT 100
```

Apache Spark syntax for limiting rows.

**SELECT with Aliases:**

```sql
SELECT property1 AS alias1, property2 AS alias2 FROM object
```

Use double quotes or square brackets for aliases.

**SELECT with lastModified:**

```sql
SELECT property1, property2, infor.lastModified() FROM object
```

Returns UTC timestamp when data object was posted to Data Lake.

**SELECT with lastModified Filter:**

```sql
SELECT * FROM object
WHERE infor.lastModified() >= '2024-01-01T00:00:00.000Z';
```

Timestamp format: `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'` (UTC)

Supported operators: `=`, `>=`, `<=`, `BETWEEN`

**SELECT Localized Values:**

```sql
-- Basic locale function
SELECT locale(localizedproperty, 5) FROM object

-- With autofill
SELECT locale(localizedproperty, 5, 'autofill') FROM object

-- Without locale function (returns default locale)
SELECT localizedproperty FROM object
```

Returns localized values based on Data Catalog locale selections. Number of positions defines columns returned (property_1, property_2, etc.).

**SELECT Locale Selections:**

```sql
SELECT * FROM datacatalog.locale_selection
```

Returns locale selections defined in Data Catalog.

**UNION / UNION ALL:**

```sql
SELECT * FROM object1
UNION
SELECT * FROM object2
```

Combines result sets. Each selection must have same number of properties with same data types. UNION ALL retrieves all values including duplicates.

**EXCEPT:**

```sql
SELECT * FROM object1
EXCEPT
SELECT * FROM object2
```

Returns results from first query not included in second query.

**INTERSECT:**

```sql
SELECT * FROM object1
INTERSECT
SELECT * FROM object2
```

Returns only rows in results of both queries.

**WITH (Common Table Expression):**

```sql
WITH commontablename AS
  (SELECT property1 FROM object1)
SELECT property1 FROM commontablename
```

Defines common table expression used above main SELECT clauses.

## Joins and Subqueries

**JOIN Types:**

- `INNER JOIN`
- `OUTER JOIN`
- `JOIN`
- `LEFT INNER JOIN`
- `LEFT OUTER JOIN`
- `RIGHT JOIN`
- `CROSS JOIN`

**JOIN Syntax:**

```sql
SELECT object1.property1, object2.property2
FROM object1
INNER JOIN object2 ON object1.property1 = object2.property1
```

Supports joins for different object formats (JSON and DSV).

**Subqueries:**

```sql
-- Subquery in WHERE
SELECT * FROM Orders
WHERE customerId IN (
  SELECT customerId FROM Customers WHERE region = 'West'
);

-- Subquery in FROM (inline view)
SELECT sub.category, AVG(sub.total) AS avg_total
FROM (
  SELECT category, SUM(amount) AS total
  FROM Sales
  GROUP BY category
) sub
GROUP BY sub.category;
```

Limited support for correlated subqueries. Property alias in inline view cannot have second alias in outer query.

## Expressions and Comparison Functions

**CASE:**

```sql
CASE condition_expression
  WHEN expression_value THEN result_expression
  WHEN expression_value THEN result_expression
  ELSE result_expression
END
```

**COALESCE:**

```sql
COALESCE(argument1, argument2, argument3)
```

Returns first non-null value. Requires minimum of two arguments.

**ISNULL:**

```sql
ISNULL(expression, substitute_value)
```

Returns substitute value if expression is NULL.

**GREATEST:**

```sql
GREATEST(argument1, argument2, argument3)
```

Returns highest value from list of arguments.

**LEAST:**

```sql
LEAST(argument1, argument2, argument3)
```

Returns lowest value from list of arguments.

**NVL:**

```sql
NVL(expression, substitute_value)
```

Returns substitute value if expression is NULL.

**NVL2:**

```sql
NVL2(expression, not_null_value, null_value)
```

Returns not_null_value if expression is not NULL, otherwise returns null_value. Second and third parameters must be same data type.

## Logical and Comparison Operators

**Supported Operators:**

- `AND`, `OR`, `NOT`
- `BETWEEN`
- `IS NULL`, `IS NOT NULL`
- `LIKE`, `NOT LIKE`
- `>`, `>=`, `<`, `<=`, `=`, `<>`
- `ANY`, `ALL`, `SOME`
- `IN`

**Wildcard Characters:**

- `%` (percent) - Supported
- `_` (underscore) - Supported
- `[ ]` (brackets) - NOT supported
- `[^ ]` (caret brackets) - NOT supported

**NULL Evaluation:**

Do NOT use these patterns (unreliable results):

- `=''`
- `=' '`
- `<>''`
- `<>' '`

Use `IS NULL` or `IS NOT NULL` instead.

**Case Sensitivity:**

Data values are case-sensitive. `'abc'` and `'ABC'` are not equal.

**String to Integer Comparison:**

Compass queries support comparing strings to integers: `WHERE order_number = 123` or `order_number = '123'`

## String Functions

**CHAR:**

```sql
CHAR(ascii_code)
```

Returns ASCII character. Supports range higher than 255 ASCII codes.

**CHARINDEX:**

```sql
CHARINDEX(string_to_find, string_to_search, starting_position)
```

Returns position number of string in original expression.

**CONCAT:**

```sql
CONCAT(property1, property1, expression) AS concatenatedstring
```

Concatenates one or more values into string.

**Concatenation using ||:**

```sql
string_expression || '-' || string_expression
```

If one expression is NULL, result is NULL.

**INSTR:**

```sql
INSTR(string_to_search, string_to_find)
```

Returns position of first occurrence of substring.

**LEFT:**

```sql
LEFT(stringproperty, integer_value)
```

Returns leftmost characters of string.

**LEN / LENGTH:**

```sql
LEN(string_expression)
LENGTH(string_expression)
```

Returns length of string (excludes trailing spaces). Empty string returns 0.

**LPAD:**

```sql
LPAD('padding_characters', string_expression, overall_length)
```

Pads left of string with values up to overall string length.

**LOWER:**

```sql
LOWER(stringproperty)
```

Converts character string to lowercase.

**LTRIM:**

```sql
LTRIM(stringproperty)
LTRIM(stringproperty, trim_string)
```

Trims leading spaces or specific characters from left of string.

**REPLACE:**

```sql
REPLACE(string_expression, search_string, substitute_string)
```

Substitutes one string for another.

**RIGHT:**

```sql
RIGHT(stringproperty, integer_value)
```

Returns rightmost characters of string.

**RPAD:**

```sql
RPAD('padding_characters', string_expression, overall_length)
```

Pads right of string with values up to overall string length.

**RTRIM:**

```sql
RTRIM(stringproperty)
RTRIM(stringproperty, trim_string)
```

Trims trailing spaces or specific characters from right of string.

**SUBSTR:**

```sql
SUBSTR(string_expression, start_position, number_of_characters)
```

Returns substring of string. Third parameter is optional.

**SUBSTRING:**

```sql
SUBSTRING(string_expression, start_position, number_of_characters)
```

Returns substring or portion of string expression.

**TRIM:**

```sql
TRIM(stringproperty)
```

Trims leading and trailing spaces from string.

**UPPER:**

```sql
UPPER(stringproperty)
```

Converts character string to uppercase.

## Mathematical Functions

**Operators:**

- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Percentage: `%`

Note: `+` can also concatenate values.

**ABS:**

```sql
ABS(numeric_expression)
```

Returns absolute (positive) value.

**CEIL:**

```sql
CEIL(numeric_expression)
```

Returns smallest integer greater than or equal to value.

**CEILING:**

```sql
CEILING(numeric_expression)
```

Returns smallest integer equal to or higher than value.

**FLOOR:**

```sql
FLOOR(number_value)
```

Returns highest integer equal to or less than value.

**INT:**

```sql
INT(numeric_expression)
```

Casts number to integer (rounds down). Returns NULL if not valid number.

**ISNUMERIC:**

```sql
ISNUMERIC(expression)
```

Returns 1 if numeric, 0 if not numeric.

**POWER:**

```sql
POWER(base_number, exponent_number)
```

Raises one number to power of another. If first argument is decimal, casts to decimal(38,15) before raising. Returns error if result too large.

**ROUND:**

```sql
ROUND(number_value, number_of_decimal_places)
```

Rounds numeric value to specified decimal places.

**Signed Expression:**

```sql
SELECT -(numeric_expression)
```

Converts value from negative to positive or vice versa.

**TRUNCATE:**

```sql
TRUNCATE(number_value, number_of_decimal_places)
```

Truncates numeric value to specified decimal places.

## Aggregation Functions

**AVG:**

```sql
AVG(numeric_expression)
```

Averages numeric values in result.

**COUNT:**

```sql
COUNT(expression)
COUNT(DISTINCT expression)
```

Counts number of records. COUNT DISTINCT counts unique rows.

**MAX:**

```sql
MAX(expression)
```

Returns highest value from set. Does not support Boolean properties.

**MIN:**

```sql
MIN(expression)
```

Returns lowest value from set. Does not support Boolean properties.

**SUM:**

```sql
SUM(numeric_expression)
```

Adds numeric values and returns single value.

## Datetime Functions

**CRITICAL**: All Data Lake timestamp data is in UTC timezone. Queries using timestamp values are always considered in UTC.

**ADD_MONTHS:**

```sql
ADD_MONTHS(date_expression, number_of_months)
```

Adds or subtracts months from date. Based on Spark.

**CURRENT_DATE:**

```sql
SELECT CURRENT_DATE
```

Returns current date (e.g., 2022-04-25).

**CURRENT_TIMESTAMP:**

```sql
CURRENT_TIMESTAMP
```

Returns current datetime in UTC ISO8601 RFC3339 format (e.g., 2019-09-01T09:30:00.000Z).

**DATEADD:**

```sql
DATEADD(datepart, number_of_units, date_expression)
```

Adds or subtracts date units. Number may be positive or negative.

**DATEDIFF:**

```sql
DATEDIFF(datepart, date_expression, date_expression)
```

Returns number of datepart units between two dates/timestamps.

**DATEPART:**

```sql
DATEPART(datepart, date_expression)
```

Returns value of specific part of date/timestamp. Formats not supported: %D, %U, %u, %V, %w, %X.

**DATE_FORMAT:**

```sql
DATE_FORMAT(timestamp_expression, format)
```

Converts datetime to string (e.g., 'yyyy-MM-dd').

**DATE_SUB:**

```sql
DATE_SUB(date_expression, number_of_days)
```

Positive number subtracts days, negative number adds days.

**DATE_TRUNC:**

```sql
DATE_TRUNC('YYYY', timestamp_expression)
```

Truncates timestamp and converts to specified datetime unit.

**DAY / DAYOFMONTH / DAY_OF_MONTH:**

```sql
DAY(date_expression)
DAYOFMONTH(date_expression)
DAY_OF_MONTH(date_expression)
```

Returns day from date expression.

**FROM_UTC_TIMESTAMP:**

```sql
FROM_UTC_TIMESTAMP(UTC_timestamp, timezone)
```

Converts timestamp from UTC to selected timezone. Returns timestamp with time zone.

Example: `FROM_UTC_TIMESTAMP('2020-07-13T09:30:00Z', 'America/New_York')` returns `2020-07-13T05:30:00.000-04:00`

**GETDATE:**

```sql
GETDATE()
```

Returns current date and time in UTC ISO8601 RFC3339.

**GETUTCDATE:**

```sql
GETUTCDATE()
```

Returns current date and time in UTC ISO8601 RFC3339.

**LAST_DAY:**

```sql
LAST_DAY(date_expression)
```

Returns last day of month associated with date/datetime.

**MONTH:**

```sql
MONTH(date_expression)
```

Returns month from date expression.

**TO_DATE:**

```sql
TO_DATE('2020-05-07', 'yyyy-MM-dd')
```

Converts string to date. First parameter must be string, second is date expression.

**TRUNC:**

```sql
INT(TRUNC(CURRENT_DATE, 'MM'))
```

Truncates date/timestamp to year or month. Result is date.

**UNIX_TIMESTAMP:**

```sql
UNIX_TIMESTAMP(date_expression)
UNIX_TIMESTAMP(date_expression, format)
```

Converts date expression to UNIX timestamp format. Format parameter not required if date_expression references date/datetime property.

Example: `UNIX_TIMESTAMP('2020-07-13 10:15:01')` returns `1594635301`

**YEAR:**

```sql
YEAR(date_expression)
```

Returns year from date expression.

## Conversion Functions

**CAST:**

```sql
CAST(expression AS data_type)
```

Casts value/expression to data type. **Returns NULL if cast fails** (no error thrown).

Supported data types: `varchar`, `date`, `datetime`, `datetime2`, `decimal`, `integer`, `bigint`

**CONVERT (datetime to string):**

```sql
CONVERT(datetime_expression, string_expression, date_style)
```

Converts date/datetime to string. Always requires three parameters. Date expressions not supported.

**CONVERT (string to datetime):**

```sql
CONVERT(string_type, datetime_expression, date_style)
```

Converts string to specific datetime style. First parameter is string datatype and size (e.g., varchar(20)). Third parameter is style number (defined by Microsoft SQL Server). Date expressions not supported. Styles 130 and 131 not supported.

## Analytic Functions

**LEAD:**

```sql
LEAD(expression, offset_value, default_value) OVER (PARTITION BY ... ORDER BY ...)
```

Accesses data from following or subsequent row of result set.

**RANK ... OVER ... PARTITION BY:**

```sql
RANK() OVER ([PARTITION BY value_expression1, value_expression2, ...] ORDER BY ...)
```

Ranks or numbers row results. If partition used, rank is number of row within partition. Used WITH TIES to assign same rank value to tied results.

**ROW_NUMBER ... OVER ... PARTITION BY:**

```sql
ROW_NUMBER() OVER ([PARTITION BY value_expression1, value_expression2, ...] ORDER BY ...)
```

Numbers result set. If partition used, returns row number within partition. Use ORDER BY to sort results.

## Views

**CREATE VIEW:**

```sql
CREATE VIEW view_name AS select_statement
```

Example:

```sql
CREATE VIEW example_view AS (
  SELECT productname, companyname FROM orderDetailsObject
)
```

**ALTER VIEW:**

```sql
ALTER VIEW view_name AS select_statement
```

Modifies previously created view.

**DROP VIEW:**

```sql
DROP VIEW view_name
```

Drops a view.

**SELECT from View:**

```sql
SELECT columnName FROM view_name
```

Example:

```sql
SELECT * FROM example_view
```

## Common Query Patterns

### Pattern 1: Result Limiting (SQL)

**IMPORTANT FOR IPA IMPLEMENTATIONS:**

In IPA contexts, SQL queries typically do NOT include LIMIT clauses. Data filtering is done through WHERE, GROUP BY, and HAVING clauses. Pagination is handled at the Compass API level using offset/limit parameters in the API calls.

```sql
-- IPA Implementation (typical pattern - no LIMIT in SQL)
SELECT * FROM LargeTable
WHERE status = 'Active'
ORDER BY id;

-- Pagination handled by Compass API:
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

### Pattern 1b: Pagination (Compass API)

**IMPORTANT**: Pagination is handled at the API level, not in SQL.

```text
IPA Implementation:
1. Submit query: POST /compass/v2/jobs/ with SQL query
2. Get queryId from response
3. Poll status: GET /jobs/{queryId}/status/ until FINISHED
4. Retrieve results with pagination:
   - Page 1: GET /jobs/{queryId}/result/?offset=0&limit=100000
   - Page 2: GET /jobs/{queryId}/result/?offset=100000&limit=100000
   - Continue until no more data

SQL Query (no OFFSET in SQL):
SELECT * FROM LargeTable
ORDER BY id;
```

### Pattern 2: Incremental Data Load

```sql
-- Initial load (all data - IPA context)
SELECT * FROM Orders
ORDER BY orderId;

-- Incremental load (data since last extract - IPA context)
SELECT * FROM Orders
WHERE infor.lastModified() >= '2024-01-01T00:00:00.000Z'
ORDER BY orderId;

-- Pagination handled by Compass API offset/limit parameters
```

### Pattern 3: Safe CAST with NULL Check

```sql
SELECT 
  orderId,
  CAST(orderDate AS date) AS order_date,
  CAST(orderTotal AS decimal) AS total_decimal
FROM Orders
WHERE CAST(orderDate AS date) IS NOT NULL
  AND CAST(orderTotal AS decimal) IS NOT NULL
  AND CAST(orderTotal AS decimal) > 100.00;
```

### Pattern 4: Cross-Format Join (JSON + DSV)

```sql
SELECT 
  json_obj.customerId,
  json_obj.customerName,
  dsv_obj.orderTotal
FROM CustomerJson json_obj
INNER JOIN OrdersDsv dsv_obj
  ON json_obj.customerId = dsv_obj.customerId
WHERE dsv_obj.orderDate >= '2024-01-01';
```

### Pattern 5: Aggregation with HAVING

```sql
SELECT 
  productCategory,
  COUNT(*) AS order_count,
  SUM(CAST(orderTotal AS decimal)) AS total_sales
FROM Orders
WHERE CAST(orderDate AS date) >= '2024-01-01'
GROUP BY productCategory
HAVING COUNT(*) > 100
ORDER BY total_sales DESC;
```

### Pattern 6: Common Table Expression (CTE)

```sql
WITH RecentOrders AS (
  SELECT 
    customerId,
    COUNT(*) AS order_count,
    SUM(CAST(total AS decimal)) AS total_spent
  FROM Orders
  WHERE CAST(orderDate AS date) >= '2024-01-01'
  GROUP BY customerId
)
SELECT 
  c.customerName,
  ro.order_count,
  ro.total_spent
FROM Customers c
INNER JOIN RecentOrders ro ON c.customerId = ro.customerId
WHERE ro.order_count > 5
ORDER BY ro.total_spent DESC;
```

### Pattern 7: UNION for Combining Results

```sql
SELECT customerId, 'Active' AS status FROM ActiveCustomers
UNION ALL
SELECT customerId, 'Inactive' AS status FROM InactiveCustomers
ORDER BY customerId;
```

### Pattern 8: Localized Values

```sql
-- Select localized property with 5 locale positions
SELECT 
  Id,
  locale(greeting, 5) AS greeting_localized
FROM common_greetings;

-- Result columns: Id, greeting_1, greeting_2, greeting_3, greeting_4, greeting_5
```


## Pagination: SQL vs API

**CRITICAL DISTINCTION:**

**SQL Syntax (in query string):**
- ✅ `SELECT TOP n` - Limits results to n rows
- ✅ `SELECT ... LIMIT n` - Limits results to n rows (Apache Spark syntax)
- ❌ `OFFSET` - NOT supported in Compass SQL syntax

**Compass API Parameters (in HTTP request):**
- ✅ `offset` - Row offset for pagination (query parameter)
- ✅ `limit` - Max rows per page (query parameter)
- Used in: `GET /jobs/{queryId}/result/?offset=0&limit=100000`

**Example:**

```sql
-- SQL Query (submitted to Compass API)
SELECT * FROM Orders
WHERE orderDate >= '2024-01-01'
ORDER BY orderId;
-- No OFFSET in SQL!
```

```text
-- IPA WebRun Activities (Compass API calls)
1. Submit query (POST /jobs/)
2. Poll status (GET /jobs/{queryId}/status/)
3. Get page 1: GET /jobs/{queryId}/result/?offset=0&limit=100000
4. Get page 2: GET /jobs/{queryId}/result/?offset=100000&limit=100000
5. Continue until no more data
```

**AI Assistant Rule**: Never use `OFFSET` in SQL queries. Use Compass API parameters for pagination.

## Limitations

**Not Supported:**

- ❌ `INSERT`, `UPDATE`, `DELETE` statements
- ❌ DDL statements (`CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, etc.)
- ❌ Stored procedures or user-defined functions
- ❌ Transactions or locking
- ❌ Window functions (limited/unclear support)
- ❌ Wildcard characters `[ ]` and `[^ ]`
- ❌ TOP PERCENT and TOP WITH TIES
- ❌ Correlated subqueries (limited support)
- ❌ Property alias in inline view with second alias in outer query
- ❌ DATEPART formats: %D, %U, %u, %V, %w, %X
- ❌ CONVERT datetime styles 130 and 131

**Constraints:**

- **Query Timeout**: 60 minutes maximum
- **API Pagination**: Max rows per page (varies by deployment)
- **UI Result Limit**: 10,000 rows through Compass UI
- **Duplicate Names**: Cannot have property names differing only by case
- **CAST Behavior**: Returns NULL on failure (no error thrown)
- **NULL Evaluation**: Do not use `=''` or `=' '` (unreliable)

**Comparison with Standard SQL:**

| Feature | Compass SQL | Standard SQL (Postgres/MySQL) |
|---------|-------------|-------------------------------|
| DML (INSERT/UPDATE) | ❌ Not supported | ✅ Supported |
| Window Functions | ⚠️ Limited | ✅ Full support |
| Subqueries | ✅ Supported | ✅ Supported |
| CTEs (WITH) | ✅ Supported | ✅ Supported |
| Joins | ✅ INNER, LEFT, RIGHT, CROSS | ✅ Full support |
| CAST/CONVERT | ✅ Limited types | ✅ Extensive types |
| Case Sensitivity | Names: insensitive, Values: sensitive | Configurable |
| Views | ✅ CREATE/ALTER/DROP | ✅ Full support |

## Connectivity

**JDBC Driver:**

```java
// Driver class
com.infor.idl.jdbc.Driver

// Connection string pattern
jdbc:infordatalake://<tenant-host>

// Example
jdbc:infordatalake://mytenant.inforcloudsuite.com
```

**Compass API (REST):**

- Endpoint: `https://<tenant>/IONAPI/compass/v2/queries`
- Authentication: OAuth2 bearer token
- Pagination: Use `LIMIT` and `OFFSET` in query
- Response: JSON with data array and metadata

**Query Editor:**

- Access via Infor OS Portal > Data Fabric > Compass
- Interactive query building and execution
- Export results to CSV/Excel
- Result limit: 10,000 rows

## AI Assistant Guidelines

**When generating Compass SQL queries:**

1. **Start with object metadata check**: Verify object exists in Data Catalog
2. **Use CAST defensively**: Always check for NULL after type conversion
3. **Quote problematic names**: Use double quotes for spaces, hyphens, numbers, reserved words
4. **DO NOT add LIMIT clauses when reviewing user code**: In IPA implementations, users typically don't use LIMIT in SQL queries. Filtering is done through WHERE, GROUP BY, and HAVING clauses. Pagination is handled at the Compass API level using offset/limit parameters.
5. **Implement API pagination**: Use Compass API `offset` and `limit` parameters for large datasets
6. **Explain limitations**: Tell user if requested feature isn't supported
7. **Provide NULL handling**: Show how to handle CAST failures
8. **Use UTC timestamps**: All timestamps are in UTC timezone
9. **Consider incremental loads**: Use `infor.lastModified()` for incremental data extraction

**CRITICAL - LIMIT Clause Usage:**

- **When writing NEW queries for testing/exploration**: You MAY suggest LIMIT for safety
- **When reviewing USER code in IPA context**: DO NOT suggest adding LIMIT clauses
- **Reason**: IPA processes retrieve all matching data; pagination happens via Compass API calls, not SQL LIMIT

**Example AI Response Pattern (New Query):**

```text
I'll generate a Compass SQL query to [task]. Note that:
- Compass SQL is read-only (no INSERT/UPDATE)
- CAST returns NULL on failure, so I'll add NULL checks
- For pagination, use Compass API offset/limit parameters
- All timestamps are in UTC

[Query here]

This query:
1. Casts dateColumn to date type (returns NULL if invalid)
2. Filters out NULL conversions in WHERE clause
3. Uses infor.lastModified() for incremental data load
```

**Example AI Response Pattern (Code Review):**

```text
Reviewing your Compass SQL query:

Issues found:
1. GROUP BY includes literal constant '<!RunDate>' - should be removed
2. Commented code has NULL evaluation issue (='' is unreliable)

Improved query:
[Query without LIMIT clause - pagination handled by Compass API]
```

**For Comprehensive SQL Analysis:**

Use the `compass-sql-analyzer` skill for detailed analysis:

```text
Activate the compass-sql-analyzer skill to analyze Compass SQL queries for:
- Syntax validation (Compass SQL compliance)
- Performance analysis (pagination, CAST usage, JOIN optimization)
- Durability assessment (handling 1K to millions of rows)
- Flexibility review (parameterization, reusability)
- Best practices recommendations
- Improved code with explanations
```

The skill provides comprehensive analysis across 6 dimensions with severity ratings, impact assessment, and production-ready refactored code.

## See Also

- `.kiro/skills/compass-sql-analyzer/` - Comprehensive SQL analysis skill
- `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md` - Data Fabric architecture and APIs
- `Infor_Data_Fabric_User_Guide.pdf` - Official documentation (Chapter 11: Compass SQL Reference)
