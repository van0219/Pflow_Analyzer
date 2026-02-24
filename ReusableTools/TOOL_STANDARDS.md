# ReusableTools Standards

## Purpose

This document defines the standards that all tools in `ReusableTools/` must follow to ensure consistency, reliability, and maintainability.

## Core Principles

1. **Robustness**: Tools handle edge cases gracefully without crashing
2. **Intelligence**: Tools provide helpful diagnostics and suggestions
3. **Reusability**: Tools work in any context with clear interfaces
4. **Reliability**: Tools produce consistent results across different environments

## Required Standards

### 1. File Operations

**Encoding**: All file operations MUST use UTF-8 with error handling

```python
# Reading files
with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Writing files
with open(filepath, 'w', encoding='utf-8', newline='\n', errors='replace') as f:
    f.write(content)
```

**Why**: Prevents encoding errors with special characters, ensures cross-platform compatibility

### 2. Error Handling

**Structure**: Use specific exception handling with actionable messages

```python
try:
    # Operation
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        data = json.load(f)
except FileNotFoundError:
    return {
        'success': False,
        'error': f'File not found: {filepath}',
        'suggestion': 'Check the file path and try again'
    }
except json.JSONDecodeError as e:
    return {
        'success': False,
        'error': f'Invalid JSON at line {e.lineno}: {e.msg}',
        'suggestion': 'Validate JSON syntax or use repair tool'
    }
except Exception as e:
    return {
        'success': False,
        'error': f'Unexpected error: {e}'
    }
```

**Why**: Users know exactly what went wrong and how to fix it

### 3. Input Validation

**Validate before processing**:

```python
def process_file(filepath):
    """Process a file with validation"""
    
    # Check file exists
    if not Path(filepath).exists():
        return {'success': False, 'error': f'File not found: {filepath}'}
    
    # Check file is readable
    if not os.access(filepath, os.R_OK):
        return {'success': False, 'error': f'File not readable: {filepath}'}
    
    # Check file size (optional)
    file_size = Path(filepath).stat().st_size
    if file_size > 100_000_000:  # 100MB
        return {
            'success': False,
            'error': f'File too large: {file_size / 1_000_000:.1f}MB',
            'suggestion': 'Split file or use streaming approach'
        }
    
    # Process file
    # ...
```

**Why**: Fail fast with clear messages instead of cryptic errors later

### 4. Return Values

**Structure**: Return dictionaries with consistent structure

```python
# Success
return {
    'success': True,
    'result': data,
    'metadata': {
        'processed': 100,
        'skipped': 5,
        'duration': 1.23
    }
}

# Failure
return {
    'success': False,
    'error': 'Description of what went wrong',
    'suggestion': 'How to fix it',
    'context': {
        'file': filepath,
        'line': 42
    }
}
```

**Why**: Consistent interface makes tools composable and predictable

### 5. Documentation

**Docstrings**: Every function must have a docstring

```python
def process_data(input_file, output_file, options=None):
    """
    Process data from input file and save to output file.
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output file
        options (dict, optional): Processing options
            - 'format': Output format ('json', 'csv')
            - 'validate': Validate before processing (default: True)
    
    Returns:
        dict: Result with success status and metadata
            {
                'success': bool,
                'processed': int,
                'output_path': str
            }
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If options are invalid
    
    Example:
        >>> result = process_data('input.json', 'output.csv', {'format': 'csv'})
        >>> print(result['processed'])
        100
    """
```

**Why**: Self-documenting code reduces support burden

### 6. CLI Interface

**Use argparse for command-line tools**:

```python
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Tool description',
        epilog='Example: python tool.py input.json --output result.json'
    )
    parser.add_argument('input', help='Input file path')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Process
    result = process_file(args.input, args.output, verbose=args.verbose)
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)
```

**Why**: Consistent CLI experience across all tools

### 7. Progress Reporting

**For long operations, show progress**:

```python
def process_large_dataset(items):
    """Process items with progress reporting"""
    total = len(items)
    
    for i, item in enumerate(items, 1):
        # Process item
        process_item(item)
        
        # Show progress every 10%
        if i % (total // 10) == 0:
            print(f"Progress: {i}/{total} ({i*100//total}%)")
    
    print(f"✓ Completed: {total} items processed")
```

**Why**: Users know the tool is working and can estimate completion time

### 8. Logging

**Use logging module for debug output**:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_file(filepath):
    """Process file with logging"""
    logger.info(f"Processing file: {filepath}")
    
    try:
        # Process
        logger.debug(f"Reading file: {filepath}")
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            data = f.read()
        
        logger.info(f"✓ Processed {len(data)} bytes")
        return {'success': True}
        
    except Exception as e:
        logger.error(f"Failed to process {filepath}: {e}")
        return {'success': False, 'error': str(e)}
```

**Why**: Debugging is easier with structured logs

## Tool Template

Use this template for new tools:

```python
#!/usr/bin/env python3
"""
Tool Name - Brief description

Purpose: What this tool does and why it exists

Usage:
    python tool_name.py <input> [options]
    
    # As module
    from ReusableTools.tool_name import main_function
    result = main_function(input_data)

Examples:
    python tool_name.py input.json --output result.json
"""

import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main_function(input_data, options=None):
    """
    Main processing function.
    
    Args:
        input_data: Input data to process
        options (dict, optional): Processing options
    
    Returns:
        dict: Result with success status
    """
    try:
        # Validate input
        if not input_data:
            return {
                'success': False,
                'error': 'Input data is required'
            }
        
        # Process
        logger.info("Processing data...")
        result = process_data(input_data, options)
        
        logger.info("✓ Processing complete")
        return {
            'success': True,
            'result': result
        }
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def process_data(data, options):
    """Process the data"""
    # Implementation
    return data


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Tool description')
    parser.add_argument('input', help='Input file or data')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Process
    result = main_function(args.input)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✓ Output saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    # Exit
    sys.exit(0 if result['success'] else 1)
```

## Testing Checklist

Before committing a new tool, verify:

- [ ] All file operations use `encoding='utf-8', errors='replace'`
- [ ] Input validation with clear error messages
- [ ] Comprehensive error handling with try/except
- [ ] Return values follow standard structure
- [ ] Docstrings for all functions
- [ ] CLI interface with argparse (if applicable)
- [ ] Progress reporting for long operations
- [ ] Logging for debug output
- [ ] Tested with edge cases:
  - [ ] Empty input
  - [ ] Missing files
  - [ ] Invalid data
  - [ ] Large files
  - [ ] Special characters in filenames
  - [ ] Unicode content

## Examples of Good Tools

Reference these tools as examples:

1. **hook_manager.py** - Comprehensive error handling, validation, CLI interface
2. **excel_reader.py** - Good documentation, multiple output formats
3. **extract_lpd_data.py** - Clean structure, proper encoding

## Common Pitfalls

### ❌ Don't Do This

```python
# No encoding specified
with open(file, 'r') as f:
    data = f.read()

# Generic error handling
try:
    process()
except:
    print("Error")

# No validation
def process(file):
    with open(file) as f:  # Will crash if file doesn't exist
        return f.read()
```

### ✅ Do This Instead

```python
# Proper encoding
with open(file, 'r', encoding='utf-8', errors='replace') as f:
    data = f.read()

# Specific error handling
try:
    process()
except FileNotFoundError as e:
    return {'success': False, 'error': f'File not found: {e}'}
except Exception as e:
    return {'success': False, 'error': f'Unexpected error: {e}'}

# With validation
def process(file):
    if not Path(file).exists():
        return {'success': False, 'error': f'File not found: {file}'}
    
    with open(file, 'r', encoding='utf-8', errors='replace') as f:
        return {'success': True, 'data': f.read()}
```

## Maintenance

- Review this document quarterly
- Update based on lessons learned
- Add new patterns as they emerge
- Keep examples current

## Questions?

If you're unsure about a standard, check existing tools or ask for clarification.

**Remember**: These standards exist to make tools reliable and maintainable. Follow them consistently.
