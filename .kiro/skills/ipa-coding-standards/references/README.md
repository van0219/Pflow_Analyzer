# IPA Coding Standards Reference Documentation

This folder contains comprehensive reference documentation for the IPA Coding Standards skill.

## Quick Navigation

### 🚀 Getting Started

**New to coding standards analysis?**

Start here: [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md)

This guide provides complete step-by-step instructions from file organization through report generation.

### 📚 Documentation Index

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** | Complete workflow from start to finish | Starting a new analysis project |
| **[DOMAIN_ANALYSIS_GUIDE.md](DOMAIN_ANALYSIS_GUIDE.md)** | Domain-specific analysis patterns | Understanding domain requirements |
| **[JSON_SCHEMAS.md](JSON_SCHEMAS.md)** | Complete JSON structure reference | Understanding data structures or validation errors |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues and solutions | Report generation problems or errors |
| **[COMMON_ISSUES.md](COMMON_ISSUES.md)** | Catalog of known issues and fixes | Encountering errors or unexpected behavior |
| **[CODING_STANDARDS_REFERENCE.md](CODING_STANDARDS_REFERENCE.md)** | Coding standards rules reference | Understanding specific rules and violations |
| **[TOOLS_README.md](TOOLS_README.md)** | Python tool usage and examples | Tool command-line usage questions |

### 🎯 Common Scenarios

**Scenario 1: First Time Analyzing Coding Standards**

1. Read [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) - Complete workflow
2. Organize files as described in Step 1
3. Follow Phases 0-6 sequentially
4. Validate report using Step 9

**Scenario 2: Understanding Domain Analysis**

1. Check [`DOMAIN_ANALYSIS_GUIDE.md`](DOMAIN_ANALYSIS_GUIDE.md) - Domain patterns
2. Review specific domain requirements
3. Understand what AI should analyze
4. See code examples and patterns

**Scenario 3: Report Shows "No Violations Found"**

1. Check [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - "No violations found" section
2. Verify Phase 0 loaded project standards correctly
3. Check `project_standards.json` exists and is valid
4. Re-run Phase 0 if needed

**Scenario 4: JSON Structure Validation Errors**

1. Check [`JSON_SCHEMAS.md`](JSON_SCHEMAS.md) - Schema reference
2. Compare your JSON structure to expected format
3. Fix structure issues
4. Re-run validation script

**Scenario 5: Understanding Specific Rule**

1. Check [`CODING_STANDARDS_REFERENCE.md`](CODING_STANDARDS_REFERENCE.md) - Rules reference
2. Find the specific rule (e.g., Rule 1.1.1)
3. Review rule description and examples
4. Understand severity and recommendations

### 📖 Document Summaries

#### WORKFLOW_GUIDE.md

**What it covers:**
- Prerequisites and file organization
- Phase 0: Preprocessing (mandatory first step)
- Phase 1: Naming Analysis
- Phase 2: JavaScript Analysis
- Phase 3: SQL Analysis
- Phase 4: Error Handling Analysis
- Phase 5: Structure Analysis
- Phase 6: Report Assembly
- Validation and troubleshooting
- Quick reference table

**Key sections:**
- Complete Workflow (Steps 1-9)
- Troubleshooting
- Quick Reference

#### DOMAIN_ANALYSIS_GUIDE.md

**What it covers:**
- Domain 1: Naming conventions
- Domain 2: JavaScript ES5 compliance
- Domain 3: SQL queries
- Domain 4: Error handling
- Domain 5: Process structure
- Analysis patterns for each domain
- Code examples and violations
- Project standards integration

**Key sections:**
- Domain Definitions
- Analysis Patterns
- Code Examples
- Project Standards Override

#### JSON_SCHEMAS.md

**What it covers:**
- Phase 0 outputs (lpd_structure, metrics_summary, project_standards)
- Phase 1-5 analysis JSON schemas
- Required fields and validation rules
- Assembly script behavior
- Best practices

**Key sections:**
- Phase 0 Outputs
- Phase 1-5 Outputs (with RECOMMENDED structures)
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
- Common Issues (Process Count: 0, No violations found, etc.)
- Validation Commands
- Prevention Strategies

#### COMMON_ISSUES.md

**What it covers:**
- Excel file corruption and sheet name limits
- Template rendering issues
- Data structure mismatches
- Performance and context issues
- Best practices and prevention strategies

**Key sections:**
- Known Issues Catalog
- Root Cause Analysis
- Prevention Strategies
- Best Practices

#### CODING_STANDARDS_REFERENCE.md

**What it covers:**
- Complete coding standards rules (1.1.1 - 1.5.2)
- Rule descriptions and rationale
- Severity levels
- Code examples (compliant vs non-compliant)
- Recommendations

**Key sections:**
- Naming Standards (1.1.x)
- JavaScript Standards (1.2.x)
- Error Handling Standards (1.3.x)
- Configuration Standards (1.4.x)
- SQL Standards (1.5.x)

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
- **"Phase 1"** - Naming analysis
- **"Phase 2"** - JavaScript analysis
- **"Phase 3"** - SQL analysis
- **"Phase 4"** - Error handling analysis
- **"Phase 5"** - Structure analysis
- **"project_standards"** - Project standards integration
- **"validation"** - Validation commands and checks
- **"troubleshooting"** - Problem-solving guidance

### 📝 Contributing

These reference documents are maintained as part of the ipa-coding-standards skill. Updates should:

1. Maintain consistency across all documents
2. Include practical examples
3. Reference related sections in other documents
4. Follow markdown best practices
5. Keep content focused and actionable

### 🔗 Related Resources

**External Documentation:**
- Python tools: `ReusableTools/IPA_CodingStandards/`
- Templates: `ReusableTools/IPA_CodingStandards/ipa_coding_standards_template_enhanced.py`
- Validation scripts: `ReusableTools/IPA_CodingStandards/validate_*.py`

**Skill Documentation:**
- Main skill file: `../SKILL.md`
- Scripts folder: `../scripts/`

### 📅 Last Updated

March 8, 2026

---

**Need help?** Start with [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) for the complete workflow, or jump to the specific guide that matches your current task.
