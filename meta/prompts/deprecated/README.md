# Deprecated Prompts

このディレクトリには、Meta Workflow Executor v8.1 で使用されなくなったプロンプトファイルが含まれています。

## 移動されたファイル

| ファイル | 理由 | 代替方法 |
|---------|------|----------|
| `task-decomposition.md` | v8.1では3アプローチ生成でフォールバックJSONを使用 | メタワークフロー内のケース分岐ロジック |
| `workflow-generation.md` | v8.1では直接GitHub Actions形式で生成 | echo-based generation in meta workflow |
| `script-generation.md` | JavaScript実行エンジンは未実装 | GitHub Actions直接実行 |
| `documentation-generation.md` | 自動ドキュメント生成は実装されていない | 手動README.md作成 |

## 保持理由

これらのファイルは将来の機能拡張時に参考として使用される可能性があるため、削除ではなく移動として保持しています。

## v8.1で使用中のプロンプト

- `stepback-question-generator.md` - ステップバック質問の動的生成
- `stepback-answer-summarizer.md` - 回答の簡潔化処理
- `templates/task-prompt-template.md` - タスク用テンプレート（将来用）

---

**Deprecated in Meta Workflow Executor v8.1**  
**Date**: 2025-07-27