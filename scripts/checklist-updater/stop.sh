#!/bin/bash

# チェックリスト自動更新デーモンを停止するスクリプト

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
PID_FILE="$PROJECT_ROOT/.checklist-updater.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "⚠️ Checklist auto-updater is not running (PID file not found)"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "🛑 Stopping checklist auto-updater (PID: $PID)..."
    kill "$PID"
    
    # プロセスが終了するまで待つ
    for i in {1..10}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done
    
    # まだ生きていたら強制終了
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️ Process didn't stop gracefully, forcing termination..."
        kill -9 "$PID"
    fi
    
    rm "$PID_FILE"
    echo "✅ Checklist auto-updater stopped successfully"
else
    echo "⚠️ Process with PID $PID not found (removing stale PID file)"
    rm "$PID_FILE"
fi