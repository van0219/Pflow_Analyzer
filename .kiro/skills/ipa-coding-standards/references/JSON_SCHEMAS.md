# JSON Schemas Reference

Complete JSON structure reference for all phases of the IPA Coding Standards skill.

## Phase 0 Outputs

### lpd_structure.json

Complete LPD structure extracted from XML.

**Key Fields:**
- `processes`: Array of process objects
- `activities`: Array of activity objects
- `javascript_blocks`: Array of JS code blocks
- `sql_queries`: Array of SQL queries
- `config_sets`: Array of configuration sets

### metrics_summary.json

Process metrics and statistics.

**Structure:**
```json
{
  "process_name": "ProcessName",
  "process_type": "Interface Process",
  "activity_count": 78,
  "javascript_block_count": 45,
  "sql_query_count": 12,
  "error_prone_activity_count": 15,
  "es6_patterns_detected": ["let", "const", "arrow_function"],
  "generic_names_detected": ["Assign 1", "Branch 1"],
  "sql_types_detected": ["SELECT", "INSERT", "UPDATE"]
}
```

### project_standards.json

Project-specific coding standards (if available).

**Structure:**
```json
[
  {
    "rule_id": "1.1.1",
    "pattern": "<Prefix>_WF_<Description>.lpd",
    "severity": "High",
    "description": "Filename format for approval workflows"
  }
]
```

## Phase 1-5 Outputs

### naming_analysis.json

**Structure:**
```json
[
  {
    "rule_id": "1.1.1",
    "severity": "High",
    "finding": "Description",
    "current": "Current state",
    "recommendation": "How to fix",
    "activities": "Affected activities",
    "domain": "naming"
  }
]
```

### javascript_analysis.json

**Structure:**
```json
[
  {
    "rule_id": "1.2.1",
    "severity": "Medium",
    "finding": "Description",
    "current": "Current code",
    "recommendation": "How to fix",
    "activities": "Affected activities",
    "domain": "javascript"
  }
]
```

### sql_analysis.json

**Structure:**
```json
[
  {
    "rule_id": "1.5.2",
    "severity": "High",
    "finding": "Description",
    "current": "Current query",
    "recommendation": "How to fix",
    "activities": "Affected activities",
    "domain": "sql"
  }
]
```

### errorhandling_analysis.json

**Structure:**
```json
[
  {
    "rule_id": "1.3.1",
    "severity": "High",
    "finding": "Description",
    "current": "Current state",
    "recommendation": "How to fix",
    "activities": "Affected activities",
    "domain": "errorhandling"
  }
]
```

### structure_analysis.json

**Structure:**
```json
[
  {
    "rule_id": "Structure",
    "severity": "Medium",
    "finding": "Description",
    "current": "Current configuration",
    "recommendation": "How to fix",
    "activities": "N/A",
    "domain": "structure"
  }
]
```

## Validation Rules

1. All analysis JSONs must be valid JSON arrays
2. Each violation must have required fields: rule_id, severity, finding, current, recommendation, activities, domain
3. Severity must be one of: High, Medium, Low
4. Domain must match the analysis phase

## Assembly Script Behavior

The assembly script (`assemble_coding_standards_report.py`) expects:

1. All 5 analysis JSONs to exist
2. Each JSON to be a valid array
3. Violations to have consistent structure
4. Project standards to be loaded (if available)

---

For more information, see:
- [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) - Complete workflow
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Common issues
