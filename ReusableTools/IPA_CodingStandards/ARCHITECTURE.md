# IPA Coding Standards - Domain-Segmented Architecture

## Problem Statement

Analyzing large IPA processes (450+ activities, 130+ JavaScript blocks) caused context overload:
- Full IPA JSON: 6000+ lines
- AI tried to analyze everything at once
- Context window exhausted
- Shallow or incomplete analysis

## Solution: Domain-Segmented AI Analysis

Instead of analyzing everything in one pass, we:
1. Extract IPA data (Python)
2. **Organize by domain** (Python) - 5 small files
3. **Analyze each domain separately** (AI) - One at a time
4. **Merge violations** (Python) - Single master file
5. Generate ONE Excel report (Python)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  LPD File (XML)                                             │
│  InvoiceApproval_APIA_NONPOROUTING.lpd                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Extract (Python)                                   │
│  Tool: extract_lpd_data.py                                  │
│  Output: ProcessName_lpd_data.json (6000 lines)             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Organize by Domain (Python) ← NEW!                │
│  Tool: organize_by_domain.py                                │
│  Outputs 5 domain files:                                    │
│  ├─ ProcessName_domain_naming.json (250 lines)              │
│  ├─ ProcessName_domain_javascript.json (400 lines)          │
│  ├─ ProcessName_domain_sql.json (200 lines)                 │
│  ├─ ProcessName_domain_errorhandling.json (150 lines)       │
│  └─ ProcessName_domain_structure.json (100 lines)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: AI Analyzes Domain 1 (Naming)                     │
│  Reads: ProcessName_domain_naming.json (250 lines)          │
│  Analyzes: Filename, node names, config sets                │
│  Outputs: ProcessName_violations_naming.json                │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: AI Analyzes Domain 2 (JavaScript)                 │
│  Reads: ProcessName_domain_javascript.json (400 lines)      │
│  Analyzes: ES6, performance, function order                 │
│  Outputs: ProcessName_violations_javascript.json            │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: AI Analyzes Domain 3 (SQL)                        │
│  Reads: ProcessName_domain_sql.json (200 lines)             │
│  Analyzes: Pagination, Compass SQL, SELECT *                │
│  Outputs: ProcessName_violations_sql.json                   │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: AI Analyzes Domain 4 (Error Handling)             │
│  Reads: ProcessName_domain_errorhandling.json (150 lines)   │
│  Analyzes: OnError tabs, GetWorkUnitErrors                  │
│  Outputs: ProcessName_violations_errorhandling.json         │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: AI Analyzes Domain 5 (Structure)                  │
│  Reads: ProcessName_domain_structure.json (100 lines)       │
│  Analyzes: Auto-restart, process type                       │
│  Outputs: ProcessName_violations_structure.json             │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 8: Merge Violations (Python)                         │
│  Tool: merge_violations.py                                  │
│  Inputs: 5 violation files                                  │
│  Output: ProcessName_master_violations.json                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 9: AI Builds ipa_data                                │
│  Reads: ProcessName_master_violations.json                  │
│  Builds: ipa_data dictionary for report                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 10: Generate Report (Python)                         │
│  Tool: ipa_coding_standards_template.py                     │
│  Output: ProcessName_CodingStandards_YYYYMMDD.xlsx          │
│  Sheets: Executive Dashboard, Action Items, Detailed Analysis│
└─────────────────────────────────────────────────────────────┘
```

## Domain Definitions

### 1. Naming Domain
**File**: `ProcessName_domain_naming.json`

**Data Organized**:
- Filename
- Node captions (all activities)
- Generic node patterns detected
- Config set names
- Hardcoded values detected

**AI Analyzes**:
- Rule 1.1.1: Filename format
- Rule 1.1.2: Node naming (descriptive vs generic)
- Rule 1.4.1: Config set naming (vendor-specific)
- Rule 1.4.3: Hardcoded values (should use ${...})

### 2. JavaScript Domain

**File**: `ProcessName_domain_javascript.json`

**Data Organized**:
- All JavaScript blocks
- ES6 features detected (let, const, arrow functions, etc.)
- Performance patterns detected (regex in loops, string concat)
- Function declarations
- Function declaration order
- Global variables on Start node

**Variable Scoping Rules**:
- **Start Node**: Variables are automatically global to entire process
  - Syntax: `variableName = value` (no `var` keyword)
  - Scope: Entire IPA process
  - Example: `vApproverList = ""`
  
- **Assign Nodes**: Use `var` for local variables
  - Syntax: `var variableName = value` (with `var` keyword)
  - Scope: Current JavaScript block only
  - Example: `var tempArray = data.split(',')`
  - Without `var`: Creates unintended global variable

**AI Analyzes**:
- Rule 1.2.1: Process variables initialized on Start node (not about `var` keyword)
- Rule 1.2.3: Functions declared early
- ES5 compliance (no ES6 features)
- Performance issues (regex compilation, string concatenation)
- Missing `var` in Assign nodes (creates unintended globals)

### 3. SQL Domain
**File**: `ProcessName_domain_sql.json`

**Data Organized**:
- All SQL queries
- Query types (SELECT, INSERT, UPDATE, DELETE)
- Compass SQL detection
- Pagination detection
- SELECT * detection
- WHERE clause detection

**AI Analyzes**:
- Rule 1.5.2: Pagination for large datasets
- Compass SQL best practices (from steering file 05)
- SELECT * usage
- Missing WHERE clauses
- Query optimization opportunities

### 4. Error Handling Domain
**File**: `ProcessName_domain_errorhandling.json`

**Data Organized**:
- Nodes requiring error handling (WEBRN, WEBRUN, ACCFIL, etc.)
- stopOnError flags
- GetWorkUnitErrors activity detection
- Error handling coverage percentage

**AI Analyzes**:
- Rule 1.3.1: OnError tabs (stopOnError=false)
- Rule 1.3.2: GetWorkUnitErrors activity node
- Error handling coverage

### 5. Structure Domain
**File**: `ProcessName_domain_structure.json`

**Data Organized**:
- Process name and type
- Auto-restart configuration
- Activity counts by type
- Process characteristics (user interaction, webservices, file access)

**AI Analyzes**:
- Auto-restart appropriateness (context-aware)
- Process type determination
- Activity distribution

## Separation of Concerns

### Python Responsibilities (Heavy Lifting)
- Extract data from LPD XML
- Parse and organize data by domain
- Detect patterns (ES6 keywords, generic names, SQL queries)
- Calculate statistics (counts, percentages)
- Merge violations from multiple domains
- Format Excel report

### AI Responsibilities (Analysis & Judgment)
- Interpret coding standards
- Determine if pattern is a violation
- Assign severity (High, Medium, Low)
- Provide recommendations
- Add business context
- Build executive narrative

### What Python Does NOT Do
- ❌ Decide violations
- ❌ Assign severity
- ❌ Make recommendations
- ❌ Perform judgment

### What AI Does NOT Do
- ❌ Parse XML
- ❌ Extract data
- ❌ Format Excel
- ❌ Merge files

## Benefits

### 1. No Context Overload
- AI reads 200-400 lines per domain (vs 6000 lines total)
- Each domain analyzed independently
- Context window never exhausted

### 2. Full Coverage
- All 5 domains analyzed
- No data skipped
- Comprehensive review

### 3. Consistent Results
- Python organizes data consistently
- AI applies standards consistently
- Repeatable analysis

### 4. Scalable
- Works for any process size
- Tested with 450 activities, 130 JS blocks
- No upper limit

### 5. One Report
- Multi-pass analysis → ONE master violations file
- ONE Excel report per process
- Professional artifact

## File Sizes

For BayCare APIA (450 activities, 130 JS blocks):

| File | Lines | AI Context |
|------|-------|------------|
| Original JSON | 6256 | ❌ Too large |
| Naming domain | ~250 | ✅ Small |
| JavaScript domain | ~400 | ✅ Medium |
| SQL domain | ~200 | ✅ Small |
| Error Handling domain | ~150 | ✅ Small |
| Structure domain | ~100 | ✅ Tiny |
| **Total if combined** | ~1100 | ✅ Manageable |
| **Reduction** | 82% | ✅ Success |

## Performance

| Step | Time | Notes |
|------|------|-------|
| Extract | ~1s | Per 12K lines LPD |
| Organize | ~2s | Split into 5 domains |
| AI Domain 1 | ~30-60s | Naming analysis |
| AI Domain 2 | ~30-60s | JavaScript analysis |
| AI Domain 3 | ~30-60s | SQL analysis |
| AI Domain 4 | ~30-60s | Error handling analysis |
| AI Domain 5 | ~30-60s | Structure analysis |
| Merge | ~1s | Combine violations |
| Report | ~10s | Generate Excel |
| **Total** | **3-6 min** | Per process |

## Report Structure

### Sheet 1: Executive Dashboard
- KPI cards (Total violations, High severity, Compliance %)
- Radar chart (5 domains)
- Key findings with status badges
- Summary metrics

### Sheet 2: Action Items
- All violations from all domains
- Sorted by severity (High → Medium → Low)
- Columns: Domain, Rule ID, Severity, Finding, Recommendation

### Sheet 3: Detailed Analysis
- **Violations ONLY** (not compliant items)
- Grouped by domain
- Detailed findings with code snippets
- Specific activities/nodes affected

## Usage

### Command Line

```bash
# Step 1: Extract
python -c "from ReusableTools.IPA_Analyzer.extract_lpd_data import extract_lpd_data; extract_lpd_data(['Process.lpd'], 'Temp/Process_lpd_data.json')"

# Step 2: Organize by domain
python ReusableTools/IPA_CodingStandards/organize_by_domain.py Temp/Process_lpd_data.json Temp/Process

# Steps 3-7: AI analyzes each domain (via hook)

# Step 8: Merge violations
python ReusableTools/IPA_CodingStandards/merge_violations.py Temp/Process

# Steps 9-10: AI builds ipa_data and generates report (via hook)
```

### Via Hook

User triggers hook → Workflow runs automatically → ONE Excel report generated

## Files

| File | Purpose |
|------|---------|
| `organize_by_domain.py` | Splits data into 5 domain files |
| `merge_violations.py` | Merges 5 violation files into master |
| `ipa_coding_standards_template.py` | Generates Excel report |
| `.kiro/hooks/coding-standards.kiro.hook` | Orchestrates workflow |
| `ARCHITECTURE.md` | This file |

## Version History

- **v32 (2026-02-22)**: Domain-segmented architecture implemented
- **v31 (2026-02-22)**: Multi-pass workflow with error handling
- **v30 (2026-02-22)**: Programmatic analyzer (deprecated)
- **v29 (2026-02-22)**: Original workflow (context overload issues)

## References

- Steering File 10: IPA Report Generation
- Steering File 00: General Rules (Recent Session Learnings)
- Hook: `.kiro/hooks/coding-standards.kiro.hook`
