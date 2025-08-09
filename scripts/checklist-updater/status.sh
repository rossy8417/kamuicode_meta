#!/bin/bash

# チェックリスト自動更新デーモンのステータスを確認するスクリプト

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
PID_FILE="$PROJECT_ROOT/.checklist-updater.pid"
LOG_FILE="$PROJECT_ROOT/projects/workflow-execution-logs/auto-updater.log"

echo "========================================="
echo "📊 Checklist Auto-Updater Status"
echo "========================================="
echo ""

# PIDファイルの確認
if [ ! -f "$PID_FILE" ]; then
    echo "❌ Status: NOT RUNNING"
    echo "   (PID file not found)"
else
    PID=$(cat "$PID_FILE")
    
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ Status: RUNNING"
        echo "📌 Process ID: $PID"
        
        # プロセス情報を表示
        echo ""
        echo "📋 Process Details:"
        ps -fp "$PID" | tail -n 1
        
        # 最後の更新時刻を確認
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "📅 Last Update Activity:"
            tail -n 20 "$LOG_FILE" | grep -E "Starting checklist update|completed successfully|failed|No changes" | tail -n 5
        fi
        
        # 次の更新時刻を推定
        if [ -f "$LOG_FILE" ]; then
            LAST_UPDATE=$(grep "Starting checklist update" "$LOG_FILE" | tail -n 1 | sed 's/.*\[\(.*\)\].*/\1/')
            if [ -n "$LAST_UPDATE" ]; then
                echo ""
                echo "⏰ Last update started: $LAST_UPDATE"
                
                # 次の更新時刻を計算（概算）
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    # macOS
                    NEXT_UPDATE=$(date -j -f "%Y-%m-%d %H:%M:%S" -v+1H "$LAST_UPDATE" "+%Y-%m-%d %H:%M:%S" 2>/dev/null)
                else
                    # Linux
                    NEXT_UPDATE=$(date -d "$LAST_UPDATE + 1 hour" "+%Y-%m-%d %H:%M:%S" 2>/dev/null)
                fi
                
                if [ -n "$NEXT_UPDATE" ]; then
                    echo "⏱️ Next update expected: $NEXT_UPDATE (approximately)"
                fi
            fi
        fi
    else
        echo "❌ Status: NOT RUNNING"
        echo "   (Process $PID not found - stale PID file)"
        echo ""
        echo "ℹ️ To clean up: rm $PID_FILE"
    fi
fi

echo ""
echo "========================================="
echo ""

# ログファイルの確認
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(du -h "$LOG_FILE" | cut -f1)
    LOG_LINES=$(wc -l < "$LOG_FILE")
    echo "📁 Log File: $LOG_FILE"
    echo "   Size: $LOG_SIZE, Lines: $LOG_LINES"
    echo ""
    echo "To monitor logs in real-time:"
    echo "  tail -f $LOG_FILE"
else
    echo "📁 Log File: Not yet created"
fi

echo ""
echo "🔧 Available Commands:"
echo "  Start:   $SCRIPT_DIR/start.sh"
echo "  Stop:    $SCRIPT_DIR/stop.sh"
echo "  Status:  $SCRIPT_DIR/status.sh"