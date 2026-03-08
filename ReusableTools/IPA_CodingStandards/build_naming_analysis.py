#!/usr/bin/env python3
"""
IPA Coding Standards - Naming Analysis Builder
Incremental analysis script for naming conventions domain.

Usage:
    python build_naming_analysis.py [analyze|merge]
    
    analyze: Analyze naming domain data (default)
    merge: Merge chunk results into final naming_analysis.json
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

def chunk_naming_data(naming_data, chunk_size=50):
    """Chunk naming data for incremental analysis"""
    chunks = []
    
    # Chunk 1: Filename analysis
    chunks.append({
        'chunk_id': 1,
        'category': 'filename',
        'data': {
            'filename': naming_data.get('filename'),
            'process_type': naming_data.get('process_type')
        }
    })
    
    # Chunk 2+: Node captions (chunked by chunk_size)
    generic_nodes = naming_data.get('generic_nodes', [])
    for i in range(0, len(generic_nodes), chunk_size):
        chunk_nodes = generic_nodes[i:i+chunk_size]
        chunks.append({
            'chunk_id': len(chunks) + 1,
            'category': 'node_captions',
            'data': {
                'nodes': chunk_nodes,
                'chunk_range': f"{i+1}-{i+len(chunk_nodes)}"
            }
        })
    
    # Last chunk: Config sets and hardcoded values
    chunks.append({
        'chunk_id': len(chunks) + 1,
        'category': 'config_and_hardcoded',
        'data': {
            'config_sets': naming_data.get('config_sets', {}),
            'generic_config_sets': naming_data.get('generic_config_sets', []),
            'hardcoded_values': naming_data.get('hardcoded_values', [])
        }
    })
    
    return chunks

def analyze_mode():
    """Analyze naming domain data"""
    print("=" * 80)
    print("PHASE 1: NAMING ANALYSIS")
    print("=" * 80)
    print()
    
    # Load domain data
    temp_dir = Path('Temp')
    domain_files = list(temp_dir.glob('*_domain_naming.json'))
    
    if not domain_files:
        print("❌ Error: No naming domain file found in Temp/")
        print("   Expected: Temp/*_domain_naming.json")
        sys.exit(1)
    
    domain_file = domain_files[0]
    print(f"[1/4] Loading naming domain data: {domain_file.name}")
    naming_data = load_json(domain_file)
    
    # Load project standards
    standards_file = temp_dir / 'project_standards.json'
    if not standards_file.exists():
        print("❌ Error: project_standards.json not found in Temp/")
        sys.exit(1)
    
    print(f"[2/4] Loading project standards: {standards_file.name}")
    project_standards = load_json(standards_file)
    
    # Chunk data
    print(f"[3/4] Chunking naming data...")
    chunks = chunk_naming_data(naming_data)
    print(f"   ✓ Created {len(chunks)} chunks")
    
    # Save chunks for AI analysis
    print(f"[4/4] Saving chunks for AI analysis...")
    for chunk in chunks:
        chunk_file = temp_dir / f"naming_chunk_{chunk['chunk_id']}.json"
        save_json(chunk, chunk_file)
        print(f"   ✓ {chunk_file.name}")
    
    # Save metadata
    metadata = {
        'total_chunks': len(chunks),
        'chunk_files': [f"naming_chunk_{i+1}.json" for i in range(len(chunks))],
        'statistics': naming_data.get('statistics', {})
    }
    save_json(metadata, temp_dir / 'naming_metadata.json')
    
    print()
    print("=" * 80)
    print("CHUNKS READY FOR AI ANALYSIS")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. AI analyzes each chunk")
    print("  2. AI saves results as naming_chunk_N_analyzed.json")
    print("  3. Run: python build_naming_analysis.py merge")
    print()
    
    return 0

def merge_mode():
    """Merge analyzed chunks into final naming_analysis.json"""
    print("=" * 80)
    print("PHASE 1: NAMING ANALYSIS - MERGE")
    print("=" * 80)
    print()
    
    temp_dir = Path('Temp')
    
    # Load metadata
    metadata_file = temp_dir / 'naming_metadata.json'
    if not metadata_file.exists():
        print("❌ Error: naming_metadata.json not found")
        print("   Run analyze mode first")
        sys.exit(1)
    
    metadata = load_json(metadata_file)
    total_chunks = metadata['total_chunks']
    
    # Load project standards for rule_name mapping
    standards_file = temp_dir / 'project_standards.json'
    rule_map = {}
    if standards_file.exists():
        project_standards = load_json(standards_file)
        rule_map = {std['Rule_ID']: std['Rule_Name'] for std in project_standards}
    
    print(f"[1/3] Loading {total_chunks} analyzed chunks...")
    
    # Initialize merged analysis
    merged = {
        'domain': 'naming',
        'violations': [],
        'statistics': metadata.get('statistics', {})
    }
    
    # Merge chunks
    for i in range(1, total_chunks + 1):
        chunk_file = temp_dir / f"naming_chunk_{i}_analyzed.json"
        if not chunk_file.exists():
            print(f"   ❌ Missing: {chunk_file.name}")
            print(f"   AI must analyze chunk {i} first")
            sys.exit(1)
        
        chunk_analysis = load_json(chunk_file)
        violations = chunk_analysis.get('violations', [])
        merged['violations'].extend(violations)
        print(f"   ✓ Chunk {i}: {len(violations)} violations")
    
    # Add rule_name to all violations
    print(f"[2/3] Adding rule_name to violations...")
    for v in merged['violations']:
        rule_id = v.get('rule_id', 'Custom')
        if rule_id in rule_map:
            v['rule_name'] = f"{rule_id}: {rule_map[rule_id]}"
        else:
            v['rule_name'] = f"{rule_id}: {v.get('category', 'Custom Rule')}"
    print(f"   ✓ Added rule_name to {len(merged['violations'])} violations")
    
    # Save merged analysis
    print(f"[3/3] Saving merged analysis...")
    output_file = temp_dir / 'naming_analysis.json'
    save_json(merged, output_file)
    print(f"   ✓ {output_file}")
    
    print()
    print("=" * 80)
    print("PHASE 1 COMPLETE")
    print("=" * 80)
    print()
    print(f"Total violations: {len(merged['violations'])}")
    print(f"Output: {output_file}")
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
        print("Usage: python build_naming_analysis.py [analyze|merge]")
        return 1

if __name__ == '__main__':
    sys.exit(main())
