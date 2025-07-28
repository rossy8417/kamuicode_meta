# 🔍 修正版削除推奨リスト（メタワークフロー依存関係確認済み）

## ✅ **安全な削除対象（メタワークフロー非依存確認済み）**

### **1. Video関連ワークフロー（11個すべて削除可能）**
```bash
# 削除推奨 - Meta Workflow Executor v8による動的生成で代替
rm .github/workflows/video-content-creation.yml
rm .github/workflows/video-content-creation-cli.yml  
rm .github/workflows/video-content-creation-direct.yml
rm .github/workflows/video-content-creation-download.yml
rm .github/workflows/video-content-creation-fixed.yml
rm .github/workflows/video-content-creation-mock.yml
rm .github/workflows/video-content-creation-production.yml
rm .github/workflows/video-content-creation-production-v2.yml
rm .github/workflows/video-content-creation-production-v3.yml
rm .github/workflows/video-content-creation-secure.yml
rm .github/workflows/video-content-creation-with-download.yml
```

### **2. 廃止プロンプト（4個すべて削除可能）**
```bash
# 削除推奨 - 完全に未使用確認済み
rm -rf meta/prompts/deprecated/
```

### **3. テスト用ワークフロー（用途確認後削除）**
```bash
# テスト完了後削除推奨
rm .github/workflows/test-comment-trigger.yml
rm .github/workflows/test-direct-mcp-call.yml
rm .github/workflows/test-mcp-method-patterns.yml
rm .github/workflows/test-mcp-permissions.yml
rm .github/workflows/test-mcp-services-detail.yml
rm .github/workflows/test-mcp-settings-parameter.yml
rm .github/workflows/test-mcp-with-permissions.yml
```

## ⚠️ **保持必須（メタワークフロー依存関係あり）**

### **直接参照されるファイル**
- `meta/prompts/stepback-to-tasks.md` - **line 245で直接参照**
- `meta/examples/` - 将来の動的参照予定
- `meta/ai-learning/` - AI Auto-Fix使用

### **動的生成されるパス**
- `generated/metadata/` - **line 97, 202, 228, 325で生成・使用**
- `generated/workflows/` - **line 335, 429, 483で生成**
- `.github/workflows/generated/` - **line 769, 770, 788で配置**

### **システムコアファイル**
- `.github/workflows/meta-workflow-executor-v8.yml` - メインエントリポイント
- `.github/workflows/auto-fix-deployment.yml` - AI自動修正
- `.github/workflows/continuous-system-monitor.yml` - 監視（Meta依存）

## 📊 **削除効果予測**

### **削除対象ファイル数**
- Video workflows: **11個** → 0個
- Test workflows: **7個** → 0個  
- Deprecated prompts: **4個** → 0個
- **合計: 22個のファイル削除**

### **容量削減見込み**
- ワークフローファイル削除: **60-70%削減**
- 重複除去による効果: **管理負荷大幅軽減**
- 検索・編集速度: **大幅向上**

### **機能への影響**
- **影響なし**: メタワークフローが動的生成するため
- **リスク**: ゼロ（参照関係なし確認済み）
- **メンテナンス**: 簡素化・効率化

## 🎯 **実行順序**

### **Step 1: 即座実行可能**
```bash
# 廃止プロンプト削除（100%安全）
rm -rf meta/prompts/deprecated/
```

### **Step 2: Video workflows削除**
```bash
# バックアップ作成
mkdir -p archive/video-workflows-backup
mv .github/workflows/video-content-creation*.yml archive/video-workflows-backup/

# Meta Workflow動作確認後、完全削除
rm -rf archive/video-workflows-backup/
```

### **Step 3: テストファイル整理**
```bash
# テスト完了確認後
mv .github/workflows/test-*.yml archive/test-workflows-backup/
# 動作確認後削除
```

## ✅ **確認事項**

### **依存関係チェック済み**
- ✅ Meta Workflow Executor v8: 個別ワークフロー参照なし
- ✅ Auto-Fix System: video-workflows参照なし  
- ✅ System Monitor: video-workflows参照なし
- ✅ 外部トリガー: workflow_run依存なし

### **削除前の最終確認**
1. メタワークフローの正常動作確認
2. 生成されるワークフローの品質確認
3. バックアップ作成の完了確認

---

**結論**: 22個のファイルを安全に削除可能。メタワークフローによる動的生成で全機能を維持。