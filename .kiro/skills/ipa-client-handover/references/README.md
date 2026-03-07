# IPA Client Handover Reference Documentation

This folder contains comprehensive reference documentation for the IPA Client Handover skill.

## Quick Navigation

### 🚀 Getting Started

**New to client handover generation?**

Start here: [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md)

This guide provides complete step-by-step instructions from file organization through report generation.

### 📚 Documentation Index

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** | Complete workflow from start to finish | Starting a new handover project |
| **[PHASE3_CONFIGURATION_GUIDE.md](PHASE3_CONFIGURATION_GUIDE.md)** | Critical Phase 3 requirements | Configuration sheet is empty or incomplete |
| **[JSON_SCHEMAS.md](JSON_SCHEMAS.md)** | Complete JSON structure reference | Understanding data structures or validation errors |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues and solutions | Report generation problems or errors |
| **[TOOLS_README.md](TOOLS_README.md)** | Python tool usage and examples | Tool command-line usage questions |

### 🎯 Common Scenarios

**Scenario 1: First Time Generating Client Handover**

1. Read [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) - Complete workflow
2. Organize files as described in Step 1
3. Follow Phases 0-5 sequentially
4. Validate report using Step 9

**Scenario 2: System Configuration Sheet is Empty**

1. Check [`PHASE3_CONFIGURATION_GUIDE.md`](PHASE3_CONFIGURATION_GUIDE.md) - Root cause analysis
2. Verify Phase 3 output has required structures
3. Re-run Phase 3 with correct extraction patterns
4. Validate before Phase 5

**Scenario 3: Report Shows "Process Count: 0"**

1. Check [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - "Process Count: 0" section
2. Verify Phase 0 was run (not manual extraction)
3. Check `lpd_structure.json` and `metrics_summary.json` exist
4. Re-run Phase 0 if needed

**Scenario 4: JSON Structure Validation Errors**

1. Check [`JSON_SCHEMAS.md`](JSON_SCHEMAS.md) - Schema reference
2. Compare your JSON structure to expected format
3. Fix structure issues
4. Re-run validation script

**Scenario 5: Understanding Tool Parameters**

1. Check [`TOOLS_README.md`](TOOLS_README.md) - Tool documentation
2. Find the specific tool you're using
3. Review parameters and examples
4. Run tool with correct arguments

### 📖 Document Summaries

#### WORKFLOW_GUIDE.md

**What it covers:**
- Prerequisites and file organization
- Phase 0: Preprocessing (mandatory first step)
- Phase 1: Business Requirements Analysis
- Phase 2: Workflow Architecture Analysis
- Phase 3: Configuration & Technical Components
- Phase 4: Risk & Compliance Review
- Phase 5: Report Assembly
- Validation and troubleshooting
- Multi-process workflow
- Quick reference table

**Key sections:**
- Complete Workflow (Steps 1-9)
- Multi-Process Workflow
- Troubleshooting
- Quick Reference

#### PHASE3_CONFIGURATION_GUIDE.md

**What it covers:**
- Critical Phase 3 requirements
- Required data structures (file_channel_config, process_variables, configuration_dependencies)
- Root cause of empty configuration sheets
- Extraction patterns with code examples
- Validation commands
- Assembly script priority order
- Common mistakes and best practices

**Key sections:**
- Required Data Structures
- Root Cause of Empty Configuration Sheets
- Extraction Patterns
- Validation Before Assembly

#### JSON_SCHEMAS.md

**What it covers:**
- Phase 0 outputs (lpd_structure, metrics_summary, spec_raw, wu_log_data)
- Phase 1-4 analysis JSON schemas
- Required fields and validation rules
- Assembly script behavior
- Graceful degradation patterns
- Best practices

**Key sections:**
- Phase 0 Outputs
- Phase 1-4 Outputs (with RECOMMENDED structures)
- Validation Rules
- Assembly Script Behavior

#### TROUBLESHOOTING.md

**What it covers:**
- Quick diagnosis commands
- Common issues with root cause analysis
- Step-by-step fixes
- Prevention strategies
- Validation commands

**Key sections:**
- Quick Diagnosis
- Common Issues (Process Count: 0, Config variables: 0, etc.)
- Validation Commands
- Prevention Strategies

#### TOOLS_README.md

**What it covers:**
- Python tool descriptions
- Command-line parameters
- Usage examples
- Integration with workflow
- Testing and validation

**Key sections:**
- Tool Descriptions
- Command-Line Examples
- Workflow Integration
- Testing and Validation

### 🔍 Search Tips

**Looking for specific information?**

Use your editor's search function (Ctrl+F or Cmd+F) to search across all reference files:

- **"Phase 0"** - Preprocessing information
- **"Phase 3"** - Configuration analysis
- **"file_channel_config"** - File channel configuration
- **"configuration_dependencies"** - System configuration
- **"activity_descriptions"** - Activity documentation
- **"validation"** - Validation commands and checks
- **"troubleshooting"** - Problem-solving guidance

### 📝 Contributing

These reference documents are maintained as part of the ipa-client-handover skill. Updates should:

1. Maintain consistency across all documents
2. Include practical examples
3. Reference related sections in other documents
4. Follow markdown best practices
5. Keep content focused and actionable

### 🔗 Related Resources

**External Documentation:**
- Python tools: `ReusableTools/IPA_ClientHandover/`
- Template: `ipa_client_handover_template.py` (workspace root)
- Validation scripts: `ReusableTools/IPA_ClientHandover/validate_*.py`

**Skill Documentation:**
- Main skill file: `../SKILL.md`
- Scripts folder: `../scripts/`

### 📅 Last Updated

March 7, 2026

---

**Need help?** Start with [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) for the complete workflow, or jump to the specific guide that matches your current task.
