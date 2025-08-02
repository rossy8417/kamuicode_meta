# Workflow Execution Logs

このディレクトリには、ワークフロー実行時の問題と解決策のログを保存します。

## ログファイル構造

- `execution-log-YYYY-MM-DD.md` - 日付ごとの実行ログ
- `error-solutions.md` - エラーと解決策のカタログ（累積）
- `success-patterns.md` - 成功パターンの記録

## ログフォーマット

```
[TIMESTAMP] [STATUS] [WORKFLOW_NAME]
Issue: 問題の説明
Action: 実行したアクション
Result: 結果
```