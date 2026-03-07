# Client Handover Workflow Guide

## Overview

This guide provides step-by-step instructions for generating client handover documentation using the stateless pipeline architecture.

## Prerequisites

- LPD file (required)
- ANA-050 specification (optional but recommended)
- Work unit log file (optional but recommended for production validation)
- Python 3.x installed
- Required Python packages: `openpyxl`, `python-docx`, `lxml`

## Complete Workflow

### Step 1: Organize Files

Create a project structure:

```
Projects/
└── {Client}/
    └── {RICE_Item}/
        ├── {ProcessName}.lpd
        ├── ANA-050_{Description}.docx
        └── {WorkUnit}_log.txt
```

Example:
```
Projects/
└── FPI/
    └── MatchReport/
        ├── MatchReport_Outbound.lpd
        ├── ANA-050_Analysis_Outgoing_Match_Report.docx
        └── 36829_log.txt
```

### Step 2: Phase 0 - Preprocessing (MANDATORY)

**Purpose**: Extract and structure data from source files

**Command**:
```bash
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py \
  "Projects/{Client}/{RICE}/Process.lpd" \
  "Projects/{Client}/{RICE}/ANA-050_Spec.docx" \
  "Projects/{Client}/{RICE}/WorkUnit_log.txt"
```

**Example**:
```bash
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py \
  "Projects/FPI/MatchReport/MatchReport_Outbound.lpd" \
  "Projects/FPI/MatchReport/ANA-050_Analysis_Outgoing_Match_Report.docx" \
  "Projects/FPI/MatchReport/36829_log.txt"
```

**Output Files** (in `Temp/` folder):
- `spec_raw.json` - Extracted ANA-050 content
- `lpd_structure.json` - Extracted LPD process structure
- `metrics_summary.json` - Pre-calculated metrics
- `wu_log_data.json` - Extracted work unit log data (if provided)

**Verification**:
```bash
# Check files exist
ls Temp/*.json

# Check file sizes (should be > 0 bytes)
ls -lh Temp/*.json
```

### Step 3: Phase 1 - Business Requirements Analysis

**Purpose**: Extract business objectives, requirements, stakeholders, and integrations

**Input**: `Temp/spec_raw.json`

**Task**: Create `Temp/business_analysis.json` with:

```json
{
  "business_objectives": [
    "Extract General Ledger Total data from FSM for external match reporting",
    "Provide automated file-based integration for multiple Finance Enterprise Groups"
  ],
  "business_requirements": [
    {
      "requirement": "File-triggered data extraction process",
      "description": "IPA process must be triggered by file channel when input file is dropped",
      "source": "Requirements Details section"
    }
  ],
  "stakeholders": [
    {
      "name": "FPI Technical Team",
      "role": "Process owner and orchestration management",
      "involvement": "Monitors file channels, manages orchestration tool"
    }
  ],
  "integrations": [
    {
      "system": "FSM Landmark",
      "business_class": "GeneralLedgerTotal",
      "purpose": "Source system for GL balance data extraction"
    }
  ],
  "key_features": [
    "Automated file-triggered GL data extraction",
    "Multi-association support via folder-based FEG identification"
  ]
}
```

**Analysis Steps**:
1. Read `spec_raw.json` completely
2. Extract business objectives from Overview section
3. Extract requirements from Requirements Details section
4. Identify stakeholders from Reviewers and document properties
5. Identify integrations from Proposed Solution section
6. Generate key features from objectives and integrations

### Step 4: Phase 2 - Workflow Architecture Analysis

**Purpose**: Map process workflows, decision points, and activity descriptions

**Input**: `Temp/lpd_structure.json`

**Task**: Create `Temp/workflow_analysis.json` with:

```json
{
  "workflow_steps": [
    {
      "step": 1,
      "activity_id": "ReadInput",
      "activity_type": "File Read",
      "description": "Read run date from input file",
      "business_purpose": "Retrieve the period date that determines which GL data to extract"
    }
  ],
  "decision_nodes": [
    {
      "activity_id": "Branch4660",
      "decision_type": "Date Validation",
      "conditions": [
        {
          "name": "ValidDate",
          "description": "Run date is in valid MM/DD/YYYY format",
          "next_step": "GetAccessToken"
        }
      ]
    }
  ],
  "activity_descriptions": {
    "ReadInput": "Read run date from input file dropped in FEG-specific Input folder",
    "Assign1540": "Parse and validate run date, convert to Julian format, identify FEG"
  },
  "activity_purposes": {
    "ReadInput": "Triggered when FPI orchestration tool drops date file in Input folder",
    "Assign1540": "Runs after reading input file - validates date and identifies association"
  }
}
```

**CRITICAL**: `activity_descriptions` and `activity_purposes` are the PRIMARY source for activity documentation. The assembly script uses this priority order:

1. **PRIORITY 1**: `activity_descriptions[activity_id]` and `activity_purposes[activity_id]`
2. **PRIORITY 2**: `workflow_steps` matching (legacy fallback)
3. **PRIORITY 3**: Generic type-based descriptions (last resort)

**Analysis Steps**:
1. **Check process count**: If `lpd_structure.json` has multiple processes (>1), use chunked processing
2. **For Single Process**: Analyze `lpd_structure.json` directly
3. **For Multiple Processes** (RECOMMENDED for 3+ processes or 300+ total activities):
   - Run `python ReusableTools/IPA_ClientHandover/split_lpd_by_process.py`
   - This creates `lpd_process_1.json`, `lpd_process_2.json`, etc.
   - Analyze EACH process file individually (prevents context overload)
   - Merge results into `workflow_analysis.json`
4. For EACH activity in EACH process:
   - ASSGN: Analyze JavaScript code to describe transformations
   - WEBRN/LM: Analyze SQL queries and API endpoints
   - BRANCH: Analyze branch conditions to describe routing logic
   - Timer: Describe wait duration and purpose
   - ACCFIL: Describe file operations
   - SUBPROC: Describe subprocess purpose
5. Create `activity_descriptions` with specific, business-friendly descriptions
6. Create `activity_purposes` with when/why explanations
7. Map workflow steps in sequential order
8. Identify decision nodes and their conditions

**Multi-Process Example**:
```bash
# Step 1: Split combined LPD structure
python ReusableTools/IPA_ClientHandover/split_lpd_by_process.py

# Step 2: Analyze each process individually
# Process 1 (450 activities) - manageable context
# Process 2 (35 activities) - manageable context  
# Process 3 (45 activities) - manageable context

# Step 3: Merge results
python Temp/merge_activity_descriptions.py
```

### Step 5: Phase 3 - Configuration & Technical Components

**Purpose**: Document configuration dependencies and settings

**Input**: `Temp/lpd_structure.json`, `Temp/metrics_summary.json`

**Task**: Create `Temp/configuration_analysis.json` with:

```json
{
  "file_channel_config": [
    {
      "variable": "FileChannelFileName",
      "purpose": "Name of the input file dropped by orchestration tool",
      "example_value": "20240315.txt",
      "modification_instructions": "File channel configuration in Process Server Administrator"
    }
  ],
  "process_variables": [
    {
      "variable": "OauthCreds",
      "purpose": "OAuth2 credentials for Data Fabric API authentication",
      "example_value": "{\"client_id\":\"...\",\"client_secret\":\"...\"}",
      "modification_instructions": "Update System Configuration > Interface > API_AuthCred_{FEG}"
    }
  ],
  "configuration_dependencies": [
    {
      "config_set": "Interface",
      "property": "API_AuthCred_AGW",
      "purpose": "OAuth2 credentials for AGW Finance Enterprise Group",
      "modification_instructions": "Update in System Configuration > Interface"
    }
  ]
}
```

**CRITICAL**: These three structures are REQUIRED for System Configuration sheet. See `PHASE3_CONFIGURATION_GUIDE.md` for detailed extraction patterns.

**Analysis Steps**:
1. Read `lpd_structure.json` completely
2. Extract file channel variables from START activity
3. Extract process variables from START activity initialization
4. Extract configuration dependencies from `_configuration.` references
5. For each configuration item, provide:
   - Variable/property name
   - Purpose (what it's used for)
   - Example value (realistic value)
   - Modification instructions (how to change it)

### Step 6: Phase 4 - Risk & Compliance Review

**Purpose**: Identify technical risks, maintenance concerns, and compliance requirements

**Input**: All prior JSON outputs

**Task**: Create `Temp/risk_assessment.json` with:

```json
{
  "technical_risks": [
    {
      "risk": "OAuth Token Expiration During Execution",
      "severity": "Low",
      "likelihood": "Low",
      "impact": "Process obtains fresh token at start",
      "mitigation": "Process includes retry logic for token acquisition"
    }
  ],
  "maintenance_risks": [
    {
      "risk": "Adding New Finance Enterprise Groups",
      "severity": "Medium",
      "likelihood": "Medium",
      "impact": "Requires code changes to credential selection logic",
      "mitigation": "Document FEG addition procedure"
    }
  ],
  "scalability_concerns": [
    {
      "concern": "Growing Data Volumes",
      "current_state": "Process handles a few thousand records",
      "future_state": "Data volume may grow during period close",
      "recommendation": "Monitor query execution times and record counts"
    }
  ]
}
```

**Analysis Steps**:
1. Review all prior analysis outputs
2. Identify technical risks (OAuth, API, query timeouts)
3. Identify maintenance risks (adding FEGs, credential rotation)
4. Identify scalability concerns (data volume, concurrent execution)
5. Document compliance requirements (security, audit trail)
6. Provide mitigation strategies for each risk

### Step 7: Validate Analysis JSONs

**Purpose**: Verify JSON structure before report assembly

**Command**:
```bash
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

**Expected Output**:
```
✓ lpd_structure.json: Valid
✓ metrics_summary.json: Valid
✓ business_analysis.json: Valid
✓ workflow_analysis.json: Valid
✓ configuration_analysis.json: Valid
  - file_channel_config: 3 items
  - process_variables: 10 items
  - configuration_dependencies: 7 items
✓ risk_assessment.json: Valid
```

**If validation fails**: Fix the reported issues before proceeding to Phase 5.

### Step 8: Phase 5 - Report Assembly

**Purpose**: Generate final Excel report

**Command**:
```bash
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py {Client} {RICE_Item}
```

**Example**:
```bash
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py FPI MatchReport
```

**Output**: `Client_Handover_Results/{Client}_{RICE_Item}_ClientHandover_{timestamp}.xlsx`

**Report Sheets**:
- 📊 Executive Summary
- 📋 Business Requirements
- ✅ Production Validation
- ⚙️ System Configuration
- 📚 Activity Node Guide
- ⚙️ Process_{ProcessName} (one per process)
- 🔧 Maintenance Guide

### Step 9: Validate Generated Report

**Purpose**: Verify report quality and completeness

**Command**:
```bash
python ReusableTools/IPA_ClientHandover/validate_report.py "Client_Handover_Results/{Client}_{RICE_Item}.xlsx"
```

**Expected Output**:
```
✓ Executive Summary: 13 rows
✓ Business Requirements: 9 rows
✓ Production Validation: 30 rows
✓ System Configuration: 34 rows
✓ Activity Node Guide: 11 rows
✓ Maintenance Guide: 28 rows
✓ Process_1: 42 rows

✅ REPORT IS VALID - All critical sections have data
```

## Multi-Process Workflow

For RICE items with multiple processes:

### Step 1: Run Phase 0 for Each Process

```bash
# Process 1
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py \
  "Projects/{Client}/{RICE}/Process1.lpd" \
  "Projects/{Client}/{RICE}/ANA-050_Spec.docx" \
  "Projects/{Client}/{RICE}/WU1_log.txt" \
  "Temp/Process1"

# Process 2
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py \
  "Projects/{Client}/{RICE}/Process2.lpd" \
  "Projects/{Client}/{RICE}/ANA-050_Spec.docx" \
  "Projects/{Client}/{RICE}/WU2_log.txt" \
  "Temp/Process2"
```

### Step 2: Consolidate Analysis

Create consolidated analysis JSONs that merge data from all processes:

- `business_analysis.json` - RICE-level objectives (same for all processes)
- `workflow_analysis.json` - Process-specific workflows (dict of dicts)
- `configuration_analysis.json` - Consolidated configuration (merge all)
- `risk_assessment.json` - Consolidated risks (merge all)

### Step 3: Run Phase 5 with Consolidated Data

```bash
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py {Client} {RICE_Item}
```

**Result**: ONE report with multiple Process sheets.

## Troubleshooting

See `TROUBLESHOOTING.md` for common issues and solutions.

## Quick Reference

| Phase | Input | Output | Duration |
|-------|-------|--------|----------|
| 0 | LPD, Spec, WU log | 4 JSON files | 2-3s |
| 1 | spec_raw.json | business_analysis.json | 30-45s |
| 2 | lpd_structure.json | workflow_analysis.json | 30-45s |
| 3 | lpd_structure.json, metrics_summary.json | configuration_analysis.json | 30-45s |
| 4 | All prior JSONs | risk_assessment.json | 30-45s |
| 5 | All JSONs | Excel report | 5-10s |

**Total Time**: ~3-4 minutes per process

## Related Documentation

- `JSON_SCHEMAS.md` - Complete JSON structure reference
- `PHASE3_CONFIGURATION_GUIDE.md` - Detailed Phase 3 extraction patterns
- `TROUBLESHOOTING.md` - Common issues and solutions
- `TOOLS_README.md` - Tool usage and examples
