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

- **Domain-Segmented Analysis**: Analyzes 5 domains separately (Naming, JavaScript, SQL, Error Handling, Structure)
- **Project Standards Integration**: Loads and applies client-specific coding standards
- **Incremental Processing**: Chunks large processes to prevent context overload
- **Crash-Safe**: Resumable from any phase
- **Scalable**: Works with any process size (tested with 450+ activities)
- **One Process at a Time**: Generates ONE Excel report per process

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

### Detailed Analysis (Enhanced)
- Process Overview
- Violations with Impact Analysis
- Code Examples (before, after, explanation)
- Testing Notes
- Priority Score

### Process Flow
- Process information
- Complexity breakdown with scoring
- Activity flow diagram
- Critical paths and recommendations

## Required Files

For each process:

- **LPD file** (required): Process definition file
- **Project standards file** (optional): `Projects/<Client>/project_standards_<Client>.xlsx`

## Workflow Overview

**Stateless Pipeline Architecture (Crash-Safe)**

This skill uses a stateless, file-based pipeline that eliminates context accumulation:

1. **User Selection** (Interactive)
   - Select client from Projects/ directory
   - Select RICE item
   - Select ONE LPD file
   - Confirm project standards availability

2. **Phase 0: Preprocessing** (Python Only - No AI)
   - Extract LPD structure → `lpd_structure.json`
   - Calculate metrics → `metrics_summary.json`
   - Load project standards → `project_standards.json`
   - Pre-calculate: ES6 patterns, generic names, SQL types, error-prone activities

3. **Phase 1: Naming Analysis** (AI - Incremental)
   - Input: `lpd_structure.json` (naming data only), `project_standards.json`
   - Task: Analyze filename, node captions, config sets, hardcoded values
   - Process: Python chunks data → AI analyzes chunks → Python merges
   - Output: `naming_analysis.json`
   - Return: "Phase 1 complete. naming_analysis.json written."

4. **Phase 2: JavaScript Analysis** (AI - Incremental)
   - Input: `lpd_structure.json` (JavaScript blocks only), `project_standards.json`
   - Task: Analyze ES5 compliance, performance, function order, variable scoping
   - Process: Python chunks JS blocks → AI analyzes chunks → Python merges
   - Output: `javascript_analysis.json`
   - Return: "Phase 2 complete. javascript_analysis.json written."

5. **Phase 3: SQL Analysis** (AI - Incremental)
   - Input: `lpd_structure.json` (SQL queries only), `project_standards.json`
   - Task: Analyze Compass SQL, pagination, SELECT *, optimization
   - Process: Python chunks queries → AI analyzes chunks → Python merges
   - Output: `sql_analysis.json`
   - Return: "Phase 3 complete. sql_analysis.json written."

6. **Phase 4: Error Handling Analysis** (AI - Incremental)
   - Input: `lpd_structure.json` (error-prone activities only), `project_standards.json`
   - Task: Analyze OnError tabs, GetWorkUnitErrors, error coverage
   - Process: Python chunks activities → AI analyzes chunks → Python merges
   - Output: `errorhandling_analysis.json`
   - Return: "Phase 4 complete. errorhandling_analysis.json written."

7. **Phase 5: Structure Analysis** (AI - Direct)
   - Input: `lpd_structure.json` (process-level data), `metrics_summary.json`, `project_standards.json`
   - Task: Analyze auto-restart, process type, activity distribution
   - Output: `structure_analysis.json`
   - Return: "Phase 5 complete. structure_analysis.json written."

8. **Phase 6: Report Assembly** (Python Only - No AI)
   - Merge: All analysis JSON outputs
   - Build: ipa_data structure using `build_ipa_data_helper.py`
   - Generate: Excel report using `ipa_coding_standards_template_enhanced.py`
   - Save to: `Coding_Standards_Results/`

**Key Benefits:**

- ✅ No context accumulation (each phase isolated at ~2-3 KB)
- ✅ No crashes (stable execution regardless of file size)
- ✅ Faster execution (reduced reasoning overhead)
- ✅ Enterprise-grade quality maintained
- ✅ Clear separation: AI analyzes, Python processes

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

**Incremental Pipeline (Current Architecture):**

- Phase 0 (Preprocessing): ~2-3s
- Phase 1 (Naming Analysis): ~1-2 min (chunked)
- Phase 2 (JavaScript Analysis): ~2-3 min (chunked)
- Phase 3 (SQL Analysis): ~1-2 min (chunked)
- Phase 4 (Error Handling Analysis): ~1-2 min (chunked)
- Phase 5 (Structure Analysis): ~30-60s (direct)
- Phase 6 (Report Assembly): ~5-10s
- **Total**: ~8-12 min per process (stable, no crashes)

**Key Improvements:**
- ✅ No AI output >3 KB (was variable with subagents)
- ✅ No context accumulation (each chunk isolated)
- ✅ Crash-safe (can resume from any chunk)
- ✅ Scalable (works for 50 or 5,000 activities)

## Output

Excel report saved to: `Coding_Standards_Results/<Client>_<RICE>_<ProcessName>_CodingStandards_<timestamp>.xlsx`

## Example Usage

```text
/ipa-coding-standards
```

Then follow the interactive prompts to:

1. Select client (e.g., "BayCare")
2. Select RICE item (e.g., "APIA")
3. Select LPD file (e.g., "InvoiceApproval_APIA_NONPOROUTING.lpd")
4. Confirm project standards file
5. Confirm report generation

## Architecture Notes

### Stateless Pipeline Design

**Problem**: Sequential subagent execution caused variable context usage and potential failures.

**Solution**: File-based stateless pipeline

- **Phase 0 (Python)**: Deterministic preprocessing, no AI reasoning
- **Phases 1-5 (AI)**: Independent analysis phases, each reads JSON input and writes JSON output
- **Phase 6 (Python)**: Deterministic report assembly, no AI reasoning

**Key Principles:**

1. **Intelligence from focused analysis, not cumulative memory**
2. **Each phase operates in isolation** (~2-3 KB context per chunk)
3. **File-based state transfer** (JSON files replace conversational memory)
4. **Minimal AI output** ("Phase N complete. file.json written.")
5. **No context accumulation** (stable execution regardless of file size)

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

### Role Separation

- **Python**: Extract data, parse files, structure raw data, format reports, perform calculations, chunk data, merge results
- **AI (Kiro)**: Assess code quality, identify violations, determine severity, make recommendations, score quality metrics

## Critical Rules

1. **ONE PROCESS AT A TIME**
   - ONE LPD → ONE report
   - No multi-process consolidation (different use case than Client Handover)

2. **STATELESS PHASE EXECUTION**
   - Each phase reads ONLY required JSON files
   - Each phase writes ONLY one JSON output
   - Each phase returns minimal confirmation
   - No context accumulation across phases

3. **PROJECT STANDARDS PRECEDENCE**
   - Phase 0 ALWAYS loads project standards (if available)
   - Each analysis phase reads project standards FIRST
   - Project standards override steering defaults
   - If no project standards, use steering defaults only

4. **PYTHON LIFTS HEAVY LOAD**
   - Python: Extract, organize, chunk, merge, format
   - AI: Analyze chunks, identify violations, recommend fixes
   - Python does NOT make judgments

5. **INCREMENTAL WRITING**
   - Large domains (JavaScript, SQL) processed in chunks
   - AI analyzes small chunks (~20-50 items)
   - Python merges chunk results
   - Prevents context overload

6. **INTERNAL REVIEW FOCUS**
   - Technical language and code criticism allowed
   - Severity ratings (High, Medium, Low)
   - Specific code examples and recommendations
   - Focus on HOW to fix, not just WHAT is wrong

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

