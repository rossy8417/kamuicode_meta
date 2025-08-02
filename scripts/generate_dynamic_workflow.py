#!/usr/bin/env python3
import json
import sys
import os
import re
from datetime import datetime

def generate_workflow_from_requirements(requirements, capabilities, complexity):
    """Generate dynamic workflow based on analyzed requirements"""
    
    # Select minimal units based on capabilities
    unit_mapping = {
        'web-search': 'minimal-units/planning/web-search.yml',
        'data-analysis': 'minimal-units/planning/data-analysis.yml', 
        'news-planning': 'minimal-units/planning/news-planning.yml',
        'image-generation': 'minimal-units/media/image/t2i-imagen3.yml',
        'video-generation': 'minimal-units/media/video/t2v-veo3.yml',
        'audio-generation': 'minimal-units/media/audio/bgm-generate-mcp.yml',
        'text-to-speech': 'minimal-units/media/audio/t2s-minimax-turbo-mcp.yml',
        'video-editing': 'minimal-units/postprod/video-concat.yml',
        'banner-design': 'minimal-units/media/banner/banner-text.yml'
    }
    
    selected_units = []
    seen_capabilities = set()
    
    for cap in capabilities.split(','):
        cap = cap.strip()
        if cap and cap not in seen_capabilities:  # Avoid duplicates
            seen_capabilities.add(cap)
            if cap in unit_mapping:
                selected_units.append({
                    'capability': cap,
                    'unit_path': unit_mapping[cap],
                    'estimated_time': '3-5 minutes'
                })
    
    # Generate workflow structure
    workflow = {
        'metadata': {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'complexity': complexity,
            'total_units': len(selected_units),
            'capabilities_detected': list(seen_capabilities)
        },
        'minimal_units': selected_units,
        'execution_pattern': 'sequential' if complexity == 'simple' else 'mixed_parallel'
    }
    
    return workflow

if __name__ == "__main__":
    # Read input parameters
    requirements = os.environ.get('REQUIREMENTS', '')
    capabilities = os.environ.get('CAPABILITIES', '')
    complexity = os.environ.get('COMPLEXITY', 'medium')
    
    print(f"Debug - Capabilities: {capabilities}")
    print(f"Debug - Complexity: {complexity}")
    
    # Generate workflow
    workflow = generate_workflow_from_requirements(requirements, capabilities, complexity)
    
    # Create directory and save result
    os.makedirs('../metadata', exist_ok=True)
    with open('../metadata/dynamic_workflow.json', 'w') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dynamic workflow generated with {len(workflow['minimal_units'])} units")
    print(f"📁 Saved to: ../metadata/dynamic_workflow.json")