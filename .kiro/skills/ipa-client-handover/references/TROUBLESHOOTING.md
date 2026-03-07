# Client Handover Generation - Troubleshooting Guide

## Quick Diagnosis

Run the validation script to identify issues:
```bash
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

## Common Issues and Solutions

### Issue 1: "File not found: Temp/lpd_structure.json"

**Cause**: Phase 0 (preprocessing) was skipped

**Solution**:
```bash
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py <lpd_file> <spec_file> [wu_log_file]
```

**Prevention**: Always run Phase 0 first

---

### Issue 2: "Process Count: 0" in report

**Cause**: Missing or empty lpd_structure.json

**Diagnosis**:
```bash
python -c "import json; print(json.load(open('Temp/lpd_structure.json'))['processes'])"
```

**Solution**:
1. Delete Temp/lpd_structure.json
2. Re-run Phase 0
3. Verify file has processes array

---

### Issue 3: "ERROR: Invalid client_name '--client'"

**Cause**: Used named arguments instead of positional

**Wrong**:
```bash
python assemble_client_handover_report.py --client FPI --rice MatchReport
```

**Correct**:
```bash
python assemble_client_handover_report.py FPI MatchReport
```

---

### Issue 4: "AttributeError: 'list' object has no attribute 'get'"

**Cause**: Old version of assembly script (before flexibility fix)

**Solution**:
1. Verify you have the latest version with flexible parsing
2. Check line ~180 has `isinstance()` checks
3. If not, update from repository

---

### Issue 5: "ImportError: cannot import name 'extract_spec_data'"

**Cause**: Old version of preprocessing script

**Solution**:
1. Open `ReusableTools/IPA_ClientHandover/preprocess_client_handover.py`
2. Change line 24 from `extract_spec_data` to `extract_spec`
3. Change line 51 from `extract_spec_data(spec_file)` to `extract_spec(spec_file)`

---

### Issue 6: Report has empty sheets

**Cause**: Analysis JSONs don't match expected structure

**Diagnosis**:
```bash
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

**Solution**:
1. Check validation output for specific issues
2. Review JSON_SCHEMAS.md for correct structure
3. Regenerate problematic JSON files

---

### Issue 7: "Invalid JSON" error

**Cause**: Malformed JSON file

**Diagnosis**:
```bash
python -m json.tool Temp/<filename>.json
```

**Solution**:
1. Fix JSON syntax errors (missing commas, brackets, quotes)
2. Use online JSON validator if needed
3. Regenerate file if too corrupted

---

### Issue 8: Garbage filename created (e.g., "--client_FPI.xlsx")

**Cause**: Old version of assembly script without input validation

**Solution**:
1. Delete garbage file
2. Update assembly script to latest version with validation
3. Use correct positional arguments

---

## Verification Checklist

Before running Phase 5, verify:

```bash
# Check all files exist
Test-Path Temp/lpd_structure.json
Test-Path Temp/metrics_summary.json
Test-Path Temp/business_analysis.json
Test-Path Temp/workflow_analysis.json
Test-Path Temp/configuration_analysis.json
Test-Path Temp/risk_assessment.json

# Validate structure
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py

# Check file sizes (should not be tiny)
Get-ChildItem Temp/*.json | Select-Object Name, Length
```

All files should be >100 bytes. If any file is <100 bytes, it's likely empty or malformed.

---

## Recovery Procedures

### Complete Reset
```bash
# Delete all temp files
Remove-Item Temp/*.json

# Start from Phase 0
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py <lpd> <spec> [wu_log]

# Recreate analysis JSONs (Phases 1-4)
# ... manual AI analysis ...

# Validate before assembly
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py

# Generate report
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py <client> <rice>
```

### Partial Reset (Keep Phase 0 outputs)
```bash
# Delete only analysis JSONs
Remove-Item Temp/business_analysis.json
Remove-Item Temp/workflow_analysis.json
Remove-Item Temp/configuration_analysis.json
Remove-Item Temp/risk_assessment.json

# Recreate analysis JSONs (Phases 1-4)
# ... manual AI analysis ...

# Continue from validation
```

---

## Getting Help

### Check Documentation
1. `JSON_SCHEMAS.md` - Expected JSON structure
2. `.kiro/steering/10_IPA_Report_Generation.md` - Complete workflow
3. `.kiro/steering/00_Core_System_Rules.md` - Core requirements

### Run Tests
```bash
# End-to-end integration test
python ReusableTools/IPA_ClientHandover/test_end_to_end.py

# Validation only
python ReusableTools/IPA_ClientHandover/validate_analysis_jsons.py
```

### Debug Mode
Add print statements to see what's happening:
```python
# In assembly script, add before line causing error:
print(f"DEBUG: workflow_analysis = {workflow_analysis}")
print(f"DEBUG: decision_points type = {type(workflow_analysis.get('decision_points'))}")
```

---

## Prevention Best Practices

1. **Always run Phase 0 first** - Don't skip preprocessing
2. **Validate before assembly** - Catch issues early
3. **Use correct syntax** - Positional arguments, not named
4. **Keep scripts updated** - Pull latest fixes from repository
5. **Test with minimal data** - Ensure graceful degradation works
6. **Document custom changes** - If you modify JSONs manually

---

## Known Limitations

1. **Manual Phases 1-4**: Currently require manual AI analysis (no automated scripts yet)
2. **No schema enforcement**: Assembly script is flexible but doesn't enforce strict schemas
3. **Limited error messages**: Some errors may not be immediately clear
4. **No rollback**: If Phase 5 fails, must fix and re-run (no automatic rollback)

---

## Future Improvements

- [ ] Automated Phase 1-4 Python scripts
- [ ] Strict JSON schema validation with jsonschema library
- [ ] Better error messages with suggested fixes
- [ ] Automatic backup/restore on failure
- [ ] Progress indicators for long-running operations
- [ ] Dry-run mode to preview without generating report
