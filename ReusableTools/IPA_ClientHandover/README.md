# IPA Client Handover Tools

Stateless pipeline architecture for generating comprehensive client-facing IPA documentation.

## Architecture

This toolset uses a **stateless, file-based pipeline** that eliminates context accumulation and prevents crashes.

### Pipeline Flow

```text
Phase 0: Preprocessing (Python)
├─ Tool: preprocess_client_handover.py
├─ Input: LPD file, ANA-050 spec
└─ Output: spec_raw.json, lpd_structure.json, metrics_summary.json

Phase 1: Business Requirements Analysis (AI)
├─ Input: spec_raw.json
├─ Task: Extract business objectives, requirements, stakeholders
└─ Output: business_analysis.json

Phase 2: Workflow Architecture Analysis (AI)
├─ Input: lpd_structure.json
├─ Task: Identify workflow steps, decision points, transformations
└─ Output: workflow_analysis.json

Phase 3: Configuration & Technical Components (AI)
├─ Input: lpd_structure.json, metrics_summary.json
├─ Task: Document configuration, file channels, web services
└─ Output: configuration_analysis.json

Phase 4: Risk & Compliance Review (AI)
├─ Input: All prior JSON outputs
├─ Task: Identify risks, maintenance concerns, best practices
└─ Output: risk_assessment.json

Phase 5: Report Assembly (Python)
├─ Tool: assemble_client_handover_report.py
├─ Input: All JSON outputs from phases 1-4
├─ Template: ipa_client_handover_template.py (workspace root)
└─ Output: Comprehensive Excel report
```

## Tools

### Phase 0: preprocess_client_handover.py

Deterministic preprocessing with no AI reasoning.

**Usage:**
```bash
python ReusableTools/IPA_ClientHandover/preprocess_client_handover.py <lpd_file> <spec_file> [output_dir]
```

**Outputs:**
- `spec_raw.json` - Extracted ANA-050 content
- `lpd_structure.json` - Extracted LPD process structure
- `metrics_summary.json` - Pre-calculated metrics (activity counts, ES6 patterns, SQL statements, integrations)

### Phase 5: assemble_client_handover_report.py

Merges all analysis outputs and generates Excel report.

**Usage:**
```bash
python ReusableTools/IPA_ClientHandover/assemble_client_handover_report.py <client_name> <rice_item> [temp_dir] [output_dir]
```

**Inputs:**
- `business_analysis.json` (from Phase 1)
- `workflow_analysis.json` (from Phase 2)
- `configuration_analysis.json` (from Phase 3)
- `risk_assessment.json` (from Phase 4)
- `lpd_structure.json` (from Phase 0)
- `metrics_summary.json` (from Phase 0)

**Output:**
- Excel report: `Client_Handover_Results/<Client>_<RICE>.xlsx`

## Legacy Tools (Deprecated)

The following tools are deprecated and replaced by the stateless pipeline:

- `organize_by_sections.py` → Replaced by `preprocess_client_handover.py`
- `merge_documentation.py` → Replaced by `assemble_client_handover_report.py`
- `consolidate_processes.py` → Integrated into `assemble_client_handover_report.py`
- `generate_client_handover_report.py` → Replaced by `assemble_client_handover_report.py`

## Key Benefits

✅ **No context accumulation** - Each phase isolated at ~10 KB
✅ **No crashes** - Stable execution regardless of file size
✅ **Faster execution** - Reduced reasoning overhead
✅ **Enterprise-grade quality** - Comprehensive documentation maintained
✅ **Leverages existing templates** - No template rewrite needed
✅ **Clear separation** - AI analyzes, Python processes

## Related Documentation

- `.kiro/steering/00_Workflow_Engineering_Principles.md` - Stateless pipeline architecture
- `.kiro/steering/10_IPA_Report_Generation.md` - Report generation guidelines
- `.kiro/skills/ipa-client-handover/SKILL.md` - Skill documentation
- `ipa_client_handover_template.py` (workspace root) - Excel template

## Template Integration

The `assemble_client_handover_report.py` tool builds an `ipa_data` dictionary that feeds into the existing `ipa_client_handover_template.py`. This maintains backward compatibility while enabling the stateless pipeline architecture.

### ipa_data Structure

```python
{
    'client_name': str,
    'process_group': str,
    'process_details': dict,
    'business_requirements': dict,
    'config_variables': list,
    'activity_guide': list,
    'maintenance_guide': dict,
    'production_validation': dict,
    'processes': list,
    'risk_assessment': dict,
    'metrics_summary': dict
}
```

## Migration from Legacy Architecture

If you have existing workflows using the old multi-subagent architecture:

1. Replace subagent orchestration with stateless phase execution
2. Use `preprocess_client_handover.py` for Phase 0
3. Execute Phases 1-4 directly (AI analysis with file-based state transfer)
4. Use `assemble_client_handover_report.py` for Phase 5

The existing template (`ipa_client_handover_template.py`) requires no changes.
