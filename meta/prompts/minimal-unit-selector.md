# Minimal Unit Selector Prompt

ユーザーの要求とタスク分解結果に基づいて、53個の利用可能なミニマルユニットから適切なものを選択してください。

## 入力情報
- ユーザー要求: {{USER_REQUEST}}
- 分解されたタスク: {{DECOMPOSED_TASKS}}
- ワークフロータイプ: {{WORKFLOW_TYPE}}

## 利用可能なミニマルユニット（全53個）

### 🎨 画像生成・処理（5個）
- t2i-imagen3: Google Imagen3による高品質画像生成
- image-t2i: 汎用Text-to-Image（複数モデル対応）
- t2i-sdxl: Stable Diffusion XLによる画像生成
- i2i-flux-kontext: Flux Kontextによる画像変換
- image-analysis: 画像内容の分析

### 🏷️ バナーデザイン・実装（1個）
- banner-text: バナー画像にテキスト追加・デザイン実装

### 🎬 動画生成・処理（12個）
- video-generation: 汎用動画生成（i2v/t2v対応）
- t2v-veo3: Google Veo3によるText-to-Video
- t2v-wan: Wan V2によるText-to-Video
- i2v-seedance: SeeDanceによるImage-to-Video
- r2v-vidu: Reference-to-Video生成
- v2v-luma-ray2: Luma Ray2による動画変換
- v2v-creatify: Creatifyによる動画編集
- video-concat: 複数動画の結合
- upscale-topaz: Topazによる動画アップスケール
- video-analysis: 動画内容の分析
- video-prompt-opt: 動画プロンプトの最適化
- title-composition: タイトルフレーム合成

### 🎵 音声・音楽（10個）
- bgm-generate: BGM生成（シミュレーション版）
- bgm-generate-mcp: BGM生成（MCP版）
- t2s-google: Google Text-to-Speech
- t2s-minimax-turbo: MiniMax Turbo TTS
- t2s-minimax-voice: MiniMax Voice Design
- t2s-openai: OpenAI Text-to-Speech
- audio-elevenlabs: ElevenLabs音声生成
- audio-minimax: MiniMax音声生成
- bgm-overlay: BGMのオーバーレイ
- wav-segmentation: 音声ファイルの分割

### 👄 字幕・リップシンク（6個）
- srt-make: SRTファイル生成
- srt-sync: SRT同期調整
- srt-translate: SRT翻訳
- subtitle-overlay: 字幕オーバーレイ
- lipsync-pixverse: Pixverseリップシンク
- pixverse-quota-guard: Pixverseクォータ管理

### 📋 企画・分析（6個）
- planning-ccsdk: Claude Code SDKによる企画立案
- banner-planning: バナー企画立案
- news-planning: ニュース企画
- web-search: Web検索による情報収集
- data-analysis: データ分析
- data-visualization: データ可視化

### 📰 コンテンツ作成（5個）
- blog-generation: ブログ記事生成
- article-generation: 記事生成
- news-summary: ニュース要約
- slide-generation: プレゼンテーション生成
- markdown-summary: Markdownサマリー生成

### 🛠️ ユーティリティ・統合（8個）
- local-save: ローカル保存
- fal-upload: FALへのアップロード
- git-branch-setup: Gitブランチセットアップ
- git-pr-create: プルリクエスト作成
- cleanup-branch: ブランチクリーンアップ
- pdf-create: PDF作成
- sns-publish: SNS投稿

### 🎭 3D生成（1個）
- i2i3d-hunyuan: HunyuanによるImage-to-3D

## 選択基準

### 1. 超詳細な人間的選択
人間が無意識に行うような詳細なユニット選択を行ってください：
- **準備段階**: 環境確認、リソース準備、計画立案ユニット
- **調査段階**: web-search、image-analysis、data-analysisなど
- **生成段階**: 複数バリエーション生成のため同じユニットを複数選択
- **品質確認段階**: analysis系ユニットで品質チェック
- **改善段階**: 最適化、編集、調整ユニット
- **最終段階**: 保存、配信、ドキュメント化ユニット

### 2. 並列処理の最適化
- **3項並列**: 独立した調査・分析タスク（例：web-search + image-analysis + data-analysis）
- **4項並列**: バリエーション生成（例：4つの異なるスタイルで画像生成）
- **5項並列**: 包括的カバレッジ（例：5つの異なる形式で出力）
- **依存関係を考慮**: 前段の出力を必要とするユニットは適切に配置

### 3. ユニット選択の網羅性
- 53個のユニットから幅広く選択
- 同じユニットを異なる目的で複数回使用可能
- カテゴリをまたいだ統合的な選択

### 4. 人間的な冗長性
- 最小限ではなく、人間が自然に行うような冗長性を含む
- 「念のため」の確認ユニット
- 「品質向上」のための追加処理ユニット

## 出力形式
```json
{
  "selected_units": [
    {
      "task_id": "task-001",
      "unit_name": "planning-ccsdk",
      "unit_path": "minimal-units/planning/planning-ccsdk.yml",
      "purpose": "全体計画と構造設計",
      "inputs": {
        "prompt": "ユーザー要求から生成されたプロンプト"
      },
      "dependencies": [],
      "parallel_group": 1,
      "execution_order": 1
    },
    {
      "task_id": "task-002",
      "unit_name": "web-search",
      "unit_path": "minimal-units/planning/web-search.yml",
      "purpose": "参考情報の収集",
      "inputs": {
        "query": "関連情報の検索クエリ"
      },
      "dependencies": [],
      "parallel_group": 1,
      "execution_order": 1
    },
    {
      "task_id": "task-003",
      "unit_name": "image-analysis",
      "unit_path": "minimal-units/image/image-analysis.yml",
      "purpose": "既存リソースの分析",
      "inputs": {
        "image_path": "参考画像パス"
      },
      "dependencies": [],
      "parallel_group": 1,
      "execution_order": 1
    }
  ],
  "parallel_optimization": {
    "strategy": "初期フェーズ3項並列、生成フェーズ4項並列、検証フェーズ2項並列",
    "groups": {
      "1": {"units": 3, "type": "research", "description": "調査・分析フェーズ"},
      "2": {"units": 4, "type": "generation", "description": "メイン生成フェーズ"},
      "3": {"units": 2, "type": "validation", "description": "品質検証フェーズ"},
      "4": {"units": 3, "type": "refinement", "description": "改善・最適化フェーズ"},
      "5": {"units": 2, "type": "delivery", "description": "配信・保存フェーズ"}
    }
  },
  "unit_statistics": {
    "total_selected": 25,
    "by_category": {
      "planning": 5,
      "image": 6,
      "video": 8,
      "audio": 4,
      "utility": 2
    },
    "reused_units": [
      {"unit": "image-t2i", "count": 4, "reason": "複数スタイルでの生成"},
      {"unit": "video-generation", "count": 3, "reason": "異なる設定での生成"}
    ]
  },
  "human_behavior_notes": [
    "複数の参考情報源から情報収集",
    "試行錯誤的な生成プロセス",
    "段階的な品質向上",
    "最終確認と微調整"
  ]
}