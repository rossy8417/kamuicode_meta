# Workflow Validation Guide

**Unified validation and repair guide for GitHub Actions workflows**

## Overview

This guide consolidates all workflow validation patterns and auto-repair protocols used in the Meta-Workflow system.

## Validation Script

**Location**: `scripts/workflow-validator.py`

**Usage**:
```bash
# Validate only
python3 scripts/workflow-validator.py workflow.yml

# Validate and auto-fix
python3 scripts/workflow-validator.py workflow.yml --auto-fix
```

## Validation Checks

### 1. Critical Errors (Prevent Execution)

#### YAML Syntax
- **Check**: Valid YAML structure
- **Fix**: Automatic repair of common syntax errors

#### HEREDOC Patterns
- **Check**: No `cat > file << EOF` patterns
- **Fix**: Convert to echo commands automatically

#### Local Uses References
- **Check**: No `uses: ./path` references
- **Fix**: Comment out with inline implementation note

### 2. Required Structure

#### Top-level Fields
- `name`: Workflow name
- `on`: Trigger configuration
- `jobs`: Job definitions

#### Job Requirements
- `runs-on`: Required for each job
- `steps`: Should have at least one step

#### workflow_dispatch Inputs
- Valid types: `string`, `choice`, `boolean`, `environment`
- Choice inputs must have `options`

### 3. Best Practices (Warnings)

#### Path Patterns
- No absolute paths (use variables)
- PROJECT_DIR must be defined if used

#### MCP Configuration
- Include Write tool with image generation
- Use standard config: `.claude/mcp-kamuicode.json`

#### Data Persistence
- Explicit save paths with Claude Code
- Multi-pattern file search
- URL validity checks

## Auto-Repair Protocols

### HEREDOC Elimination
```bash
# Before (causes YAML error)
cat > file.json << 'EOF'
{
  "key": "value"
}
EOF

# After (auto-fixed)
echo '{' > file.json
echo '  "key": "value"' >> file.json
echo '}' >> file.json
```

### Local Uses Replacement
```yaml
# Before
- uses: ./minimal-units/example.yml

# After (auto-fixed)
# DISABLED: Local uses not supported
# Original: uses: ./minimal-units/example.yml
# TODO: Inline the implementation
- run: echo "Placeholder for implementation"
```

## Validation Report

### Output Format
```json
{
  "workflow": "path/to/workflow.yml",
  "valid": true,
  "can_execute": true,
  "errors": [],
  "warnings": [],
  "fixes_applied": []
}
```

### Report Location
- Saved to: `{workflow_dir}/validation_report.json`
- Used by meta-workflow for decision making

## Integration with Meta-Workflow

### Phase 6: Validation & Deploy
1. Run comprehensive validation
2. Apply auto-fixes if needed
3. Re-validate after fixes
4. Check critical errors
5. Proceed only if executable

### Error Handling
- Critical errors → Stop deployment
- Warnings → Log but continue
- Auto-fixed → Document changes

## Common Issues and Solutions

### Issue: workflow_dispatch Won't Trigger
**Cause**: HEREDOC in workflow
**Solution**: Auto-fix converts to echo commands

### Issue: Placeholder Files Created
**Cause**: Missing Write tool in Claude Code
**Solution**: Validation warns, meta-workflow adds Write tool

### Issue: URL Expiration
**Cause**: No immediate download after generation
**Solution**: Validation checks for curl download patterns

## Related Documents

- `docs/YAML_CONSTRUCTION_GUIDELINES.md` - YAML best practices
- `docs/CLAUDE_CODE_DATA_PERSISTENCE_GUIDE.md` - Data persistence patterns
- `docs/MINIMAL_UNIT_CONNECTION_PATTERNS.md` - Unit data flow

## Maintenance

### Adding New Checks
1. Add to `workflow-validator.py`
2. Update this guide
3. Test with known problematic workflows

### Updating Fix Patterns
1. Test fix on sample workflows
2. Update auto-repair logic
3. Document in this guide

---

**Version**: 1.0
**Last Updated**: 2025-08-11
**Status**: Active