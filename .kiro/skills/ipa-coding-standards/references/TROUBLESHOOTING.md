# Troubleshooting Guide

Common issues and solutions for IPA Coding Standards analysis.

## Quick Diagnosis

```bash
# Verify all Phase 0 outputs exist
Test-Path Temp/lpd_structure.json
Test-Path Temp/metrics_summary.json
Test-Path Temp/project_standards.json

# Verify all analysis outputs exist
Test-Path Temp/naming_analysis.json
Test-Path Temp/javascript_analysis.json
Test-Path Temp/sql_analysis.json
Test-Path Temp/errorhandling_analysis.json
Test-Path Temp/structure_analysis.json
```

## Common Issues

### Issue: "Process Count: 0"

**Cause**: Phase 0 was skipped or failed

**Fix**:
1. Verify LPD file path is correct
2. Re-run Phase 0: `python ReusableTools/IPA_CodingStandards/preprocess_coding_standards.py <lpd_path> <client>`
3. Check `lpd_structure.json` exists and contains data

### Issue: "No violations found"

**Cause**: Project standards not loaded or analysis incomplete

**Fix**:
1. Check `project_standards.json` exists
2. Verify all analysis JSONs exist (Phases 1-5)
3. Re-run failed phases
4. Check if process actually has violations

### Issue: "Missing domain analysis"

**Cause**: One of Phases 1-5 failed

**Fix**:
1. Check Temp/ folder for partial outputs
2. Identify which phase failed
3. Re-run that specific phase
4. Check error messages in console

### Issue: "Invalid project standards"

**Cause**: Excel file format incorrect

**Fix**:

1. Verify sheet name is "Standards"
2. Check column headers match expected format
3. Ensure no empty rows
4. Re-run Phase 0

### Issue: "JSONDecodeError: Unexpected UTF-8 BOM"

**Cause**: Files created with PowerShell `Out-File` include UTF-8 BOM by default, which Python's JSON parser rejects

**Fix**:

When creating JSON files manually in PowerShell, use one of these methods:

**Method 1: Use ASCII encoding**
```powershell
'{"violations": []}' | Out-File "Temp/file.json" -Encoding ASCII
```

**Method 2: Use .NET WriteAllText without BOM**
```powershell
$content = '{"violations": []}'
[System.IO.File]::WriteAllText("Temp/file.json", $content, (New-Object System.Text.UTF8Encoding $false))
```

**Prevention**: The preprocessing script now automatically cleans the Temp folder at the start of each process, preventing this issue in normal workflows.

---

For more information, see:
- [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) - Complete workflow
- [`COMMON_ISSUES.md`](COMMON_ISSUES.md) - Known issues catalog
