# Minimal Units Catalog

ミニマルユニットの包括的なカタログです。メタワークフローシステムはこのカタログを参照して、動的にワークフローを構築します。

**総ユニット数: 53個**

## Categories and Units

### 🎨 Image Generation & Processing
- **t2i-imagen3**: Google Imagen3による高品質画像生成
- **image-t2i**: 汎用Text-to-Image（複数モデル対応）
- **t2i-sdxl**: Stable Diffusion XLによる画像生成
- **i2i-flux-kontext**: Flux Kontextによる画像変換
- **image-analysis**: 画像内容の分析
- **banner-text**: バナー画像にテキスト追加

### 🎬 Video Generation & Processing
- **video-generation**: 汎用動画生成（i2v/t2v対応）
- **t2v-veo3**: Google Veo3によるText-to-Video
- **t2v-wan**: Wan V2によるText-to-Video
- **i2v-seedance**: SeeDanceによるImage-to-Video
- **r2v-vidu**: Reference-to-Video生成
- **v2v-luma-ray2**: Luma Ray2による動画変換
- **v2v-creatify**: Creatifyによる動画編集
- **video-concat**: 複数動画の結合
- **upscale-topaz**: Topazによる動画アップスケール
- **video-analysis**: 動画内容の分析
- **video-prompt-opt**: 動画プロンプトの最適化
- **title-composition**: タイトルフレーム合成

### 🎵 Audio Generation & Processing
- **bgm-generate**: BGM生成（シミュレーション版）
- **bgm-generate-mcp**: BGM生成（MCP版）
- **t2s-google**: Google Text-to-Speech
- **t2s-minimax-turbo**: MiniMax Turbo TTS
- **t2s-minimax-voice**: MiniMax Voice Design
- **t2s-openai**: OpenAI Text-to-Speech
- **audio-elevenlabs**: ElevenLabs音声生成
- **audio-minimax**: MiniMax音声生成
- **bgm-overlay**: BGMのオーバーレイ
- **wav-segmentation**: 音声ファイルの分割

### 👄 Lipsync & Subtitles
- **lipsync-pixverse**: Pixverseリップシンク
- **pixverse-quota-guard**: Pixverseクォータ管理
- **srt-make**: SRTファイル生成
- **srt-sync**: SRT同期調整
- **srt-translate**: SRT翻訳
- **subtitle-overlay**: 字幕オーバーレイ

### 📋 Planning & Analysis
- **planning-ccsdk**: Claude Code SDKによる企画
- **web-search**: Web検索による情報収集
- **article-generation**: 記事生成
- **markdown-summary**: Markdownサマリー生成
- **data-analysis**: データ分析
- **data-visualization**: データ可視化

### 📰 Content Creation
- **blog-generation**: ブログ記事生成
- **news-planning**: ニュース企画
- **news-summary**: ニュース要約
- **slide-generation**: プレゼンテーション生成
- **banner-planning**: バナー企画

### 🛠️ Utility & Integration
- **local-save**: ローカル保存
- **fal-upload**: FALへのアップロード
- **git-branch-setup**: Gitブランチセットアップ
- **git-pr-create**: プルリクエスト作成
- **cleanup-branch**: ブランチクリーンアップ
- **pdf-create**: PDF作成
- **sns-publish**: SNS投稿

### 🎭 3D Generation
- **i2i3d-hunyuan**: HunyuanによるImage-to-3D

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