# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

This is a Meta Workflow Generator System built with Claude Code GitHub Actions integration. The system generates complete workflows based on user requests through Issues or manual triggers.

## Architecture

### Modular Meta Workflow System
- **Prompt Separation**: All prompts are managed as external files in `meta/prompts/`
- **Small Nodes**: Each job has a single responsibility
- **Reliable Execution**: Validates each step before proceeding
- **Re-executable**: Failed jobs can be re-run independently

### Core Components
- `meta/prompts/`: Prompt files for task decomposition, workflow generation, script generation, and documentation
- `.github/workflows/meta-workflow-generator.yml`: Main meta workflow
- `.github/ISSUE_TEMPLATE/`: Issue templates for workflow requests
- Generated outputs: Complete workflows, scripts, and documentation

## Development Setup

### Required Secrets
- `CLAUDE_CODE_OAUTH_TOKEN`: Claude Code authentication token

### MCP Configuration
- Requires `mcp-kamuicode.json` configuration file
- Should be placed in `~/.claude/mcp-kamuicode.json`

### Execution Methods
1. **Issue-driven**: Create issues using the template
2. **Manual**: Use workflow_dispatch trigger

## Notes

- The system automatically decomposes abstract user requests into concrete tasks
- Supports parallel execution for performance optimization
- Includes comprehensive error handling and retry logic
- All generated workflows include validation and testing steps
- Standard development best practices are followed throughout the generated code