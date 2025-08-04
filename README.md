# Meta Workflow Generator System (Kamui Rossy)

🤖 **Claude Code GitHub Actions統合**によるメタワークフロージェネレーターシステム

## 🎯 概要

このシステムは、ユーザーのリクエストに基づいて完全なワークフローを自動生成するメタワークフロージェネレーターです。**ミニマルユニットベース動的構築**と**段階的デプロイシステム**により、高品質で実行可能なGitHub Actionsワークフローを効率的に生成します。

## 🏗️ アーキテクチャ v10.0

### **ミニマルユニットベース・デュアルアプローチシステム**
- **Claude Code SDK中心**: ユーザー要求を分析し、タスクを動的に分解
- **デュアルアプローチ生成**: 
  - **オリジナルアプローチ**: ミニマルユニットから動的にワークフロー構築
  - **オーケストレーターアプローチ**: kamuicode-workflowパターンを参考に構築
- **ベスト・オブ・ボス選択**: 両アプローチを比較し、最良の要素を組み合わせ
- **基本配置パターン**: 直列・並列・条件分岐・ループ処理の基本パターンを実装
- **動的配置**: 並列処理、条件分岐、ループ処理を要求に応じて自動判断
- **拡張可能**: 新しいユニットやカスタムノードを必要に応じて作成・統合
- **タスク依存関係管理**: データフローと前提条件に基づく厳密な実行順序
- **最適並列処理**: 3-5項並列を依存関係を考慮して自動配置
- **品質検証**: YAML構文、GitHub Actions構造、MCP参照、依存関係チェック

### **核心コンポーネント**
- **`minimal-units/`**: 80個の再利用可能なワークフロー部品（画像、動画、音声、企画、外部API等）
- **`kamuicode-workflow/`**: 参考となるオーケストレーター・モジュールパターン
- **`.github/workflows/meta-workflow-executor-v10.yml`**: Claude Code SDKベースの動的メタワークフロー
- **`.github/workflows/auto-fix-deployment.yml`**: 自動デプロイ・エラー回復システム
- **`.github/workflows/continuous-system-monitor.yml`**: システム健全性監視
- **`meta/prompts/`**: タスク分解、ユニット選択、ワークフロー生成用プロンプト

## 📁 ディレクトリ構成

```
📦 Kamui Rossy
├── 🤖 .github/workflows/
│   ├── meta-workflow-executor-v10.yml         # 動的メタワークフロー v10.0
│   ├── auto-fix-deployment.yml                # 自動修復システム
│   ├── continuous-system-monitor.yml          # 連続監視システム
│   └── generated/                             # 生成ワークフロー配置
│
├── 🧩 minimal-units/                          # ミニマルユニット（再利用可能部品）
│   ├── planning/        # 企画・分析ユニット
│   ├── image/           # 画像生成・処理ユニット
│   ├── video/           # 動画生成・処理ユニット
│   ├── audio/           # 音声・音楽生成ユニット
│   ├── 3d/              # 3Dモデル生成ユニット
│   ├── assembly/        # 統合・結合ユニット
│   ├── subtitle/        # 字幕・リップシンクユニット
│   ├── data/            # データ分析・可視化ユニット
│   ├── external/        # 外部連携ユニット
│   └── utility/         # ユーティリティユニット
│
├── 📋 meta/
│   └── prompts/         # プロンプトファイル群
│       ├── minimal-unit-selector.md           # ユニット選択プロンプト
│       ├── workflow-composer.md               # ワークフロー構成プロンプト
│       ├── stepback-question-generator.md
│       ├── stepback-answer-analyzer.md
│       ├── stepback-to-tasks.md
│       └── task-prompt-template.md
│
├── 🔧 kamuicode-workflow/  # 参考パターン（subtree）
│   └── module-workflow/    # オーケストレーター・モジュール例
│
├── 🏗️ generated/        # 自動化出力（GitHub Actions）
│   ├── metadata/        # 分析結果（永続保存）
│   └── logs/           # 実行ログ（各run-XX-timestamp）
│
├── 💻 cli_generated/     # CLI専用出力
│   └── media/          # CLIメディア生成物
│       ├── images/     # CLI画像生成
│       ├── videos/     # CLI動画生成
│       ├── audio/      # CLI音声生成
│       └── 3d/         # CLI 3D生成
│
├── ⚙️ cli_config/        # CLI設定ファイル群
│   ├── .claude_mcp_defaults.md    # MCP デフォルト設定
│   ├── .env.claude               # CLI環境変数
│   └── claude_mcp_helpers.md     # MCPヘルパー関数
│
├── 📚 docs/             # プロジェクトドキュメント
│   ├── mcp/            # MCP関連ドキュメント（英語）
│   ├── system/         # システム管理ドキュメント（英語）
│   └── archive/        # 過去の作業記録
│
├── 🗃️ projects/         # プロジェクトベース出力
│   ├── current-session/   # 現在セッション
│   ├── project-image-generation/
│   ├── project-video-generation/
│   └── project-audio-generation/
│
└── 🛠️ scripts/          # ユーティリティスクリプト
    ├── fal_upload_helper.py
    └── generate-mcp-permissions.py
```

## 🚀 使用方法

### **GitHub Actions（自動化）**
1. **Issue駆動**: 専用テンプレートでIssueを作成
2. **手動実行**: `workflow_dispatch`トリガーで直接実行
3. **段階的デプロイ**: 生成 → 検証 → ステージング (.disabled) → 手動有効化

### **Claude Code CLI（対話型）**
1. **環境認識**: CLI設定を自動読み込み（`cli_config/`）
2. **メディア生成**: `cli_generated/media/` に自動出力
3. **GitHub Actions分離**: 出力先を完全分離して競合回避

## 🔧 MCP設定

### **核心設定ファイル：`.claude/mcp-kamuicode.json`**
このファイルはKamui Rossyシステムの**最重要設定ファイル**です。

#### **ファイルの役割**
- **MCP サービス定義**: 44個以上のAI生成・外部APIサービスのエンドポイント設定
- **Claude Code統合**: GitHub ActionsでClaude CodeがMCPツールを使用するための必須設定
- **環境変数参照**: `{{API_KEY_NAME}}`形式でシークレットを安全に参照

#### **設定されているサービス**
1. **AI生成サービス（24個）**: 初期から組み込まれている画像・動画・音声生成サービス
2. **外部APIサービス（20個以上）**: v10.0で追加された外部連携サービス

### **CLI専用設定**
- **`cli_config/.claude_mcp_defaults.md`**: CLI用デフォルト設定
- **`cli_config/claude_mcp_helpers.md`**: 使用例・ヘルパー関数

### **利用可能サービス（`.claude/mcp-kamuicode.json`に設定済み）**

#### **AI生成サービス（24個）**
- **T2I（画像生成）**: 
  - `t2i-google-imagen3`: Google Imagen3
  - `t2i-fal-imagen4-ultra`: 高品質画像生成
  - `t2i-fal-imagen4-fast`: 高速画像生成
  - `t2i-fal-flux-schnell`: Flux高速生成
  - `t2i-fal-rundiffusion-photo-flux`: フォトリアル画像
- **T2V（動画生成）**: 
  - `t2v-fal-veo3-fast`: 高速動画生成
  - `t2v-fal-wan-v2-2-a14b-t2v`: 高品質動画生成
- **I2V（画像→動画）**: 
  - `i2v-fal-hailuo-02-pro`: プロ品質アニメーション
  - `i2v-fal-bytedance-seedance-v1-lite`: 軽量アニメーション
- **T2M（音楽生成）**: `t2m-google-lyria`
- **T2S（音声合成）**: `t2s-fal-minimax-speech-02-turbo`
- **V2A（動画→音声）**: `v2a-fal-thinksound`
- **V2V（動画編集）**: リップシンク、背景除去、アップスケール等
- **I2I（画像編集）**: Flux Kontext編集
- **I2I3D（画像→3D）**: `i2i3d-fal-hunyuan3d-v21`
- **その他**: トレーニング、Reference-to-Video等

#### **外部APIサービス（20個以上）**
- **AI・ML**: OpenAI GPT/DALL-E、ElevenLabs、HuggingFace
- **SNS**: YouTube、Twitter/X、Reddit
- **通信**: Slack、Discord、Telegram、SendGrid
- **データ**: NewsAPI、天気、Google Sheets、株価、arXiv
- **開発**: GitHub API、Notion

## 🛡️ 環境分離システム

### **CLI・GitHub Actions分離**
- **CLI出力**: `cli_generated/` + `cli_config/`
- **GitHub Actions出力**: `generated/` + `projects/`
- **競合防止**: `.claudeignore` でファイル保護

### **設定ファイル優先順位**
1. **CLI優先**: `.claude/settings.local.json` (2025-07-28 17:22更新)
2. **共有**: `.claude/mcp-kamuicode.json`
3. **GitHub Actions専用**: `.claude/settings.github-actions.json`

## 📊 システム状況

- **アーキテクチャ**: v10.0（ミニマルユニットベース動的生成 + 外部API統合）
- **ミニマルユニット**: 80個
  - 画像: 5個
  - 動画: 7個
  - 音声: 10個
  - バナー: 1個
  - 3D: 1個
  - 企画: 6個
  - コンテンツ: 5個
  - 後処理: 12個
  - ユーティリティ: 7個
  - **外部API: 27個** ⭐NEW
- **MCP サービス**: 44個以上（AI生成24個 + 外部API 20個以上）
- **参考パターン**: kamuicode-workflowオーケストレーター
- **CLI環境**: アクティブ（2025-07-28 17:22）

## 🔑 必要なGitHub Actionsシークレット

### **必須シークレット**
- `CLAUDE_CODE_OAUTH_TOKEN`: Claude Code認証トークン（必須）

### **外部API用シークレット**（使用するAPIに応じて設定）

#### **AI・機械学習**
- `OPENAI_API_KEY`: OpenAI API（GPT、DALL-E、要約、翻訳）
- `ELEVENLABS_API_KEY`: ElevenLabs音声合成
- `HUGGINGFACE_API_KEY`: Hugging Face推論API

#### **コミュニケーション**
- `SLACK_BOT_TOKEN`: Slack通知・ファイルアップロード
- `DISCORD_WEBHOOK_URL`: Discord Webhook通知
- `TELEGRAM_BOT_TOKEN`: Telegramメッセージ送信
- `SENDGRID_API_KEY`: SendGridメール送信

#### **ソーシャルメディア**
- `YOUTUBE_API_KEY`: YouTube動画アップロード・情報取得
- `TWITTER_API_KEY`: Twitter/X投稿・検索（Bearer Token）
- `REDDIT_CLIENT_ID`: Reddit API クライアントID
- `REDDIT_CLIENT_SECRET`: Reddit API クライアントシークレット

#### **データ・分析**
- `NEWSAPI_KEY`: NewsAPI.org ニュース取得
- `OPENWEATHERMAP_API_KEY`: OpenWeatherMap天気情報
- `GOOGLE_SHEETS_CREDENTIALS`: Google Sheetsサービスアカウント（Base64エンコード）
- `FINNHUB_API_KEY`: Finnhub株価データ

#### **開発ツール**
- `GITHUB_TOKEN`: GitHub API（デフォルトと異なる場合）
- `NOTION_API_KEY`: Notion統合トークン

### **設定方法**

#### **方法1: 一括設定スクリプト（推奨）**
```bash
# 1. .envファイルを編集（必要なAPIキーを設定）
cp .env.example .env  # まだない場合
nano .env  # 実際のAPIキーに置き換える

# 2. スクリプトで一括設定
./scripts/env-to-secrets.sh .env

# または、コメント行を除いて直接設定
grep -v '^#' .env | grep -v '^$' | while IFS='=' read -r key value; do 
  gh secret set "$key" -b "$value" -R rossy8417/kamuicode_meta
done
```

#### **方法2: GitHub CLIで個別設定**
```bash
# 例：OpenAI APIキーを設定
gh secret set OPENAI_API_KEY -b "sk-your-api-key-here"
```

#### **方法3: GitHub Web UIで手動設定**
1. GitHub リポジトリの Settings → Secrets and variables → Actions
2. 「New repository secret」をクリック
3. Name と Secret value を入力して保存

### **便利ツール**
- `.env`: サンプル環境変数ファイル（モックデータ付き）
- `scripts/env-to-secrets.sh`: .envファイルから一括設定するスクリプト
- `scripts/setup-github-secrets.sh`: 対話型セットアップスクリプト

## 📝 バージョン履歴

### v10.0 (2025-08-02) - 外部API統合
- **外部API統合**: 27個の外部APIミニマルユニットを追加
- **ミニマルユニット拡張**: 53個 → 80個に増加
- **MCP サービス拡張**: 24個 → 44個以上に拡張
- **メタワークフロー強化**: 全外部APIの自動検出、日英キーワード対応
- **新カテゴリ追加**: AI・ML、SNS、通信、データ分析、開発ツール

### v9.0 (2025-07-31) - ミニマルユニットベース
- ミニマルユニットベース動的生成システムの確立
- kamuicode-workflowパターンの採用
- 段階的デプロイシステムの実装

## 🔗 重要リンク

- **システム管理**: `docs/system/CLEANUP_PROTOCOL.md`
- **CLI環境管理**: `docs/system/CLI_ENVIRONMENT_MANAGEMENT.md`
- **成功パターン**: `docs/successful-workflow-patterns.md`
- **MCP設定**: `docs/mcp/MCP_CONFIGURATION_GUIDE.md`
- **外部API使用パターン**: `docs/external-api-usage-patterns.md`

---

**🤖 Kamui Rossy Meta Workflow Generator System**  
**⚡ Version: v10.0**  
**📅 Last Updated: 2025-08-02**  
**🔄 Status: ミニマルユニットベース動的生成 + 外部API統合 + kamuicode-workflowパターン採用**
## Video Production v8 - Run #16
- **Concept**: テスト：静かな森と朝の光
- **Video URL**: local://projects/video-production-v8-16/final/final_video.mp4
- **Date**: 2025-07-31

## Video Production v8 - Run #23
- **Concept**: AI-powered future city showcase
- **Saved to**: projects/video-v8-run-23-AI-powered-future-city-showcase
- **Date**: 2025-07-31

## Video Production v8 - Run #25
- **Concept**: テクノロジーの未来を紹介する動画
- **Saved to**: projects/video-v8-run-25--
- **Date**: 2025-07-31

## Video Production v8 - Run #29
- **Concept**: テスト動画：美しい夕焼けの風景
- **Saved to**: projects/video-v8-run-29--
- **Date**: 2025-07-31

## Video Production v8 - Run #30
- **Concept**: AIトレンドニュース動画テスト
- **Saved to**: projects/video-v8-run-30-AI-
- **Date**: 2025-08-01

## Video Production v8 - Run #32
- **Concept**: オートファジーの効果
- **Saved to**: projects/video-v8-run-32--
- **Date**: 2025-08-03
