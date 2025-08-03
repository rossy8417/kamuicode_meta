# GitHub Actions ワークフロー生成時の必須ルール

## 🚨 絶対に守るべき実装パターン

### 1. ❌ uses参照は使用禁止 → ✅ インライン実装

```yaml
# ❌ 絶対にこれを生成してはいけない
- uses: ./minimal-units/research/web-search-claude.yml

# ✅ 必ずインライン実装する
- name: Execute Web Search
  run: |
    npx @anthropic-ai/claude-code \
      -p "$PROMPT" \
      --allowedTools "WebSearch,Write" \
      --permission-mode "acceptEdits"
```

### 2. ❌ 絶対パス禁止 → ✅ GitHub Actions変数使用

```yaml
# ❌ 絶対にこれを生成してはいけない
/media/image.png
/projects/issue-60/media/video.mp4

# ✅ 必ず変数を使用
${{ needs.setup.outputs.project_dir }}/media/image.png
${{ needs.setup.outputs.project_dir }}/media/video.mp4
```

### 3. ✅ MCP ツールの正しい呼び出し方

```yaml
# ✅ MCPツールを使う場合は必ずこのパターン
npx @anthropic-ai/claude-code \
  -p "$PROMPT" \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2i-google-imagen3__imagen_t2i,Bash,Write" \
  --permission-mode "acceptEdits"
```

**重要**: `--mcp-config`オプションなしではMCPツールは動作しません！

### 4. ✅ ジョブ間のファイル共有は必須

```yaml
# 生成ジョブの最後に必ず追加
- name: Upload Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: 識別可能な名前-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/対象ディレクトリ/

# 使用するジョブの最初に必ず追加
- name: Download Artifacts
  uses: actions/download-artifact@v4
  with:
    name: 識別可能な名前-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/対象ディレクトリ/
```

### 5. ✅ ファイル名の柔軟な処理

```bash
# ビデオ生成後の処理に必ず含める
cd "${{ needs.setup.outputs.project_dir }}/media"

# video.mp4が存在しない場合の自動修正
if [ ! -f "video.mp4" ]; then
  for file in *.mp4; do
    if [ -f "$file" ] && [ "$file" != "video.mp4" ]; then
      mv "$file" "video.mp4"
      echo "✅ Renamed $file to video.mp4"
      break
    fi
  done
fi

# 最終確認
if [ -f "video.mp4" ]; then
  echo "completed=true" >> $GITHUB_OUTPUT
  echo "video_path=${{ needs.setup.outputs.project_dir }}/media/video.mp4" >> $GITHUB_OUTPUT
else
  echo "❌ Video generation failed"
  ls -la  # デバッグ情報
  exit 1
fi
```

### 6. ✅ エラー診断情報の組み込み

```bash
# すべての確認処理でエラー時の診断情報を出力
if [ ! -f "期待するファイル" ]; then
  echo "❌ Error: Expected file not found"
  echo "Current directory contents:"
  ls -la
  echo "Full path checked: $(pwd)/期待するファイル"
  exit 1
fi
```

## 📋 チェックリスト（ワークフロー生成時）

生成されたワークフローが以下を満たしているか確認：

- [ ] `uses: ./minimal-units/`が含まれていない
- [ ] すべてのパスが`${{ needs.setup.outputs.project_dir }}`を使用
- [ ] MCPツール使用時は`--mcp-config`オプションあり
- [ ] ジョブ間でファイルを渡す場合はartifact upload/downloadあり
- [ ] ファイル生成後は存在確認とエラー処理あり
- [ ] ファイル名が固定できない場合は自動リネーム処理あり

## 🎯 メタワークフローへの指示

これらのルールをメタワークフローのプロンプトに組み込むことで、最初から正しいワークフローを生成できます。