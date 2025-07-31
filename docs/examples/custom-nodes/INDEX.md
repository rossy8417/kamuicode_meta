# Custom Node Examples Index

Meta Workflow Generator System で使用可能な**カスタムノード実装例**の一覧です。

## 📂 Available Examples

### 🎨 Media Processing
| ファイル | 用途 | 適用場面 |
|---------|------|----------|
| **multi-format-generator.yml** | 同一コンテンツの複数フォーマット生成 | 画像・動画・音声を同時生成する場合 |

**特徴**: 3つのメディアフォーマットを並列生成し、品質チェック・最適化・統合までを自動化

### 📊 Data Processing  
| ファイル | 用途 | 適用場面 |
|---------|------|----------|
| **batch-processor.yml** | 大量データの分割バッチ処理 | 数十〜数百のアイテムを効率的に処理する場合 |

**特徴**: Matrix戦略を使用した5並列バッチ処理、失敗時の部分結果保存、統合レポート生成

### 🌐 External Integration
| ファイル | 用途 | 適用場面 |
|---------|------|----------|
| **api-aggregator.yml** | 複数外部APIからの情報収集・統合 | 市場調査、競合分析、トレンド分析が必要な場合 |

**特徴**: ニュース・ソーシャル・市場・技術データの並列収集、品質評価、インサイト生成

### 🔧 Utilities
| ファイル | 用途 | 適用場面 |
|---------|------|----------|
| **health-checker.yml** | システム・サービスヘルスチェック | ワークフロー実行前後の状態確認が必要な場合 |

**特徴**: システムリソース・MCPサービス・ネットワーク・依存関係の包括的チェック

## 🎯 Selection Guide

### 処理タイプ別の選択

#### **大量処理が必要** → `batch-processor.yml`
- 10個以上のアイテムを処理
- 処理時間の最適化が重要
- 部分的な失敗を許容できる

#### **複数メディア形式が必要** → `multi-format-generator.yml`  
- 1つのコンセプトから複数フォーマット生成
- フォーマット間の整合性が重要
- 品質の統一性が必要

#### **外部データ収集が必要** → `api-aggregator.yml`
- 複数のデータソースから情報収集
- データの信頼性評価が重要
- インサイト生成が必要

#### **システム安定性が重要** → `health-checker.yml`
- 高信頼性ワークフローの実行前
- 定期的なシステム監視
- 障害の早期発見

### 統合パターン

#### **前処理として使用**
```yaml
jobs:
  health-check:
    uses: ./docs/examples/custom-nodes/utilities/health-checker.yml
    
  main-processing:
    needs: [health-check]
    if: needs.health-check.outputs.system_status == 'healthy'
    # メイン処理
```

#### **並列処理として使用**  
```yaml
jobs:
  data-collection:
    uses: ./docs/examples/custom-nodes/external-integration/api-aggregator.yml
    
  content-generation:
    uses: ./docs/examples/custom-nodes/media-processing/multi-format-generator.yml
    
  integration:
    needs: [data-collection, content-generation]
    # 統合処理
```

#### **大量処理として使用**
```yaml
jobs:
  prepare-items:
    # アイテム準備
    
  batch-process:
    uses: ./docs/examples/custom-nodes/data-processing/batch-processor.yml
    needs: [prepare-items]
```

## 🔄 Customization Guidelines

### 基本的なカスタマイズ手順

1. **適切な例をベースに選択**
2. **入力パラメータの調整**
3. **処理ロジックの修正**
4. **出力フォーマットの統一**
5. **エラーハンドリングの適用**

### 共通パターンの活用

#### **環境セットアップ**
```yaml
- name: Setup Environment
  run: |
    mkdir -p projects/current-session/custom-processing/
    echo "PROCESSING_DIR=projects/current-session/custom-processing" >> $GITHUB_ENV
```

#### **品質チェック**
```yaml
- name: Quality Assessment
  run: |
    QUALITY_SCORE=0
    # 品質評価ロジック
    echo "quality_score=$QUALITY_SCORE" >> $GITHUB_OUTPUT
```

#### **エラーハンドリング**
```yaml
- name: Error Recovery
  if: failure()
  run: |
    # 部分的結果の保存
    # エラーレポートの生成
```

## 📈 Evolution to Minimal Units

カスタムノードが汎用的で再利用価値が高い場合、ミニマルユニット化を検討：

1. **汎用性の評価**: 複数のプロジェクトで使用可能か
2. **パラメータ化**: 設定可能なパラメータの整理
3. **ドキュメント作成**: 用途と使用方法の明記
4. **テスト実装**: 様々な条件でのテスト
5. **minimal-units/への統合**: 適切なカテゴリに配置

## 🛠️ Development Tips

### **効率的な開発**
- 既存の例から開始
- 段階的な機能追加
- 小さな単位でのテスト

### **品質保証**
- エラーハンドリングの実装
- 出力フォーマットの統一
- ドキュメントの整備

### **保守性**  
- 明確な変数名
- 適切なコメント
- モジュール化された構造

---

**Meta Workflow Generator System v9.0**  
**Created**: 2025-07-31  
**Examples**: 4 categories, 4 implementations