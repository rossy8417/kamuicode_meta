# Claude Code CLI 設定ファイル群

このディレクトリにはClaude Code CLIセッション用の設定ファイルが含まれています。

## 📁 ファイル構成

### `.claude_mcp_defaults.md`
- **目的**: MCP（Model Control Protocol）ツール用のデフォルト設定
- **内容**: メディア出力ディレクトリルール、標準パラメータ
- **自動適用**: Claude CodeがMCPツール使用時に自動的に参照

### `.env.claude` 
- **目的**: CLI環境変数の定義
- **内容**: デフォルト出力パス、プロジェクト情報
- **使用**: CLIセッション開始時に自動ロード

### `claude_mcp_helpers.md`
- **目的**: MCPツール使用時のヘルパー関数と使用例
- **内容**: 画像・動画・音声・3D生成の設定例
- **言語**: 日本語（ユーザー向け説明）

## 🔧 使用方法

これらのファイルはClaude Code CLIが自動的に読み込むため、手動設定は不要です。

### 自動適用される設定
- **メディア出力先**: `./cli_generated/media/[type]/`
- **ファイル名プレフィックス**: `claude_generated`
- **自動オープン**: `true`

## ⚠️ 注意事項

- これらのファイルはCLI専用です
- GitHub Actionsからは変更しないでください
- 設定変更時は`.claude/settings.local.json`も確認してください

## 🔗 関連ファイル

- **`.claude/settings.local.json`**: CLI権限設定（最終更新: 2025-07-28 17:22）
- **`.claude/mcp-kamuicode.json`**: MCP サービス設定（GitHub Actionsと共有）
- **`cli_generated/`**: CLI生成コンテンツの出力先

# CLI Generated Media Directory

## 📁 メディア出力ディレクトリ構造

```
cli_generated/media/
├── images/     # 画像生成 (T2I, I2I) - Claude Code CLI
├── videos/     # 動画生成 (T2V, I2V, V2V) - Claude Code CLI  
├── audio/      # 音声生成 (T2S, T2M, V2A) - Claude Code CLI
└── 3d/         # 3Dモデル生成 (I23D) - Claude Code CLI
```

## 🎯 GitHub Actions との分離

- **`cli_generated/media/`**: ローカルClaude Code CLI使用時の出力先
- **`generated/media/`**: GitHub Actions等のワークフロー実行時の出力先
- **混在防止**: それぞれ独立した管理で競合を避ける

## 📝 推奨使用方法（Claude Code CLI）

### MCPツール使用時のパラメータ指定
```yaml
# 画像生成
output_directory: "./cli_generated/media/images"

# 動画生成  
output_directory: "./cli_generated/media/videos"

# 音声生成
output_directory: "./cli_generated/media/audio"

# 3Dモデル生成
output_directory: "./cli_generated/media/3d"
```

---
**更新日**: 2025-07-28  
**管理**: CLI環境分離システム