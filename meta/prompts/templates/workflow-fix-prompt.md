# Workflow Fix Prompt Template

## Common Issues and Fixes

### 1. Claude Code SDK vs npx Pattern

**Issue**: Using `const { ClaudeCode } = require('@anthropic-ai/claude-code');` in Node.js scripts
**Fix**: Use `npx @anthropic-ai/claude-code` directly

**Pattern to Replace**:
```javascript
// ❌ WRONG - Node.js SDK approach
const { ClaudeCode } = require('@anthropic-ai/claude-code');
const client = new ClaudeCode();
const result = await client.mcp.callTool('tool_name', params);
```

**Replace With**:
```bash
# ✅ CORRECT - npx CLI approach
PROMPT="Generate content using MCP tool with these parameters..."
npx @anthropic-ai/claude-code \
  -p "$PROMPT" \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "$SUBMIT_TOOL,$STATUS_TOOL,$RESULT_TOOL,Bash,Write" \
  --permission-mode "acceptEdits"
```

### 2. Task Type Classification

**Creative Tasks** (Use Claude Code SDK or npx with Read/Write/Edit tools):
- Planning and analysis
- Content writing and editing
- Task decomposition
- Creative prompt generation

**Templated Tasks** (Use npx with specific MCP tools):
- Image generation (t2i-*)
- Video generation (t2v-*, i2v-*)
- Audio generation (t2s-*, t2m-*)
- 3D model generation (i2i3d-*)
- Video processing (v2v-*)

### 3. MCP Tool Usage Pattern

For media generation, always use the three-step pattern:
1. Submit job with specific MCP tool
2. Check status (if available)
3. Get result (if available)

**Example for Image Generation**:
```bash
# Determine MCP tools based on service
case "$MODEL" in
  "t2i-google-imagen3")
    SUBMIT_TOOL="mcp__t2i-google-imagen3__imagen_t2i"
    STATUS_TOOL=""  # Not available for this service
    RESULT_TOOL=""   # Not available for this service
    ;;
  "t2i-fal-imagen4-ultra")
    SUBMIT_TOOL="mcp__t2i-fal-imagen4-ultra__imagen4_ultra_submit"
    STATUS_TOOL="mcp__t2i-fal-imagen4-ultra__imagen4_ultra_status"
    RESULT_TOOL="mcp__t2i-fal-imagen4-ultra__imagen4_ultra_result"
    ;;
esac

# Use npx with specific MCP tools
PROMPT="Generate an image using $MODEL with the following prompt:
**Prompt**: $IMAGE_PROMPT
**Aspect Ratio**: 16:9

Steps:
1. Use $SUBMIT_TOOL to start generation
2. Monitor status with $STATUS_TOOL (if available)
3. Get result with $RESULT_TOOL (if available)
4. Save the image URL to output.txt"

npx @anthropic-ai/claude-code \
  -p "$PROMPT" \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "$SUBMIT_TOOL,$STATUS_TOOL,$RESULT_TOOL,Bash,Write" \
  --permission-mode "acceptEdits"
```

### 4. Directory Structure

Always use project-based structure:
```bash
PROJECT_DIR="projects/issue-$ISSUE_NUMBER-$TIMESTAMP"
mkdir -p "$PROJECT_DIR"/{logs,metadata,temp,final,media}
```

### 5. Job Output Passing

Ensure proper job output definitions:
```yaml
outputs:
  project_dir: ${{ steps.setup.outputs.project_dir }}
  timestamp: ${{ steps.setup.outputs.timestamp }}
```

And proper needs declarations:
```yaml
needs: [setup, previous_job]
```

## Auto-Fix Instructions for Meta-Workflow

When generating workflows, follow these rules:

1. **For Planning Jobs**: Use npx with Read/Write/Edit tools
2. **For Media Generation Jobs**: Use npx with specific MCP tools (not SDK)
3. **Never create Node.js scripts** that use `require('@anthropic-ai/claude-code')`
4. **Always check minimal units** for implementation patterns
5. **Use echo-based generation** instead of HEREDOC for YAML files

## Validation Checklist

- [ ] No `const { ClaudeCode } = require()` patterns
- [ ] All media generation uses npx with MCP tools
- [ ] Project directory structure is consistent
- [ ] Job outputs and needs are properly declared
- [ ] MCP tool names match the service configuration