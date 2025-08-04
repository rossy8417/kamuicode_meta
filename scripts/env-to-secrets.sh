#!/bin/bash
# .envファイルからGitHub Secretsへ一括設定する簡易スクリプト

# 引数チェック
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <env-file>"
    echo "Example: $0 .env"
    exit 1
fi

ENV_FILE="$1"

# ファイル存在チェック
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: File '$ENV_FILE' not found"
    exit 1
fi

# gh CLIチェック
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed"
    exit 1
fi

# 認証チェック
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

# リポジトリ情報取得
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Setting secrets for: $REPO"
echo "From file: $ENV_FILE"
echo ""

# プレビュー
echo "=== Preview ==="
grep -v '^#' "$ENV_FILE" | grep -v '^$' | while IFS='=' read -r key value; do
    echo "$key = ${value:0:10}..."
done

echo ""
read -p "Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

# 設定実行
echo "Setting secrets..."
grep -v '^#' "$ENV_FILE" | grep -v '^$' | while IFS='=' read -r key value; do
    if gh secret set "$key" -b "$value" -R "$REPO"; then
        echo "✓ $key"
    else
        echo "✗ $key (failed)"
    fi
done

echo ""
echo "Done! Current secrets:"
gh secret list