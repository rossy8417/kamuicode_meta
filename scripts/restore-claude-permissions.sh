#!/bin/bash
# Claude Code設定を復元するスクリプト

SETTINGS_FILE=".claude/settings.local.json"
TEMPLATE_FILE=".claude/settings.local.template.json"

echo "🔧 Claude Code設定復元ツール"
echo "============================="

# テンプレートファイルの存在確認
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "❌ テンプレートファイルが見つかりません: $TEMPLATE_FILE"
    exit 1
fi

# 現在の設定をバックアップ
if [ -f "$SETTINGS_FILE" ]; then
    BACKUP_FILE=".claude/backups/settings-$(date +%Y%m%d-%H%M%S).json"
    mkdir -p .claude/backups
    cp "$SETTINGS_FILE" "$BACKUP_FILE"
    echo "✅ 現在の設定をバックアップしました: $BACKUP_FILE"
fi

# テンプレートから復元
cp "$TEMPLATE_FILE" "$SETTINGS_FILE"
echo "✅ テンプレートから設定を復元しました"

# 権限リストを表示
echo ""
echo "📝 復元された権限:"
echo "  - Bash関連: git, gh, npm, python, 基本コマンドなど"
echo "  - ファイル操作: Edit, Read, Write, Glob, Grep, LS"
echo "  - 拡張ツール: Task, TodoWrite, WebFetch, WebSearch"
echo "  - スクリプト: ./scripts/*.sh へのアクセス"
echo ""
echo "💡 ヒント: 設定が上書きされた場合は、このスクリプトを再実行してください"