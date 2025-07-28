# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

This is a **Meta Workflow Generator System (Kamui Rossy)** built with Claude Code GitHub Actions integration. The system uses **template-based generation** with **staged deployment system** to generate high-quality, executable GitHub Actions workflows efficiently.

## CLI Environment Recognition

**CRITICAL**: Active CLI environment detected (CLI settings updated: 2025-07-28 17:22)

### Environment Separation Rules
- **CLI Environment**: `cli_generated/` directory + `.env.claude` + local settings
- **GitHub Actions**: `generated/` directory + automation settings
- **Never mix CLI and automation outputs**

### File Management Priority
1. **CLI-Protected**: `cli_generated/`, `cli_config/`, `.claude/settings.local.json`
2. **Shared**: `.claude/mcp-kamuicode.json` (coordinate updates)
3. **GitHub Actions**: `generated/`, `.github/workflows/`

### MCP Output Directory Rules
- **CLI Sessions**: Use `./cli_generated/media/[images|videos|audio|3d]/`
- **GitHub Actions**: Use `./generated/media/[type]/` or `./projects/project-name/`
- **File Prefix**: CLI uses `claude_generated` or `claude_[type]` prefix

## Current Architecture (v8.1)

### Template-Based Meta Workflow System with Simplified Deployment
- **Template Selection**: Uses 9 reference workflows in `meta/examples/` instead of complex task decomposition
- **Simplified 3-Stage Deployment**: generation → validation → deployment with .disabled safety mechanism
- **Prompt Separation**: All prompts managed as external files in `meta/prompts/`
- **Small Nodes**: Each job has single responsibility with independent re-execution capability
- **Quality Validation**: YAML syntax, GitHub Actions structure, MCP references, dependencies check
- **Persistent Storage**: Final workflows in simplified `.github/workflows/generated/` structure

### Core Components
- **`meta/examples/`**: 9 GitHub Actions workflow templates (video, 3D, audio, image, blog, data analysis, multimedia, news, presentation)
- **`.github/workflows/meta-workflow-executor-v8.yml`**: Main meta workflow (v8.1 with Critical System Repair Protocol)
- **`.github/workflows/auto-fix-deployment.yml`**: Automated deployment and error recovery system
- **`.github/workflows/continuous-system-monitor.yml`**: System health monitoring
- **`.github/ISSUE_TEMPLATE/`**: Issue templates for workflow requests
- **`meta/prompts/`**: Prompt files for task decomposition, workflow generation, script generation, documentation
- **`generated/`**: Organized outputs with metadata and logs storage
- **`.github/workflows/generated/`**: Simple workflow deployment area

## Critical System Repair & Improvement Protocol (v8.1)

### 🚨 MANDATORY Workflow Repair Guidelines

When encountering GitHub Actions YAML errors or workflow failures, follow this **proven repair protocol** that achieved 100% success rate:

#### **Phase 1: Problem Diagnosis**
1. **Identify Failure Pattern**: Check `gh run list --workflow="workflow-name"` for failure types
2. **Isolate Failure Point**: Use `gh run view <run-id> --log-failed` for specific error location
3. **Categorize Issue Type**:
   - YAML Syntax Error → Apply HEREDOC Elimination Protocol
   - GitHub Context Variable Error → Apply Safe Variable Protocol  
   - File Path Error → Apply Flexible Path Resolution
   - Artifact Access Error → Apply Artifact Flow Protocol

#### **Phase 2: Systematic Repair (PROVEN EFFECTIVE)**

**🔧 HEREDOC Elimination Protocol**
```yaml
# ❌ PROBLEMATIC (Causes YAML parsing errors)
cat > file.yml << 'EOF'
name: "workflow"
on: workflow_dispatch
EOF

# ✅ SAFE (Echo-based generation)
echo 'name: "workflow"' > file.yml
echo 'on: workflow_dispatch' >> file.yml
```

**🔧 Safe GitHub Context Variable Protocol**
```yaml
# ❌ PROBLEMATIC (In HEREDOC context)
cat > file.json << EOF
{"issue": ${{ github.event.issue.number }}}
EOF

# ✅ SAFE (Variable extraction first)
ISSUE_NUMBER="${{ github.event.issue.number }}"
echo "{\"issue\": $ISSUE_NUMBER}" > file.json
```

**🔧 Flexible Path Resolution Protocol**
```bash
# Multi-pattern file search approach
FOUND_FILE=""
if [ -f "$EXPECTED_PATH" ]; then
  FOUND_FILE="$EXPECTED_PATH"
elif [ -f "$(basename "$EXPECTED_PATH")" ]; then
  FOUND_FILE="$(basename "$EXPECTED_PATH")"
else
  FOUND_FILE=$(find . -name "*target*.yml" | head -1)
fi
```

**🔧 Python Execution Protocol**
```bash
# ❌ PROBLEMATIC (Multi-line indentation errors)
python3 -c "
import yaml
try:
    # Complex logic
"

# ✅ SAFE (One-liner approach)
python3 -c "import yaml; yaml.safe_load(open('file.yml'))" 2>/dev/null
```

#### **Phase 3: Incremental Testing Protocol**

1. **Minimal Working Version First**: Create simplest possible working workflow
2. **Staged Enhancement**: Add one feature at a time, test after each addition
3. **Commit + Push Every Fix**: `git commit -m "fix: specific-issue" && git push`
4. **Validate Each Stage**: Ensure each modification works before proceeding

#### **Phase 4: Template Quality Assurance**

**🔧 GitHub Actions Structure Validation**
Templates must include ALL required fields:
```yaml
name: "Template Name"           # ✅ Required
on:                            # ✅ Required  
  workflow_dispatch:           # ✅ Required
jobs:                          # ✅ Required
  job-name:                    # ✅ Required
    runs-on: ubuntu-latest     # ✅ Required
    steps:                     # ✅ Required
      - name: Step Name        # ✅ Required
        run: echo "command"    # ✅ Required
```

**🔧 Template Conversion Protocol**
When converting task definitions to GitHub Actions:
1. **Extract Core Logic**: Identify essential workflow steps
2. **Map to GitHub Actions Jobs**: Convert logical steps to actual jobs
3. **Add Proper Triggers**: Include `workflow_dispatch` with inputs
4. **Include Error Handling**: Add validation and fallback steps
5. **Test YAML Validity**: Use `python3 -c "import yaml; yaml.safe_load(open('file.yml'))"`

### **Emergency Fallback Strategy**
If all else fails, create minimal fallback workflow:
```yaml
name: "Fallback Workflow"
on: workflow_dispatch
jobs:
  fallback:
    runs-on: ubuntu-latest
    steps:
      - name: Fallback Step
        run: echo "Fallback workflow executed"
```

### **Success Metrics Achieved (v8.1)**
- ✅ 12/12 Jobs Success Rate: 100%
- ✅ All 4 Phases Completed: validation → generation → evaluation → deployment
- ✅ 7 Artifacts Generated: Complete workflow package
- ✅ Zero YAML Syntax Errors: Robust echo-based generation
- ✅ Zero File Path Errors: Flexible resolution logic

### **Auto-Application Instructions for Claude Code**

**CRITICAL**: When any GitHub Actions workflow fails, **automatically apply this protocol**:

1. **First Response**: Check `gh run list --workflow="failing-workflow"` and `gh run view <id> --log-failed`
2. **Error Classification**: 
   - Contains "YAML syntax error" → Apply HEREDOC Elimination immediately
   - Contains "File not found" → Apply Flexible Path Resolution  
   - Contains "IndentationError" → Apply Python Execution Protocol
   - Contains `${{ github.*` in error → Apply Safe Variable Protocol
3. **Repair Implementation**: Use exact code patterns shown above
4. **Testing**: Always `git commit && git push` after each fix
5. **Validation**: Confirm with `gh run list` before proceeding

**Template Repair Trigger**: When validate-workflow-structure fails with score < 75:
- Immediately check templates in `meta/examples/` 
- Apply Template Conversion Protocol to any non-GitHub Actions format files
- Prioritize templates used by current workflow generation

**Quality Gates**: Never bypass these checks:
- YAML syntax validation with Python
- GitHub Actions structure requirements (name, on, jobs, steps)
- File path existence before operations
- Artifact flow continuity between jobs

### **Maintenance Schedule**
- **Daily**: Monitor `gh run list` for failures  
- **Weekly**: Validate all templates in `meta/examples/`
- **Monthly**: Review and update protocol based on new failure patterns

## Development Guidelines for Claude Code

### File Structure to Respect
```
meta/examples/           # 9 reference workflow templates - DO NOT modify existing structure
├── README.md           # Complete documentation with Mermaid diagrams
├── video-content-creation.yml (14 tasks, 45min)
├── multimedia-ad-campaign.yml (16 tasks, 60min)
├── 3d-model-creation.yml (10 tasks, 30min)
├── image-generation.yml (8 tasks, 20min)
├── audio-music-creation.yml (11 tasks, 35min)
├── presentation-slide-creation.yml (12 tasks, 40min)
├── data-analysis-visualization.yml (8 tasks, 45min)
├── news-summarization.yml (6 tasks, 25min)
└── blog-article-creation.yml (9 tasks, 35min)

.github/workflows/
├── meta-workflow-executor-v8.yml    # Main meta workflow (v8.1)
├── auto-fix-deployment.yml          # Automated error recovery system
├── continuous-system-monitor.yml    # System health monitoring
└── generated/                       # Simple generated workflow deployment
    └── *.yml                        # Generated workflows

generated/               # Metadata and logs storage
├── metadata/            # Analysis data (persistent)
│   ├── stepback-analysis/
│   ├── requirement-analysis/
│   ├── task-decomposition/
│   └── evaluation/
└── logs/               # Execution logs (persistent)
    └── run-{number}-{timestamp}/
```

### MCP Integration Rules
**MCP Configuration**: See `docs/MCP_CONFIGURATION_GUIDE.md` for complete service list and setup instructions.

**Key MCP Services** (from `.claude/mcp-kamuicode.json`):
- **T2I**: `t2i-google-imagen3`, `t2i-fal-imagen4-ultra`, `t2i-fal-imagen4-fast`
- **T2V**: `t2v-fal-veo3-fast`
- **I2V**: `i2v-fal-hailuo-02-pro`, `i2v-fal-bytedance-seedance-v1-lite`
- **T2M**: `t2m-google-lyria`
- **V2A**: `v2a-fal-thinksound`
- **V2V**: `v2v-fal-luma-ray2-modify`, `v2v-fal-creatify-lipsync`, `v2v-fal-pixverse-lipsync`
- **I2I3D**: `i2i3d-fal-hunyuan3d-v21`

**IMPORTANT**: 
- Do NOT reference non-existent MCP services (e.g., `web-search`, `rss-parser`, `generic kamuicode`). Use external API calls instead.
- For GitHub Actions, set environment variables: `CLAUDE_CODE_CI_MODE=true` and `CLAUDE_CODE_AUTO_APPROVE_MCP=true`

### Code Patterns to Follow

#### File Path Reference Pattern (Critical)
```bash
# Consistent file path extraction from MCP outputs
IMAGE_PATH=$(jq -r '.image_url // .file_path // "none"' "$ref_file" 2>/dev/null)
VIDEO_PATH=$(jq -r '.video_url // .file_path // "none"' "$video_file")
AUDIO_PATH=$(jq -r '.audio_url // .file_path // "none"' "$audio_file")

# IMPORTANT: Use projects/ paths for all project storage
mkdir -p projects/current-session/metadata      # For current session metadata
mkdir -p projects/current-session/logs          # For execution logs
mkdir -p projects/current-session/temp          # For temporary files
mkdir -p projects/current-session/scripts       # For temporary scripts
mkdir -p projects/current-session/final         # For final deliverables

# IMPORTANT: Use .github/workflows/generated/ for final workflow deployment
mkdir -p .github/workflows/generated             # For generated workflows (simple structure)

# Directory existence checks before file operations
if [ ! -d "$(dirname "$TARGET_FILE")" ]; then
  mkdir -p "$(dirname "$TARGET_FILE")"
fi
```

### 🚨 MANDATORY FILE ORGANIZATION RULES 🚨

**CRITICAL**: Follow these rules EXACTLY. No exceptions. No creativity.

#### **Project-Based File Creation Rules**
```bash
# ✅ CORRECT - Use project-based directory structure
projects/current-session/scripts/    # Temporary scripts (auto-delete eligible)
projects/current-session/temp/       # Temporary files
projects/current-session/logs/       # Execution logs
projects/current-session/metadata/   # Analysis metadata
projects/current-session/final/      # Final deliverables
projects/project-name/               # Specific project files

# ❌ FORBIDDEN - Never create these patterns
./new_directory/           # No new root directories
./temp_something/          # No root temp directories  
./*_temp/                 # No root temp patterns
./script_*.py             # No root script files
./output_*.json           # No root output files
./generated/              # Old structure - use projects/ instead
./downloads/              # Old structure - use projects/ instead
```

#### **Script Generation Rules**
```bash
# ✅ CORRECT - Project-based scripts location
projects/current-session/scripts/workflow_script.py    # Auto-delete eligible
projects/current-session/scripts/temp_processing.sh    # Auto-delete eligible
projects/project-name/scripts/specific_tool.py         # Project-specific scripts

# ✅ CORRECT - Permanent utility scripts (rare)
scripts/utility_tool.py                               # Only if truly reusable

# ❌ FORBIDDEN - Never place scripts here
./script.py                             # Root directory
./temp_script.sh                        # Root directory
./process_*.py                          # Root directory
./generated/scripts/                    # Old structure
```

#### **Output File Rules**
```bash
# ✅ CORRECT - Project-based output locations
projects/current-session/final/output.mp4           # Final deliverables
projects/current-session/temp/intermediate.json     # Temporary processing
projects/project-name/assets/result.png             # Project assets

# ❌ FORBIDDEN - Root directory pollution
./output.mp4                            # Root directory
./result.json                           # Root directory
./scene_*.mp4                          # Root directory (clean up existing!)
./generated/final/                      # Old structure
./downloads/project-name/               # Old structure
```

#### **Directory Creation Rules**
1. **NEVER create new directories in root** without explicit approval
2. **ALWAYS use project-based structure**: `projects/`, `docs/`, `scripts/`, `meta/`
3. **Check directory existence** before creating subdirectories
4. **Use proper subdirectory naming**: `projects/[project-name]/[purpose]/[files]`
5. **For current session**: Use `projects/current-session/` as default project

#### **Enforcement Protocol**
- **Before creating any file**: Check if target directory exists in approved structure
- **Before mkdir**: Verify it's within approved directory tree
- **After task completion**: Verify no files were created in root directory
- **Violation penalty**: Task must be redone with correct file placement

### 🧹 **Cleanup and Organization Guidelines**

For file deletion and directory organization tasks, refer to:
**📋 `docs/analysis/CLEANUP_PROTOCOL.md`**

This document contains:
- **バルス Protocol**: Complete system reset guidelines
- **整理整頓ガイドライン**: Directory organization standards and criteria
- **判定基準**: Classification criteria for deletion/integration/preservation
- **実行チェックリスト**: Pre/post organization verification steps

**When asked to "整理整頓" or organize directories:**
1. Review the guidelines in `CLEANUP_PROTOCOL.md`
2. Apply the established criteria (プロジェクト中心主義, 重複解消原則, シンプル構造原則)
3. Confirm with user before executing major changes
4. Update relevant documentation after changes

#### Ultra-Detailed Task Breakdown
Each workflow must include:
- **Human unconscious thought process simulation**
- **GitHub Actions node design**
- **Task dependencies and parallel groups**
- **Implementation details with MCP/script/external API**
- **Validation criteria and error handling**
- **Duration estimates (5-60 minutes total)**

#### Simplified 3-Stage Deployment Implementation
The main workflow now uses:
1. **Template Selection** → Select best template from `meta/examples/` based on workflow type
2. **Workflow Generation** → Generate workflow based on selected template
3. **Validation** → YAML syntax, GitHub Actions structure, MCP references check (75+ score required)
4. **Direct Deployment** → `.github/workflows/generated/` (simple structure)
5. **Metadata & Logs Storage** → `projects/current-session/metadata/` + `projects/current-session/logs/` (permanently stored)

### Development Best Practices

#### When Adding New Workflows
1. **Use existing templates** as base structure
2. **Follow ultra-detailed task breakdown pattern**
3. **Include proper MCP service integration**
4. **Add file path reference patterns**
5. **Update `meta/examples/README.md`** with Mermaid diagram
6. **Test deployment through simplified staging system**

#### When Modifying Main Workflow
- **Maintain simplified staged deployment system**
- **Keep validation scoring system (75+ points for pass)**
- **Preserve template selection logic**
- **Deploy to `.github/workflows/generated/` for generated workflows**
- **Simple structure without complex subdirectories**

#### Error Handling
- **External API fallbacks** for missing MCP services
- **Retry logic** with exponential backoff
- **Comprehensive logging** to `.logs/` directories
- **Graceful degradation** strategies

### Required Secrets & Configuration
- **`CLAUDE_CODE_OAUTH_TOKEN`**: Claude Code authentication token
- **`.claude/mcp-kamuicode.json`**: MCP configuration (AI generation services only)

### Execution Methods
1. **Issue-driven**: Create issues using workflow-request.yml template
2. **Manual**: Use `workflow_dispatch` trigger with parameters
3. **Simple deployment**: Automatic quality assurance → direct deployment to `.github/workflows/generated/`

## Development Philosophy

- **Quality over Speed**: Use simplified staged deployment for reliability
- **Template-based Efficiency**: Leverage existing patterns instead of generating from scratch  
- **MCP-First**: Integrate AI generation services as primary tools
- **External API Fallback**: Handle missing services gracefully
- **Ultra-detailed Decomposition**: Break down to AI/script/MCP executable granularity
- **Parallel Execution**: Optimize performance with dependency management
- **Safe Deployment**: Use .disabled extension for staging safety
- **Manual Activation**: Ensure human oversight for workflow activation

## Notes for Claude Code Sessions

- **This system is actively developed using Claude Code** - maintain development continuity
- **All examples in `meta/examples/` represent production-ready templates**
- **The main workflow uses template selection instead of complex task decomposition**
- **Simplified staged deployment prevents broken workflows from reaching production**
- **File path reference patterns are critical for workflow continuity**
- **MCP services are limited to AI generation - use external APIs for other functions**
- **Final workflows are deployed to `.github/workflows/generated/` in simple structure**