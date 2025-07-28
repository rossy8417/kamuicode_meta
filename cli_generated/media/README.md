# CLI Generated Media Directory

このディレクトリは、**ローカルのClaude Code CLI**で生成されたメディアファイル専用です。

## Directory Structure

```
cli_generated/media/
├── images/     # 画像生成 (T2I, I2I) - Claude Code CLI
├── videos/     # 動画生成 (T2V, I2V, V2V) - Claude Code CLI  
├── audio/      # 音声生成 (T2S, T2M, V2A) - Claude Code CLI
└── 3d/         # 3Dモデル生成 (I23D) - Claude Code CLI
```

## vs generated/media/ ディレクトリとの違い

- **`cli_generated/media/`**: ローカルClaude Code CLI使用時の出力先
- **`generated/media/`**: GitHub Actions等のワークフロー実行時の出力先

## 推奨使用方法（Claude Code CLI）

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

これで、GitHub ActionsのワークフローとClaude Code CLIの出力が混在しません！