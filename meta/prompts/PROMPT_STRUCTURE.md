# Prompt Template Structure Documentation

## Overview
This document describes the structure and usage of prompt templates in the meta-workflow system.

## Current Structure (2025-08-17)

### Main Template
- **File**: `meta/prompts/generation-prompt-template.txt`
- **Purpose**: Primary template for workflow generation
- **Lines**: 210
- **Features**:
  - Claude Code SDK error handling patterns
  - MCP result saving patterns
  - I2V file verification logic
  - Narration generation fallback mechanisms
  - HEREDOC prevention rules
  - Recovery job requirements

### Template Loading in Meta-Workflow

The meta-workflow executor v12 now loads the prompt template from an external file:

```bash
# Line 664-666 in meta-workflow-executor-v12.yml
if [ -f "meta/prompts/generation-prompt-template.txt" ]; then
  cp meta/prompts/generation-prompt-template.txt generation_prompt.txt
else
  # Fallback to embedded prompt (legacy support)
fi
```

### Key Improvements (Latest Update)

1. **External File Loading**: Template is now loaded from file instead of being embedded
2. **Error Handling**: Added Claude Code SDK error handling with fallback patterns
3. **File Saving**: Enhanced MCP result saving to prevent placeholder files
4. **Narration Fallback**: espeak-ng fallback for T2S failures

### Directory Structure

```
meta/prompts/
├── generation-prompt-template.txt    # Main template (active)
├── generation-prompt-template.txt.old # Previous version (backup)
├── templates/
│   └── workflow-fix-prompt.md       # Fix prompt for validation
├── active/                          # Active prompts (legacy)
├── deprecated/                      # Deprecated prompts
└── docs/                           # Documentation

```

## Usage

### For Meta-Workflow
The meta-workflow automatically loads `generation-prompt-template.txt` during workflow generation phase.

### For Manual Updates
1. Edit `meta/prompts/generation-prompt-template.txt`
2. Commit changes
3. Meta-workflow will use updated template on next run

### Template Variables
- `PROJECT_DIR_PLACEHOLDER`: Replaced with actual project directory
- `SECRETS_PLACEHOLDER`: Replaced with GitHub Actions secrets syntax

## Maintenance

### Adding New Patterns
1. Add pattern to `generation-prompt-template.txt`
2. Document in this file
3. Test with meta-workflow execution

### Version Control
- Keep backup as `.old` file when making major changes
- Document changes in commit messages

## Recent Changes Log

### 2025-08-17
- Externalized prompt template from meta-workflow
- Added Claude Code SDK error handling
- Enhanced I2V file saving patterns
- Added narration generation fallback
- Consolidated duplicate templates

### Previous Versions
- `generation-prompt-template.txt.old`: Pre-enhancement version (151 lines)
- Embedded prompt in meta-workflow: Now serves as fallback only