#!/bin/bash
# GitHub Actionsのアーティファクトを自動ダウンロードするスクリプト

echo "🔍 最新のワークフロー実行を確認中..."

# 最新の成功したワークフロー実行を取得
LATEST_RUN=$(gh run list --workflow=video-content-creation-production-v8.yml --status=success --limit=1 --json databaseId,displayTitle,createdAt --jq '.[0]')

if [ -z "$LATEST_RUN" ]; then
    echo "❌ 成功したワークフロー実行が見つかりません"
    exit 1
fi

RUN_ID=$(echo "$LATEST_RUN" | jq -r '.databaseId')
RUN_TITLE=$(echo "$LATEST_RUN" | jq -r '.displayTitle')
RUN_DATE=$(echo "$LATEST_RUN" | jq -r '.createdAt')

echo "✅ 最新の実行を発見:"
echo "   ID: $RUN_ID"
echo "   タイトル: $RUN_TITLE"
echo "   実行日時: $RUN_DATE"

# ダウンロード済みかチェック
DOWNLOAD_MARKER="projects/.downloaded-runs"
mkdir -p projects
touch "$DOWNLOAD_MARKER"

if grep -q "^$RUN_ID$" "$DOWNLOAD_MARKER" 2>/dev/null; then
    echo "ℹ️ この実行は既にダウンロード済みです"
    exit 0
fi

echo "📥 アーティファクトをダウンロード中..."

# プロジェクトディレクトリ名を生成
PROJECT_NAME=$(echo "$RUN_TITLE" | sed 's/[^a-zA-Z0-9-]/-/g' | sed 's/--*/-/g' | cut -c1-50)
PROJECT_DIR="projects/run-${RUN_ID}-${PROJECT_NAME}"
mkdir -p "$PROJECT_DIR"

# 全アーティファクトをダウンロード
echo "📦 利用可能なアーティファクト:"
gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID/artifacts --jq '.artifacts[] | "\(.name) (\(.size_in_bytes/1048576 | round)MB)"'

# アーティファクトを個別にダウンロード
gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID/artifacts --jq '.artifacts[] | .id' | while read -r ARTIFACT_ID; do
    ARTIFACT_NAME=$(gh api repos/$GITHUB_REPOSITORY/actions/artifacts/$ARTIFACT_ID --jq '.name')
    echo "⬇️ ダウンロード中: $ARTIFACT_NAME"
    
    # アーティファクトをダウンロード
    gh api repos/$GITHUB_REPOSITORY/actions/artifacts/$ARTIFACT_ID/zip > "$PROJECT_DIR/${ARTIFACT_NAME}.zip"
    
    # 解凍
    mkdir -p "$PROJECT_DIR/$ARTIFACT_NAME"
    unzip -q "$PROJECT_DIR/${ARTIFACT_NAME}.zip" -d "$PROJECT_DIR/$ARTIFACT_NAME"
    rm "$PROJECT_DIR/${ARTIFACT_NAME}.zip"
done

# ダウンロード完了をマーク
echo "$RUN_ID" >> "$DOWNLOAD_MARKER"

echo "✅ ダウンロード完了: $PROJECT_DIR"
echo "📁 ディレクトリ構造:"
tree "$PROJECT_DIR" -L 2 2>/dev/null || find "$PROJECT_DIR" -maxdepth 2 -type d | sort