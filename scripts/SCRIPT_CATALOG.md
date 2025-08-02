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

#### 3. **download-workflow-results.sh**
- **用途**: ワークフロー実行結果の一括ダウンロード
- **使用場面**: 生成物の取得、ログ収集
- **重要度**: ⭐⭐⭐⭐⭐ (必須)
- **コマンド例**:
  ```bash
  ./scripts/download-workflow-results.sh -i  # 対話モード
  ./scripts/download-workflow-results.sh -w "Meta Workflow Executor v9"
  ```

### 🔨 ワークフロー生成・変換ツール

#### 4. **inline-minimal-unit.sh** ⭐NEW
- **用途**: ミニマルユニットのインライン展開
- **使用場面**: uses:参照をインライン実装に変換
- **重要度**: ⭐⭐⭐⭐⭐ (必須)
- **コマンド**: `./scripts/inline-minimal-unit.sh workflow.yml`

#### 5. **generate_dynamic_workflow.py**
- **用途**: 動的ワークフロー生成（旧バージョン）
- **使用場面**: 現在は使用されていない
- **重要度**: ⭐ (削除候補)
- **状態**: 非推奨

#### 6. **generate_optimized_workflow.py**
- **用途**: 最適化ワークフロー生成（旧バージョン）
- **使用場面**: 現在は使用されていない
- **重要度**: ⭐ (削除候補)
- **状態**: 非推奨

### 🔍 分析・検証ツール

#### 7. **orchestrator_analyzer.py**
- **用途**: オーケストレーターワークフロー分析
- **使用場面**: kamuicode-workflowパターンの分析
- **重要度**: ⭐⭐⭐
- **コマンド**: `python scripts/orchestrator_analyzer.py`

#### 8. **fix-yaml-syntax.py**
- **用途**: YAML構文エラーの自動修正
- **使用場面**: ワークフロー生成後の検証・修正
- **重要度**: ⭐⭐⭐⭐
- **コマンド**: `python scripts/fix-yaml-syntax.py workflow.yml`

### 🔐 権限・設定管理

#### 9. **generate-mcp-permissions.py**
- **用途**: MCP権限設定ファイル生成
- **使用場面**: 新しいMCPサービス追加時
- **重要度**: ⭐⭐⭐
- **コマンド**: `python scripts/generate-mcp-permissions.py`

### 📤 アップロード・連携ツール

#### 10. **fal_upload_helper.py**
- **用途**: FALサービスへのファイルアップロード補助
- **使用場面**: 画像・動画をFAL APIで処理する際
- **重要度**: ⭐⭐⭐
- **コマンド**: `python scripts/fal_upload_helper.py <file>`

#### 11. **local_fal_upload.py**
- **用途**: ローカルからFALへの直接アップロード
- **使用場面**: CI/CD外でのFAL利用
- **重要度**: ⭐⭐
- **コマンド**: `python scripts/local_fal_upload.py`

### 📁 プロジェクト固有スクリプト

#### 12. **extract-workflow.py** (projects/meta-workflow-v10-analysis/)
- **用途**: メタワークフローv10の分析用
- **使用場面**: v10ワークフローの構造抽出
- **重要度**: ⭐⭐ (一時的)
- **場所**: プロジェクトディレクトリ内

## 🗑️ 削除推奨スクリプト

1. **generate_dynamic_workflow.py** - メタワークフローv9で置き換え済み
2. **generate_optimized_workflow.py** - 同上

## 📝 使用頻度ランキング

1. 🥇 **download-workflow-results.sh** - 毎回のワークフロー実行後
2. 🥈 **restore-claude-permissions.sh** - Claude Code使用時
3. 🥉 **inline-minimal-unit.sh** - ワークフロー修正時
4. **fix-yaml-syntax.py** - ワークフロー生成時
5. **balus-complete.sh** - 定期メンテナンス

## 🔄 メンテナンス状況

- ✅ **活発に使用**: download-workflow-results.sh, restore-claude-permissions.sh, inline-minimal-unit.sh
- 🔧 **時々使用**: fix-yaml-syntax.py, orchestrator_analyzer.py, balus-complete.sh
- ⚠️ **まれに使用**: generate-mcp-permissions.py, fal_upload_helper.py
- ❌ **非推奨**: generate_dynamic_workflow.py, generate_optimized_workflow.py

## 📌 Quick Reference

```bash
# 最もよく使うコマンド
./scripts/download-workflow-results.sh -i    # ワークフロー結果取得
./scripts/restore-claude-permissions.sh       # Claude設定復元
./scripts/inline-minimal-unit.sh workflow.yml # uses:をインライン化

# メンテナンス
./scripts/balus-complete.sh                   # GitHub Actions完全リセット
python scripts/fix-yaml-syntax.py workflow.yml # YAML修正
```

---
最終更新: 2025-08-02