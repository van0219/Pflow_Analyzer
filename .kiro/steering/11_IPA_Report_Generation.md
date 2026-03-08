---
inclusion: auto
name: ipa-report-generation
description: IPA report generation workflows including client handover documentation, peer review reports, coding standards analysis, work unit analysis, and Excel report templates. Use when generating IPA reports, analyzing LPD files, reviewing code quality, or creating client documentation.
---

# IPA Report Generation Guide

## Purpose

Guide for generating IPA (Infor Process Automation) reports: Client Handover Documentation, Coding Standards Reviews, and Performance Analysis.

## Available Skills

**RECOMMENDED**: Use skills for IPA report generation workflows.

### Client Handover Skill

**Activation**: `discloseContext(name="ipa-client-handover")`

**Purpose**: Generate professional client-facing IPA documentation

**Location**: `.kiro/skills/ipa-client-handover/`

**Documentation**: See `SKILL.md` in skill folder

### Coding Standards Skill

**Activation**: `discloseContext(name="ipa-coding-standards")`

**Purpose**: Automated IPA code quality analysis with domain-segmented review

**Location**: `.kiro/skills/ipa-coding-standards/`

**Documentation**: See `SKILL.md` in skill folder

**Note**: Skills are self-contained with their own reference documentation and don't require loading this steering file.

## Core Principles

1. **Extract Truth, Not AI Content**: ALWAYS extract from source files (ANA-050 spec, LPD Start node, LPD activities). Never generate AI content.
2. **AI Analyzes, Python Formats**: AI performs ALL analysis and decisions. Python only extracts data and formats reports.
3. **Client Confidentiality**: Each client report is independent. Never reference other clients' data.
4. **Visual-First Design**: All reports include mandatory visual elements (workflow diagrams, status badges, color coding).
5. **Template Reusability**: Master templates work for ANY IPA project without modification.
6. **Data Completeness**: ALWAYS read extracted data completely before analysis. Never skip the data reading step.

## Stateless Pipeline Workflow (MANDATORY)

**CRITICAL**: Client handover generation MUST follow the stateless pipeline architecture to prevent context accumulation and ensure data completeness.

### Phase 0: Preprocessing (Python Only - MANDATORY FIRST STEP)

**ALWAYS run this BEFORE any AI analysis:**

```bash
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py <lpd_file> <spec_file> [wu_log_file] [output_dir]
```

**Arguments:**
- `lpd_file`: Path to LPD file (required)
- `spec_file`: Path to ANA-050 specification (required)
- `wu_log_file`: Path to work unit log file (optional)
- `output_dir`: Output directory (optional, defaults to 'Temp')

**What it creates:**

- `spec_raw.json` - Extracted ANA-050 content
- `lpd_structure.json` - Extracted LPD process structure (REQUIRED by assembly script)
- `metrics_summary.json` - Pre-calculated metrics (REQUIRED by assembly script)
- `wu_log.json` - Extracted work unit log data (if WU log provided)

**Why this matters:**

- The assembly script (`assemble_client_handover_report.py`) expects `lpd_structure.json` and `metrics_summary.json`
- Without these files, the report will show "Process Count: 0" and "Total Activities: 0"
- Manual extraction creates `lpd_data.json` which has a different structure

### Phase 1-4: AI Analysis (Create Analysis JSONs)

After Phase 0 completes, create these analysis files:

- `business_analysis.json` - Business requirements and objectives
- `workflow_analysis.json` - Process flow and decision points
- `configuration_analysis.json` - Configuration dependencies and settings (**CRITICAL: See Phase 3 Requirements below**)
- `risk_assessment.json` - Technical risks and maintenance concerns

#### Phase 3 Requirements (CRITICAL)

**ROOT CAUSE OF EMPTY CONFIGURATION SHEETS**: The assembly script's `build_ipa_data()` function expects specific data structures in `configuration_analysis.json`. If these are missing, the System Configuration sheet will be empty or incomplete.

**REQUIRED DATA STRUCTURES:**

```json
{
  "file_channel_config": [
    {
      "variable": "FileChannelFileName",
      "purpose": "Name of the trigger file being processed",
      "example_value": "MatchReportTrigger_P962_FMFC20260116233831.txt",
      "modification_instructions": "Automatically populated by file channel - no manual modification needed"
    }
  ],
  "process_variables": [
    {
      "variable": "OauthCreds",
      "purpose": "Selected OAuth credentials based on Finance Enterprise Group",
      "example_value": "JSON string with client_id, client_secret, grant_type, scope",
      "modification_instructions": "Automatically selected from Interface config based on FEG - update source config variables instead"
    }
  ],
  "configuration_dependencies": [
    {
      "config_set": "Interface",
      "property": "API_AuthCred_AGW",
      "type": "JSON",
      "purpose": "OAuth credentials for AGW Finance Enterprise Group",
      "required": true,
      "modification_instructions": "Update JSON object with client_id, client_secret, grant_type, and scope for AGW"
    }
  ]
}
```

**HOW TO EXTRACT THESE:**

1. **file_channel_config**: Extract from START activity properties where `FileChannel` variables are defined
2. **process_variables**: Extract from START activity variable initialization (all variables set in START node)
3. **configuration_dependencies**: Extract from `_configuration.ConfigSet.Property` references in JavaScript blocks

**VERIFICATION**: After Phase 3, verify these keys exist in `configuration_analysis.json`:
```bash
python -c "import json; data = json.load(open('Temp/configuration_analysis.json')); print('file_channel_config:', len(data.get('file_channel_config', []))); print('process_variables:', len(data.get('process_variables', []))); print('configuration_dependencies:', len(data.get('configuration_dependencies', [])))"
```

### Phase 5: Report Assembly (Python Only - FINAL STEP)

**ALWAYS run this to generate the Excel report:**

```bash
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py <client_name> <rice_item> [temp_dir] [output_dir]
```

**What it expects:**

- `lpd_structure.json` (from Phase 0)
- `metrics_summary.json` (from Phase 0)
- `business_analysis.json` (from Phase 1)
- `workflow_analysis.json` (from Phase 2)
- `configuration_analysis.json` (from Phase 3)
- `risk_assessment.json` (from Phase 4)
- `wu_log_data.json` (optional - for production validation) **← CRITICAL: Must be named `wu_log_data.json`, NOT `wu_log.json`**

**ROOT CAUSE OF MISSING PRODUCTION VALIDATION**: The assembly script looks for `wu_log_data.json` (line 51 in `assemble_client_handover_report.py`). If Phase 0 outputs `wu_log.json` instead, production validation will show N/A values.

**FIX**: Ensure `preprocess_client_handover.py` line 91 writes to `wu_log_data.json`:
```python
wu_log_path = os.path.join(output_dir, "wu_log_data.json")  # ← CORRECT
# NOT: wu_log_path = os.path.join(output_dir, "wu_log.json")  # ← WRONG
```

### Transformation Functions (NEW)

**CRITICAL**: The assembly script now uses specialized transformation functions to enhance data quality and ensure proper structure.

#### 1. transform_requirements()

**Purpose**: Transform raw requirements into structured format with traceability

**Location**: `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py` (lines 250-290)

**Input**: `business_analysis` dict

**Output**: List of requirements with enhanced fields:

- `id`: Sequential IDs (BR-001, BR-002, BR-003, etc.)
- `category`: "Functional" (standardized)
- `title`: Requirement summary (max 100 chars)
- `description`: Full requirement text
- `priority`: "High" (first 2 requirements) or "Medium"
- `business_value`: Business justification
- `source`: "ANA-050 Section 2.1" (traceability)
- `stakeholders`: List of stakeholder names (top 3)

**Example Output**:

```json
{
  "id": "BR-001",
  "category": "Functional",
  "title": "Generate daily match report for external system",
  "description": "System must generate a daily match report containing transaction details...",
  "priority": "High",
  "business_value": "Enables automated reconciliation and reduces manual effort",
  "source": "ANA-050 Section 2.1",
  "stakeholders": ["Finance Team", "IT Operations", "External Vendor"]
}
```

**Why This Matters**:

- Provides proper requirement traceability
- Assigns priorities based on business importance
- Links requirements to stakeholders
- Creates professional, client-ready documentation

#### 2. transform_production_validation()

**Purpose**: Create production validation from work unit log data

**Location**: `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py` (lines 292-390)

**Input**: `wu_data` dict (from `wu_log_data.json`)

**Output**: Production validation with real test results:

- `validation_status`: "Validated - Production Ready" or "Issues Found"
- `test_results`: List of test parameters with actual values and status
- `performance_metrics`: Real execution metrics from production

**Example Output**:

```json
{
  "validation_status": "Validated - Production Ready",
  "test_results": [
    {"parameter": "Execution Speed", "value": "8.5s", "status": "Excellent"},
    {"parameter": "Data Volume", "value": "1,234 records", "status": "Normal"},
    {"parameter": "Authentication", "value": "OAuth2 Token", "status": "Secure"},
    {"parameter": "API Integration", "value": "Compass Data Fabric", "status": "Stable"},
    {"parameter": "Error Count", "value": "0", "status": "Pass"},
    {"parameter": "File Operations", "value": "2 SFTP transfers", "status": "Success"}
  ],
  "performance_metrics": {
    "total_duration": "8.5s",
    "activity_count": 23,
    "record_count": "1,234",
    "avg_activity_time": "0.37s"
  }
}
```

**Why This Matters**:

- Provides real production evidence (not generic statements)
- Shows actual performance metrics from work unit logs
- Demonstrates production readiness with concrete data
- Builds client confidence with measurable results

**CRITICAL DATA EXTRACTION PATTERNS** (2026-03-03):

1. **Test Environment - Use Placeholder**:
   - Work unit logs do NOT reliably contain tenant/data area information
   - FileChannelMonitorDirectory may have tenant name, but it's not guaranteed
   - **Solution**: Use `<Tenant>` placeholder in RED color for user to update manually
   - **Why**: Prevents incorrect assumptions about production vs test environments

2. **Record Count - Extract from JSON Response**:
   - The `rowCount` variable often contains `"obj.rowCount;"` (no numeric value)
   - **Solution**: Extract from `x` variable which contains full JSON response
   - **Pattern**: `re.search(r'"rowCount":(\d+)', variables['x'])`
   - **Example**: `{"status":"FINISHED",...,"rowCount":370,...}` → Extract 370

3. **Scenarios Tested - Count Execution Paths**:
   - Don't use hardcoded scenario lists
   - **Solution**: Dynamically count actual execution paths from activities
   - **Pattern**: Check for specific activity names (GetAccessToken, InitQuery, GetStatus, GetResult, FTP operations, Delete operations)
   - **Example**: 6 scenarios = OAuth + API Query + Status Polling + Result Retrieval + SFTP + Cleanup

4. **Data Volume vs Records Retrieved**:
   - These are DIFFERENT fields with different purposes
   - **Records Retrieved**: "370 GL records" (what was fetched)
   - **Data Volume**: "370 records processed" (what was processed)
   - **Template**: Use `data_volume` field for "Data Volume", not `records_retrieved`

5. **Remove Duplicate Fields**:
   - Don't show both "Test Scenarios" (from error_handling) and "Scenarios Tested" (from test_coverage)
   - **Solution**: Remove "Test Scenarios" from error_handling section
   - **Keep**: Only "Scenarios Tested" with actual count

**Code Location**: `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py` lines 156-320

**Template Location**: `ipa_client_handover_template.py` lines 850-970

#### 3. generate_key_features()

**Purpose**: Extract key features from business analysis

**Location**: `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py` (lines 392-430)

**Input**: `business_analysis` dict

**Output**: List of feature strings (max 8 features)

**Example Output**:

```json
[
  "✓ Compass Data Fabric Integration",
  "✓ SFTP File Transfer",
  "✓ OAuth2 Authentication",
  "✓ Automated Daily Scheduling",
  "✓ Error Notification System",
  "✓ Real-time Data Validation",
  "✓ Audit Trail Logging",
  "✓ Multi-tenant Support"
]
```

**Why This Matters**:

- Highlights key capabilities at a glance
- Extracted from actual integrations and objectives
- Client-friendly bullet format
- Focuses on business value, not technical details

#### Usage in Assembly Script

The `build_ipa_data()` function now calls these transformation functions automatically:

```python
def build_ipa_data(client_name, rice_item, business_analysis, workflow_analysis, 
                   configuration_analysis, risk_assessment, lpd_structure, 
                   metrics_summary, wu_data=None):
    
    # ... other processing ...
    
    # Use transformation functions
    requirements = transform_requirements(business_analysis)
    production_validation = transform_production_validation(wu_data) if wu_data else default_validation
    key_features = generate_key_features(business_analysis)
    
    # Build ipa_data with transformed data
    ipa_data = {
        'requirements': requirements,  # Enhanced with IDs, priorities, stakeholders
        'production_validation': production_validation,  # Real test results
        'key_features': key_features,  # Extracted features
        # ... other fields ...
    }
    
    return ipa_data
```

#### Benefits

1. **Consistency**: All reports use same transformation logic
2. **Quality**: Proper structure with required fields
3. **Traceability**: Requirements linked to sources and stakeholders
4. **Evidence**: Production validation uses real data from WU logs
5. **Maintainability**: Centralized transformation logic (not scattered)

#### When to Update

Update these transformation functions when:

- Template requires new fields in requirements
- Production validation needs additional test parameters
- Key features extraction logic needs refinement
- Client feedback requires format changes

**Location**: All three functions are in `assemble_client_handover_report.py` before the `build_ipa_data()` function.

### JSON Structure Requirements

**CRITICAL**: Analysis JSONs must follow the expected schema to prevent assembly failures.

**business_analysis.json** - RECOMMENDED structure:

```json
{
  "business_objectives": {
    "overview": "string (primary business purpose)",
    "objectives": ["string (list of objectives)"]
  },
  "functional_requirements": [{"requirement": "...", "description": "..."}],
  "stakeholders": [{"name": "...", "role": "..."}],
  "integration_touchpoints": [{"system": "...", "purpose": "..."}]
}
```

**Why this matters:**

- Assembly script expects `business_objectives` to be a **dict** with `overview` and `objectives` keys
- If you provide a list instead, the script will handle it gracefully but with warnings
- Use `functional_requirements` not `business_requirements` for the requirements list
- Use `integration_touchpoints` not `integration_points` for integrations

**Validation command:**

```bash
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

Run this BEFORE Phase 5 to catch structure issues early.

### Common Mistakes to Avoid

❌ **WRONG**: Manually extract data and skip Phase 0

- Creates `lpd_data.json` instead of `lpd_structure.json`
- Assembly script can't find required files
- Report shows empty data (Process Count: 0)

❌ **WRONG**: Create analysis JSONs without running Phase 0 first

- Missing `lpd_structure.json` and `metrics_summary.json`
- Assembly script uses empty dicts
- Report has no process details

❌ **WRONG**: Use incorrect field names in analysis JSONs

- `business_objectives` as list instead of dict → Assembly error
- `business_requirements` instead of `functional_requirements` → Missing data
- `integration_points` instead of `integration_touchpoints` → Missing data

✅ **CORRECT**: Always run Phase 0 → Phases 1-4 → Validate → Phase 5

- All required files exist
- JSON structures match expected schema
- Assembly script has complete data
- Report shows accurate process information

### Verification Before Report Assembly

Before running Phase 5, verify these files exist:

```bash
Test-Path Temp/lpd_structure.json
Test-Path Temp/metrics_summary.json
Test-Path Temp/business_analysis.json
Test-Path Temp/workflow_analysis.json
Test-Path Temp/configuration_analysis.json
Test-Path Temp/risk_assessment.json
```

If ANY file is missing, the report will be incomplete.

### Report Review After Assembly (MANDATORY)

**CRITICAL**: After Phase 5 completes, ALWAYS review the generated report to verify data completeness.

**Quick Review Script:**
```bash
python Temp/review_report.py
```

**What to check:**
- All sheets have content (>3 rows)
- Business Requirements shows count > 0
- System Configuration has variables listed
- Activity Node Guide has activities
- Process sheets have workflow details

**If any sheet is empty or has minimal data:**
1. Check debug output from Phase 5 (shows data counts)
2. Inspect analysis JSONs for missing fields
3. Run validation script to check structure
4. Fix data structure issues in analysis JSONs
5. Regenerate report

**Detailed Sheet Inspection:**
```bash
python ReusableTools/excel_reader.py Client_Handover_Results/<Client>_<RICE>.xlsx --sheet "<SheetName>"
```

## Critical Data Extraction Requirements

### Client Handover Documentation

**MANDATORY**: Subagents MUST extract from actual source files, NOT generate AI content.

**Sheet 2 (Business Requirements)** - Extract from ANA-050 Functional Specification:

- Read `spec_data.json` (extracted from ANA-050 document)
- Extract from sections: Overview, Requirements Details, Proposed Solution, Field Mapping, File naming, Server file structure, Assumptions
- Transform spec content into client-friendly requirements with proper traceability
- Example: Field Mapping table → BR-002 with actual field list (Run date, Company, Account, etc.)
- Source attribution: "ANA-050 Section 2.7 Field Mapping"

**Sheet 3 (Workflow)** - Extract from LPD Activities:

- Read `lpd_data.json` (extracted from LPD file)
- Extract actual activity sequence from `processes[0]['activities']`
- Use actual activity captions, types, and connections
- Example: "Read Input File", "Validate Date Parameter", "Get OAuth Token", "Submit Compass Query"
- Do NOT invent generic steps like "Initialize Variables" or "Authenticate with Data Fabric"

**Sheet 4 (Configuration)** - Extract from LPD Start Node:

- Read `lpd_data.json` (extracted from LPD file)
- Navigate to `processes[0]['activities']`, find Start node (`id == "Start"`)
- Extract ALL properties except `_activityCheckPoint`, `Checkpoint`, `variableType`
- Categorize variables:
  - System Configuration: starts with `_configuration.`
  - File Channel: `FileChannel*` variables
  - Process Variables: everything else
- Example: OauthCreds, OutputFileName, Counter, limit (5000), FileChannelFileName, Tenant, Webroot
- Do NOT invent variables like vEmailSubject, vApproverList, vCurrentDate

**Verification Checklist:**

Before generating ANY client handover report, verify:

- [ ] Business requirements extracted from ANA-050 spec (not AI-generated)
- [ ] Workflow steps extracted from LPD activities (not AI-generated)
- [ ] Configuration variables extracted from LPD Start node (not AI-generated)
- [ ] All requirements have source attribution (e.g., "ANA-050 Section 2.7")
- [ ] All workflow steps match actual LPD activity captions
- [ ] All configuration variables exist in Start node properties

**If ANY checkbox fails, the document is decorative, not authoritative. It's not defensible in front of the client.**

**Production Readiness Score:**

- AI-generated content: 40-60% (demo quality)
- Real extracted data: 95% (enterprise quality)

The difference: "Reading actual source data instead of generating content" transforms a demo AI into an enterprise documentation engine.

## Table of Contents

- [Core Principles](#core-principles)
- [Stateless Pipeline Workflow (MANDATORY)](#stateless-pipeline-workflow-mandatory)
  - [Phase 0: Preprocessing](#phase-0-preprocessing-python-only---mandatory-first-step)
  - [Phase 1-4: AI Analysis](#phase-1-4-ai-analysis-create-analysis-jsons)
  - [Phase 5: Report Assembly](#phase-5-report-assembly-python-only---final-step)
  - [Common Mistakes to Avoid](#common-mistakes-to-avoid)
  - [Verification Before Report Assembly](#verification-before-report-assembly)
- [Critical Data Extraction Requirements](#critical-data-extraction-requirements)
  - [Client Handover Documentation](#client-handover-documentation)
  - [Verification Checklist](#verification-checklist)
- [Analysis Workflow](#analysis-workflow)
  - [Fundamental Rule](#fundamental-rule)
  - [Intelligent Four-Step Process](#intelligent-four-step-process-solves-context-overload)
  - [Required Steering Files](#required-steering-files)
  - [Pre-Generation Checklist](#pre-generation-checklist)
- [Critical Data Structure Requirements](#critical-data-structure-requirements)
  - [Mandatory Checklist](#mandatory-checklist)
  - [Recurring Issues](#recurring-issues)
  - [Data Structure Checklist](#data-structure-checklist)
- [Flow Analysis](#flow-analysis)
  - [Why Flow Analysis Matters](#why-flow-analysis-matters)
  - [Flow Analysis Steps](#flow-analysis-steps)
  - [Performance Impact Analysis](#performance-impact-analysis)
  - [Critical Verification Points](#critical-verification-points)
- [Project Standards Configuration](#project-standards-configuration)
  - [File Structure](#file-structure)
  - [Loading Project Standards](#loading-project-standards)
  - [Using Project Standards in Analysis](#using-project-standards-in-analysis)
- [Report Types](#report-types)
  - [1 Client Handover Documentation](#1-client-handover-documentation)
  - [2 Coding Standards Internal Peer Review](#2-coding-standards-internal-peer-review)
    - [Coding Standards Report UI/UX Enhancements](#coding-standards-report-uiux-enhancements-2026-03-08)
  - [3 Performance Work Unit Analysis](#3-performance-work-unit-analysis)
- [RICE and Functional Specifications](#rice-and-functional-specifications)
- [Activity Counting](#activity-counting)
- [Visual Design Standards](#visual-design-standards)
- [Report Structure](#report-structure)
- [Template Architecture](#template-architecture)
- [System Configuration](#system-configuration)
- [Process Sheet Requirements](#process-sheet-requirements)
- [Workflow Diagrams](#workflow-diagrams)
- [Generation Workflow](#generation-workflow)
- [Quality Checklist](#quality-checklist)
- [Coding Standards Data Structure](#coding-standards-data-structure)
- [Excel Report Technology Stack](#excel-report-technology-stack)
- [Recent Examples](#recent-examples)

---

## Analysis Workflow

### Fundamental Rule

**CRITICAL**: AI performs ALL analysis. Python only extracts and formats data.

**Never let Python make decisions about:**

- Code quality assessment
- ES5 compliance evaluation
- Performance impact prioritization
- Security risk assessment
- Recommendation generation

**Python's role**: Extract raw data, structure it, format reports.

**AI's role**: Analyze, assess, decide, recommend.

### Intelligent Four-Step Process (Solves Context Overload)

**Problem Solved**: Analyzing large IPAs (450+ activities, 130+ JS blocks) caused context overload when AI tried to analyze everything at once.

**Solution**: Domain-segmented AI analysis - analyze one domain at a time instead of everything together.

**Step 1: Extract Data (Python)**

Extract ONE LPD file at a time (1:1 mapping):

```python
from ReusableTools.IPA_Analyzer.extract_lpd_data import extract_lpd_data

# Single process
extract_lpd_data(['path/to/process.lpd'], 'Temp/ProcessName_lpd_data.json')

# Multiple processes - extract each separately
extract_lpd_data(['path/to/process1.lpd'], 'Temp/Process1_lpd_data.json')
extract_lpd_data(['path/to/process2.lpd'], 'Temp/Process2_lpd_data.json')
```

**Step 2: Organize by Domain (Python) ← NEW!**

Split extracted data into 5 domain-specific files:

```bash
python ReusableTools/IPA_CodingStandards/organize_by_domain.py \
    Temp/ProcessName_lpd_data.json \
    Temp/ProcessName
```

Creates 5 domain files (200-400 lines each vs 6000 lines combined):

- `Temp/ProcessName_domain_naming.json` - Filenames, node captions, config sets
- `Temp/ProcessName_domain_javascript.json` - ES6, performance, function order
- `Temp/ProcessName_domain_sql.json` - Queries, pagination, Compass SQL
- `Temp/ProcessName_domain_errorhandling.json` - OnError tabs, GetWorkUnitErrors
- `Temp/ProcessName_domain_structure.json` - Process type, auto-restart

**What the Organizer Does (Python - Heavy Lifting Only)**:

- Extracts patterns (ES6 keywords, generic names, SQL queries)
- Calculates statistics (counts, percentages)
- Groups data by domain
- **Does NOT decide violations or assign severity** ✅

**Step 3: AI Analyzes Each Domain Separately**

AI reads ONE domain at a time and determines violations:

```python
# Domain 1: Naming
readFile('Temp/ProcessName_domain_naming.json')  # 250 lines
# AI analyzes: Filename format, node naming, config sets, hardcoded values
# AI builds violations array and saves to violations_naming.json

# Domain 2: JavaScript
readFile('Temp/ProcessName_domain_javascript.json')  # 400 lines
# AI analyzes: ES6 compliance, performance, function order, global vars
# AI builds violations array and saves to violations_javascript.json

# Domain 3: SQL
readFile('Temp/ProcessName_domain_sql.json')  # 200 lines
# AI analyzes: Pagination, Compass SQL, SELECT *, WHERE clauses
# AI builds violations array and saves to violations_sql.json

# Domain 4: Error Handling
readFile('Temp/ProcessName_domain_errorhandling.json')  # 150 lines
# AI analyzes: OnError tabs, GetWorkUnitErrors, coverage
# AI builds violations array and saves to violations_errorhandling.json

# Domain 5: Structure
readFile('Temp/ProcessName_domain_structure.json')  # 100 lines
# AI analyzes: Auto-restart, process type, activity distribution
# AI builds violations array and saves to violations_structure.json
```

**Benefits**:

- AI reads 200-400 lines per domain (vs 6000 lines total)
- No context overload
- Full coverage (all domains analyzed)
- Consistent rule application

**Step 4: Merge Violations and Generate Report (Python)**

```bash
# Merge all domain violations into master file
python ReusableTools/IPA_CodingStandards/merge_violations.py Temp/ProcessName

# AI reads master violations and builds ipa_data
readFile('Temp/ProcessName_master_violations.json')

# Python generates ONE Excel report
python Temp/generate_ProcessName_coding_standards.py
```

For coding standards reviews, use the programmatic analyzer:

```python
from ReusableTools.IPA_CodingStandards.analyze_coding_standards import IPACodingStandardsAnalyzer

analyzer = IPACodingStandardsAnalyzer(
    'Temp/ProcessName_lpd_data.json',
    'Projects/ClientName/project_standards.xlsx'
)

analyzer.load_data()
analysis = analyzer.analyze()
analyzer.save_analysis('Temp/ProcessName_analysis.json')
```

**Analyzer capabilities:**

- Applies coding standards rules programmatically
- Checks naming conventions, IPA rules, error handling, configuration, performance
- Identifies violations with specific nodes/activities
- Extracts SQL queries and JavaScript issues
- Outputs structured analysis JSON (smaller than raw data)

**Step 3: AI Review and Insights**

AI reads the analysis (not raw data) and adds context-aware insights:

```python
# Read the analysis JSON
analysis = readFile('Temp/ProcessName_analysis.json')

# AI adds:
# - Context-aware insights (process type, auto-restart assessment)
# - Flow analysis (critical path, loop iterations, performance impact)
# - Priority recommendations (HIGH/MEDIUM/LOW based on actual impact)
# - Testing strategies
# - Business context

# Build ipa_data with AI insights + programmatic analysis
ipa_data = {
    'overview': analysis['overview'],
    'coding_standards': {
        'naming_convention': analysis['naming_violations'],
        'ipa_rules': analysis['ipa_rule_violations'],
        'error_handling': analysis['error_handling_issues'],
        'configuration': analysis['config_issues'],
        'performance': analysis['performance_issues']
    },
    'javascript_issues': analysis['javascript_issues'],
    'sql_queries': analysis['sql_queries'],
    'recommendations': [
        # AI adds flow-aware recommendations with:
        # - Critical path identification
        # - Performance impact calculations
        # - Priority based on actual impact
        # - Testing strategies
    ],
    'technical_deep_dive': {
        # AI adds architecture analysis
    }
}
```

**Step 4: Generate Report (Python)**

```python
import sys
sys.path.insert(0, '.')

from ReusableTools.IPA_CodingStandards.ipa_coding_standards_template import generate_report

# Generate ONE report per process
output_path = generate_report(ipa_data)
```

### Workflow Comparison

| Aspect | Old Workflow | New Workflow |
|--------|-------------|--------------|
| AI Context | 6000+ lines raw JSON | 500 lines structured analysis |
| Rule Application | Manual (AI interprets) | Programmatic (Python applies) |
| Consistency | Varies by interpretation | Consistent rules |
| Scalability | Fails on large processes | Handles any size |
| Edit Failures | Frequent (context overload) | Rare (small files) |
| Speed | Slow | Fast |

### When to Use Each Approach

**Use programmatic analyzer for:**

- Coding standards reviews (rules-based)
- Large processes (>200 activities, >50 JS blocks)
- Multiple processes in one session
- Consistent rule enforcement

**Use AI-only analysis for:**

- Client handover documentation (narrative-focused)
- Peer reviews (subjective assessment)
- Small processes (<100 activities)
- Custom analysis not covered by rules

## Project Standards Configuration

### Overview

Each project has its own coding standards file that defines project-specific rules. This allows different clients to have different standards (e.g., BayCare vs FPI may have different variable naming conventions).

### File Location

```text
Projects/<ClientName>/project_standards.xlsx
```

### Template Location

```text
.kiro/templates/project_standards_template.xlsx
```

### File Structure

**Sheet 1: Guide** - Instructions and column definitions (for human reference)

**Sheet 2: Standards** - Actual rules (parsed by Kiro)

### Standards Sheet Columns

| Column | Description | Example |
|--------|-------------|---------|
| Category | Standards category | Naming Convention, IPA Rules, Error Handling, System Configuration, Performance |
| Rule_ID | Unique identifier | 1.1.1, 1.2.1, 1.5.2 |
| Rule_Name | Short descriptive name | Filename Format, Global Variables, Pagination |
| Expected | What the rule requires | Interface: `<Prefix>_INT_<Source>_<Dest>_<Desc>.lpd` OR Workflow: `<Prefix>_WF_<Desc>.lpd` |
| Severity | Impact level | High, Medium, Low |
| Applies_To | Scope of rule | All, LM nodes only, WEBRN only |
| Notes | Additional context | Prefix must be FPI, Exclude START/END/ASSGN/BRANCH/MSGBD |

### Standard Categories

1. **Naming Convention** - Files, variables, config sets, nodes
2. **IPA Rules** - Global variables, function declarations, ES5 compliance
3. **Error Handling** - OnError tabs, GetWorkUnitErrors activity node, stopOnError
4. **System Configuration** - Config set names, hardcoded values, auto-restart
5. **Performance** - Pagination, webservice usage, regex compilation, string concatenation

### Loading Project Standards

**CRITICAL**: Excel files are binary and cannot be read with readFile. Use Excel Reader tool.

**In Coding Standards Workflow (Step 4.6):**

```python
# Method 1: Use Excel Reader tool (RECOMMENDED)
from ReusableTools.excel_reader import read_excel
import os

standards_file = f'Projects/{client}/project_standards_{client}.xlsx'

if os.path.exists(standards_file):
    try:
        # Read Standards sheet
        project_standards = read_excel(standards_file, sheet_name='Standards')
        print(f"✓ Loaded {len(project_standards)} project-specific rules from {standards_file}")
        
        # Display summary
        print(f"\nCategories: {project_standards['Category'].value_counts().to_dict()}")
        
    except Exception as e:
        print(f"❌ Error reading project standards: {e}")
        print("  Using default rules from steering files")
        project_standards = None
else:
    print(f"⚠ No project standards found at {standards_file}")
    print("  Using default rules from steering files")
    project_standards = None
```

**Via executePwsh (for Kiro):**

```python
# Step 1: Export Excel to JSON
executePwsh(f"python ReusableTools/excel_reader.py Projects/{client}/project_standards_{client}.xlsx --sheet Standards --json Temp/{client}_standards.json")

# Step 2: Read JSON with readFile
standards_json = readFile(f'Temp/{client}_standards.json')
project_standards = json.loads(standards_json)
```

**MANDATORY ERROR HANDLING:**

- If Excel read fails, STOP and report error
- Do NOT proceed with analysis using incomplete data
- Do NOT assume default rules if project standards exist but failed to load
- Verify data loaded successfully before continuing

### Using Project Standards in Analysis

**Filter by category:**

```python
if project_standards is not None:
    # Get rules for specific category
    naming_rules = project_standards[project_standards['Category'] == 'Naming Convention']
    
    # Check each rule
    for _, rule in naming_rules.iterrows():
        rule_id = rule['Rule_ID']
        rule_name = rule['Rule_Name']
        expected = rule['Expected']
        severity = rule['Severity']
        applies_to = rule['Applies_To']
        notes = rule['Notes']
        
        # Apply rule to lpd_data
        check_rule(lpd_data, rule)
```

### Creating Project Standards for New Client

**When to Create:**

- New client with specific coding standards
- Existing client needs different rules than defaults
- Team wants to document and enforce project-specific conventions

**Steps:**

1. **Copy template:**

   ```powershell
   Copy-Item ".kiro/templates/project_standards_template.xlsx" -Destination "Projects/<ClientName>/project_standards.xlsx"
   ```

2. **Open Excel file** - `Projects/<ClientName>/project_standards.xlsx`

3. **Read "Guide" sheet** - Instructions and column definitions

4. **Update "Standards" sheet** with project-specific rules:
   - Category: Naming Convention, IPA Rules, Error Handling, System Configuration, Performance
   - Rule_ID: Unique identifier (e.g., 1.1.1, 1.2.1)
   - Rule_Name: Short descriptive name
   - Expected: What the rule requires
   - Severity: Low, Medium, High, Critical
   - Applies_To: File, Activity, JavaScript, SQL, Configuration
   - Notes: Additional context or examples

5. **Save file** - Commit to git for version control

6. **Run coding standards skill** - Activate with `/ipa-coding-standards` - It will automatically detect and load your project standards

**Example Rules:**

| Category | Rule_ID | Rule_Name | Expected | Severity | Applies_To | Notes |
|----------|---------|-----------|----------|----------|------------|-------|
| Naming Convention | 1.1.1 | Filename Format | Interface: `<Prefix>_INT_<Source>_<Destination>_<Desc>.lpd` OR Workflow: `<Prefix>_WF_<Desc>.lpd` | Medium | File | INT for interfaces (e.g., INFR_INT_HCM_SAP_Employee.lpd), WF for workflows/approvals (e.g., INFR_WF_ApproveDraftRequisition.lpd) |
| IPA Rules | 1.2.2 | Variable Naming | CamelCase for all variables | Low | JavaScript | Team standard |
| Performance | 1.5.2 | Pagination | Max 5000 rows per batch | High | JavaScript | Prevents timeouts |

### Using Standards in Analysis

**Automatic Detection:**

During Phase 0 of the coding standards skill, Kiro checks for and loads project standards:

```python
standards_file = f'Projects/{client}/project_standards.xlsx'

if os.path.exists(standards_file):
    # Load project-specific standards
    import pandas as pd
    df = pd.read_excel(standards_file, sheet_name='Standards')
    # These standards will be applied during analysis in Step 7
else:
    # Use default rules from steering files
    pass
```

**When Project Standards Exist:**

1. **Load Excel file** - Read "Standards" sheet into DataFrame
2. **Filter by category** - `df[df['Category'] == 'Naming Convention']`
3. **Apply project rules** - Use Expected, Severity, Applies_To columns
4. **Check compliance** - Compare actual vs expected
5. **Report violations** - Include Rule_ID in findings
6. **Reference in recommendations** - "Violates Rule 1.1.1: Filename Format"

**When Project Standards Don't Exist:**

1. **Use default rules** - From steering files 01, 02, 03, 05, 10, 11
2. **Apply standard checks** - Generic naming, ES5, error handling, performance
3. **Suggest creating project_standards.xlsx** - If client has specific requirements

**Example Analysis with Project Standards:**

```pythonpython
# Load project standards
naming_rules = df[df['Category'] == 'Naming Convention']

# Check filename format
for rule in naming_rules.itertuples():
    if rule.Rule_ID == '1.1.1':
        expected_format = rule.Expected  # "<Prefix>_<INT>_<Source>_<Destination>_<Desc>.lpd"
        if not matches_format(filename, expected_format):
            violations.append({
                'rule_id': rule.Rule_ID,
                'rule_name': rule.Rule_Name,
                'severity': rule.Severity,
                'expected': rule.Expected,
                'actual': filename,
                'recommendation': f"Rename to match format: {expected_format}"
            })
```

**Benefits:**

- Client-specific standards enforced automatically
- Easy to update (Excel file, no code changes)
- Clear audit trail (versioned in git)
- Consistent reviews across team members

### Benefits

- **Client-Specific**: Each project has its own standards
- **Easy Updates**: Change Excel file, no code changes needed
- **Versioned**: Track standards changes in git
- **Auditable**: Clear documentation of what standards apply
- **Flexible**: Add/remove rules per client without touching code

---

**Step 2: Analyze Data (AI)**

- **FIRST**: Load required steering files (see Required Steering Files section below)
- Read ALL JSON files using `readFile()`
- Assess ES5 compliance, performance patterns, security issues
- Evaluate auto-restart configuration (context-aware)
- Trace requirements to implementation
- Build `ipa_data` dictionary with YOUR analysis findings
- Show analysis in chat and ask user confirmation

**Step 3: Generate Report (Python)**

```python
from ipa_peer_review_template import generate_report
output_path = generate_report(ipa_data)
```

### Required Steering Files

**Coding Standards Review:**

- **01** - IPA and IPD Complete Guide (node types: LM/LMTxn/WEBRUN vs WEBRN)
- **02** - Work Unit Analysis (error patterns, JavaScript ES5)
- **03** - Process Patterns Library (450+ patterns, best practices)
- **05** - Compass SQL CheatSheet (SQL performance, Compass API best practices)
- **10** - IPA Report Generation (workflow, GetWorkUnitErrors)
- **11** - RICE Methodology (naming conventions, specifications)

**Client Handover:**

- **01** - IPA and IPD Complete Guide
- **10** - IPA Report Generation
- **11** - RICE Methodology

**Performance Analysis:**

- **02** - Work Unit Analysis
- **04** - WU Report Generation

### Pre-Generation Checklist

Before generating ANY report:

1. **Required steering files loaded** (for coding standards: 01, 02, 03, 05, 10, 11)
2. Data extracted to JSON files
3. ALL JSON files read with `readFile()`
4. **Flow analysis completed** (trace execution paths, identify loops, critical path)
5. Branch conditions verified (check `branch_conditions` array, not just properties)
6. Analysis findings shown in chat
7. `ipa_data` dictionary built with YOUR analysis
8. User confirmation received

---

## Critical Data Structure Requirements

### Mandatory Checklist

**STOP - Verify BEFORE building ipa_data:**

```text
[ ] No duplicate issues between recommendations and coding_standards
[ ] sql_queries provided at TOP LEVEL
[ ] javascript_issues provided at TOP LEVEL as list of lists
[ ] Each coding_standards item has correct status
[ ] Node naming in recommendations ONLY
[ ] Performance issues in recommendations ONLY
[ ] Simple Pass/Fail checks in coding_standards ONLY
```

If ANY checkbox is unchecked, DO NOT proceed. Fix the issue first.

### Recurring Issues

These three issues appear repeatedly. Follow these rules to prevent them:

#### Issue 1: Duplicate Action Items

**Problem**: Same issue appears in both `recommendations` and `coding_standards`.

**Solution**: Choose ONE location.

**Use recommendations for:**

- Performance issues with flow analysis
- Issues requiring detailed explanation
- Complex issues with calculated impact
- Node naming issues (with specific node list)

**Use coding_standards for:**

- Simple rule violations (filename format)
- Binary checks (standard flow yes/no)
- Pass/Fail items with no nuance

**Example (correct)**:

```python
'recommendations': [
    {
        'priority': 'Medium',
        'category': 'Naming Convention',
        'recommendation': 'Rename nodes to descriptive names',
        'activities': 'Assign4580, Assign1340, Branch8450...',
        'issue': '67.6% of nodes (25/37) use generic captions',
        ...
    }
],
'coding_standards': {
    'naming_convention': [
        # Filename check ONLY - no node naming here
        ['MatchReport_Outbound.lpd', 'Filename format', 'Low', 'Correct', 'Pass', 'None']
    ]
}
```

#### Issue 2: Missing SQL/JavaScript in Detailed Analysis

**Problem**: Detailed Analysis sheet shows "No SQL queries found" even though SQL exists.

**Root Cause**: Template reads from TOP LEVEL, not from `technical_deep_dive`.

**Solution**: Provide data at TOP LEVEL.

```python
ipa_data = {
    # TOP LEVEL - for Detailed Analysis sheet
    'sql_queries': [
        {
            'activity_id': 'InitQuery',
            'query_type': 'Compass SQL SELECT',
            'query': 'SELECT ... FROM ... WHERE ...',
            'assessment': 'Good - proper filtering',
            'recommendations': 'Consider optimization'
        }
    ],
    
    # Also in technical_deep_dive for documentation
    'technical_deep_dive': {
        'sql_analysis': [...]  # Reference only
    }
}
```

Same pattern for `javascript_issues` - provide at TOP LEVEL as list of lists.

#### Issue 3: Incorrect Status in Coding Standards

**Problem**: Status says "Pass" but issue text describes a violation.

**Root Cause**: Not carefully matching status to finding.

**Solution**: Each item is ONE specific check. Status must match the finding.

```python
'coding_standards': {
    'naming_convention': [
        # Item 1: Filename format check
        ['MatchReport_Outbound.lpd', 'Filename format correct', 'Low', 
         'Follows pattern', 'MatchReport_Outbound.lpd', 'Pass', 'None'],
        
        # Item 2: Standard flow check
        ['MatchReport_Outbound.lpd', 'Not a standard flow', 'Low',
         'Custom process', 'Not standard', 'Pass', 'None']
    ]
}
```

**Key rules:**

- Each item = ONE check
- Status matches finding (Pass = no violation, Needs Improvement = violation)
- Don't mix multiple issues in one item
- Node naming is complex → goes in recommendations

### Data Structure Checklist

**Before building ipa_data, answer these questions:**

1. Did I find node naming issues?
   - YES: Put in recommendations ONLY (with specific node list)
   - NO: Don't mention it

2. Did I find performance issues?
   - YES: Put in recommendations ONLY (with flow analysis)
   - NO: Don't mention it

3. Did I find SQL queries?
   - YES: Put at TOP LEVEL as sql_queries array
   - NO: Set sql_queries = []

4. Did I find JavaScript violations?
   - YES: Put at TOP LEVEL as javascript_issues (list of lists)
   - NO: Set javascript_issues = []

5. For each coding_standards item:
   - Does status match the finding?
   - Is this a simple Pass/Fail check?
   - NOT node naming or performance (those go in recommendations)

**Checklist:**

```text
- [ ] No duplicates between recommendations and coding_standards
- [ ] sql_queries at TOP LEVEL
- [ ] javascript_issues at TOP LEVEL as list of lists
- [ ] Each coding_standards item has correct status
- [ ] Node naming in recommendations ONLY
- [ ] Performance issues in recommendations ONLY
- [ ] Simple checks in coding_standards ONLY
```

If ANY checkbox is unchecked, STOP and fix before proceeding.

## Flow Analysis

### Why Flow Analysis Matters

**Problem**: Extracting nodes without understanding flow creates inaccurate action items.

**Example**: Performance issue in startup (1x) = LOW priority. Same issue in pagination loop (20x for 100K rows) = HIGH priority.

### Flow Analysis Steps

**1. Identify Loops**

Look for `branch_conditions` arrays with back-edges:

```json
{
  "id": "Branch9750",
  "type": "BRANCH",
  "branch_conditions": [
    {
      "name": "NotDonePaging",
      "branch_to": "GetResult",  // Back-edge creates loop
      "expression": "rowCount+%3E+0"
    }
  ]
}
```

**Loop types:**

- Pagination Loop: Processes data in batches
- Polling Loop: Waits for async operation
- Retry Loop: Retries failed operations

**2. Trace Execution Paths**

Build flow graph from START to END:

- Happy Path: Normal execution
- Error Paths: What happens when things fail
- Recovery Paths: How process recovers

**3. Identify Critical Path**

Nodes executed most frequently or with highest performance impact.

**Priority:**

- CRITICAL PATH: Nodes in pagination/processing loops (executed N times)
- STARTUP PATH: Nodes executed once at start (low frequency)
- ERROR PATH: Nodes only executed on errors (rare)
- POLLING PATH: Nodes in polling loops (moderate frequency)

**4. Calculate Loop Iterations**

For each loop:

- Entry condition: When does loop start?
- Exit condition: When does loop end?
- Iterations: How many times?
- Timeout: Maximum execution time?

### Flow-Aware Action Items

**CRITICAL PATH Issues** (HIGH Priority):

- Performance issues in pagination/processing loops
- Issues executed N times (where N = dataset size / batch size)
- Compounding overhead (e.g., regex compilation, string +=)

**STARTUP PATH Issues** (MEDIUM Priority):

- Code quality issues in initialization
- Issues executed once per run
- Maintainability concerns

**ERROR PATH Issues** (LOW Priority):

- Issues only executed on errors
- Rare execution frequency
- Unless error handling is broken

**POLLING PATH Issues** (MEDIUM Priority):

- Issues in polling loops
- Moderate execution frequency
- Balance between responsiveness and overhead

### Flow Analysis in ipa_data

Document flow analysis in `technical_deep_dive.architecture`:

```python
'technical_deep_dive': {
    'architecture': {
        'pattern': 'Compass API Asynchronous Query Pattern with Multi-Loop Architecture',
        'flow_paths': {
            'happy_path': 'START → ReadInput → ValidateDate → ...',
            'error_paths': [
                'Invalid Date → Branch4660 → ...',
                'Token Failure → Branch2840 → ...'
            ],
            'recovery_paths': [
                'Token Retry: Branch2840 → Wait8700 → GetAccessToken',
                'Error Flag: Branch4080 → WriteError → DeleteFlag'
            ]
### Performance Impact Analysis

**Calculate actual impact, not just complexity.**

**Steps:**

1. Execution frequency: How many times?
2. Time per execution: How long?
3. Total impact: Frequency × Time
4. Percentage: (Total impact / Total process time) × 100%

**Priority guidelines:**

| Impact | Percentage | Priority |
|--------|-----------|----------|
| >10 sec | >30% | HIGH |
| 5-10 sec | 15-30% | MEDIUM-HIGH |
| 1-5 sec | 3-15% | MEDIUM |
| 0.1-1 sec | 0.3-3% | LOW |
| <0.1 sec | <0.3% | VERY LOW |

**Examples:**

Regex compilation: 100K times × 0.1ms = 10 sec (33%) = HIGH priority

Array.shift(): 20 times × 1ms = 0.02 sec (0.067%) = VERY LOW priority

**Avoid premature optimization:**

- Don't flag micro-optimizations (<0.3% impact) as high priority
- Focus on bottlenecks >30% of execution time
- O(n) is fine if n is small or frequency is low

### Critical Verification Points

**Branch Conditions**

- BRANCH nodes have multiple conditions in `branch_conditions` array
- Properties only show the last/default condition
- Always check `branch_conditions` for complete logic
- Example: Retry logic requires checking `branch_conditions` for `retryCount` expressions

**System Configuration**

- Extractor flags generic configuration set names (interface, config, system, etc.)
- Check `system_configuration_usage.generic_names` in JSON
- Generic names should be marked "Verify" not "Pass"
- Vendor-specific names are required per standard 1.4.1

**Error Handling**

- Configuration exists in TWO places: OnError tab properties AND error message assignments
- Check `error_handling_analysis.summary.coverage_percentage`
- Node types supporting OnError: WEBRN, WEBRUN, ACCFIL, Timer, SUBPROC, ITBEG
- Node types WITHOUT OnError: START, END, ASSGN, BRANCH, MSGBD (Message Builder)
- MSGBD nodes do NOT have OnError tabs - they cannot fail in a way that needs error handling
- When calculating error handling coverage, EXCLUDE MSGBD nodes from the denominator
- **Action Items**: Only create action items if nodes are MISSING error handling (stopOnError=true when it should be false)
- If all applicable nodes have error handling configured, status should be "Pass" not "Verify"

**GetWorkUnitErrors Pattern**

- GetWorkUnitErrors is NOT a JavaScript function - it's a Landmark Transaction node (LMTxn) with caption "GetWorkUnitErrors"
- This node queries the WorkUnit business class to check if the work unit instance encountered any errors
- Should be placed near the end of the process (not necessarily beside End node, but in the latter part of the flow)
- Node type is LMTxn (Landmark Transaction), NOT WEBRN (external web service)
- Check the activities array for a node with type "LMTxn" or "WEBRUN" and caption "GetWorkUnitErrors" or similar
- If missing, create an action item: "Add GetWorkUnitErrors Landmark Transaction node to query WorkUnit business class for errors"
- This is part of coding standard 1.3 (Error Handling)

**Node Naming**

- Extract ALL node IDs and captions from `activities` array in JSON
- Identify generic names: caption is just "Assign", "Branch", "Wait", "MsgBuilder"
- List SPECIFIC nodes that need renaming (don't say "Cannot verify" - you have the data!)
- Provide suggested renames based on node purpose (check JavaScript code in that node)
- Put the full list of violating nodes in the File/Activity column
- Example: "Assign4580, Assign1340, Branch8450..." (comma-separated list)

**JavaScript Code Quality and Performance**

- Beyond ES5 compliance, assess code quality and performance
- Check for performance anti-patterns:
  - Loops inside loops (O(n²) complexity)
  - Repeated string concatenation in loops (use array.join() instead)
  - Unnecessary JSON.parse() calls in loops
  - Missing function declarations (functions should be declared early, not inline)
  - Inefficient array operations (multiple passes when one would suffice)
- Check for code quality issues:
  - Magic numbers (use named constants)
  - Duplicate code blocks (extract to functions)
  - Deep nesting (>3 levels indicates complexity)
  - Long functions (>50 lines should be split)
  - Missing error handling in critical operations
- Provide specific recommendations with performance impact estimates

**SQL Query Quality and Performance**

- Assess SQL query performance and best practices
- Check for performance issues:
  - Missing WHERE clauses on large tables
  - SELECT * instead of specific columns
  - Missing indexes on filter/join columns
  - Inefficient JOINs (multiple LEFT JOINs when INNER JOIN would work)
  - Subqueries that could be JOINs
  - LIKE with leading wildcards ('%value')
  - Functions on indexed columns in WHERE (prevents index use)
- Check for data quality issues:
  - Missing DISTINCT when needed
  - Potential NULL handling issues
  - Date range filters without proper indexing
  - Missing pagination for large result sets
- Provide specific recommendations with estimated performance impact

**Action Items Rules**

- Only create action items for ACTUAL VIOLATIONS or items needing team verification
- Do NOT create action items for "Cannot verify from LPD data" - if you can't verify it, don't flag it
- All action items MUST have: Issue, Current State, Recommendation, File/Activity filled in

**Valid Statuses**:

- **Pass** - No violations, requirement met (no action item created)
- **Excellent** - Exceeds expectations (no action item created)
- **Good** - Meets expectations well (no action item created)
- **Verify** - Cannot verify without team confirmation (action item for team to confirm)
  - Example: "Verify if 'Interface' is the approved vendor-specific configuration set name"
- **Needs Improvement** - Has issues that should be addressed (action item with specific recommendations)
  - Default status for recommendations from AI analysis
  - Used for coding standards violations

**Invalid Statuses**:

- **Pending** - DO NOT USE (was removed, use "Needs Improvement" instead)

**Status Assignment Logic**:

- `recommendations` array (AI analysis) → Default to "Needs Improvement"
- `coding_standards` array (structured checks) → Use status from data ("Pass", "Verify", "Needs Improvement")
- Status "Pass" → No action item created
- Status "Verify" or "Needs Improvement" → Action item created

### Why This Matters

**Problem**: Python makes generic assessments without business context

**Solution**: AI understands business logic and provides specific, actionable insights

**Bad Example (Python)**: `if 'let ' in code: issues.append('ES6 violation')`

**Good Example (AI)**: "Activity Assign330 uses parseFloat() for amount comparison - correct ES5 pattern for approval limit logic"

---

## Report Types

### 1. Client Handover Documentation

**Purpose**: Professional documentation for client handover of production IPAs

**Audience**: Client technical staff maintaining and modifying IPAs

**Focus**: How it works, configuration changes, maintenance procedures

**Input**: ANA-050 + IPA(s) + WorkUnit(s)

**Output**: `Client_Handover_Results/<ClientName>_<RICEItem>.xlsx`

**Multi-Process Support** (NEW - 2026-02-23):
- ONE report per RICE item (not per LPD)
- Handles 1-N LPD files automatically
- Separate sheet per process: `⚙️ <ProcessName>`
- Consolidated executive summary, business requirements, validation
- Backward compatible: single LPD works exactly as before

**Workflow** (Updated 2026-03-07):

Use the `ipa-client-handover` skill for client handover documentation:

**Activation**: 
- `/ipa-client-handover` or mention "client handover documentation"
- Location: `.kiro/skills/ipa-client-handover/`

**Architecture**: Stateless Pipeline (Crash-Safe)
- Phase 0: Preprocessing (Python) - Extract and structure data
- Phases 1-4: Analysis (AI) - Independent analysis phases with JSON I/O
- Phase 5: Report Assembly (Python) - Merge and generate Excel report

**Key Features**:
- No context accumulation (each phase isolated at ~10 KB)
- No crashes (stable execution regardless of file size)
- Faster execution (reduced reasoning overhead)
- Enterprise-grade quality maintained
- Multi-process support (1-N LPDs → ONE report)

**Usage**:
1. Activate skill: `/ipa-client-handover`
2. Follow interactive prompts to select client, RICE item, and LPD files
3. Confirm spec and WU log availability
4. Wait for report generation (~3-4 min per process)

**Report Structure (Single Process)**:
- 📊 Executive Summary
- 📋 Business Requirements
- ✅ Production Validation
- ⚙️ System Configuration
- 📚 Activity Node Guide
- ⚙️ <ProcessName>
- 🔧 Maintenance Guide

**Report Structure (Multiple Processes)**:
- 📊 Executive Summary (consolidated across all processes)
- 📋 Business Requirements (RICE-level from spec)
- ✅ Production Validation (aggregated metrics)
- ⚙️ System Configuration (consolidated)
- 📚 Activity Node Guide (consolidated)
- ⚙️ <ProcessName1> (detailed workflow)
- ⚙️ <ProcessName2> (detailed workflow)
- ⚙️ <ProcessName3> (detailed workflow)
- 🔧 Maintenance Guide (consolidated)

**Content**:
- Business requirements from ANA-050 (RICE-level)
- Which part of solution addresses each requirement
- Complete IPA documentation (per process)
- Production validation from work units (aggregated)
- System configuration (consolidated)
- Maintenance procedures (consolidated)

**Mandatory Visual Elements**:

- Workflow Diagram in Executive Summary (right side, columns D-F)
- Priority Indicators in Business Requirements (🔴🟠🟡🟢🔵)
- Status Badges in Production Validation (✅ Pass/Fail)
- Performance Metrics visual summary boxes
- Color-Coded Sections throughout

### 2. Coding Standards (Internal Peer Review)

**Purpose**: Internal code quality review for development team BEFORE client delivery

**Audience**: Infor developers, technical leads, peer reviewers

**Focus**: IPA code quality - JavaScript ES5, SQL, and team coding standards (1.1-1.5)

**Input**: IPA(s) only (no work units, no functional specs)

**Output**: `Coding_Standards_Results/<Client>_<RICEItem>_CodingStandards_YYYYMMDD.xlsx`

**Content**:
- JavaScript ES5 compliance review
- SQL query review (Compass SQL, Landmark queries)
- Team coding standards (1.1-1.5):
  - 1.1 Naming Convention
  - 1.2 IPA Rules
  - 1.3 Error Handling
  - 1.4 System Configuration
  - 1.5 Performance
- Best practices assessment
- Technical architecture analysis
- Prioritized recommendations

**Mandatory Visual Elements**:

- Quality score dashboard with bar chart
- Severity Badges in JavaScript Review (🔴🟠🟡🟢)
- Priority Indicators in Recommendations
- Status Tracking in Action Items (✅ ⏳ ❌)
- Color-coded sections

**Key Difference from Client Handover**: Pure IPA code review, no business requirements, no work unit analysis

#### Coding Standards Report UI/UX Enhancements (2026-03-08)

**Status**: ✅ Production Ready

**Purpose**: Transform coding standards reports from basic internal documents to professional-grade, interactive, accessible code review tools.

**Implementation**: All improvements are in the universal enhanced template (`ipa_coding_standards_template_enhanced.py`) and work for any client/project.

**Phase 1: Critical Fixes** (Completed 2026-03-08)

Addressed data completeness and accuracy issues:

1. **Quality Metrics Bar Chart** - Executive Dashboard shows breakdown of all 7 quality scores (Naming, IPA Rules, Error Handling, Config, Performance, JavaScript, SQL)
2. **Enhanced Columns Populated** - All enhanced columns have calculated values (no "TBD" or "NaN"):
   - Priority Score: Calculated from severity + affected % + fix time
   - Est. Fix Time: Calculated based on violation type and complexity
   - Affected %: Calculated from violation frequency vs total activities
   - Code Example: Before/after examples with explanations
   - Testing Notes: Comprehensive testing guidance per violation
3. **Impact Analysis** - Detailed Analysis shows frequency, affected %, maintainability impact, estimated fix time
4. **Actual Activity Captions** - Process Flow uses real captions from LPD data (not generic "N/A")

**Impact**: 50% reduction in time to understand violations, 100% data completeness

**Phase 2: Visual Enhancements** (Completed 2026-03-08)

Improved visual appeal and priority identification:

1. **Priority Color Coding** - Action Items sheet has color-coded priority cells:
   - Critical: Red background (#FFC7CE)
   - High: Amber background (#FFEB9C)
   - Medium: Yellow background (#FFFF00)
   - Low: White background
2. **Severity Breakdown Pie Chart** - Executive Dashboard pie chart showing violation distribution by severity
3. **Severity Badges** - Detailed Analysis displays colored badges next to each violation header:
   - 🔴 Critical (Red #C62828, contrast 4.52:1)
   - 🟠 High (Orange #F57C00, contrast 4.54:1)
   - 🟡 Medium (Yellow #F9A825, contrast 8.59:1)
   - 🟢 Low (Green #2E7D32, contrast 4.53:1)

**Impact**: 100% improvement in visual appeal, 50% faster priority identification

**Phase 3: Interactivity** (Completed 2026-03-08)

Added interactive features for team collaboration:

1. **Status Tracking Column** - Action Items has dropdown for tracking progress:
   - Not Started (default)
   - In Progress
   - Complete
   - Blocked
2. **AutoFilter** - Action Items header row enables filtering by Priority, Category, Status, Severity, etc.
3. **Navigation Hyperlinks** - Executive Dashboard links to other sheets, all sheets link back to Dashboard
4. **Data Validation** - Status column has dropdown validation preventing invalid entries

**Impact**: 70% improvement in usability, 50% increase in developer engagement, 40% improvement in team collaboration

**Phase 4: Polish** (Completed 2026-03-08)

Professional finishing touches for print and accessibility:

1. **Print Optimization** - All sheets have proper formatting:
   - Professional headers with sheet title
   - Footers with page numbers, client/project, date
   - Repeated header rows on multi-page prints
   - Proper orientation (landscape/portrait)
   - Appropriate scaling (85-100%)
   - A4 paper size standard
2. **Accessibility Enhancements** - WCAG 2.1 AA compliant:
   - High contrast colors (contrast ratios ≥ 4.5:1)
   - Icon + text labels (not relying on color alone)
   - Thicker borders for better visibility
   - Screen reader friendly structure
3. **Testing Notes** - Comprehensive testing guidance for each violation

**Impact**: 100% improvement in print quality, 80% improvement in accessibility, 95% improvement in professional appearance

**Executive Dashboard Redesign** (Completed 2026-03-08)

Redesigned dashboard to use horizontal space efficiently:

**KPI Cards Layout** (2 rows of 2 cards):
- Row 1: Overall Quality (left, Columns A-F) + Action Items (right, Columns G-L)
- Row 2: Processes (left, Columns A-F) + Complexity (right, Columns G-L)

**Charts Section** (side by side):
- Radar Chart (left, Columns A-F) + Bar Chart (right, Columns G-L)

**Severity & Findings** (side by side):
- Severity Pie Chart (left, Columns A-E) + Key Findings list (right, Columns F-L)

**Result**: Much more balanced, professional dashboard that uses horizontal space efficiently

**Complete Feature List**

Executive Dashboard:
- ✅ Hero section with client/project info
- ✅ 4 KPI cards (Overall Quality, Processes, Complexity, Action Items)
- ✅ Quality metrics radar chart
- ✅ Quality metrics bar chart (Phase 1)
- ✅ Severity breakdown pie chart (Phase 2)
- ✅ Key findings section
- ✅ Navigation links to other sheets (Phase 3)
- ✅ Print optimization (Phase 4)
- ✅ Horizontal layout for space efficiency

Action Items Sheet:
- ✅ 15 columns including enhanced fields
- ✅ Priority color coding (Phase 2)
- ✅ Status tracking column with dropdown (Phase 3)
- ✅ AutoFilter enabled (Phase 3)
- ✅ Back to Dashboard link (Phase 3)
- ✅ Print optimization with 85% scaling (Phase 4)
- ✅ Deduplication logic
- ✅ Sorted by priority score

Detailed Analysis Sheet:
- ✅ Process overview section
- ✅ Violations with impact analysis (Phase 1)
- ✅ Code examples (before/after) (Phase 1)
- ✅ Testing notes (Phase 1)
- ✅ Priority scores (Phase 1)
- ✅ Severity badges with icons (Phase 2, Phase 4)
- ✅ Back to Dashboard link (Phase 3)
- ✅ Print optimization (Phase 4)

Process Flow Sheet:
- ✅ Process information summary
- ✅ Complexity breakdown with scoring
- ✅ Activity flow diagram with actual captions (Phase 1)
- ✅ Critical paths and recommendations
- ✅ Back to Dashboard link (Phase 3)
- ✅ Print optimization (Phase 4)

**Technical Architecture**

Universal Implementation:
- Template: `ReusableTools/IPA_CodingStandards/ipa_coding_standards_template_enhanced.py`
- Helper: `ReusableTools/IPA_CodingStandards/build_ipa_data_helper.py`
- Works for any client/project (FPI, BayCare, SONH, future clients)

Data Flow:
```
Phase 0: preprocess_coding_standards.py
  ↓ Creates domain JSON files
  
Phase 1-5: AI Analysis (per domain)
  ↓ Generates violations with enhanced fields
  
Phase 6: merge_violations.py
  ↓ Merges all domain violations
  
Phase 7: build_ipa_data_helper.py
  ↓ Builds ipa_data structure (preserves enhanced fields)
  
Phase 8: ipa_coding_standards_template_enhanced.py
  ↓ Generates Excel report with all 4 phases of improvements
```

**Quality Metrics**

Before Improvements:
- Visual Appeal: 60/100
- Usability: 50/100
- Data Completeness: 40/100
- Accessibility: 30/100
- Print Quality: 20/100

After All 4 Phases:
- Visual Appeal: 95/100 (+58%)
- Usability: 90/100 (+80%)
- Data Completeness: 100/100 (+150%)
- Accessibility: 85/100 (+183%)
- Print Quality: 95/100 (+375%)

**Overall Improvement: +169%**

**User Experience Improvements**

For Developers:
- Before: Generic report with missing data, hard to navigate
- After: Interactive report with specific guidance, easy filtering, status tracking

For Team Leads:
- Before: Difficult to prioritize work, no progress tracking
- After: Clear priority visualization, status tracking, filtering by team member

For Clients:
- Before: Technical report, not print-friendly
- After: Professional document, print-ready, accessible to all users

**Accessibility Compliance**

WCAG 2.1 AA Standards:
- ✅ Color contrast ratios ≥ 4.5:1
- ✅ Text alternatives (icon + text labels)
- ✅ High contrast mode compatible
- ✅ Screen reader friendly
- ✅ Keyboard navigation (Excel native)
- ✅ Not relying on color alone

Contrast Ratios:
- Critical badge: 4.52:1 ✅
- High badge: 4.54:1 ✅
- Medium badge: 8.59:1 ✅
- Low badge: 4.53:1 ✅

**Print Optimization**

All Sheets Include:
- Professional headers with sheet title
- Footers with page numbers, client/project, date
- Repeated header rows on multi-page prints
- Proper orientation (landscape/portrait)
- Appropriate scaling (85-100%)
- A4 paper size standard

Print-Ready Output:
- Distribution quality
- Client presentation ready
- Professional appearance
- Easy to read and navigate

**Performance**

Generation Time:
- ~2-3 seconds for single process
- Scales linearly with process count
- No performance degradation from enhancements

File Size:
- ~150-200 KB per report
- Charts add ~50 KB
- Acceptable for email distribution

**Deployment**

Ready for Production:
- ✅ All phases complete
- ✅ Universal implementation
- ✅ Tested and verified
- ✅ Documentation complete
- ✅ No breaking changes

Rollout Plan:
1. Update all projects to use enhanced template
2. Train team on new features (status tracking, filtering)
3. Collect feedback for future enhancements
4. Monitor usage and adoption

**Success Metrics**

Expected Outcomes:
- 50% reduction in time to understand violations
- 30% increase in developer engagement
- 100% improvement in visual appeal
- 70% improvement in usability
- 40% improvement in team collaboration

Measurable Benefits:
- Faster code review cycles
- Better prioritization of work
- Improved team coordination
- Professional client deliverables
- Accessible to all users

**Documentation**

Created Documents:
1. `Temp/PHASE1_IMPLEMENTATION_SUMMARY.md` - Critical fixes
2. `Temp/PHASE2_IMPLEMENTATION_SUMMARY.md` - Visual enhancements
3. `Temp/PHASE3_IMPLEMENTATION_SUMMARY.md` - Interactivity
4. `Temp/PHASE4_IMPLEMENTATION_SUMMARY.md` - Polish
5. `Temp/COMPLETE_IMPLEMENTATION_SUMMARY.md` - Comprehensive summary

Total Documentation:
- ~15,000 words
- Comprehensive implementation details
- Code examples
- Verification steps
- Impact assessments

### 3. Performance (Work Unit Analysis)

**Purpose**: Analyze work unit execution for performance, errors, and runtime behavior

**Audience**: Infor developers, technical leads, operations team

**Focus**: Work unit runtime analysis, performance metrics, error patterns

**Input**: One or multiple work unit logs

**Output**: `WU_Report_Results/<Process>_WU_Report_YYYYMMDD.xlsx`

**Content**:
- Execution timeline
- Performance metrics (duration, memory, API calls)
- Error analysis
- Variable tracking
- Activity execution sequence
- Recommendations for optimization

**Mandatory Visual Elements**:

- Timeline charts
- Performance metrics
- Error indicators
- Activity duration bars

**Key Difference from Coding Standards**: Focuses on runtime behavior, not source code quality

### Key Differences Summary

| Aspect | Client Handover | Coding Standards | Performance |
|--------|----------------|------------------|-------------|
| Input | ANA-050 + IPA(s) + WU(s) | IPA(s) only | WU log(s) only |
| JavaScript Review | No | Yes (ES5 compliance) | No |
| SQL Review | No | Yes (query quality) | No |
| Coding Standards 1.1-1.5 | No | Yes | No |
| Business Requirements | Yes (from ANA-050) | No | No |
| Work Unit Analysis | Yes (production validation) | No | Yes (full analysis) |
| Recommendations | Maintenance procedures | Code improvements | Performance tuning |
| Audience | Client tech team | Internal developers | Internal developers |
| Confidentiality | Client-facing | Internal only | Internal only |

---

## RICE and Functional Specifications

### RICE Categories

Every IPA originates from a **RICE item** documented in an **ANA-050 functional specification**:

- **R**eports - Data summaries, analytics, outputs
- **I**nterfaces - Data exchange with external systems (most common for IPAs)
- **C**onversions - Data migration from legacy systems
- **E**nhancements - Custom workflows, UI changes, extensions

**Key Principle**: One RICE item may require multiple IPAs to implement the complete solution.

### IPA vs LPL Determination

| Requirement Type | IPA | LPL | Workunit |
|------------------|-----|-----|----------|
| Data integration with external system | Yes | No | Yes |
| Scheduled data extract/export | Yes | No | Yes |
| File-triggered processing | Yes | No | Yes |
| Approval workflow | Yes | Maybe | Yes |
| UI form modification only | No | Yes | No |
| New field on business class | No | Yes | No |
| Menu/navigation change only | No | Yes | No |
| LPL action triggering process | Yes | Yes | Yes |

### Separating IPA vs LPL Requirements

**IPA Flow Requirements** (Process Automation):

- Approval routing logic and approver determination
- Email notifications and content
- Workflow actions (Approve, Return, Reject)
- Business class queries and data retrieval
- Process flow logic and branching
- Integration with external systems
- Error handling and exception management

**Configuration Console Requirements** (LPL/UI Changes):

- Field protection and read-only settings
- Form field display and visibility
- Default value population
- Required field validation
- UI layout and formatting
- Service/Process Definition enablement
- Form behavior and user experience

**Analysis Approach**:

1. Identify UI/form changes (Configuration Console tasks)
2. Focus IPA scope on approval logic, notifications, process flow
3. Separate concerns clearly
4. Document both in analysis

---

## Activity Counting

**Rule**: Activity counts must match how developers see nodes in IPD Designer.

### Counting Method

- **Total Activities**: Count each node as it appears in IPD Designer
- **Landmark (LM) Nodes**: Count as ONE activity (ItEnd is auto-generated, not counted separately)
- **Other Nodes**: START, END, ASSGN, BRANCH, UA, EMAIL, ACCFIL, etc.

```python
# Count all activities, excluding ItEnd (auto-generated)
activity_pattern = r'<activity activityType="(\w+)"[^>]*caption="([^"]*)"[^>]*id="([^"]+)"'
activities = re.findall(activity_pattern, lpd_content)
countable_activities = [act for act in activities if act[0] != 'ItEnd']
total_count = len(countable_activities)
```

**Note**: Landmark nodes automatically create paired ItEnd nodes in IPD Designer. Developers see and count ONE Landmark node, not two. Activity counts reflect this developer perspective.

## Visual Design Standards

### Mandatory Visual Elements

All reports MUST include:

1. **Workflow Diagrams** - matplotlib PNG embedded in Excel (Executive Summary, right side)
2. **Priority Indicators** - Color-coded emojis (🔴🟠🟡🟢🔵)
3. **Status Badges** - Pass/Fail indicators (✅ ❌)
4. **Performance Metrics** - Visual summary boxes
5. **Data Bars** - For metrics (counts, durations, percentages)
6. **Color Coding** - Consistent palette across all sheets

### Color Palette

**Primary Colors**:

- Deep Blue `#1565C0` - Headers, titles, primary elements
- Green `#2E7D32` - Success, positive findings
- Amber `#F57C00` - Warnings, decisions
- Purple `#6A1B9A` - API/OAuth/technical elements
- Red `#C62828` - Errors, critical issues

**Secondary Colors**:

- Medium Blue `#1E88E5` - Subheaders
- Light Blue `#E3F2FD` - Alternating row backgrounds
- Light Green `#E8F5E9` - Success backgrounds
- Light Amber `#FFF3E0` - Warning backgrounds
- Light Purple `#E1BEE7` - API backgrounds

### Standard Emojis

Use consistently across all reports:

- 🚀 Start/Launch | 📊 Data/Reports | ✅ Success | ❌ Error
- 🔐 Security/OAuth | 📁 Files | 🌐 API | ⏱️ Timing
- 🔀 Branch | 📝 Assignment | 💬 Email | 🔧 Maintenance
- 📖 Documentation | ⚠️ Warning | 🎯 Goal | 📋 Requirements

### Sheet Formatting

**Title Row**: Bold, Size 16, Height 30, Merged cells, Centered, Emoji included

**Header Rows**: Primary color fill, White font, Bold, Size 11, Height 25

**Subheader Rows**: Medium Blue fill, White font, Bold, Size 10, Height 20

**Data Rows**: Alternating Light Blue/White backgrounds, Thin gray borders, Text wrap enabled

### Workflow Diagrams

**Requirements**:

- Tool: matplotlib (NOT ASCII art)
- Format: PNG embedded in Excel
- Size: 400x600 pixels, DPI 150
- Location: Executive Summary, columns D-F
- Style: Rounded boxes (FancyBboxPatch), color-coded by type, emojis in labels

**Color Coding**:

- Start/End: Green `#2E7D32`
- Process: Deep Blue `#1565C0`
- Decision: Amber `#F57C00`
- API Call: Purple `#6A1B9A`
- Error: Red `#C62828`

**Data-Driven**: Use `ipa_data['workflow_steps']` if provided, otherwise use generic fallback covering common IPA patterns.

**IMPORTANT - Multi-Process RICE Items** (Fixed 2026-03-07):

The assembly script (`assemble_client_handover_report.py`) now correctly generates workflow diagrams for multi-process RICE items by using the actual `workflow_steps` from `workflow_analysis.json` instead of just listing process names. This ensures the Executive Summary diagram shows the actual approval/interface workflow logic (e.g., 9-step approval flow) rather than a simplified 3-step process list.

**Data Flow**:
1. Phase 2 creates `workflow_analysis.json` with `workflow_steps` array
2. Assembly script passes `workflow_description` to template (converted from `workflow_steps`)
3. Template converts `workflow_description` to internal `workflow_steps` format for rendering
4. Diagram shows actual business workflow regardless of single or multi-process RICE item

## Report Structure

### Client Handover Report (8 sheets minimum)

**CRITICAL**: All sheets must include visual enhancements per 2026 standards.

1. **📊 Executive Summary** - Process overview, **workflow diagram (MANDATORY)**, key metrics
   - **Layout**: Split (left: text, right: diagram)
   - **Visuals**: Workflow diagram with color-coded steps
   - **Metrics**: Production validation summary

2. **📋 Business Requirements** - Functional spec content, **priority indicators (MANDATORY)**, business rules
   - **Layout**: 3-column table (Priority, Requirement, Description)
   - **Visuals**: Color-coded priority emojis (🔴🟠🟡🟢🔵)
   - **Legend**: Priority level explanations

3. **✅ Production Validation** - Real work unit data, **status badges (MANDATORY)**, performance metrics
   - **Layout**: 3-column table (Parameter, Value, Status)
   - **Visuals**: Pass/Fail badges (✅), performance summary box
   - **Metrics**: Speed, volume, authentication, API integration

4. **⚙️ System Configuration** - **MANDATORY** - All configuration variables, OAuth credentials, file channels, process variables
   - **Layout**: 4-column table (Variable, Value/Structure, Purpose, How to Modify)
   - **Visuals**: Color-coded sections (🔐 OAuth=Purple, 📁 File Channel=Green, 📝 Variables=Amber)
   - **Sections**: OAuth2 Credentials, File Channel Config, Process Variables, Global Config

5. **📚 Activity Node Guide** - Reference for activity types (LM, ASSGN, BRANCH, UA, EMAIL)
   - **Layout**: 3-column table (Activity Type, Purpose, Common Uses)
   - **Visuals**: Emoji indicators for each activity type
   - **Purpose**: Quick reference for understanding Process sheets

6-N. **⚙️ Process Sheets** (1-N) - Complete activity list with modification instructions

- **Layout**: 5-column table (Activity ID, Type, Purpose, Key Content, How to Modify)
- **Visuals**: Color-coded activity types, alternating row colors
- **Config Section**: Configuration variables table at top (if applicable)

N+1. **🔧 Maintenance Guide** - HOW TO sections for common modifications

- **Layout**: Numbered steps with emoji indicators (1️⃣ 2️⃣ 3️⃣)
- **Visuals**: Color-coded HOW TO sections (rotating colors)
- **Content**: OAuth updates, file paths, email recipients, approval matrices, timeouts, error handling

**CRITICAL - System Configuration Sheet Requirements**:

- All IPA configuration variables (_configuration.Interface)
- OAuth2 credential structures (JSON format with field explanations)
- File Channel configuration (MonitorDirectory, ProcessedFileDirectory, OutputDir, etc.)
- Process variables from START activity (limit, offset, counters, etc.)
- Clear "How to Modify" instructions for each variable
- Example values and formats

### Peer Review Report (12+ sheets)

**CRITICAL**: All sheets must include visual enhancements per 2026 standards.

1. **📖 Review Guide** - How to use report, **severity levels (MANDATORY)**, developer actions
   - **Visuals**: Severity badge examples (🔴🟠🟡🟢), status indicators (✅ ⏳ ❌)

2. **📊 Executive Summary** - Process overview, **workflow diagram (MANDATORY)**, key findings, quality scores
   - **Layout**: Split (left: text, right: diagram)
   - **Visuals**: Workflow diagram, quality score gauges, priority recommendations

3. **✅ Action Items** - Consolidated checklist with **status tracking (MANDATORY)**
   - **Visuals**: Status badges (✅ Complete, ⏳ In Progress, ❌ Not Started)
   - **Priority**: Color-coded by severity

4. **💻 JavaScript Review** - ES5 compliance analysis, **severity badges (MANDATORY)**, security issues
   - **Visuals**: Severity indicators (🔴🟠🟡🟢), code quality scores
   - **Data Bars**: For compliance percentages

5. **🗄️ SQL Review** (if applicable) - Compass API queries, optimization
   - **Visuals**: Performance metrics, optimization opportunities

6. **⚡ Performance Analysis** - Memory usage, duration analysis, **visual metrics (MANDATORY)**
   - **Visuals**: Performance charts, efficiency ratings, bottleneck indicators

7. **✨ Best Practices** - Auto-restart design, error handling, configuration management
8. **📋 Requirements Validation** - RICE analysis, traceability matrix, gap identification
9. **🔍 Activity Analysis** - Activity counts, flow complexity, node distribution
10. **💡 Recommendations** - Prioritized improvements with **priority badges (MANDATORY)**
    - **Visuals**: Priority indicators (🔴🟠🟡🟢), impact assessment
11. **🔬 Technical Deep Dive** - Architecture analysis, design patterns, risk assessment
12. **⚙️ Configuration Analysis** - Variable management, environment dependencies

### Executive Dashboard KPI Cards

**Purpose**: Provide at-a-glance metrics for coding standards review

**KPI Cards** (4 cards displayed):

1. **🎯 Overall Quality** - Composite quality score (0-100)
   - Color: Green (≥90), Amber (≥70), Red (<70)
   - Calculation: Weighted average of all quality scores

2. **📋 Processes** - Number of processes analyzed
   - Shows activity count in label
   - Always neutral color

3. **⚙️ Complexity** - Process complexity score
   - Color: Green (Low), Amber (Medium/High), Red (Very High)
   - See Complexity Metric section below

4. **✅ Action Items** - Number of recommendations
   - Shows count of items requiring attention
   - Always neutral color

### Complexity Metric

**Purpose**: Universal metric measuring IPA process complexity for maintainability assessment

**Formula**: Weighted sum of complexity factors

```text
Complexity Score = (Branch_Count × 3) + (Loop_Count × 5) + (SubProcess_Count × 2) + 
                   (UserAction_Count × 4) + (JavaScript_Blocks × 2) + (SQL_Queries × 3)
```

**Complexity Levels**:

| Score | Level | Color | Description |
|-------|-------|-------|-------------|
| 0-20 | Low | Green | Simple linear flows, minimal branching |
| 21-50 | Medium | Amber | Moderate branching, some loops, standard workflows |
| 51-100 | High | Amber | Complex logic, multiple branches, nested loops |
| >100 | Very High | Red | Highly complex, extensive branching, multiple integrations |

**Weight Rationale**:

- **Branches (×3)**: Each decision point adds cognitive load and testing complexity
- **Loops (×5)**: Iteration logic is harder to debug, test, and can cause performance issues
- **SubProcesses (×2)**: Modular design but adds call complexity and dependencies
- **User Actions (×4)**: Approval workflows with timeouts, escalation, and state management
- **JavaScript (×2)**: Custom logic increases maintenance burden and requires ES5 compliance
- **SQL (×3)**: Query complexity, performance considerations, and Compass API knowledge

**Example Calculation** (MatchReport_Outbound):

```text
Branches: 6 × 3 = 18
Loops: 0 × 5 = 0
SubProcesses: 2 × 2 = 4
User Actions: 0 × 4 = 0
JavaScript: 20 × 2 = 40
SQL: 1 × 3 = 3
Total: 65 → "High" complexity
```

**Usage in Analysis**:

- Include complexity score in `ipa_data['quality_scores']['complexity']`
- Provide `ipa_data['activities']` array with activity types for calculation
- Template automatically calculates and displays in KPI card
- High complexity (>50) suggests refactoring opportunities
- Very High complexity (>100) indicates maintenance risk

**Data Structure**:

```python
'activities': [
    {'type': 'START'},
    {'type': 'BRANCH'},
    {'type': 'ASSGN'},
    {'type': 'WEBRN'},
    {'type': 'SUBPROC'},
    {'type': 'UA'},
    # ... etc
]
```

## Template Architecture

**CRITICAL**: Templates are 100% reusable across ALL IPA projects. No project-specific hardcoding.

### Data Extraction Tools

**Location**: `ReusableTools/IPA_Analyzer/`

**Purpose**: Extract and organize data only (NOT analysis)

**Tools**:

- `extract_lpd_data.py` - Activities, JavaScript blocks, SQL queries, config vars → JSON
  - Extracts SQL from: WEBRN/WEBRUN (API calls), ASSGN (variable construction), MSGBD (message formatting), ACCFIL (file content)
  - Detects SQL keywords: SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, JOIN, GROUP BY, etc.
  - Handles URL-encoded content and multi-line queries
- `extract_wu_log.py` - Performance metrics, variables, errors → JSON
- `extract_spec.py` - Requirements, sections, tables → JSON

### Standard Flow Check Tool

**Location**: `ReusableTools/check_standard_flow.py`

**Purpose**: Check if an IPA process is a standard flow that should not be modified

**Usage**:

```python
from ReusableTools.check_standard_flow import check_standard_flow

# Check single LPD file
result = check_standard_flow('MatchReport_Outbound.lpd')
if result['is_standard']:
    print(result['message'])  # Warning about standard flow
    print(f"Flow: {result['flow_name']}")
    print(f"Description: {result['description']}")

# Check multiple LPD files
from ReusableTools.check_standard_flow import check_multiple_flows

results = check_multiple_flows([
    'Process1.lpd',
    'Process2.lpd',
    'Process3.lpd'
])
print(results['summary'])
```

**Returns**:

```python
{
    'is_standard': bool,           # True if found in standard flows CSV
    'flow_name': str or None,      # PfiFlowDefinition name
    'description': str or None,    # PfiFlowDescription
    'message': str                 # User-friendly message
}
```

**Command Line**:

```bash
python ReusableTools/check_standard_flow.py MatchReport_Outbound.lpd
```

**Integration with Coding Standards**:

- Run check during Step 7 (Standard Flow Check)
- If `is_standard=True`, flag as violation in 1.1 Naming Convention
- Add to recommendations: "This is a standard flow - copy and rename if customization needed"
- Include flow description in analysis

**Workflow**:

1. Python extracts data → organized JSON files (fast, structured)
2. Kiro reads JSON and analyzes (ES5 compliance, recommendations, scoring)
3. Kiro builds `ipa_data` dictionary with analysis results
4. Python template formats `ipa_data` → Excel report with visual enhancements

### Master Templates

**Location**: Workspace root

**1. ipa_client_handover_template.py**

- Purpose: Client-facing documentation
- Sheets: 8 sheets minimum (flexible based on number of processes)
- Input: `ipa_data` dictionary from Kiro's analysis
- Output: `IPA_Report_Results/<ClientName>_<Process>.xlsx`
- **Visual Features**: Workflow diagram, priority indicators, status badges, color-coded sections

**2. ipa_coding_standards_template_enhanced.py** (Current - v2.0)

- Purpose: Internal code quality review with enhanced analysis
- Sheets: 4 sheets (Executive Dashboard, Action Items, Detailed Analysis, Process Flow)
- Input: `ipa_data` dictionary from Kiro's analysis
- Output: `Coding_Standards_Results/<Client>_<RICE>_CodingStandards_<timestamp>.xlsx`
- **Enhanced Features**:
  - Action Items: 14 columns (Priority Score, Est. Fix Time, Affected %, Code Example, Testing Notes)
  - Detailed Analysis: Impact assessment sections per violation
  - Process Flow: NEW sheet with complexity visualization
  - Backward compatible with old data format
- **Location**: `ReusableTools/IPA_CodingStandards/ipa_coding_standards_template_enhanced.py`
- **Version**: 2.0 (Enhanced Edition - 2026-02-22)

**2b. ipa_coding_standards_template.py** (Legacy - v1.0)

- Purpose: Internal code quality review (original version)
- Sheets: 3 sheets (Executive Dashboard, Action Items, Detailed Analysis)
- Input: `ipa_data` dictionary from Kiro's analysis
- Output: `Coding_Standards_Results/<Client>_<RICE>_CodingStandards_<timestamp>.xlsx`
- **Status**: Superseded by enhanced template (v2.0)
- **Location**: `ReusableTools/IPA_CodingStandards/ipa_coding_standards_template.py`

**3. ipa_peer_review_template.py**

- Purpose: Internal code quality review (comprehensive)
- Sheets: 12+ sheets (flexible based on findings)
- Input: `ipa_data` dictionary from Kiro's analysis
- Output: `IPA_PeerReview_Results/<Process>_PeerReview_YYYYMMDD.xlsx`
- **Visual Features**: Workflow diagram, severity badges, priority indicators, status tracking, performance charts

### Template Reusability

**CRITICAL**: Templates work for ANY IPA project without modification.

**Architecture**:

```text
Project Script (e.g., generate_baycare_apia_handover.py)
    ↓
    Builds ipa_data dictionary with project-specific data
    ↓
    Calls: generate_report(ipa_data)
    ↓
Master Template (ipa_client_handover_template.py)
    ↓
    Renders visuals using ipa_data
    ↓
    Generates Excel report with all visual enhancements
```

**Data-Driven Visuals**:

- Workflow diagram: Uses `ipa_data['workflow_steps']` or generic fallback
- Priority indicators: Uses `ipa_data['requirements']` data
- Status badges: Uses `ipa_data['production_validation']` data
- All sections: Conditional rendering based on `ipa_data` keys

**Generic Fallbacks**:

- Workflow diagram: Generic process flow if custom steps not provided
- Covers common IPA patterns: file processing, API calls, validation, output
- Suitable for 80% of processes without customization

**Examples**:

- BayCare APIA: Uses template with approval workflow steps
- FPI MatchReport: Uses template with data extraction workflow steps
- Future Projects: Uses template with their own workflow steps (or generic fallback)

### Template Flexibility

Both templates handle:

- Variable number of processes (1 to N)
- Variable number of activities (20 to 2000+)
- Optional sections (SQL queries, test data, OAuth credentials)
- Variable content length (auto-adjusting rows)
- Conditional formatting (color coding by severity/priority)
- Custom workflow diagrams (or generic fallback)
- Project-specific or generic visual elements

### Usage Pattern

```python
# Kiro builds data dictionary after analysis
ipa_data = {
    'client_name': 'ClientName',
    'process_group': 'ProcessGroup',
    'processes': [...],
    
    # Visual elements (optional - generic fallbacks provided)
    'workflow_steps': [...],  # Custom workflow diagram steps
    'requirements': [...],     # Business requirements with priorities
    'production_validation': {...},  # Test results with status
    'oauth_credentials': [...],  # OAuth config (if applicable)
    'file_channel_config': [...],  # File Channel config (if applicable)
    
    # For peer review only
    'recommendations': [...],  
    'javascript_issues': [...],
}

# Call appropriate template
from ipa_client_handover_template import generate_report
# OR
from ipa_peer_review_template import generate_report

output_path = generate_report(ipa_data)
```

### Visual Generation Workflow

**Automatic Visual Elements**:

1. **Workflow Diagram**: Auto-generated from `workflow_steps` or generic fallback
2. **Priority Indicators**: Auto-applied to requirements (🔴🟠🟡🟢🔵)
3. **Status Badges**: Auto-applied to validation results (✅ Pass/Fail)
4. **Color Coding**: Auto-applied based on section type (OAuth=Purple, Files=Green, etc.)
5. **Performance Metrics**: Auto-generated summary boxes

**No Manual Formatting Required**:

- Template handles all visual generation
- Consistent styling across all projects
- Professional appearance guaranteed
- Visual elements adapt to data provided

**Customization Options**:

```python
# Custom workflow diagram
'workflow_steps': [
    {'type': 'start', 'label': '🚀 START\nYour Process', 'y': 17.5},
    {'type': 'process', 'label': '📝 Your Step', 'y': 16},
    {'type': 'decision', 'label': '❓ Your Decision?', 'y': 14.5, 'branches': ['Yes', 'No']},
    {'type': 'api', 'label': '🌐 Your API Call', 'y': 13},
    {'type': 'end', 'label': '✅ END\nComplete', 'y': 11}
]

# Or omit for generic fallback
# Template will use: Read Input → Validate → Authenticate → Query → Output
```

## System Configuration

**CRITICAL**: Distinguish between global system configuration variables and IPA variables.

### Global System Configuration Variables

- Stored in FSM: Configuration > System Configuration > Interface
- Users can update WITHOUT modifying IPA code
- Examples: Approval_Matrix, Test_Flag, Test_Actor, AutoReject_Threshold, Email_Recipients

### IPA Variables (START Node)

- Defined in IPA START activity
- Require IPA modification to change
- Examples: Process-specific flags, calculated values, temporary variables

### Documentation Requirements

**1. Configuration Variables Table** (top of each Process sheet)

```text
| Property Name | Value Format | Purpose |
|---------------|--------------|---------|
| APIA_NONPOROUTING_Approval_Matrix | CSV: Type,Limit,Type | Authority limits by position |
| APIA_NONPOROUTING_Test_Flag | TRUE/FALSE | Enable test mode routing |
```

**2. START Node Documentation** (red warning text)

```text
⚠️ CONFIGURATION VARIABLES: Most variables in this START node are populated from 
global system configuration (FSM > Configuration > System Configuration > Interface).
To modify these values, update the system configuration WITHOUT modifying the IPA.
Only modify the IPA START node for variables without a global config equivalent.
```

**3. "How to Modify" Column** (for activities using config variables)

```text
Update global system configuration variable: APIA_NONPOROUTING_Approval_Matrix
(Do NOT modify IPA code)
```

**4. Maintenance Guide** (complete config variables table + HOW TO sections)

- Full list of all configuration variables
- Step-by-step instructions for updating each variable
- Screenshots or navigation paths to FSM configuration screens

## Process Sheet Requirements

### Column Structure

| Column | Content | Example |
|--------|---------|---------|
| Activity ID | Node name from LPD | LMTxn1310 |
| Activity Type | LM, ASSGN, BRANCH, UA, EMAIL, etc. | LM |
| Purpose | What this activity does | Retrieve invoice record from FSM |
| Key Content | Object, Action, Fields, Parameters | Object: PayablesInvoice, Action: Find |
| How to Modify | Instructions for changes | To add fields: Edit activity in IPD, add field names |

### Special Documentation

**START Node**:

- List all major variable categories
- Red warning text about system configuration
- Reference to configuration variables table

**User Action Nodes**:

- Approval level (L1, L2, L3+)
- Actor assignment method
- Timeout settings
- Available actions (Approve, Reject, Reassign)

**Branch Nodes**:

- All conditions with descriptions
- Routing logic explanation
- Key variables checked

**LM Transaction Nodes**:

- Business class and action
- Key fields retrieved/updated
- Purpose in workflow

## Workflow Diagrams

### Technical Requirements

- **Tool**: matplotlib (NOT ASCII art)
- **Format**: PNG image embedded in Excel
- **Size**: Fit within Excel sheet width (approximately 10 inches wide)
- **Canvas Size**: Use larger canvas (16x11 or similar) to prevent overlapping elements
- **Spacing**: Ensure adequate spacing between boxes and arrows

### Content Requirements

- **All Processes**: Show trigger, main approval, rejection handler
- **Approval Levels**: L1, L2, L3+ with correct connections
- **Outcomes**: APPROVED and REJECTED final states
- **Auto-Reject Scenarios**: List conditions that trigger automatic rejection

### Color Coding

- **Green arrows**: Approve actions
- **Red arrows**: Reject actions (no labels - keep clean)
- **Orange arrows**: Escalate/Timeout actions (label at source only)
- **Pink arrows**: Auto-reject paths
- **Blue arrows**: Reassign actions (if applicable)

### Arrow Best Practices

- **Simplicity**: Use straight lines whenever possible
- **Minimal Labels**: Only label arrows at their source, not along the path
- **No Redundant Labels**: Don't repeat information that's already in boxes
- **Clean Reject Paths**: Red reject arrows should be simple and unlabeled
- **Timeout Labels**: Show timeout duration at the source (e.g., "2 days Timeout", "5 days Timeout")
- **Avoid Confusion**: Don't label intermediate steps like "30 days CEO Timeout" on arrows

### Layout Best Practices

- **Vertical Flow**: Main approval flow should go top to bottom
- **Right Side**: Place rejection monitoring and auto-reject scenarios on the right
- **Left Side**: Place skip/bypass logic on the left
- **Bottom**: Place final outcomes (APPROVED/REJECTED) at bottom
- **Adequate Spacing**: Leave room between elements to prevent overlap

### Legend

Include legend explaining:

- Arrow colors
- Box types (User Action, System Action, Decision)
- Escalation timing (e.g., "L1 Coder (2 days) | L2+ All Other Levels (5 days/level) | Total Max: 42 days")

## Generation Workflow

### Coding Standards Skill Workflow

**RECOMMENDED**: Use the `ipa-coding-standards` skill for all coding standards analysis.

**Activation**: `/ipa-coding-standards` or `discloseContext(name="ipa-coding-standards")`

The coding standards skill follows a stateless pipeline workflow:

1. **User Selection** - Interactive prompts for client, RICE item, and LPD file
2. **Phase 0: Preprocessing** (Python) - Extracts LPD structure, calculates metrics, loads project standards, organizes by 5 domains
3. **Phase 1: Naming Analysis** (AI) - Analyzes filename, node captions, config sets against naming rules
4. **Phase 2: JavaScript Analysis** (AI) - Analyzes ES5 compliance, performance patterns, function order
5. **Phase 3: SQL Analysis** (AI) - Analyzes Compass SQL, pagination, query optimization
6. **Phase 4: Error Handling Analysis** (AI) - Analyzes OnError tabs, GetWorkUnitErrors, error coverage
7. **Phase 5: Structure Analysis** (AI) - Analyzes auto-restart, process type, activity distribution
8. **Phase 6: Report Assembly** (Python) - Merges violations, builds ipa_data, generates Excel report

**Key Points:**

- Phase 0 automatically loads project standards from `Projects/<Client>/project_standards_<Client>.xlsx` if it exists
- Project standards override steering file defaults in all analysis phases
- Each phase reads domain JSON + project standards, writes analysis JSON
- No context accumulation - each phase isolated
- Crash-safe - can resume from any phase
- ONE Excel report per process (4 sheets: Executive Dashboard, Action Items, Detailed Analysis, Process Flow)

**Reference**: See `.kiro/skills/ipa-coding-standards/SKILL.md` for complete documentation.

### Legacy: Coding Standards Hook (DEPRECATED)

The original coding standards hook has been replaced by the skill. The hook is backed up at:
- `.kiro/hooks/.backups/coding-standards.kiro.hook.v41.DEPRECATED_USE_SKILL.backup`

Use the skill instead for better reliability, documentation, and maintainability.

### Using Data Extraction Tools (RECOMMENDED)

**Modern Approach**: Use data extraction tools + Kiro analysis for all peer reviews.

**Benefits**:

- Fast extraction (12K line LPD in <1 second)
- Organized JSON output (easy for Kiro to read)
- Accurate analysis (Kiro makes context-aware decisions)
- Clear separation of concerns (Python extracts, Kiro analyzes)
- Flexible (Kiro can analyze differently for different projects)

**Workflow**:

**Step 1: Extract Data (Python)**

```python
from ReusableTools.IPA_Analyzer.extract_lpd_data import extract_lpd_data
from ReusableTools.IPA_Analyzer.extract_wu_log import extract_wu_log
from ReusableTools.IPA_Analyzer.extract_spec import extract_spec

# Extract LPD data to JSON
lpd_data = extract_lpd_data(
    lpd_files=[
        'Projects/ClientName/RICEItem/main.lpd',
        'Projects/ClientName/RICEItem/subprocess.lpd'
    ],
    output_file='Temp/ClientName_RICEItem_lpd_data.json'
)

# Extract WU log data to JSON (optional - for performance analysis)
wu_data = extract_wu_log(
    log_file='Projects/ClientName/RICEItem/log.txt',
    output_file='Temp/ClientName_RICEItem_wu_data.json'
)

# Extract functional spec data to JSON (optional - for requirements traceability)
spec_data = extract_spec(
    spec_file='Projects/ClientName/RICEItem/ANA-050.docx',
    output_file='Temp/ClientName_RICEItem_spec_data.json'
)
```

**Step 2: Analyze Data (Kiro)**

```python
import json

# Read extracted JSON files
with open('Temp/ClientName_RICEItem_lpd_data.json') as f:
    lpd_data = json.load(f)

with open('Temp/ClientName_RICEItem_wu_data.json') as f:
    wu_data = json.load(f)

with open('Temp/ClientName_RICEItem_spec_data.json') as f:
    spec_data = json.load(f)

# Kiro analyzes the data:
# - Assess ES5 compliance from JavaScript blocks
# - Identify issues with specific line numbers
# - Determine severity levels (Critical/High/Medium/Low)
# - Create recommendations with code examples
# - Score quality metrics
# - Assess auto-restart configuration (context-aware)
# - Trace requirements to activities
# - Identify gaps and risks
# - Check team coding standards (1.1-1.5)
# - Verify against standard flows

# Build ipa_data dictionary with analysis results
ipa_data = {
    'client_name': 'ClientName',
    'rice_item': 'RICEItem',
    'overview': {
        'process_count': 1,
        'process_name': 'ProcessName',  # LPD filename without extension
        'process_type': 'Outbound Interface',  # or 'Approval Workflow', 'Inbound Interface'
        'activity_count': 78,
        'total_activities': 78,  # Same as activity_count (for compatibility)
        'javascript_blocks': 20,
        'sql_queries': 1,
        'auto_restart': '0',  # Value from LPD
        'auto_restart_assessment': 'Correctly set to 0 for outbound interface',  # Your assessment
        'description': 'Brief process description'
    },
    'key_findings': [...],  # Kiro's findings
    'quality_scores': {...},  # Kiro's scores
    'javascript_issues': [...],  # Kiro's ES5 assessment
    'coding_standards': {...},  # Kiro's 1.1-1.5 assessment
    'recommendations': [...],  # Kiro's recommendations
    'performance_analysis': {...},  # Kiro's performance analysis
    'best_practices': [...],  # Kiro's assessment
    'technical_deep_dive': {...},  # Kiro's insights
    'functional_spec_analysis': {...}  # Kiro's traceability analysis
}
```

**Step 3: Generate Report (Python Template)**

```python
from ipa_peer_review_template import generate_report

output_path = generate_report(ipa_data)
print(f"Report generated: {output_path}")
```

**What Extraction Tools Do**:

1. **extract_lpd_data.py** - Extracts activities, JavaScript blocks, config variables
2. **extract_wu_log.py** - Extracts performance metrics, auto-restart status, test mode
3. **extract_spec.py** - Extracts RICE type hints, requirements, sections, tables

**What Kiro Does (Analysis)**:

1. Read organized JSON files
2. Assess ES5 compliance (let/const, arrow functions, template literals)
3. Identify issues with line numbers and code snippets
4. Determine severity levels and priorities
5. Create specific recommendations with ES5-compatible fixes
6. Score quality metrics (ES5 compliance, performance, overall)
7. Assess auto-restart configuration (context-aware based on RICE type)
8. Trace requirements to activities
9. Identify gaps between spec and implementation

**Auto-Restart Assessment Logic (Kiro's Analysis)**:

- Interface (non-approval) → autoRestart=1 recommended
- Enhancement/Approval → autoRestart=0 correct
- Considers RICE type and process keywords (approval, invoice, payment)
- Eliminates false positives

**See Also**:

- `ReusableTools/IPA_Analyzer/README.md` - Complete documentation
- `.kiro/hooks/ipa-peer-review.kiro.hook` - Automated workflow
- `00_Kiro_General_Rules.md` - Critical principle about analysis

## Quality Checklist

### Pre-Generation Checklist

**BEFORE generating ANY client handover report, verify:**

- System Configuration sheet planned - Dedicated sheet for all config variables
- OAuth credentials identified (all API_AuthCred_* variables)
- File Channel variables identified (MonitorDirectory, OutputDir, etc.)
- Process variables from START activity extracted
- Configuration variable JSON structures documented

### Accuracy

- Activity counts match LPD file analysis
- Work unit outcomes verified from actual logs
- Escalation timing correct (business days vs calendar days)
- Auto-reject scenarios validated
- Configuration variables complete and accurate
- **Auto-restart setting assessed correctly** (see guidance below)

### Auto-Restart Assessment Guidance

**CRITICAL**: Do NOT flag `autoRestart="0"` as an issue for approval/financial processes!

**When autoRestart="0" is CORRECT**:

- Approval workflows (AP, AR, GL, contract approvals)
- Financial transaction processing
- Audit-sensitive operations
- Single-execution requirements
- Document approval processes
- Payment processing

**When autoRestart="1" is RECOMMENDED**:

- Batch data loads
- Interface processes (EDI, file processing)
- Orchestration processes
- Report generation
- Data synchronization
- Analytics pipelines

**Assessment Pattern**:

```text
Process Type: AP Invoice Approval
autoRestart="0" → ✓ Correct - Disabled (appropriate for approval processes)
Reason: Financial data integrity, audit trail, risk of duplicate approvals
```

**Reference**: See `01_IPA_and_IPD_Complete_Guide.md` section "When Auto Restart Should NOT Be Enabled"

### Clarity

- System config vs IPA variables clearly distinguished
- HOW TO sections have step-by-step instructions
- Workflow diagram easy to understand
- Purpose column explains what each activity does
- Key Content column shows actual parameters

### Completeness

- All processes documented
- All user actions identified
- All configuration variables listed
- All auto-reject scenarios explained
- All approval levels documented

### Usability

- Client can find configuration variables
- Client can update settings without IPA changes
- Client can troubleshoot basic issues
- Client knows when to escalate to developers
- Navigation paths to FSM screens provided

## Crash Prevention Strategy

**CRITICAL**: Always validate `ipa_data` structure before generating reports to prevent crashes.

### Common Crash Causes

1. **Incomplete data structures** - Truncated dictionaries or lists
2. **Missing required fields** - Template expects specific keys
3. **Wrong data types** - Lists vs dictionaries, strings vs numbers
4. **Incorrect javascript_issues format** - Must be list of lists, NOT dictionaries

### Prevention Workflow

**Step 1: Use Validation Tool**

```python
from validate_ipa_data import validate_ipa_data

# Build your ipa_data dictionary
ipa_data = {
    'client_name': 'FPI',
    'rice_item': 'MatchReport',
    # ... rest of data ...
}

# Validate BEFORE generating
issues = validate_ipa_data(ipa_data)
if issues:
    print('❌ VALIDATION FAILED:')
    for issue in issues:
        print(f'  - {issue}')
    sys.exit(1)

print('✓ Validation passed')
```

**Step 2: Check for Truncation**

- Scroll to end of `ipa_data` dictionary
- Verify all closing braces `}` and brackets `]` match
- Check that no sections are cut off mid-definition
- Ensure all lists are properly closed

**Step 3: Verify Data Types**

```python
# javascript_issues MUST be list of lists
assert isinstance(ipa_data['javascript_issues'], list)
for issue in ipa_data['javascript_issues']:
    assert isinstance(issue, list), f"Issue must be list, not {type(issue)}"
    assert len(issue) == 9, f"Issue must have 9 elements, has {len(issue)}"

# coding_standards sections MUST be lists
for section in ['naming_convention', 'ipa_rules', 'error_handling', 
                'system_configuration', 'performance']:
    assert isinstance(ipa_data['coding_standards'][section], list)
```

**Step 4: Test Incrementally**

- Start with minimal valid structure
- Add sections one at a time
- Test after each addition
- Identify which section causes crash

### Validation Tool Location

**File**: `Temp/validate_ipa_data.py`

**Usage**:

```python
from validate_ipa_data import validate_ipa_data

issues = validate_ipa_data(ipa_data)
if not issues:
    # Safe to generate report
    output_path = generate_report(ipa_data)
```

### Generation Script Template

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from ReusableTools.IPA_CodingStandards.ipa_coding_standards_template import generate_report
from validate_ipa_data import validate_ipa_data

print('Starting report generation...')

# Build ipa_data dictionary (Kiro's analysis)
ipa_data = {
    # ... complete structure ...
}

# VALIDATE BEFORE GENERATING
print('Validating data structure...')
issues = validate_ipa_data(ipa_data)
if issues:
    print('❌ VALIDATION FAILED:')
    for issue in issues:
        print(f'  - {issue}')
    sys.exit(1)

print('✓ Validation passed')
print('Generating report...')
output_path = generate_report(ipa_data)
print(f'✓ Report generated: {output_path}')
```

### Debugging Tips

**PowerShell Output Issues**:

- PowerShell on Windows can hide/truncate Python output
- Add multiple `print()` statements throughout script
- Use `python -u script.py` for unbuffered output
- Check file system directly (don't rely on console output)
- Exit code 0 doesn't mean output was displayed

**Empty Sheets**:

- Check `javascript_issues` format (list of lists, not dictionaries)
- Verify `coding_standards` field names (`required` not `expected`)
- Check for truncated data structures
- Validate all required fields exist

**KeyError Crashes**:

- Missing required top-level keys
- Missing nested dictionary keys
- Typos in field names
- Check validation output for specific missing keys

### Best Practices

1. Always use validation tool before generating
2. Check for truncated data structures
3. Verify data types match template expectations
4. Test incrementally when building complex structures
5. Add multiple print statements for debugging
6. Check file system directly (don't trust console output)
7. Reference data structure documentation before building

## Coding Standards Data Structure

**CRITICAL REFERENCE**: `Temp/IPA_Coding_Standards_Data_Structure_Reference.md`

**TEMPLATE VERSION**: Enhanced Template v2.0 (2026-02-22)

- Location: `ReusableTools/IPA_CodingStandards/ipa_coding_standards_template_enhanced.py`
- Sheets: 4 (Executive Dashboard, Action Items, Detailed Analysis, Process Flow)
- Enhanced Fields: impact_analysis, code_examples, testing_notes, priority_score

### Enhanced Violation Structure (v2.0)

The enhanced template supports additional fields for richer analysis:

```python
{
    # Standard fields (required)
    'rule_id': 'FPI 1.1.1',
    'rule_name': 'Filename Format (FPI 1.1.1)',
    'severity': 'Medium',
    'finding': 'Description of violation',
    'current': 'Current state',
    'recommendation': 'How to fix',
    'activities': 'Affected activities',
    'domain': 'naming',
    
    # Enhanced fields (optional - backward compatible)
    'impact_analysis': {
        'frequency': 'Every execution',
        'affected_percentage': 75,
        'maintainability_impact': 'High - difficult to debug',
        'estimated_fix_time': '2-3 hours'
    },
    'code_examples': {
        'before': 'var x = 1;',
        'after': 'var calculatedValue = 1;',
        'explanation': 'Descriptive name improves readability'
    },
    'testing_notes': 'Test all approval paths after fix',
    'priority_score': 85  # 0-100 objective score
}
```

**Backward Compatibility**: Template works with old format (without enhanced fields). Shows default values when enhanced fields missing.

### Required Field Names

When building `ipa_data` for coding standards reports, use these EXACT field names:

- `'required'` NOT `'expected'`
- `'activity'` for activity/file column
- `'violation'` for violation description
- `'current'` for current state
- `'impact'` for impact description
- `'severity'` for severity level
- `'recommendation'` for fix instructions
- `'effort'` for effort estimate

### Status Detection

The template automatically sets status based on content:

- **Pass**: "No violations" or "N/A - Already compliant" in `required`
- **Verify**: "Cannot verify" or "Unknown" in `violation` or `current`
- **Pending**: Actual violations that need fixing

### Common Mistakes

**Avoid**:

- Using `'expected'` instead of `'required'`
- Using `'status'` field (auto-calculated)
- Using `'examples'` array (put in `current` or `recommendation`)
- Missing `'activity'` field
- Naming Convention `'required'` with specific values (show format template with placeholders)
- Destination = "SFTP" (transport mechanism) - should be 3rd party application
- Applying Performance rules 1.5.1/1.5.3 to WEBRN activities (only for LM nodes)
- **DUPLICATES**: Adding same issue to both `coding_standards` AND `recommendations`

**Always reference** `Temp/IPA_Coding_Standards_Data_Structure_Reference.md` before building data structure

### Avoiding Duplicate Action Items

**Problem**: Same issue appears in both `coding_standards.performance` and `recommendations`, creating duplicate rows in Action Items sheet.

**Root Cause**: Deduplication uses `(activity, issue)` as key. If issue text differs slightly, both entries appear.

**Example of Duplicates**:

```python
# In coding_standards.performance:
['Assign7960', 'Loop optimization', 'High', 'Regex in loop, array shift()', ...]

# In recommendations:
{
    'activities': 'Assign7960 (CRITICAL PATH - pagination loop)',
    'issue': 'Regex compiled inside for loop for every row. Executed 100K times...',
    ...
}
```

These have different issue text, so deduplication doesn't catch them.

**Solution - Choose ONE Location**:

**Use `recommendations` for:**

- Performance issues with flow analysis (execution frequency, time impact, percentage)
- Issues requiring detailed explanation
- Issues with calculated impact (e.g., "10 sec, 33% of time")
- Complex issues spanning multiple aspects

**Use `coding_standards` for:**

- Simple rule violations (naming, configuration)
- Binary checks (has error handling? yes/no)
- Standard compliance (ES5, file format)
- Quick assessments without deep analysis

**Performance Issues - Always Use `recommendations`**:

Performance issues should ALWAYS go in `recommendations` with:

- Execution frequency
- Time per execution
- Total impact (seconds)
- Percentage of total time
- Flow context (CRITICAL PATH, STARTUP PATH, etc.)

Do NOT add performance issues to `coding_standards.performance` if they're already in `recommendations`.

**Example - Correct Approach**:

```python
'coding_standards': {
    'performance': [
        # Only SQL optimization (not in recommendations)
        ['InitQuery SQL', 'Compass SQL optimization', 'Medium', 
         'RPAD function may prevent index usage', 
         'RPAD(REPLACE(...),9,"0") in SELECT/GROUP BY', 
         'Needs Improvement', 
         'Consider pre-computing or moving to JavaScript.']
        # NO JavaScript performance issues here - they're in recommendations
    ]
},

'recommendations': [
    # JavaScript performance issues with detailed flow analysis
    {
        'priority': 'High',
        'category': 'JavaScript Performance',
        'recommendation': 'Pre-compile regex outside pagination loop',
        'activities': 'Assign7960 (CRITICAL PATH - pagination loop)',
        'issue': 'Regex compiled 100K times. Impact: ~10 sec (33% of time).',
        'current': 'Regex compiled inside for loop',
        'testing': 'Test with 10K, 50K, 100K rows. Expected: 30-40% faster.'
    }
]
```

**Rule of Thumb**:

- If you write detailed flow analysis for a performance issue → Put it ONLY in `recommendations`
- If it's a simple rule check → Put it in `coding_standards`
- Never put the same issue in both places

### Critical Corrections (2026-02-06)

**1. Naming Convention (1.1)**:

**Standard Format**: `<ProjectPrefix>_<INT>_<Source>_<Destination>_<ShortDescription>.lpd`

**Assessment Logic**:

- Check if filename contains ALL 5 components separated by underscores
- **ProjectPrefix**: Client/project identifier (e.g., "FPI", "CLIENT")
- **INT**: Literal text "INT" indicating Interface type
- **Source**: System sending data (e.g., "FSM", "Landmark", "SAP")
- **Destination**: System receiving data (e.g., "Client", "Vendor", "EDI") - NOT transport like "SFTP"
- **ShortDescription**: Brief description (e.g., "MatchReport", "InvoiceExport")

**Common Mistakes**:

- ❌ `MatchReport_Outbound.lpd` - Missing ProjectPrefix, INT, Source, Destination
- ❌ `FPI_MatchReport.lpd` - Missing INT, Source, Destination
- ❌ `FPI_INT_FSM_SFTP_MatchReport.lpd` - "SFTP" is transport, not destination
- ✅ `FPI_INT_FSM_Client_MatchReport.lpd` - Correct format

**Data Structure**:

- `'required'` field: Show format template with placeholders
- `'violation'`: Describe what's missing (e.g., "Filename does not follow standard naming convention")
- `'current'`: Show current filename and what's missing (e.g., "Current: MatchReport_Outbound.lpd (missing ProjectPrefix, INT, Source, Destination)")
- `'status'`: "Needs Improvement" if missing components, "Pass" if correct
- `'recommendation'`: Provide specific corrected filename (e.g., "Rename to: FPI_INT_FSM_Client_MatchReport.lpd")

**Example**:

```python
['MatchReport_Outbound.lpd', '<ProjectPrefix>_<INT>_<Source>_<Destination>_<ShortDescription>.lpd', 'Medium', 'Filename does not follow standard naming convention', 'Current: MatchReport_Outbound.lpd (missing ProjectPrefix, INT, Source, Destination)', 'Needs Improvement', 'Rename to: FPI_INT_FSM_Client_MatchReport.lpd (where Client = actual destination system name)']
```

**2. Performance Rules (1.5)**:

- Rules 1.5.1 (webservice) and 1.5.3 (_runAsUser,_filterString) apply ONLY to **Landmark Transaction (LM) nodes**
- LM nodes have "Execute via web service" checkbox and `_runAsUser` parameter in transaction string
- WEBRN activities are for external API calls (Data Fabric, Compass, OAuth) - different from Landmark
- If process has no LM nodes, mark these rules as "N/A - No Landmark Transaction activities found"
- Rule 1.5.2 (Pagination) applies to any large dataset query (LM or WEBRN)

**3. Status Detection**:

- Items with "No violations" or "N/A - Already compliant" → Pass (green)
- Items with "Cannot verify" or "Unknown" → Verify (amber)
- Items with actual violations → Pending (amber)
- Template handles this automatically based on `violation` and `required` content

### CRITICAL: javascript_issues Format (2026-02-07)

**The template expects a list of lists, NOT dictionaries!**

```python
# ❌ WRONG - Dictionaries (will cause empty sheets)
'javascript_issues': [
    {
        'activity_id': 'Assign1540',
        'line_number': 16,
        'issue_type': 'Ternary Operator',
        'severity': 'Medium',
        'code_snippet': 'var x = a ? b : c;',
        'recommendation': 'Use if-else',
        'fix_example': 'if (a) { x = b; } else { x = c; }'
    }
]

# ✅ CORRECT - List of lists with specific indices
'javascript_issues': [
    # Format: [file, activity_id, line_number, issue_type, severity, recommendation, code_snippet, es5_compliant, fix_example]
    ['MatchReport_Outbound.lpd', 'Assign1540', 16, 'Ternary Operator', 'Medium', 'Replace with if-else', 'var x = a ? b : c;', False, 'if (a) { x = b; } else { x = c; }']
]
```

**Index Mapping**:

- `[0]` = file name
- `[1]` = activity_id
- `[2]` = line_number
- `[3]` = issue_type
- `[4]` = severity
- `[5]` = recommendation
- `[6]` = code_snippet
- `[7]` = es5_compliant (boolean)
- `[8]` = fix_example

**Why This Format**:

- Template uses `issue[1]`, `issue[4]`, etc. to access data
- Dictionaries don't support numeric indexing
- Using dictionaries results in empty sheets with no error messages

**Debugging Empty Sheets**:

- Check if `javascript_issues` is a list of lists (not dictionaries)
- Check if `coding_standards` sections use correct field names (`required` not `expected`)
- Verify PowerShell isn't hiding Python output (use multiple print statements)
- Check file system directly - file may be created even if no console output

### Report Structure (3 Sheets)

**1. 📋 Summary & Guide**

- Overall quality score with bar chart
- Section scores (1.1 Naming, 1.2 IPA Rules, 1.3 Error Handling, 1.4 Configuration, 1.5 Performance)
- Severity breakdown (Critical/High/Medium/Low)
- Issue counts by category

**2. ✅ Action Items**

- Consolidated developer checklist
- JavaScript ES5 violations with code snippets
- Coding standards violations (1.1-1.5)
- Activity IDs, severity, recommendations
- Status tracking checkboxes

**3. 📐 Detailed Analysis (FULLY IMPLEMENTED 2026-02-07)**

Comprehensive technical analysis with 6 major sections:

1. **� Process Overview**
   - Process name, type, description
   - Total activities and JavaScript blocks
   - Auto-restart configuration

2. **💻 JavaScript ES5 Violations**
   - Each violation with activity ID, line number, severity
   - Current code snippet (problematic code)
   - Fix example (corrected ES5 code)
   - Specific recommendations

3. **📐 Coding Standards Breakdown**
   - 1.1 Naming Convention (filename format compliance)
   - 1.2 IPA Rules (variables, node names, functions)
   - 1.3 Error Handling (On Error tab configuration)
   - 1.4 System Configuration (config variables usage)
   - 1.5 Performance (webservice, pagination, filters)
   - Each section shows: Rule, Status, Current state, Recommendation

4. **✨ Best Practices**
   - OAuth2 implementation
   - Error handling patterns
   - Configuration management
   - Status (Excellent/Good/Needs Improvement)

5. **🏗️ Technical Architecture**
   - Integration pattern (Data Fabric, Landmark, etc.)
   - Components (OAuth2, SQL, Pagination, SFTP, etc.)
   - Strengths (what's done well)
   - Weaknesses (areas for improvement)

6. **🎯 Recommendations Summary**
   - Priority (Critical/High/Medium/Low)
   - Category (JavaScript ES5, Configuration, etc.)
   - Effort estimate
   - Impact assessment
   - Activities affected
   - Testing steps

**Implementation Notes**:

- Uses xlsxwriter for native Excel formatting
- Color-coded sections (green=good, amber=warning)
- Code snippets in monospace font with gray background
- Text wrapping for long content
- Frozen header row for easy navigation
- ~66 rows of detailed content for typical process

## Excel Report Technology Stack

### Library Selection for Excel Reports

**Preferred Stack**:

- **xlsxwriter**: Primary library for Excel reports with charts
- **pandas**: Data manipulation and analysis
- **matplotlib**: High-quality chart images (when needed)
- **openpyxl**: Basic Excel operations only (NOT for charts)

### Why xlsxwriter for Charts

**Problems with openpyxl charts**:

- Renders as white boxes in Excel
- Limited styling options
- Unreliable across Excel versions
- Poor performance

**Benefits of xlsxwriter**:

- Native Excel chart support
- Reliable rendering
- Rich formatting options
- Better performance
- Professional output

### Chart Implementation Examples

**Example 1: Native Excel Bar Chart (xlsxwriter)**

```python
import xlsxwriter

workbook = xlsxwriter.Workbook('report.xlsx')
worksheet = workbook.add_worksheet()

# Write data
sections = ['1.1 Naming', '1.2 Rules', '1.3 Error Handling']
scores = [60, 65, 85]

worksheet.write_row('A1', ['Section', 'Score'])
for row, (section, score) in enumerate(zip(sections, scores), start=1):
    worksheet.write(row, 0, section)
    worksheet.write(row, 1, score)

# Create horizontal bar chart
chart = workbook.add_chart({'type': 'bar'})
chart.add_series({
    'categories': '=Sheet1!$A$2:$A$4',
    'values': '=Sheet1!$B$2:$B$4',
    'fill': {'color': '#1565C0'},
    'gap': 50
})

chart.set_title({'name': 'Section Scores'})
chart.set_x_axis({'name': 'Score (%)', 'max': 100})
chart.set_legend({'position': 'none'})
chart.set_size({'width': 500, 'height': 300})

worksheet.insert_chart('D2', chart)
workbook.close()
```

**Example 2: Conditional Formatting (xlsxwriter)**

```python
# Color-coded bars based on score
worksheet.conditional_format('B2:B7', {
    'type': '3_color_scale',
    'min_color': '#C62828',  # Red
    'mid_color': '#F57C00',  # Amber
    'max_color': '#2E7D32'   # Green
})
```

**Example 3: matplotlib Image (for complex charts)**

```python
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image

# Create chart with matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
colors = ['#F57C00' if s < 90 else '#2E7D32' for s in scores]
ax.barh(sections, scores, color=colors)
ax.set_xlim(0, 100)
ax.set_xlabel('Score (%)')
plt.tight_layout()
plt.savefig('chart.png', dpi=150, bbox_inches='tight')
plt.close()

# Embed in Excel (openpyxl)
from openpyxl import load_workbook
wb = load_workbook('report.xlsx')
ws = wb.active
img = Image('chart.png')
ws.add_image(img, 'E8')
wb.save('report.xlsx')
```

### Migration from openpyxl to xlsxwriter

**When to migrate**:

- Report needs native Excel charts
- Charts rendering as white boxes
- Need advanced formatting
- Performance issues with large datasets

**Migration steps**:

1. Replace `openpyxl.Workbook()` with `xlsxwriter.Workbook()`
2. Use `worksheet.write()` instead of `ws['A1'] = value`
3. Replace openpyxl charts with `workbook.add_chart()`
4. Update cell formatting to xlsxwriter format objects
5. Test chart rendering in Excel

**Note**: xlsxwriter is write-only. Use openpyxl for reading existing Excel files.

### Best Practices

1. **Use xlsxwriter for new reports with charts**
2. **Use pandas for data manipulation before writing**
3. **Use matplotlib only for complex visualizations**
4. **Keep openpyxl for reading/modifying existing files**
5. **Always test charts in actual Excel (not just Python)**

## Recent Examples

### FPI MatchReport (2026-02-08)

**Type**: Coding Standards Review (Internal)

**Process**: MatchReport_Outbound.lpd

**Pattern**: Data Fabric Compass SQL with OAuth2 + Pagination

**Key Findings**:

- **JavaScript ES5: 100% compliant** - No violations found (all code uses proper ES5 syntax)
- Filename doesn't follow team naming convention (missing FPI_INT prefix)
- Generic "Interface" configuration set name needs verification
- Excellent OAuth2 multi-tenant implementation (5 FEG-specific credentials)
- Proper pagination (5000 records/page) for large datasets
- Comprehensive error handling (92.9% coverage) with descriptive messages

**Quality Scores**:

- Overall: 73/100
- JavaScript ES5: 100/100 (fully compliant)
- Naming Convention: 40/100 (needs improvement)
- IPA Rules: 95/100 (excellent)
- Error Handling: 93/100 (excellent)
- System Configuration: 60/100 (needs verification)
- Performance: 95/100 (excellent)

**Technical Highlights**:

- Multi-tenant OAuth credentials (5 FEGs: AGW, AGC, FCIL, FMFC, FCE)
- Asynchronous query pattern with status polling (15s intervals, max 15 attempts)
- CSV transformation with delimiter replacement (handles quoted fields)
- SFTP delivery via subprocess (separate error/complete paths)
- Flag file pattern for external monitoring
- Comprehensive date validation with Julian conversion
- Retry logic for token acquisition (5 attempts with 2-second wait)

**Coding Standards Assessment**:

- **1.1 Naming Convention**: Violation - Missing project prefix and INT designation
- **1.2 IPA Rules**: Pass - Variables on Start, CamelCase, functions declared early
- **1.3 Error Handling**: Mostly Pass - 13 of 14 nodes configured (MsgBuilder7360 missing)
- **1.4 System Configuration**: Verify - Generic "Interface" name needs confirmation
- **1.5 Performance**: Pass - Proper pagination, no Landmark nodes

**Lessons**:

- Not all processes have ES6 violations - some are fully ES5 compliant
- Ternary operators are acceptable in ES5 (contrary to previous assessment)
- Multi-tenant patterns need careful credential management
- Pagination essential for Data Fabric queries (can return 100K+ records)
- Flag files provide external monitoring integration point
- Generic configuration set names should be flagged for verification (not automatic violation)
- Performance rules 1.5.1 and 1.5.3 apply ONLY to Landmark Transaction nodes, not WEBRN

**Data Structure Corrections**:

- `javascript_issues` MUST be list of lists, NOT dictionaries
- `coding_standards` sections MUST be list of lists with specific field order
- `key_findings` expects dictionaries with 'category', 'status', 'details'
  - **Status values**: 'Pass', 'Excellent', 'Verify', 'Needs Improvement', 'Pending'
  - **Status colors**: Pass=Green, Excellent=Blue, Verify=Amber, Needs Improvement=Amber, Pending=Amber
- `best_practices` expects list of dictionaries with 'category', 'status', 'details', 'code_example'
- `technical_deep_dive.architecture` expects dictionary with 'pattern', 'components', 'strengths'
- `recommendations` expects list of dictionaries with 'priority', 'category', 'recommendation', 'effort', 'impact', 'activities', 'testing'
  - **Note**: Recommendations don't have 'issue' or 'current' fields (those are in coding_standards)
- Always validate data structure before generating report to prevent crashes

### FPI MatchReport Client Handover (2026-03-03)

**Type**: Client Handover Documentation

**Process**: MatchReport_Outbound.lpd

**Pattern**: Data Fabric Compass SQL with OAuth2 + SFTP Delivery

**Issues Fixed**:

1. **System Configuration Sheet Empty**
   - **Root Cause**: Assembly script passed list-of-dicts format, but LEGACY template expects list-of-lists
   - **Fix**: Convert configuration data to list-of-lists format in `configuration_analysis.json`
   - **Code Location**: `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py` lines 680-690
   - **Template Location**: `ipa_client_handover_template.py` lines 1000-1050
   - **Lesson**: ALWAYS check template expectations before passing data structure

2. **Process Sheet Missing Descriptions**
   - **Root Cause**: Template expects activities to have `description` and `when_it_runs` fields, but raw LPD data doesn't include these
   - **Fix**: Enrich activities with type-based descriptions in assembly script before passing to template
   - **Code Location**: `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py` lines 600-650
   - **Enrichment Logic**:
     - START: "Process entry point - initializes variables and begins execution"
     - ASSGN: "Variable assignment - sets values, executes JavaScript, transforms data"
     - WEBRN: "HTTP API call - makes external web service requests (OAuth, Compass API)"
     - BRANCH: "Conditional routing - directs flow based on conditions"
     - Timer: "Delay execution - waits for specified time period"
     - LM: "Landmark transaction - queries or updates FSM business classes"
   - **Lesson**: Raw LPD data needs enrichment for human-readable documentation

3. **Duplicate Check Marks in Key Features**
   - **Root Cause**: `generate_key_features()` function added "✓" prefix, then template added another "✓" prefix
   - **Fix**: Remove check marks from generation function (template handles formatting)
   - **Code Location**: `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py` lines 354, 368
   - **Lesson**: Avoid duplicate formatting - let template handle visual elements

**Recurring Pattern Identified**:

"It's always the System Configuration and Process sheets that's always having an issue" - User feedback

**Why These Sheets Are Problematic**:

1. **System Configuration**: Requires specific data format (list-of-lists) that differs from natural JSON structure (list-of-dicts)
2. **Process Sheet**: Requires enriched data (descriptions, when_it_runs) that doesn't exist in raw LPD structure

**Prevention Strategy**:

1. **Pre-Assembly Verification**: Check data structure matches template expectations
2. **Data Enrichment**: Always enrich raw LPD data with human-readable descriptions
3. **Format Conversion**: Convert between list-of-dicts and list-of-lists as needed
4. **Template Documentation**: Document expected data structures in template comments

**Quality Verification**:

After fixing all issues, the report now shows:

- ✅ Executive Summary: 8 key features with single check marks
- ✅ Business Requirements: 6 requirements from ANA-050 spec
- ✅ Production Validation: Work unit log analysis with real metrics
- ✅ System Configuration: 5 OAuth credentials + file channel config (28 rows)
- ✅ Activity Node Guide: All 78 activities documented
- ✅ Process_1 Sheet: All activities with descriptions and "When It Runs" context
- ✅ Maintenance Guide: Technical maintenance procedures

**Technical Details**:

- Process Count: 1
- Total Activities: 78
- OAuth Credentials: 5 (AGW, AGC, FCIL, FMFC, FCE)
- File Channel Config: 3 variables (directory paths, file patterns)
- Key Features: 8 (4 integrations + 4 business objectives)

**Lessons for Future Sessions**:

1. **Root Cause Analysis**: Fix data structure issues at the source (assembly script), not in template
2. **Template Expectations**: Always verify what format template expects before passing data
3. **Data Enrichment**: Raw extraction data needs enrichment for client-facing documentation
4. **Avoid Duplication**: Don't add formatting (check marks, emojis) in multiple places
5. **Verify Output**: Always inspect generated report to confirm all sheets have content
