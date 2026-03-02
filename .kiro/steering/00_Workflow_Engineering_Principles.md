---
inclusion: auto
name: workflow-engineering
description: Subagent architecture, hook design, context budget planning, workflow splitting, orchestration optimization, and multi-phase execution strategies.
---

# Workflow Engineering Principles

## Table of Contents

- [Stateless Pipeline Architecture](#stateless-pipeline-architecture)
  - [Core Principle](#core-principle)
  - [Stateless vs Stateful Execution](#stateless-vs-stateful-execution)
  - [File-Based State Transfer](#file-based-state-transfer)
  - [Phase Isolation Pattern](#phase-isolation-pattern)
- [Subagent Architecture](#subagent-architecture)
  - [Critical Design Rules](#critical-design-rules)
  - [Subagent Verification Checklist](#subagent-verification-checklist)
- [IPA Analysis Workflow](#ipa-analysis-workflow)
  - [Mandatory Workflow Steps](#mandatory-workflow-steps)
  - [Key Rules](#key-rules)
- [Reusable Tools](#reusable-tools)
  - [Key Tools](#key-tools)
  - [Hook Manager](#hook-manager-critical-for-hook-editing)
  - [Excel Reader](#excel-reader-critical-for-binary-files)
- [Advanced Architectural Patterns](#advanced-architectural-patterns)
  - [Hook Structure Validation](#hook-structure-validation)
  - [Schema Validation for Subagent Outputs](#schema-validation-for-subagent-outputs)
  - [Context Accumulation in Sequential Execution](#context-accumulation-in-sequential-execution)

## Stateless Pipeline Architecture

### Core Principle

**Intelligence must come from focused domain analysis, not cumulative conversational memory.**

Each phase must operate in isolation, using file-based state transfer instead of shared reasoning history.

### Stateless vs Stateful Execution

**❌ STATEFUL (Causes Context Accumulation Crashes)**

```text
Phase 1 → Phase 2 → Phase 3 → Phase 4 → CRASH
  ↓         ↓         ↓         ↓
Context   Context   Context   Context
 10 KB     25 KB     45 KB     80 KB (CRASH)
```

- Each phase inherits full conversational history
- Previous reasoning traces passed to subsequent phases
- Large structured outputs stored in conversation memory
- Cumulative context growth across phases

**✅ STATELESS (Crash-Safe)**

```text
Phase 1 → file.json → Phase 2 → file.json → Phase 3
  ↓                     ↓                     ↓
Context               Context               Context
 10 KB                 10 KB                 10 KB
```

- Each phase reads only required source files
- Produces structured JSON output
- Returns minimal confirmation
- Clears reasoning context before next phase

### File-Based State Transfer

**Pattern:**

```python
# Phase 1: Analysis
input_data = read_json("source_data.json")
analysis_result = perform_analysis(input_data)
write_json("analysis_result.json", analysis_result)
return "Phase 1 complete. analysis_result.json written."

# Phase 2: Next Analysis (CLEAN CONTEXT)
analysis_data = read_json("analysis_result.json")
next_result = perform_next_analysis(analysis_data)
write_json("next_result.json", next_result)
return "Phase 2 complete. next_result.json written."
```

**Benefits:**

- No context accumulation
- Each phase starts with clean slate
- Explicit data dependencies
- Easy to debug and resume
- Parallel execution possible

### Phase Isolation Pattern

**Client Handover Example:**

```text
Phase 0: Preprocessing (Python Only)
├─ Extract ANA-050 content → spec_raw.json
├─ Extract LPD structure → lpd_structure.json
├─ Calculate metrics → metrics_summary.json
└─ No AI reasoning

Phase 1: Business Requirements Analysis
├─ Input: spec_raw.json
├─ Task: Extract business objectives, requirements, stakeholders
├─ Output: business_analysis.json
└─ Return: "Phase 1 complete. business_analysis.json written."

Phase 2: Workflow Architecture Analysis
├─ Input: lpd_structure.json
├─ Task: Identify process branches, decision nodes, transformations
├─ Output: workflow_analysis.json
└─ Return: "Phase 2 complete. workflow_analysis.json written."

Phase 3: Configuration & Technical Components
├─ Input: lpd_structure.json, metrics_summary.json
├─ Task: Identify file channels, web services, security roles
├─ Output: configuration_analysis.json
└─ Return: "Phase 3 complete. configuration_analysis.json written."

Phase 4: Risk & Compliance Review
├─ Input: All prior JSON outputs
├─ Task: Identify technical risks, maintenance risks, scalability concerns
├─ Output: risk_assessment.json
└─ Return: "Phase 4 complete. risk_assessment.json written."

Phase 5: Report Assembly (Python Only)
├─ Merge: All JSON outputs
├─ Populate: Client handover template
└─ Generate: Final Excel report
```

**Critical Rules:**

1. No multi-subagent sequential inheritance
2. No parallel subagent execution for large reasoning tasks
3. Each phase must operate independently
4. Do not include prior reasoning traces in prompts
5. Only pass filenames as inputs between phases
6. Keep conversational output minimal
7. AI performs analysis only — Python performs heavy data processing

**Quality Assurance:**

Each phase must:

- Reference source data explicitly
- Avoid generic summaries
- Provide detailed structured JSON
- Separate technical and non-technical explanations
- Maintain enterprise-grade documentation depth

**Expected Outcomes:**

- ✅ No context accumulation crashes
- ✅ Reduced execution instability
- ✅ Stable memory footprint
- ✅ Faster execution due to reduced reasoning overhead
- ✅ Maximum documentation detail preserved
- ✅ Clear separation of concerns between AI reasoning and deterministic processing

## Subagent Architecture

### Critical Design Rules

**RULE 1: No Nested Subagent Calls**

- Subagents must NEVER have `invokeSubAgent` tool access
- Only the main agent can invoke subagents
- Subagents must use their own `fsWrite` tool, never invoke file-writer-helper

**RULE 2: Valid Tool Access Patterns**

- `tools: ["read"]` - Analysis only, returns data to main agent
- `tools: ["read", "fsWrite"]` - Can analyze and save files directly (RECOMMENDED)
- `tools: ["read", "shell"]` - Rare, for specialized operations
- ❌ NEVER: Any combination with `invokeSubAgent`

**RULE 3: Subagent Output Handling**

Two patterns:

1. **Return Pattern**: Subagent returns analysis as JSON string, main agent saves file
2. **Save Pattern** (RECOMMENDED): Subagent saves its own output using fsWrite directly
   - For large files (>1000 lines), hook prompt instructs subagent to use chunked writes

**RULE 4: Explicit Steering File Loading**

Subagents must use `discloseContext()` to load domain-specific steering files at workflow start:

- NO auto-loading (unreliable in subagents)
- Load ONLY domain-specific files needed
- Exclude `00_Kiro_General_Rules.md` (already provided via system instructions)

**Steering File Name Mapping**:

- `00_Workflow_Engineering_Principles.md` → `discloseContext(name="workflow-engineering")`
- `01_IPA_and_IPD_Complete_Guide.md` → `discloseContext(name="ipa-ipd-guide")`
- `02_Work_Unit_Analysis.md` → `discloseContext(name="work-unit-analysis")`
- `03_Process_Patterns_Library.md` → `discloseContext(name="process-patterns")`
- `04_WU_Report_Generation.md` → `discloseContext(name="wu-report-generation")`
- `05_Compass_SQL_CheatSheet.md` → `discloseContext(name="compass-sql")`
- `06_FSM_Business_Classes_and_API.md` → `discloseContext(name="fsm-business-classes")`
- `10_IPA_Report_Generation.md` → `discloseContext(name="ipa-report-generation")`
- `11_RICE_Methodology_and_Specifications.md` → `discloseContext(name="rice-methodology")`

**RULE 5: Explicit Context Passing**

Hook prompts must pass explicit context parameters:

- **Client**: Client name (e.g., "FPI", "BayCare")
- **RICE**: RICE item name (e.g., "MatchReport", "APIA")
- **Process**: Process name from LPD (e.g., "MatchReport_Outbound")

**RULE 6: Context Budget Planning**

Calculate cumulative context BEFORE designing multi-subagent workflows:

- Formula: Hook + (Subagent_Def + Input) * N subagents
- If cumulative > 60 KB, consider splitting workflow
- If cumulative > 80 KB, MUST split workflow into separate hooks

**Pattern: Two-Hook Split (Best for 5+ subagents)**

```text
Hook 1: Data Preparation
- Extract data
- Organize by sections
- Save section files
- END (user triggers Hook 2)

Hook 2: Analysis + Report (CLEAN CONTEXT)
- Launch subagents sequentially
- Merge results
- Generate report
```

### Subagent Verification Checklist

Before creating/modifying a subagent:

- [ ] Does it have `invokeSubAgent` access? → Remove it
- [ ] Does it invoke file-writer-helper? → Remove and use fsWrite
- [ ] Does it have `tools: ["read", "fsWrite"]` for saving files? → Correct
- [ ] Does it use `discloseContext()` to load steering files? → Add if missing
- [ ] Does it load ONLY domain-specific steering files? → Remove general rules
- [ ] Does hook pass explicit context (Client, RICE, Process)? → Add if missing
- [ ] Are input file paths explicitly documented in workflow? → Add if missing

## IPA Analysis Workflow

### Mandatory Workflow Steps

**ROOT CAUSE OF RECURRING ISSUE**: Skipping the data reading step and going straight to report generation.

#### Step 1: Extract Data (Python)

```python
extract_lpd_data(lpd_files, 'Temp/project_lpd_data.json')
```

#### Step 2: READ THE COMPLETE JSON DATA (Kiro) - BLOCKING REQUIREMENT

```text
🛑 STOP - You MUST read the JSON file using readFile() BEFORE proceeding
🛑 DO NOT build ipa_data without reading the extracted data first
🛑 DO NOT rely on summary statistics - READ THE ACTUAL DATA
```

#### Step 3: ANALYZE THE DATA YOU JUST READ (Kiro)

- Review ALL processes
- Check ALL activities
- Identify ALL issues
- Count ALL violations

#### Step 4: Build ipa_data Dictionary (Kiro)

- Based on YOUR analysis from Step 3
- Include findings from ALL processes
- Provide specific examples and counts

#### Step 5: Generate Report (Python)

```python
from template import generate_report
generate_report(ipa_data)
```

### Key Rules

**1:1 JSON Mapping Rule**: ONE LPD file → ONE JSON file → ONE report

**Role Separation**:

- Python: Extract data, parse files, structure raw data, format reports, perform calculations
- AI (Kiro): Assess code quality, identify issues, make recommendations, score quality metrics, determine severity

**DEDUPLICATION RULE**: Build `recommendations` array DIRECTLY from `violations` array to prevent duplicate action items.

**Main Agent Orchestration**: When Python tools handle data merging and processing, main agent should only orchestrate the workflow. Do NOT read intermediate files - Python will handle that. Only verify files exist, don't read them.

## Reusable Tools

### Key Tools

| Tool | Location | Purpose |
|------|----------|---------|
| **IPA Analyzer** | `ReusableTools/IPA_Analyzer/` | Extract data from LPD files, WU logs, specs |
| **Coding Standards** | `ReusableTools/IPA_CodingStandards/` | Programmatic coding standards analysis |
| **Hook Manager** | `ReusableTools/hook_manager.py` | Safe hook editing with backups, validation, repair |
| **Excel Reader** | `ReusableTools/excel_reader.py` | Read Excel files when readFile fails (binary files) |
| **JSON Validator** | `ReusableTools/validate_json.py` | Generic JSON validator with hook auto-detection |

### Hook Manager (CRITICAL FOR HOOK EDITING)

Comprehensive Python tool for safe hook editing that operates outside the context system.

**Commands:**

```bash
python ReusableTools/hook_manager.py validate <hook_file>
python ReusableTools/hook_manager.py backup <hook_file>
python ReusableTools/hook_manager.py restore <hook_file> <backup_path>
python ReusableTools/hook_manager.py analyze <hook_file>
python ReusableTools/hook_manager.py repair <hook_file>
```

**When to Use:**

- ANY hook editing in long sessions (10+ messages)
- After ANY fsWrite failure on hook files
- Before making major hook changes (backup first)

### Excel Reader (CRITICAL FOR BINARY FILES)

Read Excel files when readFile fails with "File seems to be binary".

**Usage:**

```python
# Via executePwsh (recommended)
executePwsh("python -c \"from ReusableTools.excel_reader import read_excel; df = read_excel('file.xlsx', sheet_name='Standards', display=True)\"")

# Export to JSON first
executePwsh("python ReusableTools/excel_reader.py file.xlsx --sheet Standards --json output.json")
```

**Integration:** MANDATORY for reading project_standards.xlsx files in coding standards workflow.

## Advanced Architectural Patterns

### Hook Structure Validation

Hooks should have ONLY ONE "prompt" key, inside the "then" object:

```json
{
  "enabled": true,
  "name": "HookName",
  "description": "...",
  "version": "N",
  "when": {...},
  "newSession": true,
  "then": {
    "type": "askAgent",
    "prompt": "ALL WORKFLOW INSTRUCTIONS GO HERE"
  }
}
```

**Never add a root-level "prompt" key** - this is NOT part of the standard hook schema.

### Schema Validation for Subagent Outputs

AI-driven subagents need explicit schema validation to ensure uniform output.

**Three-Layer Defense:**

1. **Schema Validator**: Defines exact JSON schemas, validates required fields
2. **Merge-Time Validation**: Validates each subagent output before merging
3. **Defensive Transformations**: Report generator handles variations, provides fallbacks

**Critical Rules:**

- Always run schema validation during merge process
- Report generator must handle variations in subagent output (dict vs array)
- Provide fallbacks for missing fields
- Merge raw data with analyzed data for completeness

### Context Accumulation in Sequential Execution

**Problem:** Client handover workflow crashed at subagent #3 (Configuration Analyzer) despite all optimizations (hook simplification, explicit input files, data extraction). Cumulative context reached 80 KB at crash point.

**Root Cause:** Sequential subagent execution in the SAME SESSION accumulates context from all previous subagents:

- Hook prompt: 17 KB
- Subagent #1 (definition + input): ~12 KB
- Subagent #2 (definition + input): ~30 KB
- Subagent #3 (definition + input): ~5 KB
- **Cumulative at crash: 80 KB** (exceeds system limits)

**Key Discovery:** Even with optimized prompts and small input files, sequential execution accumulates context linearly. By subagent #3, the system has loaded:

- Original hook prompt
- All previous subagent definitions
- All previous input files
- All previous outputs (even if not explicitly read)

**Solution:** Use stateless pipeline architecture instead of multi-subagent chaining.

**NEW RECOMMENDED PATTERN: Stateless Pipeline**

Replace multi-subagent orchestration with file-based phase execution:

```text
Phase 0: Python preprocessing → JSON files
Phase 1: AI analysis → JSON output → "Phase 1 complete"
Phase 2: AI analysis → JSON output → "Phase 2 complete"
Phase 3: AI analysis → JSON output → "Phase 3 complete"
Phase 4: AI analysis → JSON output → "Phase 4 complete"
Phase 5: Python assembly → Final report
```

Each phase operates independently with clean context.

**LEGACY PATTERN: Two-Hook Split (Deprecated)**

- Hook 1 (Data Preparation): Extract + Organize (Steps 1-7)
- Hook 2 (Analysis + Report): Launch subagents + Generate report (Steps 8-14)
- Benefit: Hook 2 starts with CLEAN context, no accumulation
- Tradeoff: User must trigger two hooks instead of one
- **Issue**: Still accumulates context within Hook 2

**Prevention:**

1. **Context Budget Checklist**

   - [ ] Calculate hook prompt size
   - [ ] Calculate each subagent definition size
   - [ ] Calculate each input file size
   - [ ] Calculate cumulative context: Hook + Sum(Subagent + Input)
   - [ ] If cumulative > 60 KB, plan workflow split
   - [ ] If cumulative > 80 KB, MUST split workflow

2. **Workflow Design Checklist**

   - [ ] Count subagents (if 5+, consider split)
   - [ ] Measure cumulative context
   - [ ] Design split points (data prep vs analysis)
   - [ ] Test with actual files before production
   - [ ] Document context budget in hook description

3. **Testing Checklist**

   - [ ] Test with largest expected input files
   - [ ] Monitor context at each subagent execution
   - [ ] Verify no crashes at any point
   - [ ] Measure total execution time
   - [ ] Document context budget and split rationale

**Affected Files:**

- `.kiro/hooks/ipa-client-handover.kiro.hook` (v44 - crashed at subagent #3)
- `.kiro/steering/00_Workflow_Engineering_Principles.md` - This documentation

**Impact:** Identified fundamental limit of sequential subagent execution in same session. Stateless pipeline pattern provides reliable solution for multi-phase workflows.
