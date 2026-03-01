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

1. **User Selection** (Interactive)
   - Select client from Projects/ directory
   - Select RICE item
   - Select one or more LPD files (multi-select)
   - Confirm spec and WU log availability

2. **Data Extraction** (Python)
   - Extract data from LPD files
   - Extract business requirements from spec (if available)
   - Extract validation data from WU logs (if available)

3. **Section Organization** (Python)
   - Organize data into 5 documentation sections
   - Create section files for analysis

4. **Section Analysis** (AI Subagents - Sequential)
   - Business Requirements Analyzer
   - Workflow Analyzer
   - Configuration Analyzer
   - Activity Guide Generator
   - Validation Analyzer

5. **Documentation Merge** (Python)
   - Merge analyzed sections per process
   - Consolidate multiple processes (if applicable)

6. **Report Generation** (Python + Template)
   - Generate comprehensive Excel report
   - Save to Client_Handover_Results/

## Python Tools

This skill uses the following Python tools from `ReusableTools/IPA_ClientHandover/`:

- `organize_by_sections.py` - Splits data into 5 documentation sections
- `merge_documentation.py` - Merges analyzed sections per process
- `consolidate_processes.py` - Consolidates multiple processes into RICE-level doc
- `generate_client_handover_report.py` - Generates final Excel report

Template: `ipa_client_handover_template.py` (workspace root)

## Subagents Used

- `ipa-business-requirements-analyzer` - Extracts business requirements from specs
- `ipa-workflow-analyzer` - Maps process workflows and approval paths
- `ipa-configuration-analyzer` - Documents configuration with modification instructions
- `ipa-activity-guide-generator` - Creates activity reference documentation
- `ipa-validation-analyzer` - Analyzes production validation from WU logs

## Performance

- Extraction: ~1s per file
- Organization: ~2s per process
- AI analysis (5 subagents sequential): ~2-3 min per process
- Consolidation: ~2s
- Report generation: <10s
- **Total**: ~2-3 min per process + consolidation

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

### Section-Segmented Design

**Problem**: Large LPD files with complex workflows overwhelm single-pass analysis.

**Solution**: Multi-pass documentation generation

- Python extracts and organizes data by documentation sections (5 sections)
- AI analyzes each section with specialized subagents (SEQUENTIAL for reliability)
- Python merges results into master documentation
- ONE Excel report generated PER RICE ITEM (not per LPD)

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

2. **SEQUENTIAL SUBAGENT EXECUTION**
   - Launch 5 specialized subagents ONE AT A TIME
   - Sequential execution prevents resource exhaustion
   - Each subagent completes before next one starts

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

## Related Documentation

- `.kiro/steering/01_IPA_and_IPD_Complete_Guide.md` - IPA concepts and patterns
- `.kiro/steering/10_IPA_Report_Generation.md` - Report generation guidelines
- `.kiro/steering/11_RICE_Methodology_and_Specifications.md` - RICE methodology
- `.kiro/hooks/ipa-client-handover.kiro.hook` - Original hook implementation

## Confidentiality

Client-facing documentation. Do not reference other clients or internal implementation details.
