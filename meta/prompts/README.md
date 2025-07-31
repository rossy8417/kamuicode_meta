# Meta Workflow Prompts

Meta Workflow Executor v8.1 で使用されるプロンプトファイルの管理ディレクトリです。

## 📁 ディレクトリ構造

```
meta/prompts/
├── README.md                    # このファイル
├── active/                      # アクティブなプロンプト（v8.1で使用中）
│   ├── stepback-question-generator.md
│   ├── stepback-answer-summarizer.md
│   └── stepback-to-tasks.md
├── templates/                   # テンプレートファイル
│   └── task-prompt-template.md
└── deprecated/                  # 非アクティブなプロンプト
    ├── minimal-unit-selector.md
    └── workflow-composer.md
```

## 📁 アクティブなプロンプト（active/）

### **stepback-question-generator.md**
- **用途**: ユーザーのワークフロー要求を分析し、詳細化のための質問を動的生成
- **使用場面**: Issue作成時の要求分析
- **出力先**: `generated/metadata/stepback-analysis/generated-questions.md`
- **実装状況**: ✅ v8.1で使用中

### **stepback-answer-summarizer.md**
- **用途**: ユーザーの詳細回答を GitHub Actions 抽出用の簡潔形式に要約
- **使用場面**: ワークフロー生成前の回答処理
- **出力形式**: `Q[1-5]回答:` パターン
- **実装状況**: ✅ v8.1で使用中

### **stepback-to-tasks.md** ⭐ NEW
- **用途**: ステップバック回答を分析して、ユーザー要求に最適化されたタスクプランを生成
- **使用場面**: タスク分解ジョブでのClaude Code実行
- **出力先**: `generated/metadata/task-decomposition/task-plan.json`
- **実装状況**: ✅ v8.1で追加（動的タスク分解対応）

## 📂 テンプレート（templates/）

### **task-prompt-template.md**
- **用途**: 個別タスク実行用のプロンプトテンプレート
- **変数**: `{{task_name}}`, `{{task_description}}` など
- **実装状況**: 🔄 将来の機能拡張用

## 🗂️ 非アクティブなプロンプト（deprecated/）

v8.1アーキテクチャで使用されなくなったプロンプトファイルが保管されています：

### **minimal-unit-selector.md**
- **旧用途**: 53個のミニマルユニットから適切なものを選択
- **廃止理由**: v8.1でのテンプレート選択方式への移行
- **移行日**: 2025-07-31

### **workflow-composer.md**  
- **旧用途**: 選択されたミニマルユニットを組み合わせてワークフロー構成
- **廃止理由**: echo-based直接生成方式への移行
- **移行日**: 2025-07-31

## 🔄 Meta Workflow v8.1 での使用フロー

```mermaid
graph TD
    A[Issue作成] --> B[stepback-question-generator.md]
    B --> C[ユーザー回答]
    C --> D[stepback-answer-summarizer.md]
    D --> E[Meta Workflow実行]
    E --> F[stepback-to-tasks.md]
    F --> G{Claude Code利用可能?}
    G -->|Yes| H[動的タスク分解]
    G -->|No| I[フォールバック静的分解]
    H --> J[ユーザー要求反映タスクプラン]
    I --> K[固定的タスクプラン]
    J --> L[3アプローチ生成]
    K --> L
    L --> M[最終ワークフロー出力]
    
    style B fill:#e8f5e8
    style D fill:#e8f5e8
    style F fill:#f0f8ff
    style H fill:#e8f5e8
    style J fill:#f0fff0
```

## 📝 プロンプト追加ガイドライン

新しいプロンプトファイルを追加する際は：

1. **明確な用途**: 何のために使用されるかを明記
2. **出力先指定**: `generated/metadata/` 以下の適切な場所
3. **変数定義**: `{{variable_name}}` 形式で統一
4. **エラーハンドリング**: フォールバック戦略を含める
5. **ドキュメント更新**: このREADMEと`CLAUDE.md`に追記

## 🔧 メンテナンス

- **定期見直し**: 四半期ごとに使用状況を確認
- **廃止プロンプト**: deprecated/ ディレクトリに移動
- **バージョン管理**: メジャーアップデート時に構造見直し

---

**Meta Workflow Executor v8.1**  
**Last Updated**: 2025-07-27