# MCP Configuration Guide for GitHub Actions with Claude Code

## Overview
This guide documents how to configure MCP (Model Control Protocol) services for use with Claude Code in GitHub Actions workflows, using the `.claude/mcp-kamuicode.json` configuration file approach (not direct URL).

## Important: Configuration Method
- **Method**: JSON configuration file (`.claude/mcp-kamuicode.json`)
- **NOT**: Direct URL configuration in workflows
- **Purpose**: Centralized MCP service management for GitHub Actions

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

## Available MCP Service Types (44+ Services Total)

### AI Generation Services (24 Services)

#### Text-to-Image (T2I) Services
Services that generate images from text descriptions:
- `t2i-google-imagen3`: Google's image generation model
- `t2i-fal-imagen4-ultra`: High-quality image generation ⭐
- `t2i-fal-imagen4-fast`: Speed-optimized image generation ⭐
- `t2i-fal-flux-schnell`: Fast image generation ⭐
- `t2i-fal-rundiffusion-photo-flux`: Photorealistic image generation ⭐

### Text-to-Video (T2V) Services
Services that create videos from text prompts:
- `t2v-fal-veo3-fast`: Fast text-to-video generation ⭐
- `t2v-fal-wan-v2-2-a14b-t2v`: High-quality video with visual quality and motion diversity ⭐

### Image-to-Video (I2V) Services
Services that animate static images into videos:
- `i2v-fal-hailuo-02-pro`: Professional image-to-video animation ⭐
- `i2v-fal-bytedance-seedance-v1-lite`: Lightweight image animation ⭐

### Text-to-Music (T2M) Services
Services that compose music from text descriptions:
- `t2m-google-lyria`: Google's music generation model ⭐

### Text-to-Speech (T2S) Services
Services that convert text to spoken audio:
- `t2s-fal-minimax-speech-02-turbo`: Fast text-to-speech generation ⭐

### Video-to-Audio (V2A) Services
Services that generate audio/sound effects for videos:
- `v2a-fal-thinksound`: Video-to-audio generation ⭐

### Video-to-Video (V2V) Services
Services that modify or enhance existing videos:
- `v2v-fal-luma-ray2-modify`: Video modification and enhancement ⭐
- `v2v-fal-bria-background-removal`: Remove video backgrounds ⭐
- `v2v-fal-creatify-lipsync`: Realistic lip synchronization ⭐
- `v2v-fal-pixverse-lipsync`: High-quality lip sync generation ⭐
- `v2v-fal-minimax-voice-design`: Custom voice generation ⭐
- `v2v-fal-pixverse-extend`: Video extension and enhancement ⭐
- `v2v-fal-topaz-upscale-video`: Advanced video upscaling, frame interpolation, and enhancement ⭐

### Image-to-Image (I2I) Services
Services for image editing and enhancement:
- `i2i-fal-flux-kontext-max`: Advanced image enhancement ⭐
- `i2i-fal-flux-kontext-lora`: Image editing with LoRA support ⭐

### Image-to-3D (I2I3D) Services
Services that convert 2D images to 3D models:
- `i2i3d-fal-hunyuan3d-v21`: Image-to-3D model generation ⭐

### Training Services
Services for model training:
- `train-fal-flux-kontext-trainer`: LoRA model training ⭐

### Reference-to-Video (R2V) Services
Services that generate videos from reference materials:
- `r2v-fal-vidu-q1`: Reference-based video generation ⭐

### External API Services (20+ Services)

#### Social Media & Communication Services
External services for social media and communication:
- `external-openai-gpt`: OpenAI GPT-4/GPT-3.5 API for text generation and analysis
- `external-openai-image`: OpenAI Image Generation (gpt-image-1) API
- `external-openai-tts`: OpenAI Text-to-Speech API
- `external-elevenlabs-tts`: ElevenLabs text-to-speech API
- `external-youtube-api`: YouTube Data API v3 for video management and statistics
- `external-twitter-api`: Twitter/X API v2 for social media interaction
- `external-slack-api`: Slack Web API for team communication
- `external-discord-webhook`: Discord webhook integration
- `external-telegram-api`: Telegram Bot API for messaging
- `external-sendgrid-api`: SendGrid email delivery service

#### Data & Analytics Services
External services for data processing and analytics:
- `external-newsapi`: NewsAPI for global news aggregation
- `external-openweathermap`: OpenWeatherMap API for weather data
- `external-google-sheets`: Google Sheets API for spreadsheet operations
- `external-finnhub-api`: Finnhub stock market data API
- `external-arxiv-api`: arXiv API for scientific paper search

#### Development & Productivity Services
External services for development and productivity:
- `external-github-api`: GitHub API for repository and issue management
- `external-notion-api`: Notion API for knowledge management
- `external-reddit-api`: Reddit API for community content
- `external-huggingface-api`: Hugging Face Inference API for ML models
- `external-translate-api`: Translation API services

## MCP Configuration File Setup

The MCP configuration should be stored in `.claude/mcp-kamuicode.json` in your repository. This file contains the service definitions and endpoints for all available MCP services.

### File Structure Example:
```json
{
  "mcpServers": {
    "service-name": {
      "type": "http",
      "url": "service-endpoint-url",
      "description": "Service description"
    },
    // For external APIs with authentication:
    "external-api-name": {
      "type": "http",
      "url": "https://api.example.com/endpoint",
      "description": "External API service description",
      "env": {
        "API_KEY": "{{API_KEY_ENV_VAR}}"
      }
    },
    // ... more services
  }
}
```

**Important**: 
- Never commit URLs directly in workflows or documentation
- Always reference services through the `.claude/mcp-kamuicode.json` file
- Keep the JSON file in your repository but ensure URLs are properly secured

## GitHub Actions Workflow Configuration

### Step 1: Create MCP Configuration File
Place the configuration at `.claude/mcp-kamuicode.json` in your repository.

### Step 2: Workflow Setup
```yaml
name: "Video Content Creation Production"
on:
  workflow_dispatch:
    inputs:
      video_concept:
        description: 'Video concept'
        required: true
        type: string

jobs:
  generate-with-mcp:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Verify MCP config exists
        run: |
          if [ -f ".claude/mcp-kamuicode.json" ]; then
            echo "✅ MCP config found"
          else
            echo "❌ MCP config not found"
            exit 1
          fi
          
      - name: Generate with Claude Code and MCP
        uses: anthropics/claude-code-base-action@beta
        env:
          CLAUDE_CODE_CI_MODE: "true"
          CLAUDE_CODE_AUTO_APPROVE_MCP: "true"
          # External API keys (if using external services)
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
          # ... other API keys as needed
        with:
          prompt: |
            Use t2i-google-imagen3 to generate an image.
            Save the result with full URL.
          system_prompt: |
            You are Claude Code in CI/CD. All MCP tools are pre-authorized.
          mcp_config: ".claude/mcp-kamuicode.json"  # ← Critical: This references the JSON file
          allowed_tools: "View,mcp__t2i-google-imagen3__*,Bash,Write"
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

### Key Configuration Elements:

1. **mcp_config Parameter**: 
   - MUST point to `.claude/mcp-kamuicode.json`
   - This tells Claude Code to use the JSON configuration file
   - NOT a direct URL to MCP service

2. **Environment Variables**:
   ```yaml
   env:
     CLAUDE_CODE_CI_MODE: "true"
     CLAUDE_CODE_AUTO_APPROVE_MCP: "true"
   ```
   These are critical for GitHub Actions to bypass permission prompts.

3. **Allowed Tools Pattern**:
   - Format: `mcp__service-name__*`
   - Example: `mcp__t2i-google-imagen3__*`
   - The service name MUST match exactly what's in the JSON file

4. **System Prompt**:
   - Include: "All MCP tools are pre-authorized"
   - This helps Claude Code understand it's in a CI/CD environment

## Important Notes

1. **Service Names**: Must match exactly as defined in the configuration
2. **URLs**: Cloud Run endpoints may change - always verify with latest configuration
3. **Permissions**: In CI/CD, MCP permissions need special handling
4. **CLAUDE.md Reference**: This configuration should be referenced in CLAUDE.md for system consistency
5. **External APIs**: Require environment variables for API keys (use GitHub Secrets)
6. **Environment Variables**: Use {{VARIABLE_NAME}} placeholder format in JSON configuration

## Real Example from Video Production Workflow

```yaml
- name: Generate images with MCP
  uses: anthropics/claude-code-base-action@beta
  env:
    CLAUDE_CODE_CI_MODE: "true"
    CLAUDE_CODE_AUTO_APPROVE_MCP: "true"
  with:
    prompt: |
      1. Read concept from generated/concept/plan.json
      2. Generate 5 key scene images using t2i-google-imagen3
      3. Style: cinematic
      4. Download images using FULL URLs
      5. Save results to generated/images/results.json
    system_prompt: |
      You are Claude Code in CI/CD. All MCP tools are pre-authorized.
      Use FULL URLs from MCP responses!
    mcp_config: ".claude/mcp-kamuicode.json"
    allowed_tools: "View,mcp__t2i-google-imagen3__*,Bash,Write,Read"
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    max_turns: "20"
```

## Troubleshooting

### Common Issues:

1. **MCP Permission Denied Error**:
   ```
   "Claude requested permissions to use mcp__service__method, but you haven't granted it yet."
   ```
   **Solution**: Ensure environment variables are set:
   ```yaml
   env:
     CLAUDE_CODE_CI_MODE: "true"
     CLAUDE_CODE_AUTO_APPROVE_MCP: "true"
   ```

2. **Service Not Found**:
   - Verify service name in `allowed_tools` matches exactly the name in `.claude/mcp-kamuicode.json`
   - Check JSON file syntax is valid

3. **URL Endpoint Issues**:
   - If MCP calls fail, the URL in the JSON might be outdated
   - Test the endpoint manually if possible
   - Update the URL in `.claude/mcp-kamuicode.json` if needed

### Validation Steps:

1. **Validate JSON syntax**:
   ```bash
   python3 -c "import json; json.load(open('.claude/mcp-kamuicode.json'))"
   ```

2. **Check MCP config is being loaded**:
   Add this debug step in your workflow:
   ```yaml
   - name: Debug MCP config
     run: |
       echo "MCP Config contents:"
       cat .claude/mcp-kamuicode.json
   ```

3. **Verify service names match**:
   The service name in `allowed_tools` must exactly match the key in the JSON:
   - JSON: `"t2i-google-imagen3": { ... }`
   - Workflow: `allowed_tools: "mcp__t2i-google-imagen3__*"`

## External API Configuration

### Required GitHub Secrets
When using external APIs, add these secrets to your repository:
- `OPENAI_API_KEY`: OpenAI API key for GPT, image generation, TTS
- `ELEVENLABS_API_KEY`: ElevenLabs API key for voice synthesis
- `YOUTUBE_API_KEY`: YouTube Data API v3 key
- `TWITTER_API_KEY`: Twitter/X API v2 bearer token
- `SLACK_BOT_TOKEN`: Slack bot user OAuth token
- `DISCORD_WEBHOOK_URL`: Discord webhook URL
- `TELEGRAM_BOT_TOKEN`: Telegram bot token
- `SENDGRID_API_KEY`: SendGrid API key
- `NEWSAPI_KEY`: NewsAPI.org API key
- `OPENWEATHERMAP_API_KEY`: OpenWeatherMap API key
- `GOOGLE_SHEETS_CREDENTIALS`: Google service account JSON (base64 encoded)
- `FINNHUB_API_KEY`: Finnhub stock API key
- `GITHUB_TOKEN`: GitHub personal access token (if different from default)
- `NOTION_API_KEY`: Notion integration token
- `REDDIT_CLIENT_ID`: Reddit app client ID
- `REDDIT_CLIENT_SECRET`: Reddit app client secret
- `HUGGINGFACE_API_KEY`: Hugging Face API token

### Using External APIs in Workflows
```yaml
- name: Use External APIs
  uses: anthropics/claude-code-base-action@beta
  env:
    CLAUDE_CODE_CI_MODE: "true"
    CLAUDE_CODE_AUTO_APPROVE_MCP: "true"
    # Pass through required API keys
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
  with:
    prompt: |
      1. Use external-newsapi to fetch latest AI news
      2. Use external-openai-gpt to summarize the news
      3. Save results to generated/news-summary.json
    mcp_config: ".claude/mcp-kamuicode.json"
    allowed_tools: "View,mcp__external-newsapi__*,mcp__external-openai-gpt__*,Bash,Write"
```

## Maintenance

- **Regular Updates**: Check for new services monthly
- **Endpoint Verification**: Test endpoints when workflows fail
- **Documentation**: Update this guide when adding new services
- **API Key Rotation**: Regularly rotate external API keys for security