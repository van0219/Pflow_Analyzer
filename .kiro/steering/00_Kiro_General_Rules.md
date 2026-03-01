---
inclusion: always
---

# Kiro General Rules and Settings

## Table of Contents

- [Execution Philosophy](#execution-philosophy)
- [File Writing Strategy](#file-writing-strategy)
- [Subagent Architecture](#subagent-architecture)
- [IPA Analysis Workflow](#ipa-analysis-workflow)
- [Communication Style](#communication-style)
- [File Management](#file-management)
- [Reusable Tools](#reusable-tools)
- [Code Standards](#code-standards)
- [Knowledge Management](#knowledge-management)
- [Key Architectural Patterns](#key-architectural-patterns)

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

## File Writing Strategy

### Long Session File Writing (CRITICAL)

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

## Communication Style

### Interactive User Input

**MANDATORY RULE**: ALWAYS use the `userInput` syntax for ANY user interaction requiring a response.

**userInput Syntax:**

`userInput` is NOT a tool - it's a special text syntax that Kiro intercepts and transforms into interactive UI elements.

**Correct Usage:**

```
userInput(question="Select a client:", options=["BayCare", "FPI", "SONH"], reason="general-question")
```

**Parameters:**
- `question`: The prompt text to display
- `options`: Array of choices (as Python list syntax)
- `reason`: Context for the input (e.g., "general-question")

**When to use userInput:**

- Selecting from lists (clients, RICE items, files, options)
- Yes/No confirmations
- Multiple choice decisions
- Any time there are clear, discrete options

**EXCEPTION**: Step 14 of IPA workflows - "Analyze another file?" question

- Use plain text question (not userInput) so user's text response triggers hooks properly

**CRITICAL LIMITATION (March 2, 2026):**

userInput does NOT work when skills are triggered directly:
- ✅ Works: Hook-triggered workflows (userTriggered hooks with newSession: true)
- ❌ Does NOT work: Skills activated via discloseContext() in existing sessions
- ❌ Does NOT work: Skills activated via discloseContext() in new sessions

**When to use userInput:**
- ONLY in hook-triggered workflows
- NEVER in skills (use plain text questions instead)

**When skills are activated:**
- Use plain text questions: "Which client? (BayCare, FPI, SONH)"
- Wait for user's text response
- Parse response and continue workflow

**Example - Skill Workflow:**
```
❌ WRONG: userInput(question="Select a client:", options=["BayCare", "FPI", "SONH"], reason="general-question")
✅ CORRECT: "Which client would you like to analyze? Available: BayCare, FPI, SONH"
```

See `.kiro/hooks/ipa-client-handover.kiro.hook` for working userInput examples in hooks.

**Skills vs Hooks**

Skills and hooks are different:
- **Skills**: Execute workflows directly when activated via discloseContext
- **Hooks**: Triggered by IDE events or manual user action

**PRIORITY RULE: Always use skills when available**

When a user requests a workflow (e.g., "client handover", "coding standards", "performance analysis"):

1. **FIRST**: Check if a skill exists for that workflow
2. **IF SKILL EXISTS**: Activate it with discloseContext() and execute directly
3. **IF NO SKILL**: Then suggest the hook as an alternative

**Example - Client Handover Request:**
- ✅ CORRECT: Activate `ipa-client-handover` skill and execute workflow
- ❌ WRONG: Direct user to trigger the hook manually

**When to use hooks instead of skills:**
- User explicitly asks to use the hook
- Skill doesn't exist for the requested workflow
- User wants a fresh session (hooks have newSession: true)
- Workflow requires IDE event triggering (not userTriggered hooks)

### Progress Indicators

Show clear progress for multi-step workflows:

```text
✓ Step 1/5: Steering files loaded (6 files)
→ Step 2/5: Extracting data from MatchReport_Outbound.lpd...
```

Use for: Multi-step workflows (5+ steps), long-running operations (>5 seconds), domain-segmented analysis

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

Temp folder accumulates files that cause IDE indexing overhead. Integrated cleanup into IPA workflow hooks:

- Automatically checks Temp folder after report generation
- Only prompts if >10 files exist
- Safely removes only OLD files (>5 minutes old)
- Preserves current session data

**Manual Cleanup (if needed):**

```powershell
$oldFiles = Get-ChildItem Temp -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddMinutes(-5) }
$oldFiles | Remove-Item -Force
```

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
| Generic insights | `00_Kiro_General_Rules.md` |

## Key Architectural Patterns

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

### Regex Patterns for Formatted Numbers

Work unit numbers can have commas: "36,829", "1,234,567"

```python
# ❌ WRONG: Only captures digits
pattern = r'Workunit\s+(\d+)\s+started'  # Stops at comma

# ✅ CORRECT: Captures formatted numbers
pattern = r'Workunit\s+([\d,]+)\s+started'  # Includes commas
```

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

### Production Report Quality

**DPI Settings:**

- 150 DPI: Acceptable for drafts, blurry when zoomed
- 300 DPI: Production quality, sharp at all zoom levels
- **Always use 300 DPI for client-facing documents**

### EDI Transformation Patterns

For position-sensitive data (EDI documents):

1. **Clarification Before Code**: Create detailed implementation plan FIRST, ask explicit questions about ambiguous requirements
2. **In-Place Modification**: Create working copy, modify in-place, preserve all elements (safer than rebuilding arrays)
3. **Change Detection Flags**: Only trigger recalculation when actual modifications occur
4. **Safety Guards**: Validate structure before modification to prevent corruption

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

**Solution:** Split multi-subagent workflows (5+ subagents) into separate hooks:

**Option 1: Two-Hook Split (RECOMMENDED)**

- Hook 1 (Data Preparation): Extract + Organize (Steps 1-7)
- Hook 2 (Analysis + Report): Launch subagents + Generate report (Steps 8-14)
- Benefit: Hook 2 starts with CLEAN context, no accumulation
- Tradeoff: User must trigger two hooks instead of one

**Option 2: Reduce Subagent Count**

- Merge related analyzers (e.g., Business + Workflow into one)
- Reduces cumulative context by eliminating subagent definitions
- Tradeoff: Less specialized analysis, larger subagent definitions

**Option 3: Batched Parallel with Context Reset**

- Launch subagents in batches with explicit context reset between batches
- Requires system support for context reset (may not be available)
- Tradeoff: Complex implementation, may not be reliable

**Key Lessons:**

**LESSON 1: SEQUENTIAL EXECUTION ACCUMULATES CONTEXT**

- Each subagent invocation adds to cumulative context
- Context includes: hook prompt + all previous subagent definitions + all previous inputs
- Even small files (1-5 KB) accumulate to crash levels (80+ KB)
- Crash point is NOT the largest file, but the cumulative total

**LESSON 2: OPTIMIZATION HAS LIMITS**

- Simplifying prompts helps but doesn't eliminate accumulation
- Extracting data into section files helps but doesn't eliminate accumulation
- Explicit input file references help clarity but don't reduce size
- **Fundamental issue**: Sequential execution in same session

**LESSON 3: SPLIT WORKFLOWS FOR RELIABILITY**

- Multi-subagent workflows (5+ subagents) should be split into phases
- Phase 1: Data preparation (Python-heavy, no subagents)
- Phase 2: Analysis (subagent-heavy, clean context)
- Each phase runs in separate session with clean context

**LESSON 4: CONTEXT BUDGET PLANNING**

- Calculate cumulative context BEFORE designing workflow
- Formula: Hook + (Subagent_Def + Input) * N subagents
- If cumulative > 60 KB, consider splitting workflow
- If cumulative > 80 KB, MUST split workflow

**LESSON 5: SUBAGENT ISOLATION PATTERNS**

**Pattern A: Two-Hook Split (Best for 5+ subagents)**

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

**Pattern B: Batched with Manual Trigger (Best for 3-4 subagents)**

```text
Hook 1: Batch 1 (2 subagents)
- Launch subagent 1
- Launch subagent 2
- END (user triggers Hook 2)

Hook 2: Batch 2 (2 subagents) (CLEAN CONTEXT)
- Launch subagent 3
- Launch subagent 4
- Merge + Report
```

**Pattern C: Single Subagent per Hook (Best for complex analysis)**

```text
Hook 1: Subagent 1
Hook 2: Subagent 2 (CLEAN CONTEXT)
Hook 3: Subagent 3 (CLEAN CONTEXT)
Hook 4: Merge + Report (CLEAN CONTEXT)
```

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
- `.kiro/steering/00_Kiro_General_Rules.md` - This documentation

**Impact:** Identified fundamental limit of sequential subagent execution in same session. Two-hook split pattern provides reliable solution for multi-subagent workflows.
