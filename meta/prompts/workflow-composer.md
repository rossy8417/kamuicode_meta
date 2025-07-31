# Human-like Workflow Composer Prompt

選択されたミニマルユニットを組み合わせて、人間が作成したような自然で詳細なGitHub Actionsワークフローを構成してください。

## 入力情報
- 選択されたユニット: {{SELECTED_UNITS}}
- 並列最適化戦略: {{PARALLEL_OPTIMIZATION}}
- タスク分解結果: {{TASK_DECOMPOSITION}}
- ワークフローメタデータ: {{WORKFLOW_METADATA}}

## ワークフロー構成原則

### 1. タスク依存関係と実行順序の厳密な管理
人間の思考プロセスに基づいた正確なタスク順序：

#### 依存関係の原則
- **前提条件の明確化**: 各タスクの前提となる条件を明示
- **データフローの追跡**: 前タスクの出力を次タスクの入力に確実に接続
- **並列可能性の判断**: 独立したタスクのみ並列実行
- **クリティカルパスの識別**: 全体の完了時間を左右する重要な経路

```yaml
name: "Human-like Workflow - {{WORKFLOW_TYPE}}"
run-name: "🚀 {{WORKFLOW_DESCRIPTION}} | ${{ github.actor }} | #${{ github.run_number }}"

on:
  workflow_dispatch:
    inputs:
      # Phase 1: 準備・計画
      planning_detail:
        description: '計画の詳細度'
        type: choice
        options: ['quick', 'standard', 'thorough']
        default: 'standard'
      
      # Phase 2: 実行設定
      quality_mode:
        description: '品質優先度'
        type: choice
        options: ['speed-first', 'balanced', 'quality-first']
        default: 'balanced'
      
      # Phase 3: 並列処理
      parallel_scale:
        description: '並列実行規模'
        type: choice
        options: ['conservative-3way', 'moderate-4way', 'aggressive-5way']
        default: 'moderate-4way'

jobs:
  # === Phase 1: 準備・調査フェーズ（3項並列） ===
  setup-environment:
    name: "🔧 環境セットアップ"
    runs-on: ubuntu-latest
    outputs:
      setup_complete: ${{ steps.verify.outputs.ready }}
    steps:
      - name: "環境準備"
        run: echo "Setting up environment..."

  research-references:
    name: "🔍 参考情報リサーチ"
    runs-on: ubuntu-latest
    outputs:
      references: ${{ steps.collect.outputs.refs }}
    steps:
      - name: "情報収集"
        run: echo "Researching references..."

  analyze-requirements:
    name: "📊 要件分析"
    runs-on: ubuntu-latest
    outputs:
      analysis: ${{ steps.analyze.outputs.result }}
    steps:
      - name: "詳細分析"
        run: echo "Analyzing requirements..."

  # === Phase 2: メイン処理フェーズ（4-5項並列） ===
  generate-variation-1:
    name: "🎨 バリエーション1生成"
    needs: [setup-environment, research-references, analyze-requirements]
    runs-on: ubuntu-latest
    # ... ミニマルユニット統合

  # === Phase 3: 品質確認フェーズ ===
  quality-check:
    name: "✅ 品質チェック"
    needs: [all-generation-jobs]
    runs-on: ubuntu-latest
    # ... 品質検証処理

  # === Phase 4: 最終調整フェーズ ===
  final-polish:
    name: "✨ 最終仕上げ"
    needs: [quality-check]
    runs-on: ubuntu-latest
    # ... 最終調整処理
```

### 2. タスク依存関係の正確な実装

#### 依存関係の明示的な定義
```yaml
# 正確な依存関係チェーン
prepare-assets:
  name: "Prepare Assets"
  runs-on: ubuntu-latest
  outputs:
    assets_ready: ${{ steps.prepare.outputs.ready }}

analyze-requirements:
  name: "Analyze Requirements"  
  needs: [prepare-assets]  # 前タスクの完了が必須
  runs-on: ubuntu-latest

generate-content:
  name: "Generate Content"
  needs: [analyze-requirements]  # 分析完了後に実行
  runs-on: ubuntu-latest
```

#### ミニマルユニット統合の仕様準拠
```yaml
# GitHub Actions仕様に準拠した統合
integration-job:
  uses: ./.github/workflows/minimal-units/image/t2i-imagen3.yml
  with:
    prompt: ${{ needs.prepare.outputs.prompt }}
    settings: ${{ needs.analyze.outputs.config }}
  secrets: inherit
```

#### 詳細なステップ説明
```yaml
research-visual-style:
  name: "🔍 ビジュアルスタイルのリサーチ"
  runs-on: ubuntu-latest
  steps:
    - name: "参考画像の収集"
      run: echo "Collecting reference images..."
    
    - name: "スタイル分析"
      run: echo "Analyzing visual styles..."
    
    - name: "ムードボード作成"
      run: echo "Creating mood board..."
```

### 3. タスク実行順序とタイミングの最適化

#### 依存関係に基づく実行順序
```yaml
# Phase 1: データ収集（並列可能）
collect-user-data:
  runs-on: ubuntu-latest
  
collect-reference-data:
  runs-on: ubuntu-latest
  
# Phase 2: 分析（Phase 1完了後）
analyze-all-data:
  needs: [collect-user-data, collect-reference-data]
  runs-on: ubuntu-latest
  
# Phase 3: 生成準備（分析結果に依存）
prepare-generation-config:
  needs: [analyze-all-data]
  runs-on: ubuntu-latest
  
# Phase 4: 並列生成（設定完了後）
generate-variant-1:
  needs: [prepare-generation-config]
  runs-on: ubuntu-latest
  
generate-variant-2:
  needs: [prepare-generation-config]
  runs-on: ubuntu-latest
```

#### 並列処理の実装（依存関係を考慮）

##### 3項並列（独立タスクのみ）
```yaml
# 相互依存のない調査タスクを同時実行
parallel-research:
  strategy:
    matrix:
      include:
        - task: web-search
          query: "latest trends"
        - task: image-analysis  
          source: "reference_images"
        - task: market-research
          scope: "target_audience"
```

##### 4項並列（同一前提条件のタスク）
```yaml
# 同じ設定データを使う生成タスクを並列化
generate-variations:
  needs: [prepare-generation-config]
  strategy:
    matrix:
      variant: [style-a, style-b, style-c, style-d]
```

##### 条件付き並列（動的な並列数）
```yaml
# 分析結果に基づいて並列数を調整
dynamic-generation:
  needs: [analyze-all-data]
  strategy:
    matrix:
      task: ${{ fromJSON(needs.analyze-all-data.outputs.parallel_tasks) }}
```

### 4. 人間的な進捗表示
```yaml
steps:
  - name: "📊 進捗: 25% - 初期化完了"
    run: echo "::notice title=Progress::Phase 1 of 4 completed"
  
  - name: "📊 進捗: 50% - 生成処理中"
    run: echo "::notice title=Progress::Phase 2 of 4 in progress"
  
  - name: "📊 進捗: 75% - 品質確認中"
    run: echo "::notice title=Progress::Phase 3 of 4 running"
  
  - name: "📊 進捗: 100% - 完了"
    run: echo "::notice title=Progress::All phases completed!"
```

### 5. エラーハンドリングと再試行
```yaml
generate-with-retry:
  name: "🔄 生成処理（再試行付き）"
  runs-on: ubuntu-latest
  steps:
    - name: "初回試行"
      id: first_attempt
      continue-on-error: true
      run: |
        # 生成処理
        
    - name: "再試行（必要時）"
      if: steps.first_attempt.outcome == 'failure'
      run: |
        echo "::warning::初回失敗、設定を調整して再試行..."
        # 調整した設定で再試行
```

### 6. 最終成果物の整理
```yaml
organize-deliverables:
  name: "📦 成果物の整理"
  needs: [all-processing-jobs]
  runs-on: ubuntu-latest
  steps:
    - name: "ファイル整理"
      run: |
        mkdir -p final/images final/videos final/documents
        
    - name: "メタデータ生成"
      run: |
        echo "Generating metadata..."
        
    - name: "最終レポート作成"
      run: |
        echo "Creating final report..."
```

## 出力要件
1. 人間が理解しやすい構造とコメント
2. 詳細な進捗表示とログ
3. 適切なエラーメッセージ
4. 並列処理の最適な実装
5. 成果物の整理された出力

## 品質チェック項目
- [ ] 人間的な命名規則の使用
- [ ] 自然なフェーズ分割
- [ ] 適切な並列処理（3-5項）
- [ ] 詳細な進捗表示
- [ ] 包括的なエラーハンドリング
- [ ] 成果物の整理