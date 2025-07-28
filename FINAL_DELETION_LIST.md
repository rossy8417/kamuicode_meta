# 🗑️ 最終削除対象リスト

## ✅ **削除対象（確認完了）**

### **1. テストワークフロー（8個）**
```bash
# test-から始まるワークフロー（7個）
rm .github/workflows/test-comment-trigger.yml
rm .github/workflows/test-direct-mcp-call.yml
rm .github/workflows/test-mcp-method-patterns.yml
rm .github/workflows/test-mcp-permissions.yml
rm .github/workflows/test-mcp-services-detail.yml
rm .github/workflows/test-mcp-settings-parameter.yml
rm .github/workflows/test-mcp-with-permissions.yml

# テスト用途のワークフロー（1個）
rm .github/workflows/audio-generation-test.yml
```

### **2. 廃止プロンプト（5個 - ディレクトリごと）**
```bash
# 完全に未使用確認済み
rm -rf meta/prompts/deprecated/
```

### **3. 空のメタデータディレクトリ（4個）**
```bash
rmdir generated/metadata/evaluation
rmdir generated/metadata/requirement-analysis  
rmdir generated/metadata/stepback-analysis
rmdir generated/metadata/task-decomposition
```

### **4. 特定用途の古いスクリプト**
```bash
rm -rf generated/news_video_scripts/
```

## 🚫 **削除しないもの（据え置き）**

### **Video関連ワークフロー（据え置き）**
- `.github/workflows/video-content-creation*.yml` → **保持**

### **重要なデータ**
- `meta/examples/` → 将来の参照予定
- `meta/prompts/stepback-to-tasks.md` → 直接参照中
- `generated/logs/` → 実行履歴
- `meta/ai-learning/` → AI学習データ

## 🚀 **実行コマンド**

```bash
# テストワークフロー削除（test-から始まる + テスト用途）
rm .github/workflows/test-*.yml
rm .github/workflows/audio-generation-test.yml

# 廃止プロンプト削除
rm -rf meta/prompts/deprecated/

# 空のメタデータディレクトリ削除
rmdir generated/metadata/evaluation 2>/dev/null || true
rmdir generated/metadata/requirement-analysis 2>/dev/null || true
rmdir generated/metadata/stepback-analysis 2>/dev/null || true
rmdir generated/metadata/task-decomposition 2>/dev/null || true

# 古いスクリプト削除
rm -rf generated/news_video_scripts/

echo "✅ 削除完了（テストワークフロー、廃止プロンプト、空ディレクトリ、古いスクリプト）"
```

---

**削除対象**: テストワークフロー8個 + 廃止プロンプト5個 + 空ディレクトリ4個 + 古いスクリプト1個 = **18ファイル/ディレクトリ**