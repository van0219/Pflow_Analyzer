# ION OneView BOD Download Tool

Download and analyze BOD (Business Object Document) data from Infor ION OneView API for data quality investigations.

## Purpose

This tool is used to investigate data quality issues by:
1. Downloading raw BOD data objects from ION OneView
2. Loading them into a SQLite database for analysis
3. **Comparing BOD data against IPA output files** to verify data integrity
4. Running queries to identify anomalies (e.g., zero values, missing data)
5. Generating comparison reports that prove where issues originated

## Use Cases

- **GLSummary Zero Value Investigation**: Download BODs from BIFSM/BICE, compare against GLSummary.csv to verify if zeros came from source data or were introduced by IPA
- **Data Flow Verification**: Trace data from GLTOT cube → Application Engine → BICE → ION → Data Lake → IPA Output
- **Period/Ledger Analysis**: Identify which periods or ledgers have data quality issues
- **IPA Output Validation**: Prove whether IPA correctly extracted and transformed the source data

## Limitations

### Single BOD Type Per Investigation

This tool supports **one BOD type (document name) per investigation**. Each investigation folder contains:
- One set of downloaded BOD files (same schema)
- One SQLite table (`BODData`)
- One SQL transformation query

**Why this limitation?**
- Most data quality investigations trace back to a single source BOD
- Each BOD type has a different schema (different fields/columns)
- Keeping it simple handles 90%+ of use cases

**For multi-BOD analysis** (e.g., IPA joins `FPI_FCE_IDL_GLTotals` + `FPI_FCE_IDL_GLAccounts`):
1. Run separate investigations for each BOD type
2. Ask Kiro to create a custom analysis script that:
   - Connects to multiple SQLite databases
   - Joins the data as needed
   - Performs the combined analysis

This approach keeps the tool simple while still supporting complex scenarios through custom scripts.

## Folder Structure

```
ION_BOD_Download/
├── ion_bod_downloader.py   # Main download script
├── bod_analyzer.py         # SQLite loader, analyzer, and comparison tool
├── config/
│   ├── CLIENT1_PRD.ionapi  # Production credentials
│   └── ...
└── <investigation_name>/   # One folder per investigation (self-contained)
    ├── bod_data.db         # SQLite database (all BOD types as separate tables)
    ├── GLSummary_Dec15.csv # Comparison file (IPA output being investigated)
    ├── GLSummary_Dec12.csv # Optional: Known good baseline file
    ├── downloads/          # Downloaded BOD files
    │   ├── bod_0001_xxx.json   # Downloaded BOD files
    │   └── message_ids.json    # List of downloaded MessageIDs
    ├── sql/                # SQL queries for this investigation
    │   ├── original_query.sql      # User-provided IPA SQL (Compass syntax)
    │   └── transformation.sql      # Kiro-generated SQLite-compatible version
    └── reports/            # Analysis and comparison reports
        └── BOD_Comparison_Report.xlsx
```

## File Upload Locations

When using this tool, you may need to upload files. Here are the exact paths:

| File Type | Upload To | Notes |
|-----------|-----------|-------|
| `.ionapi` credentials | `ReusableTools/ION_BOD_Download/config/` | e.g., `CLIENT_PRD.ionapi` |
| **Comparison file(s)** | `ReusableTools/ION_BOD_Download/<investigation_name>/` | e.g., `GLSummary_Dec15.csv` - the IPA output being investigated |
| Baseline file (optional) | `ReusableTools/ION_BOD_Download/<investigation_name>/` | e.g., `GLSummary_Dec12.csv` - known good file for comparison |
| Original IPA SQL (Optional) | `ReusableTools/ION_BOD_Download/original_query.sql` | Kiro will move it to the investigation's `sql/` folder after creation |

**IMPORTANT - Comparison File Requirement:**
- The comparison file is **REQUIRED** for a complete investigation
- Without it, you can only analyze BOD data in isolation (no proof of where issues originated)
- The investigation folder is created first, then you upload the comparison file(s) there
- Common comparison files: GLSummary.csv, MatchReport.csv, or any IPA output file

**Note on SQL file**: Since the investigation folder doesn't exist yet when you start, place the SQL file in the main `ION_BOD_Download/` folder. Kiro will:
1. Create the investigation folder structure
2. Move `original_query.sql` to `<investigation>/sql/original_query.sql`
3. Convert it to SQLite syntax as `<investigation>/sql/transformation.sql`

## Multi-Environment Support

Each FSM environment has different OAuth2 credentials. Store multiple `.ionapi` files in the `config/` folder:

| File | Environment |
|------|-------------|
| `CLIENT_PRD.ionapi` | Production |
| `CLIENT_TST.ionapi` | Test |
| `CLIENT_TRN.ionapi` | Training |
| `CLIENT_AX1.ionapi` | Sandbox |

The `--ionapi` parameter is **required** - you must specify which credentials file to use for each investigation.

## Prerequisites

- Python 3.8+
- Required packages: `requests`, `pandas`, `openpyxl`
- Valid `.ionapi` credentials file from Infor OS

## Usage

### Via Kiro Agent Hook (Recommended)

1. Click the "ION BOD Investigation" hook in the Agent Hooks panel
2. Kiro will prompt you for ALL parameters upfront:
   - `.ionapi` credentials file (e.g., `ReusableTools/ION_BOD_Download/config/CLIENT_PRD.ionapi`)
   - Document name (e.g., `FPI_FCE_IDL_GLTotals`)
   - Date range in **Manila time** (start and end)
   - Investigation name (for subfolder)
   - **Comparison file(s)** - the IPA output file(s) to compare against (REQUIRED)
   - **Optional**: IPA SQL query for transformation (must be provided BEFORE investigation begins if needed)
3. Kiro will create the investigation folder, then ask you to upload the comparison file(s)
4. Kiro will convert Manila time to UTC, download BODs, load into SQLite
5. Kiro will compare BOD data against your comparison file(s) and generate a comparison report

### Via Command Line

```bash
# Download BODs (note: command line still uses UTC format)
# Manila time 2025-12-16 10:49:00 = UTC 2025-12-16T02:49:00.000Z
python ion_bod_downloader.py \
    --ionapi config/IMS.ionapi \
    --doc-name FPI_FCE_IDL_GLTotals \
    --start "2025-12-16T02:49:00.000Z" \
    --end "2025-12-16T03:00:00.000Z" \
    --output dec15_investigation/downloads

# Analyze downloaded BODs (raw data only - no comparison)
python bod_analyzer.py \
    --input dec15_investigation/downloads \
    --output dec15_investigation/reports/analysis.xlsx

# Analyze with SQL aggregation (matches IPA output)
python bod_analyzer.py \
    --input dec15_investigation/downloads \
    --sql dec15_investigation/sql/transformation.sql \
    --output dec15_investigation/reports/analysis_aggregated.xlsx

# Compare BOD data against IPA output file (RECOMMENDED)
python bod_analyzer.py \
    --input dec15_investigation/downloads \
    --sql dec15_investigation/sql/transformation.sql \
    --compare dec15_investigation/GLSummary_Dec15.csv \
    --output dec15_investigation/reports/comparison_report.xlsx
```

### Timezone Note

- **Via Kiro Hook**: Provide times in **Manila time (UTC+8)** - Kiro handles the conversion
- **Via Command Line**: Use **UTC format** directly (e.g., `2025-12-16T02:49:00.000Z`)
- **Conversion**: Manila time - 8 hours = UTC (e.g., Manila 10:49 AM = UTC 02:49)

### Custom SQL Transformation (Optional - Provide BEFORE Investigation)

If your IPA process uses a SQL query to transform the raw BOD data (aggregation, column selection, field concatenation, null handling, etc.), you can provide that SQL query to get an accurate apples-to-apples comparison with the IPA output.

**IMPORTANT**: The SQL query must be provided BEFORE the investigation begins, not after. This is parameter #6 in the investigation setup.

**When to provide a SQL file:**
- Your IPA process transforms the data (GROUP BY, CASE statements, field formatting)
- You want to compare BOD data with the IPA output (e.g., GLSummary.csv)
- Record counts or field values differ between raw BOD and IPA output

**When NOT needed:**
- You just want to analyze raw BOD data for patterns
- Your IPA doesn't transform the data
- You're investigating data at the source level

**How to provide the SQL:**

1. **File method (recommended)**: Place your original IPA SQL file at:
   - Path: `ReusableTools/ION_BOD_Download/original_query.sql`
   - Kiro will move it to the investigation folder after creation
2. **Chat method**: Provide the SQL directly when Kiro asks for parameter #6
   - Kiro will save it as `original_query.sql` in the investigation folder

**Example workflow:**

1. User places `original_query.sql` in `ReusableTools/ION_BOD_Download/` (or provides SQL in chat)
2. Kiro creates the investigation folder structure
3. Kiro moves/saves the SQL as `<investigation_name>/sql/original_query.sql`
4. Kiro converts to SQLite syntax and saves as `<investigation_name>/sql/transformation.sql`
5. Analyzer uses `transformation.sql` for analysis
6. Both files are kept for reference/debugging

**Sample SQL files:**

- See `GLSummary_Dec15_Investigation/sql/` for a real-world example

**Important Notes:**
- Provide your **original IPA SQL** - Kiro will handle the SQLite conversion
- Both original and transformed SQL are kept for investigation purposes
- If analysis results don't match expected output, the SQL logic can be reviewed

## API Details

### ION OneView API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/IONSERVICES/oneviewapi/data` | Query for BOD MessageIDs |
| `/IONSERVICES/oneviewapi/data/streamDocumentPayload` | Download BOD payload |
| `/IONSERVICES/oneviewapi/data/facets` | Get available field values |

### Filter Syntax

```
(document_sent_from eq 'lid://infor.bice.bice') and 
(document_name eq 'FPI_FCE_IDL_GLTotals') and 
message_date range [2025-12-16T02:49:00.000Z, 2025-12-16T03:00:00.000Z]
```

### Common Source Filters

| Source | Description |
|--------|-------------|
| `lid://infor.bice.bice` | BICE (BI Cube Extract) - data from GLTOT cube |
| `lid://infor.ipa.ipa` | IPA processes |
| `lid://infor.fsm.fsm` | FSM application |

## Output Files

### Downloaded BODs
- `bod_0001_<message_id>.json` - Individual BOD payloads (NDJSON format)
- `message_ids.json` - List of all downloaded MessageIDs

### Analysis Output
- `bod_data.db` - SQLite database with all BOD records
- `BOD_Comparison_Report.xlsx` - Excel report with comparison analysis

### Comparison Report Contents
The comparison report includes:
1. **Summary** - Record counts, analysis mode, comparison file info
2. **Zero Analysis** - Zero value breakdown by ledger/period for both BOD and IPA output
3. **Comparison Results** - Side-by-side comparison showing:
   - Records in BOD but not in IPA output
   - Records in IPA output but not in BOD
   - Zero value discrepancies
4. **Conclusion** - Clear statement of whether zeros came from source or were introduced by IPA

## Example Investigation

### GLSummary Dec 15 Zero Value Issue

1. **Problem**: Client reported zeros in FunctionalAmount for Nov 2025 CORE ledger in GLSummary.csv
2. **Comparison File**: Uploaded `GLSummary_Dec15.csv` (the problematic file) to investigation folder
3. **Downloaded**: 581 BODs from Dec 16 02:49-03:00 UTC (Q4 2025 extraction)
4. **BOD Analysis**: 86.99% of Nov 2025 CORE records had zero FunctionalAmount in raw BOD data
5. **Comparison Result**: GLSummary.csv had exactly 865 non-zero records for Nov 2025 CORE - matching BOD data
6. **Conclusion**: Zeros came from source (GLTOT cube), not IPA processing - IPA correctly extracted the data

### Investigation Workflow

```
1. User provides: GLSummary_Dec15.csv (file with zeros)
2. Tool downloads: 581 BODs from ION OneView
3. Tool compares: BOD data vs GLSummary_Dec15.csv
4. Tool reports:
   - BOD Nov 2025 CORE: 6,650 records, 5,785 zeros (86.99%)
   - GLSummary Nov 2025 CORE: 6,650 records, 5,785 zeros (86.99%)
   - Match: YES - zeros existed in source data
5. Conclusion: IPA is NOT at fault - zeros came from GLTOT cube
```

## Troubleshooting

### Authentication Failed
- Verify `.ionapi` file has valid credentials
- Check if credentials have expired
- Ensure tenant ID matches the environment

### No BODs Found
- Verify date range is in UTC format
- Check document name spelling
- Try broader date range
- Use facets API to verify available document types

### Download Failures (406 Error)
- Some BODs may not be downloadable via API
- Script will continue with remaining BODs
- Check `message_ids.json` for failed downloads

## Related Documentation

- See `.kiro/steering/07_Infor_OS_Data_Fabric_Guide.md` for ION API details
- See `.kiro/steering/02_Work_Unit_Analysis.md` for data tracing methodology
