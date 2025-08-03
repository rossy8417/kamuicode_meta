# Script Catalog - Kamui Rossy Project

このカタログは、プロジェクト内のすべてのスクリプトを用途別に分類し、使用場面を明確にしたものです。

## 📋 カテゴリー別一覧

### 🔧 開発・保守ツール

#### 1. **restore-claude-permissions.sh**
- **用途**: Claude Code設定ファイルの権限復元
- **使用場面**: Claude Codeが設定を上書きした際の修復
- **重要度**: ⭐⭐⭐⭐⭐ (必須)
- **コマンド**: `./scripts/restore-claude-permissions.sh`

#### 2. **balus-complete.sh**
- **用途**: GitHub Actions履歴とキャッシュの完全削除
- **使用場面**: GitHub Actionsのリセットが必要な時
- **重要度**: ⭐⭐⭐⭐
- **コマンド**: `./scripts/balus-complete.sh`

### 📥 ダウンロード・収集ツール

#### 3. **download-workflow-artifacts.sh** ⭐統合版
- **用途**: ワークフロー実行結果の効率的なダウンロード（重複防止機能付き）
- **使用場面**: ワークフロー実行結果の取得、アーティファクト管理
- **重要度**: ⭐⭐⭐⭐⭐ (必須)
- **コマンド例**:
  ```bash
  ./scripts/download-workflow-artifacts.sh meta-workflow-executor-v12
  ./scripts/download-workflow-artifacts.sh --list 16709668564
  ./scripts/download-workflow-artifacts.sh -o projects/issue-66 16709668564
  ./scripts/download-workflow-artifacts.sh --clean  # 古いダウンロードを削除
  ```
- **備考**: 旧download-workflow-results.shとsmart-artifact-download.shの機能を統合

### 🔨 ワークフロー生成・変換ツール

#### 4. **inline-minimal-unit.sh**
- **用途**: ミニマルユニットのインライン展開
- **使用場面**: uses:参照をインライン実装に変換
- **重要度**: ⭐⭐⭐⭐⭐ (必須)
- **コマンド**: `./scripts/inline-minimal-unit.sh workflow.yml`

#### 5. **workflow-inputs-generator.py**
- **用途**: ワークフローの入力パラメータ生成
- **使用場面**: メタワークフローv12でworkflow_dispatch入力を生成
- **重要度**: ⭐⭐⭐⭐
- **コマンド**: `python scripts/workflow-inputs-generator.py`

#### 6. **domain-template-loader.py**
- **用途**: ドメインテンプレートの読み込みと処理
- **使用場面**: メタワークフローv12でドメイン検出と分析
- **重要度**: ⭐⭐⭐⭐⭐ (必須)
- **コマンド**: `python scripts/domain-template-loader.py --action detect`

### 🔍 分析・検証ツール

#### 7. **orchestrator_analyzer.py**
- **用途**: オーケストレーターワークフロー分析
- **使用場面**: kamuicode-workflowパターンの分析
- **重要度**: ⭐⭐⭐
- **コマンド**: `python scripts/orchestrator_analyzer.py`

#### 8. **fix-yaml-syntax.py**
- **用途**: YAML構文エラーの自動修正（HEREDOCエラー対応）
- **使用場面**: ワークフロー生成後の構文エラー修正
- **重要度**: ⭐⭐⭐ (保険として保持)
- **コマンド**: `python scripts/fix-yaml-syntax.py workflow.yml`

### 🔐 権限・設定管理

#### 9. **generate-mcp-permissions.py**
- **用途**: MCP権限設定ファイル生成
- **使用場面**: 新しいMCPサービス追加時
- **重要度**: ⭐⭐⭐
- **コマンド**: `python scripts/generate-mcp-permissions.py`

### 📤 アップロード・連携ツール

#### 10. **fal_upload_helper.py**
- **用途**: FALサービスへのファイルアップロード補助（統合版）
- **使用場面**: 画像・動画をFAL APIで処理する際（CI/CDとローカル両対応）
- **重要度**: ⭐⭐⭐
- **コマンド**: `python scripts/fal_upload_helper.py <file>`
- **備考**: 旧local_fal_upload.pyの機能を統合

## 🗑️ 削除済みスクリプト（2025-08-04）

1. **download-workflow-results.sh** → download-workflow-artifacts.shに統合
2. **smart-artifact-download.sh** → download-workflow-artifacts.shに統合
3. **local_fal_upload.py** → fal_upload_helper.pyに統合

## 📁 deprecatedディレクトリ

削除されたスクリプトは`scripts/deprecated/`に保管されています。

## 📝 使用頻度ランキング

1. 🥇 **download-workflow-artifacts.sh** - 毎回のワークフロー実行後
2. 🥈 **restore-claude-permissions.sh** - Claude Code使用時
3. 🥉 **domain-template-loader.py** - メタワークフロー実行時（6箇所参照）
4. **inline-minimal-unit.sh** - ワークフロー修正時
5. **generate-mcp-permissions.py** - MCP設定更新時

## 🔄 メンテナンス状況

- ✅ **活発に使用**: download-workflow-artifacts.sh, restore-claude-permissions.sh, domain-template-loader.py
- 🔧 **時々使用**: inline-minimal-unit.sh, workflow-inputs-generator.py, orchestrator_analyzer.py
- ⚠️ **まれに使用**: generate-mcp-permissions.py, fal_upload_helper.py, fix-yaml-syntax.py, balus-complete.sh

## 📌 Quick Reference

```bash
# 最もよく使うコマンド
./scripts/download-workflow-artifacts.sh meta-workflow-executor-v12  # アーティファクト取得
./scripts/restore-claude-permissions.sh                              # Claude設定復元
python scripts/domain-template-loader.py --action detect             # ドメイン検出

# ワークフロー生成・修正
./scripts/inline-minimal-unit.sh workflow.yml                        # uses:をインライン化
python scripts/workflow-inputs-generator.py                          # 入力パラメータ生成

# メンテナンス
./scripts/balus-complete.sh                                          # GitHub Actions完全リセット
python scripts/fix-yaml-syntax.py workflow.yml                      # YAML修正（必要時のみ）
```

## 📋 スクリプト総数
- **現在**: 10個（13個から3個削除）
- **削除済み**: 3個（deprecatedに移動）

---
最終更新: 2025-08-04