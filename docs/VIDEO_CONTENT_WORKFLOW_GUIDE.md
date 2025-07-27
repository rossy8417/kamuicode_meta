# Video Content Creation Production Workflow ガイド

## 概要
このワークフローは、リポジトリの `.claude/mcp-kamuicode.json` を使用してMCPサービスのURLを隠蔽しています。

## 特徴

### 1. URLの隠蔽
```yaml
mcp_config: ".claude/mcp-kamuicode.json"  # リポジトリの設定を使用
```
- ワークフローファイルにMCPサービスのURLを直接記載しない
- `.claude/mcp-kamuicode.json` に全てのMCP設定が含まれている

### 2. System Promptの使用
```yaml
system_prompt: |
  You are Claude Code in CI/CD. All MCP tools are pre-authorized.
```
- MCP権限を自動的に承認する設定

### 3. 完全なワークフロー
1. **Setup**: MCP設定ファイルの存在確認
2. **Concept Planning**: 動画コンセプトの詳細計画
3. **Image Generation**: 各シーンの画像生成（1:1デフォルト）
4. **Audio Generation**: BGM生成
5. **Video Generation**: 画像から動画生成（I2V）
6. **Final Package**: 最終パッケージ作成

## 使用方法

1. **ワークフローの実行**
   ```bash
   gh workflow run video-content-creation-production.yml \
     -f video_concept="製品紹介動画" \
     -f target_audience="professional" \
     -f video_length="30" \
     -f video_style="commercial" \
     -f quality_setting="high"
   ```

2. **結果の確認**
   - GitHub Actions ページで実行状況を確認
   - `final-package-{run_number}` アーティファクトをダウンロード

## 必要な設定

1. **Secrets**
   - `CLAUDE_CODE_OAUTH_TOKEN`: Claude Code認証トークン

2. **ファイル**
   - `.claude/mcp-kamuicode.json`: MCP設定（リポジトリに含まれている）

## セキュリティ

- MCPサービスのURLはリポジトリの設定ファイルに集約
- ワークフローファイルには機密情報を含まない
- OAuth tokenはGitHub Secretsで管理