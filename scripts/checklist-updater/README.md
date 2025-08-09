# Checklist Auto-Updater

ログ履歴から自動的にチェックリストドキュメントを更新するシステムです。

## 🎯 機能

- 1時間ごとにログファイルをスキャンして新しいパターンを検出
- 汎用チェックリストとドメイン特有チェックリストを自動更新
- バックグラウンドでデーモンとして動作

## 📂 ファイル構成

```
scripts/checklist-updater/
├── README.md           # このファイル
├── start.sh           # デーモン起動スクリプト
├── stop.sh            # デーモン停止スクリプト
├── status.sh          # ステータス確認スクリプト
└── update-from-logs.py # 実際の更新処理を行うPythonスクリプト
```

## 🔧 必要なファイル

**これらのファイルはすべて必要です：**

1. **`update-from-logs.py`** - コア機能
   - ログファイルの解析
   - パターンの抽出と分類
   - チェックリストの更新

2. **`start.sh`** - デーモン管理
   - バックグラウンドプロセスの起動
   - 1時間ごとの自動実行

3. **`stop.sh`** - デーモン管理
   - プロセスの安全な停止

4. **`status.sh`** - 監視
   - 動作状態の確認
   - 次回更新時刻の表示

## 🚀 使い方

### 自動更新を開始
```bash
./scripts/checklist-updater/start.sh
```

### ステータス確認
```bash
./scripts/checklist-updater/status.sh
```

### ログの監視
```bash
tail -f projects/workflow-execution-logs/auto-updater.log
```

### 自動更新を停止
```bash
./scripts/checklist-updater/stop.sh
```

### 手動で一度だけ実行
```bash
python3 scripts/checklist-updater/update-from-logs.py
```

## 📝 更新対象

- **汎用チェックリスト**: `projects/workflow-execution-logs/meta-workflow-construction-checklist.md`
- **ドメイン特有チェックリスト**: `meta/domain-templates/[domain]/checklist-[domain]-specific.md`

## ⚙️ 設定

- **更新間隔**: 1時間（start.sh内の`sleep 3600`で調整可能）
- **スキャン範囲**: 過去24時間のログ（update-from-logs.py内の`--hours 24`で調整可能）
- **PIDファイル**: `.checklist-updater.pid`（プロジェクトルート）
- **ログファイル**: `projects/workflow-execution-logs/auto-updater.log`