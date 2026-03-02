---
inclusion: always
---

# Core System Rules

## Table of Contents

- [Execution Philosophy](#execution-philosophy)
  - [Core Principles](#core-principles)
  - [Decision Matrix](#decision-matrix)
  - [Verification Before Analysis](#verification-before-analysis)
  - [Client Handover Workflow Requirements](#client-handover-workflow-requirements)
- [Communication Style](#communication-style)
  - [Interactive User Input](#interactive-user-input)
  - [Progress Indicators](#progress-indicators)
- [File Writing Strategy](#file-writing-strategy)
- [File Management](#file-management)
  - [Directory Structure](#directory-structure)
  - [Git Ignore Pattern](#git-ignore-pattern)
  - [Workspace Cleanup](#workspace-cleanup)
- [Code Standards](#code-standards)
  - [Python Scripts](#python-scripts)
  - [IPA JavaScript (ES5 Only)](#ipa-javascript-es5-only)
- [Knowledge Management](#knowledge-management)
  - [Documentation Strategy](#documentation-strategy)
  - [Table of Contents Standards](#table-of-contents-standards)
  - [Steering File Organization](#steering-file-organization)
- [Key Architectural Patterns](#key-architectural-patterns)
  - [Template Modification Rule](#template-modification-rule)
  - [Data Flow Tracing](#data-flow-tracing)
  - [Production Report Quality](#production-report-quality)
  - [Matplotlib Emoji Rendering](#matplotlib-emoji-rendering)
  - [Nested Data Flattening](#nested-data-flattening)
  - [Regex Patterns for Formatted Numbers](#regex-patterns-for-formatted-numbers)
  - [EDI Transformation Patterns](#edi-transformation-patterns)

## Execution Philosophy

### Core Principles

**ACT IMMEDIATELY** - Execute clear directives without overthinking or unnecessary questions.

**STOP IMMEDIATELY** - When user says "stop", "wait", "oh wait", or "hold on", STOP ALL ACTIONS immediately. Acknowledge and wait for new instructions.

### Decision Matrix

| Situation | Action |
|-----------|--------|
| Clear commands ("update X", "fix Y", "analyze Z") | Act without asking |
| Routine operations (reading files, running scripts) | Act without asking |
| Destructive operations (deleting files, dropping databases) | Ask first |
| Ambiguous requests with multiple interpretations | Ask first |
| User says "stop", "wait", "oh wait", "hold on" | Stop immediately |
| File operation fails with "Operation was aborted" | Stop immediately |

### Verification Before Analysis

Before ANY analysis, verify:

- [ ] All required files successfully read
- [ ] No truncation warnings unresolved
- [ ] Binary files handled with appropriate tools (excel_reader.py for Excel files)
- [ ] Data structures complete and valid

**If ANY checkbox fails, STOP and fix before proceeding.**

### Client Handover Workflow Requirements

**BLOCKING REQUIREMENT**: When generating client handover documentation, MUST follow stateless pipeline:

**Phase 0 (MANDATORY FIRST):**
```bash
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py <lpd> <spec>
```

Creates: `lpd_structure.json`, `metrics_summary.json`, `spec_raw.json`

**Phases 1-4:** Create analysis JSONs (business, workflow, configuration, risk)

**Phase 5 (MANDATORY LAST):**
```bash
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py <client> <rice>
```

**Common Mistake**: Skipping Phase 0 and manually extracting data
- Results in missing `lpd_structure.json` and `metrics_summary.json`
- Assembly script shows "Process Count: 0" and "Total Activities: 0"
- Report is incomplete

**Verification**: Before Phase 5, confirm these files exist:
- `Temp/lpd_structure.json` ✓
- `Temp/metrics_summary.json` ✓
- `Temp/business_analysis.json` ✓
- `Temp/workflow_analysis.json` ✓
- `Temp/configuration_analysis.json` ✓
- `Temp/risk_assessment.json` ✓

See `.kiro/steering/10_IPA_Report_Generation.md` for complete workflow documentation.

## Communication Style

### Interactive User Input

**MANDATORY RULE**: ALWAYS use the `userInput` syntax for ANY user interaction requiring a response.

**userInput Syntax:**

`userInput` is NOT a tool - it's a special text syntax that Kiro intercepts and transforms into interactive UI elements.

**Correct Usage:**

```text
userInput(question="Select a client:", options=["BayCare", "FPI", "SONH"], reason="general-question")
```

**Parameters:**

- `question`: The prompt text to display
- `options`: Array of choices (as Python list syntax)
- `reason`: Context for the input (e.g., "general-question")

**When to use userInput:**

- Selecting from lists
- Yes/No confirmations
- Multiple choice decisions
- Any time there are clear, discrete options

**CRITICAL LIMITATION (March 2, 2026):**

userInput does NOT work when skills are triggered directly:

- ✅ Works: Hook-triggered workflows (userTriggered hooks with newSession: true)
- ❌ Does NOT work: Skills activated via discloseContext() in existing sessions
- ❌ Does NOT work: Skills activated via discloseContext() in new sessions

**When to use userInput:**

- ONLY in hook-triggered workflows
- NEVER in skills (use plain text questions instead)

**When skills are activated:**

- Use plain text questions: "Which option? (A, B, C)"
- Wait for user's text response
- Parse response and continue workflow

### Progress Indicators

Show clear progress for multi-step workflows:

```text
✓ Step 1/5: Steering files loaded (6 files)
→ Step 2/5: Extracting data from MatchReport_Outbound.lpd...
```

Use for: Multi-step workflows (5+ steps), long-running operations (>5 seconds), domain-segmented analysis

## File Writing Strategy

**Rule**: In long sessions (10+ messages), use specialized tools instead of direct fsWrite to avoid context-related failures.

**For Hook Files**: Use `ReusableTools/hook_manager.py` Python tool

- Provides validation, backups, and operates outside context system
- Commands: `validate`, `backup`, `restore`, `analyze`, `repair`
- Use for ANY hook editing in long sessions

**For Other Files**: Use `file-writer-helper` subagent

- Use after ANY fsWrite failure
- Use for large file writes (>200 lines)
- Use for multiple file edits in sequence

**Fallback Workflow**:

1. Try direct fsWrite first (if context is light AND not a hook file)
2. If fsWrite fails once → Immediately delegate to appropriate tool
3. Do NOT retry fsWrite multiple times
4. Continue working without interruption

**The user should NEVER have to ask you to continue after a file write failure.**

## File Management

### Directory Structure

| Directory | Purpose |
|-----------|---------|
| **Master templates** | Workspace root |
| **Temporary scripts** | `Temp/` folder |
| **Reports** | `Client_Handover_Results/`, `Coding_Standards_Results/`, `Performance_Results/` |
| **Credentials** | `Credentials/` folder (NEVER commit to git) |

### Git Ignore Pattern

Keep folder structure in Git but ignore generated contents:

```gitignore
# Ignore contents but keep folder structure
Temp/*
!Temp/.gitkeep

Coding_Standards_Results/*
!Coding_Standards_Results/.gitkeep
```

### Workspace Cleanup

Temp folder accumulates files that cause IDE indexing overhead.

- Automatically check Temp folder after operations
- Only prompt if >10 files exist
- Safely remove only OLD files (>5 minutes old)
- Preserve current session data

**Manual Cleanup (if needed):**

```powershell
$oldFiles = Get-ChildItem Temp -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddMinutes(-5) }
$oldFiles | Remove-Item -Force
```

## Code Standards

### Python Scripts

- Include shebang `#!/usr/bin/env python3`
- Include main guard: `if __name__ == "__main__":`
- Use `sys.path` resolution for dynamic imports
- Convert sets to lists before JSON serialization
- Use specialized libraries (pandas, numpy, matplotlib) rather than limiting to basic libraries

### IPA JavaScript (ES5 Only)

**CRITICAL**: IPA JavaScript nodes run in ES5 environment. Modern syntax causes immediate runtime errors.

**ES5 Compliance Checklist:**

- [ ] Use `var` exclusively (no `let`, `const`)
- [ ] No arrow functions (use `function` declarations)
- [ ] No template literals (use string concatenation)
- [ ] No destructuring (use explicit assignment)
- [ ] No modern array methods like map/filter/reduce (use `for` loops)
- [ ] No default parameters (check inside function)
- [ ] Ternary operators ARE valid ES5: `var x = condition ? value1 : value2;`

**IPA Assign Node Architecture:**

- Entire script wrapped in function: `function transformImport(importFileContent, fileName)`
- No top-level `return` statements (Assign nodes don't allow them)
- Function invoked at end: `transformImport(ImportFile, FileName);`
- Configuration variables inside function (not at top level)

**Production Safety Patterns:**

1. **Floating Point Comparison**: Always round before comparison

   ```javascript
   // ✅ SAFE
   var roundedSum = roundToDecimals(sumQty, ROUND_DECIMALS);
   if (roundedSum === 0)
   ```

2. **Null/Undefined Guards**: Check inputs before use

   ```javascript
   // ✅ SAFE
   if (!inputFileContent || typeof inputFileContent !== "string") {
       inputFileContent = "";
   }
   ```

3. **Defensive Division**: Check denominator before dividing

   ```javascript
   // ✅ SAFE
   if (originalQuantity === 0) {
       exceptions.push({...});
       continue;
   }
   var unitCost = extendedAmount / originalQuantity;
   ```

## Knowledge Management

### Documentation Strategy

Update relevant steering files in `.kiro/steering/` when new patterns or approaches are established.

### Table of Contents Standards

All steering files MUST include a proper Table of Contents (TOC):

- Place TOC immediately after the main title (H1)
- Use markdown anchor links: `[Section Name](#section-name)`
- Include all H2 sections (##) as top-level TOC items
- Include H3 sections (###) as nested items under their parent H2
- Use proper indentation for nested items (2 spaces per level)

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
| Agent automation | `13_Kiro_Agent_Automation_Guide.md` |
| Workflow engineering | `00_Workflow_Engineering_Principles.md` (auto-loaded) |

### Keyword-Based Steering File Loading

**BLOCKING REQUIREMENT**: BEFORE proceeding with user requests, check for task-specific keywords and load appropriate steering files FIRST.

**Keyword Detection & Required Files:**

📊 **WORK UNIT ANALYSIS** (wu, log, work unit, error):
```
readMultipleFiles(['.kiro/steering/02_Work_Unit_Analysis.md', '.kiro/steering/04_WU_Report_Generation.md'])
```

🔍 **CODING STANDARDS** (coding standards, peer review, LPD, analyze process):
```
readMultipleFiles(['.kiro/steering/01_IPA_and_IPD_Complete_Guide.md', '.kiro/steering/02_Work_Unit_Analysis.md', '.kiro/steering/03_Process_Patterns_Library.md', '.kiro/steering/05_Compass_SQL_CheatSheet.md', '.kiro/steering/10_IPA_Report_Generation.md', '.kiro/steering/11_RICE_Methodology_and_Specifications.md'])
```

📋 **CLIENT HANDOVER** (client handover, documentation, handover report):
```
readMultipleFiles(['.kiro/steering/01_IPA_and_IPD_Complete_Guide.md', '.kiro/steering/10_IPA_Report_Generation.md', '.kiro/steering/11_RICE_Methodology_and_Specifications.md'])
```

🔌 **FSM/LANDMARK API** (FSM, Landmark, business class, WebRun, API):
```
readMultipleFiles(['.kiro/steering/06_FSM_Business_Classes_and_API.md', '.kiro/steering/01_IPA_and_IPD_Complete_Guide.md'])
```

📊 **DATA FABRIC** (Compass SQL, Data Fabric, Data Lake, ION, BOD):
```
readMultipleFiles(['.kiro/steering/05_Compass_SQL_CheatSheet.md', '.kiro/steering/07_Infor_OS_Data_Fabric_Guide.md'])
```

📄 **IDM** (IDM, document management, ContentDocument, CaptureDocument):
```
readMultipleFiles(['.kiro/steering/08_Infor_IDM_Guide.md', '.kiro/steering/01_IPA_and_IPD_Complete_Guide.md'])
```

🌐 **EXTERNAL API** (OAuth2, external API, Lightspeed, Stripe, third-party):
```
readMultipleFiles(['.kiro/steering/12_External_API_OAuth2_Integration_Guide.md'])
```

🤖 **AUTOMATION** (hook, skill, power, steering, spec, automation):
```
readMultipleFiles(['.kiro/steering/13_Kiro_Agent_Automation_Guide.md'])
```

🎯 **RICE SPECS** (RICE, ANA-050, DES-020, functional spec, technical spec):
```
readMultipleFiles(['.kiro/steering/11_RICE_Methodology_and_Specifications.md'])
```

**If NO keywords detected, proceed with the original request.**

## Key Architectural Patterns

### Template Modification Rule

**CRITICAL**: NEVER modify working templates without verification.

**Before modifying ANY template or working code:**

1. Check what it ALREADY supports
2. Read the existing code carefully
3. Look for similar patterns already implemented
4. Test with existing code first

**Most "template issues" are actually data flow issues upstream.** Fix the data source, not the template.

### Data Flow Tracing

When reports have missing data, trace from source to destination:

- extraction → organization → analysis → merge → consolidation → generate → template
- Identify where data exists vs where code is looking for it
- Use tools like `excel_reader.py` to inspect actual Excel contents
- Fix at the source, not at the destination

### Production Report Quality

**DPI Settings:**

- 150 DPI: Acceptable for drafts, blurry when zoomed
- 300 DPI: Production quality, sharp at all zoom levels
- **Always use 300 DPI for client-facing documents**

### Matplotlib Emoji Rendering

**Problem**: Matplotlib cannot render emojis - causes corrupted/garbled diagram output.

**Solution**: Strip ALL emojis from matplotlib text using regex pattern before rendering.

```python
import re

def remove_emojis(text):
    """Remove all emojis from text to prevent matplotlib rendering issues"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002300-\U000023FF"  # misc technical
        u"\U00002600-\U000027BF"  # misc symbols & dingbats
        u"\U00002702-\U000027B0"  # dingbats
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # supplemental symbols
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text).strip()
```

**Emoji Usage Guidelines**:

- Excel sheet names: Emojis OK
- Excel cell content: Emojis OK
- Matplotlib diagrams: NO EMOJIS
- Python logging/console: Emojis OK

### Nested Data Flattening

**Problem**: Using `str(dict)` to display nested data creates unreadable JSON strings in Excel.

**Solution**: Extract meaningful fields from nested structures.

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

### Regex Patterns for Formatted Numbers

Work unit numbers can have commas: "36,829", "1,234,567"

```python
# ❌ WRONG: Only captures digits
pattern = r'Workunit\s+(\d+)\s+started'  # Stops at comma

# ✅ CORRECT: Captures formatted numbers
pattern = r'Workunit\s+([\d,]+)\s+started'  # Includes commas
```

### EDI Transformation Patterns

For position-sensitive data (EDI documents):

1. **Clarification Before Code**: Create detailed implementation plan FIRST, ask explicit questions about ambiguous requirements
2. **In-Place Modification**: Create working copy, modify in-place, preserve all elements (safer than rebuilding arrays)
3. **Change Detection Flags**: Only trigger recalculation when actual modifications occur
4. **Safety Guards**: Validate structure before modification to prevent corruption
