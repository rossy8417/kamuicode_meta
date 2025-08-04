# Claude Code SDK CLI Reference

This document provides a comprehensive reference for Claude Code SDK CLI options, specifically for use in GitHub Actions workflows and YAML configurations.

## Basic Command Structure

```bash
# Standard format
npx @anthropic-ai/claude-code [options] -p "prompt"

# With MCP tools
npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__serverName__toolName,Write,Read" \
  -p "prompt"
```

## Essential CLI Options

### Core Options

| Option | Description | Example |
|--------|-------------|---------|
| `-p, --print` | Execute without interactive mode | `-p "Analyze this code"` |
| `--max-turns` | Limit number of agent turns | `--max-turns 15` |
| `--model` | Set model (sonnet/opus) | `--model sonnet` |
| `--verbose` | Enable detailed logging | `--verbose` |
| `--output-format` | Output format (text/json/stream-json) | `--output-format json` |
| `--input-format` | Input format (text/stream-json) | `--input-format text` |

### Tool Management

| Option | Description | Example |
|--------|-------------|---------|
| `--allowedTools` | Allowed tools without permission | `--allowedTools "Read,Write,Edit"` |
| `--disallowedTools` | Disallowed tools | `--disallowedTools "Bash"` |
| `--mcp-config` | MCP configuration file | `--mcp-config ".claude/mcp-kamuicode.json"` |

### Permission Modes

| Option | Description | Example |
|--------|-------------|---------|
| `--permission-mode` | Permission handling mode | `--permission-mode acceptEdits` |
| `--dangerously-skip-permissions` | Skip all permissions (CI use) | `--dangerously-skip-permissions` |
| `--permission-prompt-tool` | MCP tool for permissions | `--permission-prompt-tool mcp__permissions__approve` |

### Session Management

| Option | Description | Example |
|--------|-------------|---------|
| `-c, --continue` | Continue latest conversation | `-c -p "Fix the errors"` |
| `-r, --resume` | Resume specific session | `-r "session-id" -p "Continue"` |
| `--add-dir` | Add additional directories | `--add-dir ../lib ../shared` |

## MCP Tool Naming Convention

MCP tools follow this naming pattern:
```
mcp__${serverName}__${toolName}
```

Examples:
- `mcp__t2i-google-imagen3__imagen_t2i`
- `mcp__filesystem__read_file`
- `mcp__web-search__search`

## GitHub Actions Usage Patterns

### Basic Pattern
```yaml
- name: Execute with Claude Code SDK
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    npx @anthropic-ai/claude-code \
      -p "$PROMPT" \
      --allowedTools "Read,Write" \
      --max-turns 10 \
      --permission-mode "acceptEdits"
```

### With MCP Tools
```yaml
- name: Generate Image with MCP
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    CLAUDE_CODE_CI_MODE: true
    CLAUDE_CODE_AUTO_APPROVE_MCP: true
  run: |
    npx @anthropic-ai/claude-code \
      -p "Generate an image of a sunset" \
      --mcp-config ".claude/mcp-kamuicode.json" \
      --allowedTools "mcp__t2i-google-imagen3__imagen_t2i,Write" \
      --permission-mode "acceptEdits"
```

### Non-Interactive Analysis
```yaml
- name: Analyze Code
  run: |
    npx @anthropic-ai/claude-code \
      -p "Analyze for security vulnerabilities" \
      --allowedTools "Read" \
      --output-format json \
      --max-turns 5 > analysis.json
```

### Piped Input
```yaml
- name: Process Log File
  run: |
    cat error.log | npx @anthropic-ai/claude-code \
      -p "Analyze these errors and suggest fixes" \
      --allowedTools "Write" \
      --permission-mode "acceptEdits"
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_CODE_CI_MODE` | Enable CI mode | `false` |
| `CLAUDE_CODE_AUTO_APPROVE_MCP` | Auto-approve MCP tools | `false` |
| `ANTHROPIC_API_KEY` | API key for authentication | Required |
| `CLAUDE_CODE_OAUTH_TOKEN` | OAuth token (alternative auth) | Optional |

## Common Tool Combinations

### Planning & Analysis
```bash
--allowedTools "Read,Write,Edit"
```

### Web Research
```bash
--allowedTools "WebSearch,Write"
```

### Image Generation
```bash
--allowedTools "mcp__t2i-google-imagen3__imagen_t2i,Write"
```

### File System Operations
```bash
--allowedTools "mcp__filesystem__read_file,mcp__filesystem__list_directory,Write"
```

## Best Practices

1. **Always specify `--max-turns`** to prevent infinite loops
2. **Use `--permission-mode "acceptEdits"`** for automated workflows
3. **Set environment variables** for CI/CD environments
4. **Use specific tool allowlists** rather than allowing all tools
5. **Enable verbose logging** for debugging with `--verbose`
6. **Use JSON output format** for programmatic parsing

## Error Handling

```bash
# Check exit code
if npx @anthropic-ai/claude-code -p "task" --max-turns 5; then
  echo "Success"
else
  echo "Failed with exit code $?"
fi

# Capture output and errors
OUTPUT=$(npx @anthropic-ai/claude-code -p "task" 2>&1)
```

## References

- [Official CLI Reference](https://docs.anthropic.com/ja/docs/claude-code/cli-reference)
- [SDK Documentation](https://docs.anthropic.com/ja/docs/claude-code/sdk)
- [MCP Documentation](https://docs.anthropic.com/ja/docs/claude-code/mcp)