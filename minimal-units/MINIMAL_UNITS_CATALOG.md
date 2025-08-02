# Minimal Units Catalog

Comprehensive catalog of minimal units. The meta-workflow system references this catalog to dynamically construct workflows.

**Total Units: 81**

## Categories and Units

### 🎨 Media Production

#### 🖼️ Image Generation (5 units)
- **t2i-imagen3**: High-quality image generation with Google Imagen3 (minimal-units/media/image/t2i-imagen3.yml)
- **image-t2i**: ✅ Generic Text-to-Image with quality settings (v8 updated) (minimal-units/media/image/image-t2i.yml)
- **t2i-sdxl**: Image generation with Stable Diffusion XL (minimal-units/media/image/t2i-sdxl.yml)
- **i2i-flux-kontext**: Image transformation with Flux Kontext (minimal-units/media/image/i2i-flux-kontext.yml)
- **image-analysis**: Image content analysis (minimal-units/media/image/image-analysis.yml)

#### 🎬 Video Generation (7 units)
- **video-generation**: ✅ Generic video generation with quality settings (v8 updated) (minimal-units/media/video/video-generation.yml)
- **t2v-veo3**: Text-to-Video with Google Veo3 (minimal-units/media/video/t2v-veo3.yml)
- **t2v-wan**: Text-to-Video with Wan V2 (minimal-units/media/video/t2v-wan.yml)
- **i2v-seedance**: Image-to-Video with SeeDance (minimal-units/media/video/i2v-seedance.yml)
- **r2v-vidu**: Reference-to-Video generation (minimal-units/media/video/r2v-vidu.yml)
- **video-analysis**: Video content analysis (minimal-units/media/video/video-analysis.yml)
- **video-prompt-opt**: Video prompt optimization (minimal-units/media/video/video-prompt-opt.yml)

#### 🎵 Audio Generation (10 units)
- **bgm-generate**: BGM generation (simulation version) (minimal-units/media/audio/bgm-generate.yml)
- **bgm-generate-mcp**: ✅ BGM generation (MCP version with lyria_generate fixed) (minimal-units/media/audio/bgm-generate-mcp.yml)
- **t2s-google**: Google Text-to-Speech (minimal-units/media/audio/t2s-google.yml)
- **t2s-minimax-turbo**: MiniMax Turbo TTS (simulation version) (minimal-units/media/audio/t2s-minimax-turbo.yml)
- **t2s-minimax-turbo-mcp**: ✅ MiniMax Turbo TTS (MCP version implemented) (minimal-units/media/audio/t2s-minimax-turbo-mcp.yml)
- **t2s-minimax-voice**: MiniMax Voice Design (minimal-units/media/audio/t2s-minimax-voice.yml)
- **t2s-openai**: OpenAI Text-to-Speech (minimal-units/media/audio/t2s-openai.yml)
- **audio-elevenlabs**: ElevenLabs voice generation (minimal-units/media/audio/audio-elevenlabs.yml)
- **audio-minimax**: MiniMax voice generation (minimal-units/media/audio/audio-minimax.yml)
- **wav-segmentation**: Audio file segmentation (minimal-units/media/audio/wav-segmentation.yml)

#### 🏷️ Banner Design (1 unit)
- **banner-text**: Add text to banner image with design implementation (minimal-units/media/banner/banner-text.yml)

#### 🎭 3D Generation (1 unit)
- **i2i3d-hunyuan**: Image-to-3D with Hunyuan (minimal-units/media/3d/i2i3d-hunyuan.yml)

### 📋 Planning & Analysis (7 units)
- **planning-ccsdk**: Planning with Claude Code SDK (minimal-units/planning/planning-ccsdk.yml)
- **banner-planning**: Banner planning (minimal-units/planning/banner-planning.yml)
- **news-planning**: News planning (minimal-units/planning/news-planning.yml)
- **web-search-claude**: ✅ Web search using Claude Code WebSearch tool (minimal-units/planning/web-search-claude.yml)
- **web-search-gemini**: Web search using Gemini API (minimal-units/planning/web-search-gemini.yml)
- **data-analysis**: Data analysis (minimal-units/planning/data-analysis.yml)
- **data-visualization**: Data visualization (minimal-units/planning/data-visualization.yml)

### 📰 Content Creation (5 units)
- **blog-generation**: Blog article generation (minimal-units/content/blog-generation.yml)
- **article-generation**: Article generation (minimal-units/content/article-generation.yml)
- **news-summary**: News summarization (minimal-units/content/news-summary.yml)
- **slide-generation**: Presentation generation (minimal-units/content/slide-generation.yml)
- **markdown-summary**: Markdown summary generation (minimal-units/content/markdown-summary.yml)

### ⚡ Post-Production (12 units)
- **lipsync-pixverse**: Pixverse lip sync (minimal-units/postprod/lipsync-pixverse.yml)
- **pixverse-quota-guard**: Pixverse quota management (minimal-units/postprod/pixverse-quota-guard.yml)
- **srt-make**: SRT file generation (minimal-units/postprod/srt-make.yml)
- **srt-sync**: SRT synchronization adjustment (minimal-units/postprod/srt-sync.yml)
- **srt-translate**: SRT translation (minimal-units/postprod/srt-translate.yml)
- **subtitle-overlay**: Subtitle overlay (minimal-units/postprod/subtitle-overlay.yml)
- **video-concat**: ✅ Multiple video concatenation with narration support (v8 updated) (minimal-units/postprod/video-concat.yml)
- **title-composition**: Title frame composition (minimal-units/postprod/title-composition.yml)
- **upscale-topaz**: Video upscaling with Topaz (minimal-units/postprod/upscale-topaz.yml)
- **v2v-luma-ray2**: Video transformation with Luma Ray2 (minimal-units/postprod/v2v-luma-ray2.yml)
- **v2v-creatify**: Video editing with Creatify (minimal-units/postprod/v2v-creatify.yml)
- **bgm-overlay**: BGM overlay (minimal-units/postprod/bgm-overlay.yml)

### 🛠️ Utility & Integration (7 units)
- **local-save**: Local file saving (minimal-units/utility/local-save.yml)
- **fal-upload**: FAL upload (minimal-units/utility/fal-upload.yml)
- **git-branch-setup**: Git branch setup (minimal-units/git-ops/git-branch-setup.yml)
- **git-pr-create**: Pull request creation (minimal-units/external/git-pr-create.yml)
- **cleanup-branch**: Branch cleanup (minimal-units/git-ops/cleanup-branch.yml)
- **pdf-create**: PDF creation (minimal-units/external/pdf-create.yml)
- **sns-publish**: SNS publishing (minimal-units/external/sns-publish.yml)

### 🌐 External APIs (27 units) [FINAL UPDATE]
#### YouTube API
- **youtube-upload**: YouTube video upload (minimal-units/external/youtube-upload.yml)
- **youtube-video-info**: YouTube video info retrieval (minimal-units/external/youtube-video-info.yml) ⭐NEW

#### News & Weather APIs
- **newsapi-fetch**: NewsAPI article fetch (minimal-units/external/newsapi-fetch.yml)
- **weather-fetch**: OpenWeatherMap weather data (minimal-units/external/weather-fetch.yml)

#### Communication APIs
- **slack-notify**: Slack notification (minimal-units/external/slack-notify.yml)
- **slack-file-upload**: Slack file upload (minimal-units/external/slack-file-upload.yml) ⭐NEW
- **discord-webhook**: Discord Webhook notification (minimal-units/external/discord-webhook.yml) ⭐NEW
- **telegram-send-message**: Telegram message send (minimal-units/external/telegram-send-message.yml) ⭐NEW
- **sendgrid-send-email**: SendGrid email send (minimal-units/external/sendgrid-send-email.yml) ⭐NEW

#### AI & ML APIs
- **openai-gpt**: OpenAI GPT text generation (minimal-units/external/openai-gpt.yml)
- **openai-summarize**: OpenAI summarization (minimal-units/external/openai-summarize.yml) ⭐NEW
- **openai-translate**: OpenAI translation (minimal-units/external/openai-translate.yml) ⭐NEW
- **openai-image-gen**: OpenAI image generation (gpt-image-1) (minimal-units/external/openai-image-gen.yml) ⭐NEW
- **elevenlabs-tts**: ElevenLabs text-to-speech (minimal-units/external/elevenlabs-tts.yml)
- **huggingface-inference**: Hugging Face model inference (minimal-units/external/huggingface-inference.yml) ⭐NEW

#### Data & Analytics APIs
- **google-sheets-write**: Google Sheets data write (minimal-units/external/google-sheets-write.yml)
- **google-sheets-read**: Google Sheets data read (minimal-units/external/google-sheets-read.yml) ⭐NEW
- **finnhub-stock-quote**: Finnhub stock quote fetch (minimal-units/external/finnhub-stock-quote.yml) ⭐NEW

#### Social Media APIs
- **twitter-post**: Twitter/X post (minimal-units/external/twitter-post.yml)
- **twitter-search**: Twitter/X search (minimal-units/external/twitter-search.yml) ⭐NEW
- **reddit-search**: Reddit post search (minimal-units/external/reddit-search.yml) ⭐NEW

#### Development APIs
- **github-issue-create**: GitHub Issue creation (minimal-units/external/github-issue-create.yml) ⭐NEW
- **github-repo-search**: GitHub repository search (minimal-units/external/github-repo-search.yml) ⭐NEW
- **github-workflow-dispatch**: GitHub Workflow dispatch (minimal-units/external/github-workflow-dispatch.yml) ⭐NEW
- **github-release-create**: GitHub Release creation (minimal-units/external/github-release-create.yml) ⭐NEW
- **arxiv-search**: arXiv paper search (minimal-units/external/arxiv-search.yml) ⭐NEW
- **notion-create-page**: Notion page creation (minimal-units/external/notion-create-page.yml) ⭐NEW

### 🎬 Workflow Compositions (1 unit)
- **video-production-workflow**: ✅ Integrated video production workflow (v8 success pattern) (minimal-units/workflows/video-production-workflow.yml)

## Usage Guidelines

### 1. Unit Selection
The meta-workflow selects units based on:
- **Task requirements**: User's desired outcome
- **Dependencies**: Required pre/post processing
- **Parallelization**: Tasks that can run concurrently
- **Quality requirements**: Desired quality level

### 2. Dynamic Composition
- **Serial placement**: When dependencies exist
- **Parallel placement**: For independent tasks
- **Conditional branching**: Result-based processing
- **Loop processing**: Multiple item processing

### 3. Unit Extension
When new units are needed:
1. Consider if existing unit combinations suffice
2. Determine necessity for new unit creation
3. Create following interface specifications
4. Add to catalog

## Metadata Structure

Each unit has the following metadata:
```yaml
name: unit-name
description: Unit description
category: category
inputs:
  - name: input_name
    type: string/number/boolean
    required: true/false
outputs:
  - name: output_name
    type: string/number/boolean
dependencies:
  - other-unit-name
parallel_safe: true/false
estimated_time: "1-5 minutes"
```

## Integration with Meta Workflow

The meta-workflow system:
1. Loads this catalog
2. Analyzes tasks with Claude Code SDK
3. Selects and places required units
4. Dynamically generates workflows

## Related Documentation

- **Unit Creation Guide**: `docs/MINIMAL_UNIT_CREATION_GUIDE.md`
- **Interface Specifications**: `docs/UNIT_INTERFACE_SPEC.md`
- **Usage Patterns**: `docs/external-api-usage-patterns.md`

---
Updated: 2025-08-02