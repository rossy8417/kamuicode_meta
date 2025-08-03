#!/bin/bash
# Download Workflow Artifacts with Deduplication
# 重複を避けて効率的にワークフローのアーティファクトをダウンロード

set -euo pipefail

# カラー出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# ヘルプ表示
show_help() {
    echo -e "${BLUE}Download Workflow Artifacts Script${NC}"
    echo ""
    echo "Usage: $0 [options] <workflow-name-or-run-id>"
    echo ""
    echo "Options:"
    echo "  -h, --help           Show this help message"
    echo "  -o, --output <dir>   Output directory (default: projects/downloads/YYYY-MM-DD)"
    echo "  -f, --force          Force download even if files exist"
    echo "  -l, --list           List artifacts without downloading"
    echo "  -c, --clean          Clean old downloads (keep last 5)"
    echo ""
    echo "Examples:"
    echo "  $0 meta-workflow-executor-v12"
    echo "  $0 --list 16709668564"
    echo "  $0 -o projects/issue-66-results 16709668564"
}

# デフォルト値
OUTPUT_BASE="projects/downloads"
FORCE_DOWNLOAD=false
LIST_ONLY=false
CLEAN_OLD=false
WORKFLOW_IDENTIFIER=""

# オプション解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -o|--output)
            OUTPUT_BASE="$2"
            shift 2
            ;;
        -f|--force)
            FORCE_DOWNLOAD=true
            shift
            ;;
        -l|--list)
            LIST_ONLY=true
            shift
            ;;
        -c|--clean)
            CLEAN_OLD=true
            shift
            ;;
        *)
            WORKFLOW_IDENTIFIER="$1"
            shift
            ;;
    esac
done

# クリーンアップモード
if [ "$CLEAN_OLD" = true ]; then
    echo -e "${YELLOW}🧹 Cleaning old downloads...${NC}"
    if [ -d "$OUTPUT_BASE" ]; then
        # 最新5つを除いて削除
        find "$OUTPUT_BASE" -maxdepth 1 -type d -name "20*" | sort -r | tail -n +6 | while read -r dir; do
            echo -e "${RED}  Removing: $dir${NC}"
            rm -rf "$dir"
        done
    fi
    echo -e "${GREEN}✅ Cleanup completed${NC}"
    exit 0
fi

# ワークフロー識別子チェック
if [ -z "$WORKFLOW_IDENTIFIER" ]; then
    echo -e "${RED}Error: Workflow name or run ID is required${NC}"
    show_help
    exit 1
fi

# ワークフロー実行IDを取得
if [[ "$WORKFLOW_IDENTIFIER" =~ ^[0-9]+$ ]]; then
    RUN_ID="$WORKFLOW_IDENTIFIER"
else
    # ワークフロー名から最新の実行を取得
    echo -e "${YELLOW}🔍 Finding latest run for workflow: $WORKFLOW_IDENTIFIER${NC}"
    RUN_INFO=$(gh run list --workflow="$WORKFLOW_IDENTIFIER" -L 1 --json databaseId,status,conclusion,createdAt)
    
    if [ -z "$RUN_INFO" ] || [ "$RUN_INFO" = "[]" ]; then
        echo -e "${RED}Error: No runs found for workflow: $WORKFLOW_IDENTIFIER${NC}"
        exit 1
    fi
    
    RUN_ID=$(echo "$RUN_INFO" | jq -r '.[0].databaseId')
    RUN_STATUS=$(echo "$RUN_INFO" | jq -r '.[0].status')
    RUN_CONCLUSION=$(echo "$RUN_INFO" | jq -r '.[0].conclusion')
    RUN_DATE=$(echo "$RUN_INFO" | jq -r '.[0].createdAt')
    
    echo -e "${GREEN}Found run:${NC}"
    echo -e "  Run ID: $RUN_ID"
    echo -e "  Status: $RUN_STATUS"
    echo -e "  Conclusion: $RUN_CONCLUSION"
    echo -e "  Created: $RUN_DATE"
fi

# アーティファクト一覧を取得
echo -e "${YELLOW}📋 Fetching artifacts for run $RUN_ID...${NC}"
ARTIFACTS=$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$RUN_ID/artifacts" --jq '.artifacts')
ARTIFACT_COUNT=$(echo "$ARTIFACTS" | jq 'length')

if [ "$ARTIFACT_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}No artifacts found for this run${NC}"
    exit 0
fi

echo -e "${GREEN}Found $ARTIFACT_COUNT artifacts:${NC}"
echo "$ARTIFACTS" | jq -r '.[] | "  - \(.name) (\(.size_in_bytes | tonumber / 1024 / 1024 | floor)MB)"'

# リストモードの場合はここで終了
if [ "$LIST_ONLY" = true ]; then
    exit 0
fi

# 出力ディレクトリを作成
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
OUTPUT_DIR="$OUTPUT_BASE/$TIMESTAMP"
mkdir -p "$OUTPUT_DIR"

# ダウンロードマニフェスト
MANIFEST_FILE="$OUTPUT_DIR/.manifest.json"
echo "{\"run_id\": \"$RUN_ID\", \"timestamp\": \"$TIMESTAMP\", \"artifacts\": {}}" > "$MANIFEST_FILE"

# 各アーティファクトをダウンロード
echo -e "${YELLOW}⬇ Downloading artifacts...${NC}"
echo "$ARTIFACTS" | jq -c '.[]' | while read -r artifact; do
    ARTIFACT_ID=$(echo "$artifact" | jq -r '.id')
    ARTIFACT_NAME=$(echo "$artifact" | jq -r '.name')
    ARTIFACT_SIZE=$(echo "$artifact" | jq -r '.size_in_bytes')
    ARTIFACT_PATH="$OUTPUT_DIR/$ARTIFACT_NAME"
    
    # 既存ファイルチェック
    if [ -d "$ARTIFACT_PATH" ] && [ "$FORCE_DOWNLOAD" = false ]; then
        echo -e "${GREEN}✓ Skipping '$ARTIFACT_NAME' - already exists${NC}"
        continue
    fi
    
    echo -e "${BLUE}⬇ Downloading '$ARTIFACT_NAME'...${NC}"
    
    # ダウンロード
    mkdir -p "$ARTIFACT_PATH"
    if gh run download "$RUN_ID" -n "$ARTIFACT_NAME" -D "$ARTIFACT_PATH"; then
        # マニフェストを更新
        jq --arg name "$ARTIFACT_NAME" \
           --arg id "$ARTIFACT_ID" \
           --arg size "$ARTIFACT_SIZE" \
           --arg path "$ARTIFACT_PATH" \
           '.artifacts[$name] = {id: $id, size: $size, path: $path, downloaded_at: now | todate}' \
           "$MANIFEST_FILE" > "${MANIFEST_FILE}.tmp" && \
        mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"
        
        echo -e "${GREEN}✓ Downloaded '$ARTIFACT_NAME'${NC}"
    else
        echo -e "${RED}✗ Failed to download '$ARTIFACT_NAME'${NC}"
    fi
done

# プロジェクト構造の整理
echo -e "${YELLOW}📁 Organizing downloaded files...${NC}"

# Issue番号ベースの整理
ISSUE_DIR=$(find "$OUTPUT_DIR" -name "issue_number.txt" -type f | head -1)
if [ -n "$ISSUE_DIR" ] && [ -f "$ISSUE_DIR" ]; then
    ISSUE_NUMBER=$(cat "$ISSUE_DIR")
    PROJECT_DIR="projects/issue-${ISSUE_NUMBER}-${TIMESTAMP}"
    
    echo -e "${BLUE}Creating project directory: $PROJECT_DIR${NC}"
    mkdir -p "$PROJECT_DIR"
    
    # アーティファクトを適切な場所に配置
    for artifact_dir in "$OUTPUT_DIR"/*; do
        if [ -d "$artifact_dir" ]; then
            artifact_name=$(basename "$artifact_dir")
            case "$artifact_name" in
                *workflow*)
                    mkdir -p "$PROJECT_DIR/generated-workflow"
                    cp -r "$artifact_dir"/* "$PROJECT_DIR/generated-workflow/" 2>/dev/null || true
                    ;;
                *domain*|*template*)
                    mkdir -p "$PROJECT_DIR/metadata"
                    cp -r "$artifact_dir"/* "$PROJECT_DIR/metadata/" 2>/dev/null || true
                    ;;
                *task*|*decomposition*)
                    mkdir -p "$PROJECT_DIR/analysis"
                    cp -r "$artifact_dir"/* "$PROJECT_DIR/analysis/" 2>/dev/null || true
                    ;;
                *)
                    mkdir -p "$PROJECT_DIR/artifacts"
                    cp -r "$artifact_dir"/* "$PROJECT_DIR/artifacts/" 2>/dev/null || true
                    ;;
            esac
        fi
    done
    
    # シンボリックリンクを作成
    ln -sf "$(realpath "$PROJECT_DIR")" "$OUTPUT_BASE/latest"
    
    echo -e "${GREEN}✅ Files organized in: $PROJECT_DIR${NC}"
fi

# サマリー表示
echo -e "${GREEN}📊 Download Summary:${NC}"
echo -e "  Run ID: $RUN_ID"
echo -e "  Total artifacts: $ARTIFACT_COUNT"
echo -e "  Output directory: $OUTPUT_DIR"
if [ -n "${PROJECT_DIR:-}" ]; then
    echo -e "  Project directory: $PROJECT_DIR"
fi
echo -e "  Manifest: $MANIFEST_FILE"

echo -e "${GREEN}✅ Download completed successfully!${NC}"