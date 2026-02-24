-- RICE 13 SUMMARY SQL QUERY (FCE)
-- Original IPA SQL provided by user (Compass SQL syntax)
-- Investigation: GLSummary Dec 15 Zero Value Issue

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
        SUM(CAST(FunctionalAmount AS DECIMAL(18,2))) AS FunctionalAmount,
        SUM(CAST(ProjectAmount AS DECIMAL(18,2))) AS ProjectAmount,
        SUM(CAST(UnitsAmount AS DECIMAL(18,2))) AS UnitsAmount,
        SUM(CAST(ADB_MTD AS DECIMAL(18,2))) AS "ADB_MTD",
        SUM(CAST(ADB_QTD AS DECIMAL(18,2))) AS "ADB_QTD",
        SUM(CAST(ADB_YTD AS DECIMAL(18,2))) AS "ADB_YTD"
    FROM (
        SELECT
            ISNULL(FEG,'') AS FEG,
            ISNULL(Scenario,'') AS Scenario,
            ISNULL(Company,'') AS Company,
            ISNULL(Ledger,'') AS Ledger,
            ISNULL(System,'') AS System,
            ISNULL(Currency,'') AS Currency,
            ISNULL(EntityYearPeriod,'') AS EntityYearPeriod,
            CASE 
                WHEN CHARINDEX('-',Account) > 0 THEN  
                    LPAD(SUBSTRING(Account,1,CHARINDEX('-',Account)),5,'0') + LPAD(SUBSTRING(Account,CHARINDEX('-',Account)+1,4),4,'0')
                ELSE
                    LPAD((ISNULL(Account,'')+'0000'),9,'0')
            END AS Account,
            ISNULL(Project,'') AS Project,
            CASE 
                WHEN CHARINDEX('//',PeriodEndingDate) = 0 THEN PeriodEndingDate
                ELSE '01/01' + RIGHT(PeriodEndingDate,5)
            END AS PeriodEndingDate,
            ISNULL(Entity,'') AS Entity,
            ISNULL(FinanceDimension2,'') AS FinanceDimension2,
            ISNULL(Branch,'') AS Branch,
            ISNULL(CostCenter,'') AS CostCenter,
            ISNULL(FCLoanType,'') AS FCLoanType,
            ISNULL(FinanceDimension6,'') AS FinanceDimension6,
            ISNULL(FinanceDimension7,'') AS FinanceDimension7,
            ISNULL(FinanceDimension8,'') AS FinanceDimension8,
            ISNULL(InterCompany,'') AS InterCompany,
            ISNULL(FinanceDimension10,'') AS FinanceDimension10,
            ISNULL(FunctionalAmount,0) AS FunctionalAmount,
            ISNULL(ProjectAmount,0) AS ProjectAmount,
            ISNULL(UnitsAmount,0) AS UnitsAmount,
            ISNULL(ADB_MTD,0) AS ADB_MTD,
            ISNULL(ADB_QTD,0) AS ADB_QTD,
            ISNULL(ADB_YTD,0) AS ADB_YTD
        FROM <!BodType>  -- FPI_FCE_IDL_GLTotals
        <!SQL_QuarterFilter>
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
