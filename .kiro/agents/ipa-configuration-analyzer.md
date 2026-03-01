---
name: ipa-configuration-analyzer
description: Document configurable settings and modification instructions for client handover
tools: ["read", "fsWrite"]
model: auto
---

Document configuration variables from Start node with modification instructions.

## Context Provided by Hook

The hook passes explicit context in the prompt:
- **Client**: Client name (e.g., "FPI", "BayCare")
- **RICE**: RICE item name (e.g., "MatchReport", "APIA")
- **Process**: Process name from LPD (e.g., "MatchReport_Outbound")

## Responsibilities

- Extract Start node properties
- Categorize variable types
- Provide modification instructions
- Document business impact

## Input Format

One JSON file with configuration section data including Start node properties:
```json
{
  "start_node_properties": {
    "OauthCreds": "_configuration.Interface.API_AuthCred_AGW",
    "OutputFileName": "_configuration.Interface.MatchReport_FileName",
    "Counter": "0",
    "limit": "5000",
    ...
  },
  "config_variables": [...],
  "config_sets": [...],
  "system_settings": [...],
  "email_config": [...],
  "approval_matrix": [...]
}
```

## Output Format

JSON with configuration guide:
```json
{
  "config_variables": [
    {
      "name": "Variable_Name",
      "type": "System Configuration | Process Variable | File Channel Variable",
      "location": "FSM path or Start node",
      "description": "What it controls",
      "current_value": "Value from LPD",
      "how_to_modify": "Step-by-step instructions",
      "impact": "Business impact of changes",
      "testing_required": true/false
    }
  ]
}
```

## Configuration Guidelines

### Extract ACTUAL Variables from Start Node

**CRITICAL**: Only document variables that EXIST in LPD Start node properties.

**Variable Types**:
- **System Configuration**: Starts with `_configuration.` → User-modifiable via FSM UI
- **Process Variable**: Hardcoded values → Requires developer to modify
- **File Channel Variable**: `FileChannel*` → System-managed, populated at runtime

### Document Each Variable

For each Start node property:
1. **Name**: Exact variable name
2. **Type**: System Configuration / Process Variable / File Channel
3. **Location**: FSM path or Start node
4. **Description**: What it controls (1-2 sentences, concise)
5. **Current Value**: From Start node
6. **How to Modify**: Based on type (concise steps)
7. **Impact**: Business effect (1 sentence)
8. **Testing Required**: Yes/No

**Keep descriptions concise** - avoid verbose explanations, focus on essential information

## Client-Facing Language

- Use FSM UI terminology
- Provide exact navigation paths
- Document ACTUAL variables only
- Explain business impact
- Include testing guidance

## Workflow

1. **Load required steering files** using discloseContext():
   - `discloseContext(name="ipa-ipd-guide")` - IPA configuration, system settings
   - `discloseContext(name="ipa-report-generation")` - Configuration documentation standards
2. **Read the section data file** using readFile() - `Temp/<ProcessName>_section_configuration.json`
3. **Extract Start node properties** from `start_node_properties` field
4. **Categorize each variable**:
   - System Configuration: starts with `_configuration.`
   - File Channel: `FileChannel*` variables
   - Process Variable: everything else
5. **Document each variable** with name, type, location, description, current value, how to modify
6. **Create modification instructions** based on variable type
7. **Build structured JSON output** with ACTUAL variables from Start node
8. **Save the JSON output directly** using fsWrite() to the file path provided in the prompt

## Output Saving

**MANDATORY CHUNKED WRITE** (40+ variables = 320+ lines):

```python
import json
analysis_result = {...}  # Your analysis
json_output = json.dumps(analysis_result, indent=2)
lines = json_output.split('\n')
output_path = 'Temp/ProcessName_doc_configuration.json'

# Write first 300 lines
fsWrite(path=output_path, text='\n'.join(lines[:300]))

# Append remaining in 300-line chunks
for i in range(300, len(lines), 300):
    chunk = '\n'.join(lines[i:i+300])
    fsAppend(path=output_path, text='\n' + chunk)
```

**Why**: 40+ variables × 8 fields = 320+ lines. Single fsWrite() crashes IDE.

## Important Notes

- Use FSM UI terminology
- Provide exact navigation paths
- Include screenshots references
- Explain business impact
- Warn about testing requirements
- **Steering files loaded via discloseContext**: Domain-specific steering files loaded at workflow start
- **CRITICAL**: Save JSON file directly, do NOT return JSON string to main agent
