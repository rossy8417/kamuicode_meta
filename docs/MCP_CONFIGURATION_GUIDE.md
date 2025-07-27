# MCP Configuration Guide for Kamui Code

## Overview
This guide documents the MCP (Model Control Protocol) configuration for integrating AI generation services with Claude Code in the Kamui Code Meta system.

## MCP Configuration File Location
- **Path**: `.claude/mcp-kamuicode.json`
- **Format**: JSON
- **Purpose**: Define AI generation service endpoints accessible to Claude Code

## Configuration Structure

```json
{
  "mcpServers": {
    "service-name": {
      "type": "http",
      "url": "https://service-endpoint-url",
      "description": "Service description with capabilities"
    }
  }
}
```

## Available MCP Services (as of 2025-01-28)

### Text-to-Image (T2I)
- `t2i-google-imagen3`: Google Imagen 3 Text-to-Image Generation
- `t2i-fal-imagen4-ultra`: Fal.ai Imagen4 Ultra (High Quality) ⭐
- `t2i-fal-imagen4-fast`: Fal.ai Imagen4 Fast (Speed Optimized) ⭐
- `t2i-fal-flux-schnell`: Fal.ai Flux-1 Schnell (Fast) ⭐
- `t2i-fal-rundiffusion-photo-flux`: Fal.ai Rundiffusion Photo Flux ⭐

### Text-to-Video (T2V)
- `t2v-fal-veo3-fast`: Fal.ai Veo3 Fast Text-to-Video Generation ⭐

### Image-to-Video (I2V)
- `i2v-fal-hailuo-02-pro`: Fal.ai Hailuo-02 Pro Image-to-Video Generation ⭐
- `i2v-fal-bytedance-seedance-v1-lite`: Fal.ai ByteDance Seedance V1 Lite ⭐

### Text-to-Music (T2M)
- `t2m-google-lyria`: Google Lyria Text-to-Music Generation ⭐

### Text-to-Speech (T2S)
- `t2s-fal-minimax-speech-02-turbo`: Fal.ai MiniMax Speech-02-Turbo ⭐

### Video-to-Audio (V2A)
- `v2a-fal-thinksound`: Fal.ai ThinkSound Video-to-Audio Generation ⭐

### Video-to-Video (V2V)
- `v2v-fal-luma-ray2-modify`: Fal.ai Luma Dream Machine Ray-2 Modification ⭐
- `v2v-fal-bria-background-removal`: Fal.ai Bria Video Background Removal ⭐
- `v2v-fal-creatify-lipsync`: Fal.ai Creatify Lipsync ⭐
- `v2v-fal-pixverse-lipsync`: Fal.ai Pixverse Lipsync ⭐
- `v2v-fal-minimax-voice-design`: Fal.ai Minimax Voice Design ⭐
- `v2v-fal-pixverse-extend`: Fal.ai Pixverse Extend ⭐

### Image-to-3D (I2I3D)
- `i2i3d-fal-hunyuan3d-v21`: Fal.ai Hunyuan3D v2.1 Image-to-3D Model Generation ⭐

### Other Services
- `i2i-fal-flux-kontext-max`: Fal.ai Flux Kontext Max Image Enhancement ⭐
- `i2i-fal-flux-kontext-lora`: Fal.ai Flux Kontext LoRA Image Editing ⭐
- `train-fal-flux-kontext-trainer`: Fal.ai Flux Kontext Trainer LoRA Training ⭐
- `r2v-fal-vidu-q1`: Fal.ai Vidu Q1 Reference-to-Video Generation ⭐

## Complete Configuration Template

Save this as `.claude/mcp-kamuicode.json`:

```json
{
  "mcpServers": {
    "t2i-google-imagen3": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2i/google/imagen",
      "description": "Google Imagen 3 Text-to-Image Generation"
    },
    "t2m-google-lyria": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2m/google/lyria",
      "description": "Google Lyria Text-to-Music Generation ⭐"
    },
    "t2i-fal-imagen4-ultra": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2i/fal/imagen4/ultra",
      "description": "Fal.ai Imagen4 Ultra Text-to-Image (High Quality) ⭐"
    },
    "t2i-fal-imagen4-fast": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2i/fal/imagen4/fast",
      "description": "Fal.ai Imagen4 Fast Text-to-Image (Speed Optimized) ⭐"
    },
    "t2v-fal-veo3-fast": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2v/fal/veo3/fast",
      "description": "Fal.ai Veo3 Fast Text-to-Video Generation ⭐"
    },
    "i2v-fal-hailuo-02-pro": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/i2v/fal/minimax/hailuo-02/pro",
      "description": "Fal.ai Hailuo-02 Pro Image-to-Video Generation ⭐"
    },
    "i2i-fal-flux-kontext-max": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/i2i/fal/flux/kontext/max",
      "description": "Fal.ai Flux Kontext Max Image-to-Image Enhancement ⭐"
    },
    "i2i3d-fal-hunyuan3d-v21": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/i2i3d/fal/hunyuan/3d-v21",
      "description": "Fal.ai Hunyuan3D v2.1 Image-to-3D Model Generation ⭐"
    },
    "v2a-fal-thinksound": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/v2a/fal/thinksound/audio/standard",
      "description": "Fal.ai ThinkSound Video-to-Audio Generation ⭐"
    },
    "v2v-fal-luma-ray2-modify": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/v2v/fal/luma/dream-machine/ray-2/modify",
      "description": "Fal.ai Luma Dream Machine Ray-2 Video-to-Video Modification ⭐"
    },
    "r2v-fal-vidu-q1": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/r2v/fal/vidu/q1",
      "description": "Fal.ai Vidu Q1 Reference-to-Video Generation ⭐"
    },
    "t2i-fal-flux-schnell": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2i/fal/flux/schnell",
      "description": "Fal.ai Flux-1 Schnell Text-to-Image (Fast) ⭐"
    },
    "t2i-fal-rundiffusion-photo-flux": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2i/fal/rundiffusion/photo-flux",
      "description": "Fal.ai Rundiffusion Photo Flux Text-to-Image ⭐"
    },
    "t2s-fal-minimax-speech-02-turbo": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-024457-8bc6d0d5-820994673238.us-central1.run.app/t2s/fal/minimax/speech-02-turbo",
      "description": "Fal.ai MiniMax Speech-02-Turbo Text-to-Speech Generation ⭐"
    },
    "i2i-fal-flux-kontext-lora": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/i2i/fal/flux/kontext",
      "description": "Fal.ai Flux Kontext LoRA Image-to-Image Editing with LoRA Support ⭐"
    },
    "train-fal-flux-kontext-trainer": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/train/fal/flux/kontext",
      "description": "Fal.ai Flux Kontext Trainer LoRA Training ⭐"
    },
    "v2v-fal-bria-background-removal": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/video/fal/bria/background-removal",
      "description": "Fal.ai Bria Video Background Removal - Remove video backgrounds with transparency ⭐"
    },
    "v2v-fal-creatify-lipsync": {
      "type": "http",
      "url": "https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/v2v/fal/creatify/lipsync",
      "description": "Fal.ai Creatify Lipsync - Realistic lipsync video optimized for speed, quality, and consistency ⭐"
    },
    "v2v-fal-pixverse-lipsync": {
      "type": "http",
      "url": "https://mcp-pixverse-lipsync-20250723-131006-ebd10b2c-820994673238.us-central1.run.app/v2v/fal/pixverse/lipsync",
      "description": "Fal.ai Pixverse Lipsync - High-quality video-to-video lipsync generation ⭐"
    },
    "v2v-fal-minimax-voice-design": {
      "type": "http",
      "url": "https://mcp-fal-minimax-voice-design-20250725-133906-d3c2-zl3xx5lsaq-uc.a.run.app/v2v/fal/minimax/voice-design",
      "description": "Fal.ai Minimax Voice Design - Custom voice generation and design ⭐"
    },
    "v2v-fal-pixverse-extend": {
      "type": "http",
      "url": "https://mcp-fal-pixverse-extend-20250726-231026-824376d5-820994673238.us-central1.run.app/v2v/fal/pixverse/extend",
      "description": "Fal.ai Pixverse Extend - Video extension and enhancement ⭐"
    },
    "i2v-fal-bytedance-seedance-v1-lite": {
      "type": "http",
      "url": "https://mcp-fal-bytedance-seedance-v1-lite-i2v-20250727-6-zl3xx5lsaq-uc.a.run.app/i2v/fal/bytedance/seedance-v1-lite",
      "description": "Fal.ai ByteDance Seedance V1 Lite Image-to-Video Generation ⭐"
    }
  }
}
```

## Usage in GitHub Actions

When using MCP services in GitHub Actions workflows:

1. **Configuration Path**: Always use `.claude/mcp-kamuicode.json`
2. **Environment Variables**: Set these for CI/CD environments:
   ```yaml
   env:
     CLAUDE_CODE_CI_MODE: "true"
     CLAUDE_CODE_AUTO_APPROVE_MCP: "true"
   ```
3. **Allowed Tools**: Specify MCP tools with pattern: `mcp__service-name__*`

## Important Notes

1. **Service Names**: Must match exactly as defined in the configuration
2. **URLs**: Cloud Run endpoints may change - always verify with latest configuration
3. **Permissions**: In CI/CD, MCP permissions need special handling
4. **CLAUDE.md Reference**: This configuration should be referenced in CLAUDE.md for system consistency

## Troubleshooting

### Common Issues:
1. **Permission Denied**: Add environment variables for auto-approval
2. **Service Not Found**: Verify service name matches configuration exactly
3. **URL Changes**: Update endpoints when services are redeployed

### Validation:
```bash
# Validate JSON syntax
python3 -c "import json; json.load(open('.claude/mcp-kamuicode.json'))"
```

## Maintenance

- **Regular Updates**: Check for new services monthly
- **Endpoint Verification**: Test endpoints when workflows fail
- **Documentation**: Update this guide when adding new services