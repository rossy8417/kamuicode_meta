# Workflow Composer Prompt

選択されたミニマルユニットを組み合わせて、完全なGitHub Actionsワークフローを構成してください。

## 入力情報
- 選択されたユニット: {{SELECTED_UNITS}}
- 並列グループ: {{PARALLEL_GROUPS}}
- ワークフローメタデータ: {{WORKFLOW_METADATA}}

## ワークフロー構成ルール

### 1. 基本構造
```yaml
name: Generated Workflow
on:
  workflow_dispatch:
    inputs:
      # 動的に生成される入力パラメータ

jobs:
  # セットアップジョブ
  setup:
    runs-on: ubuntu-latest
    outputs:
      # 必要な出力
    steps:
      # 初期化処理

  # ミニマルユニットから生成されたジョブ
  # ...
```

### 2. ミニマルユニット統合
各ミニマルユニットは以下の方法で統合します：

#### 直接参照方式
```yaml
unit-name:
  uses: ./.github/workflows/minimal-units/category/unit-name.yml
  with:
    input1: ${{ inputs.value }}
    input2: ${{ needs.previous-job.outputs.value }}
  secrets: inherit
```

#### インライン展開方式
ミニマルユニットの内容を直接ワークフローに展開し、以下を調整：
- ジョブ名にプレフィックス追加
- needs関係の調整
- 入出力の接続

### 3. 依存関係の管理
- 依存関係に基づいて`needs:`を設定
- 並列グループは同じ依存を持つように調整
- 出力を次のジョブの入力に接続

### 4. エラーハンドリング
- 各ジョブに`continue-on-error`を適切に設定
- 重要なジョブには再試行ロジックを追加
- フォールバック処理を組み込み

### 5. 最適化
- 並列実行可能なジョブは同時実行
- キャッシュの活用
- アーティファクトの効率的な受け渡し

## 出力要件
1. 完全に実行可能なGitHub Actions YAML
2. すべての入力パラメータが定義済み
3. シークレットの参照が正しい
4. YAML構文が有効
5. ジョブ間の依存関係が正しい

## 品質チェック項目
- [ ] YAML構文の妥当性
- [ ] GitHub Actions仕様への準拠
- [ ] ミニマルユニットの正しい統合
- [ ] 入出力の整合性
- [ ] エラーハンドリングの実装