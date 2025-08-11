#!/bin/bash

# 永続的なデーモンとして実行する方法

echo "=== チェックリスト自動更新デーモン永続化オプション ==="
echo ""
echo "現在のデーモン（PID: $(cat /tmp/checklist-updater.pid 2>/dev/null || echo 'なし')）はターミナル依存です。"
echo ""
echo "永続化する方法："
echo ""
echo "1. nohupで実行（ログアウト後も継続）："
echo "   nohup bash scripts/checklist-updater/start-daemon.sh > /dev/null 2>&1 &"
echo ""
echo "2. systemdサービスとして登録（Linux/WSL2）："
echo "   sudo cp scripts/checklist-updater/checklist-updater.service /etc/systemd/system/"
echo "   sudo systemctl enable checklist-updater"
echo "   sudo systemctl start checklist-updater"
echo ""
echo "3. cronで定期実行（デーモンではなくcron）："
echo "   crontab -e"
echo "   0 * * * * cd /path/to/kamui_rossy && python3 scripts/checklist-updater/advanced-log-analyzer.py"
echo ""
echo "推奨: WSL2環境では方法1（nohup）が簡単で効果的です。"