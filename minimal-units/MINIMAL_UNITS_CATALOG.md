# Minimal Units Catalog

ミニマルユニットの包括的なカタログです。メタワークフローシステムはこのカタログを参照して、動的にワークフローを構築します。

**総ユニット数: 80個**

## Categories and Units

### 🎨 Media Production

#### 🖼️ Image Generation (5個)
- **t2i-imagen3**: Google Imagen3による高品質画像生成 (minimal-units/media/image/t2i-imagen3.yml)
- **image-t2i**: ✅ 汎用Text-to-Image（画質設定対応・v8更新済み） (minimal-units/media/image/image-t2i.yml)
- **t2i-sdxl**: Stable Diffusion XLによる画像生成 (minimal-units/media/image/t2i-sdxl.yml)
- **i2i-flux-kontext**: Flux Kontextによる画像変換 (minimal-units/media/image/i2i-flux-kontext.yml)
- **image-analysis**: 画像内容の分析 (minimal-units/media/image/image-analysis.yml)

#### 🎬 Video Generation (7個)
- **video-generation**: ✅ 汎用動画生成（画質設定対応・v8更新済み） (minimal-units/media/video/video-generation.yml)
- **t2v-veo3**: Google Veo3によるText-to-Video (minimal-units/media/video/t2v-veo3.yml)
- **t2v-wan**: Wan V2によるText-to-Video (minimal-units/media/video/t2v-wan.yml)
- **i2v-seedance**: SeeDanceによるImage-to-Video (minimal-units/media/video/i2v-seedance.yml)
- **r2v-vidu**: Reference-to-Video生成 (minimal-units/media/video/r2v-vidu.yml)
- **video-analysis**: 動画内容の分析 (minimal-units/media/video/video-analysis.yml)
- **video-prompt-opt**: 動画プロンプトの最適化 (minimal-units/media/video/video-prompt-opt.yml)

#### 🎵 Audio Generation (10個)
- **bgm-generate**: BGM生成（シミュレーション版） (minimal-units/media/audio/bgm-generate.yml)
- **bgm-generate-mcp**: ✅ BGM生成（MCP版・lyria_generate修正済み） (minimal-units/media/audio/bgm-generate-mcp.yml)
- **t2s-google**: Google Text-to-Speech (minimal-units/media/audio/t2s-google.yml)
- **t2s-minimax-turbo**: MiniMax Turbo TTS（シミュレーション版） (minimal-units/media/audio/t2s-minimax-turbo.yml)
- **t2s-minimax-turbo-mcp**: ✅ MiniMax Turbo TTS（MCP版・実装済み） (minimal-units/media/audio/t2s-minimax-turbo-mcp.yml)
- **t2s-minimax-voice**: MiniMax Voice Design (minimal-units/media/audio/t2s-minimax-voice.yml)
- **t2s-openai**: OpenAI Text-to-Speech (minimal-units/media/audio/t2s-openai.yml)
- **audio-elevenlabs**: ElevenLabs音声生成 (minimal-units/media/audio/audio-elevenlabs.yml)
- **audio-minimax**: MiniMax音声生成 (minimal-units/media/audio/audio-minimax.yml)
- **wav-segmentation**: 音声ファイルの分割 (minimal-units/media/audio/wav-segmentation.yml)

#### 🏷️ Banner Design (1個)
- **banner-text**: バナー画像にテキスト追加・デザイン実装 (minimal-units/media/banner/banner-text.yml)

#### 🎭 3D Generation (1個)
- **i2i3d-hunyuan**: HunyuanによるImage-to-3D (minimal-units/media/3d/i2i3d-hunyuan.yml)

### 📋 Planning & Analysis (6個)
- **planning-ccsdk**: Claude Code SDKによる企画 (minimal-units/planning/planning-ccsdk.yml)
- **banner-planning**: バナー企画立案 (minimal-units/planning/banner-planning.yml)
- **news-planning**: ニュース企画 (minimal-units/planning/news-planning.yml)
- **web-search**: Web検索による情報収集 (minimal-units/planning/web-search.yml)
- **data-analysis**: データ分析 (minimal-units/planning/data-analysis.yml)
- **data-visualization**: データ可視化 (minimal-units/planning/data-visualization.yml)

### 📰 Content Creation (5個)
- **blog-generation**: ブログ記事生成 (minimal-units/content/blog-generation.yml)
- **article-generation**: 記事生成 (minimal-units/content/article-generation.yml)
- **news-summary**: ニュース要約 (minimal-units/content/news-summary.yml)
- **slide-generation**: プレゼンテーション生成 (minimal-units/content/slide-generation.yml)
- **markdown-summary**: Markdownサマリー生成 (minimal-units/content/markdown-summary.yml)

### ⚡ Post-Production (12個)
- **lipsync-pixverse**: Pixverseリップシンク (minimal-units/postprod/lipsync-pixverse.yml)
- **pixverse-quota-guard**: Pixverseクォータ管理 (minimal-units/postprod/pixverse-quota-guard.yml)
- **srt-make**: SRTファイル生成 (minimal-units/postprod/srt-make.yml)
- **srt-sync**: SRT同期調整 (minimal-units/postprod/srt-sync.yml)
- **srt-translate**: SRT翻訳 (minimal-units/postprod/srt-translate.yml)
- **subtitle-overlay**: 字幕オーバーレイ (minimal-units/postprod/subtitle-overlay.yml)
- **video-concat**: ✅ 複数動画の結合（ナレーション対応・v8更新済み） (minimal-units/postprod/video-concat.yml)
- **title-composition**: タイトルフレーム合成 (minimal-units/postprod/title-composition.yml)
- **upscale-topaz**: Topazによる動画アップスケール (minimal-units/postprod/upscale-topaz.yml)
- **v2v-luma-ray2**: Luma Ray2による動画変換 (minimal-units/postprod/v2v-luma-ray2.yml)
- **v2v-creatify**: Creatifyによる動画編集 (minimal-units/postprod/v2v-creatify.yml)
- **bgm-overlay**: BGMのオーバーレイ (minimal-units/postprod/bgm-overlay.yml)

### 🛠️ Utility & Integration (7個)
- **local-save**: ローカル保存 (minimal-units/utility/local-save.yml)
- **fal-upload**: FALへのアップロード (minimal-units/utility/fal-upload.yml)
- **git-branch-setup**: Gitブランチセットアップ (minimal-units/git-ops/git-branch-setup.yml)
- **git-pr-create**: プルリクエスト作成 (minimal-units/external/git-pr-create.yml)
- **cleanup-branch**: ブランチクリーンアップ (minimal-units/git-ops/cleanup-branch.yml)
- **pdf-create**: PDF作成 (minimal-units/external/pdf-create.yml)
- **sns-publish**: SNS投稿 (minimal-units/external/sns-publish.yml)

### 🌐 External APIs (27個) [FINAL UPDATE]
#### YouTube API
- **youtube-upload**: YouTube動画アップロード (minimal-units/external/youtube-upload.yml)
- **youtube-video-info**: YouTube動画情報取得 (minimal-units/external/youtube-video-info.yml) ⭐NEW

#### News & Weather APIs
- **newsapi-fetch**: NewsAPI記事取得 (minimal-units/external/newsapi-fetch.yml)
- **weather-fetch**: OpenWeatherMap天気情報取得 (minimal-units/external/weather-fetch.yml)

#### Communication APIs
- **slack-notify**: Slack通知送信 (minimal-units/external/slack-notify.yml)
- **slack-file-upload**: Slackファイルアップロード (minimal-units/external/slack-file-upload.yml) ⭐NEW
- **discord-webhook**: Discord Webhook送信 (minimal-units/external/discord-webhook.yml) ⭐NEW
- **telegram-send-message**: Telegramメッセージ送信 (minimal-units/external/telegram-send-message.yml) ⭐NEW
- **sendgrid-send-email**: SendGridメール送信 (minimal-units/external/sendgrid-send-email.yml) ⭐NEW

#### AI & ML APIs
- **openai-gpt**: OpenAI GPTテキスト生成 (minimal-units/external/openai-gpt.yml)
- **openai-summarize**: OpenAI要約生成 (minimal-units/external/openai-summarize.yml) ⭐NEW
- **openai-translate**: OpenAI翻訳 (minimal-units/external/openai-translate.yml) ⭐NEW
- **openai-image-gen**: OpenAI画像生成 (gpt-image-1) (minimal-units/external/openai-image-gen.yml) ⭐NEW
- **elevenlabs-tts**: ElevenLabs音声合成 (minimal-units/external/elevenlabs-tts.yml)
- **huggingface-inference**: Hugging Faceモデル推論 (minimal-units/external/huggingface-inference.yml) ⭐NEW

#### Data & Analytics APIs
- **google-sheets-write**: Google Sheetsデータ書き込み (minimal-units/external/google-sheets-write.yml)
- **google-sheets-read**: Google Sheetsデータ読み取り (minimal-units/external/google-sheets-read.yml) ⭐NEW
- **finnhub-stock-quote**: Finnhub株価取得 (minimal-units/external/finnhub-stock-quote.yml) ⭐NEW

#### Social Media APIs
- **twitter-post**: Twitter/X投稿 (minimal-units/external/twitter-post.yml)
- **twitter-search**: Twitter/X検索 (minimal-units/external/twitter-search.yml) ⭐NEW
- **reddit-search**: Reddit投稿検索 (minimal-units/external/reddit-search.yml) ⭐NEW

#### Development APIs
- **github-issue-create**: GitHub Issue作成 (minimal-units/external/github-issue-create.yml) ⭐NEW
- **github-repo-search**: GitHubリポジトリ検索 (minimal-units/external/github-repo-search.yml) ⭐NEW
- **github-workflow-dispatch**: GitHub Workflow実行 (minimal-units/external/github-workflow-dispatch.yml) ⭐NEW
- **github-release-create**: GitHub Release作成 (minimal-units/external/github-release-create.yml) ⭐NEW
- **arxiv-search**: arXiv論文検索 (minimal-units/external/arxiv-search.yml) ⭐NEW
- **notion-create-page**: Notionページ作成 (minimal-units/external/notion-create-page.yml) ⭐NEW

### 🎬 Workflow Compositions (1個)
- **video-production-workflow**: ✅ 動画制作統合ワークフロー（v8成功パターン） (minimal-units/workflows/video-production-workflow.yml)

## Usage Guidelines

### 1. Unit Selection
メタワークフローは以下の基準でユニットを選択します：
- **タスク要求**: ユーザーが求める最終成果物
- **依存関係**: 必要な前処理・後処理
- **並列可能性**: 同時実行可能なタスク
- **品質要求**: 求められる品質レベル

### 2. Dynamic Composition
- **直列配置**: 依存関係がある場合
- **並列配置**: 独立したタスクの場合
- **条件分岐**: 結果に応じた処理
- **ループ処理**: 複数アイテムの処理

### 3. Unit Extension
新しいユニットが必要な場合：
1. 既存ユニットの組み合わせで対応可能か検討
2. 新規ユニット作成の必要性を判断
3. インターフェース仕様に従って作成
4. カタログに追加

## Metadata Structure

各ユニットは以下のメタデータを持ちます：
```yaml
name: unit-name
description: ユニットの説明
category: カテゴリ
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

メタワークフローシステムは：
1. このカタログを読み込み
2. Claude Code SDKでタスクを分析
3. 必要なユニットを選択・配置
4. 動的にワークフローを生成

---
更新日: {{ current_date }}