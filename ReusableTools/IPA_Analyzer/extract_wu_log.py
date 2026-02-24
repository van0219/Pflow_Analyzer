#!/usr/bin/env python3
"""
Work Unit Log Data Extraction Tool

Purpose: Extract structured data from work unit logs for Kiro to analyze
This tool does NOT analyze - it only extracts and organizes data

Output: JSON file with performance metrics, activity execution data
"""

import re
import json
from datetime import datetime
from pathlib import Path


def extract_wu_log(log_file: str, output_file: str = None) -> dict:
    """
    Extract structured data from work unit log
    
    Args:
        log_file: Path to work unit log file
        output_file: Optional output JSON file path
    
    Returns:
        Dictionary with extracted data
    """
    print(f"Extracting data from {Path(log_file).name}...")
    
    with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    result = {
        'file': Path(log_file).name,
        'metadata': extract_metadata(content),
        'activities': extract_activities(content),
        'variables': extract_variables(content),
        'errors': extract_errors(content)
    }
    
    # Save to JSON if output file specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(result, f, indent=2)
        print(f"✓ Data saved to {output_file}")
    
    return result


def extract_metadata(content: str) -> dict:
    """Extract work unit metadata"""
    metadata = {}
    
    # Work unit number - try multiple patterns (handle commas in numbers like "36,829")
    wu_match = re.search(r'Workunit\s+([\d,]+)\s+started', content, re.IGNORECASE)
    if not wu_match:
        wu_match = re.search(r'Work Unit:\s*([\d,]+)', content, re.IGNORECASE)
    metadata['work_unit_number'] = wu_match.group(1) if wu_match else 'Unknown'
    
    # Auto restart
    auto_restart_match = re.search(r'Auto Restart:\s*(\w+)', content, re.IGNORECASE)
    metadata['auto_restart'] = auto_restart_match.group(1) if auto_restart_match else 'Unknown'
    
    # Process name
    process_match = re.search(r'Process name:\s*(.+)', content)
    metadata['process_name'] = process_match.group(1).strip() if process_match else 'Unknown'
    
    # Service name
    service_match = re.search(r'Service name:\s*(.+)', content)
    metadata['service_name'] = service_match.group(1).strip() if service_match else 'Unknown'
    
    # Start and end times - get the first workunit start and last activity complete
    start_match = re.search(r'Workunit [\d,]+ started @ (.+)', content)
    # Find last completed activity
    end_matches = list(re.finditer(r'completed @ (.+)', content))
    end_match = end_matches[-1] if end_matches else None
    
    if start_match:
        metadata['start_time'] = start_match.group(1).strip()
    if end_match:
        metadata['end_time'] = end_match.group(1).strip()
    
    # Calculate duration
    if start_match and end_match:
        try:
            start_time = datetime.strptime(start_match.group(1).strip(), '%m/%d/%Y %I:%M:%S.%f %p')
            end_time = datetime.strptime(end_match.group(1).strip(), '%m/%d/%Y %I:%M:%S.%f %p')
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            metadata['duration_ms'] = duration_ms
            metadata['duration_readable'] = format_duration(duration_ms)
        except Exception as e:
            metadata['duration_ms'] = None
            metadata['duration_readable'] = 'Unknown'
    
    # Status
    if 'completed @' in content:
        metadata['status'] = 'Completed'
    elif 'failed @' in content or 'ERROR:' in content:
        metadata['status'] = 'Failed'
    else:
        metadata['status'] = 'Unknown'
    
    return metadata


def extract_activities(content: str) -> list:
    """Extract activity execution data with timing and performance info"""
    activities = []
    
    # Pattern: Activity name:<name> type:<type> id:<id> started @ <time>
    activity_pattern = r'Activity name:\s*(\S+)\s+type:(\w+)\s+id:(\d+)\s+started @ (.+)'
    
    for match in re.finditer(activity_pattern, content):
        activity_name = match.group(1).strip()
        activity_type = match.group(2).strip()
        activity_id = match.group(3).strip()
        start_time = match.group(4).strip()
        
        # Find corresponding completion
        completion_pattern = rf'{re.escape(activity_name)}\s+id:{activity_id}\s+completed @ (.+)'
        completion_match = re.search(completion_pattern, content)
        
        activity_data = {
            'name': activity_name,
            'type': activity_type,
            'id': activity_id,
            'start_time': start_time
        }
        
        if completion_match:
            end_time = completion_match.group(1).strip()
            activity_data['end_time'] = end_time
            
            # Calculate duration
            try:
                start_dt = datetime.strptime(start_time, '%m/%d/%Y %I:%M:%S.%f %p')
                end_dt = datetime.strptime(end_time, '%m/%d/%Y %I:%M:%S.%f %p')
                duration_ms = int((end_dt - start_dt).total_seconds() * 1000)
                activity_data['duration_ms'] = duration_ms
            except:
                activity_data['duration_ms'] = None
        
        activities.append(activity_data)
    
    return activities


def extract_variables(content: str) -> dict:
    """Extract variable values from log"""
    variables = {}
    
    # Pattern: variable name = value (with proper line boundaries)
    # Match lines that start with whitespace followed by variable = value
    var_pattern = r'^\s+(\w+)\s*=\s*(.*)$'
    
    for match in re.finditer(var_pattern, content, re.MULTILINE):
        var_name = match.group(1).strip()
        var_value = match.group(2).strip()
        
        # Skip empty values and very long values
        if var_value and len(var_value) < 500:
            # Only store if not already present or if this is a more complete value
            if var_name not in variables or len(var_value) > len(variables.get(var_name, '')):
                variables[var_name] = var_value
    
    return variables


def extract_errors(content: str) -> list:
    """Extract error messages"""
    errors = []
    
    # Error patterns
    error_patterns = [
        r'ERROR:\s*(.+?)(?=\n\n|\Z)',
        r'Exception:\s*(.+?)(?=\n\n|\Z)',
        r'Failed:\s*(.+?)(?=\n\n|\Z)'
    ]
    
    for pattern in error_patterns:
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            error_text = match.group(1).strip()
            if error_text and len(error_text) < 500:
                errors.append(error_text)
    
    return errors


def format_duration(ms: int) -> str:
    """Format duration in human-readable format"""
    if ms < 1000:
        return f"{ms}ms"
    elif ms < 60000:
        return f"{ms/1000:.2f}s"
    elif ms < 3600000:
        return f"{ms/60000:.2f}min"
    else:
        return f"{ms/3600000:.2f}hr"


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_wu_log.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    output_file = 'Temp/wu_log_data.json'
    
    result = extract_wu_log(log_file, output_file)
    print(f"\nExtracted:")
    print(f"  - Work Unit: {result['metadata']['work_unit_number']}")
    print(f"  - Status: {result['metadata']['status']}")
    print(f"  - Duration: {result['metadata'].get('duration_readable', 'Unknown')}")
    print(f"  - Activities: {len(result['activities'])}")
    print(f"  - Variables: {len(result['variables'])}")
    print(f"  - Errors: {len(result['errors'])}")
