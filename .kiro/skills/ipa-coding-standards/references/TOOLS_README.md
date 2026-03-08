# Python Tools Reference

Python tool usage and examples for IPA Coding Standards analysis.

## Phase 0: Preprocessing

### preprocess_coding_standards.py

**Purpose**: Extract and structure data for analysis phases

**Usage**:
```bash
python ReusableTools/IPA_CodingStandards/preprocess_coding_standards.py <lpd_path> <client>
```

**Parameters**:
- `lpd_path`: Path to LPD file
- `client`: Client name (for project standards lookup)

**Outputs**:
- `Temp/lpd_structure.json`
- `Temp/metrics_summary.json`
- `Temp/project_standards.json`

## Phase 1-4: Domain Analysis

### build_naming_analysis.py

**Purpose**: Analyze naming conventions

**Usage**:
```bash
python ReusableTools/IPA_CodingStandards/build_naming_analysis.py
```

**Output**: `Temp/naming_analysis.json`

### build_javascript_analysis.py

**Purpose**: Analyze JavaScript ES5 compliance

**Usage**:
```bash
python ReusableTools/IPA_CodingStandards/build_javascript_analysis.py
```

**Output**: `Temp/javascript_analysis.json`

### build_sql_analysis.py

**Purpose**: Analyze SQL queries

**Usage**:
```bash
python ReusableTools/IPA_CodingStandards/build_sql_analysis.py
```

**Output**: `Temp/sql_analysis.json`

### build_errorhandling_analysis.py

**Purpose**: Analyze error handling

**Usage**:
```bash
python ReusableTools/IPA_CodingStandards/build_errorhandling_analysis.py
```

**Output**: `Temp/errorhandling_analysis.json`

## Phase 6: Report Assembly

### assemble_coding_standards_report.py

**Purpose**: Generate Excel report from analysis outputs

**Usage**:
```bash
python ReusableTools/IPA_CodingStandards/assemble_coding_standards_report.py <client> <rice> <process_name>
```

**Parameters**:
- `client`: Client name
- `rice`: RICE item name
- `process_name`: Process name

**Output**: `Coding_Standards_Results/<Client>_<RICE>_<ProcessName>_CodingStandards_<timestamp>.xlsx`

---

For more information, see:
- [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) - Complete workflow
- [`JSON_SCHEMAS.md`](JSON_SCHEMAS.md) - JSON structure reference
