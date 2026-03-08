#!/usr/bin/env python3
"""
IPA Coding Standards - Error Handling Analysis Builder
Incremental analysis script for error handling domain.

Usage:
    python build_errorhandling_analysis.py [analyze|merge]
"""

import json
import sys
from pathlib import Path

def load_json(filepath):
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """Save JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def chunk_errorhandling_data(eh_data, chunk_size=20):
    """Chunk error handling data for incremental analysis"""
    chunks = []
    nodes = eh_data.get('nodes_analysis', [])
    
    for i in range(0, len(nodes), chunk_size):
        chunk_nodes = nodes[i:i+chunk_size]
        chunks.append({
            'chunk_id': len(chunks) + 1,
            'category': 'error_handling_nodes',
            'data': {
                'nodes': chunk_nodes,
                'chunk_range': f"{i+1}-{i+len(chunk_nodes)}",
                'has_get_work_unit_errors': eh_data.get('has_get_work_unit_errors', False)
            }
        })
    
    return chunks

def analyze_mode():
    """Analyze error handling domain data"""
    print("=" * 80)
    print("PHASE 4: ERROR HANDLING ANALYSIS")
    print("=" * 80)
    print()
    
    temp_dir = Path('Temp')
    domain_files = list(temp_dir.glob('*_domain_errorhandling.json'))
    
    if not domain_files:
        print("❌ Error: No error handling domain file found")
        sys.exit(1)
    
    domain_file = domain_files[0]
    print(f"[1/4] Loading error handling domain data: {domain_file.name}")
    eh_data = load_json(domain_file)
    
    standards_file = temp_dir / 'project_standards.json'
    print(f"[2/4] Loading project standards: {standards_file.name}")
    project_standards = load_json(standards_file)
    
    print(f"[3/4] Chunking error handling data...")
    chunks = chunk_errorhandling_data(eh_data)
    print(f"   ✓ Created {len(chunks)} chunks")
    
    print(f"[4/4] Saving chunks for AI analysis...")
    for chunk in chunks:
        chunk_file = temp_dir / f"errorhandling_chunk_{chunk['chunk_id']}.json"
        save_json(chunk, chunk_file)
        print(f"   ✓ {chunk_file.name}")
    
    metadata = {
        'total_chunks': len(chunks),
        'chunk_files': [f"errorhandling_chunk_{i+1}.json" for i in range(len(chunks))],
        'statistics': eh_data.get('statistics', {})
    }
    save_json(metadata, temp_dir / 'errorhandling_metadata.json')
    
    print()
    print("=" * 80)
    print("CHUNKS READY FOR AI ANALYSIS")
    print("=" * 80)
    print()
    
    return 0

def merge_mode():
    """Merge analyzed chunks"""
    print("=" * 80)
    print("PHASE 4: ERROR HANDLING ANALYSIS - MERGE")
    print("=" * 80)
    print()
    
    temp_dir = Path('Temp')
    metadata_file = temp_dir / 'errorhandling_metadata.json'
    
    if not metadata_file.exists():
        print("❌ Error: errorhandling_metadata.json not found")
        sys.exit(1)
    
    metadata = load_json(metadata_file)
    total_chunks = metadata['total_chunks']
    
    print(f"[1/2] Loading {total_chunks} analyzed chunks...")
    
    merged = {
        'domain': 'errorhandling',
        'violations': [],
        'statistics': metadata.get('statistics', {})
    }
    
    for i in range(1, total_chunks + 1):
        chunk_file = temp_dir / f"errorhandling_chunk_{i}_analyzed.json"
        if not chunk_file.exists():
            print(f"   ❌ Missing: {chunk_file.name}")
            sys.exit(1)
        
        chunk_analysis = load_json(chunk_file)
        violations = chunk_analysis.get('violations', [])
        merged['violations'].extend(violations)
        print(f"   ✓ Chunk {i}: {len(violations)} violations")
    
    print(f"[2/2] Saving merged analysis...")
    output_file = temp_dir / 'errorhandling_analysis.json'
    save_json(merged, output_file)
    print(f"   ✓ {output_file}")
    
    print()
    print("=" * 80)
    print("PHASE 4 COMPLETE")
    print("=" * 80)
    print()
    print(f"Total violations: {len(merged['violations'])}")
    print()
    
    return 0

def main():
    """Main entry point"""
    mode = sys.argv[1] if len(sys.argv) > 1 else 'analyze'
    
    if mode == 'analyze':
        return analyze_mode()
    elif mode == 'merge':
        return merge_mode()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python build_errorhandling_analysis.py [analyze|merge]")
        return 1

if __name__ == '__main__':
    sys.exit(main())
