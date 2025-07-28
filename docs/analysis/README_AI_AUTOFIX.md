# AI-Powered Auto-Fix System Setup Guide

## 概要
Claude Code SDKを活用した高度な自動修正システムが実装されました。

## 主な改善点

### 1. **AI駆動の深い分析**
- 固定パターンマッチングから、コンテキストを理解するAI分析へ
- エラーログの完全な理解と根本原因の特定
- 信頼度スコアに基づく判断

### 2. **動的な修正生成**
- 事前定義された修正から、状況に応じた修正提案へ
- コード変更の自動実装
- 複数の修正案の並列適用

### 3. **継続的学習**
- インシデントごとの学習データ蓄積
- パターン認識の改善
- 将来の問題予防策の自動生成

## セットアップ方法

### 1. 必要なシークレットの設定

GitHub Secrets に以下を追加してください：

- `CLAUDE_CODE_OAUTH_TOKEN`: Claude Pro/Maxのトークン

### 2. トークンの生成方法

```bash
# ローカルで実行
claude setup-token
# 生成されたトークンをGitHub Secretsに追加
```

### 3. 学習データの初期化

既に初期化済みです：
- `meta/ai-learning/patterns.json` - パターンライブラリ

## 期待される効果

- **修正精度の向上**: 70%以上の信頼度で自動修正
- **学習による改善**: インシデントごとに賢くなる
- **工数削減**: 手動デバッグ時間の大幅削減
- **予防的改善**: 将来の問題を未然に防ぐ提案

## システム構成

### Phase 1: AI-Powered Failure Analysis
- MCPサーバー設定による深いコンテキスト理解
- 失敗ログの完全分析
- Claude Code SDKによるインテリジェント分析

### Phase 2: AI-Driven Fix Implementation  
- 動的修正提案の実装
- コード検証
- 自動PR作成

### Phase 3: AI Learning and Improvement
- インシデントからの学習
- パターンライブラリの更新
- 改善レポートの生成

## 使用されるMCPサーバー

- `@modelcontextprotocol/server-github`: GitHub API統合
- `@modelcontextprotocol/server-filesystem`: ファイルシステムアクセス

## トラブルシューティング

1. **Claude Code SDK未インストール**
   - 自動インストールが実行されます

2. **OAuth Token無効**
   - `claude setup-token`で再生成してください

3. **MCP接続エラー**
   - NPXによる自動インストールが実行されます

## 次回のワークフロー失敗時

システムが自動的に：
1. 失敗を検出・分析
2. AI駆動の修正を提案・実装
3. PRを作成してレビューを依頼
4. 学習データを更新

手動による確認・マージのみが必要です。