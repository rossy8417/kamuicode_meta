# Claude Code vs MCP Usage Guidelines

## 🎯 Basic Principles

**Use Claude Code Direct Execution for:**
- Text generation
- Prompt analysis  
- Task decomposition
- Workflow planning
- Code generation
- Configuration file creation
- Documentation generation

**Use MCP Servers for:**
- Image generation (Google Imagen3, Fal.ai, etc.)
- Video generation (Veo3, Hailuo, etc.)
- Audio generation (Google Lyria, etc.)
- 3D generation (Hunyuan3D, etc.)
- Complex multimodal processing

## 📋 Specific Usage Patterns

### ✅ Claude Code Direct Execution Examples

```yaml
# Task decomposition
- name: Decompose Tasks
  run: |
    claude --continue "$(cat task-decomposition-prompt.md)" \
      --output-format text

# Workflow generation
- name: Generate Workflow
  run: |
    claude --continue "Generate GitHub Actions workflow for: ${{ inputs.description }}" \
      --output-format text
```

### 🔌 MCP Usage Examples

```yaml
# Only when AI generation services are required
- name: Generate Media Content
  run: |
    claude --continue "Generate video advertisement" \
      --mcp-config .claude/mcp-kamuicode.json \
      --allowedTools "t2v-fal-veo3-fast,t2i-google-imagen3"
```

## 🔧 Dynamic MCP Configuration

Create MCP configuration dynamically based on workflow type:

```yaml
- name: Setup MCP Config (if needed)
  run: |
    if [[ "${{ inputs.workflow_type }}" =~ ^(image|video|audio)-generation$ ]]; then
      mkdir -p .claude
      cat > .claude/mcp-kamuicode.json << 'EOF'
    {
      "mcpServers": {
        "ai-generation": {
          "type": "http", 
          "url": "https://mcp-server-url",
          "description": "AI generation services"
        }
      }
    }
    EOF
    else
      echo "MCP not required for text-only workflow"
    fi
```

## 🚀 Performance Optimization

1. **Text Processing**: Claude Code direct execution (high speed)
2. **AI Generation**: MCP usage (only when necessary)
3. **Fallback**: Claude Code direct execution when MCP fails

## 🔍 Troubleshooting

### Common Issues and Solutions

**Issue**: MCP error in text generation
**Solution**: Switch to Claude Code direct execution

**Issue**: Authentication error in image generation  
**Solution**: Check and recreate MCP configuration

**Issue**: Unnecessary MCP calls
**Solution**: Make MCP usage conditional based on workflow type check

## 📊 Efficiency Comparison

| Task | Claude Code Direct | MCP | Recommended |
|------|-------------------|-----|-------------|
| Text generation | ✅ Fast | ❌ Unnecessary | Claude Code |
| Image generation | ❌ Impossible | ✅ Required | MCP |
| Task decomposition | ✅ Optimal | ❌ Overspec | Claude Code |
| Video generation | ❌ Impossible | ✅ Required | MCP |

---
🎯 **Principle**: Use Claude Code direct for simple tasks, MCP only when AI generation services are required