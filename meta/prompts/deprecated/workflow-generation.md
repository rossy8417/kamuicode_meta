# Workflow YAML Generation Prompt

提供されたタスクプランに基づいて、GitHub Actionsワークフローを生成してください。

## 生成要件
1. 各タスクを個別のステップまたはジョブとして実装
2. 依存関係を適切に処理
3. エラーハンドリングを組み込み
4. アーティファクトでデータを受け渡し

## ファイル生成
`.github/workflows/generated-[workflow-type].yml` を生成してください。

## ワークフロー構造
```yaml
name: [Descriptive Name]
run-name: ${{ github.actor }} executes [workflow-type] 🚀

on:
  push:
    paths:
      - 'prompts/**'
      - 'config/**'
  workflow_dispatch:
    inputs:
      debug_mode:
        type: boolean
        default: false

env:
  CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}

jobs:
  # 初期化ジョブ
  initialize:
    runs-on: ubuntu-latest
    outputs:
      task_config: ${{ steps.load.outputs.config }}
    steps:
      - uses: actions/checkout@v4
      - id: load
        run: |
          CONFIG=$(cat config/task-plan.json | jq -c .)
          echo "config=$CONFIG" >> $GITHUB_OUTPUT

  # 各タスクを個別のジョブとして実装
  [task-id]:
    needs: [dependencies]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install -g @anthropic-ai/claude-code
      - name: Execute Task
        run: node script/lib/task-executor.js --task [task-id]
      - uses: actions/upload-artifact@v4
        with:
          name: [task-id]-output
          path: output/[task-id]/
```

## 重要な実装詳細
- 並列実行可能なタスクは並列ジョブとして実装
- 各ジョブは独立して再実行可能
- タイムアウトは各タスクの推定時間の2倍に設定
- デバッグモードでは詳細ログを出力