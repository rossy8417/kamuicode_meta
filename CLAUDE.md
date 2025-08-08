# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📚 Documentation Reference Guide

**🎯 Context-based references - Only access needed docs for your specific task**

### For workflow generation & dependencies
→ **`docs/UNIFIED_DEPENDENCY_GUIDE.md`** (AI-optimized, single source)

### For minimal unit selection & catalog
→ **`minimal-units/MINIMAL_UNITS_CATALOG.md`** (80 units, full paths)

### For technical implementation details
→ **`docs/UNIT_INTERFACE_SPEC.md`** (YAML interface specs)

### For prompt creation & meta-workflow design
→ **`meta/prompts/`** directory specific prompt files

### For meta-workflow construction & validation
→ **`projects/workflow-execution-logs/meta-workflow-construction-checklist.md`** (Universal construction checklist)
→ **`docs/YAML_CONSTRUCTION_GUIDELINES.md`** (YAML structure guidelines)
→ **`docs/successful-workflow-patterns.md`** (Proven success patterns)
→ **`meta/domain-templates/video-production/checklist-video-specific.md`** (Video generation domain-specific)

### For system overview & architecture
→ **`README.md`** (system overview)

**⚠️ Important**: Other docs (docs/, kamuicode-workflow/) are detailed technical references. Not needed for regular tasks.

## 🎯 Task Execution Priority Guidelines

### Before Starting Any Task
1. **List all pending tasks** using TodoWrite tool
2. **Analyze dependencies** between tasks to identify blocking issues
3. **Consider execution order** to minimize rework and maximize efficiency
4. **Present the plan** to user before execution when handling multiple tasks

### Priority Decision Framework
1. **🚨 Blocking Issues First**: Fix problems preventing other work
   - Example: Fix envsubst JSON issue before testing meta-workflow
   - Example: Create required methods before modifying callers

2. **🏗️ Foundation Before Features**: Build infrastructure before implementation
   - Example: Update domain-template-loader.py before meta-workflow changes
   - Example: Fix file organization before adding new features

3. **✅ Test Before Deploy**: Validate all changes before deployment
   - Example: Test workflow locally before git push
   - Example: Verify JSON structure before using in production

4. **📝 Document After Changes**: Update documentation after code modifications
   - Example: Update CLAUDE.md after system changes
   - Example: Log execution results in workflow-execution-logs

### Example Priority Analysis
```
Pending Tasks:
1. Add new method to domain-template-loader.py
2. Fix meta-workflow v12 task decomposition 
3. Test meta-workflow v12
4. Delete specific commands from settings.json
5. Verify all 24 domain templates

Optimal Order:
1. First: Add method (others depend on this)
2. Second: Fix meta-workflow (uses the new method)
3. Third: Delete settings commands (clean environment)
4. Fourth: Test meta-workflow (needs 1,2,3 complete)
5. Last: Verify templates (can run independently)
```

### Common Task Dependencies
- **Script changes** → **Workflow updates** → **Testing**
- **Environment setup** → **Feature implementation** → **Validation**
- **Error fixes** → **Retry execution** → **Log results**

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

## Current Architecture (v12.0)

### Domain Template Enhanced Meta Workflow System
- **Claude Code SDK Integration**: Dynamic task decomposition using Claude Code SDK
- **80 Minimal Units**: Complete catalog of reusable workflow components
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
- **`minimal-units/`**: 80 reusable workflow units organized by category
  - 8 Image units (t2i-imagen3, image-analysis, banner-text, etc.)
  - 13 Video units (t2v-veo3, i2v-seedance, video-concat, etc.)
  - 10 Audio units (bgm-generate-mcp, t2s-google, bgm-overlay, etc.)
  - 9 Planning units (planning-ccsdk, web-search, data-analysis, etc.)
  - 7 Utility units (local-save, git-pr-create, sns-publish, etc.)
  - 27 External API units (YouTube, OpenAI, Slack, Twitter, Google Sheets, GitHub, etc.)
  - And more...
- **`.github/workflows/meta-workflow-executor-v12.yml`**: Domain template integrated meta workflow
- **`meta/prompts/`**: Enhanced prompts for human-like task decomposition and dependency analysis
- **`.github/workflows/generated/`**: Generated workflow deployment area

### Key Principles
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

## Critical Workflow Generation Rules (MUST FOLLOW)

### 🚨 Prevent Common Errors When Generating Workflows

**IMPORTANT**: These rules prevent the most common errors discovered through testing. Follow them EXACTLY when generating workflows:

#### 1. ❌ NEVER use `uses:` with local paths
```yaml
# ❌ WRONG - GitHub Actions cannot reference local files
- uses: ./minimal-units/research/web-search-claude.yml

# ✅ CORRECT - Always inline the implementation
- name: Execute Web Search
  run: |
    npx @anthropic-ai/claude-code \
      -p "$PROMPT" \
      --allowedTools "WebSearch,Write" \
      --permission-mode "acceptEdits"
```

#### 2. ❌ NEVER use absolute paths
```yaml
# ❌ WRONG - Will fail in GitHub Actions
path: /media/image.png
path: /projects/issue-60/media/video.mp4

# ✅ CORRECT - Always use variables
path: ${{ needs.setup.outputs.project_dir }}/media/image.png
```

#### 3. ✅ ALWAYS include MCP config for AI tools
```bash
# ❌ WRONG - MCP tools won't work
npx @anthropic-ai/claude-code --allowedTools "mcp__t2i-kamui-imagen3__imagen_t2i"

# ✅ CORRECT - Must include config
npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2i-kamui-imagen3__imagen_t2i,Bash,Write"
```

#### 4. ✅ ALWAYS share files between jobs with artifacts
```yaml
# After generating files
- name: Upload Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: my-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/media/

# Before using files from another job
- name: Download Artifacts
  uses: actions/download-artifact@v4
  with:
    name: my-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/media/
```

#### 5. ✅ ALWAYS handle dynamic filenames
```bash
# Video files often have dynamic names - handle them
if [ ! -f "video.mp4" ]; then
  for file in *.mp4; do
    if [ -f "$file" ]; then
      mv "$file" "video.mp4"
      break
    fi
  done
fi
```

### Meta-Workflow Integration
When meta-workflow generates workflows, it MUST check:
- No `uses:` references to local files
- All paths use `${{ needs.setup.outputs.project_dir }}`
- MCP tools include `--mcp-config`
- Jobs sharing files have artifact upload/download
- File existence checks with error handling

## 🚨 MCP (Model Context Protocol) Connection Management

### **CRITICAL: MCP Server Connection Limitations**

**The kamui-code.ai MCP server automatically disconnects after approximately 15-20 minutes of connection time.**

#### Impact on GitHub Actions
- Connection will be lost during long-running workflows (>20 minutes)
- All MCP tools (image/video/audio generation) become unavailable
- Manual reconnection would interrupt GitHub Actions execution

#### MCP Connection Strategy
1. **Track Elapsed Time Since Workflow Start**
   ```bash
   # Record workflow start time
   WORKFLOW_START_TIME=$(date +%s)
   
   # Check elapsed time before MCP operations
   check_elapsed_time() {
     local current_time=$(date +%s)
     local elapsed=$((current_time - WORKFLOW_START_TIME))
     
     if [ $elapsed -gt 900 ]; then  # 15 minutes
       echo "Warning: Approaching MCP timeout limit"
       echo "Switching to fallback generation methods"
       return 1
     fi
     return 0
   }
   ```

2. **Preventive Measures**
   - Check connection viability BEFORE starting MCP operations
   - Use fallback methods if approaching timeout
   - Complete MCP operations early in workflow

3. **Workflow Design Pattern**
   ```yaml
   # ✅ RECOMMENDED: Front-load MCP operations
   jobs:
     early-mcp-operations:  # Run within first 10 minutes
       timeout-minutes: 10
       steps:
         - name: Check Time Window
           run: |
             if [ "${{ job.index }}" -gt 10 ]; then
               echo "Too late for MCP, using fallback"
               exit 0
             fi
         - name: Execute MCP Tools
           run: |
             # All MCP operations here
   
     later-operations:  # Non-MCP operations
       needs: early-mcp-operations
       steps:
         - name: Process with local tools
           run: |
             # FFmpeg, ImageMagick, etc.
   ```

#### Important Notes
- **DO NOT attempt manual reconnection during GitHub Actions** - it will interrupt the workflow
- **DO NOT rely on MCP tools after 15 minutes** of workflow runtime
- **ALWAYS have fallback methods** ready for when MCP is unavailable

### Workflow Design Best Practices

#### 1. Task Minimization
- Keep individual tasks small and focused (single responsibility)
- **Each task should complete within 5 minutes (MCP接続維持のため)**
- Split large operations into multiple smaller tasks
- This reduces failure impact and improves debuggability

#### 2. Data Sharing Considerations
- Be careful with job dependencies - each job runs on a separate machine
- Use artifacts for file sharing between jobs
- For small data (< 1KB), use GitHub Outputs
- For medium data (< 100KB), use base64 encoded outputs
- For large data (> 100KB), always use artifacts

#### 3. Video Workflow Specific Patterns
- **Add video-editing-plan unit** before final FFmpeg concatenation
- This analyzes all generated materials (video, audio, BGM)
- Creates optimal editing instructions and timing
- Ensures professional quality output

#### 4. YAML Construction Guidelines
- **Refer to docs/YAML_CONSTRUCTION_GUIDELINES.md** for detailed patterns
- NEVER use HEREDOC in GitHub Actions
- Always use echo commands for line-by-line generation
- Handle GitHub Actions variables safely

#### 5. Dependency Management
- **Refer to docs/MINIMAL_UNIT_DATA_DEPENDENCIES.md** for unit I/O specs
- Understand data flow between minimal units
- Identify parallelizable tasks
- Handle URL expiration with rolling processing

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
├── meta-workflow-executor-v12.yml   # Current meta workflow with domain templates
├── auto-fix-deployment.yml          # Automated error recovery system
├── continuous-system-monitor.yml    # System health monitoring
└── generated/                       # Generated workflow deployment area
    └── *.yml                        # Generated workflows

projects/                # ALL GitHub Actions outputs go here
├── issue-{number}-{timestamp}/      # Meta-workflow outputs (Issue-driven)
│   ├── metadata/                    # Analysis data, task decomposition
│   ├── logs/                        # Meta-workflow execution logs
│   ├── generated-workflow/          # Generated workflow file (.yml)
│   └── validation-report/           # Workflow validation results
└── {workflow-name}-{timestamp}/     # Generated workflow outputs (media files)
    ├── metadata/                    # Processing metadata
    ├── logs/                        # Execution logs
    ├── media/                       # Generated media files
    │   ├── images/                  # Generated images
    │   ├── videos/                  # Generated videos
    │   ├── audio/                   # Generated audio files
    │   └── 3d/                      # Generated 3D models
    └── final/                       # Final deliverables
```

### MCP Integration Rules
**MCP Configuration**: See `docs/MCP_CONFIGURATION_GUIDE.md` for complete service list and setup instructions.

**⚠️ CRITICAL Prerequisites**:
- MCP server (kamui-code.ai) auto-disconnects after ~15-20 minutes
- Connection will be lost during long GitHub Actions runs
- Manual reconnection interrupts workflow execution
- Must use time-based strategy, NOT reconnection attempts

**MCP Tool Usage Checklist**:
```bash
# 1. Time-based Decision (REQUIRED)
WORKFLOW_START=${{ github.run_started_at }}  # Use GitHub's timestamp
ELAPSED_MINUTES=$(( ($(date +%s) - $(date -d "$WORKFLOW_START" +%s)) / 60 ))

if [ $ELAPSED_MINUTES -lt 12 ]; then
  echo "✅ Safe to use MCP tools (${ELAPSED_MINUTES} minutes elapsed)"
  # Use MCP tools
else
  echo "⚠️ MCP timeout risk - using fallback (${ELAPSED_MINUTES} minutes elapsed)"
  # Use fallback methods - DO NOT attempt reconnection
fi

# 2. Batch MCP Operations Early (RECOMMENDED)
# Run all MCP operations in first 10 minutes
# Then switch to local processing

# 3. Fallback Ready (MANDATORY)
# Always have non-MCP alternatives:
# - FFmpeg for video/audio
# - ImageMagick for images
# - espeak-ng for TTS
```

**Key MCP Services** (from `.claude/mcp-kamuicode.json`) - 44+ services total:

#### AI Generation Services (24 services):
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

#### External API Services (20+ services):
- **YouTube**: Video upload, info retrieval
- **OpenAI**: GPT text generation, summarization, translation, image generation (gpt-image-1)
- **Slack**: Messaging, file uploads
- **Twitter/X**: Tweet posting, search
- **Google Sheets**: Read/write operations
- **GitHub**: Issues, releases, workflow dispatch, repository search
- **Discord**: Webhook messaging
- **Telegram**: Bot messaging
- **Notion**: Page creation
- **SendGrid**: Email sending
- **ElevenLabs**: Advanced TTS
- **NewsAPI**: News aggregation
- **Weather**: OpenWeatherMap integration
- **Finnhub**: Stock market data
- **arXiv**: Scientific paper search
- **Reddit**: Content search
- **Hugging Face**: Model inference
- **Anthropic**: Claude API
- **Stripe**: Payment processing

**IMPORTANT**: 
- Do NOT reference non-existent MCP services. Use the exact service names listed above.
- For external APIs, ensure API keys are set in GitHub Secrets or environment variables.
- For GitHub Actions, set environment variables: `CLAUDE_CODE_CI_MODE=true` and `CLAUDE_CODE_AUTO_APPROVE_MCP=true`

### Code Patterns to Follow

#### File Path Reference Pattern (Critical)
```bash
# Consistent file path extraction from MCP outputs
IMAGE_PATH=$(jq -r '.image_url // .file_path // "none"' "$ref_file" 2>/dev/null)
VIDEO_PATH=$(jq -r '.video_url // .file_path // "none"' "$video_file")
AUDIO_PATH=$(jq -r '.audio_url // .file_path // "none"' "$audio_file")

# IMPORTANT: Use projects/ paths for ALL GitHub Actions outputs
# For Meta-workflow (Issue-driven) - generates workflows:
mkdir -p projects/issue-${ISSUE_NUMBER}-${TIMESTAMP}/metadata
mkdir -p projects/issue-${ISSUE_NUMBER}-${TIMESTAMP}/logs
mkdir -p projects/issue-${ISSUE_NUMBER}-${TIMESTAMP}/generated-workflow
mkdir -p projects/issue-${ISSUE_NUMBER}-${TIMESTAMP}/validation-report

# For Generated workflows - produces media/artifacts:
mkdir -p projects/${WORKFLOW_NAME}-${TIMESTAMP}/metadata
mkdir -p projects/${WORKFLOW_NAME}-${TIMESTAMP}/logs
mkdir -p projects/${WORKFLOW_NAME}-${TIMESTAMP}/media/images
mkdir -p projects/${WORKFLOW_NAME}-${TIMESTAMP}/media/videos
mkdir -p projects/${WORKFLOW_NAME}-${TIMESTAMP}/media/audio
mkdir -p projects/${WORKFLOW_NAME}-${TIMESTAMP}/media/3d
mkdir -p projects/${WORKFLOW_NAME}-${TIMESTAMP}/final

# IMPORTANT: Use .github/workflows/generated/ for final workflow deployment
mkdir -p .github/workflows/generated             # For generated workflows (simple structure)

# Directory existence checks before file operations
if [ ! -d "$(dirname "$TARGET_FILE")" ]; then
  mkdir -p "$(dirname "$TARGET_FILE")"
fi
```

### 🚨 MANDATORY FILE ORGANIZATION RULES 🚨

**CRITICAL**: Follow these rules EXACTLY. No exceptions. No creativity.

#### **ALL OUTPUT MUST GO TO PROJECTS DIRECTORY**
```bash
# ✅ CORRECT - Everything goes to projects/
projects/issue-{number}-{timestamp}/     # Issue-driven outputs
projects/workflow-name-{timestamp}/      # Workflow execution outputs
projects/current-session/                # Current work session
projects/production/                     # Production deliverables
projects/archive/                        # Archived outputs
projects/workflow-execution-logs/        # Execution logs
projects/analysis/                       # Analysis results

# ❌ FORBIDDEN - Never create these in root
./production/              # NO root production directory
./test-runs/              # NO root test directory
./meta-workflow-v*/       # NO root analysis directories
./workflow-execution-logs/ # NO root log directories (use projects/)
./output/                 # NO root output directory
./downloads/              # NO root downloads directory
./artifacts/              # NO root artifacts directory
```

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

For file deletion and directory organization, see: **`docs/analysis/CLEANUP_PROTOCOL.md`**

### Workflow Generation Requirements

Each workflow must include:
- **Task dependencies and parallel groups**
- **Implementation with MCP/script/external API**
- **Validation criteria and error handling**
- **Duration estimates (5-60 minutes total)**

### Development Best Practices

#### When Working on Tasks
1. **Follow task priority guidelines** (see Task Execution Priority section)
2. **Check dependencies** before starting work
3. **Test changes** before committing
4. **Log results** in workflow-execution-logs

#### Error Handling
- **Apply repair protocols** immediately for known issues
- **Use retry logic** with exponential backoff
- **Log all errors** to `projects/workflow-execution-logs/`
- **Document solutions** for future reference

### Required Secrets & Configuration
- **`CLAUDE_CODE_OAUTH_TOKEN`**: Claude Code authentication token
- **`.claude/mcp-kamuicode.json`**: MCP configuration (AI generation services + External APIs)
- **External API Keys**: Set in GitHub Secrets
  - `YOUTUBE_API_KEY`, `OPENAI_API_KEY`, `SLACK_BOT_TOKEN`, `TWITTER_BEARER_TOKEN`
  - `GOOGLE_SHEETS_CREDENTIALS`, `GITHUB_TOKEN`, `ELEVENLABS_API_KEY`
  - `NEWSAPI_KEY`, `WEATHER_API_KEY`, `FINNHUB_API_KEY`
  - And more as needed for each external service

### Execution Methods
1. **Issue-driven**: Create issues using workflow-request.yml template
2. **Manual**: Use `workflow_dispatch` trigger with parameters
3. **Simple deployment**: Automatic quality assurance → direct deployment to `.github/workflows/generated/`

## Development Philosophy

- **Priority-Driven Development**: Follow task priority guidelines for efficient execution
- **Quality over Speed**: Test before deployment, log all results
- **MCP-First**: Use AI generation services as primary tools
- **Graceful Degradation**: Handle failures with fallback strategies
- **Safe Deployment**: Validate workflows before production

## Custom Node Examples

When existing minimal units cannot handle specific requirements, see:
**📂 `docs/examples/custom-nodes/`** for extension patterns

## 🚨 System Development Rules for Claude Code

### 1. Workflow Execution Logs
**Always log workflow execution issues and solutions**:
- Location: `projects/workflow-execution-logs/`
- Format: `execution-log-YYYY-MM-DD.md`
- Log immediately when issues occur
- Include: timestamp, workflow name, issue, action taken, result

Example:
```
### [15:25:00] [START] test-websearch-simple.yml
Issue: Need to verify WebSearch actually works
Action: Created minimal test with just WebSearch query
Result: Success in 1m3s
```

### 2. Commit and Push Frequently
- **Commit after completing each task**
- **Push immediately after commit**
- Don't wait to batch multiple changes
- Continue working locally without interruption

### 3. Error Tracking Pattern
```bash
# In workflow logs
echo "[$(date +%Y-%m-%d_%H:%M:%S)] ERROR: $ERROR_MESSAGE" >> error.log
echo "[$(date +%Y-%m-%d_%H:%M:%S)] SOLUTION: $SOLUTION" >> error.log
echo "[$(date +%Y-%m-%d_%H:%M:%S)] RESULT: $RESULT" >> error.log
```

### 4. Known Issues to Track
- Meta-workflow generates `uses: ./minimal-units/...` which doesn't work in GitHub Actions
- Need to inline minimal unit implementations
- Complex JSON in envsubst causes task decomposition failures
- WebSearch execution takes 1-2 minutes for simple queries

### 5. Script Management Policy
**CRITICAL**: Before creating any new script, follow the Script Management Policy:
- **Policy Location**: `scripts/SCRIPT_MANAGEMENT_POLICY.md`
- **Key Rule**: "Enhance existing scripts rather than creating new ones"
- Always search existing scripts first, extend rather than duplicate

### 6. 📦 GitHub Actions Artifact Download Rules

**🚨 MANDATORY**: Never download artifacts to root directory - files will scatter!

#### ✅ Correct Method (Use Existing Script)
```bash
# Use the dedicated organized download script
./scripts/download-workflow-artifacts.sh <run-id>

# Or specify custom output directory
./scripts/download-workflow-artifacts.sh -o projects/issue-66-analysis <run-id>
```

#### ❌ NEVER Use Manual Download in Root
```bash
# This scatters files everywhere - FORBIDDEN
gh run download <run-id>
```

#### 🔧 Manual Download (If Script Unavailable)
```bash
# Create project directory first
mkdir -p projects/issue-{number}-run-{run-id}
cd projects/issue-{number}-run-{run-id}
gh run download {run-id}
```

**Result Structure**:
```
projects/issue-{number}-{timestamp}/
├── generated-workflow/
├── metadata/           # domain templates
├── analysis/          # task decomposition  
└── artifacts/         # other files
```