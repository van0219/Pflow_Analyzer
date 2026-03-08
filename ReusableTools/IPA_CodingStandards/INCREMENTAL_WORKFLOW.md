# IPA Coding Standards - Incremental Workflow

Complete implementation of the incremental analysis pipeline for coding standards reports.

## Architecture

Stateless, file-based pipeline that eliminates context accumulation:

- **Phase 0 (Python)**: Deterministic preprocessing, no AI reasoning
- **Phases 1-5 (AI)**: Independent analysis phases, each reads JSON input and writes JSON output
- **Phase 6 (Python)**: Deterministic report assembly, no AI reasoning

## Available Scripts

### Phase 0: Preprocessing
```bash
python ReusableTools/IPA_CodingStandards/preprocess_coding_standards.py <lpd_file> <client>
```

Creates:
- `lpd_structure.json` - Complete LPD structure
- `metrics_summary.json` - Process metrics
- `project_standards.json` - Client-specific standards
- `*_domain_naming.json` - Naming data
- `*_domain_javascript.json` - JavaScript blocks
- `*_domain_sql.json` - SQL queries
- `*_domain_errorhandling.json` - Error handling nodes
- `*_domain_structure.json` - Process structure

### Phase 1: Naming Analysis
```bash
python ReusableTools/IPA_CodingStandards/build_naming_analysis.py analyze
# AI analyzes chunks and creates naming_chunk_N_analyzed.json files
python ReusableTools/IPA_CodingStandards/build_naming_analysis.py merge
```

Output: `naming_analysis.json`

### Phase 2: JavaScript Analysis
```bash
python ReusableTools/IPA_CodingStandards/build_javascript_analysis.py analyze
# AI analyzes chunks and creates javascript_chunk_N_analyzed.json files
python ReusableTools/IPA_CodingStandards/build_javascript_analysis.py merge
```

Output: `javascript_analysis.json`

### Phase 3: SQL Analysis
```bash
python ReusableTools/IPA_CodingStandards/build_sql_analysis.py analyze
# AI analyzes chunks and creates sql_chunk_N_analyzed.json files
python ReusableTools/IPA_CodingStandards/build_sql_analysis.py merge
```

Output: `sql_analysis.json`

### Phase 4: Error Handling Analysis
```bash
python ReusableTools/IPA_CodingStandards/build_errorhandling_analysis.py analyze
# AI analyzes chunks and creates errorhandling_chunk_N_analyzed.json files
python ReusableTools/IPA_CodingStandards/build_errorhandling_analysis.py merge
```

Output: `errorhandling_analysis.json`

### Phase 5: Structure Analysis
```bash
python ReusableTools/IPA_CodingStandards/build_structure_analysis.py
# AI analyzes structure data directly (no chunking needed)
```

Output: `structure_analysis.json`

### Phase 6: Report Assembly
```bash
python ReusableTools/IPA_CodingStandards/assemble_coding_standards_report.py <client> <rice_item> <process_name>
```

Output: Excel report in `Coding_Standards_Results/`

## Key Principles

1. **Intelligence from focused analysis, not cumulative memory**
2. **Each phase operates in isolation** (~2-3 KB context per chunk)
3. **File-based state transfer** (JSON files replace conversational memory)
4. **Minimal AI output** ("Phase N complete. file.json written.")
5. **No context accumulation** (stable execution regardless of file size)

## Violation Structure

Each violation must include:
```json
{
  "rule_id": "1.1.4",
  "rule_name": "Node Naming",
  "severity": "Medium",
  "finding": "Description of the issue",
  "current": "Current state",
  "recommendation": "How to fix it",
  "activities": ["Activity1", "Activity2"],
  "domain": "naming",
  "impact_analysis": {
    "estimated_fix_time": "30 minutes",
    "affected_percentage": 64.0
  },
  "priority_score": 60,
  "code_examples": {
    "before": "Before code",
    "after": "After code",
    "explanation": "Why this change"
  },
  "testing_notes": "How to test the fix"
}
```

## Templates

- **ipa_coding_standards_template_enhanced.py** - Current template (v2.0) with 4 sheets
- **ipa_coding_standards_template.py** - Legacy template (v1.0) with 3 sheets

## Helper Functions

- **build_ipa_data_helper.py** - Builds ipa_data from violations (prevents duplicates)
- **organize_by_domain.py** - Used by preprocessing script
- **merge_violations.py** - Used by assembly script

## Performance

- Phase 0: ~2-3s
- Phase 1: ~1-2 min (chunked)
- Phase 2: ~2-3 min (chunked)
- Phase 3: ~1-2 min (chunked)
- Phase 4: ~1-2 min (chunked)
- Phase 5: ~30-60s (direct)
- Phase 6: ~5-10s
- **Total**: ~8-12 min per process (stable, no crashes)

## Troubleshooting

### "Process Count: 0"
Phase 0 was skipped - run preprocessing first

### "No violations found"
Check if project standards loaded correctly

### "Missing domain analysis"
One of Phases 1-5 failed - check Temp/ folder for partial outputs

### Empty sheets in report
Analysis JSONs incomplete - validate structure

### Template compatibility issues
Ensure violations have all required fields (finding, activities, domain, etc.)
