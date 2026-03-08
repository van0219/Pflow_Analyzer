---
name: "ipa-client-handover"
description: "Generate professional client-facing IPA documentation with comprehensive Excel reports including workflow diagrams, business requirements, activity guides, and maintenance instructions. Use when creating client handover documentation, documenting IPA processes, or generating comprehensive process documentation."
---

# IPA Client Handover Documentation Skill

Generate professional, client-facing documentation for IPA processes. This skill creates comprehensive Excel reports with workflow diagrams, business requirements, activity guides, configuration documentation, and production validation.

## What This Skill Does

Creates client handover documentation that:

- Extracts business requirements from functional specifications (ANA-050)
- Maps process workflows and approval paths from LPD files
- Documents configurable settings with modification instructions
- Generates activity reference guides in business-friendly language
- Validates production readiness from work unit logs
- Produces ONE consolidated Excel report per RICE item (supports multiple processes)

## When to Use This Skill

Use this skill when you need to:

- Create client handover documentation for completed IPA implementations
- Document IPA processes for knowledge transfer
- Generate comprehensive process documentation for maintenance teams
- Produce professional reports for project deliverables
- Document multiple related processes as a single RICE deliverable

## Key Features

- **Multi-Process Support**: Handles 1-N LPD files per RICE item, generates ONE report
- **Section-Segmented Architecture**: Analyzes 5 documentation sections with specialized subagents
- **Client-Facing Language**: No code criticism, focuses on understanding and maintenance
- **Production-Grade**: Extracts real data from source files (95% ready)
- **Scalable**: Works with any IPA size
- **Graceful Degradation**: Works with or without specs/WU logs

## Documentation Sections

1. **Business Requirements** - What and why (from functional spec)
2. **Workflow** - How it flows (from LPD activities)
3. **Configuration** - What can be changed (from config variables)
4. **Activity Guide** - Reference documentation (from activities)
5. **Validation** - Production proof (from WU logs)

## Report Structure

### Single Process Report

- Executive Summary
- Business Requirements
- Validation Summary
- Configuration Guide
- Activity Guide
- Process Workflow (detailed)
- Maintenance Guide

### Multiple Process Report

- Executive Summary (consolidated)
- Business Requirements (RICE-level)
- Validation Summary (consolidated)
- Configuration Guide (consolidated)
- Activity Guide (consolidated)
- Process_<ProcessName1> (detailed workflow)
- Process_<ProcessName2> (detailed workflow)
- Process_<ProcessName3> (detailed workflow)
- Maintenance Guide (consolidated)

## Required Files

For each process:

- **LPD file** (required): Process definition file
- **ANA-050 spec** (optional): Functional specification document
- **Work unit log** (optional): Production validation log

## Workflow Overview

**NEW: Stateless Pipeline Architecture (Crash-Safe)**

This skill uses a stateless, file-based pipeline that eliminates context accumulation:

**Pre-Workflow Cleanup:**

Before starting the workflow, clean up the Temp folder to ensure a fresh start:

```powershell
# Remove all files in Temp/ except .gitkeep
Get-ChildItem Temp -File | Where-Object { $_.Name -ne '.gitkeep' } | Remove-Item -Force
```

This prevents stale data from previous runs from interfering with the current analysis.

1. **User Selection** (Interactive)
   - Select client from Projects/ directory
   - Select RICE item
   - Select one or more LPD files (multi-select)
   - Confirm spec and WU log availability

2. **Phase 0: Preprocessing** (Python Only - No AI)
   - Extract ANA-050 content → `spec_raw.json`
   - Extract LPD structure → `lpd_structure.json`
   - Calculate metrics → `metrics_summary.json`
   - Pre-calculate: activity counts, script lengths, ES6 patterns, SQL statements, integrations

3. **Phase 1: Business Requirements Analysis** (AI)
   - Input: `spec_raw.json`
   - Task: Extract business objectives, requirements, stakeholders, integrations
   - Output: `business_analysis.json`
   - Return: "Phase 1 complete. business_analysis.json written."

4. **Phase 2: Workflow Architecture Analysis** (AI - Incremental Writing)
   - Input: `lpd_structure.json` (or individual `lpd_process_N.json` files for multi-process)
   - Task: Generate specific activity descriptions for EACH activity based on JavaScript code, SQL queries, and branch conditions
   - **CRITICAL**: Use Python script to WRITE workflow_analysis.json incrementally, NOT by reading everything into memory
   - Output: `workflow_analysis.json` with `activity_descriptions` and `activity_purposes` dictionaries
   - Return: "Phase 2 complete. workflow_analysis.json written."
   
   **Phase 2 Correct Approach - Incremental Writing:**
   
   For ANY size process (single or multiple):
   1. Create Python script: `Temp/build_workflow_analysis.py`
   2. Script reads lpd_structure in CHUNKS (e.g., 50 activities at a time)
   3. For each chunk, AI analyzes and returns descriptions
   4. Script APPENDS to workflow_analysis.json incrementally
   5. Final result: Complete workflow_analysis.json without loading everything into memory
   
   **Example Python approach:**
   ```python
   # Read activity count from metrics
   # Loop through activities in chunks of 50
   # For each chunk: AI analyzes → returns dict → append to JSON
   # Result: workflow_analysis.json built incrementally
   ```
   
   **WRONG APPROACH (causes crashes):**
   - ❌ Read entire lpd_structure.json into AI context
   - ❌ Generate entire workflow_analysis.json in one response
   - ❌ Write massive JSON output all at once
   
   **RIGHT APPROACH (crash-safe):**
   - ✅ Python script orchestrates the workflow
   - ✅ AI analyzes small chunks (50 activities)
   - ✅ Python appends results incrementally
   - ✅ No memory/context overload
   
   **Phase 2 Required Output:**
   ```json
   {
     "activity_descriptions": {
       "ActivityID": "Specific description based on JavaScript/SQL/branch analysis"
     },
     "activity_purposes": {
       "ActivityID": "When and why this activity runs"
     }
   }
   ```

5. **Phase 3: Configuration & Technical Components** (AI - Incremental)
   - **Script**: `ReusableTools/IPA_ClientHandover/build_configuration_analysis.py`
   - Input: `lpd_process_N.json` files
   - Task: Extract and analyze configuration by category
   - **CRITICAL**: Use Python script to extract and chunk configuration data
   - Output: `configuration_analysis.json`
   - Return: "Phase 3 complete. configuration_analysis.json written."
   
   **Phase 3 Incremental Approach:**
   
   1. Run `python ReusableTools/IPA_ClientHandover/build_configuration_analysis.py`
   2. Script extracts configuration by category:
      - Process variables (START activity with _configuration references)
      - File channels (ACCFIL activities)
      - Web services (WEBRN activities)
      - Security roles
      - Config dependencies
   3. Saves chunks: `config_chunk_process_variables.json`, etc.
   4. AI analyzes each chunk (~1-2 KB output per category)
   5. AI saves as `config_chunk_CATEGORY_analyzed.json`
   6. Run `python ReusableTools/IPA_ClientHandover/build_configuration_analysis.py merge`
   7. Output: Complete `configuration_analysis.json`
   
   **AI Analysis Task (per chunk):**
   ```json
   {
     "analysis": [
       {
         "variable": "vTestFlag",
         "purpose": "Controls test mode routing",
         "example_value": "true/false",
         "modification_instructions": "Set to false in production"
       }
     ]
   }
   ```
   
   **Phase 3 Final Output Structure:**
   ```json
   {
     "file_channel_config": [...],
     "process_variables": [...],
     "configuration_dependencies": [...]
   }
   ```

6. **Phase 4: Risk & Compliance Review** (AI - Incremental)
   - **Script**: `ReusableTools/IPA_ClientHandover/build_risk_assessment.py`
   - Input: Previous analysis outputs (business, workflow, configuration, metrics)
   - Task: Analyze risks by category (3-5 key risks per category)
   - **CRITICAL**: Keep output small - focus on key risks only
   - Output: `risk_assessment.json`
   - Return: "Phase 4 complete. risk_assessment.json written."
   
   **Phase 4 Incremental Approach:**
   
   1. Run `python ReusableTools/IPA_ClientHandover/build_risk_assessment.py`
   2. Script loads previous analysis outputs and extracts risk context
   3. Creates 5 risk chunks by category:
      - Technical risks (integration failures, data quality)
      - Maintenance risks (configuration drift, documentation)
      - Scalability concerns (performance, volume)
      - Compliance requirements (audit trail, authorization)
      - Data quality risks (validation, completeness)
   4. Saves chunks: `risk_chunk_technical_risks.json`, etc.
   5. AI analyzes each chunk (~1-2 KB output, 3-5 risks max)
   6. AI saves as `risk_chunk_CATEGORY_analyzed.json`
   7. Run `python ReusableTools/IPA_ClientHandover/build_risk_assessment.py merge`
   8. Output: Complete `risk_assessment.json`
   
   **AI Analysis Task (per chunk - KEEP SMALL):**
   ```json
   {
     "risks": [
       {
         "risk": "Hyland OnBase interface failures",
         "severity": "Critical",
         "impact": "Invoices not received for approval",
         "mitigation": "Implement monitoring and retry logic",
         "monitoring": "Real-time interface health checks"
       }
     ]
   }
   ```
   
   **CRITICAL**: Return only 3-5 key risks per category, not exhaustive lists.

7. **Phase 4.5: Executive Summary Diagram** (AI - Multi-Process Only)
   - **WHEN**: Only for RICE items with 2+ processes
   - **WHY**: Executive summary diagram requires understanding cross-process interactions
   - Input: `metrics_summary.json` (process names, counts, types), `business_analysis.json` (RICE purpose)
   - Task: Create high-level RICE workflow showing how processes interact
   - Output: `executive_diagram.json` with diagram structure
   - Return: "Phase 4.5 complete. executive_diagram.json written."
   
   **Phase 4.5 Approach:**
   ```python
   # Check process count from metrics_summary.json
   if process_count == 1:
       # Skip Phase 4.5, use individual process diagram
       pass
   else:
       # Generate cross-process interaction diagram
       # Example: Main Process → Reject Handler → Nightly Trigger
       # Focus on: triggers, data flow, error handling
   ```
   
   **Phase 4.5 Required Output:**
   ```json
   {
     "diagram_type": "multi_process_interaction",
     "processes": [
       {"name": "Main", "role": "Primary workflow", "triggers": ["Manual", "API"]},
       {"name": "Reject", "role": "Error handler", "triggers": ["Main process failure"]},
       {"name": "Nightly", "role": "Scheduler", "triggers": ["Timer"]}
     ],
     "interactions": [
       {"from": "Main", "to": "Reject", "condition": "Validation failure"},
       {"from": "Nightly", "to": "Main", "condition": "Daily 2 AM"}
     ]
   }
   ```

8. **Phase 5: Report Assembly** (Python Only - No AI)
   - Merge: All JSON outputs
   - Transform: Use specialized transformation functions
     - `transform_requirements()` - Adds IDs, categories, priorities, stakeholders
     - `transform_production_validation()` - Creates real test results from WU logs
     - `generate_key_features()` - Extracts features from integrations
   - Populate: Client handover template with transformed data
   - Generate: Final Excel report
   - Save to: `Client_Handover_Results/`

**Key Benefits:**

- ✅ No context accumulation (each phase isolated at ~10 KB)
- ✅ No crashes (stable execution regardless of file size)
- ✅ Faster execution (reduced reasoning overhead)
- ✅ Enterprise-grade quality maintained
- ✅ Clear separation: AI analyzes, Python processes
- ✅ Enhanced data quality with transformation functions

## Transformation Functions

**NEW**: Phase 5 now uses specialized transformation functions to enhance data quality:

### 1. transform_requirements()

Transforms raw requirements into structured format with:

- Sequential IDs (BR-001, BR-002, etc.)
- Categories and priorities
- Source attribution (ANA-050 sections)
- Stakeholder assignments
- Business value statements

**Result**: Professional requirements with full traceability

### 2. transform_production_validation()

Creates production validation from work unit logs with:

- Real execution metrics (duration, record count)
- Test results with actual values
- Performance ratings (Excellent, Good, Acceptable)
- Error counts and status
- SFTP operation counts

**Result**: Evidence-based production readiness assessment

### 3. generate_key_features()

Extracts key features from business analysis:

- Integration touchpoints
- Business objectives
- System capabilities
- Client-friendly bullet format

**Result**: At-a-glance feature summary (max 8 items)

**Location**: All functions in `ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py`

**Documentation**: See `.kiro/steering/10_IPA_Report_Generation.md` for detailed specifications

## Python Tools

This skill uses the following Python tools from `ReusableTools/IPA_ClientHandover/`:

**Phase 0 (Preprocessing):**

- `preprocess_client_handover.py` - Extracts and structures data for analysis phases

**Phase 2 (Workflow Analysis - Incremental):**

- `build_workflow_analysis.py` - Chunks activities, orchestrates AI analysis, merges results

**Phase 3 (Configuration Analysis - Incremental):**

- `build_configuration_analysis.py` - Extracts config by category, orchestrates AI analysis, merges results

**Phase 4 (Risk Assessment - Incremental):**

- `build_risk_assessment.py` - Chunks risks by category, orchestrates AI analysis, merges results

**Phase 5 (Report Assembly):**

- `assemble_client_handover_report.py` - Merges JSON outputs and generates Excel report

**Pipeline Orchestration:**

- `run_incremental_pipeline.py` - Master orchestrator for all phases

**Validation & Testing:**

- `validate_analysis_jsons.py` - Validates JSON structure before assembly
- `test_end_to_end.py` - End-to-end integration test

**Documentation:**

- `JSON_SCHEMAS.md` - Complete JSON schema documentation
- `TROUBLESHOOTING.md` - Common issues and solutions
- `INCREMENTAL_PIPELINE_GUIDE.md` - Incremental architecture guide
- `README.md` - Quick start guide

**Legacy Tools (Deprecated):**

- `organize_by_sections.py` - Replaced by `preprocess_client_handover.py`
- `merge_documentation.py` - Replaced by `assemble_client_handover_report.py`
- `consolidate_processes.py` - Integrated into `assemble_client_handover_report.py`
- `generate_client_handover_report.py` - Replaced by `assemble_client_handover_report.py`

Template: `ipa_client_handover_template.py` (workspace root)

## Subagents Used

**DEPRECATED**: This skill no longer uses subagents. It uses a stateless pipeline architecture instead.

**Legacy Subagents (No Longer Used):**

- `ipa-business-requirements-analyzer` - Replaced by Phase 1 direct analysis
- `ipa-workflow-analyzer` - Replaced by Phase 2 direct analysis
- `ipa-configuration-analyzer` - Replaced by Phase 3 direct analysis
- `ipa-activity-guide-generator` - Replaced by Phase 4 direct analysis
- `ipa-validation-analyzer` - Replaced by Phase 5 direct analysis

**New Architecture**: Each phase executes directly with clean context, reading only required JSON files and producing structured output.

## Performance

**Incremental Pipeline (Current Architecture):**

- Phase 0 (Preprocessing): ~2-3s per file
- Phase 1 (Business Analysis): ~30-45s (direct AI analysis)
- Phase 2 (Workflow Analysis): ~5-10 min (11 chunks × 30s each + merge)
- Phase 3 (Configuration Analysis): ~2-5 min (5 chunks × 30s each + merge)
- Phase 4 (Risk Analysis): ~2-5 min (5 chunks × 30s each + merge)
- Phase 5 (Report Assembly): ~5-10s
- **Total**: ~10-15 min per RICE item (stable, no crashes)

**Key Improvements:**
- ✅ No AI output >3 KB (was 11 KB causing crashes)
- ✅ No context accumulation (each chunk isolated)
- ✅ Crash-safe (can resume from any chunk)
- ✅ Scalable (works for 50 or 5,000 activities)

**Legacy Multi-Subagent (Deprecated - Crashed at 530 activities):**

- Extraction: ~1s per file
- Organization: ~2s per process
- AI analysis (5 subagents sequential): ~2-3 min per process
- Consolidation: ~2s
- Report generation: <10s
- **Issue**: Crashed at Phase 4 due to 11 KB output attempt
- **Total**: ~2-3 min per process + consolidation
- **Issue**: Crashed at 80 KB context accumulation

## Output

Excel report saved to: `Client_Handover_Results/<Client>_<RICE>_ClientHandover_<timestamp>.xlsx`

## Example Usage

```text
/ipa-client-handover
```

Then follow the interactive prompts to:

1. Select client (e.g., "FPI")
2. Select RICE item (e.g., "MatchReport")
3. Select LPD file(s) (e.g., "MatchReport_Outbound.lpd")
4. Confirm spec and WU log files
5. Confirm report generation

## Architecture Notes

### Stateless Pipeline Design (NEW)

**Problem**: Multi-subagent sequential execution caused context accumulation crashes at 80 KB.

**Solution**: File-based stateless pipeline

- **Phase 0 (Python)**: Deterministic preprocessing, no AI reasoning
- **Phases 1-4 (AI)**: Independent analysis phases, each reads JSON input and writes JSON output
- **Phase 5 (Python)**: Deterministic report assembly, no AI reasoning

**Key Principles:**

1. **Intelligence from focused analysis, not cumulative memory**
2. **Each phase operates in isolation** (~10 KB context)
3. **File-based state transfer** (JSON files replace conversational memory)
4. **Minimal AI output** ("Phase N complete. file.json written.")
5. **No context accumulation** (stable execution regardless of file size)

### Multi-Process Support

**Client Perspective**: One RICE item = One handover document

- Client doesn't care how many IPAs we created internally
- They care about the RICE deliverable as a whole

**Backward Compatibility**:

- Single LPD: Works exactly as before
- Multiple LPDs: Consolidated into ONE report

### Role Separation

- **Python**: Extract data, parse files, structure raw data, format reports, perform calculations
- **AI (Kiro)**: Assess code quality, identify issues, make recommendations, score quality metrics, determine severity

## Critical Rules

1. **ONE REPORT PER RICE ITEM**
   - N LPDs → ONE report
   - Each process gets its own sheet: Process_<ProcessName>
   - Executive summary consolidates across all processes

2. **STATELESS PHASE EXECUTION** (NEW)
   - Each phase reads ONLY required JSON files
   - Each phase writes ONLY one JSON output
   - Each phase returns minimal confirmation
   - No context accumulation across phases

3. **CLIENT-FACING LANGUAGE ONLY**
   - NO code criticism or technical details
   - Focus on WHAT and WHY, not HOW
   - Use business language, not technical jargon
   - Explain how to maintain, not how to fix

4. **PYTHON LIFTS HEAVY LOAD**
   - Python: Extract, organize, merge, format
   - AI: Analyze sections, create documentation
   - Python does NOT make judgments

5. **GRACEFUL DEGRADATION**
   - If no spec: Infer requirements from LPD
   - If no WU log: Note validation not available
   - Report still generates with available data

6. **NO SUBAGENT CHAINING** (NEW)
   - Do NOT use multi-subagent sequential execution
   - Do NOT pass reasoning traces between phases
   - Do NOT store large outputs in conversation memory
   - Use file-based state transfer exclusively

## Related Documentation

- `.kiro/steering/00_Workflow_Engineering_Principles.md` - Stateless pipeline architecture
- `.kiro/steering/01_IPA_and_IPD_Complete_Guide.md` - IPA concepts and patterns
- `.kiro/steering/10_IPA_Report_Generation.md` - Report generation guidelines
- `.kiro/steering/11_RICE_Methodology_and_Specifications.md` - RICE methodology
- `.kiro/skills/ipa-client-handover/` - Skill implementation (active)
- `ReusableTools/IPA_ClientHandover/JSON_SCHEMAS.md` - JSON structure reference
- `ReusableTools/IPA_ClientHandover/TROUBLESHOOTING.md` - Issue resolution guide

## Troubleshooting

### Quick Diagnosis

```bash
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

### Common Issues

**"Process Count: 0"** → Phase 0 was skipped, run preprocessing first

**"File not found: wu_log_data.json"** → Phase 0 outputs `wu_log_data.json` (not `wu_log.json`). If you see this error, the preprocessing script needs to be updated.

**"Config variables: 0" or missing file channel/process variables"** → Phase 3 `configuration_analysis.json` is missing required data structures. Phase 3 MUST extract:
- `file_channel_config` - File channel variables (FileChannelFileName, FileChannelMonitorDirectory, etc.)
- `process_variables` - START activity variables (OauthCreds, OutputFileName, RunDate, etc.)
- `configuration_dependencies` - System Configuration variables (Interface.API_AuthCred_*, etc.)

**ROOT CAUSE**: The assembly script `build_ipa_data()` function expects these specific keys in `configuration_analysis.json`. If Phase 3 doesn't generate them, the System Configuration sheet will be empty.

**"Production Validation showing N/A"** → Work unit log file not found or `wu_log_data.json` missing. Verify Phase 0 extracted WU log successfully.

**"Invalid client_name"** → Use positional args, not `--client`

**"AttributeError"** → Data structure mismatch, update assembly script

**Empty sheets** → Analysis JSONs incomplete, validate structure

See `TROUBLESHOOTING.md` for complete guide.

## Reference Documentation

Comprehensive documentation is available in the `references/` folder:

### Core Guides

- **`WORKFLOW_GUIDE.md`** - Complete step-by-step workflow for generating client handover documentation
  - Prerequisites and file organization
  - Phase-by-phase instructions (Phases 0-5)
  - Multi-process workflow
  - Validation and troubleshooting
  - Quick reference table

- **`PHASE3_CONFIGURATION_GUIDE.md`** - Critical Phase 3 requirements and extraction patterns
  - Required data structures (`file_channel_config`, `process_variables`, `configuration_dependencies`)
  - Root cause analysis for empty configuration sheets
  - Extraction patterns with code examples
  - Validation commands
  - Common mistakes and best practices

- **`JSON_SCHEMAS.md`** - Complete JSON structure reference for all phases
  - Phase 0 outputs (lpd_structure, metrics_summary, spec_raw)
  - Phase 1-4 analysis JSON schemas
  - Required fields and validation rules
  - Assembly script behavior
  - Graceful degradation patterns

- **`TROUBLESHOOTING.md`** - Common issues and solutions
  - Quick diagnosis commands
  - Root cause analysis
  - Step-by-step fixes
  - Prevention strategies

- **`COMMON_ISSUES.md`** - Catalog of known issues and fixes (NEW)
  - Excel file corruption and sheet name limits
  - Template rendering issues (priority colors, missing data)
  - Data structure mismatches
  - Performance and context issues
  - Best practices and prevention strategies

- **`IPA_DOMAIN_KNOWLEDGE.md`** - IPA concepts for client documentation (NEW)
  - Activity type descriptions in business-friendly language
  - Common process patterns (approval, interface, integration)
  - Data access patterns (Compass API vs Landmark)
  - ANA-050 specification structure
  - Business requirements extraction patterns

- **`TOOLS_README.md`** - Python tool usage and examples
  - Tool descriptions and parameters
  - Command-line examples
  - Integration with workflow
  - Testing and validation

### When to Use Each Guide

- **Starting a new handover?** → Read `WORKFLOW_GUIDE.md` first
- **Phase 3 configuration issues?** → See `PHASE3_CONFIGURATION_GUIDE.md`
- **JSON structure questions?** → Check `JSON_SCHEMAS.md`
- **Report generation problems?** → Consult `TROUBLESHOOTING.md`
- **Known issues or errors?** → Check `COMMON_ISSUES.md` first
- **Tool usage questions?** → Reference `TOOLS_README.md`
- **IPA concepts and patterns?** → See `IPA_DOMAIN_KNOWLEDGE.md`

### Loading Reference Documentation

Reference files are loaded on-demand when needed. The skill is self-contained and portable - all necessary information is included in this skill package.

## Confidentiality

Client-facing documentation. Do not reference other clients or internal implementation details.
