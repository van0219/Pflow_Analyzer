# JSON Repair Tool for Client Handover Workflow

## Purpose

Automatically validates and repairs common JSON syntax errors in analysis files generated during Phases 1-4 of the client handover workflow.

## Problem Statement

When AI generates JSON files using `fsWrite` followed by `fsAppend`, a common pattern emerges:

1. `fsWrite` creates initial JSON structure ending with `}`
2. `fsAppend` adds more content starting with `,`
3. Result: Invalid JSON with premature closing brace

**Example of broken JSON:**
```json
{
  "section1": [...]
}
  ,
  "section2": [...]
}
```

**After repair:**
```json
{
  "section1": [...],
  "section2": [...]
}
```

## Features

The repair tool automatically fixes:

1. **Premature closing braces** - Removes `}` before `,` when more content follows
2. **Trailing commas** - Removes commas before `}` or `]`
3. **Missing closing braces** - Adds missing `}` or `]` to balance structure

## Usage

### Standalone Mode

```bash
# Validate and repair all analysis JSON files
python ReusableTools/IPA_ClientHandover/repair_analysis_jsons.py

# Create backups before repair
python ReusableTools/IPA_ClientHandover/repair_analysis_jsons.py --backup
```

### Integrated Mode

The repair tool is automatically called by `assemble_client_handover_report.py` before loading JSON files:

```python
# Phase 5 assembly script automatically runs repair
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py BayCare APIA
```

Output:
```
[0/3] Validating and repairing JSON files...
   ✓ Repaired workflow_analysis.json
     - Removed premature closing brace before comma
   ✓ All JSON files valid
```

## Files Validated

- `Temp/business_analysis.json`
- `Temp/workflow_analysis.json`
- `Temp/configuration_analysis.json`
- `Temp/risk_assessment.json`

## Exit Codes

- `0` - All files valid or successfully repaired
- `1` - Some files could not be repaired (manual intervention required)

## Backup Files

When using `--backup` flag, original files are saved with `.bak` extension:

- `business_analysis.json.bak`
- `workflow_analysis.json.bak`
- etc.

## Integration Points

1. **Phase 5 Assembly** - Automatically called before loading JSON files
2. **Validation Script** - Can be called independently for troubleshooting
3. **CI/CD Pipeline** - Can be integrated into automated testing

## Limitations

The tool handles common AI-generated JSON errors but cannot fix:

- Semantic errors (wrong data structure)
- Missing required fields
- Incorrect data types
- Logic errors in content

For these issues, manual review and correction is required.

## Testing

Test the repair tool with a deliberately broken JSON file:

```bash
python Temp/test_repair.py
```

This creates a broken JSON file, repairs it, and validates the result.

## Future Enhancements

Potential improvements:

1. Schema validation against expected structure
2. Content validation (required fields, data types)
3. Automatic field population for missing data
4. Integration with JSON schema definitions
5. Repair suggestions for complex errors

## Related Documentation

- `JSON_SCHEMAS.md` - Expected JSON structure for each phase
- `TROUBLESHOOTING.md` - Common issues and solutions
- `WORKFLOW_GUIDE.md` - Complete workflow documentation
