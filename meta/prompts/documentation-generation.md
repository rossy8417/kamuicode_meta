# Documentation Generation Prompt

生成されたワークフローのドキュメントを作成してください。

## 生成するファイル
1. `README.md` - メインドキュメント
2. `docs/SETUP.md` - セットアップガイド
3. `docs/TROUBLESHOOTING.md` - トラブルシューティング

## README.mdの構造
```markdown
# [Workflow Name]

[ワークフローの概要説明]

## 🚀 Features
- [主要機能1]
- [主要機能2]

## 📋 Prerequisites
- Node.js 20+
- Claude Code CLI
- Kamuicode MCP configuration

## 🔧 Setup
See [docs/SETUP.md](docs/SETUP.md) for detailed setup instructions.

## 📖 Usage
### Basic Usage
```bash
# Manual execution
npm run generate

# Specific task execution
npm run task -- task-001
```

### GitHub Actions
The workflow runs automatically when:
- Changes are pushed to `prompts/` or `config/`
- Manually triggered via workflow_dispatch

## 🏗️ Architecture
[タスクフローの説明]

## 🐛 Troubleshooting
See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
```

## セットアップガイドの内容
- 必要な環境変数
- MCP設定の配置方法
- シークレットの設定
- 初回実行の手順

## トラブルシューティングの内容
- よくあるエラーと解決方法
- デバッグモードの使用方法
- ログの確認方法