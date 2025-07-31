# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📚 Documentation Reference Guide

**🎯 Context-based references - Only access needed docs for your specific task**

### For workflow generation & dependencies
→ **`UNIFIED_DEPENDENCY_GUIDE.md`** (AI-optimized, single source)

### For minimal unit selection & catalog
→ **`minimal-units/MINIMAL_UNITS_CATALOG.md`** (53 units, full paths)

### For technical implementation details
→ **`minimal-units/UNIT_INTERFACE_SPEC.md`** (YAML interface specs)

### For prompt creation & meta-workflow design
→ **`meta/prompts/`** directory specific prompt files

### For system overview & architecture
→ **`README.md`** (system overview)

**⚠️ Important**: Other docs (docs/, kamuicode-workflow/) are detailed technical references. Not needed for regular tasks.

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

### ⚠️ Known Issue: Settings Overwrite
Claude Code may overwrite `.claude/settings.local.json` permissions. To restore:
```bash
./scripts/restore-claude-permissions.sh
```

### MCP Output Directory Rules
- **CLI Sessions**: Use `./cli_generated/media/[images|videos|audio|3d]/`
- **GitHub Actions**: Use `./generated/media/[type]/` or `./projects/project-name/`
- **File Prefix**: CLI uses `claude_generated` or `claude_[type]` prefix

## Current Architecture (v9.0)

### Minimal Unit Based Dual-Approach Meta Workflow System
- **Claude Code SDK Integration**: Dynamic task decomposition using Claude Code SDK
- **55 Minimal Units**: Complete catalog of reusable workflow components
- **Dual Workflow Generation**:
  - **Original Approach**: Dynamic composition from minimal units
  - **Orchestrator Approach**: Following kamuicode-workflow patterns
- **Best-of-Both Selection**: Compare and merge the best elements from both approaches
- **Ultra-Detailed Task Decomposition**: Human-like task breakdown with proper dependencies
- **Task Dependency Management**: Strict execution order based on data flow and prerequisites
- **Optimal Parallel Processing**: 3-way, 4-way, or 5-way parallel execution where dependencies allow
- **Quality Validation**: YAML syntax, GitHub Actions structure, dependency verification
- **Safe Deployment**: Generated workflows deployed with .disabled extension for review

### Core Components
- **`minimal-units/`**: 55 reusable workflow units organized by category
  - 8 Image units (t2i-imagen3, image-analysis, banner-text, etc.)
  - 13 Video units (t2v-veo3, i2v-seedance, video-concat, etc.)
  - 10 Audio units (bgm-generate-mcp, t2s-google, bgm-overlay, etc.)
  - 9 Planning units (planning-ccsdk, web-search, data-analysis, etc.)
  - 7 Utility units (local-save, git-pr-create, sns-publish, etc.)
  - And more...
- **`.github/workflows/meta-workflow-executor-v9.yml`**: Dynamic meta workflow with enhanced features
- **`meta/prompts/`**: Enhanced prompts for human-like task decomposition and dependency analysis
- **`.github/workflows/generated/`**: Generated workflow deployment area

### Key Principles (v9.0)
1. **Task Dependencies First**: Every task must declare its prerequisites
2. **Data Flow Tracking**: Outputs from one task become inputs for dependent tasks
3. **Parallel Where Possible**: Only independent tasks run in parallel
4. **Human-like Sequencing**: Tasks ordered as a human would naturally approach them
5. **GitHub Actions Compliance**: Strict adherence to YAML syntax and Actions specifications
6. **Basic Pattern Support**: Direct support for serial, parallel, conditional, and loop patterns
7. **Extensibility**: New units and custom nodes can be created when existing units don't meet requirements
8. **Not Over-dependent on Orchestrator**: Balance between using reference patterns and custom implementations

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

**Key MCP Services** (from `.claude/mcp-kamuicode.json`) - 24 services total:
- **T2I**: `t2i-google-imagen3`, `t2i-fal-imagen4-ultra`, `t2i-fal-imagen4-fast`, `t2i-fal-flux-schnell`, `t2i-fal-rundiffusion-photo-flux`
- **T2V**: `t2v-fal-veo3-fast`, `t2v-fal-wan-v2-2-a14b-t2v`
- **I2V**: `i2v-fal-hailuo-02-pro`, `i2v-fal-bytedance-seedance-v1-lite`
- **T2M**: `t2m-google-lyria`
- **T2S**: `t2s-fal-minimax-speech-02-turbo`
- **V2A**: `v2a-fal-thinksound`
- **V2V**: `v2v-fal-luma-ray2-modify`, `v2v-fal-creatify-lipsync`, `v2v-fal-pixverse-lipsync`, `v2v-fal-minimax-voice-design`, `v2v-fal-pixverse-extend`, `v2v-fal-bria-background-removal`, `v2v-fal-topaz-upscale-video`
- **I2I**: `i2i-fal-flux-kontext-max`, `i2i-fal-flux-kontext-lora`
- **I2I3D**: `i2i3d-fal-hunyuan3d-v21`
- **R2V**: `r2v-fal-vidu-q1`
- **Training**: `train-fal-flux-kontext-trainer`

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

#### Dual-Approach Workflow Generation Implementation
The main workflow now uses:
1. **Task Decomposition** → Ultra-detailed task breakdown using Claude Code SDK
2. **Unit Selection** → Select from 55 minimal units based on task requirements
3. **Parallel Workflow Generation**:
   - **Original Approach**: Dynamic composition from minimal units
   - **Orchestrator Approach**: Following kamuicode-workflow patterns
4. **Comparison & Merge** → Analyze both workflows and select best elements
5. **Final Composition** → Create hybrid workflow with best-of-both approach
6. **Validation** → YAML syntax, GitHub Actions structure, dependency verification
7. **Safe Deployment** → `.github/workflows/generated/` with .disabled extension

### Development Best Practices

#### When Adding New Workflows
1. **Reference kamuicode-workflow patterns** for orchestrator structure
2. **Follow ultra-detailed task breakdown** with dependency management
3. **Select appropriate minimal units** from 55 available units
4. **Ensure proper task sequencing** based on data flow
5. **Implement optimal parallelization** (3-5 way parallel)
6. **Test deployment through staged system**

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

## Custom Node Examples

When existing minimal units cannot handle specific requirements, use **Custom Node Examples**:

**📂 Available Categories** (`docs/examples/custom-nodes/`):
- **media-processing/**: Multi-format generation, quality optimization
- **data-processing/**: Batch processing, large dataset handling  
- **external-integration/**: API aggregation, external service integration
- **utilities/**: Health checking, system monitoring

**🎯 Key Examples**:
- `multi-format-generator.yml`: Generate image+video+audio simultaneously
- `batch-processor.yml`: Process 25+ items with 5-way parallel execution
- `api-aggregator.yml`: Collect data from news/social/market/technical APIs
- `health-checker.yml`: System resource + MCP service availability check

**📋 Usage Pattern**:
```yaml
custom-processing:
  uses: ./docs/examples/custom-nodes/category/example.yml
  needs: [prerequisite-jobs]
  with:
    custom_param: ${{ inputs.value }}
```

**🔄 Evolution Path**: Successful custom nodes should be converted to minimal units when they prove universally useful.

## Notes for Claude Code Sessions

- **This system is actively developed using Claude Code** - maintain development continuity
- **All examples in `meta/examples/` represent production-ready templates**
- **Custom node examples in `docs/examples/custom-nodes/` provide extension patterns**
- **The main workflow uses template selection instead of complex task decomposition**
- **Simplified staged deployment prevents broken workflows from reaching production**
- **File path reference patterns are critical for workflow continuity**
- **MCP services are limited to AI generation - use external APIs for other functions**
- **Final workflows are deployed to `.github/workflows/generated/` in simple structure**