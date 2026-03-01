# IPA Client Handover Scripts

This directory contains references to the Python tools used by the IPA Client Handover skill.

## Tool Locations

All Python tools are located in the workspace at:

### Data Processing Tools
- `ReusableTools/IPA_ClientHandover/organize_by_sections.py`
- `ReusableTools/IPA_ClientHandover/merge_documentation.py`
- `ReusableTools/IPA_ClientHandover/consolidate_processes.py`
- `ReusableTools/IPA_ClientHandover/generate_client_handover_report.py`

### Data Extraction Tools
- `ReusableTools/IPA_Analyzer/extract_lpd_data.py`
- `ReusableTools/IPA_Analyzer/extract_spec.py`
- `ReusableTools/IPA_Analyzer/extract_wu_log.py`

### Report Template
- `ipa_client_handover_template.py` (workspace root)

## Usage

These tools are invoked automatically by the skill workflow. They are not copied into the skill directory to maintain a single source of truth and avoid duplication.

## Tool Descriptions

### organize_by_sections.py
Splits extracted IPA data into 5 documentation section files for parallel analysis.

**Sections:**
1. Business Requirements - What and why (from functional spec)
2. Workflow - How it flows (from LPD activities)
3. Configuration - What can be changed (from LPD config variables)
4. Activity Guide - Reference documentation (from LPD activities)
5. Validation - Production proof (from WU logs)

**Usage:**
```bash
python ReusableTools/IPA_ClientHandover/organize_by_sections.py <lpd_json> <spec_json> <wu_json> <output_prefix>
```

### merge_documentation.py
Merges 5 analyzed documentation files into a single master documentation file per process.

**Usage:**
```bash
python ReusableTools/IPA_ClientHandover/merge_documentation.py <output_prefix>
```

### consolidate_processes.py
Consolidates multiple process documentation files into a single RICE-level documentation file.

**Usage:**
```bash
python ReusableTools/IPA_ClientHandover/consolidate_processes.py <rice_item> <process_name1> [<process_name2> ...]
```

### generate_client_handover_report.py
Automatically loads consolidated documentation and generates the client handover Excel report.

**Usage:**
```bash
python ReusableTools/IPA_ClientHandover/generate_client_handover_report.py <rice_item> <client_name> <rice_item>
```

## Subagents

The skill uses these specialized subagents (located in `.kiro/agents/`):

- `ipa-business-requirements-analyzer` - Extracts business requirements from specs
- `ipa-workflow-analyzer` - Maps process workflows and approval paths
- `ipa-configuration-analyzer` - Documents configuration with modification instructions
- `ipa-activity-guide-generator` - Creates activity reference documentation
- `ipa-validation-analyzer` - Analyzes production validation from WU logs

## Architecture

The skill follows a section-segmented architecture:

1. **Python extracts** data from source files (LPD, spec, WU log)
2. **Python organizes** data into 5 documentation sections
3. **AI subagents analyze** each section sequentially (prevents resource exhaustion)
4. **Python merges** analyzed sections into master documentation per process
5. **Python consolidates** multiple processes into RICE-level documentation
6. **Python generates** final Excel report using template

This architecture ensures:
- Scalability to any IPA size
- Reliable sequential execution
- Clear separation of concerns (Python = data, AI = analysis)
- Production-grade quality (extracts truth, not AI-generated content)
