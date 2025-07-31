# Meta Workflow Generator System (Kamui Rossy)

🤖 **Claude Code GitHub Actions統合**によるメタワークフロージェネレーターシステム

## 🎯 概要

このシステムは、ユーザーのリクエストに基づいて完全なワークフローを自動生成するメタワークフロージェネレーターです。**ミニマルユニットベース動的構築**と**段階的デプロイシステム**により、高品質で実行可能なGitHub Actionsワークフローを効率的に生成します。

## 🏗️ アーキテクチャ v9.0

### **ミニマルユニットベース・動的メタワークフローシステム**
- **Claude Code SDK中心**: ユーザー要求を分析し、タスクを動的に分解
- **ミニマルユニット構築**: `minimal-units/`の再利用可能な部品を組み合わせてワークフロー構築
- **基本配置パターン**: 直列・並列・条件分岐・ループ処理の基本パターンを実装
- **参考パターン活用**: kamuicode-workflowのオーケストレーターを参考にしつつ独自拡張
- **動的配置**: 並列処理、条件分岐、ループ処理を要求に応じて自動判断
- **拡張可能**: 新しいユニットやカスタムノードを必要に応じて作成・統合
- **タスク依存関係管理**: データフローと前提条件に基づく厳密な実行順序
- **最適並列処理**: 3-5項並列を依存関係を考慮して自動配置
- **品質検証**: YAML構文、GitHub Actions構造、MCP参照、依存関係チェック

### **核心コンポーネント**
- **`minimal-units/`**: 55個の再利用可能なワークフロー部品（画像、動画、音声、企画等）
- **`kamuicode-workflow/`**: 参考となるオーケストレーター・モジュールパターン
- **`.github/workflows/meta-workflow-executor-v9.yml`**: Claude Code SDKベースの動的メタワークフロー
- **`.github/workflows/auto-fix-deployment.yml`**: 自動デプロイ・エラー回復システム
- **`.github/workflows/continuous-system-monitor.yml`**: システム健全性監視
- **`meta/prompts/`**: タスク分解、ユニット選択、ワークフロー生成用プロンプト

## 📁 ディレクトリ構成

```
📦 Kamui Rossy
├── 🤖 .github/workflows/
│   ├── meta-workflow-executor-v9.yml          # 動的メタワークフロー v9.0
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

- **アーキテクチャ**: v9.0（ミニマルユニットベース動的生成）
- **ミニマルユニット**: 55個（画像8、動画13、音声10、企画9、他）
- **参考パターン**: kamuicode-workflowオーケストレーター
- **CLI環境**: アクティブ（2025-07-28 17:22）

## 🔗 重要リンク

- **システム管理**: `docs/system/CLEANUP_PROTOCOL.md`
- **CLI環境管理**: `docs/system/CLI_ENVIRONMENT_MANAGEMENT.md`
- **成功パターン**: `docs/successful-workflow-patterns.md`
- **MCP設定**: `docs/mcp/MCP_CONFIGURATION_GUIDE.md`

---

**🤖 Kamui Rossy Meta Workflow Generator System**  
**⚡ Version: v9.0**  
**📅 Last Updated: 2025-07-31**  
**🔄 Status: ミニマルユニットベース動的生成 + kamuicode-workflowパターン採用**
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
