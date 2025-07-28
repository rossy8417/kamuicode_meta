# Meta Workflow Generator System (Kamui Rossy)

🤖 **Claude Code GitHub Actions統合**によるメタワークフロージェネレーターシステム

## 🎯 概要

このシステムは、ユーザーのリクエストに基づいて完全なワークフローを自動生成するメタワークフロージェネレーターです。**テンプレートベース生成**と**段階的デプロイシステム**により、高品質で実行可能なGitHub Actionsワークフローを効率的に生成します。

## 🏗️ アーキテクチャ v8.1

### **テンプレートベース・メタワークフローシステム**
- **テンプレート選択**: 複雑なタスク分解の代わりに`meta/examples/`の15個の参考ワークフローを使用
- **簡素化3段階デプロイ**: 生成 → 検証 → デプロイ（.disabled安全機構付き）
- **プロンプト分離**: すべてのプロンプトは`meta/prompts/`で外部管理
- **小さなノード**: 各ジョブが単一責任を持ち、独立した再実行が可能
- **品質検証**: YAML構文、GitHub Actions構造、MCP参照、依存関係チェック

### **核心コンポーネント**
- **`meta/examples/`**: 15種類のGitHub Actionsワークフローテンプレート
- **`.github/workflows/meta-workflow-executor-v8.yml`**: メインメタワークフロー（v8.1、重要システム修復プロトコル付き）
- **`.github/workflows/auto-fix-deployment.yml`**: 自動デプロイ・エラー回復システム
- **`.github/workflows/continuous-system-monitor.yml`**: システム健全性監視
- **`meta/prompts/`**: タスク分解、ワークフロー生成、スクリプト生成、ドキュメント用プロンプト

## 📁 ディレクトリ構成

```
📦 Kamui Rossy
├── 🤖 .github/workflows/
│   ├── meta-workflow-executor-v8.yml          # メインメタワークフロー v8.1
│   ├── auto-fix-deployment.yml                # 自動修復システム
│   ├── continuous-system-monitor.yml          # 連続監視システム
│   └── generated/                             # 生成ワークフロー配置
│       ├── staging/     # 検証済み (.disabled)
│       ├── active/      # 本番稼働中
│       └── archive/     # 履歴保存
│
├── 📋 meta/
│   ├── examples/        # 15個のワークフローテンプレート
│   │   ├── video-content-creation.yml         # 動画制作 (14タスク)
│   │   ├── multimedia-ad-campaign.yml         # マルチメディア広告 (16タスク)
│   │   ├── 3d-model-creation.yml             # 3Dモデル生成 (10タスク)
│   │   ├── image-generation.yml              # 画像生成 (8タスク)
│   │   ├── audio-music-creation.yml          # 音楽制作 (11タスク)
│   │   ├── presentation-slide-creation.yml   # プレゼン作成 (12タスク)
│   │   ├── data-analysis-visualization.yml   # データ分析 (8タスク)
│   │   └── ...他8個のテンプレート
│   └── prompts/         # プロンプトファイル群
│       ├── stepback-question-generator.md
│       ├── stepback-answer-summarizer.md
│       ├── stepback-to-tasks.md
│       └── task-prompt-template.md
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

### **共有設定**
- **`.claude/mcp-kamuicode.json`**: MCP サービス設定（GitHub Actions・CLI共用）

### **CLI専用設定**
- **`cli_config/.claude_mcp_defaults.md`**: CLI用デフォルト設定
- **`cli_config/claude_mcp_helpers.md`**: 使用例・ヘルパー関数

### **利用可能サービス**
- **T2I**: 画像生成 (Google Imagen3, Fal.ai等)
- **T2V**: 動画生成 (Veo3, Hailuo等)
- **T2M**: 音楽生成 (Google Lyria等)
- **I2V, V2V, V2A, I2I3D**: その他マルチモーダル生成サービス

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

- **アーキテクチャ**: v8.1（重要システム修復プロトコル搭載）
- **テンプレート**: 15個（video, 3D, audio, image, blog, data analysis等）
- **成功率**: 12/12ジョブ 100%成功（過去実績）
- **CLI環境**: アクティブ（2025-07-28 17:22）

## 🔗 重要リンク

- **システム管理**: `docs/system/CLEANUP_PROTOCOL.md`
- **CLI環境管理**: `docs/system/CLI_ENVIRONMENT_MANAGEMENT.md`
- **成功パターン**: `docs/successful-workflow-patterns.md`
- **MCP設定**: `docs/mcp/MCP_CONFIGURATION_GUIDE.md`

---

**🤖 Kamui Rossy Meta Workflow Generator System**  
**⚡ Version: v8.1**  
**📅 Last Updated: 2025-07-28**  
**🔄 Status: CLI環境アクティブ + GitHub Actions統合稼働中**