# Common Issues and Solutions

This document catalogs common issues encountered during client handover report generation and their solutions.

## Table of Contents

- [Excel File Issues](#excel-file-issues)
- [Template Issues](#template-issues)
- [Data Structure Issues](#data-structure-issues)
- [Performance Issues](#performance-issues)

## Excel File Issues

### Issue: Excel File Corruption - "Repaired Records: Worksheet properties"

**Symptoms:**
- Excel shows recovery dialog when opening file
- Sheets named "Recovered Sheet1", "Recovered Sheet2", etc.
- Error message: "Repaired Records: Worksheet properties from /xl/workbook.xml part (Workbook)"

**Root Cause:**
Duplicate sheet names caused by truncating long process names to Excel's 31-character limit.

**Example:**
```
InvoiceApproval_APIA_NONPOROUTING → ⚙️ InvoiceApproval_APIA_NONPORO (31 chars)
InvoiceApproval_APIA_NONPOROUTING_Reject → ⚙️ InvoiceApproval_APIA_NONPORO (DUPLICATE!)
```

**Solution:**
The template now implements intelligent sheet name generation with collision detection:

```python
def create_process_sheet(wb, process, idx):
    """Create individual process sheet with unique name"""
    process_name = process.get('name', f'Process {idx}')
    base_sheet_name = f"⚙️ {process_name}"
    
    # Excel sheet name limit is 31 chars - ensure uniqueness
    if len(base_sheet_name) > 31:
        max_name_length = 28 - len(str(idx))
        sheet_name = f"{base_sheet_name[:max_name_length]}{idx}"
    else:
        sheet_name = base_sheet_name
    
    # Collision detection
    existing_names = [sheet.title for sheet in wb.worksheets]
    if sheet_name in existing_names:
        counter = 1
        while f"{sheet_name[:29]}{counter}" in existing_names:
            counter += 1
        sheet_name = f"{sheet_name[:29]}{counter}"
    
    ws = wb.create_sheet(sheet_name)
    return ws
```

**Prevention:**
- Always use index-based naming for multi-process reports
- Check for existing sheet names before creating new ones
- Test with long process names during development

**Fixed In:** `ipa_client_handover_template.py` (2026-03-07)

---

### Issue: Permission Denied When Regenerating Report

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'Client_Handover_Results/BayCare_APIA.xlsx'
```

**Root Cause:**
The Excel file is open in Excel or another application.

**Solution:**
1. Close the Excel file
2. Regenerate the report
3. If file is locked by another process, use Task Manager to close Excel

**Prevention:**
- Close Excel files before regenerating
- Use validation scripts that don't lock files
- Consider adding file lock detection to assembly script

---

## Template Issues

### Issue: Missing Priority Values in Business Requirements

**Symptoms:**
- Priority column shows empty cells for some requirements
- Priority cells appear white/blank despite having data

**Root Cause:**
Priority color mapping in template doesn't include all priority levels used in analysis data.

**Example:**
```python
# ❌ INCOMPLETE: Missing "Critical" priority
priority_colors = {
    'High': 'FF6B6B',
    'Medium': 'FFA500',
    'Low': '4ECDC4'
}

# When priority is "Critical", defaults to white ('FFFFFF')
# White text on white background = invisible
```

**Solution:**
Add all priority levels to color mapping:

```python
# ✅ COMPLETE: Includes all priority levels
priority_colors = {
    'Critical': 'C62828',  # Dark red - highest priority
    'High': 'FF6B6B',      # Light red
    'Medium': 'FFA500',    # Orange
    'Low': '4ECDC4'        # Teal
}
```

**Prevention:**
- Define standard priority levels in JSON schemas
- Validate priority values in analysis phase
- Use default color for unknown priorities (not white)

**Fixed In:** `ipa_client_handover_template.py` (2026-03-07)

---

### Issue: Empty Description Column in Business Requirements

**Symptoms:**
- Description column (D) is empty for all requirements
- Only Title and Priority are populated

**Root Cause:**
Data structure mismatch between analysis output and template expectations.

**Analysis Output:**
```json
{
  "requirement": "Text here",  ← Used as TITLE
  "source": "Section 2.5",
  "priority": "Critical"
  // NO "description" field
}
```

**Template Expects:**
```python
req_title = req.get('requirement', '') or req.get('title', '')
req_description = req.get('description', '')  ← Always empty!
```

**Solution:**
Update `transform_requirements()` in assembly script to generate descriptions:

```python
def transform_requirements(business_analysis):
    for idx, req in enumerate(requirements, start=1):
        req_title = req.get('requirement', '')
        req_description = req.get('description', '')
        
        # Generate description if missing
        if not req_description and req_title:
            req_description = f"Requirement to {req_title.lower()}"
        
        transformed.append({
            'title': req_title,
            'description': req_description,
            'priority': req.get('priority', 'Medium'),
            # ... other fields
        })
```

**Prevention:**
- Phase 1 analysis should generate both title and description
- Transform function should enrich missing fields
- Template should handle missing descriptions gracefully

**Status:** Identified (2026-03-07) - Fix pending

---

## Data Structure Issues

### Issue: Process Sheet Detection Fails in Validation

**Symptoms:**
```
❌ No Process sheets found
```
Despite process sheets being present in the report.

**Root Cause:**
Validation script looks for sheets starting with `⚙️ Process_` but actual sheets are named `⚙️ InvoiceApproval_...`

**Solution:**
Update validation regex to detect any sheet starting with ⚙️ emoji (excluding standard sheets):

```python
# ❌ OLD: Too specific
process_sheets = [s for s in sheet_names if s.startswith('⚙️ Process_')]

# ✅ NEW: Flexible
expected_sheets = ['📊 Executive Summary', '📋 Business Requirements', ...]
process_sheets = [s for s in sheet_names if s.startswith('⚙️') and s not in expected_sheets]
```

**Fixed In:** `ReusableTools/IPA_ClientHandover/validate_report.py` (2026-03-07)

---

### Issue: Configuration Variables Not Appearing in System Configuration Sheet

**Symptoms:**
- System Configuration sheet shows "Config variables: 0"
- File channel and process variables missing

**Root Cause:**
Phase 3 `configuration_analysis.json` missing required data structures.

**Required Structures:**
```json
{
  "file_channel_config": [
    {"variable": "FileChannelFileName", "purpose": "...", ...}
  ],
  "process_variables": [
    {"variable": "OauthCreds", "purpose": "...", ...}
  ],
  "configuration_dependencies": [
    {"config_set": "Interface", "property": "API_AuthCred_AGW", ...}
  ]
}
```

**Solution:**
See `PHASE3_CONFIGURATION_GUIDE.md` for complete extraction patterns.

**Prevention:**
- Validate Phase 3 output before Phase 5
- Use `validate_analysis_jsons.py` to check structure
- Review Phase 3 prompt to ensure all structures are requested

---

## Performance Issues

### Issue: Context Accumulation in Multi-Subagent Workflow

**Symptoms:**
- Process crashes at ~80 KB context
- Slower execution as workflow progresses
- Memory errors in long sessions

**Root Cause:**
Legacy multi-subagent architecture accumulated context across phases.

**Solution:**
Stateless pipeline architecture (implemented 2026-01-20):
- Phase 0: Python preprocessing (no AI)
- Phases 1-4: Independent AI analysis (file-based state)
- Phase 5: Python assembly (no AI)

**Benefits:**
- No context accumulation (each phase ~10 KB)
- No crashes (stable execution)
- Faster execution (reduced reasoning overhead)

**Reference:** See skill README.md for architecture details

---

## Best Practices

### Always Validate Before Assembly

```bash
# Validate JSON structure
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py

# Check for required fields
python -c "import json; data = json.load(open('Temp/configuration_analysis.json')); print('file_channel_config' in data)"
```

### Test with Edge Cases

- Long process names (>31 characters)
- Multiple processes with similar names
- Missing optional data (spec, WU log)
- All priority levels (Critical, High, Medium, Low)

### Use Validation Tools

```bash
# Validate generated report
python ReusableTools/IPA_ClientHandover/validate_report.py "Client_Handover_Results/Report.xlsx"

# Review report quality
python ReusableTools/IPA_ClientHandover/review_client_handover_report.py "Client_Handover_Results/Report.xlsx"
```

---

## Troubleshooting Checklist

When report generation fails or produces unexpected results:

1. **Check Phase 0 Output**
   - [ ] `lpd_structure.json` exists and is valid
   - [ ] `metrics_summary.json` has correct counts
   - [ ] `spec_raw.json` has content (if spec provided)

2. **Check Analysis Phases**
   - [ ] All 4 analysis JSON files exist
   - [ ] Each JSON has required top-level keys
   - [ ] Phase 3 has `file_channel_config`, `process_variables`, `configuration_dependencies`

3. **Check Template Compatibility**
   - [ ] Priority levels match template color mapping
   - [ ] Data structure matches template expectations
   - [ ] Sheet names are unique and <31 characters

4. **Check File Permissions**
   - [ ] Output directory exists and is writable
   - [ ] No Excel files open from previous runs
   - [ ] No file locks from other processes

---

## Version History

- **2026-03-07**: Initial version with Excel corruption, priority mapping, and validation fixes
- **2026-01-20**: Stateless pipeline architecture implemented
- **2025-12-15**: Multi-process support added

---

## Related Documentation

- `WORKFLOW_GUIDE.md` - Complete workflow steps
- `PHASE3_CONFIGURATION_GUIDE.md` - Configuration extraction patterns
- `JSON_SCHEMAS.md` - Data structure specifications
- `TROUBLESHOOTING.md` - General troubleshooting guide
- `.kiro/steering/00_Core_System_Rules.md` - Common pitfalls across all workflows
