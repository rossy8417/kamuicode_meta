# Workflow Composer Prompt

選択されたミニマルユニットを組み合わせて、完全に実行可能なGitHub Actionsワークフローを構成してください。

## 入力情報
- 選択されたユニット: {{SELECTED_UNITS}}
- 並列最適化戦略: {{PARALLEL_OPTIMIZATION}}
- タスク分解結果: {{TASK_DECOMPOSITION}}
- ワークフローメタデータ: {{WORKFLOW_METADATA}}

## ワークフロー構成原則

### 1. 基本配置パターンの実装
ワークフロー構成の基本パターンを適切に組み合わせ：

#### 直列パターン（Sequential）
```yaml
task-a:
  runs-on: ubuntu-latest
  
task-b:
  needs: [task-a]
  runs-on: ubuntu-latest
  
task-c:
  needs: [task-b]
  runs-on: ubuntu-latest
```

#### 並列パターン（Parallel）
```yaml
parallel-task-1:
  runs-on: ubuntu-latest
  
parallel-task-2:
  runs-on: ubuntu-latest
  
parallel-task-3:
  runs-on: ubuntu-latest
  
merge-results:
  needs: [parallel-task-1, parallel-task-2, parallel-task-3]
  runs-on: ubuntu-latest
```

#### 条件分岐パターン（Conditional）
```yaml
check-condition:
  runs-on: ubuntu-latest
  outputs:
    branch: ${{ steps.check.outputs.branch }}
    
path-a:
  needs: [check-condition]
  if: needs.check-condition.outputs.branch == 'a'
  runs-on: ubuntu-latest
  
path-b:
  needs: [check-condition]
  if: needs.check-condition.outputs.branch == 'b'
  runs-on: ubuntu-latest
```

#### ループパターン（Matrix）
```yaml
process-items:
  strategy:
    matrix:
      item: ${{ fromJSON(needs.prepare.outputs.items) }}
  runs-on: ubuntu-latest
  steps:
    - name: Process ${{ matrix.item }}
      run: echo "Processing ${{ matrix.item }}"
```

### 2. タスク依存関係と実行順序の管理

#### 依存関係の原則
- **前提条件の明確化**: 各タスクの前提となる条件を明示
- **データフローの追跡**: 前タスクの出力を次タスクの入力に確実に接続
- **並列可能性の判断**: 独立したタスクのみ並列実行
- **クリティカルパスの識別**: 全体の完了時間を左右する重要な経路

```yaml
name: "Dynamic Workflow - {{WORKFLOW_TYPE}}"
run-name: "🚀 {{WORKFLOW_DESCRIPTION}} | ${{ github.actor }} | #${{ github.run_number }}"

on:
  workflow_dispatch:
    inputs:
      mode:
        description: '実行モード'
        type: choice
        options: ['standard', 'fast', 'quality']
        default: 'standard'
      
      parallel_scale:
        description: '並列実行規模'
        type: choice
        options: ['3-way', '4-way', '5-way']
        default: '3-way'

jobs:
  # === Phase 1: 準備・初期化 ===
  setup:
    runs-on: ubuntu-latest
    outputs:
      config: ${{ steps.prepare.outputs.config }}
    steps:
      - name: Prepare Environment
        id: prepare
        run: |
          # 環境準備処理
          echo "config={...}" >> $GITHUB_OUTPUT

  # === Phase 2: データ収集（並列実行可能） ===
  collect-data-1:
    runs-on: ubuntu-latest
    needs: [setup]
    # ミニマルユニット統合
    
  collect-data-2:
    runs-on: ubuntu-latest
    needs: [setup]
    # ミニマルユニット統合
    
  # === Phase 3: 処理実行（依存関係あり） ===
  process:
    runs-on: ubuntu-latest
    needs: [collect-data-1, collect-data-2]
    # ミニマルユニット統合
```

### 3. ミニマルユニット統合方法

#### 参照方式（reusable workflow）
```yaml
unit-job:
  uses: ./.github/workflows/minimal-units/category/unit-name.yml
  with:
    input1: ${{ inputs.value }}
    input2: ${{ needs.previous-job.outputs.value }}
  secrets: inherit
```

#### カスタムノードの作成（既存ユニットで対応できない場合）
```yaml
custom-processing:
  runs-on: ubuntu-latest
  needs: [prerequisite-jobs]
  steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Custom Processing
      run: |
        # 既存ユニットにない処理を実装
        # 必要に応じて新しいミニマルユニットとして切り出し可能
```

### 4. 拡張性の確保

#### 動的なユニット選択
```yaml
dynamic-units:
  strategy:
    matrix:
      unit: ${{ fromJSON(needs.analyze.outputs.required_units) }}
  uses: ./.github/workflows/minimal-units/${{ matrix.unit.category }}/${{ matrix.unit.name }}.yml
  with:
    config: ${{ matrix.unit.config }}
```

#### フォールバック処理
```yaml
main-process:
  runs-on: ubuntu-latest
  continue-on-error: true
  # メイン処理
  
fallback-process:
  needs: [main-process]
  if: needs.main-process.outcome == 'failure'
  runs-on: ubuntu-latest
  # 代替処理
```

### 5. kamuicode-workflowパターンの活用

オーケストレーターパターンを参考にしつつ、以下の点で拡張：

```yaml
# セットアップフェーズ（オーケストレーターパターン参考）
setup-branch:
  uses: ./.github/workflows/module-setup-branch.yml
  with:
    concept: ${{ inputs.concept }}
    
# カスタム処理の追加（拡張部分）
custom-analysis:
  needs: [setup-branch]
  runs-on: ubuntu-latest
  steps:
    - name: Custom Analysis Logic
      run: |
        # kamuicode-workflowにない独自の分析処理
```

### 6. エラーハンドリングとリトライ

```yaml
process-with-retry:
  runs-on: ubuntu-latest
  steps:
    - name: First Attempt
      id: attempt1
      continue-on-error: true
      run: |
        # 処理実行
        
    - name: Retry if Failed
      if: steps.attempt1.outcome == 'failure'
      run: |
        # 設定を調整して再試行
```

## 出力要件

1. **GitHub Actions仕様準拠**: 正確なYAML構文とActions仕様への準拠
2. **依存関係の正確性**: すべての依存関係が正しく定義
3. **データフローの完全性**: 出力と入力が適切に接続
4. **拡張可能な構造**: 新しい要求に対応できる柔軟な設計
5. **エラー処理**: 適切なエラーハンドリングとフォールバック

## 品質チェック項目

- [ ] YAML構文の妥当性
- [ ] GitHub Actions仕様への準拠
- [ ] ミニマルユニットの正しい統合
- [ ] 依存関係の整合性
- [ ] 基本パターンの適切な使用
- [ ] 拡張ポイントの確保
- [ ] エラーハンドリングの実装