#!/bin/bash

# 🚀 Universal Workflow Results Downloader with Execution Logging
# GitHub Actionsワークフローの成果物と実行ログを自動ダウンロード・整理
# 使用方法: ./download-workflow-results.sh [options] [run-id]

set -e

VERSION="2.0"
SCRIPT_NAME="Universal Workflow Results Downloader"

echo "🚀 $SCRIPT_NAME v$VERSION"
echo "════════════════════════════════════════════════════════════════"

# ヘルプメッセージ
show_help() {
    cat << EOF

使用方法:
  $0 [options] [run-id]

オプション:
  -w, --workflow NAME    特定のワークフロー名を指定
  -l, --logs-only        実行ログのみダウンロード（アーティファクトをスキップ）
  -a, --artifacts-only   アーティファクトのみダウンロード（ログをスキップ）
  -i, --interactive      インタラクティブモード
  -f, --force            既にダウンロード済みでも強制実行
  -z, --zip              結果をZIPアーカイブで圧縮
  -h, --help             このヘルプを表示

引数:
  run-id                 GitHub Actions Run ID（省略時は最新の成功実行を使用）

例:
  $0                                              # 最新の成功実行をダウンロード
  $0 -w "Meta Workflow Executor v9"              # 特定ワークフローの最新実行
  $0 -i                                           # インタラクティブモード
  $0 16666636509                                  # 特定のRun IDを指定
  $0 -l 16666636509                              # ログのみダウンロード
  $0 -z -w "Video Content Creation Production v8" # ZIP圧縮してダウンロード

サポートするワークフロー:
  • Meta Workflow Executor v9 (メタワークフロー実行ログ + 生成ワークフロー)
  • Video Content Creation Production v8 (動画制作成果物)
  • Simple Test Workflow (テスト実行結果)
  • その他すべてのGitHub Actionsワークフロー

EOF
}

# デフォルト設定
WORKFLOW_NAME=""
LOGS_ONLY=false
ARTIFACTS_ONLY=false
INTERACTIVE=false
FORCE_DOWNLOAD=false
CREATE_ZIP=false
RUN_ID=""

# パラメータ解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -w|--workflow)
            WORKFLOW_NAME="$2"
            shift 2
            ;;
        -l|--logs-only)
            LOGS_ONLY=true
            shift
            ;;
        -a|--artifacts-only)
            ARTIFACTS_ONLY=true
            shift
            ;;
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        -f|--force)
            FORCE_DOWNLOAD=true
            shift
            ;;
        -z|--zip)
            CREATE_ZIP=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "❌ 不明なオプション: $1"
            show_help
            exit 1
            ;;
        *)
            if [[ -z "$RUN_ID" ]]; then
                RUN_ID="$1"
            else
                echo "❌ 複数のRun IDが指定されました"
                exit 1
            fi
            shift
            ;;
    esac
done

# 必要なコマンドの確認
command -v gh >/dev/null 2>&1 || { echo "❌ GitHub CLI (gh) がインストールされていません"; exit 1; }

# GitHubリポジトリを設定
if [ -z "$GITHUB_REPOSITORY" ]; then
    GITHUB_REPOSITORY=$(gh repo view --json owner,name --jq '.owner.login + "/" + .name' 2>/dev/null || echo "")
    if [ -z "$GITHUB_REPOSITORY" ]; then
        echo "❌ GitHubリポジトリを特定できません。リポジトリ内で実行してください。"
        exit 1
    fi
fi

echo "📋 Repository: $GITHUB_REPOSITORY"

# インタラクティブモード
if [ "$INTERACTIVE" = true ]; then
    echo ""
    echo "🔍 利用可能なワークフロー:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    gh run list --limit=20 --json status,conclusion,workflowName,databaseId,createdAt,displayTitle | \
    jq -r 'group_by(.workflowName) | .[] | 
    "• " + .[0].workflowName + " (" + (map(select(.status == "completed" and .conclusion == "success")) | length | tostring) + " successful runs)"' | sort | uniq
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    read -p "ワークフロー名を入力 (空白で全ワークフロー): " WORKFLOW_NAME
    
    if [[ -n "$WORKFLOW_NAME" ]]; then
        echo ""
        echo "🔍 \"$WORKFLOW_NAME\" の最近の実行:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        gh run list --workflow="$WORKFLOW_NAME" --limit=10 --json status,conclusion,databaseId,createdAt,displayTitle | \
        jq -r '.[] | 
        "• Run ID: " + (.databaseId | tostring) + 
        " | " + .status + 
        " | " + (.conclusion // "in_progress") + 
        " | " + .createdAt + 
        " | " + .displayTitle'
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
    fi
    
    read -p "Run IDを入力 (空白で最新の成功実行): " INPUT_RUN_ID
    if [[ -n "$INPUT_RUN_ID" ]]; then
        RUN_ID="$INPUT_RUN_ID"
    fi
    
    echo ""
    echo "ダウンロードオプション:"
    echo "1) 全て (アーティファクト + 実行ログ)"
    echo "2) アーティファクトのみ"
    echo "3) 実行ログのみ"
    read -p "選択 (1-3, デフォルト: 1): " DOWNLOAD_OPTION
    
    case $DOWNLOAD_OPTION in
        2) ARTIFACTS_ONLY=true ;;
        3) LOGS_ONLY=true ;;
        *) ;; # デフォルト: 全て
    esac
    
    read -p "ZIPアーカイブを作成しますか？ (Y/n): " CREATE_ZIP_INPUT
    if [[ "$CREATE_ZIP_INPUT" =~ ^[Yy]$ ]] || [[ -z "$CREATE_ZIP_INPUT" ]]; then
        CREATE_ZIP=true
    fi
fi

# Run IDの特定
if [ -n "$RUN_ID" ]; then
    echo "📌 指定されたRun IDを使用: $RUN_ID"
    
    # 指定されたRunの情報を取得
    RUN_INFO=$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID" 2>/dev/null) || {
        echo "❌ Run ID $RUN_ID が見つかりません"
        exit 1
    }
    
    RUN_TITLE=$(echo "$RUN_INFO" | jq -r '.display_title')
    RUN_DATE=$(echo "$RUN_INFO" | jq -r '.created_at')
    STATUS=$(echo "$RUN_INFO" | jq -r '.status')
    CONCLUSION=$(echo "$RUN_INFO" | jq -r '.conclusion // "in_progress"')
    WORKFLOW_NAME_FROM_RUN=$(echo "$RUN_INFO" | jq -r '.name')
    BRANCH_NAME=$(echo "$RUN_INFO" | jq -r '.head_branch')
    
    if [ -z "$WORKFLOW_NAME" ]; then
        WORKFLOW_NAME="$WORKFLOW_NAME_FROM_RUN"
    fi
    
    if [ "$STATUS" != "completed" ] || [ "$CONCLUSION" != "success" ]; then
        echo "⚠️  警告: このRunは成功していません (status: $STATUS, conclusion: $CONCLUSION)"
        if [ "$INTERACTIVE" = false ]; then
            echo -n "続行しますか？ (y/N): "
            read -r CONFIRM
            if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
                exit 0
            fi
        fi
    fi
else
    echo "🔍 最新のワークフロー実行を確認中..."
    
    # 最新の成功したワークフロー実行を取得
    if [ -n "$WORKFLOW_NAME" ]; then
        LATEST_RUN=$(gh run list --workflow="$WORKFLOW_NAME" --repo="$GITHUB_REPOSITORY" --status=success --limit=1 --json databaseId,displayTitle,createdAt,name,headBranch --jq '.[0]') || {
        echo "❌ 成功したワークフロー実行が見つかりません: $WORKFLOW_NAME"
        exit 1
    }
    else
        LATEST_RUN=$(gh run list --repo="$GITHUB_REPOSITORY" --status=success --limit=1 --json databaseId,displayTitle,createdAt,name,headBranch --jq '.[0]') || {
            echo "❌ 成功したワークフロー実行が見つかりません"
            exit 1
        }
    fi
    
    RUN_ID=$(echo "$LATEST_RUN" | jq -r '.databaseId')
    RUN_TITLE=$(echo "$LATEST_RUN" | jq -r '.displayTitle')
    RUN_DATE=$(echo "$LATEST_RUN" | jq -r '.createdAt')
    WORKFLOW_NAME=$(echo "$LATEST_RUN" | jq -r '.name')
    BRANCH_NAME=$(echo "$LATEST_RUN" | jq -r '.headBranch')
    STATUS="completed"
    CONCLUSION="success"
fi

echo "✅ ワークフロー実行を特定:"
echo "   • Workflow: $WORKFLOW_NAME"
echo "   • Run ID: $RUN_ID"
echo "   • Title: $RUN_TITLE"
echo "   • Date: $RUN_DATE"
echo "   • Status: $STATUS ($CONCLUSION)"
echo "   • Branch: $BRANCH_NAME"

# ダウンロード済みかチェック
DOWNLOAD_MARKER="projects/.downloaded-runs"
mkdir -p projects
touch "$DOWNLOAD_MARKER"

if [ "$FORCE_DOWNLOAD" = false ] && grep -q "^$RUN_ID$" "$DOWNLOAD_MARKER" 2>/dev/null; then
    echo "ℹ️ この実行は既にダウンロード済みです (--force で強制実行可能)"
    exit 0
fi

# プロジェクトディレクトリ名を生成
RUN_NUMBER=$(echo "$RUN_INFO" | jq -r '.run_number' 2>/dev/null || echo "$(date +%m%d)")
CLEAN_WORKFLOW_NAME=$(echo "$WORKFLOW_NAME" | sed 's/[^a-zA-Z0-9-]/-/g' | sed 's/--*/-/g' | tr '[:upper:]' '[:lower:]')
CLEAN_TITLE=$(echo "$RUN_TITLE" | sed 's/[^a-zA-Z0-9-]/-/g' | sed 's/--*/-/g' | cut -c1-50)
PROJECT_DIR="projects/${CLEAN_WORKFLOW_NAME}-run-${RUN_NUMBER}-${CLEAN_TITLE}"
mkdir -p "$PROJECT_DIR"

echo ""
echo "📁 プロジェクトディレクトリ: $PROJECT_DIR"

# アーティファクトダウンロード
if [ "$LOGS_ONLY" = false ]; then
    echo ""
    echo "📦 アーティファクト情報:"
    ARTIFACTS=$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID/artifacts" --jq '.artifacts[] | "\(.name) (\(.size_in_bytes) bytes)"' 2>/dev/null || echo "")
    
    if [ -n "$ARTIFACTS" ]; then
        echo "$ARTIFACTS" | while read -r line; do
            echo "   • $line"
        done
        
        echo ""
        echo "⬇️ アーティファクトをダウンロード中..."
        gh run download "$RUN_ID" --repo "$GITHUB_REPOSITORY" -D "$PROJECT_DIR" || {
            echo "⚠️ アーティファクトのダウンロードに失敗しました（アーティファクトが存在しない可能性があります）"
        }
    else
        echo "   (アーティファクトは存在しません)"
    fi
fi

# 実行ログ収集
if [ "$ARTIFACTS_ONLY" = false ]; then
    echo ""
    echo "📋 実行ログを収集中..."
    
    LOG_DIR="$PROJECT_DIR/execution-logs"
    mkdir -p "$LOG_DIR"
    
    EXECUTION_LOG="$LOG_DIR/workflow-execution-log.txt"
    
    # 包括的な実行ログを生成
    cat > "$EXECUTION_LOG" << EOF
═══════════════════════════════════════════════════════════════
                    WORKFLOW EXECUTION LOG
═══════════════════════════════════════════════════════════════

📅 EXECUTION TIMESTAMP: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
🔗 GITHUB RUN: https://github.com/$GITHUB_REPOSITORY/actions/runs/$RUN_ID

🚀 EXECUTION DETAILS
═══════════════════════════════════════════════════════════════
• Workflow Name: $WORKFLOW_NAME
• GitHub Run ID: $RUN_ID
• Run Number: $RUN_NUMBER
• Execution Date: $RUN_DATE
• Repository: $GITHUB_REPOSITORY
• Branch: $BRANCH_NAME
• Status: $STATUS
• Conclusion: $CONCLUSION
• Display Title: $RUN_TITLE

🖥️ DOWNLOAD ENVIRONMENT
═══════════════════════════════════════════════════════════════
• Downloaded by: $(whoami)
• Download Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
• Download Host: $(hostname)
• Script Version: $VERSION
• Download Options: logs=$([ "$LOGS_ONLY" = true ] && echo "only" || echo "included"), artifacts=$([ "$ARTIFACTS_ONLY" = true ] && echo "only" || echo "included")

EOF

    # GitHub Actions APIから詳細情報を取得
    echo "🔍 GitHub Actions API情報を収集中..."
    
    # ワークフロー実行詳細情報
    echo "" >> "$EXECUTION_LOG"
    echo "🚀 WORKFLOW RUN INFORMATION" >> "$EXECUTION_LOG"
    echo "═══════════════════════════════════════════════════════════════" >> "$EXECUTION_LOG"
    gh api "repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID" --jq '
    "• Run ID: " + (.id | tostring) + "\n" +
    "• Run Number: " + (.run_number | tostring) + "\n" +
    "• Status: " + .status + "\n" +
    "• Conclusion: " + (.conclusion // "in_progress") + "\n" +
    "• Created: " + .created_at + "\n" +
    "• Updated: " + .updated_at + "\n" +
    "• Started: " + (.run_started_at // "N/A") + "\n" +
    "• HTML URL: " + .html_url + "\n" +
    "• Head Branch: " + .head_branch + "\n" +
    "• Head SHA: " + .head_sha + "\n" +
    "• Actor: " + .actor.login + "\n" +
    "• Triggering Actor: " + .triggering_actor.login + "\n" +
    "• Event: " + .event + "\n" +
    "• Workflow ID: " + (.workflow_id | tostring) + "\n" +
    "• Workflow URL: " + .workflow_url
    ' >> "$EXECUTION_LOG" 2>/dev/null || echo "• API情報の取得に失敗" >> "$EXECUTION_LOG"

    # ジョブ実行詳細情報
    echo "" >> "$EXECUTION_LOG"
    echo "📊 JOB EXECUTION DETAILS" >> "$EXECUTION_LOG"
    echo "═══════════════════════════════════════════════════════════════" >> "$EXECUTION_LOG"
    
    JOBS_INFO=$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID/jobs" 2>/dev/null) || echo ""
    
    if [ -n "$JOBS_INFO" ]; then
        echo "$JOBS_INFO" | jq -r '.jobs[] | 
        "Job: " + .name + "\n" +
        "  • Status: " + .status + "\n" +  
        "  • Conclusion: " + (.conclusion // "in_progress") + "\n" +
        "  • Started: " + (.started_at // "not_started") + "\n" +
        "  • Completed: " + (.completed_at // "in_progress") + "\n" +
        "  • Duration: " + (if .started_at and .completed_at then 
            (((.completed_at | fromdateiso8601) - (.started_at | fromdateiso8601)) | tostring) + " seconds"
        else "in_progress" end) + "\n" +
        "  • Runner: " + (.runner_name // "pending") + "\n" +
        "  • Runner Group: " + (.runner_group_name // "default") + "\n" +
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        ' >> "$EXECUTION_LOG"
    else
        echo "• ジョブ情報の取得に失敗" >> "$EXECUTION_LOG"
    fi

    # アーティファクト情報
    echo "" >> "$EXECUTION_LOG"
    echo "📦 ARTIFACTS INFORMATION" >> "$EXECUTION_LOG"
    echo "═══════════════════════════════════════════════════════════════" >> "$EXECUTION_LOG"
    
    ARTIFACTS_INFO=$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID/artifacts" 2>/dev/null) || echo ""
    
    if [ -n "$ARTIFACTS_INFO" ]; then
        ARTIFACT_COUNT=$(echo "$ARTIFACTS_INFO" | jq '.total_count // 0')
        echo "• Total Artifacts: $ARTIFACT_COUNT" >> "$EXECUTION_LOG"
        echo "" >> "$EXECUTION_LOG"
        
        if [ "$ARTIFACT_COUNT" -gt 0 ]; then
            echo "$ARTIFACTS_INFO" | jq -r '.artifacts[] | 
            "Artifact: " + .name + "\n" +
            "  • ID: " + (.id | tostring) + "\n" +
            "  • Size: " + (.size_in_bytes | tostring) + " bytes\n" +
            "  • Created: " + .created_at + "\n" +
            "  • Updated: " + .updated_at + "\n" +
            "  • Expired: " + (.expired | tostring) + "\n" +
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            ' >> "$EXECUTION_LOG"
        fi
    else
        echo "• アーティファクト情報の取得に失敗" >> "$EXECUTION_LOG"
    fi

    # ダウンロードされたファイル情報
    echo "" >> "$EXECUTION_LOG"
    echo "📁 DOWNLOADED FILES" >> "$EXECUTION_LOG"
    echo "═══════════════════════════════════════════════════════════════" >> "$EXECUTION_LOG"
    
    if [ -d "$PROJECT_DIR" ]; then
        TOTAL_FILES=$(find "$PROJECT_DIR" -type f | wc -l)
        TOTAL_SIZE=$(du -sh "$PROJECT_DIR" 2>/dev/null | cut -f1 || echo "Unknown")
        
        echo "• Total Files: $TOTAL_FILES" >> "$EXECUTION_LOG"
        echo "• Total Size: $TOTAL_SIZE" >> "$EXECUTION_LOG"
        echo "" >> "$EXECUTION_LOG"
        echo "File Structure:" >> "$EXECUTION_LOG"
        find "$PROJECT_DIR" -type f -exec ls -la {} \; 2>/dev/null | head -50 | while read -r line; do
            echo "  $line" >> "$EXECUTION_LOG"
        done
    fi

    # 特定ワークフローの特別な処理
    case "$WORKFLOW_NAME" in
        *"Meta Workflow"*)
            echo "" >> "$EXECUTION_LOG"
            echo "🔧 META WORKFLOW SPECIFIC INFORMATION" >> "$EXECUTION_LOG"
            echo "═══════════════════════════════════════════════════════════════" >> "$EXECUTION_LOG"
            
            # メタワークフローブランチを探す
            META_BRANCH=$(echo "$RUN_INFO" | jq -r '.head_branch' | grep -E '^meta-workflow/' || echo "")
            if [ -n "$META_BRANCH" ]; then
                echo "• Meta Workflow Branch: $META_BRANCH" >> "$EXECUTION_LOG"
                echo "• Branch Pattern: Dedicated branch strategy" >> "$EXECUTION_LOG"
                
                # ブランチから追加情報を取得しようと試みる
                BRANCH_INFO=$(gh api "repos/$GITHUB_REPOSITORY/branches/$META_BRANCH" 2>/dev/null) || echo ""
                if [ -n "$BRANCH_INFO" ]; then
                    echo "• Branch SHA: $(echo "$BRANCH_INFO" | jq -r '.commit.sha')" >> "$EXECUTION_LOG"
                    echo "• Branch Protected: $(echo "$BRANCH_INFO" | jq -r '.protected')" >> "$EXECUTION_LOG"
                fi
            fi
            ;;
        *"Video Content Creation"*)
            echo "" >> "$EXECUTION_LOG"
            echo "🎥 VIDEO PRODUCTION SPECIFIC INFORMATION" >> "$EXECUTION_LOG"
            echo "═══════════════════════════════════════════════════════════════" >> "$EXECUTION_LOG"
            echo "• Production Pipeline: Video Content Creation v8" >> "$EXECUTION_LOG"
            echo "• Expected Outputs: BGM, Narration, Images, Videos, Final Assembly" >> "$EXECUTION_LOG"
            ;;
    esac

    # フッター
    echo "" >> "$EXECUTION_LOG"
    echo "✨ LOG GENERATED BY" >> "$EXECUTION_LOG"
    echo "═══════════════════════════════════════════════════════════════" >> "$EXECUTION_LOG"
    echo "$SCRIPT_NAME v$VERSION" >> "$EXECUTION_LOG"
    echo "Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$EXECUTION_LOG"
    echo "Repository: $GITHUB_REPOSITORY" >> "$EXECUTION_LOG"
    echo "" >> "$EXECUTION_LOG"
    
    echo "✅ 実行ログを生成: $EXECUTION_LOG"
fi

# ワークフロー情報ファイルを作成
echo ""
echo "📋 ワークフロー情報ファイルを作成中..."

cat > "$PROJECT_DIR/workflow-info.json" << EOF
{
  "script_version": "$VERSION",
  "download_timestamp": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "workflow": {
    "name": "$WORKFLOW_NAME",
    "run_id": "$RUN_ID",
    "run_number": "$RUN_NUMBER",
    "title": "$RUN_TITLE",
    "status": "$STATUS",
    "conclusion": "$CONCLUSION",
    "created_at": "$RUN_DATE",
    "branch": "$BRANCH_NAME"
  },
  "repository": {
    "full_name": "$GITHUB_REPOSITORY",
    "run_url": "https://github.com/$GITHUB_REPOSITORY/actions/runs/$RUN_ID"
  },
  "download_options": {
    "logs_included": $([ "$LOGS_ONLY" = true ] || [ "$ARTIFACTS_ONLY" = false ] && echo "true" || echo "false"),
    "artifacts_included": $([ "$ARTIFACTS_ONLY" = true ] || [ "$LOGS_ONLY" = false ] && echo "true" || echo "false"),
    "forced": $FORCE_DOWNLOAD
  },
  "files": {
    "execution_log": "execution-logs/workflow-execution-log.txt",
    "project_info": "workflow-info.json"
  }
}
EOF

# ファイル整理（既存のVideo Content Creation専用ロジックを汎用化）
echo ""
echo "🔧 ファイル構造を整理中..."

cd "$PROJECT_DIR" || exit 1

# ワークフロー固有の整理処理
case "$WORKFLOW_NAME" in
    *"Video Content Creation"*)
        # Video Content Creation専用の整理
        mkdir -p audio/{bgm,narration} images/{intro,main,outro} videos/{intro,main,outro} planning metadata
        
        # BGM移動
        if [ -d "bgm-${RUN_NUMBER}" ]; then
            mv "bgm-${RUN_NUMBER}"/* audio/bgm/ 2>/dev/null || true
        fi
        
        # ナレーション移動（高度な選択ロジック）
        if [ -d "narration-${RUN_NUMBER}" ]; then
            NARRATION_FILES=($(find "narration-${RUN_NUMBER}" -name "narration.mp3" -type f))
            
            if [ ${#NARRATION_FILES[@]} -gt 0 ]; then
                echo "🔍 Found ${#NARRATION_FILES[@]} narration file(s)"
                
                BEST_NARRATION=""
                BEST_SIZE=0
                
                for NARRATION_FILE in "${NARRATION_FILES[@]}"; do
                    NARRATION_SIZE=$(stat -c%s "$NARRATION_FILE" 2>/dev/null || echo "0")
                    echo "  - $NARRATION_FILE: ${NARRATION_SIZE} bytes"
                    
                    if [ "$NARRATION_SIZE" -gt 400000 ] && [ "$NARRATION_SIZE" -lt 500000 ]; then
                        BEST_NARRATION="$NARRATION_FILE"
                        BEST_SIZE="$NARRATION_SIZE"
                        echo "    ✅ 実際の音声ファイルを検出"
                        break
                    elif [ "$NARRATION_SIZE" -gt "$BEST_SIZE" ] && [ "$NARRATION_SIZE" -lt 600000 ]; then
                        BEST_NARRATION="$NARRATION_FILE"
                        BEST_SIZE="$NARRATION_SIZE"
                    fi
                done
                
                if [ -n "$BEST_NARRATION" ]; then
                    cp "$BEST_NARRATION" audio/narration/narration.mp3
                    echo "✅ 最適なナレーションファイルを選択: $BEST_NARRATION ($BEST_SIZE bytes)"
                fi
            fi
        fi
        
        # その他のファイル移動
        for dir in planning environment; do
            if [ -d "${dir}-${RUN_NUMBER}" ]; then
                mv "${dir}-${RUN_NUMBER}"/* "${dir}/" 2>/dev/null || true
            fi
        done
        
        # 画像・動画移動
        for scene in intro main outro; do
            if [ -d "images-${scene}-${RUN_NUMBER}" ]; then
                mv "images-${scene}-${RUN_NUMBER}"/* "images/${scene}/" 2>/dev/null || true
            fi
            if [ -d "videos-${scene}-${RUN_NUMBER}" ]; then
                mv "videos-${scene}-${RUN_NUMBER}"/* "videos/${scene}/" 2>/dev/null || true
            fi
        done
        
        # 最終パッケージ移動
        if [ -d "final-video-package-${RUN_NUMBER}" ]; then
            mv "final-video-package-${RUN_NUMBER}"/* . 2>/dev/null || true
        fi
        ;;
        
    *"Meta Workflow"*)
        # Meta Workflow専用の整理
        mkdir -p generated-workflows metadata analysis logs
        
        # メタワークフロー生成物の整理
        find . -name "*.yml" -not -path "./execution-logs/*" -not -name "workflow-info.json" -exec mv {} generated-workflows/ \; 2>/dev/null || true
        find . -name "*.json" -not -path "./execution-logs/*" -not -name "workflow-info.json" -exec mv {} metadata/ \; 2>/dev/null || true
        find . -name "*.md" -not -path "./execution-logs/*" -exec mv {} analysis/ \; 2>/dev/null || true
        ;;
        
    *)
        # 汎用的な整理
        mkdir -p outputs logs metadata
        
        # 一般的なファイル整理
        find . -name "*.log" -not -path "./execution-logs/*" -exec mv {} logs/ \; 2>/dev/null || true
        find . -name "*.json" -not -path "./execution-logs/*" -not -name "workflow-info.json" -exec mv {} metadata/ \; 2>/dev/null || true
        find . -name "*.md" -not -path "./execution-logs/*" -exec mv {} outputs/ \; 2>/dev/null || true
        ;;
esac

# 空のアーティファクトディレクトリを削除
rmdir *-${RUN_NUMBER} 2>/dev/null || true

cd - > /dev/null

# ダウンロード完了をマーク
echo "$RUN_ID" >> "$DOWNLOAD_MARKER"

# ZIP作成
if [ "$CREATE_ZIP" = true ]; then
    echo ""
    echo "📦 ZIPアーカイブを作成中..."
    
    ARCHIVE_NAME="${CLEAN_WORKFLOW_NAME}-run-${RUN_NUMBER}-$(date +%Y%m%d-%H%M%S).zip"
    
    if command -v zip >/dev/null 2>&1; then
        (cd projects && zip -r "$ARCHIVE_NAME" "$(basename "$PROJECT_DIR")" > /dev/null)
        echo "✅ アーカイブ作成完了: projects/$ARCHIVE_NAME"
    else
        echo "⚠️ zip コマンドが見つかりません。アーカイブをスキップします。"
    fi
fi

# 結果表示
echo ""
echo "✅ ダウンロード完了!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 Location: $PROJECT_DIR"
echo "📊 Files: $(find "$PROJECT_DIR" -type f | wc -l) total files"
echo "💾 Size: $(du -sh "$PROJECT_DIR" | cut -f1)"

if [ "$LOGS_ONLY" = false ] && [ "$ARTIFACTS_ONLY" = false ]; then
    echo "📋 Logs: execution-logs/workflow-execution-log.txt"
    echo "📦 Artifacts: アーティファクトディレクトリ内"
elif [ "$LOGS_ONLY" = true ]; then
    echo "📋 Logs Only: execution-logs/workflow-execution-log.txt"
elif [ "$ARTIFACTS_ONLY" = true ]; then
    echo "📦 Artifacts Only: アーティファクトディレクトリ内"
fi

echo ""
echo "🚀 次のステップ:"
echo "   1. 実行ログを確認: cat $PROJECT_DIR/execution-logs/workflow-execution-log.txt"
echo "   2. プロジェクト情報: cat $PROJECT_DIR/workflow-info.json"
if [ -f "$PROJECT_DIR/final_video.mp4" ]; then
    echo "   3. 動画を確認: open $PROJECT_DIR/final_video.mp4"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"