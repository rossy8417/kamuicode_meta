# Claude Code vs MCP 使い分けガイドライン

## 🎯 基本原則

**Claude Code GitHub Actions直接実行を使用:**
- テキスト生成
- プロンプト分析  
- タスク分解
- ワークフロープランニング
- コード生成
- 設定ファイル作成
- ドキュメント生成

**MCPサーバーを使用:**
- 画像生成 (Google Imagen3, Fal.ai等)
- 動画生成 (Veo3, Hailuo等)
- 音声生成 (Google Lyria等)
- 3D生成 (Hunyuan3D等)
- 複雑なマルチモーダル処理

## 📋 具体的な使い分け

### ✅ Claude Code 直接実行の例

```yaml
# タスク分解
- name: Decompose Tasks
  run: |
    claude --continue "$(cat task-decomposition-prompt.md)" \
      --output-format text

# ワークフロー生成
- name: Generate Workflow
  run: |
    claude --continue "Generate GitHub Actions workflow for: ${{ inputs.description }}" \
      --output-format text
```

### 🔌 MCP使用の例

```yaml
# AI生成サービスが必要な場合のみ
- name: Generate Media Content
  run: |
    claude --continue "Generate video advertisement" \
      --mcp-config .claude/mcp-kamuicode.json \
      --allowedTools "t2v-fal-veo3-fast,t2i-google-imagen3"
```

## 🔧 MCP設定の動的生成

ワークフロータイプに応じてMCP設定を動的に作成：

```yaml
- name: Setup MCP Config (if needed)
  run: |
    if [[ "${{ inputs.workflow_type }}" =~ ^(image|video|audio)-generation$ ]]; then
      mkdir -p .claude
      cat > .claude/mcp-kamuicode.json << 'EOF'
    {
      "mcpServers": {
        "ai-generation": {
          "type": "http", 
          "url": "https://mcp-server-url",
          "description": "AI generation services"
        }
      }
    }
    EOF
    else
      echo "MCP not required for text-only workflow"
    fi
```

## 🚀 パフォーマンス最適化

1. **テキスト処理**: Claude Code直接実行（高速）
2. **AI生成**: MCP使用（必要時のみ）
3. **フォールバック**: MCP失敗時はClaude Code直接実行

## 🔍 トラブルシューティング

### よくある問題と解決法

**問題**: テキスト生成でMCPエラー
**解決**: Claude Code直接実行に変更

**問題**: 画像生成で認証エラー  
**解決**: MCP設定を確認・再作成

**問題**: 不要なMCP呼び出し
**解決**: ワークフロータイプをチェックしてMCP使用を条件付きに

## 📊 効率性の比較

| タスク | Claude Code直接 | MCP | 推奨 |
|--------|----------------|-----|------|
| テキスト生成 | ✅ 高速 | ❌ 不要 | Claude Code |
| 画像生成 | ❌ 不可 | ✅ 必要 | MCP |
| タスク分解 | ✅ 最適 | ❌ オーバースペック | Claude Code |
| 動画生成 | ❌ 不可 | ✅ 必要 | MCP |

---
🎯 **原則**: シンプルなタスクはClaude Code直接、AI生成サービスが必要な場合のみMCPを使用