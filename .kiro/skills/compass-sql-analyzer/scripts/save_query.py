#!/usr/bin/env python3
"""
Save long SQL queries to Temp folder for analysis.

Usage:
    python scripts/save_query.py <query_text>
    python scripts/save_query.py --file <input_file>
"""

import sys
from pathlib import Path
from datetime import datetime

def save_query(query_text, output_dir="Temp"):
    """Save SQL query to Temp folder with timestamp"""
    
    # Create Temp directory if it doesn't exist
    temp_dir = Path(output_dir)
    temp_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"query_to_analyze_{timestamp}.sql"
    filepath = temp_dir / filename
    
    # Save query
    filepath.write_text(query_text, encoding='utf-8')
    
    print(f"✓ Query saved to: {filepath}")
    print(f"✓ Lines: {len(query_text.splitlines())}")
    print(f"✓ Characters: {len(query_text)}")
    
    return str(filepath)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python save_query.py <query_text>")
        print("  python save_query.py --file <input_file>")
        sys.exit(1)
    
    if sys.argv[1] == "--file":
        # Read from file
        if len(sys.argv) < 3:
            print("Error: --file requires input file path")
            sys.exit(1)
        
        input_file = Path(sys.argv[2])
        if not input_file.exists():
            print(f"Error: File not found: {input_file}")
            sys.exit(1)
        
        query_text = input_file.read_text(encoding='utf-8')
    else:
        # Read from command line argument
        query_text = sys.argv[1]
    
    # Save query
    save_query(query_text)

if __name__ == "__main__":
    main()
