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
