# IPA Coding Standards Workflow Guide

Complete step-by-step workflow for generating coding standards analysis reports.

## Prerequisites

1. **LPD File**: Process definition file to analyze
2. **Project Standards** (optional): `Projects/<Client>/project_standards_<Client>.xlsx`
3. **Python Environment**: Python 3.x with required libraries

## Complete Workflow

### Step 1: File Organization

Organize your files in the Projects directory:

```
Projects/
└── <Client>/
    ├── <RICE>/
    │   └── ProcessName.lpd
    └── project_standards_<Client>.xlsx (optional)
```

### Step 2: Activate Skill

```text
/ipa-coding-standards
```

Or use:

```text
discloseContext(name="ipa-coding-standards")
```

### Step 3: User Selection (Interactive)

The skill will prompt you for:

1. **Client**: Select from Projects/ directory (e.g., "BayCare")
2. **RICE Item**: Select from client folder (e.g., "APIA")
3. **LPD File**: Select ONE process file (e.g., "InvoiceApproval_APIA_NONPOROUTING.lpd")
4. **Project Standards**: Confirm if `project_standards_<Client>.xlsx` exists

### Step 4: Phase 0 - Preprocessing (Python Only)

**Script**: `python ReusableTools/IPA_CodingStandards/preprocess_coding_standards.py <lpd_path> <client>`

**What it does:**
- Extracts LPD structure
- Calculates metrics (activity counts, JS blocks, SQL queries)
- Loads project standards (if available)
- Pre-calculates patterns (ES6, generic names, SQL types)

**Outputs:**
- `Temp/lpd_structure.json` - Complete LPD structure
- `Temp/metrics_summary.json` - Process metrics
- `Temp/project_standards.json` - Project-specific standards

**Verification:**
```powershell
Test-Path Temp/lpd_structure.json
Test-Path Temp/metrics_summary.json
Test-Path Temp/project_standards.json
```

### Step 5: Phase 1 - Naming Analysis (AI Incremental)

**Script**: `python ReusableTools/IPA_CodingStandards/build_naming_analysis.py`

**What it does:**
- Extracts naming data (filename, node captions, config sets)
- Creates chunks (50 nodes per chunk)
- AI analyzes each chunk
- Merges results

**Output:**
- `Temp/naming_analysis.json`

**Verification:**
```powershell
Test-Path Temp/naming_analysis.json
```

### Step 6: Phase 2 - JavaScript Analysis (AI Incremental)

**Script**: `python ReusableTools/IPA_CodingStandards/build_javascript_analysis.py`

**What it does:**
- Extracts JavaScript blocks
- Creates chunks (20 JS blocks per chunk)
- AI analyzes each chunk for ES5 compliance
- Merges results

**Output:**
- `Temp/javascript_analysis.json`

**Verification:**
```powershell
Test-Path Temp/javascript_analysis.json
```

### Step 7: Phase 3 - SQL Analysis (AI Incremental)

**Script**: `python ReusableTools/IPA_CodingStandards/build_sql_analysis.py`

**What it does:**
- Extracts SQL queries
- Creates chunks (30 queries per chunk)
- AI analyzes each chunk for Compass SQL compliance
- Merges results

**Output:**
- `Temp/sql_analysis.json`

**Verification:**
```powershell
Test-Path Temp/sql_analysis.json
```

### Step 8: Phase 4 - Error Handling Analysis (AI Incremental)

**Script**: `python ReusableTools/IPA_CodingStandards/build_errorhandling_analysis.py`

**What it does:**
- Extracts error-prone activities (WEBRN, WEBRUN, ACCFIL)
- Creates chunks (40 activities per chunk)
- AI analyzes each chunk for error handling
- Merges results

**Output:**
- `Temp/errorhandling_analysis.json`

**Verification:**
```powershell
Test-Path Temp/errorhandling_analysis.json
```

### Step 9: Phase 5 - Structure Analysis (AI Direct)

**What it does:**
- AI reads structure data directly (~100 lines)
- Analyzes auto-restart, process type, activity distribution
- Writes output

**Output:**
- `Temp/structure_analysis.json`

**Verification:**
```powershell
Test-Path Temp/structure_analysis.json
```

### Step 10: Phase 6 - Report Assembly (Python Only)

**Script**: `python ReusableTools/IPA_CodingStandards/assemble_coding_standards_report.py <client> <rice> <process_name>`

**What it does:**
- Loads all analysis JSONs
- Merges violations
- Builds ipa_data structure
- Generates Excel report

**Output:**
- `Coding_Standards_Results/<Client>_<RICE>_<ProcessName>_CodingStandards_<timestamp>.xlsx`

**Verification:**
```powershell
Test-Path Coding_Standards_Results/<Client>_<RICE>_<ProcessName>_CodingStandards_*.xlsx
```

## Troubleshooting

### Issue: "Process Count: 0"

**Cause**: Phase 0 was skipped or failed

**Fix**:
1. Verify LPD file path is correct
2. Re-run Phase 0
3. Check `lpd_structure.json` exists

### Issue: "No violations found"

**Cause**: Project standards not loaded or analysis incomplete

**Fix**:
1. Check `project_standards.json` exists
2. Verify all analysis JSONs exist (Phases 1-5)
3. Re-run failed phases

### Issue: "Missing domain analysis"

**Cause**: One of Phases 1-5 failed

**Fix**:
1. Check Temp/ folder for partial outputs
2. Identify which phase failed
3. Re-run that specific phase

## Quick Reference

| Phase | Script | Input | Output | Time |
|-------|--------|-------|--------|------|
| 0 | preprocess_coding_standards.py | LPD file | lpd_structure.json, metrics_summary.json, project_standards.json | ~2-3s |
| 1 | build_naming_analysis.py | lpd_structure.json | naming_analysis.json | ~1-2 min |
| 2 | build_javascript_analysis.py | lpd_structure.json | javascript_analysis.json | ~2-3 min |
| 3 | build_sql_analysis.py | lpd_structure.json | sql_analysis.json | ~1-2 min |
| 4 | build_errorhandling_analysis.py | lpd_structure.json | errorhandling_analysis.json | ~1-2 min |
| 5 | (AI direct) | lpd_structure.json, metrics_summary.json | structure_analysis.json | ~30-60s |
| 6 | assemble_coding_standards_report.py | All analysis JSONs | Excel report | ~5-10s |

**Total Time**: ~8-12 min per process

## Next Steps

After generating the report:

1. Review Executive Dashboard for overall quality
2. Check Action Items for prioritized violations
3. Review Detailed Analysis for code examples
4. Examine Process Flow for complexity insights
5. Share report with development team

---

For more detailed information, see:
- [`DOMAIN_ANALYSIS_GUIDE.md`](DOMAIN_ANALYSIS_GUIDE.md) - Domain-specific patterns
- [`JSON_SCHEMAS.md`](JSON_SCHEMAS.md) - JSON structure reference
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Common issues
