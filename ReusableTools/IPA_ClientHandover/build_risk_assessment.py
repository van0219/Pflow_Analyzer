#!/usr/bin/env python3
"""
Incremental Risk Assessment Builder
Analyzes risks by category to avoid context overload
"""

import json
import sys
from pathlib import Path

def load_analysis_files():
    """Load previous analysis outputs"""
    data = {}
    
    files = {
        "business": "Temp/business_analysis.json",
        "workflow": "Temp/workflow_analysis.json",
        "configuration": "Temp/configuration_analysis.json",
        "metrics": "Temp/metrics_summary.json"
    }
    
    for key, filepath in files.items():
        path = Path(filepath)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data[key] = json.load(f)
        else:
            data[key] = {}
    
    return data

def extract_risk_context(data):
    """Extract relevant context for risk analysis"""
    context = {
        "integrations": [],
        "complexity_metrics": {},
        "configuration_items": [],
        "business_requirements": []
    }
    
    # Extract integrations
    if "integrations" in data.get("business", {}):
        context["integrations"] = data["business"]["integrations"]
    
    # Extract complexity metrics
    if "metrics" in data:
        context["complexity_metrics"] = {
            "total_activities": data["metrics"].get("total_activities", 0),
            "total_processes": data["metrics"].get("total_processes", 0),
            "javascript_blocks": data["metrics"].get("total_javascript_blocks", 0),
            "sql_queries": data["metrics"].get("total_sql_queries", 0)
        }
    
    # Extract configuration items
    config = data.get("configuration", {})
    context["configuration_items"] = {
        "file_channels": len(config.get("file_channel_config", [])),
        "web_services": len(config.get("web_service_config", [])),
        "process_variables": len(config.get("process_variables", [])),
        "config_dependencies": len(config.get("configuration_dependencies", []))
    }
    
    # Extract business requirements
    if "requirements" in data.get("business", {}):
        context["business_requirements"] = data["business"]["requirements"][:5]  # Top 5
    
    return context

def create_risk_chunks(context):
    """Create risk analysis chunks by category"""
    chunks = {
        "technical_risks": {
            "focus": "Integration failures, data quality, system dependencies",
            "context": {
                "integrations": context["integrations"],
                "complexity": context["complexity_metrics"]
            }
        },
        "maintenance_risks": {
            "focus": "Configuration drift, documentation gaps, knowledge transfer",
            "context": {
                "configuration_items": context["configuration_items"]
            }
        },
        "scalability_concerns": {
            "focus": "Performance, volume handling, resource constraints",
            "context": {
                "complexity": context["complexity_metrics"]
            }
        },
        "compliance_requirements": {
            "focus": "Audit trail, authorization, segregation of duties",
            "context": {
                "business_requirements": context["business_requirements"]
            }
        },
        "data_quality_risks": {
            "focus": "Data validation, completeness, accuracy",
            "context": {
                "integrations": context["integrations"]
            }
        }
    }
    
    return chunks

def main():
    print("=" * 80)
    print("RISK ASSESSMENT BUILDER - INCREMENTAL MODE")
    print("=" * 80)
    
    # Load analysis files
    print("\n[1/3] Loading previous analysis outputs...")
    data = load_analysis_files()
    print(f"   ✓ Loaded {len([k for k, v in data.items() if v])} analysis files")
    
    # Extract risk context
    print("\n[2/3] Extracting risk context...")
    context = extract_risk_context(data)
    print(f"   ✓ Integrations: {len(context['integrations'])}")
    print(f"   ✓ Configuration items: {sum(context['configuration_items'].values())}")
    
    # Create risk chunks
    print("\n[3/3] Creating risk analysis chunks...")
    chunks = create_risk_chunks(context)
    
    for category, chunk_data in chunks.items():
        chunk_file = Path(f"Temp/risk_chunk_{category}.json")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            json.dump({
                "category": category,
                "focus": chunk_data["focus"],
                "context": chunk_data["context"]
            }, f, indent=2)
        print(f"   ✓ {category} → {chunk_file.name}")
    
    print(f"\n   Next steps:")
    print(f"   1. AI analyzes each risk_chunk_*.json file")
    print(f"   2. AI returns 3-5 key risks per category (keep output small)")
    print(f"   3. Run: python Temp/build_risk_assessment.py merge")
    
    return 0

def merge_chunks():
    """Merge analyzed chunks into final risk_assessment.json"""
    print("=" * 80)
    print("MERGING RISK ASSESSMENT CHUNKS")
    print("=" * 80)
    
    risk_assessment = {
        "technical_risks": [],
        "maintenance_risks": [],
        "scalability_concerns": [],
        "compliance_requirements": [],
        "data_quality_risks": [],
        "integration_risks": [],
        "business_continuity": [],
        "recommendations": []
    }
    
    categories = ["technical_risks", "maintenance_risks", "scalability_concerns",
                  "compliance_requirements", "data_quality_risks"]
    
    for category in categories:
        analyzed_file = Path(f"Temp/risk_chunk_{category}_analyzed.json")
        if analyzed_file.exists():
            print(f"\n   Merging {category}...")
            with open(analyzed_file, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)
            
            # Add to appropriate section
            if "risks" in chunk_data:
                risk_assessment[category] = chunk_data["risks"]
            elif "concerns" in chunk_data:
                risk_assessment[category] = chunk_data["concerns"]
            elif "requirements" in chunk_data:
                risk_assessment[category] = chunk_data["requirements"]
            
            print(f"   ✓ {category}: {len(risk_assessment[category])} items")
        else:
            print(f"   - {category} not found (skipped)")
    
    # Add generic sections if not provided
    if not risk_assessment["integration_risks"]:
        risk_assessment["integration_risks"] = [
            {
                "risk": "External system connectivity",
                "severity": "High",
                "impact": "Process failures if external systems unavailable",
                "mitigation": "Implement retry logic and error handling",
                "monitoring": "Monitor integration health and response times"
            }
        ]
    
    if not risk_assessment["business_continuity"]:
        risk_assessment["business_continuity"] = [
            {
                "scenario": "System outage",
                "impact": "Process execution delays",
                "mitigation": "Establish manual fallback procedures",
                "recovery_time": "4-8 hours"
            }
        ]
    
    if not risk_assessment["recommendations"]:
        risk_assessment["recommendations"] = [
            {
                "priority": "High",
                "recommendation": "Implement comprehensive monitoring",
                "rationale": "Proactive identification of issues",
                "effort": "Medium"
            }
        ]
    
    # Save final output
    output_file = Path("Temp/risk_assessment.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(risk_assessment, f, indent=2)
    
    print(f"\n   ✓ Written: {output_file}")
    print("\n" + "=" * 80)
    print("PHASE 4 COMPLETE")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "merge":
        sys.exit(merge_chunks())
    else:
        sys.exit(main())
