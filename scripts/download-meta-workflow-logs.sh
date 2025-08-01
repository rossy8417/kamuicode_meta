#!/bin/bash

# Meta Workflow Execution Logs Download Script
# Usage: ./scripts/download-meta-workflow-logs.sh [run_id] [issue_number]

set -e

echo "📋 Meta Workflow Execution Logs Download Script"
echo "════════════════════════════════════════════════"

# Parameters
RUN_ID=${1:-""}
ISSUE_NUMBER=${2:-""}

# Help function
show_help() {
    echo "Usage: $0 [run_id] [issue_number]"
    echo ""
    echo "Download comprehensive execution logs from Meta Workflow v9 runs"
    echo ""
    echo "Parameters:"
    echo "  run_id       GitHub Actions run ID (optional - will prompt if not provided)"
    echo "  issue_number Issue number that triggered the workflow (optional)"
    echo ""
    echo "Examples:"
    echo "  $0 16666636509 56                    # Download specific run logs"
    echo "  $0                                   # Interactive mode"
    echo ""
    echo "The script will:"
    echo "  1. Find the Meta Workflow v9 branch created for the run"
    echo "  2. Download all execution logs and generated files"
    echo "  3. Create a local archive for easy access"
    echo ""
}

# Check if help requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Interactive mode if no parameters provided
if [[ -z "$RUN_ID" ]]; then
    echo "🔍 Finding recent Meta Workflow v9 runs..."
    echo ""
    
    # Show recent Meta Workflow runs
    echo "Recent Meta Workflow v9 executions:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    gh run list --workflow=".github/workflows/meta-workflow-executor-v9.yml" --limit=10 --json status,conclusion,databaseId,createdAt,displayTitle | \
    jq -r '.[] | 
    "• Run ID: " + (.databaseId | tostring) + 
    " | Status: " + .status + 
    " | " + (.conclusion // "in_progress") + 
    " | " + .createdAt + 
    " | " + .displayTitle'
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    read -p "Enter Run ID to download: " RUN_ID
    
    if [[ -z "$RUN_ID" ]]; then
        echo "❌ Run ID is required"
        exit 1
    fi
fi

# Validate run ID format
if ! [[ "$RUN_ID" =~ ^[0-9]+$ ]]; then
    echo "❌ Invalid Run ID format. Expected numeric value, got: $RUN_ID"
    exit 1
fi

echo "📥 Downloading logs for GitHub Actions Run ID: $RUN_ID"

# Get run information
echo "🔍 Fetching run information..."
RUN_INFO=$(gh api "repos/$(gh repo view --json owner,name --jq '.owner.login + "/" + .name')/actions/runs/$RUN_ID" 2>/dev/null) || {
    echo "❌ Failed to fetch run information for Run ID: $RUN_ID"
    echo "   Please verify the Run ID exists and you have access to the repository"
    exit 1
}

# Extract run details
RUN_STATUS=$(echo "$RUN_INFO" | jq -r '.status')
RUN_CONCLUSION=$(echo "$RUN_INFO" | jq -r '.conclusion // "in_progress"')
RUN_BRANCH=$(echo "$RUN_INFO" | jq -r '.head_branch')
RUN_CREATED=$(echo "$RUN_INFO" | jq -r '.created_at')

echo "✅ Run found:"
echo "   • Status: $RUN_STATUS"
echo "   • Conclusion: $RUN_CONCLUSION"  
echo "   • Branch: $RUN_BRANCH"
echo "   • Created: $RUN_CREATED"

# Try to find the meta-workflow branch
WORKFLOW_BRANCH=""
if [[ "$RUN_BRANCH" =~ ^meta-workflow/issue-.*$ ]]; then
    WORKFLOW_BRANCH="$RUN_BRANCH"
    echo "✅ Found Meta Workflow branch: $WORKFLOW_BRANCH"
else
    echo "🔍 Searching for Meta Workflow branch..."
    # Try to find branches with the run ID
    POSSIBLE_BRANCHES=$(gh api "repos/$(gh repo view --json owner,name --jq '.owner.login + "/" + .name')/branches" --jq ".[] | select(.name | contains(\"$RUN_ID\")) | .name" 2>/dev/null || echo "")
    
    if [[ -n "$POSSIBLE_BRANCHES" ]]; then
        WORKFLOW_BRANCH=$(echo "$POSSIBLE_BRANCHES" | head -1)
        echo "✅ Found possible Meta Workflow branch: $WORKFLOW_BRANCH"
    else
        echo "⚠️  Could not automatically find Meta Workflow branch"
        echo "   The logs might be in the main branch or a different branch"
        WORKFLOW_BRANCH="main"
    fi
fi

# Create local download directory
DOWNLOAD_DIR="downloads/meta-workflow-logs-run-$RUN_ID"
mkdir -p "$DOWNLOAD_DIR"

echo "📁 Creating download directory: $DOWNLOAD_DIR"

# Try to determine project folder
PROJECT_FOLDER="meta-workflow-issue-${ISSUE_NUMBER:-unknown}-$RUN_ID"

echo "🔍 Looking for execution logs..."

# Create a temporary directory for git operations
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Clone the repository to temp directory
echo "📦 Cloning repository (this may take a moment)..."
git clone -q "$(gh repo view --json url --jq '.url')" "$TEMP_DIR"
cd "$TEMP_DIR"

# Check if the workflow branch exists
if git show-ref --verify --quiet "refs/remotes/origin/$WORKFLOW_BRANCH"; then
    echo "✅ Checking out branch: $WORKFLOW_BRANCH"
    git checkout -q "$WORKFLOW_BRANCH" 2>/dev/null || {
        echo "⚠️  Could not checkout $WORKFLOW_BRANCH, using main branch"
        git checkout -q main
    }
else
    echo "⚠️  Branch $WORKFLOW_BRANCH not found, using main branch"
    git checkout -q main
fi

# Find the project folder
echo "🔍 Searching for project files..."
FOUND_PROJECTS=$(find generated/meta-workflow-projects -maxdepth 1 -type d -name "*$RUN_ID*" 2>/dev/null || echo "")

if [[ -n "$FOUND_PROJECTS" ]]; then
    PROJECT_FOLDER=$(basename "$FOUND_PROJECTS" | head -1)
    echo "✅ Found project folder: $PROJECT_FOLDER"
else
    echo "🔍 Searching with broader pattern..."
    FOUND_PROJECTS=$(find generated/meta-workflow-projects -maxdepth 1 -type d 2>/dev/null | grep -E "(issue-${ISSUE_NUMBER:-[0-9]+}|$RUN_ID)" | head -1 || echo "")
    
    if [[ -n "$FOUND_PROJECTS" ]]; then
        PROJECT_FOLDER=$(basename "$FOUND_PROJECTS")
        echo "✅ Found project folder: $PROJECT_FOLDER"
    else
        echo "❌ Could not find project folder for Run ID: $RUN_ID"
        echo "   Available projects:"
        find generated/meta-workflow-projects -maxdepth 1 -type d 2>/dev/null | tail -5
        exit 1
    fi
fi

PROJECT_PATH="generated/meta-workflow-projects/$PROJECT_FOLDER"

# Verify project directory exists
if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "❌ Project directory not found: $PROJECT_PATH"
    exit 1
fi

echo "📋 Found project at: $PROJECT_PATH"

# Copy all files to download directory
echo "📥 Copying project files..."
cp -r "$PROJECT_PATH"/* "../$DOWNLOAD_DIR/" 2>/dev/null || {
    echo "❌ Failed to copy project files"
    exit 1
}

# Return to original directory
cd - > /dev/null

# Generate download summary
cat > "$DOWNLOAD_DIR/download-info.txt" << EOF
═══════════════════════════════════════════════════════════════
               META WORKFLOW LOGS DOWNLOAD INFO
═══════════════════════════════════════════════════════════════

📥 DOWNLOAD DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Downloaded: $(date -u '+%Y-%m-%d %H:%M:%S UTC')
• Run ID: $RUN_ID
• Status: $RUN_STATUS
• Conclusion: $RUN_CONCLUSION
• Branch: $WORKFLOW_BRANCH
• Project Folder: $PROJECT_FOLDER

📁 DOWNLOADED FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$(find "$DOWNLOAD_DIR" -type f -name "*.txt" -o -name "*.yml" -o -name "*.json" | sort)

📊 DOWNLOAD STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total Files: $(find "$DOWNLOAD_DIR" -type f | wc -l)
• Total Size: $(du -sh "$DOWNLOAD_DIR" | cut -f1)
• Execution Logs: $(find "$DOWNLOAD_DIR/execution-logs" -name "*.txt" 2>/dev/null | wc -l) files
• Workflows: $(find "$DOWNLOAD_DIR/workflows" -name "*.yml" 2>/dev/null | wc -l) files

🚀 NEXT STEPS  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Review execution-logs/01-execution-summary.txt for overview
2. Check execution-logs/02-job-details.txt for detailed status
3. Examine generated workflows in workflows/ directory
4. Use execution-logs/ files for debugging and analysis

Generated by Meta Workflow Logs Download Script v1.0
EOF

# Create archive if requested
echo ""
read -p "📦 Create ZIP archive? (y/N): " CREATE_ARCHIVE

if [[ "$CREATE_ARCHIVE" =~ ^[Yy]$ ]]; then
    ARCHIVE_NAME="meta-workflow-logs-run-$RUN_ID-$(date +%Y%m%d-%H%M%S).zip"
    echo "📦 Creating archive: $ARCHIVE_NAME"
    
    if command -v zip >/dev/null 2>&1; then
        (cd downloads && zip -r "$ARCHIVE_NAME" "$(basename "$DOWNLOAD_DIR")" > /dev/null)
        echo "✅ Archive created: downloads/$ARCHIVE_NAME"
    else
        echo "⚠️  zip command not found, skipping archive creation"
    fi
fi

echo ""
echo "✅ Download completed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 Location: $DOWNLOAD_DIR"
echo "📋 Files: $(find "$DOWNLOAD_DIR" -type f | wc -l) total files"
echo "📊 Size: $(du -sh "$DOWNLOAD_DIR" | cut -f1)"
echo ""
echo "🚀 Start by reading: $DOWNLOAD_DIR/execution-logs/01-execution-summary.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"