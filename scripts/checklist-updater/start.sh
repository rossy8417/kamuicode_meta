#!/bin/bash

# チェックリスト自動更新デーモンを起動するスクリプト
# 1時間ごとにログからチェックリストを自動更新

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
PID_FILE="$PROJECT_ROOT/.checklist-updater.pid"
LOG_FILE="$PROJECT_ROOT/projects/workflow-execution-logs/auto-updater.log"

# 既存のプロセスをチェック
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️ Checklist auto-updater is already running (PID: $OLD_PID)"
        echo "To stop it, run: $SCRIPT_DIR/stop.sh"
        exit 1
    else
        echo "🔄 Removing stale PID file"
        rm "$PID_FILE"
    fi
fi

# ログディレクトリ作成
mkdir -p "$(dirname "$LOG_FILE")"

echo "🚀 Starting checklist auto-updater daemon..."
echo "📝 Logs will be written to: $LOG_FILE"
echo "⏰ Update interval: Every 1 hour"

# バックグラウンドでデーモンを起動
nohup bash -c "
    while true; do
        echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] Starting checklist update...\" >> \"$LOG_FILE\"
        
        cd \"$PROJECT_ROOT\"
        
        # Pythonスクリプトを実行
        python3 scripts/checklist-updater/update-from-logs.py --hours 24 >> \"$LOG_FILE\" 2>&1
        
        if [ \$? -eq 0 ]; then
            echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] ✅ Update completed successfully\" >> \"$LOG_FILE\"
        else
            echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] ❌ Update failed\" >> \"$LOG_FILE\"
        fi
        
        # 変更があればgitにコミット（オプション）
        if ! git diff --quiet; then
            echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] 📊 Changes detected, committing...\" >> \"$LOG_FILE\"
            git add -A
            git commit -m \"chore: auto-update checklists from logs [\$(date '+%Y-%m-%d %H:%M')]\" >> \"$LOG_FILE\" 2>&1
            echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] ✅ Changes committed\" >> \"$LOG_FILE\"
        else
            echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] No changes detected\" >> \"$LOG_FILE\"
        fi
        
        echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] Sleeping for 1 hour...\" >> \"$LOG_FILE\"
        echo \"----------------------------------------\" >> \"$LOG_FILE\"
        
        # 1時間待機
        sleep 3600
    done
" > /dev/null 2>&1 &

# PIDを保存
DAEMON_PID=$!
echo $DAEMON_PID > "$PID_FILE"

echo "✅ Checklist auto-updater started successfully!"
echo "📌 Process ID: $DAEMON_PID"
echo "📁 PID file: $PID_FILE"
echo ""
echo "To monitor the updater:"
echo "  tail -f $LOG_FILE"
echo ""
echo "To stop the updater:"
echo "  $SCRIPT_DIR/stop.sh"
echo ""
echo "To check status:"
echo "  $SCRIPT_DIR/status.sh"