# IPA Client Handover Documentation Tools

Tools for generating comprehensive client-facing IPA documentation.

## Overview

The client handover workflow uses specialized subagents to analyze different aspects of an IPA process and generate comprehensive documentation.

## Workflow

### Step 1: Extract Data (Python)

```bash
# Extract LPD data
python -c "from ReusableTools.IPA_Analyzer.extract_lpd_data import extract_lpd_data; extract_lpd_data(['path/to/process.lpd'], 'Temp/ProcessName_lpd_data.json')"

# Extract spec data (if available)
python -c "from ReusableTools.IPA_Analyzer.extract_spec import extract_spec; extract_spec('path/to/ANA-050.docx', 'Temp/ProcessName_spec_data.json')"

# Extract WU log data (if available)
python -c "from ReusableTools.IPA_Analyzer.extract_wu_log import extract_wu_log; extract_wu_log('path/to/log.txt', 'Temp/ProcessName_wu_data.json')"
```

### Step 2: Organize by Sections (Python)

```bash
python ReusableTools/IPA_ClientHandover/organize_by_sections.py \
    Temp/ProcessName_lpd_data.json \
    Temp/ProcessName_spec_data.json \
    Temp/ProcessName_wu_data.json \
    Temp/ProcessName
```

Creates 5 section files:
- `Temp/ProcessName_section_business.json`
- `Temp/ProcessName_section_workflow.json`
- `Temp/ProcessName_section_configuration.json`
- `Temp/ProcessName_section_activities.json`
- `Temp/ProcessName_section_validation.json`

### Step 3: Launch Section Analyzers (Parallel Subagents)

Launch 5 specialized subagents in parallel:

```python
# Business Requirements
invokeSubAgent(
    name="ipa-business-requirements-analyzer",
    prompt="Read spec and section data, extract business requirements, save to 'Temp/ProcessName_doc_business.json'",
    explanation="Analyzing business requirements"
)

# Workflow
invokeSubAgent(
    name="ipa-workflow-analyzer",
    prompt="Read section data, map workflow and approval paths, save to 'Temp/ProcessName_doc_workflow.json'",
    explanation="Analyzing workflow"
)

# Configuration
invokeSubAgent(
    name="ipa-configuration-analyzer",
    prompt="Read LPD and section data, extract configuration variables, save to 'Temp/ProcessName_doc_configuration.json'",
    explanation="Analyzing configuration"
)

# Activities
invokeSubAgent(
    name="ipa-activity-guide-generator",
    prompt="Read section data, create activity reference, save to 'Temp/ProcessName_doc_activities.json'",
    explanation="Generating activity guide"
)

# Validation
invokeSubAgent(
    name="ipa-validation-analyzer",
    prompt="Read section data, analyze work unit logs, save to 'Temp/ProcessName_doc_validation.json'",
    explanation="Analyzing validation data"
)
```

### Step 4: Generate Report (Python Helper Script)

```bash
python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py <process_name> <client_name> <rice_item>
```

Example:
```bash
python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py MatchReport_Outbound FPI MatchReport
```

## Subagents

### ipa-business-requirements-analyzer
- Extracts business requirements from ANA-050 functional specification
- Documents objectives, stakeholders, scope, and success metrics
- Uses fsWrite to save JSON files directly

### ipa-workflow-analyzer
- Maps process workflow and approval paths
- Documents decision points and integrations
- Creates visual workflow steps
- Uses fsWrite to save JSON files directly

### ipa-configuration-analyzer
- Extracts configuration variables from LPD Start node
- Documents how to modify each setting
- Categorizes variables (System Configuration, Process Variables, File Channel)
- Uses fsWrite to save JSON files directly

### ipa-activity-guide-generator
- Creates activity reference documentation in business terms
- Documents when/why activities run and what they do
- Provides maintenance guidance
- Groups related activities
- Uses fsWrite to save JSON files directly

### ipa-validation-analyzer
- Analyzes work unit logs for production validation
- Documents test summary, performance metrics, and production readiness
- Provides evidence of successful execution
- Uses fsWrite to save JSON files directly

## Important Notes

### Subagent File Writing

All client handover subagents use `fsWrite` directly to save their output files:
- **Why**: Subagents should be self-contained and use their own tools
- **Solution**: Subagents have `tools: ["read", "fsWrite"]` and save files directly
- **Large Files**: Hook prompts instruct subagents to use chunked writes (fsWrite + fsAppend) for files >1000 lines
- **Impact**: Clean architecture, no nested subagent dependencies

### Report Generation Helper

The `generate_client_handover_report.py` script:
- Automatically loads all 5 subagent outputs
- Builds the correct ipa_data structure for the template
- Handles errors gracefully with clear messages
- Eliminates manual data structure building

## Output

Generates comprehensive Excel report with 6 sheets:
1. **Executive Summary** - Overview, objectives, production validation summary
2. **Business Requirements** - Requirements, objectives, stakeholders, scope
3. **Workflow & Approvals** - Workflow steps, decision points, integrations
4. **System Configuration** - Configuration variables with modification instructions
5. **Activity Reference** - Activity guide with business-friendly descriptions
6. **Production Validation** - Test summary, performance metrics, production readiness

## Troubleshooting

### Subagent Output Incomplete

If a subagent output file is incomplete (e.g., only 6/38 activities):
- **Root Cause**: fsWrite failed due to context size in long session
- **Solution**: Subagents now use file-writer-helper automatically
- **Verification**: Check file size - should be >10KB for large processes

### Report Has No Data

If the generated report has only headers but no data:
- **Root Cause**: Wrong data structure passed to template
- **Solution**: Use `generate_client_handover_report.py` helper script
- **Verification**: Check that all 5 `_doc_*.json` files exist and are complete

### Missing Files Error

If helper script reports missing files:
- **Root Cause**: Subagents didn't complete or files were deleted
- **Solution**: Re-run subagent analysis (Steps 2-3)
- **Verification**: Check that all 5 section files and 5 doc files exist

## Related Files

- `organize_by_sections.py` - Organizes extracted data by documentation sections
- `merge_documentation.py` - Merges subagent outputs into master documentation
- `generate_client_handover_report.py` - Generates Excel report from subagent outputs
- `ipa_client_handover_template_v2.py` (workspace root) - Excel report template
