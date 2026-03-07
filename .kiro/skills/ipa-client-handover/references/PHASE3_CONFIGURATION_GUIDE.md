# Phase 3: Configuration Analysis Guide

## Critical Requirements

Phase 3 (`configuration_analysis.json`) is the MOST CRITICAL phase for System Configuration sheet population. The assembly script's `build_ipa_data()` function expects specific data structures.

## Required Data Structures

### 1. file_channel_config

**Purpose**: File channel variables that trigger the process

**Structure**: List of dictionaries

```json
{
  "file_channel_config": [
    {
      "variable": "FileChannelFileName",
      "purpose": "Name of the trigger file being processed",
      "example_value": "MatchReportTrigger_P962_FMFC20260116233831.txt",
      "modification_instructions": "Automatically populated by file channel - no manual modification needed"
    },
    {
      "variable": "FileChannelMonitorDirectory",
      "purpose": "Directory path monitored by file channel for trigger files",
      "example_value": "/ACA/FMFC/Match/Input",
      "modification_instructions": "Configure in Process Server Administrator > File Channels > Monitor Directory"
    },
    {
      "variable": "FileChannelProcessedFileDirectory",
      "purpose": "Directory where file channel moves processed files",
      "example_value": "/ACA/FMFC/Match/Input",
      "modification_instructions": "Configure in Process Server Administrator > File Channels > Processed Directory"
    }
  ]
}
```

**How to Extract**:

1. Read `lpd_structure.json`
2. Find START activity
3. Look for properties with "FileChannel" in the name
4. Extract: `FileChannelFileName`, `FileChannelMonitorDirectory`, `FileChannelProcessedFileDirectory`

### 2. process_variables

**Purpose**: Variables initialized in START activity

**Structure**: List of dictionaries

```json
{
  "process_variables": [
    {
      "variable": "OauthCreds",
      "purpose": "Selected OAuth credentials based on Finance Enterprise Group",
      "example_value": "JSON string with client_id, client_secret, grant_type, scope",
      "modification_instructions": "Automatically selected from Interface config based on FEG - update source config variables instead"
    },
    {
      "variable": "OutputFileName",
      "purpose": "Base name for output file (timestamp appended at runtime)",
      "example_value": "Match",
      "modification_instructions": "Update System Configuration > Interface > MatchReport_FileName"
    },
    {
      "variable": "limit",
      "purpose": "Number of records to retrieve per API call (pagination)",
      "example_value": "5000",
      "modification_instructions": "Hardcoded in START activity - modify START properties if different page size needed"
    }
  ]
}
```

**How to Extract**:

1. Read `lpd_structure.json`
2. Find START activity properties
3. Extract all variable assignments (key-value pairs)
4. For each variable, determine:
   - Purpose (what it's used for)
   - Example value (from properties or typical value)
   - Modification instructions (where to change it)

### 3. configuration_dependencies

**Purpose**: System Configuration properties referenced in the process

**Structure**: List of dictionaries

```json
{
  "configuration_dependencies": [
    {
      "config_set": "Interface",
      "property": "API_AuthCred_AGW",
      "purpose": "OAuth2 credentials for AGW Finance Enterprise Group",
      "modification_instructions": "Update in System Configuration > Interface. JSON format: {\"client_id\":\"...\",\"client_secret\":\"...\",\"grant_type\":\"client_credentials\",\"Tenant\":\"...\",\"Webroot\":\"...\",\"WebrootAccessToken\":\"...\",\"WebrootAccessTokenWebProgram\":\"...\"}"
    },
    {
      "config_set": "Interface",
      "property": "MatchReport_FileName",
      "purpose": "Base name for output CSV file (timestamp appended at runtime)",
      "modification_instructions": "Update in System Configuration > Interface. Example value: 'Match' results in Match_YYMMDD_HHMMSS.csv"
    }
  ]
}
```

**How to Extract**:

1. Read `lpd_structure.json`
2. Search for `_configuration.` references in JavaScript blocks
3. Extract pattern: `_configuration.{ConfigSet}.{Property}`
4. For each reference, determine:
   - Config set (e.g., "Interface")
   - Property name (e.g., "API_AuthCred_AGW")
   - Purpose (what it's used for)
   - Modification instructions (how to update it)

## Root Cause of Empty Configuration Sheets

**Problem**: System Configuration sheet is empty or shows "Config variables: 0"

**Root Cause**: Phase 3 `configuration_analysis.json` is missing required data structures

**Solution**: Ensure Phase 3 extracts all three required structures:

```python
# Verify Phase 3 output
import json
data = json.load(open('Temp/configuration_analysis.json'))
print('file_channel_config:', len(data.get('file_channel_config', [])))
print('process_variables:', len(data.get('process_variables', [])))
print('configuration_dependencies:', len(data.get('configuration_dependencies', [])))
```

Expected output:
```
file_channel_config: 3
process_variables: 10
configuration_dependencies: 7
```

## Assembly Script Priority Order

The `build_ipa_data()` function uses this priority order:

1. **PRIORITY 1**: `file_channel_config`, `process_variables`, `configuration_dependencies`
2. **PRIORITY 2**: `configuration_items` (legacy fallback)
3. **PRIORITY 3**: Empty configuration (last resort)

## Extraction Patterns

### Pattern 1: File Channel Variables

```python
# From lpd_structure.json
start_activity = next(a for a in activities if a['type'] == 'START')
properties = start_activity['properties']

file_channel_config = []
for key, value in properties.items():
    if 'FileChannel' in key:
        file_channel_config.append({
            'variable': key,
            'purpose': f"File channel {key.replace('FileChannel', '').lower()}",
            'example_value': value or "Set by file channel",
            'modification_instructions': "Configure in Process Server Administrator"
        })
```

### Pattern 2: Process Variables

```python
# From lpd_structure.json START activity
process_variables = []
for key, value in properties.items():
    if key not in ['FileChannelFileName', 'FileChannelMonitorDirectory', 'FileChannelProcessedFileDirectory']:
        process_variables.append({
            'variable': key,
            'purpose': f"Process variable for {key}",
            'example_value': value or "Set at runtime",
            'modification_instructions': "Update START activity properties or System Configuration"
        })
```

### Pattern 3: Configuration Dependencies

```python
# From lpd_structure.json JavaScript blocks
import re
config_pattern = r'_configuration\.(\w+)\.(\w+)'

configuration_dependencies = []
for js_block in javascript_blocks:
    matches = re.findall(config_pattern, js_block['code'])
    for config_set, property_name in matches:
        configuration_dependencies.append({
            'config_set': config_set,
            'property': property_name,
            'purpose': f"Configuration property for {property_name}",
            'modification_instructions': f"Update System Configuration > {config_set} > {property_name}"
        })
```

## Validation Before Assembly

Run this validation BEFORE Phase 5:

```bash
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

Expected output:
```
✓ configuration_analysis.json: Valid
  - file_channel_config: 3 items
  - process_variables: 10 items
  - configuration_dependencies: 7 items
```

## Common Mistakes

❌ **WRONG**: Using generic field names

```json
{
  "configuration_items": [...]  // Assembly script doesn't prioritize this
}
```

✅ **CORRECT**: Using specific field names

```json
{
  "file_channel_config": [...],
  "process_variables": [...],
  "configuration_dependencies": [...]
}
```

❌ **WRONG**: Missing modification instructions

```json
{
  "variable": "OauthCreds",
  "purpose": "OAuth credentials"
  // Missing: modification_instructions
}
```

✅ **CORRECT**: Complete structure

```json
{
  "variable": "OauthCreds",
  "purpose": "OAuth credentials for API authentication",
  "example_value": "{\"client_id\":\"...\"}",
  "modification_instructions": "Update System Configuration > Interface > API_AuthCred_{FEG}"
}
```

## Template Expectations

The template (`ipa_client_handover_template.py`) expects:

1. **System Configuration Variables** section:
   - Populated from `configuration_dependencies`
   - Format: Variable Name | Location | Description | Current Value | How to Modify

2. **File Channel Configuration** section:
   - Populated from `file_channel_config`
   - Format: Variable Name | Location | Description | Current Value | How to Modify

3. **Process Variables** section:
   - Populated from `process_variables`
   - Format: Variable Name | Default Value | Purpose | How to Modify

## Best Practices

1. **Always run Phase 0 first** - Provides `lpd_structure.json` with all data
2. **Extract from source** - Don't infer or guess configuration values
3. **Include modification instructions** - Tell users HOW to change settings
4. **Use example values** - Show realistic values, not placeholders
5. **Validate before assembly** - Catch structure issues early

## Related Documentation

- `JSON_SCHEMAS.md` - Complete JSON structure reference
- `TROUBLESHOOTING.md` - Common issues and solutions
- `TOOLS_README.md` - Tool usage and examples
