# IPA Analyzer - Data Extraction Tools

**Purpose**: Extract and organize data from IPA files for Kiro to analyze

**CRITICAL PRINCIPLE**: These tools do NOT analyze data. They only extract and organize it into JSON format for Kiro (AI) to analyze.

## Tools

### 1. extract_lpd_data.py
**Purpose**: Extract structured data from LPD files

**Extracts**:
- Process metadata (name, auto-restart setting)
- Activities (ID, type, caption, properties)
- JavaScript blocks (code, line count, activity reference)
  - **Only from ASSGN (Assign) nodes** - JavaScript is not in LM, WEBRUN, or other node types
  - **Handles URL-encoded JavaScript** - Detects and decodes JavaScript stored in URL-encoded format
- SQL queries (from WEBRUN nodes - Data Fabric Compass API calls)
- Configuration variables (from START node)

**Output**: JSON file with organized LPD data

**Usage**:
```python
from ReusableTools.IPA_Analyzer.extract_lpd_data import extract_lpd_data

data = extract_lpd_data(
    lpd_files=['Projects/BayCare/APIA/main.lpd', ...],
    output_file='Temp/BayCare_APIA_lpd_data.json'
)
```

**Key Features**:
- Detects URL-encoded JavaScript (properties containing %0D%0A, %2B, %3D patterns)
- Automatically decodes URL-encoded content using `urllib.parse.unquote`
- Separates JavaScript (from ASSGN nodes) from SQL (from WEBRUN nodes)
- Fast extraction: ~1 second per 12K line LPD file

### 2. extract_wu_log.py
**Purpose**: Extract structured data from work unit logs

**Extracts**:
- Metadata (work unit number, process name, service name, auto-restart, start/end times, duration, status)
- Activities executed (with start/end times and duration per activity)
- Variable values (comprehensive extraction with improved regex)
- Error messages

**Output**: JSON file with organized log data

**Usage**:
```python
from ReusableTools.IPA_Analyzer.extract_wu_log import extract_wu_log

data = extract_wu_log(
    log_file='Projects/BayCare/APIA/339_log.txt',
    output_file='Temp/BayCare_APIA_wu_data.json'
)
```

**Key Features**:
- Extracts work unit number from "Workunit X started" line
- Parses activity timing with start/end times and calculates duration
- Improved variable extraction regex: `^\s+(\w+)\s*=\s*(.*)$`
- Extracts process name and service name from log metadata
- State machine approach for line-by-line parsing

### 3. extract_spec.py
**Purpose**: Extract structured data from ANA-050 functional specifications

**Extracts**:
- Metadata (filename, paragraph count, RICE type hint)
- Requirements (numbered items and bullet points)
- Sections (major document sections)
- Tables (all tables with data)
- Full text (complete document text)

**Output**: JSON file with organized spec data

**Usage**:
```python
from ReusableTools.IPA_Analyzer.extract_spec import extract_spec

data = extract_spec(
    spec_file='Projects/BayCare/APIA/ANA-050.docx',
    output_file='Temp/BayCare_APIA_spec_data.json'
)
```

## Workflow

### Step 1: Extract Data (Python)
```python
# Extract LPD data
from ReusableTools.IPA_Analyzer.extract_lpd_data import extract_lpd_data
lpd_data = extract_lpd_data(
    lpd_files=['Projects/ClientName/RICEItem/file1.lpd', ...],
    output_file='Temp/ProjectName_lpd_data.json'
)

# Extract WU log data
from ReusableTools.IPA_Analyzer.extract_wu_log import extract_wu_log
wu_data = extract_wu_log(
    log_file='Projects/ClientName/RICEItem/log.txt',
    output_file='Temp/ProjectName_wu_data.json'
)

# Extract spec data
from ReusableTools.IPA_Analyzer.extract_spec import extract_spec
spec_data = extract_spec(
    spec_file='Projects/ClientName/RICEItem/ANA-050.docx',
    output_file='Temp/ProjectName_spec_data.json'
)
```

### Step 2: Analyze Data (Kiro)
```python
# Read extracted JSON files
import json

with open('Temp/ProjectName_lpd_data.json') as f:
    lpd_data = json.load(f)

with open('Temp/ProjectName_wu_data.json') as f:
    wu_data = json.load(f)

with open('Temp/ProjectName_spec_data.json') as f:
    spec_data = json.load(f)

# Kiro analyzes the data:
# - Assess ES5 compliance from JavaScript blocks
# - Identify issues with specific line numbers
# - Determine severity levels
# - Create recommendations
# - Score quality metrics
# - Trace requirements to activities
# - Identify gaps and risks

# Build ipa_data dictionary with analysis results
ipa_data = {
    'process_name': 'ProjectName',
    'overview': {...},  # Kiro's analysis
    'key_findings': [...],  # Kiro's findings
    'quality_scores': {...},  # Kiro's scores
    'javascript_issues': [...],  # Kiro's ES5 assessment
    'recommendations': [...],  # Kiro's recommendations
    # ... etc
}
```

### Step 3: Generate Report (Python Template)
```python
from ipa_peer_review_template import generate_report

output_path = generate_report(ipa_data)
print(f"Report generated: {output_path}")
```

## Key Principles

### What Python Does (Data Processing)
- ✅ Extract data from files
- ✅ Parse XML, JSON, DOCX formats
- ✅ Structure raw data into organized JSON
- ✅ Format analyzed data into Excel reports
- ✅ Perform calculations (duration, counts)

### What Python Does NOT Do (Analysis)
- ❌ Assess code quality
- ❌ Identify issues or root causes
- ❌ Make recommendations
- ❌ Determine severity levels
- ❌ Score quality metrics
- ❌ Provide context-aware insights

### What Kiro Does (Analysis)
- ✅ Assess ES5 compliance
- ✅ Identify issues with context
- ✅ Determine severity and priority
- ✅ Create specific recommendations
- ✅ Score quality metrics
- ✅ Trace requirements to implementation
- ✅ Identify gaps and risks
- ✅ Provide context-aware insights

## Output Format

All extraction tools output JSON files with this structure:

### LPD Data JSON
```json
{
  "processes": [
    {
      "file": "main.lpd",
      "process_name": "InvoiceApproval_APIA_NONPOROUTING",
      "auto_restart": "0",
      "activity_count": 191,
      "activities": [
        {
          "id": "Assign4120",
          "type": "ASSGN",
          "caption": "Calculate Approvers",
          "properties": {...}
        }
      ],
      "javascript_blocks": [
        {
          "activity_id": "Assign4120",
          "activity_caption": "Calculate Approvers",
          "code": "var approver = ...",
          "line_count": 25
        }
      ],
      "config_variables": [...]
    }
  ],
  "summary": {
    "total_processes": 3,
    "total_activities": 226,
    "total_javascript_blocks": 75
  }
}
```

### WU Log Data JSON
```json
{
  "file": "339_log.txt",
  "metadata": {
    "work_unit": "339",
    "auto_restart": "Disabled",
    "start_time": "01/15/2026 10:30:00.000 AM",
    "end_time": "01/15/2026 10:30:15.500 AM",
    "duration_ms": 15500,
    "duration_readable": "15.50s",
    "status": "Completed"
  },
  "activities": [...],
  "variables": {...},
  "errors": []
}
```

### Spec Data JSON
```json
{
  "file": "ANA-050.docx",
  "metadata": {
    "filename": "ANA-050.docx",
    "paragraph_count": 250,
    "table_count": 5,
    "rice_type_hint": "Enhancement"
  },
  "requirements": [
    {
      "text": "System shall route invoices for approval...",
      "original": "1. System shall route invoices..."
    }
  ],
  "sections": {...},
  "tables": [...],
  "full_text": "..."
}
```

## Dependencies

- Python 3.7+
- xml.etree.ElementTree (built-in)
- json (built-in)
- re (built-in)
- python-docx (for spec extraction): `pip install python-docx`

## Integration

These tools integrate with:
- `.kiro/hooks/ipa-peer-review.kiro.hook` - Agent hook workflow
- `ipa_peer_review_template.py` - Excel report generation
- Kiro's analysis workflow

## Performance

- Fast extraction (processes 12K line LPD in <1 second)
- Memory efficient (streams large files)
- Clean JSON output (easy for Kiro to read and analyze)

## Recent Updates

### 2026-01-16: JavaScript Extraction Fix
- **Problem**: JavaScript not being extracted (0 blocks when there were actually 148)
- **Root Cause**: Tool only looked for `expression` properties, missed URL-encoded JavaScript
- **Solution**: Added URL encoding detection and decoding, only extract from ASSGN nodes
- **Result**: Now correctly extracts all JavaScript blocks from IPA files

### 2026-01-16: Work Unit Log Extraction Fix
- **Problem**: Work unit number showing "Unknown", incomplete activity timing, missing metadata
- **Root Cause**: Incomplete regex patterns and missing extraction logic
- **Solution**: Fixed work unit number extraction, added activity timing, improved variable regex, added metadata
- **Result**: Complete work unit log data extraction with all metadata and timing information
