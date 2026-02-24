# Reusable Tools Hardening

## Overview

Systematically improve all ReusableTools to be truly reusable, helpful, intelligent, and robust. Fix encoding issues, add comprehensive error handling, improve diagnostics, and ensure tools work reliably in all scenarios.

## Goals

1. **Robustness**: Tools handle edge cases gracefully without crashing
2. **Intelligence**: Tools provide helpful diagnostics and suggestions
3. **Reusability**: Tools work in any context with clear interfaces
4. **Reliability**: Tools produce consistent results across different environments

## Current Issues

### 1. hook_manager.py - Encoding Error
- **Issue**: `'charmap' codec can't decode byte 0x8f` when exporting hooks
- **Root Cause**: Not handling UTF-8 encoding properly in export() function
- **Impact**: Cannot export hooks to clean JSON files
- **Priority**: HIGH

### 2. General Tool Quality
- **Issue**: Tools may not handle all edge cases
- **Need**: Comprehensive error handling, validation, diagnostics
- **Priority**: MEDIUM

## Requirements

### R1: Encoding Handling
All tools that read/write files must:
- Use UTF-8 encoding explicitly
- Handle encoding errors gracefully
- Provide clear error messages about encoding issues
- Support both Windows and Unix line endings

### R2: Error Handling
All tools must:
- Catch and handle exceptions gracefully
- Provide actionable error messages
- Suggest fixes when errors occur
- Never crash without explanation

### R3: Validation
All tools must:
- Validate inputs before processing
- Check file existence before reading
- Verify data structure before operating
- Provide clear validation error messages

### R4: Diagnostics
All tools must:
- Provide verbose mode for debugging
- Show progress for long operations
- Return structured results (JSON/dict)
- Include context in error messages

### R5: Documentation
All tools must:
- Have clear docstrings
- Include usage examples
- Document all parameters
- Explain return values

## Design

### Phase 1: Fix Critical Issues (hook_manager.py)

**Task 1.1: Fix export() encoding**
- Add explicit UTF-8 encoding to file operations
- Handle encoding errors with fallback
- Test with hooks containing special characters

**Task 1.2: Fix validate() encoding**
- Ensure UTF-8 reading in validate()
- Handle control characters properly
- Test with all existing hooks

**Task 1.3: Add encoding tests**
- Test with Unicode characters
- Test with control characters
- Test with mixed encodings

### Phase 2: Enhance hook_manager.py

**Task 2.1: Add update() function**
- Safely update hook fields
- Validate changes before saving
- Create backup automatically
- Return diff of changes

**Task 2.2: Add search() function**
- Search hooks by name/description
- Search prompt content
- Return matching hooks

**Task 2.3: Add lint() function**
- Check for common issues
- Suggest improvements
- Validate hook structure

### Phase 3: Audit Other Tools

**Task 3.1: Review excel_reader.py**
- Check encoding handling
- Verify error messages
- Test edge cases

**Task 3.2: Review IPA_Analyzer tools**
- Check file handling
- Verify error handling
- Test with malformed inputs

**Task 3.3: Review template generators**
- Check encoding
- Verify error handling
- Test with edge cases

### Phase 4: Create Tool Standards

**Task 4.1: Create tool template**
- Standard structure
- Required functions
- Error handling patterns
- Documentation format

**Task 4.2: Create testing guide**
- Test cases to cover
- Edge cases to check
- Validation requirements

**Task 4.3: Document best practices**
- Encoding handling
- Error messages
- Progress reporting
- Return value structure

## Implementation Tasks

### Task 1: Fix hook_manager.py Encoding (COMPLETED ✅)

**Status**: COMPLETE - All encoding issues fixed

**Files modified:**
- `ReusableTools/hook_manager.py`

**Changes made:**

1. **validate() function** - Added `errors='replace'` parameter and UnicodeDecodeError handling
2. **export() function** - Added `errors='replace'` to both read and write operations
3. **analyze() function** - Added `errors='replace'` parameter
4. **repair() function** - Added `errors='replace'` to both read and write operations
5. **All functions** - Added specific UnicodeDecodeError exception handling with helpful messages

**Testing:**
- ✅ Successfully exported available-tools-reminder.kiro.hook
- ✅ Successfully validated all hooks
- ✅ Successfully updated hook with new content
- ✅ All operations handle UTF-8 with special characters

**Result**: hook_manager.py now handles encoding robustly and provides clear error messages.

### Task 2: Add update() Function

**New function to add:**
```python
def update(self, filepath, updates):
    """
    Safely update hook fields
    
    Parameters:
        filepath: Path to hook file
        updates: Dict of fields to update
    
    Returns:
        dict with success, backup_path, changes
    """
    # 1. Backup first
    # 2. Load hook
    # 3. Validate updates
    # 4. Apply updates
    # 5. Validate result
    # 6. Save
    # 7. Return diff
```

### Task 3: Test Suite

**Create test file**: `ReusableTools/test_hook_manager.py`

Test cases:
1. Read hook with UTF-8 characters
2. Read hook with control characters
3. Export hook with special characters
4. Update hook fields
5. Validate malformed hook
6. Repair corrupted hook
7. Backup and restore
8. Diff two hooks

## Acceptance Criteria

### AC1: hook_manager.py Encoding Fixed
- ✓ Can export all existing hooks without errors
- ✓ Can validate all existing hooks without errors
- ✓ Handles UTF-8 characters correctly
- ✓ Provides clear error messages for encoding issues

### AC2: hook_manager.py Enhanced
- ✓ update() function works reliably
- ✓ search() function finds hooks
- ✓ lint() function catches issues
- ✓ All functions have comprehensive error handling

### AC3: All Tools Audited
- ✓ All tools handle encoding properly
- ✓ All tools have error handling
- ✓ All tools provide diagnostics
- ✓ All tools are documented

### AC4: Standards Documented
- ✓ Tool template created
- ✓ Testing guide created
- ✓ Best practices documented
- ✓ Examples provided

## Success Metrics

1. **Zero encoding errors** when using any tool
2. **Clear error messages** for all failure modes
3. **Comprehensive diagnostics** for debugging
4. **100% of tools** follow standards
5. **All tools tested** with edge cases

## Timeline

- **Phase 1** (Immediate): Fix hook_manager.py encoding - 30 min
- **Phase 2** (Today): Enhance hook_manager.py - 1 hour
- **Phase 3** (This week): Audit other tools - 2 hours
- **Phase 4** (This week): Create standards - 1 hour

## Notes

- Start with hook_manager.py since it's blocking current work
- Apply learnings to other tools systematically
- Document patterns for future tool development
- Create reusable error handling utilities
