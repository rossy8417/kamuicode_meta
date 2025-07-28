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

## Test Results Summary

### Environment Variables Tested
- `CLAUDE_CODE_CI_MODE=true` + `CLAUDE_CODE_AUTO_APPROVE_MCP=true` - ❌ Still requires permission
- Alternative env vars (CI, HEADLESS, NON_INTERACTIVE) - ❌ No effect
- Settings parameter with auto-approval flags - ❌ No effect
- `.claude/settings.json` with various flags - ❌ No effect

### Current Findings
1. MCP permissions in GitHub Actions require manual approval
2. No current environment variable or setting bypasses this requirement
3. Some MCP services work (image generation) while others don't (video generation)
4. This appears to be a limitation of the current Claude Code GitHub Action

## Recommended Solution

### Immediate Workaround: Hybrid Approach
1. Use Claude Code for non-MCP tasks (concept, planning, file operations)
2. For MCP-dependent tasks, use one of these approaches:
   - Generate parameters with Claude Code, execute with custom scripts
   - Use alternative services that don't require MCP
   - Create manual intervention points in the workflow

### Example Implementation
```yaml
# Phase 1: Generate parameters
- name: Generate Video Parameters
  uses: anthropics/claude-code-base-action@beta
  with:
    prompt: |
      Create video generation parameters:
      1. Read image URL from results
      2. Create video prompt
      3. Save to video-params.json
    allowed_tools: "Read,Write,Bash"

# Phase 2: Direct API call (outside Claude Code)
- name: Generate Video via API
  run: |
    # Custom script that reads params and calls MCP endpoint
    python scripts/generate_video.py --params video-params.json
```

## Next Steps
1. ✅ Document current limitations
2. ✅ Create workaround strategies
3. 🔄 Implement hybrid workflow for video production
4. 📝 Report issue to Anthropic for future improvements
5. 🔧 Create helper scripts for common MCP operations