# MCP Secrets Setup Guide

## Overview
This guide explains how to manage MCP service URLs securely using GitHub Secrets instead of embedding them directly in the `.claude/mcp-kamuicode.json` configuration file.

## Problem Statement
- MCP service URLs contain sensitive endpoint information
- Direct embedding in configuration files poses security risks
- Need centralized, secure management of MCP endpoints

## Solution: GitHub Secrets Integration

### Method 1: Environment Variable Substitution
Use GitHub Secrets with environment variable substitution in workflows.

#### Setup Steps:

1. **Create GitHub Secrets**
   ```
   MCP_T2I_IMAGEN3_URL = https://your-imagen3-endpoint
   MCP_T2V_VEO3_URL = https://your-veo3-endpoint
   MCP_I2V_HAILUO_URL = https://your-hailuo-endpoint
   ```

2. **Modified MCP Configuration**
   ```json
   {
     "mcpServers": {
       "t2i-google-imagen3": {
         "type": "http",
         "url": "${MCP_T2I_IMAGEN3_URL}",
         "description": "Google Imagen3 image generation"
       },
       "t2v-fal-veo3-fast": {
         "type": "http", 
         "url": "${MCP_T2V_VEO3_URL}",
         "description": "Fast text-to-video generation"
       }
     }
   }
   ```

3. **Workflow Configuration**
   ```yaml
   - name: Setup MCP Configuration
     run: |
       # Substitute environment variables in MCP config
       envsubst < .claude/mcp-kamuicode.json.template > .claude/mcp-kamuicode.json
     env:
       MCP_T2I_IMAGEN3_URL: ${{ secrets.MCP_T2I_IMAGEN3_URL }}
       MCP_T2V_VEO3_URL: ${{ secrets.MCP_T2V_VEO3_URL }}
       MCP_I2V_HAILUO_URL: ${{ secrets.MCP_I2V_HAILUO_URL }}
   ```

### Method 2: Dynamic Configuration Generation
Generate the MCP configuration file dynamically in workflows.

```yaml
- name: Generate MCP Configuration
  run: |
    mkdir -p .claude
    cat > .claude/mcp-kamuicode.json << 'EOF'
    {
      "mcpServers": {
        "t2i-google-imagen3": {
          "type": "http",
          "url": "${{ secrets.MCP_T2I_IMAGEN3_URL }}",
          "description": "Google Imagen3 image generation"
        },
        "t2v-fal-veo3-fast": {
          "type": "http",
          "url": "${{ secrets.MCP_T2V_VEO3_URL }}",
          "description": "Fast text-to-video generation"
        }
      }
    }
    EOF
```

## Security Considerations

### Best Practices:
1. **Never commit URLs** to repository
2. **Use meaningful secret names** (e.g., `MCP_SERVICE_TYPE_URL`)
3. **Rotate secrets regularly** when endpoints change
4. **Limit secret access** to necessary workflows only

### Secret Naming Convention:
```
MCP_{SERVICE_TYPE}_{PROVIDER}_{MODEL}_URL

Examples:
- MCP_T2I_GOOGLE_IMAGEN3_URL
- MCP_T2V_FAL_VEO3_URL
- MCP_I2V_FAL_HAILUO_URL
```

## Implementation Examples

### Complete Workflow Example:
```yaml
name: "Secure MCP Workflow"
on: workflow_dispatch

jobs:
  generate-content:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup MCP Configuration
        run: |
          mkdir -p .claude
          cat > .claude/mcp-kamuicode.json << 'EOF'
          {
            "mcpServers": {
              "t2i-google-imagen3": {
                "type": "http",
                "url": "${{ secrets.MCP_T2I_IMAGEN3_URL }}",
                "description": "Google Imagen3 image generation"
              }
            }
          }
          EOF
          
      - name: Verify Configuration
        run: |
          echo "MCP Configuration created:"
          cat .claude/mcp-kamuicode.json
          
      - name: Use Claude Code with MCP
        uses: anthropics/claude-code-base-action@beta
        env:
          CLAUDE_CODE_CI_MODE: "true"
          CLAUDE_CODE_AUTO_APPROVE_MCP: "true"
        with:
          mcp_config: ".claude/mcp-kamuicode.json"
          allowed_tools: "mcp__t2i-google-imagen3__*"
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          prompt: "Generate an image using t2i-google-imagen3"
```

## Troubleshooting

### Common Issues:

1. **Environment Variable Not Substituted**
   - Ensure `envsubst` is available in the runner
   - Check secret names match exactly
   - Verify template file exists

2. **Invalid JSON After Substitution**
   - Test JSON syntax: `python3 -c "import json; json.load(open('.claude/mcp-kamuicode.json'))"`
   - Check for missing quotes around URL values

3. **Secret Not Found**
   - Verify secret exists in repository settings
   - Check secret name spelling and case sensitivity
   - Ensure workflow has access to the secret

## Maintenance

### Regular Tasks:
- **Monthly**: Review and update endpoint URLs
- **Quarterly**: Rotate secrets for security
- **On Change**: Update documentation when adding new services

### Monitoring:
- Track MCP service response times
- Monitor for authentication failures
- Log configuration generation success/failure