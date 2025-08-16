# Common Workflow Errors and Prevention Guide

## Overview
This document catalogs frequently encountered errors in GitHub Actions workflow generation and provides prevention strategies.

## Critical Error Categories

### 1. YAML Syntax Errors

#### HEREDOC Issues
**Error**: "could not find expected ':'" in YAML parsing
**Cause**: Using HEREDOC (`cat << EOF`) within GitHub Actions YAML
**Prevention**:
```yaml
# ❌ NEVER USE HEREDOC
- name: Generate YAML
  run: |
    cat > workflow.yml << 'EOF'
    name: Workflow
    on: push
    EOF

# ✅ ALWAYS USE ECHO
- name: Generate YAML
  run: |
    echo 'name: Workflow' > workflow.yml
    echo 'on: push' >> workflow.yml
```

#### Indentation Errors
**Error**: "mapping values are not allowed here"
**Prevention**:
- Use 2-space indentation consistently
- Validate with: `python3 -c "import yaml; yaml.safe_load(open('file.yml'))"`

### 2. Bash Syntax Errors

#### Arithmetic Operations
**Error**: "bad substitution"
**Cause**: Incorrect bash arithmetic syntax
**Prevention**:
```bash
# ❌ WRONG
RESULT="${VAR - 8}"
RESULT=${VAR - 8}

# ✅ CORRECT
RESULT=$((VAR - 8))
```

#### Quote Character Types
**Error**: Unexpected token or command not found
**Cause**: Using full-width quotes (Japanese input)
**Prevention**:
```bash
# ❌ WRONG (full-width quotes)
echo "これはテストです"
variable="value"

# ✅ CORRECT (half-width quotes)
echo "これはテストです"
variable="value"
```

#### Variable Expansion in HEREDOC
**Error**: GitHub context variables not expanded
**Prevention**:
```bash
# ❌ PROBLEMATIC
cat > file.json << EOF
{"issue": ${{ github.event.issue.number }}}
EOF

# ✅ SAFE
ISSUE_NUMBER="${{ github.event.issue.number }}"
echo "{\"issue\": $ISSUE_NUMBER}" > file.json
```

### 3. Security Issues

#### Exposed Credentials
**Error**: Secrets visible in logs
**Prevention**:
```yaml
# ❌ NEVER HARDCODE
env:
  OAUTH_TOKEN: ghp_xxxxxxxxxxxx
  API_KEY: sk-xxxxxxxxxxxx

# ✅ ALWAYS USE SECRETS
env:
  OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### 4. Workflow Trigger Issues

#### Push Event Failures
**Error**: Workflow fails when triggered by push
**Prevention**:
```yaml
# ❌ INCOMPLETE
on:
  workflow_dispatch:

# ✅ COMPLETE
on:
  workflow_dispatch:
    inputs:
      # inputs with defaults
  push:
    paths-ignore:
      - '.github/workflows/**'
      - 'docs/**'
```

#### Missing Input Defaults
**Error**: Required input not provided
**Prevention**:
```yaml
# ✅ ALWAYS PROVIDE DEFAULTS
inputs:
  topic:
    description: "Topic for content"
    required: true
    default: "Technology News"  # Always include default
```

### 5. Job Dependencies

#### Artifact Sharing
**Error**: File not found in dependent job
**Prevention**:
```yaml
# Job A - Upload
- name: Upload Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: shared-files
    path: ./output/

# Job B - Download
- name: Download Artifacts
  uses: actions/download-artifact@v4
  with:
    name: shared-files
    path: ./input/
```

#### Matrix Strategy
**Error**: Empty matrix skips jobs
**Prevention**:
```yaml
strategy:
  matrix:
    item: ${{ fromJson(needs.setup.outputs.items || '["default"]') }}
  fail-fast: false  # Always include
```

### 6. Claude Code SDK Issues

#### MCP Tool Invocation
**Error**: MCP tools not available
**Prevention**:
```bash
# ✅ COMPLETE INVOCATION
npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2i-*,Write,Bash" \
  --permission-mode "acceptEdits" \
  --max-turns 40 \
  -p "$PROMPT"
```

#### File Persistence
**Error**: Generated files not saved locally
**Prevention**:
```bash
PROMPT="Generate image and:
1. Use MCP tool for generation
2. Save to ${SAVE_PATH} using Write tool
3. Save URL to ${URL_PATH} using Write tool
4. Execute ls -la to verify"
```

## Meta-Workflow Integration Checklist

When generating workflows, the meta-workflow MUST:

1. ✅ **Validate YAML Structure**
   - No HEREDOC usage
   - Proper indentation
   - Valid GitHub Actions syntax

2. ✅ **Check Bash Syntax**
   - Arithmetic operations use `$(())`
   - Only half-width quotes
   - Proper variable expansion

3. ✅ **Ensure Security**
   - No hardcoded credentials
   - All secrets use `${{ secrets.* }}`
   - OAuth tokens protected

4. ✅ **Include Triggers**
   - Both workflow_dispatch and push
   - Push has paths-ignore
   - All inputs have defaults

5. ✅ **Handle Dependencies**
   - Artifact upload/download pairs
   - Matrix fallbacks
   - Job timeout settings

6. ✅ **Claude Code Integration**
   - MCP config included
   - Proper tool allowlists
   - File persistence instructions

## Prevention Script

Add this validation to meta-workflow:
```bash
# Validate generated workflow
validate_workflow() {
  local workflow_file="$1"
  
  # Check for HEREDOC
  if grep -q '<<.*EOF' "$workflow_file"; then
    echo "ERROR: HEREDOC detected - use echo instead"
    return 1
  fi
  
  # Check for full-width quotes
  if grep -q '[""'']' "$workflow_file"; then
    echo "ERROR: Full-width quotes detected"
    return 1
  fi
  
  # Check for exposed tokens
  if grep -E 'ghp_|sk-|key-' "$workflow_file"; then
    echo "ERROR: Potential credential exposure"
    return 1
  fi
  
  # Validate YAML
  python3 -c "import yaml; yaml.safe_load(open('$workflow_file'))" || {
    echo "ERROR: Invalid YAML syntax"
    return 1
  }
  
  echo "✅ Workflow validation passed"
  return 0
}
```

## Quick Reference

| Error Type | Detection | Fix |
|------------|-----------|-----|
| HEREDOC | `<< EOF` | Use `echo` commands |
| Bad substitution | `${VAR - N}` | Use `$((VAR - N))` |
| Full-width quotes | `"text"` | Use `"text"` |
| Exposed token | `ghp_xxx` | Use `${{ secrets.* }}` |
| Missing trigger | No push handler | Add push with paths-ignore |
| Empty matrix | No fallback | Add `\|\| '["default"]'` |

## Updates History

- **2025-08-16**: Initial documentation created
- **Issues Fixed**: HEREDOC errors, bash arithmetic, quote types, token exposure
- **Workflows Affected**: news-video-improved.yml, meta-workflow-executor-v12.yml