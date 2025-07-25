# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

This is a **Meta Workflow Generator System (Kamui Rossy)** built with Claude Code GitHub Actions integration. The system uses **template-based generation** with **staged deployment system** to generate high-quality, executable GitHub Actions workflows efficiently.

## Current Architecture (v3)

### Template-Based Meta Workflow System
- **Template Selection**: Uses 9 reference workflows in `meta/examples/` instead of complex task decomposition
- **Staged Deployment**: 3-stage quality assurance (staging → validation → production)
- **Prompt Separation**: All prompts managed as external files in `meta/prompts/`
- **Small Nodes**: Each job has single responsibility with independent re-execution capability
- **Quality Validation**: YAML syntax, GitHub Actions structure, MCP references, dependencies check

### Core Components
- **`meta/examples/`**: 9 detailed reference workflow templates with ultra-detailed task breakdown
- **`.github/workflows/kamuicode-meta-generator.yml`**: Main meta workflow (updated)
- **`.github/ISSUE_TEMPLATE/`**: Issue templates for workflow requests
- **`meta/prompts/`**: Prompt files for task decomposition, workflow generation, script generation, documentation
- **Generated outputs**: Validated workflows, scripts, documentation with staged deployment

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
└── kamuicode-meta-generator.yml  # Main workflow with staged deployment
```

### MCP Integration Rules
**Available MCP Services** (from `~/.claude/mcp-kamuicode.json`):
- **T2I**: `t2i-google-imagen3`, `t2i-fal-imagen4-ultra`, `t2i-fal-imagen4-fast`
- **T2V**: `t2v-fal-veo3-fast`
- **I2V**: `i2v-fal-hailuo-02-pro`
- **T2M**: `t2m-google-lyria`
- **V2A**: `v2a-fal-metavoice-v1`
- **V2V**: `v2v-fal-cogvideo-1_5`
- **I2I3D**: `i2i3d-fal-hunyuan3d-v21`

**IMPORTANT**: Do NOT reference non-existent MCP services (e.g., `web-search`, `rss-parser`, `generic kamuicode`). Use external API calls instead.

### Code Patterns to Follow

#### File Path Reference Pattern (Critical)
```bash
# Consistent file path extraction from MCP outputs
IMAGE_PATH=$(jq -r '.image_url // .file_path // "none"' "$ref_file" 2>/dev/null)
VIDEO_PATH=$(jq -r '.video_url // .file_path // "none"' "$video_file")
AUDIO_PATH=$(jq -r '.audio_url // .file_path // "none"' "$audio_file")
```

#### Ultra-Detailed Task Breakdown
Each workflow must include:
- **Human unconscious thought process simulation**
- **GitHub Actions node design**
- **Task dependencies and parallel groups**
- **Implementation details with MCP/script/external API**
- **Validation criteria and error handling**
- **Duration estimates (5-60 minutes total)**

#### Staged Deployment Implementation
The main workflow now uses:
1. **Template Selection** → `generated/workflows/staging/`
2. **Validation** → YAML syntax, GitHub Actions structure, MCP references, dependencies
3. **Production Deployment** → `.github/workflows/` (only if validation passes)

### Development Best Practices

#### When Adding New Workflows
1. **Use existing templates** as base structure
2. **Follow ultra-detailed task breakdown pattern**
3. **Include proper MCP service integration**
4. **Add file path reference patterns**
5. **Update `meta/examples/README.md`** with Mermaid diagram

#### When Modifying Main Workflow
- **Maintain staged deployment system**
- **Keep validation scoring system (75+ points for pass)**
- **Preserve template selection logic**
- **Maintain artifact upload/download patterns**

#### Error Handling
- **External API fallbacks** for missing MCP services
- **Retry logic** with exponential backoff
- **Comprehensive logging** to `.logs/` directories
- **Graceful degradation** strategies

### Required Secrets & Configuration
- **`CLAUDE_CODE_OAUTH_TOKEN`**: Claude Code authentication token
- **`~/.claude/mcp-kamuicode.json`**: MCP configuration (AI generation services only)

### Execution Methods
1. **Issue-driven**: Create issues using workflow-request.yml template
2. **Manual**: Use `workflow_dispatch` trigger with parameters
3. **Staged validation**: Automatic quality assurance before production deployment

## Development Philosophy

- **Quality over Speed**: Use staged deployment for reliability
- **Template-based Efficiency**: Leverage existing patterns instead of generating from scratch  
- **MCP-First**: Integrate AI generation services as primary tools
- **External API Fallback**: Handle missing services gracefully
- **Ultra-detailed Decomposition**: Break down to AI/script/MCP executable granularity
- **Parallel Execution**: Optimize performance with dependency management

## Notes for Claude Code Sessions

- **This system is actively developed using Claude Code** - maintain development continuity
- **All examples in `meta/examples/` represent production-ready templates**
- **The main workflow uses template selection instead of complex task decomposition**
- **Staged deployment prevents broken workflows from reaching production**
- **File path reference patterns are critical for workflow continuity**
- **MCP services are limited to AI generation - use external APIs for other functions**