# IPA Performance Analysis Tools

This folder contains Python tools for the performance analysis workflow.

## Architecture

The performance workflow follows the same proven pattern as coding standards and client handover:

```
Extract → Organize → Analyze → Merge → Report
```

## Tools

### 1. organize_by_areas.py

**Purpose**: Organize extracted WU data into 4 focused analysis areas

**Input**: `Temp/<ProcessName>_wu_data.json` (from extract_wu_log.py)

**Output**: 4 area files
- `Temp/<ProcessName>_area_activities.json` - Activity timeline data
- `Temp/<ProcessName>_area_errors.json` - Error data
- `Temp/<ProcessName>_area_performance.json` - Performance metrics
- `Temp/<ProcessName>_area_code.json` - JavaScript/SQL code data

**Usage**:
```bash
python organize_by_areas.py Temp/CISOutbound_wu_data.json Temp/CISOutbound
```

### 2. merge_analysis.py

**Purpose**: Merge 4 area analysis files into master analysis

**Input**: 4 analysis files from subagents
- `Temp/<ProcessName>_analysis_activities.json`
- `Temp/<ProcessName>_analysis_errors.json`
- `Temp/<ProcessName>_analysis_performance.json`
- `Temp/<ProcessName>_analysis_code.json`

**Output**: `Temp/<ProcessName>_master_analysis.json`

**Usage**:
```bash
python merge_analysis.py Temp/CISOutbound
```

### 3. generate_performance_report.py

**Purpose**: Load master analysis and call wu_master_template.py

**Input**: `Temp/<ProcessName>_master_analysis.json`

**Output**: `Performance_Results/<Client>_<RICE>_Performance_YYYYMMDD.xlsx`

**Usage**:
```bash
python generate_performance_report.py CISOutbound FPI MatchReport
```

## Workflow Integration

These tools are used by the performance hook (v3) in the following workflow:

1. **Step 5**: Extract data using `extract_wu_log.py`
2. **Step 6**: Organize by areas using `organize_by_areas.py`
3. **Step 7**: Launch 4 subagents to analyze each area
4. **Step 8**: Verify subagent outputs
5. **Step 9**: Merge analysis using `merge_analysis.py`
6. **Step 10**: Confirm report generation
7. **Step 11**: Generate report using `generate_performance_report.py`

## Subagents

The workflow uses 4 specialized subagents:

1. **wu-activity-analyzer** - Activity timeline analysis
2. **wu-error-analyzer** - Error analysis and root causes
3. **wu-performance-analyzer** - Performance metrics and bottlenecks
4. **wu-code-analyzer** - JavaScript/SQL code review

## Benefits

- **No Context Overload**: Main agent never reads raw log files
- **Scalable**: Handles any log size efficiently
- **Specialized Analysis**: Each subagent focuses on one area
- **Consistent Architecture**: Same pattern as other IPA workflows
- **Python Handles Data**: AI only analyzes, Python processes

## Data Flow

```
Raw WU Log
    ↓ (extract_wu_log.py)
WU Data JSON
    ↓ (organize_by_areas.py)
4 Area Files
    ↓ (4 subagents analyze)
4 Analysis Files
    ↓ (merge_analysis.py)
Master Analysis JSON
    ↓ (generate_performance_report.py)
Excel Report
```

## Key Principles

1. **Python Extracts, AI Analyzes**: Python handles data extraction and organization, AI performs analysis
2. **Subagents Save Files Directly**: Each subagent saves its own output using fsWrite
3. **Main Agent Orchestrates Only**: Main agent never reads intermediate files
4. **Explicit JSON Validation**: All subagents validate JSON output format
5. **Temp Cleanup**: Workflow starts with automatic Temp folder cleanup
