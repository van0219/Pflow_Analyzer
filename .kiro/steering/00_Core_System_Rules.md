---
inclusion: always
---

# Core System Rules

## Table of Contents

- [Execution Philosophy](#execution-philosophy)
  - [Core Principles](#core-principles)
  - [Decision Matrix](#decision-matrix)
  - [Pre-Analysis Verification](#pre-analysis-verification)
- [Communication Guidelines](#communication-guidelines)
  - [User Interaction Patterns](#user-interaction-patterns)
  - [Progress Reporting](#progress-reporting)
- [File Operations](#file-operations)
  - [File Writing Strategy](#file-writing-strategy)
  - [Directory Structure](#directory-structure)
  - [Workspace Cleanup](#workspace-cleanup)
- [Code Standards](#code-standards)
  - [Python Conventions](#python-conventions)
  - [IPA JavaScript ES5](#ipa-javascript-es5)
- [Knowledge Management](#knowledge-management)
  - [Steering File Organization](#steering-file-organization)
  - [Keyword-Based Context Loading](#keyword-based-context-loading)
  - [Documentation Standards](#documentation-standards)
- [Architectural Patterns](#architectural-patterns)
  - [Template Modification](#template-modification)
  - [Data Flow Debugging](#data-flow-debugging)
  - [Report Quality Standards](#report-quality-standards)
  - [Common Pitfalls](#common-pitfalls)
- [Domain-Specific Workflows](#domain-specific-workflows)
  - [Client Handover Pipeline](#client-handover-pipeline)
  - [Coding Standards Pipeline](#coding-standards-pipeline)

## Execution Philosophy

### Core Principles

**ACT IMMEDIATELY** on clear directives. Don't overthink or ask unnecessary clarifying questions.

**STOP IMMEDIATELY** when user says "stop", "wait", "oh wait", or "hold on". Acknowledge and await new instructions.

### Decision Matrix

| Situation | Action |
|-----------|--------|
| Clear commands ("update X", "fix Y", "analyze Z") | Execute immediately |
| Routine operations (reading files, running scripts) | Execute immediately |
| Destructive operations (deleting files, dropping databases) | Confirm first |
| Ambiguous requests with multiple valid interpretations | Ask for clarification |
| User interruption signals ("stop", "wait", "hold on") | Stop all actions immediately |
| File operation returns "Operation was aborted" | Stop immediately, report status |

### Pre-Analysis Verification

Before performing ANY analysis task, verify these prerequisites:

1. All required files successfully read (no read errors)
2. No truncation warnings unresolved
3. Binary files handled with appropriate tools (`excel_reader.py` for Excel, not raw text reads)
4. Data structures complete and valid (no partial loads)

**If any prerequisite fails, STOP and resolve the issue before proceeding with analysis.**

## Communication Guidelines

### User Interaction Patterns

**CRITICAL LIMITATION**: The `userInput` tool has context-specific availability:

- ✅ Available: Hook-triggered workflows (userTriggered hooks with `newSession: true`)
- ❌ Unavailable: Skills activated via `discloseContext()` in any session

**When userInput is available:**

Use the `userInput` tool for structured choices:

```python
userInput(
    question="Select a client:",
    options=["BayCare", "FPI", "SONH"],
    reason="general-question"
)
```

**When userInput is unavailable (skills context):**

Use plain text questions and parse responses:

```text
Which option would you like? (A, B, or C)
```

Then wait for user's text response and parse accordingly.

### Progress Reporting

For multi-step workflows (5+ steps) or long operations (>5 seconds), show clear progress:

```text
✓ Step 1/5: Loaded steering files (6 files)
→ Step 2/5: Extracting data from MatchReport_Outbound.lpd...
```

Use progress indicators for:

- Multi-step workflows with 5+ distinct phases
- Long-running operations exceeding 5 seconds
- Domain-segmented analysis tasks

## File Operations

### File Writing Strategy

**Context-Aware Fallback Pattern**: In long sessions (10+ messages), direct `fsWrite` may fail due to context limitations. Use specialized tools:

**For Hook Files:**

Use `ReusableTools/hook_manager.py`:

```bash
python ReusableTools/hook_manager.py validate <hook_file>
python ReusableTools/hook_manager.py backup <hook_file>
```

Commands: `validate`, `backup`, `restore`, `analyze`, `repair`

**For Other Files:**

Use `file-writer-helper` subagent:

- Trigger after ANY `fsWrite` failure
- Use for large files (>200 lines)
- Use for multiple sequential edits

**CRITICAL**: The `file-writer-helper` subagent MUST NOT call `invokeSubAgent` (prevents infinite recursion).

**Fallback Workflow:**

1. Try direct `fsWrite` (if context is light AND not a hook file)
2. On first failure → Immediately delegate to appropriate tool
3. Do NOT retry `fsWrite` multiple times
4. Continue workflow without user intervention

**The user should never need to prompt you to continue after a file write failure.**

### Directory Structure

| Directory | Purpose | Git Tracking |
|-----------|---------|--------------|
| Workspace root | Master templates | Tracked |
| `Temp/` | Temporary scripts and intermediate files | Ignored (keep `.gitkeep`) |
| `Client_Handover_Results/` | Generated client handover reports | Ignored (keep `.gitkeep`) |
| `Coding_Standards_Results/` | Generated coding standards reports | Ignored (keep `.gitkeep`) |
| `Performance_Results/` | Generated performance reports | Ignored (keep `.gitkeep`) |
| `Credentials/` | API credentials and connection files | Ignored (NEVER commit) |

**Git Ignore Pattern:**

```gitignore
# Keep folder structure, ignore generated contents
Temp/*
!Temp/.gitkeep

Coding_Standards_Results/*
!Coding_Standards_Results/.gitkeep

Performance_Results/*
!Performance_Results/.gitkeep

Client_Handover_Results/*
!Client_Handover_Results/.gitkeep

Credentials/*
```

### Workspace Cleanup

The `Temp/` folder accumulates intermediate files that cause IDE indexing overhead.

**Automatic Cleanup Policy:**

- Check `Temp/` folder after operations
- Only prompt if >10 files exist
- Remove only OLD files (>5 minutes old)
- Preserve current session data

**Manual Cleanup (PowerShell):**

```powershell
$oldFiles = Get-ChildItem Temp -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddMinutes(-5) }
$oldFiles | Remove-Item -Force
```

## Code Standards

### Python Conventions

All Python scripts must follow these standards:

```python
#!/usr/bin/env python3

import sys
from pathlib import Path

# Dynamic import resolution
sys.path.append(str(Path(__file__).parent))

# ... script logic ...

if __name__ == "__main__":
    main()
```

**Key Requirements:**

- Include shebang: `#!/usr/bin/env python3`
- Include main guard: `if __name__ == "__main__":`
- Use `sys.path` resolution for dynamic imports
- Convert sets to lists before JSON serialization
- Prefer specialized libraries (pandas, numpy, matplotlib) over basic implementations

### IPA JavaScript ES5

**CRITICAL**: IPA JavaScript nodes execute in ES5 environment. Modern syntax causes immediate runtime errors.

**ES5 Compliance Checklist:**

| Feature | ES5 Compliant | Modern (Forbidden) |
|---------|---------------|-------------------|
| Variables | `var x = 1;` | `let x = 1;` `const x = 1;` |
| Functions | `function f() {}` | `() => {}` `async/await` |
| Strings | `"Hello " + name` | `` `Hello ${name}` `` |
| Assignment | `var x = obj.prop;` | `var {prop} = obj;` |
| Loops | `for (var i = 0; i < n; i++)` | `arr.map()` `arr.filter()` |
| Parameters | Check inside function | `function f(x = 1)` |
| Conditionals | `var x = cond ? a : b;` ✅ | N/A |

**IPA Assign Node Architecture:**

```javascript
// Entire script wrapped in function
function transformImport(importFileContent, fileName) {
    // Configuration variables INSIDE function
    var CONFIG_VALUE = "setting";
    
    // ... transformation logic ...
    
    // NO top-level return statements
}

// Function invoked at end
transformImport(ImportFile, FileName);
```

**Production Safety Patterns:**

1. **Floating Point Comparison** - Always round before comparison:

   ```javascript
   var roundedSum = roundToDecimals(sumQty, ROUND_DECIMALS);
   if (roundedSum === 0) { /* safe comparison */ }
   ```

2. **Null/Undefined Guards** - Validate inputs:

   ```javascript
   if (!inputFileContent || typeof inputFileContent !== "string") {
       inputFileContent = "";
   }
   ```

3. **Defensive Division** - Check denominator:

   ```javascript
   if (originalQuantity === 0) {
       exceptions.push({error: "Division by zero"});
       continue;
   }
   var unitCost = extendedAmount / originalQuantity;
   ```

## Knowledge Management

### Steering File Organization

| Domain | Steering File | Keywords |
|--------|---------------|----------|
| Workflow engineering | `01_Workflow_Engineering_Principles.md` | workflow, subagent, orchestration |
| IPA/IPD fundamentals | `02_IPA_and_IPD_Complete_Guide.md` | IPA, IPD, LPD, process designer |
| Work unit analysis | `03_Work_Unit_Analysis.md` | wu, log, work unit, error |
| Process patterns | `04_Process_Patterns_Library.md` | approval, workflow, pattern |
| WU report generation | `05_WU_Report_Generation.md` | wu report, performance, analysis |
| Compass SQL | `06_Compass_SQL_CheatSheet.md` | SQL, Compass, Data Fabric |
| FSM business classes | `07_FSM_Business_Classes_and_API.md` | FSM, Landmark, business class, API |
| Data Fabric/ION | `08_Infor_OS_Data_Fabric_Guide.md` | Data Fabric, ION, BOD, Data Lake |
| IDM integration | `09_Infor_IDM_Guide.md` | IDM, document, ContentDocument |
| FSM navigation | `10_FSM_Navigation_Guide.md` | FSM UI, navigation, Playwright |
| IPA reports | `11_IPA_Report_Generation.md` | client handover, coding standards |
| RICE methodology | `12_RICE_Methodology_and_Specifications.md` | RICE, ANA-050, DES-020 |
| External API OAuth2 | `13_External_API_OAuth2_Integration_Guide.md` | OAuth2, external API, third-party |
| Agent automation | `14_Kiro_Agent_Automation_Guide.md` | hook, skill, power, automation |

### Keyword-Based Context Loading

**BLOCKING REQUIREMENT**: Before proceeding with user requests, detect task-specific keywords and load appropriate steering files FIRST.

**Keyword Detection Rules:**

📊 **WORK UNIT ANALYSIS** - Keywords: `wu`, `log`, `work unit`, `error`

Load: `03_Work_Unit_Analysis.md`, `05_WU_Report_Generation.md`

🔍 **CODING STANDARDS** - Keywords: `coding standards`, `peer review`, `LPD`, `analyze process`

Load: `02_IPA_and_IPD_Complete_Guide.md`, `03_Work_Unit_Analysis.md`, `04_Process_Patterns_Library.md`, `06_Compass_SQL_CheatSheet.md`, `11_IPA_Report_Generation.md`, `12_RICE_Methodology_and_Specifications.md`

📋 **CLIENT HANDOVER** - Keywords: `client handover`, `documentation`, `handover report`

Load: `02_IPA_and_IPD_Complete_Guide.md`, `11_IPA_Report_Generation.md`, `12_RICE_Methodology_and_Specifications.md`

🔧 **FSM/LANDMARK API** - Keywords: `FSM`, `Landmark`, `business class`, `WebRun`, `API`

Load: `07_FSM_Business_Classes_and_API.md`, `02_IPA_and_IPD_Complete_Guide.md`

💾 **DATA FABRIC** - Keywords: `Compass SQL`, `Data Fabric`, `Data Lake`, `ION`, `BOD`

Load: `06_Compass_SQL_CheatSheet.md`, `08_Infor_OS_Data_Fabric_Guide.md`

📄 **IDM** - Keywords: `IDM`, `document management`, `ContentDocument`, `CaptureDocument`

Load: `09_Infor_IDM_Guide.md`, `02_IPA_and_IPD_Complete_Guide.md`

🌐 **EXTERNAL API** - Keywords: `OAuth2`, `external API`, `Lightspeed`, `Stripe`, `third-party`

Load: `13_External_API_OAuth2_Integration_Guide.md`

🤖 **AUTOMATION** - Keywords: `hook`, `skill`, `power`, `steering`, `spec`, `automation`

Load: `14_Kiro_Agent_Automation_Guide.md`

🎯 **RICE SPECS** - Keywords: `RICE`, `ANA-050`, `DES-020`, `functional spec`, `technical spec`

Load: `12_RICE_Methodology_and_Specifications.md`

**If no keywords detected, proceed with the original request.**

### Documentation Standards

**MANDATORY Front Matter Requirements:**

ALL steering files MUST include front matter with this EXACT format:

```yaml
---
inclusion: auto
name: short-kebab-case-name
description: Brief description of what this steering file covers and when to use it.
---
```

**Front Matter Rules:**

- `inclusion: auto` is MANDATORY for all steering files (NOT "always", NOT just "auto" alone)
- `name:` MUST be a short, kebab-case identifier (e.g., "process-patterns", "ipa-report-generation")
- `description:` MUST explain what the file covers and when to activate it
- Front matter MUST be followed by a blank line before the main title

**Example:**

```markdown
---
inclusion: auto
name: process-patterns
description: IPA process patterns library with 450+ analyzed workflows. Use when creating new LPD files or analyzing existing processes.
---

# Process Patterns Library
```

**Table of Contents Requirements:**

All steering files MUST include a proper TOC:

- Place TOC immediately after main title (H1)
- Use markdown anchor links: `[Section Name](#section-name)`
- Include all H2 sections as top-level TOC items
- Include H3 sections as nested items (2-space indentation)

**Steering File Updates:**

When establishing new patterns or approaches, update relevant steering files in `.kiro/steering/`.

## Architectural Patterns

### Template Modification

**CRITICAL RULE**: Never modify working templates without verification.

**Before modifying ANY template or working code:**

1. Verify what it ALREADY supports
2. Read existing code carefully
3. Look for similar patterns already implemented
4. Test with existing code first

**Root Cause Principle**: Most "template issues" are actually data flow issues upstream. Fix the data source, not the template.

### Data Flow Debugging

When reports have missing data, trace the pipeline from source to destination:

```text
extraction → organization → analysis → merge → consolidation → generate → template
```

**Debugging Steps:**

1. Identify where data exists vs where code looks for it
2. Use `excel_reader.py` to inspect actual Excel contents
3. Verify data structure at each pipeline stage
4. Fix at the source, not at the destination

### Report Quality Standards

**DPI Settings for Client-Facing Documents:**

| DPI | Quality | Use Case |
|-----|---------|----------|
| 150 | Acceptable for drafts | Blurry when zoomed |
| 300 | Production quality | Sharp at all zoom levels ✅ |

**Always use 300 DPI for client-facing documents.**

### Common Pitfalls

#### Matplotlib Emoji Rendering

**Problem**: Matplotlib cannot render emojis, causing corrupted diagram output.

**Solution**: Strip ALL emojis before rendering:

```python
import re

def remove_emojis(text):
    """Remove emojis to prevent matplotlib rendering issues"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002300-\U000023FF"  # misc technical
        u"\U00002600-\U000027BF"  # misc symbols
        u"\U00002702-\U000027B0"  # dingbats
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # supplemental
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text).strip()
```

**Emoji Usage Guidelines:**

| Context | Emojis Allowed |
|---------|----------------|
| Excel sheet names | ✅ Yes |
| Excel cell content | ✅ Yes |
| Matplotlib diagrams | ❌ No |
| Python logging/console | ✅ Yes |

#### Nested Data Flattening

**Problem**: Using `str(dict)` creates unreadable JSON strings in Excel.

**Solution**: Extract meaningful fields from nested structures:

```python
# ❌ BAD: Unreadable JSON strings
for key, value in data.items():
    if isinstance(value, (dict, list)):
        cell.value = str(value)

# ✅ GOOD: Flatten nested structures
if 'nested_section' in data:
    section = data['nested_section']
    for field_name, field_value in section.items():
        row_data.append((field_name, field_value, status))
```

#### Regex for Formatted Numbers

**Problem**: Work unit numbers can have commas: "36,829", "1,234,567"

**Solution**: Include commas in regex pattern:

```python
# ❌ WRONG: Stops at comma
pattern = r'Workunit\s+(\d+)\s+started'

# ✅ CORRECT: Captures formatted numbers
pattern = r'Workunit\s+([\d,]+)\s+started'
```

#### Duplicate Formatting in Data Pipeline

**Problem**: Formatting applied in multiple places causes duplication (e.g., double check marks "✓ ✓").

**Solution**: Apply formatting in ONE place only - preferably the template:

```python
# ❌ BAD: Generation function adds formatting
def generate_key_features(data):
    return [f"✓ {feature}" for feature in features]

# Template also adds formatting
ws[f'A{row}'] = f"✓ {feature}"  # Results in "✓ ✓ Feature"

# ✅ GOOD: Generation function returns plain text
def generate_key_features(data):
    return features  # No formatting

# Template handles ALL formatting
ws[f'A{row}'] = f"✓ {feature}"  # Results in "✓ Feature"
```

**Rule**: Let templates handle visual elements (check marks, emojis, colors). Data functions should return plain content.

#### Template Data Structure Mismatch

**Problem**: Assembly script passes data in one format, but template expects a different format.

**Example**: System Configuration sheet empty because template expects list-of-lists but receives list-of-dicts.

**Solution**: Verify template expectations BEFORE passing data:

```python
# ❌ BAD: Assume template accepts any format
configuration_data = [
    {"variable": "OauthCreds", "value": "...", "purpose": "..."},
    {"variable": "OutputFile", "value": "...", "purpose": "..."}
]

# ✅ GOOD: Convert to format template expects
# Template expects: [["Variable", "Value", "Purpose"], ["OauthCreds", "...", "..."]]
configuration_data = [
    ["Variable Name", "Value", "Purpose"],
    ["OauthCreds", "...", "..."],
    ["OutputFile", "...", "..."]
]
```

**Debugging Steps**:

1. Read template code to see what data structure it expects
2. Check if data is accessed as `row[0]` (list) or `row['field']` (dict)
3. Convert data format in assembly script, not in template
4. Verify output by inspecting generated Excel file

**Common Template Expectations**:

- **LEGACY templates**: Expect list-of-lists `[["col1", "col2"], ["val1", "val2"]]`
- **MODERN templates**: Accept list-of-dicts `[{"col1": "val1", "col2": "val2"}]`
- **Check template code**: Look for `row[0]` vs `row.get('field')` to determine format

#### Missing Data Enrichment

**Problem**: Raw LPD data lacks human-readable descriptions needed for client documentation.

**Example**: Process sheet shows activity IDs and types but "Description" column is empty (NaN).

**Solution**: Enrich raw data with descriptions BEFORE passing to template:

```python
# ❌ BAD: Pass raw LPD data directly
activities = process.get('activities', [])  # Only has id, type, caption

# ✅ GOOD: Enrich with descriptions
enriched_activities = []
for activity in process.get('activities', []):
    activity_type = activity.get('type', '')
    
    # Add type-based description
    type_descriptions = {
        'START': 'Process entry point - initializes variables',
        'ASSGN': 'Variable assignment - executes JavaScript',
        'WEBRN': 'HTTP API call - external web service',
        'BRANCH': 'Conditional routing - directs flow'
    }
    
    enriched_activities.append({
        'id': activity.get('id'),
        'type': activity_type,
        'caption': activity.get('caption'),
        'description': type_descriptions.get(activity_type, f'{activity_type} activity'),
        'when_it_runs': 'Sequential execution - after previous activity'
    })
```

**Rule**: Raw extraction data is for machines. Client documentation needs enriched, human-readable content.

# ✅ CORRECT: Captures formatted numbers
pattern = r'Workunit\s+([\d,]+)\s+started'
```

#### EDI Transformation Patterns

For position-sensitive data (EDI documents):

1. **Clarification Before Code**: Create detailed implementation plan FIRST
2. **In-Place Modification**: Modify working copy, preserve all elements
3. **Change Detection Flags**: Only recalculate when modifications occur
4. **Safety Guards**: Validate structure before modification

#### Excel Sheet Name Limits

**Problem**: Excel has a 31-character limit for sheet names. Long process names or duplicate names after truncation cause workbook corruption.

**Root Cause**: When multiple processes have long names, simple truncation creates duplicates:
- `InvoiceApproval_APIA_NONPOROUTING` → `⚙️ InvoiceApproval_APIA_NONPORO` (31 chars)
- `InvoiceApproval_APIA_NONPOROUTING_Reject` → `⚙️ InvoiceApproval_APIA_NONPORO` (DUPLICATE!)

Excel rejects duplicate sheet names, causing corruption with error: "Repaired Records: Worksheet properties from /xl/workbook.xml part (Workbook)"

**Solution**: Implement intelligent sheet name generation with collision detection:

```python
def create_process_sheet(wb, process, idx):
    """Create individual process sheet with unique name"""
    process_name = process.get('name', f'Process {idx}')
    base_sheet_name = f"⚙️ {process_name}"
    
    # Excel sheet name limit is 31 chars - ensure uniqueness
    if len(base_sheet_name) > 31:
        # Truncate and add index to ensure uniqueness
        max_name_length = 28 - len(str(idx))
        sheet_name = f"{base_sheet_name[:max_name_length]}{idx}"
    else:
        sheet_name = base_sheet_name
    
    # Ensure sheet name is unique (collision detection)
    existing_names = [sheet.title for sheet in wb.worksheets]
    if sheet_name in existing_names:
        counter = 1
        while f"{sheet_name[:29]}{counter}" in existing_names:
            counter += 1
        sheet_name = f"{sheet_name[:29]}{counter}"
    
    ws = wb.create_sheet(sheet_name)
    return ws
```

**Key Protection Layers**:

1. **Length Check**: Truncate if >31 characters
2. **Index Suffix**: Add process index for uniqueness
3. **Collision Detection**: Check existing sheet names before creating
4. **Counter Fallback**: Add numeric suffix if collision still occurs

**Result**: Sheet names like `⚙️ InvoiceApproval_APIA_NON1`, `NON2`, `NON3` - all unique and under 31 characters.

**Prevention**: Always use this pattern when creating dynamic sheet names in Excel templates.

## Domain-Specific Workflows

### Client Handover Pipeline

**BLOCKING REQUIREMENT**: When generating client handover documentation, use the `ipa-client-handover` skill.

**Activation**:

```text
/ipa-client-handover
```

Or mention "client handover documentation" in your request.

**Architecture**: Incremental Pipeline (Crash-Safe)

The skill uses an incremental, file-based pipeline to prevent context accumulation and crashes:

**Phase 0 (Preprocessing - Python Only):**

```bash
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py <lpd> <spec> [wu_log]
```

Creates: `lpd_structure.json`, `metrics_summary.json`, `spec_raw.json`, `wu_log_data.json` (if provided)

**Phase 1 (Business Analysis - AI Direct):**

AI analyzes spec_raw.json directly (~7 KB output acceptable)
- Output: `business_analysis.json`

**Phase 2 (Workflow Analysis - Incremental):**

```bash
python ReusableTools/IPA_ClientHandover/build_workflow_analysis.py
```

1. Python extracts activities and creates chunks (50 activities each)
2. AI analyzes each chunk (~2-3 KB output per chunk)
3. AI saves as `workflow_chunk_N_analyzed.json`
4. Run merge: `python ReusableTools/IPA_ClientHandover/build_workflow_analysis.py merge`
5. Output: `workflow_analysis.json`

**Phase 3 (Configuration Analysis - Incremental):**

```bash
python ReusableTools/IPA_ClientHandover/build_configuration_analysis.py
```

1. Python extracts config by category (process variables, file channels, web services)
2. AI analyzes each category (~1-2 KB output per category)
3. AI saves as `config_chunk_CATEGORY_analyzed.json`
4. Run merge: `python ReusableTools/IPA_ClientHandover/build_configuration_analysis.py merge`
5. Output: `configuration_analysis.json`

**Phase 4 (Risk Assessment - Incremental):**

```bash
python ReusableTools/IPA_ClientHandover/build_risk_assessment.py
```

1. Python loads previous outputs and creates risk chunks by category
2. AI analyzes each category (~1-2 KB output, 3-5 risks max per category)
3. AI saves as `risk_chunk_CATEGORY_analyzed.json`
4. Run merge: `python ReusableTools/IPA_ClientHandover/build_risk_assessment.py merge`
5. Output: `risk_assessment.json`

**Phase 5 (Report Assembly - Python Only):**

```bash
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py <client> <rice>
```

**Key Benefits**:

- ✅ No large AI outputs (max 3 KB per response, was 11 KB causing crashes)
- ✅ No context accumulation (each chunk isolated at ~2-3 KB)
- ✅ Crash-safe (can resume from any chunk)
- ✅ Scalable (works for 50 or 5,000 activities)
- ✅ Multi-process support (1-N LPDs → ONE report)

**Critical Rule: AI Output Size Limits**

| Phase | Max Output per Chunk | Chunk Count | Total Output |
|-------|---------------------|-------------|--------------|
| Phase 1 | 7 KB | 1 | ~7 KB |
| Phase 2 | 3 KB | 11 | ~33 KB |
| Phase 3 | 2 KB | 5 | ~10 KB |
| Phase 4 | 2 KB | 5 | ~10 KB |
| **Total** | **~2.5 KB avg** | **22** | **~60 KB** |

**Previous Architecture (Crashed)**: Phase 4 tried to generate 11 KB in one response → CRASH at 6m 13s

**Common Mistake**: Skipping Phase 0 and manually extracting data

Results in:

- Missing `lpd_structure.json` and `metrics_summary.json`
- Assembly script shows "Process Count: 0" and "Total Activities: 0"
- Incomplete report

**Pre-Phase 5 Verification Checklist:**

- `Temp/lpd_structure.json` exists
- `Temp/metrics_summary.json` exists
- `Temp/business_analysis.json` exists
- `Temp/workflow_analysis.json` exists (with `activity_descriptions` and `activity_purposes`)
- `Temp/configuration_analysis.json` exists
- `Temp/risk_assessment.json` exists

**CRITICAL: Phase 2 (workflow_analysis.json) Requirements:**

The `workflow_analysis.json` file MUST include `activity_descriptions` and `activity_purposes` dictionaries for comprehensive activity documentation:

```json
{
  "activity_descriptions": {
    "activity_id": "Specific description based on JavaScript/SQL/branch analysis"
  },
  "activity_purposes": {
    "activity_id": "When and why this activity runs"
  }
}
```

**How to Generate Activity Descriptions:**

1. Read `Temp/lpd_structure.json` completely to get all JavaScript blocks, SQL queries, and branch conditions
2. For EACH activity (all 39 real activities, excluding empty connectors):
   - ASSGN: Analyze JavaScript code to describe transformations, extractions, validations
   - WEBRN: Analyze SQL queries and API endpoints to describe data operations
   - BRANCH: Analyze branch conditions to describe routing logic
   - Timer: Describe wait duration and purpose
   - ACCFIL: Describe file operations (read/write/delete)
   - SUBPROC: Describe subprocess purpose
3. Use business-friendly language focused on WHAT, not HOW
4. Include specific details: field names, API endpoints, transformation logic, error conditions

**Assembly Script Priority Order:**

1. **PRIORITY 1**: `activity_descriptions[activity_id]` and `activity_purposes[activity_id]` (RECOMMENDED)
2. **PRIORITY 2**: `workflow_steps` matching (legacy fallback)
3. **PRIORITY 3**: Generic type-based descriptions (last resort)

**Reference**: See `.kiro/steering/11_IPA_Report_Generation.md` for complete workflow documentation and `.kiro/skills/ipa-client-handover/` for skill implementation.

### Coding Standards Pipeline

**BLOCKING REQUIREMENT**: When performing coding standards analysis, use the `ipa-coding-standards` skill.

**Activation**:

```text
/ipa-coding-standards
```

Or mention "coding standards analysis" in your request.

**Architecture**: Stateless Pipeline with Direct AI Analysis

The skill uses a hybrid approach that's simpler than Client Handover:

**Phase 0 (Preprocessing - Python Only):**

```bash
python ReusableTools/IPA_CodingStandards/preprocess_coding_standards.py <lpd> <client>
```

Creates: `lpd_structure.json`, `metrics_summary.json`, `project_standards.json`, and 5 domain JSON files

**Phase 1-5 (AI Analysis - Direct):**

AI analyzes each domain JSON file directly (no incremental scripts needed):
- Phase 1: Naming conventions (`domain_naming.json`)
- Phase 2: JavaScript ES5 compliance (`domain_javascript.json`)
- Phase 3: SQL queries (`domain_sql.json`)
- Phase 4: Error handling (`domain_errorhandling.json`)
- Phase 5: Process structure (`domain_structure.json`)

Each phase reads the domain JSON + `project_standards.json` and writes an analysis JSON.

**Phase 6 (Report Assembly - Python Only):**

```bash
python ReusableTools/IPA_CodingStandards/merge_violations.py Temp/<ProcessName>
# Then use existing build_ipa_data_helper.py and template
```

**Key Benefits:**

- ✅ No context accumulation (domain files already small ~200-400 lines)
- ✅ No crashes (stable execution)
- ✅ Simpler than Client Handover (no incremental chunking scripts needed)
- ✅ Project standards integration (client-specific rules override defaults)
- ✅ One process at a time (generates ONE Excel report per process)

**Why This Works:**

`organize_by_domain.py` already chunks data into 5 small domain files during Phase 0. Each domain file is small enough for direct AI analysis without additional chunking.

**Reference**: See `.kiro/steering/11_IPA_Report_Generation.md` for complete workflow documentation and `.kiro/skills/ipa-coding-standards/` for skill implementation.
