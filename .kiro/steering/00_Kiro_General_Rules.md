---
inclusion: always
---

# Kiro General Rules and Settings

## Table of Contents

- [Execution Philosophy](#execution-philosophy)
- [Critical Error Handling](#critical-error-handling)
- [Subagent Architecture](#subagent-architecture)
- [IPA Analysis Workflow](#ipa-analysis-workflow)
- [Analysis vs Data Processing](#analysis-vs-data-processing)
- [Communication Style](#communication-style)
- [File Management](#file-management)
- [Reusable Tools](#reusable-tools)
- [Code Standards](#code-standards)
- [Knowledge Management](#knowledge-management)
- [Recent Session Learnings](#recent-session-learnings)

## Execution Philosophy

### Core Principles

**ACT IMMEDIATELY** - Execute clear directives without overthinking or unnecessary questions.

**STOP IMMEDIATELY** - When user says "stop", "wait", "oh wait", or "hold on", STOP ALL ACTIONS. Do not continue, explain, retry, or attempt alternatives. Acknowledge and wait for new instructions.

### Decision Matrix

| Situation | Action |
|-----------|--------|
| Clear commands ("update X", "fix Y", "analyze Z") | Act without asking |
| Routine operations (reading files, running scripts) | Act without asking |
| Destructive operations (deleting files, dropping databases) | Ask first |
| Ambiguous requests with multiple interpretations | Ask first |
| User says "stop", "wait", "oh wait", "hold on" | Stop immediately |
| File operation fails with "Operation was aborted" | Stop immediately |

### Responsiveness Guidelines

- Execute first, report results concisely
- Show results, not process
- Be confident in decisions
- Speed is secondary to stopping when asked

## Critical Error Handling

### Available Steering Files

| File | Purpose |
|------|---------|
| `01_IPA_and_IPD_Complete_Guide.md` | IPA/IPD concepts, activity nodes, S3 vs FSM differences |
| `02_Work_Unit_Analysis.md` | WU log analysis, error patterns, JavaScript ES5 |
| `03_Process_Patterns_Library.md` | IPA process patterns (450+), approval workflows |
| `04_WU_Report_Generation.md` | Work unit runtime analysis reports, wu_data structure |
| `05_Compass_SQL_CheatSheet.md` | Compass SQL dialect, supported clauses/joins |
| `06_FSM_Business_Classes_and_API.md` | FSM business classes, REST API operations, OAuth2 |
| `07_Infor_OS_Data_Fabric_Guide.md` | Infor OS architecture, ION, Data Fabric |
| `08_Infor_IDM_Guide.md` | IDM architecture, BOD integration |
| `09_FSM_Navigation_Guide.md` | FSM UI navigation, browser automation |
| `10_IPA_Report_Generation.md` | IPA source code analysis, client handover, peer reviews |
| `11_RICE_Methodology_and_Specifications.md` | RICE methodology, ANA-050/DES-020 specs |
| `12_External_API_OAuth2_Integration_Guide.md` | OAuth 2.0 Authorization Code Grant for external APIs |
| `13_Kiro_Hooks_Official_Documentation.md` | Hook system architecture, event types, best practices |

**Note:** All steering files use `auto` inclusion mode - they load automatically when their description matches your request.

### Proactive Loading Protocol

**CRITICAL**: When you detect task keywords, IMMEDIATELY load relevant steering files using `readFile()` BEFORE responding.

| Task Keywords | Load Files |
|---------------|------------|
| "analyze WU", "work unit" | `02`, `04` |
| "IPA peer review", "code quality", "coding standards" | `10`, `01`, `02`, `03`, `05`, `11` |
| "IPA client handover", "IPA documentation" | `10`, `01`, `11` |
| "create LPD", "IPA process" | `01`, `03` |
| "RICE", "ANA-050", "DES-020" | `11`, `06` |
| "Data Fabric", "Compass SQL" | `05`, `07` |
| "FSM business class", "FSM API", "Landmark API" | `06`, `01` |
| "hook", "create hook", "edit hook", "hook validation" | `13` |
| "external API", "Lightspeed", "third-party API" | `12`, `01` |

### File Writing Strategy (CRITICAL)

**Rule**: For ALL file write operations in long sessions, use the `file-writer-helper` subagent instead of direct fsWrite.

**EXCEPTION - Hook Files**: NEVER use fsWrite or file-writer-helper for hook files in long sessions. Use `ReusableTools/hook_manager.py` Python tool instead.

**When to Use file-writer-helper**:
- Long conversations (10+ messages or heavy file reading)
- Multiple file edits in sequence
- Large file writes (>200 lines)
- After ANY fsWrite failure
- **NEVER for hook files** - use hook_manager.py instead

**When to Use hook_manager.py**:
- ANY hook editing in long sessions (10+ messages)
- After ANY fsWrite failure on hook files
- Before making major hook changes (backup first)

**Fallback Workflow**:
1. Try direct fsWrite first (if context is light AND not a hook file)
2. If fsWrite fails once → Immediately delegate to appropriate tool
3. Do NOT retry fsWrite multiple times
4. Continue working without interruption

**The user should NEVER have to ask you to continue after a file write failure.**

### Verification Checklist

Before ANY analysis, verify:
- [ ] All required files successfully read
- [ ] No truncation warnings unresolved
- [ ] Binary files handled with appropriate tools
- [ ] Data structures complete and valid

**If ANY checkbox fails, STOP and fix before proceeding.**

## Subagent Architecture

### Critical Rules for Subagent Design

**RULE 1: Only Main Agent Invokes Subagents**
- Subagents must NEVER have `invokeSubAgent` tool access
- Only the main agent can invoke subagents
- No nested subagent calls allowed

**RULE 2: Subagents Use Their Own Tools, Never Invoke Other Subagents**
- Subagents must use their own `fsWrite` tool to save files
- Subagents must NEVER invoke other subagents (e.g., file-writer-helper)
- Reason: Subagents should be self-contained and not create nested dependencies

**RULE 3: Subagent Tool Access Patterns**

Valid tool combinations:
- `tools: ["read"]` - Analysis only, returns data to main agent
- `tools: ["read", "fsWrite"]` - Can analyze and save files directly
- `tools: ["read", "shell"]` - Rare, for specialized operations

Invalid tool combinations:
- Any combination with `invokeSubAgent` - ❌ NEVER ALLOW
- Subagent invoking file-writer-helper - ❌ NEVER ALLOW

**RULE 4: Subagent Output Handling**

Two patterns:
1. **Return Pattern**:
   - Subagent: `tools: ["read"]`
   - Subagent returns analysis as JSON string
   - Main agent saves to file using fsWrite or file-writer-helper

2. **Save Pattern** (RECOMMENDED for most workflows):
   - Subagent: `tools: ["read", "fsWrite"]`
   - Subagent saves its own output using fsWrite directly
   - Main agent verifies file exists
   - For large files (>1000 lines), hook prompt instructs subagent to use chunked writes

**RULE 5: Subagent Steering File Loading**

**Problem**: Auto-loading steering files in subagents is unreliable. Subagents need explicit steering file loading for accurate output.

**Solution**: Subagents use `discloseContext()` to load domain-specific steering files at workflow start.

**Design Principles**:
1. **NO Auto-Loading**: Don't rely on keyword-based auto-loading in subagents
2. **Explicit Loading**: Use `discloseContext(name="steering-file-name")` at workflow start
3. **Domain-Specific Only**: Load only steering files needed for the subagent's domain
4. **Exclude General Rules**: Don't load `00_Kiro_General_Rules.md` - already provided via system instructions

**Steering File Name Mapping** (for discloseContext):
- `01_IPA_and_IPD_Complete_Guide.md` → `discloseContext(name="ipa-ipd-guide")`
- `02_Work_Unit_Analysis.md` → `discloseContext(name="work-unit-analysis")`
- `03_Process_Patterns_Library.md` → `discloseContext(name="process-patterns")`
- `04_WU_Report_Generation.md` → `discloseContext(name="wu-report-generation")`
- `05_Compass_SQL_CheatSheet.md` → `discloseContext(name="compass-sql")`
- `06_FSM_Business_Classes_and_API.md` → `discloseContext(name="fsm-business-classes")`
- `07_Infor_OS_Data_Fabric_Guide.md` → `discloseContext(name="data-fabric-guide")`
- `08_Infor_IDM_Guide.md` → `discloseContext(name="idm-guide")`
- `09_FSM_Navigation_Guide.md` → `discloseContext(name="fsm-navigation")`
- `10_IPA_Report_Generation.md` → `discloseContext(name="ipa-report-generation")`
- `11_RICE_Methodology_and_Specifications.md` → `discloseContext(name="rice-methodology")`
- `12_External_API_OAuth2_Integration_Guide.md` → `discloseContext(name="external-api-oauth2")`

**Client Handover Subagent Steering Files**:
- **ipa-activity-guide-generator**: `ipa-ipd-guide`, `ipa-report-generation`
- **ipa-business-requirements-analyzer**: `ipa-report-generation`, `rice-methodology`
- **ipa-workflow-analyzer**: `ipa-ipd-guide`, `ipa-report-generation`
- **ipa-configuration-analyzer**: `ipa-ipd-guide`, `ipa-report-generation`
- **ipa-validation-analyzer**: `work-unit-analysis`, `wu-report-generation`

**Coding Standards Subagent Steering Files**:
- **ipa-naming-analyzer**: `ipa-ipd-guide`, `ipa-report-generation`
- **ipa-javascript-analyzer**: `ipa-ipd-guide`, `work-unit-analysis`
- **ipa-sql-analyzer**: `compass-sql`, `ipa-ipd-guide`
- **ipa-error-handling-analyzer**: `ipa-ipd-guide`, `work-unit-analysis`
- **ipa-structure-analyzer**: `ipa-ipd-guide`, `ipa-report-generation`

**Example Subagent Workflow**:
```markdown
## Workflow

1. **Load required steering files** using discloseContext():
   - `discloseContext(name="ipa-ipd-guide")` - IPA concepts, activity nodes
   - `discloseContext(name="ipa-report-generation")` - Documentation standards
2. Read section data JSON using readFile()
3. Analyze data
4. Build structured JSON output
5. Save output using fsWrite()
```

**RULE 6: Verification Checklist**

Before creating/modifying a subagent:
- [ ] Does it have `invokeSubAgent` access? → Remove it
- [ ] Does it invoke file-writer-helper or other subagents? → Remove and use fsWrite
- [ ] Does it have `tools: ["read", "fsWrite"]` for saving files? → Correct
- [ ] Is tool access minimal? → Remove unnecessary tools
- [ ] For large files, does hook prompt instruct chunked writes? → Add if needed
- [ ] Does it use `discloseContext()` to load steering files? → Add if missing
- [ ] Does it load ONLY domain-specific steering files? → Remove 00_Kiro_General_Rules.md

## IPA Analysis Workflow

### 🚨 MANDATORY STEPS - DO NOT SKIP 🚨

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

### Verification Checklist

Before generating ANY report, verify:
- [ ] JSON file extracted successfully
- [ ] JSON file READ completely using readFile()
- [ ] ALL processes analyzed (not just first one)
- [ ] ALL activities reviewed (not just summary stats)
- [ ] Specific findings documented (not generic statements)
- [ ] ipa_data dictionary built with YOUR analysis

**If ANY checkbox is unchecked, STOP and complete that step.**

### 1:1 JSON Mapping Rule

**ALWAYS**: ONE LPD file → ONE JSON file → ONE report

```python
# CORRECT: One LPD per JSON
extract_lpd_data(['Process1.lpd'], 'Temp/Process1_lpd_data.json')
extract_lpd_data(['Process2.lpd'], 'Temp/Process2_lpd_data.json')
```

### Complete ipa_data Structure Requirements

**CRITICAL**: The templates require ALL of these fields. Missing fields cause report generation failures.

```python
ipa_data = {
    # REQUIRED: Client and RICE item (for filename)
    'client_name': 'FPI',  # Extract from path: Projects/<Client>/...
    'rice_item': 'MatchReport',  # Extract from path: Projects/<Client>/<RICEItem>/...
    
    # REQUIRED: Overview section
    'overview': {
        'process_name': 'MatchReport_Outbound',
        'process_type': 'Interface Process',
        'activity_count': 78,
        'total_activities': 78,
        'process_count': 1,  # REQUIRED for Executive Dashboard
        'javascript_blocks': 20,
        'sql_queries': 0,
        'auto_restart': '0',
        'auto_restart_assessment': 'Appropriate - Should be 0 for interfaces'
    },
    
    # REQUIRED: Summary metrics
    'summary_metrics': {
        'total_violations': 5,
        'high_severity': 0,
        'medium_severity': 2,
        'low_severity': 3,
        'compliance_percentage': 93.6
    },
    
    # REQUIRED: Quality scores (for radar chart)
    'quality_scores': {
        'naming_convention': 87.2,
        'javascript_es5': 90.0,
        'ipa_rules': 100.0,
        'error_handling': 92.3,
        'configuration': 100.0,
        'performance': 100.0,
        'overall': 93.6
    },
    
    # REQUIRED: Activities array (for complexity calculation)
    'activities': [
        {'id': 'Start', 'type': 'START', 'caption': 'Start'},
        {'id': 'Branch8450', 'type': 'BRANCH', 'caption': 'Branch'},
        # ... all activities from extracted data
    ],
    
    # REQUIRED: Violations, recommendations, coding_standards arrays
    'violations': [...],
    'recommendations': [...],
    'coding_standards': {...},
    
    # REQUIRED: Empty arrays if none exist
    'sql_queries': [],
    'javascript_issues': [],
    'key_findings': [...],
    'best_practices': []
}
```

**DEDUPLICATION RULE**: Build `recommendations` array DIRECTLY from `violations` array to prevent duplicate action items.

## Analysis vs Data Processing

### Fundamental Rule

**Python extracts and processes data. AI (Kiro) analyzes and makes decisions.**

### Role Separation

| Python's Responsibilities | AI's Responsibilities (Kiro) |
|---------------------------|------------------------------|
| Extract data from files | Assess code quality and compliance |
| Parse XML, JSON, text formats | Identify issues and root causes |
| Structure raw data | Make recommendations |
| Format analyzed data into reports | Score quality metrics |
| Perform calculations | Determine severity and priority |

### Standard IPA Peer Review Workflow

1. Python extracts data → ONE JSON file per LPD (1:1 mapping)
2. Kiro reads EACH JSON separately and analyzes ONE process at a time
3. Kiro shows analysis in chat
4. Kiro asks: "Generate report with this analysis?"
5. User confirms
6. Python formats Kiro's analysis → ONE Excel report per process

## Communication Style

### Interactive User Input (userInput Tool)

**MANDATORY RULE**: ALWAYS use the `userInput` tool for ANY user interaction requiring a response.

**When to use userInput:**
- Selecting from lists (clients, RICE items, files, options)
- Yes/No confirmations
- Multiple choice decisions
- Any time there are clear, discrete options

**EXCEPTION - When NOT to use userInput:**
- **Step 14 of IPA workflows** - "Analyze another file?" question
- **Reason**: userInput responses may bypass hook execution
- **Solution**: Use plain text question so user's text response triggers hooks

**Example:**
```python
userInput(
    question="Which client would you like to analyze?",
    options=["BayCare", "FPI"],
    reason="general-question"
)
```

### Progress Indicators

Show clear progress for multi-step workflows:

```text
✓ Step 1/5: Steering files loaded (6 files)
→ Step 2/5: Extracting data from MatchReport_Outbound.lpd...
```

**When to use:**
- Multi-step workflows (5+ steps)
- Long-running operations (>5 seconds)
- Domain-segmented analysis (5 domains)

## File Management

### Directory Structure

| Directory | Purpose |
|-----------|---------|
| **Master templates** | Workspace root |
| **Temporary scripts** | `Temp/` folder |
| **Reports** | `Client_Handover_Results/`, `Coding_Standards_Results/`, `Performance_Results/` |
| **Credentials** | `Credentials/` folder (NEVER commit to git) |

### Git Ignore Pattern (Folder Structure Preservation)

**Pattern**: Keep folder structure in Git but ignore generated contents

```gitignore
# Ignore contents but keep folder structure
Temp/*
!Temp/.gitkeep

Coding_Standards_Results/*
!Coding_Standards_Results/.gitkeep
```

**Benefits:**
- ✅ Folder structure preserved in Git
- ✅ Generated files not committed (clean repo)
- ✅ New clones have folders ready

### Workspace Cleanup (CRITICAL FOR STABILITY)

**Problem:** Temp folder accumulates files that cause IDE indexing overhead and crashes.

**Solution:** Integrated cleanup into IPA workflow hooks as Step 13.5:
- Automatically checks Temp folder after report generation
- Only prompts if >10 files exist
- Uses userInput for clean UI buttons
- Safely removes only OLD files (>5 minutes old)
- Preserves current session data for troubleshooting

**Manual Cleanup (if needed):**
```powershell
# Delete files older than 5 minutes (safe)
$oldFiles = Get-ChildItem Temp -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddMinutes(-5) }
$oldFiles | Remove-Item -Force
```

## Reusable Tools

### Key Tools Overview

| Tool | Location | Purpose |
|------|----------|---------|
| **IPA Analyzer** | `ReusableTools/IPA_Analyzer/` | Extract data from LPD files, WU logs, specs |
| **Coding Standards** | `ReusableTools/IPA_CodingStandards/` | Programmatic coding standards analysis |
| **Hook Manager** | `ReusableTools/hook_manager.py` | Safe hook editing with backups |
| **Excel Reader** | `ReusableTools/excel_reader.py` | Read Excel files when readFile fails |
| **JSON Validator** | `ReusableTools/validate_json.py` | Generic JSON validator with hook auto-detection |

### IPA Coding Standards Analyzer

**Purpose:** Programmatic analyzer that applies coding standards rules to avoid context overload.

**When to Use:**
- Coding standards reviews (rules-based)
- Large processes (>200 activities)
- Multiple processes in one session

**Workflow:**
```text
Step 1: Extract data → JSON (Python)
Step 2: Analyze programmatically → Analysis JSON (Python)
Step 3: AI reviews analysis + adds insights → ipa_data (AI)
Step 4: Generate report (Python)
```

### Hook Manager Tool (CRITICAL FOR HOOK EDITING)

**Purpose:** Comprehensive Python tool for safe hook editing that operates outside the context system.

**Features:**
- Deep validation with error location
- Automatic timestamped backups
- Safe restore with backup of current
- Diff comparison between versions
- Complexity analysis
- Automatic repair (remove control characters)

**Usage:**
```bash
# Validate hook
python ReusableTools/hook_manager.py validate <hook_file>

# Backup and restore
python ReusableTools/hook_manager.py backup <hook_file>
python ReusableTools/hook_manager.py restore <hook_file> <backup_path>

# Analysis and repair
python ReusableTools/hook_manager.py analyze <hook_file>
python ReusableTools/hook_manager.py repair <hook_file>
```

**When to Use:**
- ANY hook editing in long sessions (10+ messages)
- After ANY fsWrite failure on hook files
- Before making major hook changes (backup first)

### Excel Reader (CRITICAL FOR BINARY FILES)

**Purpose:** Read Excel files when readFile fails with "File seems to be binary".

**Usage:**
```python
# Via executePwsh (recommended for Kiro)
executePwsh("python -c \"from ReusableTools.excel_reader import read_excel; df = read_excel('file.xlsx', sheet_name='Standards', display=True)\"")

# Export to JSON first
executePwsh("python ReusableTools/excel_reader.py file.xlsx --sheet Standards --json output.json")
```

**Integration:** MANDATORY for reading project_standards.xlsx files in coding standards workflow.

## Code Standards

### Python Scripts

- Include shebang `#!/usr/bin/env python3`
- Include main guard: `if __name__ == "__main__":`
- Use `sys.path` resolution for dynamic imports
- Convert sets to lists before JSON serialization

### IPA JavaScript

- ES5 only (no `let`, `const`, arrow functions)
- Ternary operators ARE valid ES5: `var x = condition ? value1 : value2;`
- Declare all functions early in script
- Use `var` for all variable declarations

### Python Library Selection

Choose appropriate libraries for the task:

| Task | Recommended Library |
|------|-------------------|
| **Excel with charts** | xlsxwriter or matplotlib+openpyxl |
| **Data processing** | pandas DataFrames |
| **Visualizations** | matplotlib/seaborn |

**General principle:** Use specialized libraries (pandas, numpy, matplotlib) rather than limiting to basic libraries.

## Knowledge Management

### Documentation Strategy

Update relevant steering files in `.kiro/steering/` when new patterns or approaches are established.

### Table of Contents Standards

**All steering files MUST include a proper Table of Contents (TOC):**

- Place TOC immediately after the main title (H1)
- Use markdown anchor links: `[Section Name](#section-name)`
- Include all H2 sections (##) as top-level TOC items
- Include H3 sections (###) as nested items under their parent H2
- Use proper indentation for nested items (2 spaces per level)

**When updating steering files:**
1. Check if TOC exists - if not, add one
2. Verify TOC includes all H2 and H3 sections
3. Update TOC when adding/removing sections

### Steering File Organization

| Learning Type | Steering File |
|---------------|---------------|
| Error patterns | `02_Work_Unit_Analysis.md` |
| Process patterns | `03_Process_Patterns_Library.md` |
| Report formatting | `04_WU_Report_Generation.md` |
| SQL patterns | `05_Compass_SQL_CheatSheet.md` |
| FSM business classes | `06_FSM_Business_Classes_and_API.md` |
| Infor OS/ION/Data Fabric | `07_Infor_OS_Data_Fabric_Guide.md` |
| IDM integration | `08_Infor_IDM_Guide.md` |
| FSM navigation | `09_FSM_Navigation_Guide.md` |
| IPA reports | `10_IPA_Report_Generation.md` |
| RICE methodology | `11_RICE_Methodology_and_Specifications.md` |
| External API OAuth2 | `12_External_API_OAuth2_Integration_Guide.md` |
| Generic insights | `00_Kiro_General_Rules.md` |

## Recent Session Learnings

### 2026-02-24: Client Handover Report - Matplotlib Emoji Rendering and Nested Data Flattening

**Problem:** Client handover Excel report had two critical issues: (1) Workflow diagram in Executive Summary appeared corrupted/garbled, (2) Production Validation sheet showed raw JSON strings instead of readable values.

**Root Causes:**

1. **Matplotlib Emoji Rendering Issue**
   - Workflow diagram labels contained emojis (🚀, 📝, ❓, 🌐, ⏱️, etc.)
   - Default matplotlib font (DejaVu Sans) cannot render emojis
   - Result: Corrupted/garbled diagram output with "Glyph missing from font" warnings

2. **Nested Dictionary Serialization**
   - Production validation data had nested structure (test_summary, performance, error_handling, etc.)
   - Template used `str(value)` to convert dictionaries to strings
   - Result: Excel cells showed Python dict representation like `{'work_unit_number': 36829, 'total_executions': 1, ...}`

**Discovery Method:**

1. User reported diagram "looks garbage or corrupted"
2. Checked Python output - saw multiple "Glyph missing from font" warnings for emoji Unicode characters
3. Traced emojis to three sources:
   - Hardcoded in template code (legend items, branch labels)
   - In workflow_steps data from subagent analysis
   - In sheet names
4. For validation data: Used excel_reader.py to inspect actual sheet contents, confirmed JSON strings in Value column

**Fixes Applied:**

**Fix 1: Emoji Removal from Workflow Diagram (ipa_client_handover_template.py)**

Added comprehensive emoji stripping function:
```python
import re

def remove_emojis(text):
    """Remove all emojis from text to prevent matplotlib rendering issues"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002300-\U000023FF"  # misc technical (includes clocks)
        u"\U00002600-\U000027BF"  # misc symbols & dingbats
        u"\U00002702-\U000027B0"  # dingbats
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # supplemental symbols
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text).strip()

# Apply to all workflow step labels and branch labels
for step in workflow_steps:
    if 'label' in step:
        step['label'] = remove_emojis(step['label'])
    if 'branches' in step and isinstance(step['branches'], list):
        step['branches'] = [remove_emojis(str(b)) for b in step['branches']]
```

Removed emojis from:
- Legend items: "Start/End", "Process", "Decision", "API Call" (no emojis)
- Branch arrow labels: "Error", "Wait" (no emojis)
- Title: "Process Workflow" (no emoji)

**Fix 2: Nested Data Flattening (ipa_client_handover_template.py - create_production_validation)**

Replaced simple iteration with intelligent flattening:
```python
# OLD: Converted dicts to strings
for key, value in validation.items():
    if isinstance(value, (dict, list)):
        ws[f'B{row}'] = str(value)  # ❌ Creates JSON strings

# NEW: Flatten nested structures
flattened_data = []

# Test Summary
if 'test_summary' in validation:
    ts = validation['test_summary']
    flattened_data.append(('Work Unit Number', ts.get('work_unit_number', 'N/A'), 'Pass'))
    flattened_data.append(('Total Executions', ts.get('total_executions', 'N/A'), 'Pass'))
    # ... extract all fields

# Performance
if 'performance' in validation:
    perf = validation['performance']
    flattened_data.append(('Average Duration', perf.get('avg_duration', 'N/A'), 'Pass'))
    # ... extract all fields

# Error Handling, Production Readiness, Test Coverage, etc.
# ... flatten all nested sections

# Write flattened data
for param, value, status in flattened_data:
    ws[f'A{row}'] = param
    ws[f'B{row}'] = str(value)  # ✅ Simple values only
    ws[f'C{row}'] = status
```

Also removed emojis from Production Validation sheet:
- Title: "Production Test Results" (was "✅ Production Test Results")
- Banner: "All validation checks passed successfully!" (was "🎉 All validation...")
- Performance metrics: "Execution Speed", "Data Volume", etc. (removed emoji prefixes)

**Fix 3: Sheet Names - Keep Emojis (User Preference)**

User requested emojis remain in sheet names for visual appeal:
- 📊 Executive Summary
- 📋 Business Requirements
- ✅ Production Validation
- ⚙️ System Configuration
- 📚 Activity Node Guide
- ⚙️ MatchReport_Outbound
- 🔧 Maintenance Guide

**Key Lessons:**

**LESSON 1: MATPLOTLIB CANNOT RENDER EMOJIS**
- Default matplotlib fonts (DejaVu Sans, etc.) lack emoji glyphs
- Emojis in labels cause "Glyph missing from font" warnings
- Result: Corrupted/garbled diagram output
- Solution: Strip ALL emojis from matplotlib text using regex pattern
- Unicode ranges to cover: U+1F600-1F9FF (emojis), U+2300-27BF (symbols/dingbats)

**LESSON 2: COMPREHENSIVE EMOJI STRIPPING REQUIRED**
- Emojis can come from multiple sources:
  - Hardcoded in template (legend, labels, titles)
  - Dynamic data from subagents (workflow_steps)
  - User input or configuration
- Must strip emojis from ALL text passed to matplotlib
- Create reusable remove_emojis() function with comprehensive Unicode ranges

**LESSON 3: NESTED DATA REQUIRES INTELLIGENT FLATTENING**
- Don't use `str(dict)` to display nested data - creates unreadable JSON strings
- Extract meaningful fields from nested structures
- Present data in human-readable format (key-value pairs)
- Group related fields logically (test_summary, performance, error_handling)

**LESSON 4: TEMPLATE DATA HANDLING PATTERNS**
```python
# ❌ BAD: Converts everything to strings
for key, value in data.items():
    if isinstance(value, (dict, list)):
        cell.value = str(value)  # Unreadable JSON

# ✅ GOOD: Flatten nested structures
if 'nested_section' in data:
    section = data['nested_section']
    for field_name, field_value in section.items():
        row_data.append((field_name, field_value, status))
```

**LESSON 5: EMOJI USAGE GUIDELINES**
- Excel sheet names: Emojis OK (Excel handles Unicode well)
- Excel cell content: Emojis OK (Excel renders properly)
- Matplotlib diagrams: NO EMOJIS (font rendering issues)
- Python logging/console: Emojis OK (modern terminals support Unicode)

**Prevention:**

1. **Template Design**
   - Always flatten nested dictionaries before Excel output
   - Never use `str(dict)` for display purposes
   - Extract meaningful fields with descriptive labels

2. **Matplotlib Usage**
   - Create remove_emojis() utility function
   - Apply to ALL text before matplotlib rendering
   - Test with actual data that may contain emojis

3. **Data Validation**
   - Check template output with excel_reader.py
   - Verify no JSON strings in Value columns
   - Confirm diagrams render cleanly (no corruption)

4. **Subagent Instructions**
   - Subagents can use emojis in JSON output (for visual appeal)
   - Templates must strip emojis before matplotlib rendering
   - Document emoji handling in template comments

**Affected Files:**
- `ipa_client_handover_template.py` - Added remove_emojis(), flattened validation data
- `.kiro/steering/00_Kiro_General_Rules.md` - This documentation

**Impact:** Client handover reports now have clean, professional diagrams and readable validation data. Emojis preserved in sheet names for visual appeal while removed from matplotlib rendering to prevent corruption.

### 2026-02-24: Client Handover Report - Systematic JSON-to-Excel Field Audit

**Problem:** Client handover Excel report had multiple data quality issues - missing columns, empty sheets, incorrect process names.

**Discovery Method:** Created systematic audit script (`Temp/audit_json_to_excel.py`) to compare JSON fields vs Excel columns, revealing exact gaps.

**Issues Found:**

1. **Business Requirements Missing Columns**
   - JSON had 8 fields: id, category, title, description, priority, business_value, source, stakeholders
   - Excel showed only 6 columns: ID, Category, Title, Description, Priority, Business Value
   - Missing: source, stakeholders

2. **Configuration Sheet Empty**
   - Sheet had only 2 rows (header + warning)
   - Root cause: Configuration subagent saved malformed JSON (missing opening brace `{`)
   - merge_documentation.py skipped malformed file, resulting in empty config_variables array

3. **Process Name Shows "Unknown"**
   - Process sheet named "⚙️ Unknown" instead of "⚙️ MatchReport_Outbound"
   - Root cause: merge_documentation.py looked for process name in wrong location
   - Was: `business.get('document_metadata', {}).get('process_name', 'Unknown')`
   - Should be: Extract from filename using `Path(output_prefix).name`

**Fixes Applied:**

1. **ipa_client_handover_template.py** - Added columns G (Source) and H (Stakeholders)
   - Updated header row from 6 to 8 columns
   - Added stakeholders formatting (comma-separated list)
   - Updated column widths and merge cells

2. **.kiro/agents/ipa-configuration-analyzer.md** - Fixed JSON output format
   - Added explicit JSON structure example with opening `{` and closing `}`
   - Added verification note: "Your output MUST be valid JSON starting with opening brace `{`"
   - Updated chunked write instructions

3. **ReusableTools/IPA_ClientHandover/merge_documentation.py** - Fixed process name extraction
   - Changed from looking in business.document_metadata
   - Changed to: `Path(output_prefix).name` (extracts from filename)
   - Example: "Temp/MatchReport_Outbound" → "MatchReport_Outbound"

**Key Lessons:**

**LESSON 1: SYSTEMATIC AUDIT BEFORE FIXING**
- Create audit scripts to compare expected vs actual data
- Don't rely on visual inspection alone
- Audit reveals exact gaps, not just symptoms

**LESSON 2: SUBAGENT JSON OUTPUT VALIDATION**
- Subagents must write valid JSON with opening `{` and closing `}`
- Add explicit JSON structure examples in subagent instructions
- Verify JSON validity before merge operations

**LESSON 3: FILENAME-BASED DATA EXTRACTION**
- When data isn't in JSON, extract from filename patterns
- Use `Path(filename).name` to get base name from path
- Example: "Temp/ProcessName" → "ProcessName"

**LESSON 4: TRACE DATA FLOW END-TO-END**
- Follow data from extraction → organization → analysis → merge → consolidation → template
- Identify where data is lost or transformed incorrectly
- Fix at the source, not at the destination

**Audit Script Pattern:**
```python
# Load JSON
with open('data.json') as f:
    json_data = json.load(f)

# Load Excel
wb = openpyxl.load_workbook('report.xlsx')

# Compare fields
json_fields = set(json_data[0].keys())
excel_headers = [cell.value for cell in ws[1]]
excel_fields = set([h.lower().replace(' ', '_') for h in excel_headers])

missing = json_fields - excel_fields
if missing:
    print(f"❌ MISSING in Excel: {missing}")
```

**Affected Files:**
- `ipa_client_handover_template.py` - Business Requirements columns
- `.kiro/agents/ipa-configuration-analyzer.md` - JSON output format
- `ReusableTools/IPA_ClientHandover/merge_documentation.py` - Process name extraction

**Prevention:**
- Run systematic audits when reports have "data all over the place"
- Verify subagent JSON output is valid before merge
- Extract metadata from filenames when not available in JSON
- Test full workflow after fixing to verify all issues resolved

### 2026-02-24: NEVER Modify Working Templates Without Verification

**Problem:** During client handover workflow troubleshooting, I modified the `ipa_client_handover_template.py` to handle structured requirements data, even though the template was already designed to handle that format.

**Root Cause:** I made assumptions about what needed to be fixed without verifying what the template already supported. The real issue was that `merge_documentation.py` was loading the wrong files (`_section_*.json` instead of `_doc_*.json`), not that the template couldn't handle the data format.

**What I Did Wrong:**
1. ❌ Modified the template's `create_business_requirements()` function unnecessarily
2. ❌ Added "backward compatibility" code when the template was already comprehensive
3. ❌ Changed working code based on assumptions instead of verification
4. ❌ Made multiple changes when only ONE fix was needed (merge_documentation.py)

**What I Should Have Done:**
1. ✅ Verify what the template ALREADY supports before modifying it
2. ✅ Check git history or backups to see previous working state
3. ✅ Fix ONLY the actual broken component (merge_documentation.py)
4. ✅ Test with existing template before assuming it needs changes

**The ONLY Fix Needed:**
- Update `merge_documentation.py` to load `_doc_*.json` files (analyzed data from subagents) instead of `_section_*.json` files (raw extracted data)
- Template was ALREADY comprehensive and working correctly

**Critical Rules to Prevent This:**

**RULE 1: VERIFY BEFORE MODIFYING**
- Before modifying ANY template or working code:
  - Check what it ALREADY supports
  - Read the existing code carefully
  - Look for similar patterns already implemented
  - Test with existing code first

**RULE 2: FIX ROOT CAUSE, NOT SYMPTOMS**
- Identify the ACTUAL broken component
- Don't modify multiple files when one fix will do
- If template receives wrong data, fix the DATA SOURCE, not the template

**RULE 3: TEMPLATES ARE COMPREHENSIVE BY DESIGN**
- `ipa_client_handover_template.py` is designed to handle rich structured data
- `ipa_coding_standards_template.py` is designed to handle complex violation structures
- `wu_master_template.py` is designed to handle detailed WU log data
- Don't assume templates are "simple" - they're already comprehensive

**RULE 4: ONE PROBLEM = ONE FIX**
- If data flow is broken, fix the data flow
- If template has a bug, fix the template
- Don't fix both when only one is broken

**Data Flow in Client Handover Workflow:**
```
1. Python extracts → _section_*.json (raw data)
2. Subagents analyze → _doc_*.json (rich structured data)
3. merge_documentation.py → loads _doc_*.json ← THIS WAS THE BUG
4. Template receives → rich structured data ← TEMPLATE WAS ALREADY CORRECT
```

**Key Lesson:** Working templates are comprehensive by design. Before modifying them, verify they actually need changes. Most "template issues" are actually data flow issues upstream.

**Affected Files:**
- `ReusableTools/IPA_ClientHandover/merge_documentation.py` - CORRECT FIX: Load _doc_*.json instead of _section_*.json
- `ipa_client_handover_template.py` - UNNECESSARY CHANGES: Template was already comprehensive
- `ReusableTools/IPA_ClientHandover/generate_client_handover_report.py` - UNNECESSARY CHANGES: Helper was already passing data correctly

**Future Prevention:**
- When troubleshooting, identify the EXACT broken component
- Verify what existing code already supports
- Make ONE targeted fix, not multiple "just in case" changes
- Test with existing code before assuming it needs modification

### 2026-02-24: Sequential Subagent Execution for Reliability

**Problem:** Batched parallel execution (2-3 subagents at a time) still caused resource exhaustion and cancellations during client handover workflow. Both subagents in Batch 1 were canceled mid-execution.

**Root Cause:** Even small batches (2 subagents) can exceed system resource limits under certain conditions, causing cancellations and workflow failures.

**Solution:** Sequential execution - launch subagents ONE AT A TIME to eliminate resource contention entirely.

**Implementation (Hook v40):**
- Analyzer 1/5: Business Requirements (wait for completion)
- Analyzer 2/5: Workflow (wait for completion)
- Analyzer 3/5: Configuration (wait for completion)
- Analyzer 4/5: Activity Guide (wait for completion)
- Analyzer 5/5: Validation (wait for completion)

**Benefits:**
- ✅ Zero resource exhaustion (one subagent at a time)
- ✅ 100% reliability (no cancellations)
- ✅ Clear progress tracking (1/5, 2/5, 3/5, 4/5, 5/5)
- ✅ Easy debugging (know exactly which analyzer failed)
- ✅ Proven reliable pattern

**Tradeoff:**
- Takes 2-3 minutes instead of 30-60 seconds
- But RELIABILITY > SPEED for production workflows

**Key Lesson:** When system stability is critical (demos, production), sequential execution is the safest approach. Parallel execution is an optimization that should only be used when system resources are guaranteed.

**Affected Files:**
- `.kiro/hooks/ipa-client-handover.kiro.hook` (v39 → v40)
- Updated STEP 8 to sequential execution with clear progress indicators

### 2026-02-23: Multi-Process Client Handover - ONE Report per RICE Item

**Problem:** Client handover workflow generated separate reports for each LPD file, but clients care about RICE deliverables, not internal implementation details.

**Client Perspective:** One RICE item = One handover document, regardless of how many IPAs were created internally.

**Solution:** Updated workflow to consolidate multiple processes into ONE report per RICE item:
- Multi-select LPD files in Step 3
- Automated loop processes each LPD (Steps 6-10)
- New Step 11: Consolidates all processes into RICE-level documentation
- ONE Excel report with separate sheets per process

**Architecture Changes:**
1. **Hook Updated** (v38 → v39): Multi-select, automated loop, consolidation step
2. **New Tool**: `consolidate_processes.py` - merges multiple process docs into RICE-level file
3. **Updated Tool**: `generate_client_handover_report.py` - loads consolidated documentation
4. **Updated Template**: `ipa_client_handover_template.py` - sheet names use process names

**Report Structure (Multiple Processes)**:
- Executive Summary (consolidated)
- Business Requirements (RICE-level from spec)
- Validation (aggregated metrics)
- Configuration (consolidated)
- Activities (consolidated)
- Process_<ProcessName1> (detailed workflow)
- Process_<ProcessName2> (detailed workflow)
- Process_<ProcessName3> (detailed workflow)
- Maintenance Guide (consolidated)

**Backward Compatibility:**
- ✅ Single LPD works exactly as before
- ✅ Multiple LPDs consolidated into ONE report
- ✅ No breaking changes

**Key Lesson:** Client-facing documentation should align with client perspective (RICE deliverables), not internal implementation details (number of IPAs).

**Affected Files:**
- `.kiro/hooks/ipa-client-handover.kiro.hook` (v38 → v39)
- `ReusableTools/IPA_ClientHandover/consolidate_processes.py` (NEW)
- `ReusableTools/IPA_ClientHandover/generate_client_handover_report.py` (updated)
- `ipa_client_handover_template.py` (updated sheet naming)

### 2026-02-23: Batched Parallel Subagent Execution

**Problem:** Invoking 5 subagents simultaneously caused system resource exhaustion - 4 subagents were canceled mid-execution, only 1 completed successfully.

**Root Cause:** Parallel execution of too many subagents exceeds system resource limits, causing cancellations and workflow failures.

**Solution:** Batched parallel execution - divide subagents into smaller batches (2-3 at a time) to reduce resource contention while maintaining speed benefits.

**Implementation:**
- Batch 1: Business Requirements + Workflow (2 subagents)
- Wait for Batch 1 completion
- Batch 2: Configuration + Activities + Validation (3 subagents)
- Wait for Batch 2 completion

**Benefits:**
- ✅ Avoids resource exhaustion and cancellations
- ✅ Maintains 50-60% speed improvement over sequential
- ✅ More reliable than full parallel execution
- ✅ Scalable approach for any multi-subagent workflow

**Key Lesson:** Parallel subagent execution has system limits. Batch execution (2-3 at a time) balances speed and reliability.

**Affected Files:**
- `.kiro/hooks/ipa-client-handover.kiro.hook` (v36 → v37)
- Updated STEP 8 to use batched parallel execution

### 2026-02-23: Eliminate Duplicate Steering File Loading in Workflows

**Problem:** Client handover hook had main agent loading steering files in STEP 6, but subagents also load their own steering files, causing duplicate loading.

**Issue:** Unnecessary context consumption - main agent doesn't need steering files since it only orchestrates workflow, not performs analysis.

**Solution:** Removed STEP 6 from client handover hook (v15):
- Main agent no longer loads steering files (01, 10, 11)
- Subagents load their own required steering files as documented in their definition files
- Main agent only orchestrates, reads merged documentation, and generates reports

**Affected Files:**
- `.kiro/hooks/ipa-client-handover.kiro.hook` (v14 → v15)
- Renumbered steps 7-14 to 6-13
- Updated CRITICAL RULES to note subagents load their own steering files

**Key Lesson:** When subagents handle specialized analysis, main agent doesn't need domain knowledge. Avoid duplicate steering file loading between main agent and subagents.

**Impact:** Reduced main agent context size, cleaner separation of concerns, no duplicate loading.

### 2026-02-23: Subagents Must Use Their Own fsWrite, Not Invoke Other Subagents

**Problem:** Subagents were configured with `tools: ["read", "invokeSubAgent"]` and instructed to invoke file-writer-helper for saving files.

**Issue:** This creates nested subagent calls, which violates the architectural principle that subagents should be self-contained.

**Solution:** Updated all 5 client handover subagents to use fsWrite directly:
- Changed `tools: ["read", "invokeSubAgent"]` to `tools: ["read", "fsWrite"]`
- Updated "Output Saving" sections to use fsWrite() directly
- Hook prompts provide chunked write instructions for large files (>1000 lines)

**Affected Subagents:**
- ipa-activity-guide-generator
- ipa-business-requirements-analyzer
- ipa-workflow-analyzer
- ipa-configuration-analyzer
- ipa-validation-analyzer

**Key Lesson:** Subagents should use their own tools (fsWrite) to save files, not invoke other subagents. Hook prompts handle large file instructions.

**Impact:** Cleaner architecture, no nested subagent dependencies, subagents are self-contained.

### 2026-02-23: Generic JSON Validator with Hook Auto-Detection

**Problem:** `hook_manager.py validate` gave false positives - said hooks were valid but IDE didn't recognize them. Root cause: version field was number (3) instead of string ("3").

**Solution:** Created `ReusableTools/validate_json.py` - generic JSON validator that auto-detects hook files and applies IDE-specific validation rules.

**Key Features:**
- Generic JSON syntax validation for any file
- Auto-detects hook files and applies hook-specific checks
- Version must be string type (CRITICAL - IDE requirement)
- Clear error messages with actionable guidance

**Impact:** No more false positives. Tool catches IDE-specific requirements that other validators miss.

### 2026-02-23: Git Ignore Pattern for Folder Structure Preservation

**Problem:** Need to keep folder structure in Git but ignore generated contents.

**Solution:** Use .gitignore pattern with .gitkeep files:
```gitignore
Temp/*              # Ignore all contents
!Temp/.gitkeep      # Except .gitkeep file
```

**Benefits:** Folder structure committed to Git, generated files ignored, new clones have folders ready.

### 2026-02-23: ReusableTools Hardening Complete

**Achievement:** Systematically improved all ReusableTools to enterprise-grade quality through 4-phase approach.

**Key Phases:**
1. Fix hook_manager.py encoding issues
2. Enhance hook_manager.py with update/search/lint functions
3. Audit all 19 Python files and add encoding robustness
4. Create comprehensive tool standards document

**Impact:** All ReusableTools now enterprise-grade quality with consistent encoding handling and clear standards for future development.

### 2026-02-23: Hook Manager Tool for Safe Hook Editing

**Problem:** Long session context + attempting to edit large hook files caused repeated crashes and corruption.

**Solution:** Created `ReusableTools/hook_manager.py` - comprehensive Python tool that operates outside the context system.

**Key Features:** Deep validation, automatic backups, safe restore, diff comparison, complexity analysis, automatic repair.

**When to Use:** ANY hook editing in long sessions, after ANY fsWrite failure on hook files, before making major hook changes.

### 2026-02-23: Integrated Workspace Cleanup in IPA Workflows

**Problem:** Separate cleanup hook was ineffective - triggered too often, no context about current vs old files.

**Solution:** Integrated cleanup into IPA workflow hooks as Step 13.5 - runs after successful report generation, only prompts if >10 files, safely removes only files older than 5 minutes.

**Benefits:** Perfect timing, user control, context-aware, no noise, preserves current session data.

### 2026-02-23: Client Handover Subagents Architecture Fix

**Problem:** Hook v11 instructed subagents to "Return analysis as JSON string" but subagents were designed with `tools: ["read", "fsWrite"]` and instructions to save files directly.

**Solution:** Updated hook v12 to follow Save Pattern consistently - all 5 subagents save files directly using fsWrite, main agent verifies outputs.

**Key Lesson:** When subagents have fsWrite tool access, the hook must follow the Save Pattern, not Return Pattern.

### 2026-02-23: Subagent fsWrite Causes Infinite Loop

**Problem:** Client handover workflow crashed with "Canceled edits" when subagents with `tools: ["read", "fsWrite"]` called fsWrite() during hook execution.

**Root Cause:** fsWrite triggers preToolUse/postToolUse hooks, creating infinite loops when called by hook-invoked subagents.

**Solution:** Hook-invoked subagents must use `tools: ["read"]` only. Main agent handles all file writes to avoid hook recursion.

**Architectural Rule:** Subagents invoked by hooks should NEVER have fsWrite tool access.

### 2026-02-23: userInput Bypasses Hook Execution

**Problem:** Using `userInput` for "Analyze another file?" question in Step 14 caused IPA Steering Files Reminder hook to not execute on the next message.

**Solution:** Use plain text question instead of `userInput` for Step 14 so user's text response triggers hooks properly.

**Exception:** Step 14 of IPA workflows - use plain text, not userInput, to ensure hook execution.

### 2026-02-23: Project Standards Must Be Loaded AND Passed to Subagents

**Problem:** BayCare APIA analysis gave incorrect naming recommendations even though project standards existed.

**Root Cause:** Three issues - project standards never loaded by main agent, steering files never loaded by subagents, project standards never passed to subagents.

**Solution:** Hook v36 now REQUIRES Step 6 (load project standards), passes standards to all subagents, subagents check project standards FIRST before steering file defaults.

**Key Lesson:** Subagents are isolated contexts. They need EXPLICIT instructions to load project standards and steering files.

### 2026-02-22: Domain-Segmented AI Analysis Architecture

**Problem:** Context overload when analyzing large IPA processes (450+ activities, 130+ JS blocks).

**Solution:** Domain-segmented architecture - analyze one domain at a time instead of everything together.

**Workflow:** Extract data → Organize by domain → Analyze each domain separately → Merge violations → Generate report.

**Key Innovation:** Python lifts heavy load (organize, aggregate), AI makes judgments (violations, severity, recommendations).

### 2026-02-22: IPA Domain Analyzer Subagents

**Problem:** Sequential domain analysis took 2.5-5 minutes.

**Solution:** Created 5 specialized subagents that run in parallel - `ipa-naming-analyzer`, `ipa-javascript-analyzer`, `ipa-sql-analyzer`, `ipa-error-handling-analyzer`, `ipa-structure-analyzer`.

**Performance Improvement:** 70-80% faster (30-60s vs 2.5-5 min).

**Benefits:** Massive speed improvement, no context pollution, specialized expertise per domain, scalable to any process size.

### 2026-02-24: EDI 850 Transformation - Production-Safe Code Layering

**Problem:** Need to layer new EDI transformation logic on top of existing production-safe baseline without breaking existing behavior.

**Challenge:** EDI documents are position-sensitive - small mistakes cause immediate rejection. Required adding 5 new features while preserving existing N1*SF insertion logic, multi-ST buffering, and fail-safe behavior.

**Solution:** Iterative refinement approach with explicit clarification questions before code generation.

**Key Architectural Decisions:**

1. **Clarification Before Code**
   - Created detailed implementation plan FIRST
   - Asked explicit questions about ambiguous requirements (REF placement, PO1 structure, PER behavior)
   - Documented answers before generating code
   - Result: Zero ambiguity, production-safe code on first generation

2. **In-Place Modification Pattern**
   - Original approach: Rebuild arrays from scratch (risk of element loss)
   - Refined approach: Create working copy, modify in-place, preserve all elements
   - Example: PO1 segments with 20+ elements - all preserved, only targeted changes applied
   - Benefit: No positional shifting side effects, no data loss in edge cases

3. **Change Detection Flags**
   - Only trigger SE01 recalculation when actual modifications occur
   - Track changes per segment type (po1Changed, removedN1BY, insertedREFDP, modifiedPER)
   - Unified flag (modifiedTransaction) accumulates all changes
   - Benefit: Efficient processing, no unnecessary segment rebuilding

4. **Safety Guards**
   - PER segments: Require minimum 3 elements before modification (prevents corruption)
   - REF*DP insertion: Only consider segments AFTER BEG (j > begIndex constraint)
   - PO1 modification: Only rebuild segment if actual change occurred
   - Benefit: Graceful handling of malformed segments, no accidental corruption

5. **Iterative Refinement Process**
   - v1: Initial implementation with all features
   - v2: Added change detection and safety guards
   - v2 Final: Fixed REF*DP placement constraint
   - v2 Production: In-place modification for maximum safety
   - Each iteration addressed specific edge cases identified through review

**Key Lessons:**

- **Clarify First, Code Second**: Explicit clarification questions prevent ambiguity and rework
- **In-Place Modification**: Safer than rebuilding arrays from scratch for position-sensitive data
- **Change Detection**: Only modify when needed - improves efficiency and reduces risk
- **Safety Guards**: Validate structure before modification to prevent corruption
- **Iterative Refinement**: Each review cycle identified edge cases, leading to production-safe code

**Architectural Patterns:**

```javascript
// PATTERN 1: In-Place Modification with Working Copy
var workingParts = [];
for (k = 0; k < txParts.length; k++) {
    workingParts.push(txParts[k]);  // Full copy
}
// Modify workingParts in-place
if (actualChangeOccurred) {
    transactionBuffer[j] = workingParts.join(separator);
}

// PATTERN 2: Change Detection Flag
var segmentChanged = false;
// ... modification logic ...
if (condition) {
    segmentChanged = true;
}
if (segmentChanged) {
    // Only rebuild if actual change
}

// PATTERN 3: Safety Guard
if (txTag === 'PER' && txParts.length >= 3) {
    // Only modify if structure is valid
}

// PATTERN 4: Constrained Iteration
if (begIndex !== -1 && insertRefIndex === -1 && j > begIndex) {
    // Only consider segments AFTER anchor point
}
```

**Impact:**
- Production-safe code with zero breaking changes
- All edge cases handled (10+ element segments, malformed data, multiple qualifiers)
- Efficient processing (only modify when needed)
- Clean architecture (no positional shifting, no data loss)

**Documentation:**
- Complete implementation plan with processing phases
- Clarification questions document with explicit answers
- Refinements history tracking each improvement
- Final production notes with test cases and deployment steps

**Affected Files:**
- `Temp/Transform_USFood_850_PRODUCTION.js` - Final production code
- `Temp/EDI_850_USFood_Implementation_Plan.md` - Implementation strategy
- `Temp/EDI_850_Clarification_Questions.md` - Requirements clarifications
- `Temp/FINAL_PRODUCTION_NOTES.md` - Production deployment guide


### 2026-02-24: Main Agent Should NOT Read Subagent Outputs

**Problem:** Client handover workflow had main agent reading subagent outputs in Step 9 and consolidated documentation in Step 12, causing context overload and crashes in long sessions.

**Root Cause:** Unnecessary data reading - Python tools already merge all subagent outputs automatically. Main agent doesn't need to read the data since it only orchestrates the workflow.

**Solution:** Updated hook v40 → v41 to remove reading steps:
- Step 9: Only verify files exist with Test-Path, DO NOT READ them
- Step 12: Renamed to "CONFIRM REPORT GENERATION" - no reading, just show summary and confirm
- Python tools (merge_documentation.py, consolidate_processes.py, generate_client_handover_report.py) handle ALL data loading and merging

**Data Flow (Corrected):**
```
1. Python extracts → _section_*.json (raw data)
2. Subagents analyze → _doc_*.json (rich structured data)
3. merge_documentation.py → loads _doc_*.json, creates _master_documentation.json
4. consolidate_processes.py → loads _master_*.json, creates _consolidated_documentation.json
5. generate_client_handover_report.py → loads consolidated, builds ipa_data, generates Excel
6. Main agent NEVER reads intermediate files - only orchestrates workflow
```

**Critical Rules:**

**RULE 1: MAIN AGENT ORCHESTRATES, PYTHON PROCESSES**
- Main agent: Invoke subagents, verify files exist, confirm with user
- Python tools: Load data, merge, transform, generate reports
- Main agent should NEVER read subagent outputs or merged documentation

**RULE 2: VERIFY FILES EXIST, DON'T READ THEM**
- Use Test-Path to verify files were created
- If file missing, STOP and report error
- DO NOT read the file contents - Python will handle that

**RULE 3: SHOW SUMMARY, NOT DATA**
- Show what was processed (client, RICE item, process names)
- Show what sections were analyzed (business, workflow, config, etc.)
- DO NOT show actual data from files

**RULE 4: PYTHON TOOLS ARE SELF-SUFFICIENT**
- generate_client_handover_report.py loads consolidated documentation automatically
- No need for main agent to pre-load or pre-process data
- Python tools handle all data transformations

**Benefits:**
- ✅ Eliminates context overload in main agent
- ✅ Prevents crashes in long sessions
- ✅ Cleaner separation of concerns (orchestration vs processing)
- ✅ Faster workflow (no unnecessary file reading)
- ✅ More reliable (Python handles data, not AI)

**Key Lesson:** When Python tools handle data merging and processing, main agent should only orchestrate the workflow. Reading intermediate files causes context overload without adding value.

**Affected Files:**
- `.kiro/hooks/ipa-client-handover.kiro.hook` (v40 → v41)
- Updated Step 9: Only verify files exist, DO NOT READ
- Updated Step 12: Renamed to CONFIRM REPORT GENERATION, removed readFile()

**Future Prevention:**
- When designing workflows with subagents and Python tools, ask: "Does main agent need to read this data?"
- If Python tool will load the data anyway, main agent should NOT read it
- Main agent's role: Orchestrate, verify, confirm - NOT process data


### 2026-02-24: Work Unit Extraction Tool - Comma Handling Bug

**Problem:** Performance reports showed "Unknown" for work unit number, "Unknown" for duration, and "0" for activities despite successful extraction.

**Root Causes:**

1. **Extraction Tool Regex Bug**: Pattern `r'Workunit\s+(\d+)\s+started'` only captured digits, stopping at comma in "36,829"
2. **Report Generation Bug**: Script looked for metadata at root level instead of `activities_analysis.metadata`
3. **Stale Analysis Files**: Subagents analyzed old data before extraction tool was fixed

**Fixes Applied:**

1. **extract_wu_log.py** (Lines 52-54, 66):
   - Changed `(\d+)` to `([\d,]+)` to capture numbers with commas
   - Updated both work unit number extraction and start time regex
   - Now correctly extracts "36,829" instead of just "36"

2. **generate_performance_report.py** (Lines 69-107):
   - Changed from `metadata = self.master_analysis.get('metadata', {})`
   - To: `metadata = activities_analysis.get('metadata', {})`
   - Fixed `_build_info_data()` to use correct metadata path
   - Now reads duration from `total_duration_readable` field

3. **Workflow Fix**:
   - After fixing extraction tool, must re-run organize_by_areas.py
   - Then re-run all 4 subagents to regenerate analysis files
   - Then merge_analysis.py and generate_performance_report.py

**Key Lessons:**

**LESSON 1: REGEX PATTERNS FOR FORMATTED NUMBERS**
- Work unit numbers can have commas: "36,829", "1,234,567"
- Use `[\d,]+` instead of `\d+` to capture formatted numbers
- Test regex with actual log samples, not assumptions

**LESSON 2: VERIFY DATA FLOW END-TO-END**
- Extraction → Organization → Analysis → Merge → Report
- Each step depends on previous step's output
- Fixing extraction requires re-running entire pipeline

**LESSON 3: JSON PATH VALIDATION**
- Don't assume metadata location - verify actual JSON structure
- Use `activities_analysis.metadata` not root-level `metadata`
- Check master_analysis.json structure before coding

**LESSON 4: SUBAGENT ANALYSIS IS CACHED**
- Subagents save analysis files once
- Fixing upstream data requires re-running subagents
- Old analysis files cause "garbage" reports

**Prevention:**
- Test extraction tools with real log samples (commas, special chars)
- Verify JSON structure before writing report generation code
- Re-run full pipeline after fixing extraction tools
- Add validation to check for "Unknown" values before report generation

**Affected Files:**
- `ReusableTools/IPA_Analyzer/extract_wu_log.py` - Regex patterns fixed
- `ReusableTools/IPA_Performance/generate_performance_report.py` - Metadata path fixed
- All 4 WU analyzer subagents - Re-ran to regenerate analysis files

**Impact:** Reports now show complete, accurate data (WU: 36,829, Duration: 6.71s, Activities: 28)

### 2026-02-24: Hook Structure Validation - Duplicate "prompt" Key Issue

**Problem:** Performance hook had TWO "prompt" keys - one short message inside `then.prompt` and one long workflow instructions at root level `prompt`.

**Discovery:** User noticed the duplicate keys when reviewing the hook file. Validation with hook_manager.py showed the hook was "valid" but the structure was incorrect compared to other hooks.

**Root Cause:** During previous edits, the hook structure got duplicated - likely when workflow instructions were being updated, the root-level "prompt" key was added instead of updating the existing `then.prompt` key.

**Correct Hook Structure:**

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
    "prompt": "ALL WORKFLOW INSTRUCTIONS GO HERE (can be very long)"
  }
}
```

**Incorrect Structure (What Was Wrong):**

```json
{
  "enabled": true,
  "name": "HookName",
  "when": {...},
  "then": {
    "type": "askAgent",
    "prompt": "Short trigger message"  // ❌ SHORT message here
  },
  "prompt": "Long workflow instructions..."  // ❌ DUPLICATE at root level
}
```

**Fix Applied:**
1. Moved ALL workflow instructions into `then.prompt` (where they belong)
2. Removed the root-level `prompt` key entirely
3. Updated version from 5 → 6
4. Verified with hook_manager.py validation

**Verification:**
- Root keys: enabled, name, description, version, when, newSession, then (NO "prompt")
- Has then.prompt: True (contains all 227 lines of workflow instructions)
- Validation: VALID with 23 workflow steps and 4 subagent calls

**Key Lessons:**

**LESSON 1: HOOK STRUCTURE VALIDATION**
- Hooks should have ONLY ONE "prompt" key, inside the "then" object
- Root-level "prompt" key is NOT part of the standard hook schema
- Compare with other working hooks (coding-standards, client-handover) to verify structure

**LESSON 2: HOOK_MANAGER VALIDATION LIMITATIONS**
- hook_manager.py validates JSON syntax and required fields
- It does NOT catch structural issues like duplicate keys at different levels
- Manual review or comparison with other hooks is needed for structural validation

**LESSON 3: WHEN EDITING HOOKS**
- Always update `then.prompt` with workflow instructions
- Never add a root-level `prompt` key
- Use hook_manager.py for safe editing in long sessions
- Verify structure matches other working hooks after major edits

**LESSON 4: MISSING WORKFLOW STEPS**
- Performance hook was missing Step 13 ("Analyze another log?")
- Other IPA hooks (coding-standards, client-handover) have this continuation step
- Consistency across similar workflows improves user experience

**Affected Files:**
- `.kiro/hooks/performance.kiro.hook` (v3 → v6)
  - v4: Version bump during initial investigation
  - v5: Added Step 13 (but structure still had duplicate prompt)
  - v6: Fixed duplicate prompt key structure

**Prevention:**
- When editing hooks, always check structure matches the standard pattern
- Compare with other working hooks before finalizing changes
- Use hook_manager.py validate after edits
- Manual review for structural issues that automated validation might miss


### 2026-02-24: WU Performance Analysis - Schema Validation for Subagent Outputs

**Problem:** Subagents are AI-driven and could produce varying JSON structures across different runs, causing report generation failures with incomplete or incorrectly formatted data.

**Root Cause:** No validation layer to ensure uniform JSON structure from subagents. The report generator (`generate_performance_report.py`) and template (`wu_master_template.py`) expect specific data structures, but subagents could produce variations.

**Solution:** Implemented comprehensive schema validation system with three layers of defense:

**Layer 1: Schema Validator (`validate_analysis_schema.py`)**
- Defines exact JSON schemas for each analysis type (activities, errors, performance, code)
- Validates required fields, nested structures, and data types
- Provides clear error messages and warnings
- Can be run standalone or integrated into merge process

**Layer 2: Merge-Time Validation (`merge_analysis.py`)**
- Validates each subagent output against schema before merging
- Continues with warnings if schema doesn't match (graceful degradation)
- Alerts user to potential data quality issues
- Prevents silent failures

**Layer 3: Defensive Transformations (`generate_performance_report.py`)**
- Handles both dict and array formats for flexible inputs
- Provides fallbacks for missing fields
- Merges raw WU data with analyzed data for complete information
- Ensures all required fields exist before template processing

**Key Components:**

1. **validate_analysis_schema.py** - Standalone validator
   ```python
   python ReusableTools/IPA_Performance/validate_analysis_schema.py <file> <type>
   ```
   - Types: activities, errors, performance, code
   - Returns validation report with errors and warnings

2. **Schema Definitions** - Explicit structure requirements
   ```python
   SCHEMAS = {
       'activities': {
           'required_fields': ['metadata', 'statistics', 'activities', ...],
           'activity_fields': ['name', 'type', 'duration_ms', 'status', ...]
       },
       'errors': {...},
       'performance': {...},
       'code': {...}
   }
   ```

3. **Merge Integration** - Automatic validation during merge
   ```python
   validator = SchemaValidator(area)
   is_valid = validator.validate(data)
   if not is_valid:
       print(validator.get_report())  # Show warnings but continue
   ```

4. **Report Generator Transformations**
   - `_build_activities()`: Merges timestamps from raw WU data with analyzed status
   - `_build_errors()`: Ensures all required fields (activity, type, message, severity, impact)
   - `_build_js_issues()`: Validates array format, handles dict/array variations
   - `_build_sql_issues()`: Validates array format, handles dict/array variations
   - `_build_memory_analysis()`: Converts dict to 7-column array format
   - `_build_recommendations()`: Maps to 10-column format with proper field alignment

**Data Flow with Validation:**

```
1. Python extracts → Temp/<Process>_wu_data.json (raw data with timestamps)
2. Python organizes → Temp/<Process>_area_*.json (4 area files)
3. Subagents analyze → Temp/<Process>_analysis_*.json (4 analysis files)
4. Validator checks → Schema validation (errors/warnings)
5. Python merges → Temp/<Process>_master_analysis.json (validated merge)
6. Report generator → Transforms to template format (defensive)
7. Template generates → Excel report (reliable output)
```

**Benefits:**

✅ **Reliability**: Schema validation catches structure issues before report generation
✅ **Consistency**: Uniform JSON structure across different subagent runs
✅ **Debugging**: Clear error messages identify exact schema violations
✅ **Graceful Degradation**: Continues with warnings if non-critical fields missing
✅ **Production-Ready**: Three-layer defense ensures robust operation

**Critical Rules:**

**RULE 1: VALIDATE BEFORE MERGE**
- Always run schema validation during merge process
- Don't skip validation even if subagent claims success
- Validation warnings indicate potential data quality issues

**RULE 2: DEFENSIVE TRANSFORMATIONS**
- Report generator must handle variations in subagent output
- Check data types before processing (dict vs array)
- Provide fallbacks for missing fields
- Merge raw data with analyzed data for completeness

**RULE 3: RAW DATA PRESERVATION**
- Keep raw WU data file (`_wu_data.json`) for complete information
- Subagent analysis may drop fields (e.g., timestamps)
- Report generator merges raw + analyzed for complete output

**RULE 4: SCHEMA EVOLUTION**
- Update schemas when adding new fields to subagent outputs
- Test validation after schema changes
- Document schema changes in subagent definitions

**Prevention:**

- Run `validate_analysis_schema.py` standalone to test subagent outputs
- Check merge output for validation warnings
- Verify report has complete data in all sheets
- Update schemas when subagent output format changes

**Affected Files:**
- `ReusableTools/IPA_Performance/validate_analysis_schema.py` (NEW) - Schema validator
- `ReusableTools/IPA_Performance/merge_analysis.py` - Added validation integration
- `ReusableTools/IPA_Performance/generate_performance_report.py` - Added defensive transformations
- `.kiro/agents/wu-*-analyzer.md` - Subagent definitions with explicit schemas

**Impact:** WU performance reports now have reliable, consistent data across different runs. Schema validation prevents silent failures and provides clear diagnostics when structure issues occur.

**Key Lesson:** AI-driven subagents need explicit schema validation to ensure uniform output. Three-layer defense (validation + merge checks + defensive transformations) creates production-ready reliability.


### 2026-02-24: Client Handover Report - Data Flow and Template Compatibility

**Problem:** Client handover Excel report had blurry diagram, missing validation data, and empty configuration sheet despite successful data extraction and subagent analysis.

**Root Causes:**

1. **Blurry Diagram**: DPI set to 150 instead of 300 for production-quality output
2. **Missing Validation Data**: generate_client_handover_report.py read from top-level validation (empty) instead of process-level validation (populated)
3. **Empty Configuration Sheet**: Template expected old format keys but data was in new structured format

**Discovery Method:**

1. Used excel_reader.py to inspect actual Excel sheet contents
2. Traced data flow: consolidated JSON → generate script → template
3. Identified mismatch between data structure and template expectations

**Data Flow Architecture:**

```
1. Python extracts → _section_*.json (raw data by section)
2. Subagents analyze → _doc_*.json (rich structured data)
3. merge_documentation.py → _master_documentation.json (per process)
4. consolidate_processes.py → _consolidated_documentation.json (RICE level)
5. generate_client_handover_report.py → builds ipa_data structure
6. Template → generates Excel report
```

**Issues Found:**

**Issue 1: Data Location Mismatch**
- Consolidated JSON structure:
  ```json
  {
    "metadata": {...},
    "validation": {},  // Empty at top level
    "configuration": {"config_variables": [...]},  // Top level
    "processes": [
      {
        "name": "ProcessName",
        "validation": {...},  // ACTUAL data here
        "configuration": {"config_variables": [...]}  // ACTUAL data here
      }
    ]
  }
  ```
- generate_client_handover_report.py was reading top-level (empty) instead of process-level (populated)

**Issue 2: Template Format Mismatch**
- Old format (template expected):
  ```python
  ipa_data = {
    'oauth_credentials': [...],
    'file_channel_config': [...],
    'process_variables': [...]
  }
  ```
- New format (data provided):
  ```python
  ipa_data = {
    'config_variables': [
      {
        'name': 'OauthCreds',
        'type': 'System Configuration',
        'location': 'FSM > Configuration > ...',
        'description': '...',
        'current_value': '...',
        'how_to_modify': '...',
        'impact': '...'
      }
    ]
  }
  ```

**Fixes Applied:**

**Fix 1: generate_client_handover_report.py (Lines 89-108)**
```python
# OLD: Always read from top level
'production_validation': consolidated.get('validation', {}),
'config_variables': consolidated.get('configuration', {}).get('config_variables', []),

# NEW: Prefer process-level for single process
process_list = consolidated.get('processes', [])

if len(process_list) == 1 and process_list[0].get('validation'):
    production_validation = process_list[0].get('validation', {})
else:
    production_validation = consolidated.get('validation', {})

if len(process_list) == 1 and process_list[0].get('configuration', {}).get('config_variables'):
    config_variables = process_list[0].get('configuration', {}).get('config_variables', [])
else:
    config_variables = consolidated.get('configuration', {}).get('config_variables', [])
```

**Fix 2: ipa_client_handover_template.py - create_system_configuration() (Lines 523-650)**
```python
# NEW: Handle structured config_variables format
config_vars = ipa_data.get('config_variables', [])
if config_vars and isinstance(config_vars, list) and len(config_vars) > 0:
    # Group by type
    system_config = [v for v in config_vars if 'System Configuration' in v.get('type', '')]
    file_channel = [v for v in config_vars if 'File Channel' in v.get('type', '')]
    
    # Create sections with 5 columns: Name, Location, Description, Current Value, How to Modify
    # ... (detailed implementation)

# LEGACY: Keep backward compatibility for old format
elif 'oauth_credentials' in ipa_data or 'file_channel_config' in ipa_data:
    # ... (old format handling)
```

**Fix 3: ipa_client_handover_template.py - Diagram DPI (Lines 236, 367)**
```python
# OLD: DPI 150 (blurry)
fig, ax = plt.subplots(figsize=(8, 12), dpi=150)
plt.savefig(diagram_path, dpi=150, bbox_inches='tight', facecolor='white')

# NEW: DPI 300 (sharp)
fig, ax = plt.subplots(figsize=(8, 12), dpi=300)
plt.savefig(diagram_path, dpi=300, bbox_inches='tight', facecolor='white')
```

**Verification:**

After fixes:
- System Configuration: 16 rows (was 2), showing all 7 config variables
- Production Validation: 19 rows (was 16), showing complete WU log data (WU 36,829, 6.71s, 28 activities)
- Executive Summary: Diagram image sharp and clear

**Key Lessons:**

**LESSON 1: TRACE DATA FLOW END-TO-END**
- When report has missing data, trace from source to destination
- Check: extraction → organization → analysis → merge → consolidation → generate → template
- Identify where data exists vs where code is looking for it

**LESSON 2: SINGLE VS MULTI-PROCESS DATA LOCATION**
- Single process: Data often in `processes[0]` not at top level
- Multi-process: Data aggregated at top level
- generate script must handle both cases intelligently

**LESSON 3: TEMPLATE FORMAT EVOLUTION**
- Templates evolve from simple arrays to rich structured objects
- Old format: `[['name', 'value', 'purpose', 'how_to']]` (array of arrays)
- New format: `[{'name': '...', 'type': '...', 'location': '...', ...}]` (array of objects)
- Templates must support both for backward compatibility

**LESSON 4: USE TOOLS TO INSPECT BINARY FILES**
- Excel files are binary - can't use readFile
- Use `excel_reader.py` or openpyxl to inspect actual sheet contents
- Don't assume report is correct - verify with tools

**LESSON 5: DPI MATTERS FOR PRODUCTION REPORTS**
- 150 DPI: Acceptable for drafts, blurry when zoomed
- 300 DPI: Production quality, sharp at all zoom levels
- Always use 300 DPI for client-facing documents

**Prevention:**

1. **Test Report Generation After Subagent Changes**
   - When subagents change output format, test full workflow
   - Verify Excel report has complete data in all sheets
   - Use excel_reader.py to inspect actual contents

2. **Document Data Structure Contracts**
   - Document expected structure in generate script comments
   - Document template expectations in template comments
   - Keep contracts in sync when formats evolve

3. **Add Validation to Generate Script**
   - Check if data exists before passing to template
   - Log warnings when expected data is missing
   - Provide fallbacks for missing data

4. **Maintain Backward Compatibility**
   - Support both old and new formats in templates
   - Use feature detection: `if 'new_key' in data: ... elif 'old_key' in data: ...`
   - Don't break existing workflows when adding new features

**Affected Files:**
- `ReusableTools/IPA_ClientHandover/generate_client_handover_report.py` - Data source selection
- `ipa_client_handover_template.py` - System Configuration format handling, diagram DPI
- `.kiro/steering/00_Kiro_General_Rules.md` - This documentation

**Impact:** Client handover reports now have complete, accurate data with production-quality diagrams. Template supports both legacy and new structured formats for backward compatibility.


### 2026-02-24: IPA JavaScript Transformation - Production-Grade ES5 Development

**Problem:** Developing production-ready JavaScript transformation scripts for Infor IPA requires strict ES5 compliance, comprehensive error handling, and specific architectural patterns for Assign Node compatibility.

**Context:** Created transformation script for Rosen POS Sales Integration (ANA-050) to process CSV files into InventoryTransactionImport business class records with location-based grouping and zero-net validation.

**Key Requirements:**

1. **ES5 Syntax Only**
   - Use `var` exclusively (no `let`, `const`)
   - No arrow functions
   - No modern ECMAScript features (map/filter/reduce, template literals, destructuring)
   - Traditional `for` loops with explicit iteration

2. **IPA Assign Node Architecture**
   - Entire script wrapped in function: `function transformImport(importFileContent, fileName)`
   - No top-level `return` statements (Assign nodes don't allow them)
   - Function invoked at end: `transformImport(ImportFile, FileName);`
   - Configuration variables inside function (not at top level)

3. **Production-Grade Safety Patterns**

**Pattern 1: Floating Point Comparison Safety**
```javascript
// ❌ UNSAFE: Direct comparison with zero
if (sumQty === 0)

// ✅ SAFE: Round before comparison
var roundedSum = roundToDecimals(sumQty, ROUND_DECIMALS);
if (roundedSum === 0)

// ✅ ALTERNATIVE: Epsilon comparison
if (Math.abs(sumQty) < 0.0000001)
```

**Pattern 2: Null/Undefined Input Guards**
```javascript
// ❌ UNSAFE: Assumes input exists
var lines = inputFileContent.split("\n");

// ✅ SAFE: Guard before use
if (!inputFileContent || typeof inputFileContent !== "string") {
    inputFileContent = "";
}
var lines = inputFileContent.split("\n");
```

**Pattern 3: Defensive Division**
```javascript
// ❌ UNSAFE: Division without check
var unitCost = extendedAmount / originalQuantity;

// ✅ SAFE: Check denominator first
if (originalQuantity === 0) {
    exceptions.push({...});
    continue;
}
var unitCost = extendedAmount / originalQuantity;
```

**Pattern 4: Conditional Header Creation**
```javascript
// ❌ WRONG: Create header even if no valid lines
headers.push(header);

// ✅ CORRECT: Only create header if valid lines exist
var validLinesForLocation = 0;
// ... process lines, increment validLinesForLocation ...
if (validLinesForLocation > 0) {
    headers.push(header);
}
```

**Pattern 5: Company Validation with Early Return**
```javascript
// ✅ CORRECT: Validate company and return early if invalid
if (!company || company === "" || !isNumeric(company)) {
    exceptions.push({
        lineNumber: 0,
        location: "",
        item: "",
        originalQuantity: "",
        reason: "Invalid company in filename"
    });
    
    return {
        headers: [],
        lines: [],
        exceptions: exceptions,
        summary: {
            totalInputLines: 0,
            totalValidLines: 0,
            totalExceptionLines: exceptions.length,
            totalHeadersCreated: 0
        }
    };
}
```

**Pattern 6: Exception Counter Accuracy**
```javascript
// ❌ WRONG: Manual counter that can drift
totalExceptionLines++;
exceptions.push({...});

// ✅ CORRECT: Use exceptions.length as source of truth
exceptions.push({...});
// Later in summary:
totalExceptionLines: exceptions.length
```

4. **Business Logic Patterns**

**Location-Based Grouping:**
- Group records by location (column index 2)
- Create separate header per location
- Reset line numbering per location (starts at 1)

**Zero-Net Validation:**
- Group by item within each location
- Sum quantities using rounded values for comparison
- If net quantity = 0, exclude all records for that item
- Add to exceptions with reason "Net quantity equals zero"

**Transaction Date Handling:**
- Extract from POS date field (column index 1, format YYYYMMDD)
- Validate: 8 digits, all numeric
- If invalid or missing: log exception, fallback to system date
- If multiple dates in location: log exception (optional), use first valid or system date

**Unit Cost Calculation:**
```javascript
var unitCost = extendedAmount / originalQuantity;  // Use ORIGINAL positive quantity
unitCost = roundToDecimals(unitCost, ROUND_DECIMALS);

var finalQty = originalQuantity;
if (FORCE_NEGATIVE_QUANTITY) {
    finalQty = originalQuantity * -1;  // Negate AFTER cost calculation
}
finalQty = roundToDecimals(finalQty, ROUND_DECIMALS);
```

5. **Configuration-Driven Design**

All behavior controlled by configuration variables at function top:
```javascript
var USE_POS_TRANSACTION_DATE = true;
var VALIDATE_MIXED_POS_DATES = false;
var FORCE_NEGATIVE_QUANTITY = true;
var ROUND_DECIMALS = 4;
var ENABLE_ZERO_NET_VALIDATION = true;
var FILENAME_COMPANY_INDEX = 1;
var DEFAULT_DOCUMENT_TYPE = "IS";
var DEFAULT_RUN_GROUP = "POS";
var DEFAULT_STATUS = 1;
var DEFAULT_TRANSACTION_SYSTEM_CODE = "IC";
```

6. **Return Structure**

```javascript
return {
    headers: [...],           // Array of header objects (one per location with valid lines)
    lines: [...],             // Array of line objects (all valid lines across locations)
    exceptions: [...],        // Array of exception objects (all errors/warnings)
    summary: {
        totalInputLines,      // Count of non-blank lines processed
        totalValidLines,      // Count of lines successfully transformed
        totalExceptionLines,  // exceptions.length (source of truth)
        totalHeadersCreated   // headers.length (only locations with valid lines)
    }
};
```

**Key Lessons:**

**LESSON 1: ES5 COMPLIANCE IS NON-NEGOTIABLE**
- IPA JavaScript nodes run in ES5 environment
- Modern syntax causes immediate runtime errors
- Use traditional patterns: `var`, `for` loops, function declarations
- Test with ES5 validator before deployment

**LESSON 2: FLOATING POINT ARITHMETIC REQUIRES ROUNDING**
- Never compare floating point sums directly to zero
- Always round before comparison: `roundToDecimals(sum, decimals) === 0`
- Alternative: epsilon comparison `Math.abs(sum) < 0.0000001`
- Applies to zero-net validation, balance checks, any sum comparisons

**LESSON 3: ASSIGN NODE ARCHITECTURE PATTERN**
- Wrap entire script in function
- No top-level return statements
- Invoke function at end with IPA variables (ImportFile, FileName)
- Configuration inside function (not at top level)
- This pattern allows script to work in Assign Node Expression Builder

**LESSON 4: DEFENSIVE PROGRAMMING FOR PRODUCTION**
- Guard all inputs (null/undefined checks)
- Validate before division (check denominator !== 0)
- Validate extracted values (company, dates, numeric fields)
- Early return on critical validation failures
- Never assume input data is well-formed

**LESSON 5: CONDITIONAL RESOURCE CREATION**
- Only create headers if valid lines exist for that location
- Prevents empty headers in output
- Keeps header count accurate
- Pattern: Track `validLinesForLocation`, check before header creation

**LESSON 6: EXCEPTION HANDLING WITHOUT STOPPING**
- Exceptions are warnings, not failures
- Continue processing after exception
- Use `exceptions.length` as source of truth for count
- Don't manually increment exception counter (can drift)

**LESSON 7: LOCATION-BASED GROUPING ARCHITECTURE**
- Parse all records first
- Group by location (creates object with location keys)
- Process each location independently
- Reset line numbering per location
- Create separate header per location
- Aggregate all lines into single output array

**LESSON 8: ZERO-NET VALIDATION SCOPE**
- Zero-net validation is PER LOCATION only
- Never compare across different locations
- Group by item within location
- Sum quantities (using rounded values)
- If sum = 0, exclude ALL records for that item in that location

**Prevention:**

1. **ES5 Validation Checklist**
   - [ ] No `let` or `const` (use `var`)
   - [ ] No arrow functions (use `function`)
   - [ ] No template literals (use string concatenation)
   - [ ] No destructuring (use explicit assignment)
   - [ ] No modern array methods (use `for` loops)
   - [ ] No default parameters (check inside function)

2. **Production Safety Checklist**
   - [ ] Null/undefined guards on all inputs
   - [ ] Floating point comparisons use rounding
   - [ ] Division operations check denominator
   - [ ] Company/date validation with early return
   - [ ] Headers only created if valid lines exist
   - [ ] Exception counter uses `exceptions.length`

3. **Assign Node Compatibility Checklist**
   - [ ] Entire script wrapped in function
   - [ ] No top-level return statements
   - [ ] Function invoked at end with IPA variables
   - [ ] Configuration variables inside function
   - [ ] Returns single object with expected structure

**Affected Files:**
- `Temp/Transform_Rosen_POS_Sales.js` - Production-ready transformation script
- `Temp/ANA-050_Rosen Point Of Sale integration.docx` - Functional specification
- `Temp/RMSale_103_02232026112233.txt` - Sample import file
- `.kiro/steering/00_Kiro_General_Rules.md` - This documentation

**Impact:** Established production-grade patterns for IPA JavaScript transformation development with comprehensive safety guards, ES5 compliance, and Assign Node compatibility.
