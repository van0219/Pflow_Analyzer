---
name: "ipa-coding-standards"
description: "Automated IPA code quality analysis with domain-segmented review. Analyzes naming conventions, JavaScript ES5 compliance, SQL queries, error handling, and process structure. Generates comprehensive Excel reports with executive dashboards, action items, and process flow diagrams. Use when performing internal code quality reviews or peer reviews of IPA processes."
---

# IPA Coding Standards Analysis Skill

Automated code quality analysis for Infor Process Automation (IPA) processes using domain-segmented incremental analysis.

## What This Skill Does

Analyzes IPA processes against coding standards and generates comprehensive Excel reports with:

- Executive dashboard with quality metrics and KPI cards
- Action items with priority scoring and fix time estimates
- Detailed analysis with code examples and testing notes
- Process flow diagram with complexity breakdown

## When to Use This Skill

Use this skill when you need to:

- Perform internal code quality reviews of IPA processes
- Conduct peer reviews before production deployment
- Analyze coding standards compliance
- Generate technical documentation for development teams
- Identify violations and improvement opportunities

## Key Features

- Interactive selection with client/RICE/LPD options
- Batch processing for multiple LPDs in one RICE item
- Domain-segmented analysis across 5 domains
- Project standards integration with client-specific rules
- Incremental processing to prevent context overload
- Crash-safe and resumable from any phase
- Scalable for any process size

## Analysis Domains

1. **Naming** - Filename format, node captions, config set naming, hardcoded values
2. **JavaScript** - ES5 compliance, performance patterns, function order, variable scoping
3. **SQL** - Compass SQL compliance, pagination, SELECT *, query optimization
4. **Error Handling** - OnError tabs, GetWorkUnitErrors, error coverage
5. **Structure** - Auto-restart configuration, process type, activity distribution

## Report Structure

### Executive Dashboard

- KPI cards: Overall Quality, Processes, Complexity, Action Items
- Radar chart: Quality metrics visualization
- Key findings: Top 5 findings with status badges

### Action Items (Enhanced)

14 columns including:

- Priority, Category, Rule ID, Activity, Issue
- Current state, Recommendation, Effort, Impact
- Priority Score (0-100), Est. Fix Time, Affected %
- Code Example (before/after), Testing Notes
- Status (dropdown: Not Started, In Progress, Complete, Blocked)

**Conditional Formatting:**

- "Yes" values in metadata columns: Light green background (#D4EDDA), dark green bold text (#155724)
- "No" values: Gray text (#6C757D) for less emphasis
- Priority-based row colors: Critical (light red), High (light amber), Medium (light yellow), Low (white)

### Detailed Analysis (Enhanced)

- Process Overview
- Violations with Impact Analysis
- Code Examples (before, after, explanation)
- Testing Notes
- Priority Score

### Process Flow

- Process information
- Complexity breakdown with scoring
- Activity details table with metadata (Has Error Handling, Has JavaScript, Has SQL)
- Critical paths and recommendations

## Required Files

For each process:

- **LPD file** (required): Process definition file
- **Project standards file** (optional): `Projects/<Client>/project_standards_<Client>.xlsx`

## Workflow Overview

**Stateless Pipeline Architecture**

This skill uses a file-based pipeline that eliminates context accumulation. Each phase reads JSON inputs and writes JSON outputs independently.

**Key Principles:**

- Read `references/DOMAIN_ANALYSIS_GUIDE.md` before Phase 1
- AI analyzes code and identifies violations (Python only extracts/chunks/merges data)
- Consolidate similar violations during analysis (e.g., 25 generic captions → 1 violation with count)
- Project standards override steering file defaults
- Each phase operates in isolation (~2-3 KB context per chunk)

## Analysis Quality Enforcement

**CRITICAL REQUIREMENT**: Analysis quality is NEVER sacrificed for speed or convenience.

### Mandatory Data Reading Rules

**BLOCKING REQUIREMENTS** for all analysis phases (Phases 1-5):

1. **Read Complete Domain Files**
   - ALWAYS read the ENTIRE domain JSON file before analysis
   - NO shortcuts due to time constraints or large file size
   - NO relying on summary statistics or preprocessing flags
   - NO manual creation of analysis files without reading source data

2. **Handle Large Files Properly**
   - If file is truncated on first read, read in chunks until 100% complete
   - Use readFile() with line ranges if needed: `readFile(path, start_line=1, end_line=500)`, then `readFile(path, start_line=501, end_line=1000)`, etc.
   - Continue reading until no truncation warnings remain
   - Verify file completely consumed before proceeding to analysis

3. **Verify Data Completeness**
   - Check file size and line count before analysis
   - Confirm all activities/blocks/queries loaded
   - Cross-reference with metrics_summary.json counts
   - If counts don't match, re-read the file completely

4. **Follow IPA WORKFLOW ENFORCEMENT**
   - **STEP 1**: Data extracted? (Phase 0 complete)
   - **STEP 2**: Data read completely? (MOST CRITICAL - this step prevents incomplete analysis)
   - **STEP 3**: Analysis complete? (All violations identified)
   - **STEP 4**: Root cause identified? (Recommendations provided)

### Common Violations to Avoid

**❌ WRONG - Taking Shortcuts:**

```text
"I see the JavaScript domain file is 1001 lines. Let me read the first 1000 lines and create the analysis based on that."
```

**✅ CORRECT - Reading Complete Data:**

```text
"The JavaScript domain file is 1001 lines. Let me read it completely:
- First read: lines 1-1000
- Second read: lines 1001-1001
Now I have the complete data and can perform accurate analysis."
```

**❌ WRONG - Manual Analysis Creation:**

```text
"Based on the preprocessing flags, I'll manually create javascript_analysis.json with violations for ES6 patterns."
```

**✅ CORRECT - Data-Driven Analysis:**

```text
"Let me read domain_javascript.json completely to see all JavaScript blocks, then analyze each one for ES5 compliance, performance issues, and best practices."
```

### Quality vs Speed Trade-off

**ABSOLUTE RULE**: Quality ALWAYS wins over speed.

- Incomplete analysis (80% data read) = **UNACCEPTABLE**
- Complete analysis (100% data read) = **REQUIRED**
- Extra 2-3 minutes to read complete data = **MANDATORY**
- Accurate findings with all violations = **NON-NEGOTIABLE**

### Root Cause of Incomplete Analysis

**#1 Cause**: Reading only partial domain files (~80-90% of data)

**Impact**:
- Missing violations in unread sections
- Inaccurate violation counts
- Incomplete recommendations
- False confidence in report quality

**Prevention**:
- Always verify file completely read
- Check for truncation warnings
- Read in chunks if needed
- Cross-reference counts with metrics_summary.json

### Enforcement Mechanism

**Pre-Analysis Checklist** (MUST complete before writing analysis JSON):

```text
[ ] Domain file path identified
[ ] File size and line count verified
[ ] Complete file read (no truncation warnings)
[ ] All activities/blocks/queries loaded
[ ] Counts match metrics_summary.json
[ ] Ready to analyze and identify violations
```

**If ANY checkbox is unchecked, STOP and complete that step before proceeding.**

### Step 0: Interactive Selection (MANDATORY)

**Pre-Selection Cleanup:**

Before starting, clean up the Temp folder to ensure a fresh start:

```powershell
# Remove all files in Temp/ except .gitkeep
Get-ChildItem Temp -File | Where-Object { $_.Name -ne '.gitkeep' } | Remove-Item -Force
```

**Selection Process:**

1. **Discover Available Clients**
   - List all directories in `Projects/`
   - Present client options to user
   - Wait for user to select client

2. **Discover RICE Items**
   - List all subdirectories in `Projects/<Client>/`
   - Present RICE item options to user
   - Wait for user to select RICE item

3. **Discover LPD Files**
   - List all `.lpd` files in `Projects/<Client>/<RICE>/`
   - Count total LPD files found
   - Present options:
     - **Single Process Mode**: Select ONE LPD file
     - **Batch Mode**: Select ALL LPD files (if multiple exist)
   - Wait for user to choose mode and selection

4. **Verify Project Standards**
   - Check for `Projects/<Client>/project_standards_<Client>.xlsx`
   - Inform user if found or missing
   - Proceed with or without project standards

5. **Confirm Execution**
   - Display summary of selections
   - Show estimated time (8-12 min per process)
   - Wait for user confirmation to proceed

**Batch Processing:**

When user selects batch mode:

- Process each LPD sequentially (one at a time)
- Preprocessing automatically cleans Temp folder before each process
- Generate individual report for each process
- Show progress: "Processing 2 of 3: InvoiceApproval_APIA_NONPOROUTING_Reject.lpd"
- Provide summary at end with all generated report paths
- Total time: ~8-12 min × number of processes

**Batch Processing Best Practices:**

- Sequential processing: One process completes fully before starting the next
- Independent reports: Each process gets its own Excel report
- Error isolation: If one process fails, others continue
- Progress tracking: Clear indication of which process is being analyzed

**Example Interaction:**

```text
Available Clients:
1. BayCare
2. FPI
3. SONH

Which client? → User selects "1"

Available RICE Items for BayCare:
1. APIA

Which RICE item? → User selects "1"

Found 3 LPD files in BayCare/APIA:
1. InvoiceApproval_APIA_NONPOROUTING.lpd
2. InvoiceApproval_APIA_NONPOROUTING_Reject.lpd
3. InvoiceApproval_APIA_NONPOROUTING_nightly_job_trigger.lpd

Select mode:
A. Single Process (select one LPD)
B. Batch Process (analyze all 3 LPDs)

Your choice? → User selects "B"

Project Standards: Found ✓ (Projects/BayCare/project_standards_BayCare.xlsx)

Summary:
- Client: BayCare
- RICE: APIA
- Mode: Batch (3 processes)
- Estimated time: ~24-36 minutes
- Reports: 3 individual Excel files

Proceed? (yes/no) → User confirms "yes"
```

### Step 1: Phase 0 - Preprocessing (Per Process)

**Phase 0: Preprocessing** (Python Only - No AI)

- Extract LPD structure → `lpd_structure.json`
- Calculate metrics → `metrics_summary.json`
- Load project standards → `project_standards.json`
- Pre-calculate: ES6 patterns, generic names, SQL types, error-prone activities

### Step 2: Phase 1 - Naming Analysis (AI - Incremental)

- Input: `lpd_structure.json` (naming data only), `project_standards.json`
- Task: Analyze filename, node captions, config sets, hardcoded values
- Output: `naming_analysis.json`
- Return: "Phase 1 complete. naming_analysis.json written."

### Step 3: Phase 2 - JavaScript Analysis (AI - Incremental)

- Input: `lpd_structure.json` (JavaScript blocks only), `project_standards.json`
- Task: Analyze ES5 compliance, performance, function order, variable scoping
- Output: `javascript_analysis.json`
- Return: "Phase 2 complete. javascript_analysis.json written."

### Step 4: Phase 3 - SQL Analysis (AI - Incremental)

- Input: `lpd_structure.json` (SQL queries only), `project_standards.json`
- Task: Analyze Compass SQL, pagination, SELECT *, optimization
- Note: Check COMPLETE `lpd_structure.json` for Compass API pagination (InitQuery → GetResult with limit/offset)
- Output: `sql_analysis.json`
- Return: "Phase 3 complete. sql_analysis.json written."

### Step 5: Phase 4 - Error Handling Analysis (AI - Incremental)

- Input: `lpd_structure.json` (error-prone activities only), `project_standards.json`
- Task: Analyze OnError tabs, GetWorkUnitErrors, error coverage
- Output: `errorhandling_analysis.json`
- Return: "Phase 4 complete. errorhandling_analysis.json written."

### Step 6: Phase 5 - Structure Analysis (AI - Direct)

- Input: `lpd_structure.json` (process-level data), `metrics_summary.json`, `project_standards.json`
- Task: Analyze auto-restart, process type, activity distribution
- Output: `structure_analysis.json`
- Return: "Phase 5 complete. structure_analysis.json written."

### Step 7: Phase 6 - Report Assembly (Python Only - No AI)

- Merge: All analysis JSON outputs
- **Enrich Activities**: Add metadata flags (`has_javascript`, `has_sql`, `has_error_handling`) to each activity
  - Loads domain files (not analysis files) to get raw activity data
  - Builds lookup sets from `domain_javascript.json`, `domain_sql.json`, `domain_errorhandling.json`
  - Adds boolean flags to each activity object before passing to template
  - Enables accurate "Has JavaScript", "Has SQL", "Has Error Handling" columns in Activity Details table
- Build: ipa_data structure using `build_ipa_data_helper.py`
- Generate: Excel report using `ipa_coding_standards_template_enhanced.py`
- Save to: `Coding_Standards_Results/`

**Key Benefits:**

- No context accumulation (each phase isolated at ~2-3 KB)
- No crashes (stable execution regardless of file size)
- Faster execution (reduced reasoning overhead)
- Enterprise-grade quality maintained
- Clear separation: AI analyzes, Python processes

## Python Tools

This skill uses the following Python tools from `ReusableTools/IPA_CodingStandards/`:

**Phase 0 (Preprocessing):**

- `preprocess_coding_standards.py` - Extracts and structures data for analysis phases

**Phase 1-4 (Domain Analysis - Incremental):**

- `build_naming_analysis.py` - Chunks naming data, orchestrates AI analysis, merges results
- `build_javascript_analysis.py` - Chunks JS blocks, orchestrates AI analysis, merges results
- `build_sql_analysis.py` - Chunks SQL queries, orchestrates AI analysis, merges results
- `build_errorhandling_analysis.py` - Chunks error activities, orchestrates AI analysis, merges results

**Phase 6 (Report Assembly):**

- `assemble_coding_standards_report.py` - Merges JSON outputs and generates Excel report

**Helpers:**

- `build_ipa_data_helper.py` - Builds ipa_data from violations (prevents duplicates)

**Legacy Tools (Still Used):**

- `organize_by_domain.py` - Used by preprocessing script
- `merge_violations.py` - Used by assembly script

**Templates:**

- `ipa_coding_standards_template_enhanced.py` - Current template (v2.0)
- `ipa_coding_standards_template.py` - Legacy template (v1.0)

## Performance

- Total time: ~8-12 min per process (stable, no crashes)
- Batch mode: ~8-12 min × number of processes
- No context accumulation, scalable for any process size

## Output

**Single Process Mode:**

Excel report saved to: `Coding_Standards_Results/<Client>_<RICE>_<ProcessName>_CodingStandards_<timestamp>.xlsx`

**Batch Process Mode:**

Multiple Excel reports saved to `Coding_Standards_Results/`:

- `<Client>_<RICE>_<Process1>_CodingStandards_<timestamp>.xlsx`
- `<Client>_<RICE>_<Process2>_CodingStandards_<timestamp>.xlsx`
- `<Client>_<RICE>_<Process3>_CodingStandards_<timestamp>.xlsx`

Summary report displayed at end with all generated file paths.

## Example Usage

**Activation:**

```text
/ipa-coding-standards
```

**Interactive Workflow:**

The skill will guide you through selection:

1. **Select Client**: Choose from available clients in Projects/
2. **Select RICE Item**: Choose from RICE items for selected client
3. **Select Processing Mode**:
   - Single Process: Analyze one LPD file
   - Batch Process: Analyze all LPD files in RICE item
4. **Confirm Standards**: Verify project standards file availability
5. **Confirm Execution**: Review summary and proceed

**Single Process Example:**

```text
→ Client: BayCare
→ RICE: APIA
→ Mode: Single
→ LPD: InvoiceApproval_APIA_NONPOROUTING.lpd
→ Standards: ✓ Found
→ Estimated time: ~8-12 minutes
→ Output: 1 Excel report
```

**Batch Process Example:**

```text
→ Client: BayCare
→ RICE: APIA
→ Mode: Batch (3 processes)
→ LPDs: All 3 files in APIA folder
→ Standards: ✓ Found
→ Estimated time: ~24-36 minutes
→ Output: 3 individual Excel reports

Progress:
✓ 1/3: InvoiceApproval_APIA_NONPOROUTING.lpd (12 min)
→ 2/3: InvoiceApproval_APIA_NONPOROUTING_Reject.lpd...
  3/3: InvoiceApproval_APIA_NONPOROUTING_nightly_job_trigger.lpd
```

## Architecture Notes

### Stateless Pipeline Design

**Problem**: Sequential subagent execution caused variable context usage and potential failures.

**Solution**: File-based stateless pipeline

- **Phase 0 (Python)**: Deterministic preprocessing, no AI reasoning
- **Phases 1-5 (AI)**: Independent analysis phases, each reads JSON input and writes JSON output
- **Phase 6 (Python)**: Deterministic report assembly, no AI reasoning

**Key Principles:**

1. Intelligence from focused analysis, not cumulative memory
2. Each phase operates in isolation (~2-3 KB context per chunk)
3. File-based state transfer (JSON files replace conversational memory)
4. Minimal AI output ("Phase N complete. file.json written.")
5. No context accumulation (stable execution regardless of file size)

### Project Standards Integration

**Critical Feature**: Project-specific standards override steering file defaults

**Workflow**:

1. Phase 0 loads `Projects/<Client>/project_standards_<Client>.xlsx`
2. Converts to `project_standards.json`
3. Each analysis phase reads `project_standards.json` FIRST
4. Project standards take precedence over steering defaults

**Example Standards**:

- Filename format: `<Prefix>_WF_<Desc>.lpd` for approval workflows
- Config set naming: Must include vendor name
- JavaScript: No ES6 features allowed
- SQL: Pagination required for queries returning >100 rows

## Critical Rules

1. **INTERACTIVE SELECTION MANDATORY**
   - ALWAYS present client/RICE/LPD options to user
   - NEVER auto-select without user confirmation
   - Support both single and batch processing modes
   - Show clear progress in batch mode

2. **ONE PROCESS AT A TIME (Architecture)**
   - ONE LPD → ONE report (individual reports)
   - Batch mode processes sequentially, not consolidated
   - No multi-process consolidation (different use case than Client Handover)

3. **AI MUST ANALYZE EVERY PROCESS (Batch Mode)**
   - **BLOCKING REQUIREMENT**: AI reads and analyzes data for EVERY process
   - AI is the analyst; Python preprocessing is a helper
   - Create violations for ANY issues found, whether Python flagged them or not
   - NO empty violation files
   - NO skipping analysis phases
   - Each process gets full Phases 1-5 analysis
   - Python only helps with data prep and merging, NOT analysis

4. **STATELESS PHASE EXECUTION**
   - Each phase reads ONLY required JSON files
   - Each phase writes ONLY one JSON output
   - Each phase returns minimal confirmation
   - No context accumulation across phases

5. **PROJECT STANDARDS PRECEDENCE**
   - Phase 0 ALWAYS loads project standards (if available)
   - Each analysis phase reads project standards FIRST
   - Project standards override steering defaults
   - If no project standards, use steering defaults only

6. **PYTHON LIFTS HEAVY LOAD**
   - Python: Extract, organize, chunk, merge, format
   - AI: Analyze chunks, identify violations, recommend fixes
   - Python does NOT make judgments

7. **INCREMENTAL WRITING**
   - Large domains (JavaScript, SQL) processed in chunks
   - AI analyzes small chunks (~20-50 items)
   - Python merges chunk results
   - Prevents context overload

8. **INTERNAL REVIEW FOCUS**
   - Technical language and code criticism allowed
   - Severity ratings (High, Medium, Low)
   - Specific code examples and recommendations
   - Focus on HOW to fix, not just WHAT is wrong

9. **COMPLETE DATA ANALYSIS MANDATORY** ⚠️ CRITICAL
   - **BLOCKING REQUIREMENT**: Analysis quality MUST NEVER be sacrificed due to time constraints or data volume
   - **ALWAYS read complete domain files** before analysis, even if files are large or truncated
   - **NO shortcuts allowed** - read files in chunks until 100% complete
   - **NO manual creation** of analysis files without reading complete source data
   - **VERIFY file completely read** before proceeding to analysis phase
   - **Follow IPA WORKFLOW ENFORCEMENT** rules from steering files (Step 2: DATA READ COMPLETELY)
   - **Quality > Speed** - Incomplete analysis is worse than slower analysis
   - **Root Cause**: Reading only partial data (~80%) is the #1 cause of incomplete analysis
   - **Consequence**: Incomplete reports with missing violations and inaccurate findings
   - **Solution**: Use readFile() with line ranges or multiple reads until entire file consumed

## Related Documentation

- `.kiro/steering/00_Core_System_Rules.md` - Core system rules
- `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` - IPA concepts
- `.kiro/steering/11_IPA_Report_Generation.md` - Report generation guidelines
- `.kiro/skills/ipa-coding-standards/` - Skill implementation (active)
- `ReusableTools/IPA_CodingStandards/` - Python tools and templates

## Troubleshooting

### Quick Diagnosis

```bash
python ReusableTools/IPA_CodingStandards/validate_analysis_jsons.py
```

### Common Issues

**"Process Count: 0"** → Phase 0 was skipped, run preprocessing first

**"No violations found"** → Check if project standards loaded correctly

**"Missing domain analysis"** → One of Phases 1-5 failed, check Temp/ folder for partial outputs

**"Invalid project standards"** → Excel file format incorrect, verify sheet name is "Standards"

**Empty sheets** → Analysis JSONs incomplete, validate structure

See `references/TROUBLESHOOTING.md` for complete guide.

## Reference Documentation

Comprehensive documentation is available in the `references/` folder:

### Core Guides

- **`WORKFLOW_GUIDE.md`** - Complete step-by-step workflow
- **`DOMAIN_ANALYSIS_GUIDE.md`** - Domain-specific analysis patterns
- **`JSON_SCHEMAS.md`** - Complete JSON structure reference
- **`TROUBLESHOOTING.md`** - Common issues and solutions
- **`COMMON_ISSUES.md`** - Catalog of known issues and fixes
- **`CODING_STANDARDS_REFERENCE.md`** - Coding standards rules reference
- **`TOOLS_README.md`** - Python tool usage and examples

### When to Use Each Guide

- **Starting a new analysis?** → Read `WORKFLOW_GUIDE.md` first
- **Domain-specific questions?** → See `DOMAIN_ANALYSIS_GUIDE.md`
- **JSON structure questions?** → Check `JSON_SCHEMAS.md`
- **Report generation problems?** → Consult `TROUBLESHOOTING.md`
- **Known issues or errors?** → Check `COMMON_ISSUES.md` first
- **Tool usage questions?** → Reference `TOOLS_README.md`
- **Standards rules reference?** → See `CODING_STANDARDS_REFERENCE.md`

### Loading Reference Documentation

Reference files are loaded on-demand when needed. The skill is self-contained and portable - all necessary information is included in this skill package.

## Confidentiality

Internal code quality review. Technical language and code criticism appropriate.
