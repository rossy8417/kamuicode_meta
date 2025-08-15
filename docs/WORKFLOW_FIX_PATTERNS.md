# Workflow Fix Patterns for Meta-Workflow v12

This document provides comprehensive patterns for fixing common workflow errors detected during validation.

## 🚨 Critical Security Fixes

### 1. Exposed OAuth Token
**Detection Pattern:**
```bash
grep -q 'CLAUDE_CODE_OAUTH_TOKEN:\s*sk-ant-'
```

**Fix Pattern:**
```yaml
# ❌ WRONG - Exposed token
CLAUDE_CODE_OAUTH_TOKEN: sk-ant-oat01-xxxxx

# ✅ CORRECT - Using GitHub Secrets
CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

### 2. Hardcoded API Keys
**Detection Pattern:**
```bash
grep -E '(api[_-]key|token|bearer|secret)\s*:\s*[A-Za-z0-9_-]{20,}'
```

**Fix Pattern:**
```yaml
# ❌ WRONG
OPENAI_API_KEY: sk-proj-abcdef123456

# ✅ CORRECT
OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## 📝 YAML Structure Fixes

### 3. HEREDOC with GitHub Actions Variables
**Detection Pattern:**
```bash
awk '/cat.*<<.*EOF/,/^EOF$/' file | grep -q '\${{'
```

**Fix Pattern:**
```bash
# ❌ WRONG - HEREDOC with ${{ }} causes YAML parsing errors
cat > output.json << EOF
{
  "title": "${{ github.event.inputs.title }}",
  "issue": "${{ github.event.issue.number }}"
}
EOF

# ✅ CORRECT - Use echo commands
echo '{' > output.json
echo "  \"title\": \"${{ github.event.inputs.title }}\"," >> output.json
echo "  \"issue\": \"${{ github.event.issue.number }}\"" >> output.json
echo '}' >> output.json

# ✅ ALTERNATIVE - Use printf
printf '{\n  "title": "%s",\n  "issue": "%s"\n}\n' \
  "${{ github.event.inputs.title }}" \
  "${{ github.event.issue.number }}" > output.json
```

### 4. Local Uses References
**Detection Pattern:**
```bash
grep -q 'uses:.*\./'
```

**Fix Pattern:**
```yaml
# ❌ WRONG - Local file reference
- uses: ./minimal-units/image-generation.yml

# ✅ CORRECT - Inline the implementation
- name: Generate Image
  run: |
    # Implementation from minimal-units/image-generation.yml
    npx @anthropic-ai/claude-code \
      --mcp-config ".claude/mcp-kamuicode.json" \
      --allowedTools "mcp__t2i-kamui-imagen3__imagen_t2i,Write" \
      -p "Generate image: $PROMPT"
```

## 🗂️ Path Management Fixes

### 5. Hardcoded Absolute Paths
**Detection Pattern:**
```bash
grep '/home/runner/work/' | grep -v '\${{'
```

**Fix Pattern:**
```bash
# ❌ WRONG - Hardcoded path
PROJECT_DIR="/home/runner/work/kamuicode_meta/kamuicode_meta/projects"

# ✅ CORRECT - Dynamic workspace path
PROJECT_DIR="${{ github.workspace }}/projects"

# ✅ ALTERNATIVE - Using needs output
PROJECT_DIR="${{ needs.setup.outputs.project_dir }}"
```

### 6. Matrix Reference in Job Outputs
**Detection Pattern:**
```bash
grep 'outputs:.*matrix\.'
```

**Fix Pattern:**
```yaml
# ❌ WRONG - Matrix variable in output name
outputs:
  scene_${{ matrix.scene }}_ready: "true"

# ✅ CORRECT - Fixed output name with matrix value in content
outputs:
  scene_ready: "scene_${{ matrix.scene }}_completed"
  scene_data: ${{ steps.process.outputs.result }}
```

## 🔄 Data Persistence Fixes

### 7. MCP Tool Output Handling
**Pattern:** Ensure MCP tool outputs are explicitly saved

```bash
# ❌ WRONG - MCP output not saved
npx @anthropic-ai/claude-code \
  --allowedTools "mcp__t2i-kamui-imagen3__imagen_t2i" \
  -p "Generate image"

# ✅ CORRECT - Explicit save instructions
npx @anthropic-ai/claude-code \
  --allowedTools "mcp__t2i-kamui-imagen3__imagen_t2i,Write,Bash" \
  -p "Generate image and:
      1. Save image to ${PROJECT_DIR}/images/output.png
      2. Save URL to ${PROJECT_DIR}/images/output-url.txt
      3. Execute: ls -la ${PROJECT_DIR}/images/"
```

## 🎯 Advanced Fix Patterns

### 8. Complex JSON Generation
**Pattern:** Avoid complex string interpolation in JSON

```bash
# ❌ WRONG - Complex interpolation
echo "{\"scenes\": [$(for i in {1..5}; do echo "\"scene_$i\""; done | tr '\n' ',')]}" > data.json

# ✅ CORRECT - Step-by-step construction
echo '{"scenes": [' > data.json
for i in {1..5}; do
  [ $i -gt 1 ] && echo -n ',' >> data.json
  echo -n "\"scene_$i\"" >> data.json
done
echo ']}' >> data.json
```

### 9. Environment Variable Escaping
**Pattern:** Proper escaping in different contexts

```bash
# In YAML context
env:
  MY_VAR: ${{ secrets.MY_SECRET }}  # GitHub Actions variable

# In bash context within YAML
run: |
  echo "MY_VAR=\${{ secrets.MY_SECRET }}" >> $GITHUB_ENV  # Escaped for bash
  
# In string context
run: |
  MESSAGE='Value is ${{ github.event.inputs.value }}'  # Single quotes preserve literal
  MESSAGE="Value is \$VALUE"  # Double quotes need escaping for variables
```

### 10. Artifact Path Resolution
**Pattern:** Consistent artifact handling

```bash
# ❌ WRONG - Assuming artifact location
VIDEO_PATH="artifacts/video.mp4"

# ✅ CORRECT - Flexible path resolution
VIDEO_PATH=$(find artifacts -name "*.mp4" -type f | head -1)
[ -z "$VIDEO_PATH" ] && VIDEO_PATH=$(find . -name "video*.mp4" -type f | head -1)
[ -z "$VIDEO_PATH" ] && echo "ERROR: Video not found" && exit 1
```

## 🔧 Fix Validation Checklist

After applying fixes, validate:

1. **YAML Syntax**: `python3 -c "import yaml; yaml.safe_load(open('workflow.yml'))"`
2. **No Exposed Secrets**: `! grep -E 'sk-ant-|api[_-]key:\s*[A-Za-z0-9]{20,}' workflow.yml`
3. **No Local Uses**: `! grep 'uses:.*\./' workflow.yml`
4. **No Hardcoded Paths**: `! grep '/home/runner/work/' workflow.yml | grep -v '\${{'`
5. **No HEREDOC with Variables**: `! awk '/cat.*<<.*EOF/,/^EOF$/' workflow.yml | grep '\${{'`

## 📚 References

- [GitHub Actions Context](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [YAML Specification](https://yaml.org/spec/1.2/spec.html)
- [Claude Code Data Persistence Guide](./CLAUDE_CODE_DATA_PERSISTENCE_GUIDE.md)
- [YAML Construction Guidelines](./YAML_CONSTRUCTION_GUIDELINES.md)