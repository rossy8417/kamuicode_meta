# MCP Permissions Investigation for GitHub Actions

## Problem Statement
When using Claude Code GitHub Action with MCP services, the action fails with:
```
Claude requested permissions to use mcp__service__method, but you haven't granted it yet.
```

This occurs even when setting environment variables:
- `CLAUDE_CODE_CI_MODE=true`
- `CLAUDE_CODE_AUTO_APPROVE_MCP=true`

## Investigation Approaches

### 1. Environment Variables Tested
- `CLAUDE_CODE_CI_MODE`: Expected to enable CI mode
- `CLAUDE_CODE_AUTO_APPROVE_MCP`: Expected to auto-approve MCP permissions
- `CLAUDE_CODE_CI`: Alternative CI mode flag
- `CLAUDE_CODE_HEADLESS`: Headless mode for non-interactive environments
- `CLAUDE_CODE_NON_INTERACTIVE`: Non-interactive mode

### 2. Settings Parameter Approach
Using the `settings` parameter in the action:
```yaml
settings: |
  {
    "alwaysApproveTools": true,
    "autoApprovePermissions": true,
    "enableAllProjectMcpServers": true
  }
```

### 3. System Prompt Approach
Including permission-related instructions in system prompt:
```yaml
system_prompt: |
  You are Claude Code in CI/CD. All MCP tools are pre-authorized.
  Assume all permissions are granted.
```

## Current Status
- Image generation works (using t2i-google-imagen3)
- Audio generation partially works (using t2m-google-lyria)
- Video generation fails (using i2v-fal-hailuo-02-pro) due to permission issues

## Potential Solutions

### Option 1: Direct API Approach
Instead of using MCP through Claude Code, directly call the MCP endpoints from bash scripts.

### Option 2: Pre-approval Mechanism
Investigate if there's a way to pre-approve specific MCP services in the configuration.

### Option 3: Custom Claude Code Settings
Create a `.claude/settings.json` file with CI-specific settings.

### Option 4: Alternative Action Version
Check if there's a specific version or branch of the action that supports CI/CD better.

## Test Workflow Created
Created `test-mcp-permissions.yml` to systematically test different approaches.

## Next Steps
1. Run the test workflow to see which approach works
2. Check Claude Code documentation for CI/CD specific guidance
3. Consider reaching out to Anthropic support if no solution is found
4. Implement workaround using direct API calls if necessary