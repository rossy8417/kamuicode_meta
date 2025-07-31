# Minimal Unit Creation Guide

このガイドでは、Kamui Rossy v9.0のミニマルユニットを作成する方法を説明します。

## ミニマルユニットとは

ミニマルユニットは、再利用可能な最小単位のGitHub Actionsワークフローコンポーネントです。各ユニットは単一の明確な目的を持ち、他のユニットと組み合わせて複雑なワークフローを構築できます。

## 基本構造

### ファイル配置
```
minimal-units/
├── category/           # カテゴリディレクトリ
│   └── unit-name.yml   # ユニットファイル
```

### YAMLテンプレート
```yaml
name: Unit Name
description: |
  ユニットの詳細な説明
  - 何をするユニットか
  - どのような入力を受け取るか
  - どのような出力を生成するか

on:
  workflow_call:
    inputs:
      # 必須入力
      required_input:
        description: '必須入力の説明'
        required: true
        type: string
      
      # オプション入力
      optional_input:
        description: 'オプション入力の説明'
        required: false
        type: string
        default: 'default_value'
    
    outputs:
      # 出力定義
      output_name:
        description: '出力の説明'
        value: ${{ jobs.main.outputs.result }}

jobs:
  main:
    runs-on: ubuntu-latest
    outputs:
      result: ${{ steps.process.outputs.value }}
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Process
        id: process
        run: |
          # 処理ロジック
          echo "value=result" >> $GITHUB_OUTPUT
```

## 設計原則

### 1. 単一責任の原則
- 各ユニットは1つの明確な目的のみを持つ
- 複雑な処理は複数のユニットに分割

### 2. 依存関係の明確化
```yaml
# 良い例：依存関係が明確
inputs:
  image_path:
    description: '処理する画像のパス'
    required: true
    type: string
  
outputs:
  processed_image_path:
    description: '処理済み画像のパス'
    value: ${{ jobs.main.outputs.path }}
```

### 3. エラーハンドリング
```yaml
steps:
  - name: Process with Error Handling
    id: process
    run: |
      set -e  # エラー時に停止
      
      # 入力検証
      if [ -z "${{ inputs.required_input }}" ]; then
        echo "Error: required_input is empty"
        exit 1
      fi
      
      # 処理実行
      # ...
    continue-on-error: false
```

### 4. 再利用性の確保
- 環境依存を最小限に
- 汎用的なパラメータ名を使用
- デフォルト値の適切な設定

## カテゴリ別ガイドライン

### 画像処理ユニット (image/)
- 入力: prompt, style, quality設定など
- 出力: 生成画像のパス、メタデータ
- 例: t2i-imagen3.yml, image-analysis.yml

### 動画処理ユニット (video/)
- 入力: 動画設定、継続時間、スタイル
- 出力: 動画ファイルパス、サムネイル
- 例: t2v-veo3.yml, video-concat.yml

### 音声処理ユニット (audio/)
- 入力: テキスト、音声設定、言語
- 出力: 音声ファイルパス、字幕データ
- 例: t2s-google.yml, bgm-overlay.yml

### 企画・分析ユニット (planning/)
- 入力: 分析対象、クエリ、設定
- 出力: 分析結果、レポート、推奨事項
- 例: planning-ccsdk.yml, web-search.yml

### ユーティリティユニット (utility/)
- 入力: ファイルパス、設定
- 出力: 処理結果、ステータス
- 例: local-save.yml, git-pr-create.yml

## MCP統合パターン

### MCP呼び出しの標準化
```yaml
- name: Call MCP Service
  run: |
    # MCP呼び出しの準備
    MCP_REQUEST=$(cat << 'EOF'
    {
      "prompt": "${{ inputs.prompt }}",
      "settings": {
        "quality": "${{ inputs.quality }}",
        "style": "${{ inputs.style }}"
      }
    }
    EOF
    )
    
    # MCP実行
    npx @claude/mcp call "${{ inputs.mcp_service }}" \
      --input "$MCP_REQUEST" \
      --output result.json
```

## テストとデバッグ

### ユニットテスト
```yaml
# test-workflows/test-unit-name.yml
name: Test Unit Name
on:
  workflow_dispatch:

jobs:
  test:
    uses: ./minimal-units/category/unit-name.yml
    with:
      required_input: "test_value"
    secrets: inherit
```

### デバッグ出力
```yaml
- name: Debug Information
  if: ${{ inputs.debug == 'true' }}
  run: |
    echo "::debug::Input values:"
    echo "::debug::  required_input: ${{ inputs.required_input }}"
    echo "::debug::  optional_input: ${{ inputs.optional_input }}"
```

## ベストプラクティス

### 1. 命名規則
- ファイル名: `action-target.yml` (例: `t2i-imagen3.yml`)
- ジョブ名: 明確で説明的な名前
- ステップ名: 処理内容を表す動詞で開始

### 2. ドキュメント
- 各ユニットに詳細な説明を含める
- 入出力の例を提供
- 制限事項や注意点を明記

### 3. バージョン管理
- 破壊的変更は避ける
- 新機能は後方互換性を保つ
- 変更履歴をコメントで記録

### 4. パフォーマンス
- 不要な処理を避ける
- キャッシュを活用
- 並列処理可能な部分を識別

## チェックリスト

新しいミニマルユニットを作成する際のチェックリスト：

- [ ] 単一の明確な目的を持っているか
- [ ] 入出力が明確に定義されているか
- [ ] エラーハンドリングが適切か
- [ ] 他のユニットとの連携が考慮されているか
- [ ] テストワークフローを作成したか
- [ ] ドキュメントが十分か
- [ ] 命名規則に従っているか
- [ ] カタログに追加したか

## 例：新しい画像処理ユニットの作成

```yaml
# minimal-units/image/enhance-quality.yml
name: Enhance Image Quality
description: |
  画像の品質を向上させるユニット
  - 入力: 元画像のパス
  - 処理: AIによる品質向上
  - 出力: 高品質画像のパス

on:
  workflow_call:
    inputs:
      image_path:
        description: '品質向上する画像のパス'
        required: true
        type: string
      
      enhancement_level:
        description: '品質向上レベル (low/medium/high)'
        required: false
        type: string
        default: 'medium'
    
    outputs:
      enhanced_image_path:
        description: '品質向上後の画像パス'
        value: ${{ jobs.enhance.outputs.path }}

jobs:
  enhance:
    runs-on: ubuntu-latest
    outputs:
      path: ${{ steps.enhance.outputs.enhanced_path }}
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Validate Input
        run: |
          if [ ! -f "${{ inputs.image_path }}" ]; then
            echo "Error: Image file not found"
            exit 1
          fi
      
      - name: Enhance Image
        id: enhance
        run: |
          # 品質向上処理
          INPUT_PATH="${{ inputs.image_path }}"
          OUTPUT_PATH="enhanced_$(basename "$INPUT_PATH")"
          
          # AIサービス呼び出し（例）
          # ... 実際の処理 ...
          
          echo "enhanced_path=$OUTPUT_PATH" >> $GITHUB_OUTPUT
      
      - name: Upload Result
        uses: actions/upload-artifact@v4
        with:
          name: enhanced-image
          path: ${{ steps.enhance.outputs.enhanced_path }}
```

このガイドラインに従って、再利用可能で高品質なミニマルユニットを作成してください。