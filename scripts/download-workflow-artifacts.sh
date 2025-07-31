#!/bin/bash
# GitHub Actionsのアーティファクトを自動ダウンロードして整理するスクリプト
# 使用方法: ./download-workflow-artifacts.sh [run-id]

set -e

echo "🎬 Video Content Creation Production v8 - Artifact Downloader"
echo "=================================================="

# ヘルプメッセージ
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo ""
    echo "使用方法:"
    echo "  $0              - 最新の成功したワークフロー実行をダウンロード"
    echo "  $0 <run-id>     - 指定されたRun IDのアーティファクトをダウンロード"
    echo ""
    echo "例:"
    echo "  $0"
    echo "  $0 16642048368"
    echo ""
    exit 0
fi

# 必要なコマンドの確認
command -v gh >/dev/null 2>&1 || { echo "❌ GitHub CLI (gh) がインストールされていません"; exit 1; }

# jqの代わりにghの--jqオプションを使用するので、jqは必須ではない

# GitHubリポジトリを設定
if [ -z "$GITHUB_REPOSITORY" ]; then
    GITHUB_REPOSITORY="rossy8417/kamuicode_meta"
fi

# Run IDが引数で指定されているかチェック
if [ -n "$1" ]; then
    RUN_ID="$1"
    echo "📌 指定されたRun IDを使用: $RUN_ID"
    
    # 指定されたRunの情報を取得
    RUN_TITLE=$(gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID --jq '.display_title' 2>/dev/null || echo "")
    
    if [ -z "$RUN_TITLE" ]; then
        echo "❌ Run ID $RUN_ID が見つかりません"
        exit 1
    fi
    
    RUN_DATE=$(gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID --jq '.created_at')
    STATUS=$(gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID --jq '.status')
    CONCLUSION=$(gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID --jq '.conclusion')
    
    if [ "$STATUS" != "completed" ] || [ "$CONCLUSION" != "success" ]; then
        echo "⚠️  警告: このRunは成功していません (status: $STATUS, conclusion: $CONCLUSION)"
        echo -n "続行しますか？ (y/N): "
        read -r CONFIRM
        if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
            exit 0
        fi
    fi
else
    echo "🔍 最新のワークフロー実行を確認中..."
    
    # 最新の成功したワークフロー実行を取得
    LATEST_RUN=$(gh run list --workflow="Video Content Creation Production v8" --repo=$GITHUB_REPOSITORY --status=success --limit=1 --json databaseId,displayTitle,createdAt --jq '.[0]')
    
    if [ -z "$LATEST_RUN" ]; then
        echo "❌ 成功したワークフロー実行が見つかりません"
        exit 1
    fi
    
    RUN_ID=$(echo "$LATEST_RUN" | grep -o '"databaseId":[0-9]*' | cut -d: -f2)
    RUN_TITLE=$(echo "$LATEST_RUN" | grep -o '"displayTitle":"[^"]*"' | cut -d'"' -f4)
    RUN_DATE=$(echo "$LATEST_RUN" | grep -o '"createdAt":"[^"]*"' | cut -d'"' -f4)
fi

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
# Run番号を取得（IDの最後の数字部分）
RUN_NUMBER=$(gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID --jq '.run_number')
# タイトルから動画コンセプトを抽出（"🎥 V8 Production: "を除去）
VIDEO_CONCEPT=$(echo "$RUN_TITLE" | sed 's/^🎥 V8 Production: //')
PROJECT_NAME=$(echo "$VIDEO_CONCEPT" | sed 's/[^a-zA-Z0-9-]/-/g' | sed 's/--*/-/g' | cut -c1-50)
PROJECT_DIR="projects/video-v8-run-${RUN_NUMBER}-${PROJECT_NAME}"
mkdir -p "$PROJECT_DIR"

# 全アーティファクトをダウンロード
echo "📦 利用可能なアーティファクト:"
gh api repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID/artifacts --jq '.artifacts[] | "\(.name)"' 2>/dev/null || echo "  (アーティファクト一覧の取得に失敗)"

# gh CLIを使用してダウンロード（権限承認不要）
echo "⬇️ 全アーティファクトを一括ダウンロード中..."
gh run download $RUN_ID --repo $GITHUB_REPOSITORY -D "$PROJECT_DIR"

# ダウンロード完了をマーク
echo "$RUN_ID" >> "$DOWNLOAD_MARKER"

echo "🔧 ディレクトリ構造を整理中..."

# ディレクトリ構造を整理
cd "$PROJECT_DIR" || exit 1

# 必要なディレクトリを作成
mkdir -p audio/{bgm,narration} images/{intro,main,outro} videos/{intro,main,outro} planning metadata

# ファイルを適切な場所に移動
if [ -d "bgm-${RUN_NUMBER}" ]; then
    mv "bgm-${RUN_NUMBER}"/* audio/bgm/ 2>/dev/null || true
fi

if [ -d "narration-${RUN_NUMBER}" ]; then
    # 深い階層にある全てのナレーションファイルを検出
    NARRATION_FILES=($(find "narration-${RUN_NUMBER}" -name "narration.mp3" -type f))
    
    if [ ${#NARRATION_FILES[@]} -gt 0 ]; then
        echo "🔍 Found ${#NARRATION_FILES[@]} narration file(s)"
        
        # 最適なナレーションファイルを選択
        BEST_NARRATION=""
        BEST_SIZE=0
        
        for NARRATION_FILE in "${NARRATION_FILES[@]}"; do
            NARRATION_SIZE=$(stat -c%s "$NARRATION_FILE" 2>/dev/null || echo "0")
            echo "  - $NARRATION_FILE: ${NARRATION_SIZE} bytes"
            
            # 400KB-500KB範囲（実際の音声）を最優先
            if [ "$NARRATION_SIZE" -gt 400000 ] && [ "$NARRATION_SIZE" -lt 500000 ]; then
                BEST_NARRATION="$NARRATION_FILE"
                BEST_SIZE="$NARRATION_SIZE"
                echo "    ✅ 実際の音声ファイルを検出"
                break
            # モノラル/ステレオ判定でより適切なファイルを選択
            elif [ "$NARRATION_SIZE" -gt "$BEST_SIZE" ] && [ "$NARRATION_SIZE" -lt 600000 ]; then
                BEST_NARRATION="$NARRATION_FILE"
                BEST_SIZE="$NARRATION_SIZE"
            fi
        done
        
        if [ -n "$BEST_NARRATION" ]; then
            cp "$BEST_NARRATION" audio/narration/narration.mp3
            echo "✅ 最適なナレーションファイルを選択: $BEST_NARRATION ($BEST_SIZE bytes)"
            
            # ファイルタイプ確認
            FILE_TYPE=$(file "$BEST_NARRATION" | grep -o "Monaural\|Stereo" || echo "Unknown")
            echo "   🎵 Audio format: $FILE_TYPE"
            
            # 関連ファイルを同じディレクトリから取得
            NARRATION_DIR=$(dirname "$BEST_NARRATION")
            if [ -f "$NARRATION_DIR/narration-url.txt" ]; then
                cp "$NARRATION_DIR/narration-url.txt" audio/narration/
                echo "   📎 Copied narration-url.txt"
            fi
            if [ -f "$NARRATION_DIR/narration-duration.txt" ]; then
                cp "$NARRATION_DIR/narration-duration.txt" audio/narration/
                echo "   ⏱️ Copied narration-duration.txt"
            fi
        else
            echo "⚠️ Using first available narration file"
            cp "${NARRATION_FILES[0]}" audio/narration/narration.mp3
        fi
        
        # 他の関連ファイルも探して移動
        find "narration-${RUN_NUMBER}" -name "narration-url.txt" -type f -exec cp {} audio/narration/ \; 2>/dev/null || true
        find "narration-${RUN_NUMBER}" -name "narration-duration.txt" -type f -exec cp {} audio/narration/ \; 2>/dev/null || true
    else
        # 従来の移動方法
        echo "⚠️ Using legacy narration file movement"
        mv "narration-${RUN_NUMBER}"/* audio/narration/ 2>/dev/null || true
    fi
fi

if [ -d "planning-${RUN_NUMBER}" ]; then
    mv "planning-${RUN_NUMBER}"/* planning/ 2>/dev/null || true
fi

if [ -d "environment-${RUN_NUMBER}" ]; then
    mv "environment-${RUN_NUMBER}"/* metadata/ 2>/dev/null || true
fi

# 画像ファイルの移動
for scene in intro main outro; do
    if [ -d "images-${scene}-${RUN_NUMBER}" ]; then
        mv "images-${scene}-${RUN_NUMBER}"/* "images/${scene}/" 2>/dev/null || true
    fi
done

# 動画ファイルの移動
for scene in intro main outro; do
    if [ -d "videos-${scene}-${RUN_NUMBER}" ]; then
        mv "videos-${scene}-${RUN_NUMBER}"/* "videos/${scene}/" 2>/dev/null || true
    fi
done

# 最終パッケージの移動
if [ -d "final-video-package-${RUN_NUMBER}" ]; then
    mv "final-video-package-${RUN_NUMBER}"/* . 2>/dev/null || true
fi

# 空のディレクトリを削除
rmdir *-${RUN_NUMBER} 2>/dev/null || true

# ワークフロー情報ファイルを作成
cat > workflow-info.json << EOF
{
  "workflow": "video-content-creation-production-v8",
  "run_number": ${RUN_NUMBER},
  "run_id": "${RUN_ID}",
  "concept": "${VIDEO_CONCEPT}",
  "created_at": "${RUN_DATE}",
  "github_repository": "${GITHUB_REPOSITORY}",
  "structure": {
    "planning": "企画ドキュメント",
    "images": {
      "intro": "イントロ画像",
      "main": "メイン画像",
      "outro": "アウトロ画像"
    },
    "videos": {
      "intro": "イントロ動画",
      "main": "メイン動画",
      "outro": "アウトロ動画"
    },
    "audio": {
      "bgm": "背景音楽",
      "narration": "ナレーション音声"
    },
    "metadata": "環境情報・実行ログ",
    "final_outputs": {
      "final_video.mp4": "最終動画（BGM・ナレーション付き）",
      "combined.mp4": "結合動画（音声なし）",
      "summary.md": "実行サマリー"
    }
  }
}
EOF

cd - > /dev/null

echo "✅ ダウンロード完了: $PROJECT_DIR"
echo "📁 ディレクトリ構造:"
tree "$PROJECT_DIR" -L 2 2>/dev/null || find "$PROJECT_DIR" -maxdepth 2 -type d | sort

# 最終動画の情報を表示
if [ -f "$PROJECT_DIR/final_video.mp4" ]; then
    FILE_SIZE=$(ls -lh "$PROJECT_DIR/final_video.mp4" | awk '{print $5}')
    echo ""
    echo "🎥 最終動画: $PROJECT_DIR/final_video.mp4 (${FILE_SIZE})"
    echo ""
    echo "📌 次のステップ:"
    echo "   1. 動画を確認: open $PROJECT_DIR/final_video.mp4"
    echo "   2. サマリーを確認: cat $PROJECT_DIR/summary.md"
    echo "   3. プロジェクト情報: cat $PROJECT_DIR/workflow-info.json"
fi