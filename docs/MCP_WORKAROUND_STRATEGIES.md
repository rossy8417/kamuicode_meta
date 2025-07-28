# MCP Workaround Strategies for GitHub Actions

## Current Issue
MCP services require permission approval in GitHub Actions, even with environment variables set. This blocks automated workflows.

## Workaround Strategies

### Strategy 1: Two-Phase Approach
Split the workflow into two phases:
1. **Phase 1**: Use Claude Code to generate the API call parameters
2. **Phase 2**: Use traditional scripts to make the actual MCP calls

Example:
```yaml
- name: Generate API Parameters
  uses: anthropics/claude-code-base-action@beta
  with:
    prompt: |
      Generate parameters for image generation:
      1. Read concept
      2. Create prompt for image
      3. Save parameters to api-params.json
    allowed_tools: "Read,Write,Bash"

- name: Call MCP Service Directly
  run: |
    # Use the generated parameters to call MCP service
    # This bypasses the permission issue
```

### Strategy 2: Pre-generated Scripts
Create scripts that handle MCP interactions outside of Claude Code:
1. Use Claude Code to generate specialized scripts
2. Execute scripts directly in bash steps
3. Scripts handle authentication and API calls

### Strategy 3: Hybrid Approach
- Use Claude Code for tasks that don't require MCP (concept generation, file manipulation)
- Use direct API calls or external services for MCP-dependent tasks
- Combine results in final steps

### Strategy 4: Local Development Pattern
1. Run MCP-dependent tasks locally with Claude Code
2. Commit generated assets to repository
3. Use GitHub Actions for non-MCP tasks only

### Strategy 5: Custom Action Wrapper
Create a custom GitHub Action that:
1. Wraps Claude Code functionality
2. Pre-approves MCP permissions programmatically
3. Handles the permission flow automatically

## Recommended Approach for Video Production

Given the current limitations, recommend a hybrid approach:

1. **Concept Generation** (Claude Code) ✅
   - Works without MCP permissions
   
2. **Image Generation** (Partially working)
   - Some services work (t2i-google-imagen3)
   - Generate what's possible
   
3. **Audio Generation** (Partially working)
   - Basic generation works
   - May need fallback for complex audio
   
4. **Video Generation** (Needs workaround)
   - Option A: Generate script with parameters, execute externally
   - Option B: Use alternative video generation service
   - Option C: Manual intervention step

5. **Final Package** (Claude Code) ✅
   - Works without MCP permissions

## Implementation Priority

1. First: Get basic workflow functional with available services
2. Second: Implement workarounds for critical failing services
3. Third: Document manual steps for full automation later
4. Fourth: Investigate long-term solutions with Anthropic