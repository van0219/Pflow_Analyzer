# Common Issues Catalog

Known issues and fixes for IPA Coding Standards analysis.

## Excel File Issues

### Sheet Name Limits

**Issue**: Excel has a 31-character limit for sheet names

**Prevention**: Use short, descriptive sheet names

### File Corruption

**Issue**: Workbook corruption due to invalid data

**Prevention**: Validate all data before writing to Excel

## Template Rendering Issues

### Missing Data

**Issue**: Empty cells or sheets in generated report

**Cause**: Analysis JSON incomplete or missing fields

**Fix**: Validate JSON structure before assembly

### Priority Colors

**Issue**: Priority colors not displaying correctly

**Cause**: Invalid severity values

**Fix**: Ensure severity is one of: High, Medium, Low

## Data Structure Mismatches

### Template Expects Different Format

**Issue**: Template expects list-of-lists but receives list-of-dicts

**Fix**: Convert data format in assembly script, not in template

## Performance Issues

### Context Overload

**Issue**: AI analysis takes too long or fails

**Cause**: Too much data in single chunk

**Fix**: Reduce chunk size in incremental scripts

---

For more information, see:
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Troubleshooting guide
- [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) - Complete workflow


## KeyError: 'rule_name' in Phase 6

**Symptom**: Report assembly fails with `KeyError: 'rule_name'` when building ipa_data

**Root Cause**: AI-generated analysis files (Phases 1-5) don't include `rule_name` field, only `rule_id`

**Solution**: Automatically add `rule_name` field before Phase 6

**Fix Applied (2026-03-08)**:

Created helper script `Temp/add_rule_names.py` that:
1. Loads project standards to create rule_id → rule_name mapping
2. Iterates through all analysis JSON files
3. Adds `rule_name` field to each violation based on `rule_id`
4. Saves updated files

**Usage**:
```bash
python Temp/add_rule_names.py
```

**Prevention**: Run this script automatically after Phases 1-5 and before Phase 6 assembly.

**Long-term Fix**: Update all domain merge scripts to automatically add `rule_name` during the merge phase (similar to how structure_analysis merge already does this).

**Workflow Integration**:
- After completing Phases 1-5 (AI analysis)
- Before running Phase 6 (assembly)
- Script is idempotent (safe to run multiple times)
