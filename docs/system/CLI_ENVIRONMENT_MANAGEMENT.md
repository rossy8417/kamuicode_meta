# CLI Environment Management Guide

## Overview
This guide manages the separation between Claude Code CLI user environment and GitHub Actions automated workflows to prevent conflicts and data loss.

## Directory Structure

### CLI-Exclusive Directories
```
cli_generated/
├── media/
│   ├── images/     # CLI generated images
│   ├── videos/     # CLI generated videos
│   ├── audio/      # CLI generated audio
│   └── 3d/         # CLI generated 3D models
└── sessions/       # CLI session data
```

### Shared but CLI-Priority Files
```
.claude/
├── settings.local.json         # CLI settings (updated 2025-07-28 17:22)
├── mcp-kamuicode.json         # Shared MCP configuration
└── settings.github-actions.json  # GitHub Actions specific
```

### CLI-Only Configuration Files
```
.env.claude                    # CLI environment variables
.claude_mcp_defaults.md       # CLI MCP default settings
claude_mcp_helpers.md         # CLI helper functions (Japanese)
.claude/settings.mcp-only.json  # MCP-only settings
```

## File Management Rules

### 🚫 GitHub Actions MUST NOT Modify
- `cli_generated/` - All CLI generated content
- `.claude/settings.mcp-only.json` - CLI MCP settings
- `.env.claude` - CLI environment variables
- `.claude_mcp_defaults.md` - CLI defaults
- `claude_mcp_helpers.md` - CLI helpers

### ⚠️ CLI-Priority (GitHub Actions can read but should not overwrite)
- `.claude/settings.local.json` - CLI permissions and settings

### ✅ Shared Resources (Both can modify)
- `.claude/mcp-kamuicode.json` - MCP service configuration
- `generated/` - GitHub Actions output directory
- `projects/` - Project-based outputs

### ✅ GitHub Actions Exclusive
- `.claude/settings.github-actions.json` - CI/CD settings
- `.github/workflows/` - Workflow definitions
- `generated/` - Automated outputs

## Conflict Prevention

### File Lock Strategy
1. **CLI Detection**: Check for CLI-generated files before GitHub Actions execution
2. **Backup Strategy**: Create backups before any shared file modification
3. **Timestamp Validation**: Verify file modification times

### CLI Environment Detection
```bash
# GitHub Actions should check for CLI activity
if [ -f ".env.claude" ] && [ -d "cli_generated" ]; then
  echo "⚠️ CLI environment detected - Using read-only mode"
  CLI_ACTIVE=true
else
  echo "✅ Clean automation environment"
  CLI_ACTIVE=false
fi
```

## CLI Media Output Standards

### Default Output Directories (as defined in .claude_mcp_defaults.md)
- **Images**: `./cli_generated/media/images`
- **Videos**: `./cli_generated/media/videos`
- **Audio**: `./cli_generated/media/audio`
- **3D Models**: `./cli_generated/media/3d`

### File Naming Convention
```
Prefix: "claude_generated" or "claude_[type]"
Format: claude_img_YYYYMMDD_HHMMSS.extension
Example: claude_img_20250728_172200.png
```

## Settings Priority Hierarchy

### 1. CLI Local Settings (.claude/settings.local.json)
- **Priority**: Highest for CLI sessions
- **Last Updated**: 2025-07-28 17:22
- **Content**: Comprehensive permissions, Git operations, file system access
- **Modification**: CLI user modifications take precedence

### 2. MCP Configuration (.claude/mcp-kamuicode.json) 
- **Priority**: Shared resource
- **Usage**: Both CLI and GitHub Actions
- **Modification**: Coordinated updates only

### 3. GitHub Actions Settings (.claude/settings.github-actions.json)
- **Priority**: CI/CD exclusive
- **Usage**: Automated workflows only
- **Modification**: GitHub Actions managed

## Maintenance Protocol

### Daily
- [ ] Check `cli_generated/` directory size
- [ ] Verify no conflicts in shared files

### Weekly  
- [ ] Review CLI session activity
- [ ] Clean up temporary files (`claude_session_*`, `mcp_cli_*`)

### Monthly
- [ ] Backup CLI configurations
- [ ] Review and update file management rules
- [ ] Archive old CLI generated content

## Troubleshooting

### Common Issues

1. **File Permission Conflicts**
   ```bash
   # Check file ownership and permissions
   ls -la .claude/
   ```

2. **Directory Access Issues**
   ```bash
   # Verify CLI directory structure
   find cli_generated/ -type d -exec ls -ld {} \;
   ```

3. **Settings Sync Problems**
   ```bash
   # Compare settings files
   diff .claude/settings.local.json .claude/settings.github-actions.json
   ```

## Integration with CLAUDE.md

This CLI management system should be referenced in CLAUDE.md to ensure Claude Code understands the environment separation:

```markdown
## CLI Environment Recognition
- CLI active: Respect `cli_generated/` and local settings
- GitHub Actions: Use `generated/` and automation settings
- Never mix CLI and automation outputs
```

---

**Last Updated**: 2025-07-28  
**CLI Settings Modified**: 2025-07-28 17:22  
**Status**: Active CLI environment detected