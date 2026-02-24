# Reusable Tools

Collection of reusable Python tools for IPA analysis, data extraction, and validation.

## Tools

### IPA Analyzer (`IPA_Analyzer/`)

Extracts data from LPD files, WU logs, and spec documents into JSON format for AI analysis.

**Tools:**
- `extract_lpd_data.py` - Activities, JavaScript, config variables
- `extract_wu_log.py` - Performance metrics, variables, errors
- `extract_spec.py` - Requirements, sections, tables

**Workflow:** Python extracts → JSON → Kiro analyzes → Python formats report

See: `IPA_Analyzer/README.md`

---

### ION BOD Download (`ION_BOD_Download/`)

Downloads BOD files from ION OneView API for data quality investigations.

**Purpose:** Compare raw API data vs processed data to identify issue source.

**Tools:**
- `ion_bod_downloader.py` - Download BODs from ION API
- `bod_analyzer.py` - Analyze downloaded BOD files

See: `ION_BOD_Download/README.md`

---

### Standard Flow Check (`check_standard_flow.py`)

Checks if an IPA process is a standard flow that should not be modified.

**Purpose:** Prevent accidental modification of Infor-provided standard flows.

**Usage:**

```python
from ReusableTools.check_standard_flow import check_standard_flow

# Check single LPD file
result = check_standard_flow('MatchReport_Outbound.lpd')
if result['is_standard']:
    print(result['message'])
    print(f"Flow: {result['flow_name']}")
    print(f"Description: {result['description']}")
```

**Command Line:**

```bash
python ReusableTools/check_standard_flow.py MatchReport_Outbound.lpd
```

**Returns:**

```python
{
    'is_standard': bool,           # True if found in standard flows CSV
    'flow_name': str or None,      # PfiFlowDefinition name
    'description': str or None,    # PfiFlowDescription
    'message': str                 # User-friendly message
}
```

**Integration:**
- Used in coding standards reviews (Step 7)
- Checks against `Application+Defined+Processes.csv`
- Flags standard flows as violations in 1.1 Naming Convention
- Recommends copying and renaming for customization

**Multiple Files:**

```python
from ReusableTools.check_standard_flow import check_multiple_flows

results = check_multiple_flows([
    'Process1.lpd',
    'Process2.lpd',
    'Process3.lpd'
])
print(results['summary'])
```

---

## Directory Structure

```
ReusableTools/
├── README.md                    # This file
├── check_standard_flow.py       # Standard flow checker
├── IPA_Analyzer/                # IPA data extraction
│   ├── README.md
│   ├── extract_lpd_data.py
│   ├── extract_wu_log.py
│   ├── extract_spec.py
│   └── config/
└── ION_BOD_Download/            # ION BOD downloader
    ├── README.md
    ├── ion_bod_downloader.py
    ├── bod_analyzer.py
    └── config/
```

---

## Best Practices

1. **Separation of Concerns**: Python extracts/formats, AI analyzes
2. **JSON Intermediate**: All tools output JSON for AI consumption
3. **Reusability**: Tools work across all projects without modification
4. **Documentation**: Each tool has README with usage examples
5. **Error Handling**: Tools validate inputs and provide clear error messages

---

## Adding New Tools

When creating new reusable tools:

1. Create tool directory: `ReusableTools/<ToolName>/`
2. Add main Python script(s)
3. Create `config/` folder for configuration files
4. Add `README.md` with usage examples
5. Update this README with tool description
6. Update `.kiro/steering/00_Kiro_General_Rules.md` with tool reference
7. Add to relevant hooks if applicable

---

## See Also

- `.kiro/steering/00_Kiro_General_Rules.md` - Reusable Tools section
- `.kiro/steering/10_IPA_Report_Generation.md` - Data Extraction Tools section
- `.kiro/hooks/` - Automated workflows using these tools
