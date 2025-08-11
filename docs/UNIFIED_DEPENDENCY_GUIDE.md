# Unified Dependency Guide - For AI Generation Systems

This document provides comprehensive dependency relationships for all components (minimal units, modules, orchestrators) used in the meta-workflow system.

## 📋 Table of Contents

1. [System Hierarchy](#system-hierarchy)
2. [Dependency Matrix](#dependency-matrix)
3. [Execution Order Rules](#execution-order-rules)
4. [Typical Flow Patterns](#typical-flow-patterns)
5. [AI System Quick Reference](#ai-system-quick-reference)
6. [Claude Code Execution Patterns](#claude-code-execution-patterns)

## 🚨 Critical Implementation Requirements

### Claude Code Data Persistence Pattern (MANDATORY)

**Problem**: Claude Code executes MCP tools successfully but doesn't save files locally, resulting in placeholder files.

**Solution**: Always provide explicit save instructions with these components:
1. **Explicit save path**: `${PROJECT_DIR}/media/...` format
2. **URL file creation**: Save Google Cloud Storage URLs to `*-url.txt`
3. **Verification command**: Execute `ls -la` after generation
4. **Immediate download**: Use `curl -L -o` for URL files
5. **Multi-pattern search**: At least 3 search patterns for file retrieval

**Reference Implementation**: See `docs/CLAUDE_CODE_DATA_PERSISTENCE_GUIDE.md` and `meta/examples/claude-code-t2i-correct-pattern.yml`

## System Hierarchy

```
Orchestrator (Complete Workflow)
├── Module (Function Group)
│   └── Minimal Unit (Minimum Function)
└── Direct Execution Minimal Unit
```

### Layer Description
- **Minimal Unit**: Single function (80 units) - Latest structure: `minimal-units/[category]/[unit].yml`
- **Module**: Related unit combination (`kamuicode-workflow/module-workflow/module-*.yml`)
- **Orchestrator**: Complete workflow (`kamuicode-workflow/module-workflow/orchestrator-*.yml`)

## Dependency Matrix

### 🚦 Phase-Based Dependencies

| Phase | Required Prerequisites | Next Phase | Parallelizable |
|-------|----------------------|------------|----------------|
| **Setup** | None | Planning | ❌ |
| **Planning** | Setup completed | Production | ✅ (Multiple plans in parallel) |
| **Production** | Planning completed | Post-Production | ✅ (Image/Audio/Video in parallel) |
| **Post-Production** | Production completed | Delivery | ✅ (Subtitle/Effects in parallel) |
| **Delivery** | Post-Production completed | None | ✅ (Upload/PR in parallel) |

### 📁 Category-Based Dependencies

#### 🔧 Setup & Workflow Management
```yaml
Required execution order:
  1. git-branch-setup     # minimal-units/git-ops/git-branch-setup.yml
  2. [Main processing]
  3. git-pr-create       # minimal-units/external/git-pr-create.yml
  
Module references:
  - module-setup-branch.yml
  - module-create-pr.yml
```

#### 📋 Planning Phase
```yaml
Parallel executable:
  - planning-ccsdk        # minimal-units/planning/planning-ccsdk.yml
  - banner-planning       # minimal-units/planning/banner-planning.yml
  - news-planning         # minimal-units/planning/news-planning.yml
  - web-search           # minimal-units/planning/web-search.yml
  - data-analysis        # minimal-units/planning/data-analysis.yml
  - data-visualization   # minimal-units/planning/data-visualization.yml

Module references:
  - module-planning-ccsdk.yml
  - module-banner-planning-ccsdk.yml
  - module-news-planning-ccsdk.yml
  - module-web-search.yml
```

#### 🎨 Media Production Phase
```yaml
Image generation (5 units - parallelizable):
  dependencies: [planning completed]
  units:
    - t2i-imagen3         # minimal-units/media/image/t2i-imagen3.yml
    - image-t2i           # minimal-units/media/image/image-t2i.yml
    - t2i-sdxl            # minimal-units/media/image/t2i-sdxl.yml
    - i2i-flux-kontext    # minimal-units/media/image/i2i-flux-kontext.yml
  analysis:
    - image-analysis      # minimal-units/media/image/image-analysis.yml
  
Video generation (7 units):  
  dependencies: [image generation completed (optional)]
  units:
    - video-generation    # minimal-units/media/video/video-generation.yml
    - t2v-veo3           # minimal-units/media/video/t2v-veo3.yml
    - t2v-wan            # minimal-units/media/video/t2v-wan.yml
    - i2v-seedance       # minimal-units/media/video/i2v-seedance.yml
    - r2v-vidu           # minimal-units/media/video/r2v-vidu.yml
  analysis:
    - video-analysis     # minimal-units/media/video/video-analysis.yml
    - video-prompt-opt   # minimal-units/media/video/video-prompt-opt.yml

Audio generation (10 units - parallelizable):
  dependencies: [planning completed]
  units:
    - bgm-generate       # minimal-units/media/audio/bgm-generate.yml
    - bgm-generate-mcp   # minimal-units/media/audio/bgm-generate-mcp.yml
    - t2s-google         # minimal-units/media/audio/t2s-google.yml
    - t2s-minimax-turbo  # minimal-units/media/audio/t2s-minimax-turbo.yml
    - t2s-minimax-turbo-mcp  # minimal-units/media/audio/t2s-minimax-turbo-mcp.yml
    - t2s-minimax-voice  # minimal-units/media/audio/t2s-minimax-voice.yml
    - t2s-openai         # minimal-units/media/audio/t2s-openai.yml
    - audio-elevenlabs   # minimal-units/media/audio/audio-elevenlabs.yml
    - audio-minimax      # minimal-units/media/audio/audio-minimax.yml
    - wav-segmentation   # minimal-units/media/audio/wav-segmentation.yml

Banner design (1 unit):
  dependencies: [banner-planning completed]
  units:
    - banner-text        # minimal-units/media/banner/banner-text.yml

3D generation (1 unit):
  dependencies: [image generation completed]
  units:
    - i2i3d-hunyuan     # minimal-units/media/3d/i2i3d-hunyuan.yml

Module references:
  - module-image-generation-kc-*.yml
  - module-video-generation-kc-*.yml
  - module-audio-generation-kc-*.yml
  - module-banner-text-overlay-kc-*.yml
```

#### 📰 Content Creation Phase
```yaml
Parallel executable:
  dependencies: [planning completed, web-search completed (optional)]
  units:
    - blog-generation     # minimal-units/content/blog-generation.yml
    - article-generation  # minimal-units/content/article-generation.yml
    - news-summary        # minimal-units/content/news-summary.yml
    - slide-generation    # minimal-units/content/slide-generation.yml
    - markdown-summary    # minimal-units/content/markdown-summary.yml

Module references:
  - module-article-creation-ccsdk.yml
```

#### ⚡ Post-Production Phase
```yaml
Subtitle & Lipsync (6 units):
  dependencies: [audio generation completed, video generation completed]
  sequential_required:
    - pixverse-quota-guard  # minimal-units/postprod/pixverse-quota-guard.yml
    - lipsync-pixverse      # minimal-units/postprod/lipsync-pixverse.yml
  parallel_possible:
    - srt-make             # minimal-units/postprod/srt-make.yml
    - srt-sync             # minimal-units/postprod/srt-sync.yml
    - srt-translate        # minimal-units/postprod/srt-translate.yml
    - subtitle-overlay     # minimal-units/postprod/subtitle-overlay.yml

Integration & Enhancement (6 units):
  dependencies: [media generation completed]
  units:
    - video-concat         # minimal-units/postprod/video-concat.yml
    - title-composition    # minimal-units/postprod/title-composition.yml
    - upscale-topaz        # minimal-units/postprod/upscale-topaz.yml
    - v2v-luma-ray2        # minimal-units/postprod/v2v-luma-ray2.yml
    - v2v-creatify         # minimal-units/postprod/v2v-creatify.yml
    - bgm-overlay          # minimal-units/postprod/bgm-overlay.yml

Module references:
  - module-lipsync-generation-kc-*.yml
  - module-subtitle-overlay-ffmpeg-ccsdk.yml
  - module-video-concatenation-ffmpeg-ccsdk.yml
```

#### 🛠️ Utility & Integration Phase
```yaml
Storage (2 units):
  dependencies: [file generation completed]
  units:
    - local-save          # minimal-units/utility/local-save.yml
    - fal-upload          # minimal-units/utility/fal-upload.yml

External integration (30 units):
  dependencies: [content completed]
  core units:
    - pdf-create          # minimal-units/external/pdf-create.yml
    - sns-publish         # minimal-units/external/sns-publish.yml
    - git-pr-create       # minimal-units/external/git-pr-create.yml
  api units:
    - youtube-upload      # minimal-units/external/youtube-upload.yml
    - newsapi-fetch       # minimal-units/external/newsapi-fetch.yml
    - slack-notify        # minimal-units/external/slack-notify.yml
    - openai-gpt          # minimal-units/external/openai-gpt.yml
    # ... and 23 more external API units

Git operations (2 units):
  git-branch-setup:       # minimal-units/git-ops/git-branch-setup.yml
    - position: workflow start
  cleanup-branch:         # minimal-units/git-ops/cleanup-branch.yml
    - position: workflow end (optional)

Module references:
  - module-upload-fal-ccsdk.yml
```

## Execution Order Rules

### 🚦 Required Execution Order
```yaml
# Basic flow
1. git-branch-setup
2. planning-* (parallelizable)
3. media-production-* (parallelizable, after planning)
4. content-creation-* (parallelizable, after planning)
5. post-production-* (after media/content)
6. utility-* (after file completion)
7. git-pr-create

# Special dependencies
pixverse series:
  pixverse-quota-guard → lipsync-pixverse

Analysis series:
  *-generation → *-analysis

Subtitle series:
  srt-make → srt-sync → srt-translate → subtitle-overlay

Enhancement series:
  video-generation → upscale-topaz
  video-generation → v2v-luma-ray2
  video-generation → v2v-creatify
```

### ⚡ Recommended Parallel Execution
```yaml
# Planning phase
planning-ccsdk || banner-planning || news-planning || web-search

# Production phase  
image-generation || audio-generation || bgm-generation

# Post-processing phase
srt-make || srt-sync || title-composition

# Delivery phase
fal-upload || sns-publish
```

## Typical Flow Patterns

### Pattern 1: Simple Video Production
```yaml
Reference orchestrator: orchestrator-video-generation.yml
flow:
  setup: git-branch-setup
  planning: planning-ccsdk
  production: image-t2i → video-generation
  delivery: fal-upload → git-pr-create
  
duration: 15-20 minutes
units_used: 4 units
```

### Pattern 2: Lipsync Video Production
```yaml
Reference orchestrator: orchestrator-v2v-pixverse-lipsync-single.yml
flow:
  setup: git-branch-setup
  planning: planning-ccsdk
  production: image-t2i → audio-minimax
  postprod: pixverse-quota-guard → lipsync-pixverse → subtitle-overlay
  delivery: fal-upload → git-pr-create
  
duration: 25-30 minutes
units_used: 8 units
```

### Pattern 3: Multimedia Campaign
```yaml
Reference orchestrator: orchestrator-banner-advertisement-creation.yml
flow:
  setup: git-branch-setup
  planning: banner-planning || news-planning
  production: 
    - t2i-imagen3 || audio-generation || video-generation
  postprod: banner-text || subtitle-overlay || video-concat
  content: blog-generation || markdown-summary
  delivery: fal-upload || sns-publish || git-pr-create
  
duration: 45-60 minutes
units_used: 15-20 units
```

### Pattern 4: News Video Production
```yaml
Reference orchestrator: orchestrator-news-video-generation.yml
flow:
  setup: git-branch-setup
  research: web-search → news-summary → news-planning
  production: t2v-veo3 || t2s-google || bgm-generate
  postprod: bgm-overlay → title-composition → video-concat
  content: article-generation → markdown-summary
  delivery: fal-upload → sns-publish → git-pr-create
  
duration: 35-45 minutes
units_used: 12-15 units
```

## AI Generation System Quick Reference

### 🎯 Unit Selection Guidelines

```yaml
Purpose-based recommended units:
  Image-focused: t2i-imagen3, i2i-flux-kontext, image-analysis
  Video-focused: video-generation, t2v-veo3, upscale-topaz
  Audio-focused: t2s-minimax-voice, bgm-generate-mcp, bgm-overlay
  Content-focused: article-generation, blog-generation, markdown-summary
  Speed-focused: image-t2i, t2v-wan, t2s-google
  Quality-focused: t2i-imagen3, t2v-veo3, audio-elevenlabs
  
Quality levels:
  Economy: t2s-google, image-t2i, basic-concat
  Standard: t2i-sdxl, video-generation, bgm-generate
  Premium: t2i-imagen3, t2v-veo3, audio-elevenlabs
```

### 🚀 Automatic Selection Rules

```yaml
IF request_type == "video":
  required: [git-branch-setup, planning-ccsdk, video-generation, git-pr-create]
  optional: [image-*, audio-*, *-analysis, upscale-*]
  
IF request_type == "banner":
  required: [git-branch-setup, banner-planning, banner-text, git-pr-create]
  optional: [image-analysis, fal-upload]
  
IF request_type == "news":
  required: [git-branch-setup, web-search, news-planning, news-summary, git-pr-create]
  optional: [video-generation, audio-*, sns-publish]

IF request_type == "campaign":
  required: [git-branch-setup, planning-ccsdk, git-pr-create]
  recommended_parallel: [image-*, video-*, audio-*, content-*]
  optional: [sns-publish, pdf-create]
```

### 📊 Resource Usage Prediction

```yaml
Lightweight workflow (within 10 minutes):
  units: 3-5 units
  pattern: planning → single-generation → upload
  example: banner-planning → banner-text → fal-upload

Medium workflow (20-30 minutes):
  units: 6-10 units  
  pattern: planning → parallel-generation → postprod → upload
  example: planning → (image + audio) → lipsync → upload

Heavy workflow (45+ minutes):
  units: 12-20 units
  pattern: multi-planning → multi-generation → complex-postprod → multi-delivery
  example: (planning + research) → (image + video + audio) → (edit + enhance) → (upload + social)
```

### 🔄 Error Handling Guidelines

```yaml
Required checkpoints:
  - pixverse-quota-guard: Required before lipsync
  - *-analysis: Quality check after generation
  - fal-upload: Confirm success before next step

Fallback strategies:
  t2i-imagen3 failure → t2i-sdxl → image-t2i
  lipsync-pixverse failure → subtitle-overlay only
  bgm-generate failure → continue without audio generation

Retry recommended:
  - Network-based: web-search, fal-upload
  - AI generation: image-*, video-*, audio-*
  - Analysis: *-analysis

Skippable:
  - Quality enhancement: upscale-*, v2v-*
  - Decoration: title-composition, bgm-overlay
  - External integration: sns-publish, pdf-create
```

## Claude Code Execution Patterns

### 🚨 Mandatory Pattern for T2I (Text-to-Image)

```yaml
- name: Generate Image
  run: |
    # MANDATORY: Define explicit paths
    SAVE_PATH="${PROJECT_DIR}/media/images/scene${N}.png"
    URL_PATH="${PROJECT_DIR}/media/images/scene${N}-url.txt"
    
    # MANDATORY: Detailed instruction prompt
    PROMPT="手順:
    1. MCPツール mcp__t2i-* で画像生成
    2. Writeツールで ${SAVE_PATH} に保存
    3. URLを ${URL_PATH} に保存
    4. ls -la で確認"
    
    # MANDATORY: Include Write and Bash tools
    npx @anthropic-ai/claude-code \
      --mcp-config ".claude/mcp-kamuicode.json" \
      --allowedTools "mcp__t2i-*,Write,Bash" \
      --permission-mode "bypassPermissions" \
      -p "$PROMPT"
    
    # MANDATORY: Immediate verification and download
    ls -la "${PROJECT_DIR}/media/images/"
    [ -f "$URL_PATH" ] && curl -L -o "$SAVE_PATH" "$(cat $URL_PATH)"
    
    # MANDATORY: Multi-pattern search (3+ patterns)
    IMAGE=$(find "$PROJECT_DIR" -name "*scene*${N}*.png" | head -1)
    [ -z "$IMAGE" ] && IMAGE=$(find "$PROJECT_DIR" -name "*.png" -mmin -2 | head -1)
    [ -z "$IMAGE" ] && IMAGE=$(find "$PROJECT_DIR" -name "*.png" | head -1)
```

### 🚨 Mandatory Pattern for I2V (Image-to-Video)

```yaml
- name: Convert to Video
  run: |
    # Check for both URL and local path
    URL_FILE="${PROJECT_DIR}/media/images/scene${N}-url.txt"
    LOCAL_IMAGE="${PROJECT_DIR}/media/images/scene${N}.png"
    
    # Prioritize valid URL over local path
    if [ -f "$URL_FILE" ]; then
      IMAGE_URL=$(cat "$URL_FILE")
      if curl -IfsS --max-time 5 "$IMAGE_URL" >/dev/null 2>&1; then
        IMAGE_REF="$IMAGE_URL"
      else
        IMAGE_REF="$LOCAL_IMAGE"
      fi
    else
      IMAGE_REF="$LOCAL_IMAGE"
    fi
    
    # Explicit save path in prompt
    VIDEO_PATH="${PROJECT_DIR}/media/videos/scene${N}.mp4"
    PROMPT="Convert image to video:
    Input: ${IMAGE_REF}
    Output: ${VIDEO_PATH}
    Duration: 6-8s"
    
    npx @anthropic-ai/claude-code \
      --allowedTools "mcp__i2v-*,Write,Bash" \
      --max-turns 80 \
      -p "$PROMPT"
```

### ❌ Common Failures to Avoid

1. **Ambiguous save instructions**: Never use vague prompts like "生成してください"
2. **Missing Write tool**: Always include "Write" in --allowedTools
3. **Single search pattern**: Always use 3+ search patterns
4. **Ignoring URL expiration**: Always check URL validity before use
5. **Creating placeholders too early**: Exhaust all search options first

### ✅ Success Criteria

- File size > 10KB for images, > 300KB for videos
- Proper format validation with ffprobe/file command
- URL downloaded within 15 minutes of generation
- No placeholder files in final output

---

**By using this guide, AI systems can understand appropriate dependencies and automatically generate efficient and reliable workflows.**

**Last updated**: 2025-08-11  
**Compatible version**: v12.0 (Minimal unit based + External API integration + Claude Code patterns)  
**Integrated sources**: DEPENDENCY_MAP.md + WORKFLOW_PATTERNS.md + kamuicode-workflow/README.md + CLAUDE_CODE_DATA_PERSISTENCE_GUIDE.md