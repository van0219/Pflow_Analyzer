#!/usr/bin/env python3
"""
Excel Reader Utility

Purpose: Read Excel files (.xlsx, .xls) with support for:
- Multiple sheets
- Large datasets
- Structured output (JSON, dict, or display)
- Error handling for binary files

Usage:
    from ReusableTools.excel_reader import read_excel, read_excel_to_json
    
    # Read single sheet
    df = read_excel('file.xlsx', sheet_name='Sheet1')
    
    # Read all sheets
    all_sheets = read_excel('file.xlsx', sheet_name=None)
    
    # Export to JSON
    read_excel_to_json('file.xlsx', 'output.json', sheet_name='Standards')
"""

import pandas as pd
import json
import sys
from pathlib import Path


def _find_sheet_name(file_path, sheet_name):
    """
    Find sheet name with fuzzy matching (handles emojis, case-insensitive).
    
    Args:
        file_path (str): Path to Excel file
        sheet_name (str|int): Sheet name or index
    
    Returns:
        str|int: Matched sheet name or original input
    """
    if isinstance(sheet_name, int):
        return sheet_name
    
    try:
        xl_file = pd.ExcelFile(file_path)
        available_sheets = xl_file.sheet_names
        
        # Exact match (case-sensitive)
        if sheet_name in available_sheets:
            return sheet_name
        
        # Case-insensitive match
        for sheet in available_sheets:
            if sheet.lower() == sheet_name.lower():
                return sheet
        
        # Match without emojis (strip emojis from both sides)
        import re
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002300-\U000023FF"  # misc technical
            u"\U00002600-\U000027BF"  # misc symbols
            u"\U00002702-\U000027B0"  # dingbats
            u"\U000024C2-\U0001F251"
            u"\U0001F900-\U0001F9FF"  # supplemental
            "]+", flags=re.UNICODE)
        
        sheet_name_no_emoji = emoji_pattern.sub('', sheet_name).strip()
        
        for sheet in available_sheets:
            sheet_no_emoji = emoji_pattern.sub('', sheet).strip()
            if sheet_no_emoji.lower() == sheet_name_no_emoji.lower():
                return sheet
        
        # If no match found, return original (will raise error later)
        return sheet_name
        
    except Exception:
        return sheet_name


def read_excel(file_path, sheet_name=0, display=False, max_rows=None):
    """
    Read Excel file and return DataFrame or dict of DataFrames.
    
    Args:
        file_path (str): Path to Excel file
        sheet_name (str|int|None): Sheet name, index, or None for all sheets
        display (bool): Print DataFrame to console
        max_rows (int): Limit rows displayed (None = all rows)
    
    Returns:
        DataFrame or dict of DataFrames
    """
    try:
        # Find matching sheet name (handles emojis)
        if sheet_name is not None and sheet_name != 0:
            sheet_name = _find_sheet_name(file_path, sheet_name)
        
        # Read Excel file
        if sheet_name is None:
            # Read all sheets
            data = pd.read_excel(file_path, sheet_name=None)
            
            if display:
                for name, df in data.items():
                    print(f"\n{'='*80}")
                    print(f"Sheet: {name}")
                    print(f"{'='*80}")
                    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                    print(f"\nColumns: {', '.join(df.columns.tolist())}")
                    print(f"\nData:")
                    if max_rows:
                        print(df.head(max_rows).to_string(index=False))
                        if len(df) > max_rows:
                            print(f"\n... ({len(df) - max_rows} more rows)")
                    else:
                        print(df.to_string(index=False))
            
            return data
        else:
            # Read single sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            if display:
                print(f"\n{'='*80}")
                print(f"File: {file_path}")
                print(f"Sheet: {sheet_name}")
                print(f"{'='*80}")
                print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                print(f"\nColumns: {', '.join(df.columns.tolist())}")
                print(f"\nData:")
                if max_rows:
                    print(df.head(max_rows).to_string(index=False))
                    if len(df) > max_rows:
                        print(f"\n... ({len(df) - max_rows} more rows)")
                else:
                    print(df.to_string(index=False))
            
            return df
            
    except Exception as e:
        print(f"Error reading Excel file: {e}", file=sys.stderr)
        raise


def read_excel_to_json(file_path, output_path, sheet_name=0, orient='records'):
    """
    Read Excel file and export to JSON.
    
    Args:
        file_path (str): Path to Excel file
        output_path (str): Path to output JSON file
        sheet_name (str|int|None): Sheet name, index, or None for all sheets
        orient (str): JSON orientation ('records', 'index', 'columns', 'values')
    
    Returns:
        str: Path to output JSON file
    """
    try:
        data = read_excel(file_path, sheet_name=sheet_name)
        
        if isinstance(data, dict):
            # Multiple sheets
            json_data = {name: df.to_dict(orient=orient) for name, df in data.items()}
        else:
            # Single sheet
            json_data = data.to_dict(orient=orient)
        
        # Write JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error exporting to JSON: {e}", file=sys.stderr)
        raise


def get_sheet_names(file_path):
    """
    Get list of sheet names in Excel file.
    
    Args:
        file_path (str): Path to Excel file
    
    Returns:
        list: Sheet names
    """
    try:
        xl_file = pd.ExcelFile(file_path)
        return xl_file.sheet_names
    except Exception as e:
        print(f"Error reading sheet names: {e}", file=sys.stderr)
        raise


def read_excel_summary(file_path):
    """
    Get summary information about Excel file.
    
    Args:
        file_path (str): Path to Excel file
    
    Returns:
        dict: Summary information
    """
    try:
        xl_file = pd.ExcelFile(file_path)
        summary = {
            'file': file_path,
            'sheets': []
        }
        
        for sheet_name in xl_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            summary['sheets'].append({
                'name': sheet_name,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist()
            })
        
        return summary
        
    except Exception as e:
        print(f"Error reading Excel summary: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Read Excel files')
    parser.add_argument('file', help='Path to Excel file')
    parser.add_argument('--sheet', default=0, help='Sheet name or index (default: 0)')
    parser.add_argument('--all-sheets', action='store_true', help='Read all sheets')
    parser.add_argument('--list-sheets', action='store_true', help='List all sheet names')
    parser.add_argument('--summary', action='store_true', help='Show file summary')
    parser.add_argument('--json', help='Export to JSON file')
    parser.add_argument('--max-rows', type=int, help='Limit rows displayed')
    
    args = parser.parse_args()
    
    if args.list_sheets:
        sheets = get_sheet_names(args.file)
        print(f"\n{'='*80}")
        print(f"File: {args.file}")
        print(f"{'='*80}")
        print(f"Total Sheets: {len(sheets)}\n")
        for i, sheet in enumerate(sheets):
            print(f"{i}: {sheet}")
    elif args.summary:
        summary = read_excel_summary(args.file)
        print(json.dumps(summary, indent=2))
    elif args.json:
        sheet = None if args.all_sheets else args.sheet
        read_excel_to_json(args.file, args.json, sheet_name=sheet)
    else:
        sheet = None if args.all_sheets else args.sheet
        read_excel(args.file, sheet_name=sheet, display=True, max_rows=args.max_rows)
