# 統合依存関係ガイド - AI生成システム向け

このドキュメントは、メタワークフローシステムで使用するすべてのコンポーネント（ミニマルユニット、モジュール、オーケストレーター）の依存関係を統合的に説明します。

## 📋 目次

1. [システム階層構造](#システム階層構造)
2. [依存関係マトリックス](#依存関係マトリックス)
3. [実行順序ルール](#実行順序ルール)
4. [典型的なフローパターン](#典型的なフローパターン)
5. [AI生成システム用クイックリファレンス](#ai生成システム用クイックリファレンス)

## システム階層構造

```
オーケストレーター（完全なワークフロー）
├── モジュール（機能グループ）
│   └── ミニマルユニット（最小機能）
└── 直接実行ミニマルユニット
```

### レイヤー説明
- **ミニマルユニット**: 単一機能（53個）- 最新構造：`minimal-units/[category]/[unit].yml`
- **モジュール**: 関連ユニット組み合わせ（`kamuicode-workflow/module-workflow/module-*.yml`）
- **オーケストレーター**: 完全ワークフロー（`kamuicode-workflow/module-workflow/orchestrator-*.yml`）

## 依存関係マトリックス

### 🚦 フェーズベース依存関係

| フェーズ | 必須前提 | 次フェーズ | 並列可能 |
|---------|---------|-----------|---------|
| **Setup** | なし | Planning | ❌ |
| **Planning** | Setup完了 | Production | ✅（複数企画並列） |
| **Production** | Planning完了 | Post-Production | ✅（画像・音声・動画並列） |
| **Post-Production** | Production完了 | Delivery | ✅（字幕・エフェクト並列） |
| **Delivery** | Post-Production完了 | なし | ✅（アップロード・PR並列） |

### 📁 カテゴリ別依存関係

#### 🔧 Setup & Workflow Management
```yaml
必須実行順序:
  1. git-branch-setup     # minimal-units/git-ops/git-branch-setup.yml
  2. [メイン処理]
  3. git-pr-create       # minimal-units/external/git-pr-create.yml
  
モジュール参照:
  - module-setup-branch.yml
  - module-create-pr.yml
```

#### 📋 Planning Phase
```yaml
並列実行可能:
  - planning-ccsdk        # minimal-units/planning/planning-ccsdk.yml
  - banner-planning       # minimal-units/planning/banner-planning.yml
  - news-planning         # minimal-units/planning/news-planning.yml
  - web-search           # minimal-units/planning/web-search.yml
  - data-analysis        # minimal-units/planning/data-analysis.yml
  - data-visualization   # minimal-units/planning/data-visualization.yml

モジュール参照:
  - module-planning-ccsdk.yml
  - module-banner-planning-ccsdk.yml
  - module-news-planning-ccsdk.yml
  - module-web-search.yml
```

#### 🎨 Media Production Phase
```yaml
画像生成（5ユニット - 並列可能）:
  dependencies: [planning完了]
  units:
    - t2i-imagen3         # minimal-units/media/image/t2i-imagen3.yml
    - image-t2i           # minimal-units/media/image/image-t2i.yml
    - t2i-sdxl            # minimal-units/media/image/t2i-sdxl.yml
    - i2i-flux-kontext    # minimal-units/media/image/i2i-flux-kontext.yml
  analysis:
    - image-analysis      # minimal-units/media/image/image-analysis.yml
  
動画生成（7ユニット）:  
  dependencies: [画像生成完了(optional)]
  units:
    - video-generation    # minimal-units/media/video/video-generation.yml
    - t2v-veo3           # minimal-units/media/video/t2v-veo3.yml
    - t2v-wan            # minimal-units/media/video/t2v-wan.yml
    - i2v-seedance       # minimal-units/media/video/i2v-seedance.yml
    - r2v-vidu           # minimal-units/media/video/r2v-vidu.yml
  analysis:
    - video-analysis     # minimal-units/media/video/video-analysis.yml
    - video-prompt-opt   # minimal-units/media/video/video-prompt-opt.yml

音声生成（9ユニット - 並列可能）:
  dependencies: [planning完了]
  units:
    - bgm-generate       # minimal-units/media/audio/bgm-generate.yml
    - bgm-generate-mcp   # minimal-units/media/audio/bgm-generate-mcp.yml
    - t2s-google         # minimal-units/media/audio/t2s-google.yml
    - t2s-minimax-turbo  # minimal-units/media/audio/t2s-minimax-turbo.yml
    - t2s-minimax-voice  # minimal-units/media/audio/t2s-minimax-voice.yml
    - t2s-openai         # minimal-units/media/audio/t2s-openai.yml
    - audio-elevenlabs   # minimal-units/media/audio/audio-elevenlabs.yml
    - audio-minimax      # minimal-units/media/audio/audio-minimax.yml
    - wav-segmentation   # minimal-units/media/audio/wav-segmentation.yml

バナーデザイン（1ユニット）:
  dependencies: [banner-planning完了]
  units:
    - banner-text        # minimal-units/media/banner/banner-text.yml

3D生成（1ユニット）:
  dependencies: [画像生成完了]
  units:
    - i2i3d-hunyuan     # minimal-units/media/3d/i2i3d-hunyuan.yml

モジュール参照:
  - module-image-generation-kc-*.yml
  - module-video-generation-kc-*.yml
  - module-audio-generation-kc-*.yml
  - module-banner-text-overlay-kc-*.yml
```

#### 📰 Content Creation Phase
```yaml
並列実行可能:
  dependencies: [planning完了、web-search完了(optional)]
  units:
    - blog-generation     # minimal-units/content/blog-generation.yml
    - article-generation  # minimal-units/content/article-generation.yml
    - news-summary        # minimal-units/content/news-summary.yml
    - slide-generation    # minimal-units/content/slide-generation.yml
    - markdown-summary    # minimal-units/content/markdown-summary.yml

モジュール参照:
  - module-article-creation-ccsdk.yml
```

#### ⚡ Post-Production Phase
```yaml
字幕・リップシンク（6ユニット）:
  dependencies: [音声生成完了、動画生成完了]
  sequential_required:
    - pixverse-quota-guard  # minimal-units/postprod/pixverse-quota-guard.yml
    - lipsync-pixverse      # minimal-units/postprod/lipsync-pixverse.yml
  parallel_possible:
    - srt-make             # minimal-units/postprod/srt-make.yml
    - srt-sync             # minimal-units/postprod/srt-sync.yml
    - srt-translate        # minimal-units/postprod/srt-translate.yml
    - subtitle-overlay     # minimal-units/postprod/subtitle-overlay.yml

統合・強化（6ユニット）:
  dependencies: [メディア生成完了]
  units:
    - video-concat         # minimal-units/postprod/video-concat.yml
    - title-composition    # minimal-units/postprod/title-composition.yml
    - upscale-topaz        # minimal-units/postprod/upscale-topaz.yml
    - v2v-luma-ray2        # minimal-units/postprod/v2v-luma-ray2.yml
    - v2v-creatify         # minimal-units/postprod/v2v-creatify.yml
    - bgm-overlay          # minimal-units/postprod/bgm-overlay.yml

モジュール参照:
  - module-lipsync-generation-kc-*.yml
  - module-subtitle-overlay-ffmpeg-ccsdk.yml
  - module-video-concatenation-ffmpeg-ccsdk.yml
```

#### 🛠️ Utility & Integration Phase
```yaml
ストレージ（2ユニット）:
  dependencies: [ファイル生成完了]
  units:
    - local-save          # minimal-units/utility/local-save.yml
    - fal-upload          # minimal-units/utility/fal-upload.yml

外部連携（3ユニット）:
  dependencies: [コンテンツ完成]
  units:
    - pdf-create          # minimal-units/external/pdf-create.yml
    - sns-publish         # minimal-units/external/sns-publish.yml
    - git-pr-create       # minimal-units/external/git-pr-create.yml

Git操作（2ユニット）:
  git-branch-setup:       # minimal-units/git-ops/git-branch-setup.yml
    - position: workflow開始時
  cleanup-branch:         # minimal-units/git-ops/cleanup-branch.yml
    - position: workflow終了時（optional）

モジュール参照:
  - module-upload-fal-ccsdk.yml
```

## 実行順序ルール

### 🚦 必須実行順序
```yaml
# 基本フロー
1. git-branch-setup
2. planning-* (並列可能)
3. media-production-* (並列可能、planning後)
4. content-creation-* (並列可能、planning後)
5. post-production-* (media/content後)
6. utility-* (ファイル完成後)
7. git-pr-create

# 特別な依存関係
pixverse系:
  pixverse-quota-guard → lipsync-pixverse

分析系:
  *-generation → *-analysis

字幕系:
  srt-make → srt-sync → srt-translate → subtitle-overlay

強化系:
  video-generation → upscale-topaz
  video-generation → v2v-luma-ray2
  video-generation → v2v-creatify
```

### ⚡ 並列実行推奨
```yaml
# 企画フェーズ
planning-ccsdk || banner-planning || news-planning || web-search

# 制作フェーズ  
image-generation || audio-generation || bgm-generation

# 後処理フェーズ
srt-make || srt-sync || title-composition

# 配信フェーズ
fal-upload || sns-publish
```

## 典型的なフローパターン

### パターン1: シンプル動画制作
```yaml
参考オーケストレーター: orchestrator-video-generation.yml
flow:
  setup: git-branch-setup
  planning: planning-ccsdk
  production: image-t2i → video-generation
  delivery: fal-upload → git-pr-create
  
duration: 15-20分
units_used: 4個
```

### パターン2: リップシンク動画制作
```yaml
参考オーケストレーター: orchestrator-v2v-pixverse-lipsync-single.yml
flow:
  setup: git-branch-setup
  planning: planning-ccsdk
  production: image-t2i → audio-minimax
  postprod: pixverse-quota-guard → lipsync-pixverse → subtitle-overlay
  delivery: fal-upload → git-pr-create
  
duration: 25-30分
units_used: 8個
```

### パターン3: マルチメディアキャンペーン
```yaml
参考オーケストレーター: orchestrator-banner-advertisement-creation.yml
flow:
  setup: git-branch-setup
  planning: banner-planning || news-planning
  production: 
    - t2i-imagen3 || audio-generation || video-generation
  postprod: banner-text || subtitle-overlay || video-concat
  content: blog-generation || markdown-summary
  delivery: fal-upload || sns-publish || git-pr-create
  
duration: 45-60分
units_used: 15-20個
```

### パターン4: ニュース動画制作
```yaml
参考オーケストレーター: orchestrator-news-video-generation.yml
flow:
  setup: git-branch-setup
  research: web-search → news-summary → news-planning
  production: t2v-veo3 || t2s-google || bgm-generate
  postprod: bgm-overlay → title-composition → video-concat
  content: article-generation → markdown-summary
  delivery: fal-upload → sns-publish → git-pr-create
  
duration: 35-45分
units_used: 12-15個
```

## AI生成システム用クイックリファレンス

### 🎯 ユニット選択指針

```yaml
目的別推奨ユニット:
  画像重視: t2i-imagen3, i2i-flux-kontext, image-analysis
  動画重視: video-generation, t2v-veo3, upscale-topaz
  音声重視: t2s-minimax-voice, bgm-generate-mcp, bgm-overlay
  コンテンツ重視: article-generation, blog-generation, markdown-summary
  速度重視: image-t2i, t2v-wan, t2s-google
  品質重視: t2i-imagen3, t2v-veo3, audio-elevenlabs
  
品質レベル別:
  エコノミー: t2s-google, image-t2i, basic-concat
  スタンダード: t2i-sdxl, video-generation, bgm-generate
  プレミアム: t2i-imagen3, t2v-veo3, audio-elevenlabs
```

### 🚀 自動選択ルール

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

### 📊 リソース使用量予測

```yaml
軽量ワークフロー（10分以内）:
  units: 3-5個
  pattern: planning → single-generation → upload
  example: banner-planning → banner-text → fal-upload

中量ワークフロー（20-30分）:
  units: 6-10個  
  pattern: planning → parallel-generation → postprod → upload
  example: planning → (image + audio) → lipsync → upload

重量ワークフロー（45分以上）:
  units: 12-20個
  pattern: multi-planning → multi-generation → complex-postprod → multi-delivery
  example: (planning + research) → (image + video + audio) → (edit + enhance) → (upload + social)
```

### 🔄 エラーハンドリング指針

```yaml
必須チェックポイント:
  - pixverse-quota-guard: リップシンク前に必須
  - *-analysis: 生成後の品質確認
  - fal-upload: 成功確認後に次のステップ

フォールバック戦略:
  t2i-imagen3 失敗 → t2i-sdxl → image-t2i
  lipsync-pixverse 失敗 → subtitle-overlay のみ
  bgm-generate 失敗 → audio生成なしで継続

リトライ推奨:
  - ネットワーク系: web-search, fal-upload
  - AI生成系: image-*, video-*, audio-*
  - 解析系: *-analysis

スキップ可能:
  - 品質向上系: upscale-*, v2v-*
  - 装飾系: title-composition, bgm-overlay
  - 外部連携系: sns-publish, pdf-create
```

---

**このガイドを使用することで、AIシステムは適切な依存関係を理解し、効率的で信頼性の高いワークフローを自動生成できます。**

**最終更新**: 2025-07-31  
**対応バージョン**: v9.0（ミニマルユニットベース）  
**統合ソース**: DEPENDENCY_MAP.md + WORKFLOW_PATTERNS.md + kamuicode-workflow/README.md