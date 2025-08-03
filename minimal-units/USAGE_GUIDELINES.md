# ミニマルユニット使用ガイドライン

## 🚨 重要：ミニマルユニットの使用方法

### ❌ 絶対にしてはいけないこと

```yaml
# ❌ WRONG - GitHub Actionsはローカルファイル参照をサポートしません
- uses: ./minimal-units/planning/web-search-claude.yml
  with:
    search_query: "京都 観光"
```

### ✅ 正しい使用方法

ミニマルユニットは**参照テンプレート**として使用し、実際のワークフローには**インライン実装**してください：

```yaml
# ✅ CORRECT - インライン実装
- name: Execute Web Search
  id: execute
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  run: |
    # web-search-claude.ymlの内容をここにコピー
    npx @anthropic-ai/claude-code \
      -p "$PROMPT" \
      --allowedTools "WebSearch,Write" \
      --permission-mode "acceptEdits"
```

## 📋 ジョブ間のデータ共有

### 必須：アーティファクトを使用

```yaml
# データ生成ジョブの最後
- name: Upload Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: search-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/metadata/

# データ使用ジョブの最初
- name: Download Artifacts
  uses: actions/download-artifact@v4
  with:
    name: search-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/metadata/
```

## 🔧 MCP ツール使用時の注意

```bash
# ✅ MCP設定ファイルを必ず指定
npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2i-google-imagen3__imagen_t2i,Bash,Write"
```

## 📝 ファイル名の柔軟な処理

動的に生成されるファイル名に対応：

```bash
# 期待するファイル名にリネーム
if [ ! -f "video.mp4" ]; then
  for file in *.mp4; do
    if [ -f "$file" ]; then
      mv "$file" "video.mp4"
      break
    fi
  done
fi
```

## 🎯 メタワークフローへの指示

メタワークフローがこれらのミニマルユニットを使用する際は：

1. **インライン実装**：`uses:`参照ではなく、内容をコピーして実装
2. **変数使用**：絶対パスではなく`${{ needs.setup.outputs.project_dir }}`を使用
3. **アーティファクト**：ジョブ間でファイルを共有する場合は必須
4. **エラー処理**：ファイル存在確認とエラーメッセージを含める