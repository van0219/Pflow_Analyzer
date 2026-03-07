# Phase 2 Incremental Workflow Analysis Guide

## Overview

Phase 2 generates activity descriptions and purposes for ALL activities in a process. For large processes (30+ activities) or multi-process RICE items, this can cause context overload and crashes.

The incremental approach splits activities into manageable chunks, analyzes each chunk separately, and merges results into a single `workflow_analysis.json` file.

## When to Use Incremental Approach

Use incremental analysis when:
- Single process with 30+ activities
- Multi-process RICE item (any size)
- Previous Phase 2 attempts crashed
- Context budget is limited

## Architecture

```
lpd_structure.json (1-N processes)
    ↓
build_workflow_analysis_incremental.py
    ↓
workflow_chunk_*.json (10 activities per chunk)
    ↓
AI analyzes each chunk
    ↓
merge_chunk_results() for each chunk
    ↓
workflow_analysis.json (complete)
```

## Step-by-Step Workflow

### Step 1: Generate Chunks

```bash
python ReusableTools/IPA_ClientHandover/build_workflow_analysis_incremental.py
```

**Single Process Output:**
```
Temp/workflow_chunk_1.json
Temp/workflow_chunk_2.json
Temp/workflow_chunk_3.json
...
```

**Multi-Process Output:**
```
Temp/workflow_chunk_ProcessName1_1.json
Temp/workflow_chunk_ProcessName1_2.json
Temp/workflow_chunk_ProcessName2_1.json
Temp/workflow_chunk_ProcessName2_2.json
...
```

### Step 2: Analyze Each Chunk

For each chunk file, read the activities and generate descriptions:

```python
# Read chunk
chunk_data = json.load(open('Temp/workflow_chunk_1.json'))

# Analyze activities and generate:
descriptions = {
    'ActivityID': 'Specific description based on JavaScript/SQL/branch analysis',
    ...
}

purposes = {
    'ActivityID': 'When and why this activity runs',
    ...
}
```

### Step 3: Merge Results

**Single Process:**
```python
from ReusableTools.IPA_ClientHandover.build_workflow_analysis_incremental import merge_chunk_results

merge_chunk_results(1, descriptions, purposes)
merge_chunk_results(2, descriptions, purposes)
...
```

**Multi-Process:**
```python
merge_chunk_results(1, descriptions, purposes, process_name='ProcessName1')
merge_chunk_results(2, descriptions, purposes, process_name='ProcessName1')
merge_chunk_results(1, descriptions, purposes, process_name='ProcessName2')
...
```

### Step 4: Verify Completion

```bash
python -c "import json; data = json.load(open('Temp/workflow_analysis.json')); print('Activities:', len(data['activity_descriptions']))"
```

## Example: Single Process

```bash
# Step 1: Generate chunks
python ReusableTools/IPA_ClientHandover/build_workflow_analysis_incremental.py

# Output:
# Found 1 process(es) to analyze
# PROCESS 1/1: MatchReport_Outbound
# Total activities to analyze: 39
# Splitting into 4 chunks of 10 activities each
# ✓ Chunk 1/4 saved: Temp\workflow_chunk_1.json
# ✓ Chunk 2/4 saved: Temp\workflow_chunk_2.json
# ✓ Chunk 3/4 saved: Temp\workflow_chunk_3.json
# ✓ Chunk 4/4 saved: Temp\workflow_chunk_4.json

# Step 2-3: Analyze and merge each chunk
# (AI analyzes chunk 1, generates descriptions/purposes, then merges)
# (AI analyzes chunk 2, generates descriptions/purposes, then merges)
# (AI analyzes chunk 3, generates descriptions/purposes, then merges)
# (AI analyzes chunk 4, generates descriptions/purposes, then merges)

# Step 4: Verify
python -c "import json; data = json.load(open('Temp/workflow_analysis.json')); print('Activities:', len(data['activity_descriptions']))"
# Output: Activities: 39
```

## Example: Multi-Process

```bash
# Step 1: Generate chunks
python ReusableTools/IPA_ClientHandover/build_workflow_analysis_incremental.py

# Output:
# Found 3 process(es) to analyze
# 
# PROCESS 1/3: InvoiceApproval_APIA_NONPOROUTING
# Total activities to analyze: 45
# Splitting into 5 chunks of 10 activities each
# ✓ Chunk 1/5 saved: Temp\workflow_chunk_InvoiceApproval_APIA_NONPOROUTING_1.json
# ...
# 
# PROCESS 2/3: InvoiceApproval_APIA_NONPOROUTING_Reject
# Total activities to analyze: 12
# Splitting into 2 chunks of 10 activities each
# ✓ Chunk 1/2 saved: Temp\workflow_chunk_InvoiceApproval_APIA_NONPOROUTING_Reject_1.json
# ...
# 
# PROCESS 3/3: InvoiceApproval_APIA_NONPOROUTING_nightly_job_trigger
# Total activities to analyze: 8
# Splitting into 1 chunks of 10 activities each
# ✓ Chunk 1/1 saved: Temp\workflow_chunk_InvoiceApproval_APIA_NONPOROUTING_nightly_job_trigger_1.json

# Step 2-3: Analyze and merge each chunk
# (AI analyzes each chunk with process_name parameter)

# Step 4: Verify
python -c "import json; data = json.load(open('Temp/workflow_analysis.json')); print('Activities:', len(data['activity_descriptions']))"
# Output: Activities: 65 (45 + 12 + 8)
```

## Activity Description Guidelines

When analyzing chunks, generate descriptions that:

1. **Are specific to the activity's code**
   - Analyze JavaScript transformations
   - Analyze SQL queries and data operations
   - Analyze branch conditions and routing logic

2. **Use business-friendly language**
   - Focus on WHAT, not HOW
   - Avoid technical jargon
   - Explain in terms of business operations

3. **Include relevant details**
   - Field names being processed
   - API endpoints being called
   - Transformation logic applied
   - Error conditions handled

4. **Describe when and why**
   - When does this activity run?
   - What triggers it?
   - What happens if it fails?

## Common Pitfalls

1. **Skipping chunks** - Analyze ALL chunks, not just the first few
2. **Generic descriptions** - Use actual code analysis, not type-based templates
3. **Missing process_name** - Multi-process requires process_name parameter
4. **Not verifying completion** - Always check final activity count matches expected

## Troubleshooting

**Issue**: "No processes found in lpd_structure.json"
- **Solution**: Run Phase 0 preprocessing first

**Issue**: Chunk files not created
- **Solution**: Check lpd_structure.json exists and has valid process data

**Issue**: Activity count mismatch
- **Solution**: Verify all chunks were analyzed and merged

**Issue**: Duplicate activity IDs
- **Solution**: Check if same chunk was merged twice

## Integration with Phase 5

Phase 5 (Report Assembly) reads `workflow_analysis.json` and expects:

```json
{
  "activity_descriptions": {
    "ActivityID": "Description"
  },
  "activity_purposes": {
    "ActivityID": "Purpose"
  }
}
```

The incremental approach produces this exact structure, so Phase 5 works seamlessly regardless of whether you used incremental or direct analysis.

## Performance

- **Chunk generation**: ~1 second per process
- **AI analysis per chunk**: ~30-45 seconds
- **Merge per chunk**: <1 second
- **Total for 39 activities**: ~3-4 minutes (4 chunks × 45s)
- **Total for 100 activities**: ~8-10 minutes (10 chunks × 45s)

## Benefits

✅ No context overload - each chunk is ~10 KB
✅ No crashes - stable execution regardless of process size
✅ Parallelizable - chunks can be analyzed concurrently
✅ Resumable - can restart from any chunk
✅ Scalable - works with any number of processes
