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

4. **Phase 2: Workflow Architecture Analysis** (AI)
   - Input: `lpd_structure.json`
   - Task: Identify process branches, decision nodes, transformations, external calls
   - Output: `workflow_analysis.json`
   - Return: "Phase 2 complete. workflow_analysis.json written."

5. **Phase 3: Configuration & Technical Components** (AI)
   - Input: `lpd_structure.json`, `metrics_summary.json`
   - Task: Identify file channels, web services, security roles, configuration dependencies
   - Output: `configuration_analysis.json`
   - Return: "Phase 3 complete. configuration_analysis.json written."

6. **Phase 4: Risk & Compliance Review** (AI)
   - Input: All prior JSON outputs
   - Task: Identify technical risks, maintenance risks, scalability concerns
   - Output: `risk_assessment.json`
   - Return: "Phase 4 complete. risk_assessment.json written."

7. **Phase 5: Report Assembly** (Python Only - No AI)
   - Merge: All JSON outputs
   - Populate: Client handover template
   - Generate: Final Excel report
   - Save to: `Client_Handover_Results/`

**Key Benefits:**

- ✅ No context accumulation (each phase isolated at ~10 KB)
- ✅ No crashes (stable execution regardless of file size)
- ✅ Faster execution (reduced reasoning overhead)
- ✅ Enterprise-grade quality maintained
- ✅ Clear separation: AI analyzes, Python processes

## Python Tools

This skill uses the following Python tools from `ReusableTools/IPA_ClientHandover/`:

**Phase 0 (Preprocessing):**
- `preprocess_client_handover.py` - Extracts and structures data for analysis phases

**Phase 5 (Report Assembly):**
- `assemble_client_handover_report.py` - Merges JSON outputs and generates Excel report

**Validation & Testing:**
- `validate_analysis_jsons.py` - Validates JSON structure before assembly
- `test_end_to_end.py` - End-to-end integration test

**Documentation:**
- `JSON_SCHEMAS.md` - Complete JSON schema documentation
- `TROUBLESHOOTING.md` - Common issues and solutions
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

**Stateless Pipeline (New Architecture):**

- Phase 0 (Preprocessing): ~2-3s per file
- Phase 1 (Business Analysis): ~30-45s
- Phase 2 (Workflow Analysis): ~30-45s
- Phase 3 (Configuration Analysis): ~30-45s
- Phase 4 (Risk Analysis): ~30-45s
- Phase 5 (Report Assembly): ~5-10s
- **Total**: ~3-4 min per process (stable, no crashes)

**Legacy Multi-Subagent (Deprecated):**
- Extraction: ~1s per file
- Organization: ~2s per process
- AI analysis (5 subagents sequential): ~2-3 min per process
- Consolidation: ~2s
- Report generation: <10s
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
- `.kiro/hooks/ipa-client-handover.kiro.hook` - Hook implementation (if exists)
- `ReusableTools/IPA_ClientHandover/JSON_SCHEMAS.md` - JSON structure reference
- `ReusableTools/IPA_ClientHandover/TROUBLESHOOTING.md` - Issue resolution guide

## Troubleshooting

### Quick Diagnosis
```bash
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

### Common Issues

**"Process Count: 0"** → Phase 0 was skipped, run preprocessing first

**"File not found"** → Missing JSON file, check Phase 0 completed

**"Invalid client_name"** → Use positional args, not `--client`

**"AttributeError"** → Data structure mismatch, update assembly script

**Empty sheets** → Analysis JSONs incomplete, validate structure

See `TROUBLESHOOTING.md` for complete guide.

## Confidentiality

Client-facing documentation. Do not reference other clients or internal implementation details.
