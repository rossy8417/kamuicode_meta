#!/usr/bin/env python3
"""
Generate all MCP permissions from mcp-kamuicode.json
"""
import json
import sys

def generate_mcp_permissions(config_file):
    """Generate all possible MCP permissions from the configuration file"""
    
    # Load MCP configuration
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    permissions = []
    
    # Common method suffixes based on observed patterns
    method_patterns = {
        't2i': ['submit', 'status', 'result'],  # Text-to-Image
        't2v': ['submit', 'status', 'result'],  # Text-to-Video
        'i2v': ['submit', 'status', 'result'],  # Image-to-Video
        't2m': ['generate'],                     # Text-to-Music (Google Lyria uses different pattern)
        't2s': ['submit', 'status', 'result'],  # Text-to-Speech
        'v2a': ['submit', 'status', 'result'],  # Video-to-Audio
        'v2v': ['submit', 'status', 'result'],  # Video-to-Video
        'i2i': ['submit', 'status', 'result'],  # Image-to-Image
        'i2i3d': ['submit', 'status', 'result'], # Image-to-3D
        'r2v': ['submit', 'status', 'result'],  # Reference-to-Video
        'train': ['submit', 'status', 'result'], # Training services
    }
    
    # Special cases based on observed patterns
    special_cases = {
        't2i-google-imagen3': ['imagen_t2i'],
        't2m-google-lyria': ['lyria_generate'],
        't2i-fal-imagen4-ultra': ['imagen4_ultra_submit', 'imagen4_ultra_status', 'imagen4_ultra_result'],
        't2i-fal-imagen4-fast': ['imagen4_fast_submit', 'imagen4_fast_status', 'imagen4_fast_result'],
        't2v-fal-veo3-fast': ['veo3_fast_submit', 'veo3_fast_status', 'veo3_fast_result'],
        'i2v-fal-hailuo-02-pro': ['hailuo_02_submit', 'hailuo_02_status', 'hailuo_02_result'],
        'i2v-fal-bytedance-seedance-v1-lite': ['bytedance_seedance_v1_lite_i2v_submit', 'bytedance_seedance_v1_lite_i2v_status', 'bytedance_seedance_v1_lite_i2v_result'],
        't2s-fal-minimax-speech-02-turbo': ['minimax_speech_02_turbo_submit', 'minimax_speech_02_turbo_status', 'minimax_speech_02_turbo_result'],
        't2i-fal-flux-schnell': ['flux_schnell_submit', 'flux_schnell_status', 'flux_schnell_result'],
        't2i-fal-rundiffusion-photo-flux': ['rundiffusion_photo_flux_submit', 'rundiffusion_photo_flux_status', 'rundiffusion_photo_flux_result'],
        'v2a-fal-thinksound': ['thinksound_submit', 'thinksound_status', 'thinksound_result'],
        'i2i-fal-flux-kontext-max': ['flux_kontext_submit', 'flux_kontext_status', 'flux_kontext_result'],
        'i2i-fal-flux-kontext-lora': ['flux_kontext_submit', 'flux_kontext_status', 'flux_kontext_result'],
        'i2i3d-fal-hunyuan3d-v21': ['hunyuan3d_submit', 'hunyuan3d_status', 'hunyuan3d_result'],
        'v2v-fal-luma-ray2-modify': ['luma_ray2_submit', 'luma_ray2_status', 'luma_ray2_result'],
        'r2v-fal-vidu-q1': ['vidu_q1_submit', 'vidu_q1_status', 'vidu_q1_result'],
        'train-fal-flux-kontext-trainer': ['flux_kontext_trainer_submit', 'flux_kontext_trainer_status', 'flux_kontext_trainer_result'],
        'v2v-fal-bria-background-removal': ['submit', 'status', 'result'],
        'v2v-fal-creatify-lipsync': ['lipsync_submit', 'lipsync_status', 'lipsync_result'],
        'v2v-fal-pixverse-lipsync': ['pixverse_lipsync_submit', 'pixverse_lipsync_status', 'pixverse_lipsync_result'],
        'v2v-fal-minimax-voice-design': ['submit', 'status', 'result'],
        'v2v-fal-pixverse-extend': ['pixverse_extend_submit', 'pixverse_extend_status', 'pixverse_extend_result'],
    }
    
    # Process each MCP server
    for server_name in config.get('mcpServers', {}):
        if server_name in special_cases:
            # Use known method names for special cases
            methods = special_cases[server_name]
        else:
            # Try to determine methods based on service type
            service_type = None
            for prefix in method_patterns:
                if server_name.startswith(prefix):
                    service_type = prefix
                    break
            
            if service_type:
                # Generate method names based on pattern
                # Extract the service identifier (e.g., 'thinksound' from 'v2a-fal-thinksound')
                parts = server_name.split('-')
                if len(parts) >= 3:
                    service_id = '_'.join(parts[2:])
                    methods = [f"{service_id}_{suffix}" for suffix in method_patterns[service_type]]
                else:
                    methods = method_patterns[service_type]
            else:
                # Default methods if pattern not recognized
                methods = ['submit', 'status', 'result']
        
        # Generate permission strings
        for method in methods:
            permission = f"mcp__{server_name}__{method}"
            permissions.append(permission)
    
    return permissions

def main():
    config_file = '.claude/mcp-kamuicode.json'
    
    try:
        permissions = generate_mcp_permissions(config_file)
        
        # Print as JSON array format
        print("All MCP Permissions:")
        print("=" * 50)
        for perm in sorted(permissions):
            print(f'      "{perm}",')
        
        print(f"\nTotal permissions: {len(permissions)}")
        
        # Save to file
        output_file = 'generated/mcp-all-permissions.json'
        import os
        os.makedirs('generated', exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump({
                "mcp_permissions": permissions,
                "total": len(permissions)
            }, f, indent=2)
        
        print(f"\nPermissions saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()