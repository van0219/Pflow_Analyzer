-- RICE 13 SUMMARY SQL QUERY (FCE)
-- SQLite-compatible version (converted from Compass SQL)
-- Investigation: GLSummary Dec 15 Zero Value Issue
-- Conversions applied:
--   ISNULL(x, y) → IFNULL(x, y)
--   CHARINDEX(substr, str) → INSTR(str, substr) [parameter order reversed!]
--   LPAD(str, len, pad) → SUBSTR(pad || str, -len)
--   SUBSTRING(str, start, len) → SUBSTR(str, start, len)
--   RIGHT(str, len) → SUBSTR(str, -len)
--   CAST AS DECIMAL(18,2) → CAST AS REAL
--   <!BodType> → BODData
--   <!SQL_QuarterFilter> → removed

SELECT 
    FEG,
    Scenario,
    Company,
    Ledger,
    System,
    Currency,
    EntityYearPeriod,
    Account,
    CASE WHEN Project IS NULL OR Project = '' THEN 'NA' ELSE Project END AS Project,
    PeriodEndingDate,
    CASE WHEN Entity IS NULL OR Entity = '' THEN 'NA' ELSE Entity END AS FinanceDimension1,
    CASE WHEN FinanceDimension2 IS NULL OR FinanceDimension2 = '' THEN 'NA' ELSE FinanceDimension2 END AS FinanceDimension2,
    CASE WHEN Branch IS NULL OR Branch = '' THEN 'NA' ELSE Branch END AS FinanceDimension3,
    CASE WHEN CostCenter IS NULL OR CostCenter = '' THEN 'NA' ELSE CostCenter END AS FinanceDimension4,
    CASE WHEN FCLoanType IS NULL OR FCLoanType = '' THEN 'NA' ELSE FCLoanType END AS FinanceDimension5,
    CASE WHEN FinanceDimension6 IS NULL OR FinanceDimension6 = '' THEN 'NA' ELSE FinanceDimension6 END AS FinanceDimension6,
    CASE WHEN FinanceDimension7 IS NULL OR FinanceDimension7 = '' THEN 'NA' ELSE FinanceDimension7 END AS FinanceDimension7,
    CASE WHEN FinanceDimension8 IS NULL OR FinanceDimension8 = '' THEN 'NA' ELSE FinanceDimension8 END AS FinanceDimension8,
    CASE WHEN InterCompany IS NULL OR InterCompany = '' THEN 'NA' ELSE InterCompany END AS FinanceDimension9,
    CASE WHEN FinanceDimension10 IS NULL OR FinanceDimension10 = '' THEN 'NA' ELSE FinanceDimension10 END AS FinanceDimension10,
    FunctionalAmount,
    ProjectAmount,
    UnitsAmount,
    "ADB_MTD" AS "ADBMTD",
    "ADB_QTD" AS "ADBQTD",
    "ADB_YTD" AS "ADBYTD"
FROM (
    SELECT  
        FEG,
        Scenario,
        Company,
        Ledger,
        System,
        Currency,
        EntityYearPeriod,
        Account,
        Project,
        PeriodEndingDate,
        Entity,
        FinanceDimension2,
        Branch,
        CostCenter,
        FCLoanType,
        FinanceDimension6,
        FinanceDimension7,
        FinanceDimension8,
        InterCompany,
        FinanceDimension10,
        SUM(CAST(FunctionalAmount AS REAL)) AS FunctionalAmount,
        SUM(CAST(ProjectAmount AS REAL)) AS ProjectAmount,
        SUM(CAST(UnitsAmount AS REAL)) AS UnitsAmount,
        SUM(CAST(ADB_MTD AS REAL)) AS "ADB_MTD",
        SUM(CAST(ADB_QTD AS REAL)) AS "ADB_QTD",
        SUM(CAST(ADB_YTD AS REAL)) AS "ADB_YTD"
    FROM (
        SELECT
            IFNULL(FEG,'') AS FEG,
            IFNULL(Scenario,'') AS Scenario,
            IFNULL(Company,'') AS Company,
            IFNULL(Ledger,'') AS Ledger,
            IFNULL(System,'') AS System,
            IFNULL(Currency,'') AS Currency,
            IFNULL(EntityYearPeriod,'') AS EntityYearPeriod,
            CASE 
                WHEN INSTR(Account, '-') > 0 THEN  
                    SUBSTR('00000' || SUBSTR(Account, 1, INSTR(Account, '-')), -5) || SUBSTR('0000' || SUBSTR(Account, INSTR(Account, '-') + 1, 4), -4)
                ELSE
                    SUBSTR('000000000' || IFNULL(Account,'') || '0000', -9)
            END AS Account,
            IFNULL(Project,'') AS Project,
            CASE 
                WHEN INSTR(PeriodEndingDate, '//') = 0 THEN PeriodEndingDate
                ELSE '01/01' || SUBSTR(PeriodEndingDate, -5)
            END AS PeriodEndingDate,
            IFNULL(Entity,'') AS Entity,
            IFNULL(FinanceDimension2,'') AS FinanceDimension2,
            IFNULL(Branch,'') AS Branch,
            IFNULL(CostCenter,'') AS CostCenter,
            IFNULL(FCLoanType,'') AS FCLoanType,
            IFNULL(FinanceDimension6,'') AS FinanceDimension6,
            IFNULL(FinanceDimension7,'') AS FinanceDimension7,
            IFNULL(FinanceDimension8,'') AS FinanceDimension8,
            IFNULL(InterCompany,'') AS InterCompany,
            IFNULL(FinanceDimension10,'') AS FinanceDimension10,
            IFNULL(FunctionalAmount,0) AS FunctionalAmount,
            IFNULL(ProjectAmount,0) AS ProjectAmount,
            IFNULL(UnitsAmount,0) AS UnitsAmount,
            IFNULL(ADB_MTD,0) AS ADB_MTD,
            IFNULL(ADB_QTD,0) AS ADB_QTD,
            IFNULL(ADB_YTD,0) AS ADB_YTD
        FROM BODData
    )
    GROUP BY
        FEG,
        Scenario,
        Company,
        Ledger,
        System,
        Currency,
        EntityYearPeriod,
        Account,
        Project,
        PeriodEndingDate,
        Entity,
        FinanceDimension2,
        Branch,
        CostCenter,
        FCLoanType,
        FinanceDimension6,
        FinanceDimension7,
        FinanceDimension8,
        InterCompany,
        FinanceDimension10
)
ORDER BY 
    EntityYearPeriod,
    Account,
    Project,
    Company,
    System,
    Entity,
    FinanceDimension2,
    Branch,
    CostCenter,
    FCLoanType
