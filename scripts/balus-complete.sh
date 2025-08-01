#!/bin/bash
# 🏰💥 完全バルス - GitHub Actions完全リセットスクリプト
# Complete GitHub Actions Reset Protocol

echo "🏰💥 完全バルス実行開始..."
echo "GitHub Actions の実行履歴とキャッシュを完全削除します"

# Phase 1: GitHub Actions 実行履歴削除
echo ""
echo "Phase 1: 🗂️ GitHub Actions実行履歴削除"
echo "========================================"

# 実行履歴を取得して削除
run_count=0
gh run list --limit 500 --json databaseId --jq '.[].databaseId' | while read run_id; do
    if [ -n "$run_id" ]; then
        run_count=$((run_count + 1))
        echo "[$run_count] Deleting run $run_id..."
        echo "y" | gh run delete "$run_id" 2>/dev/null && echo "  ✓ Deleted" || echo "  • Skip"
    fi
done

echo ""
echo "Phase 2: 🗄️ GitHub Actions キャッシュ削除"
echo "========================================"

# キャッシュ一覧を取得して削除
cache_count=0
gh cache list --json id --jq '.[].id' | while read cache_id; do
    if [ -n "$cache_id" ]; then
        cache_count=$((cache_count + 1))
        echo "[$cache_count] Deleting cache $cache_id..."
        gh cache delete "$cache_id" 2>/dev/null && echo "  ✓ Cache deleted" || echo "  • Cache skip"
    fi
done

echo ""
echo "Phase 3: 🧹 验证とクリーンアップ確認"
echo "=================================="

# 残存確認
echo "残存実行履歴:"
remaining_runs=$(gh run list --limit 10 | wc -l)
if [ "$remaining_runs" -eq 1 ]; then
    echo "  ✓ 実行履歴: 完全削除済み"
else
    echo "  ⚠️ 実行履歴: $((remaining_runs - 1))件 残存"
fi

echo "残存キャッシュ:"
remaining_cache=$(gh cache list | wc -l)
if [ "$remaining_cache" -eq 0 ]; then
    echo "  ✓ キャッシュ: 完全削除済み"
else
    echo "  ⚠️ キャッシュ: $remaining_cache件 残存"
fi

echo ""
echo "🏰✨ 完全バルス完了！"
echo "GitHub Actions の状態が完全にリセットされました"
echo "startup_failure の原因となるキャッシュ問題を解決"