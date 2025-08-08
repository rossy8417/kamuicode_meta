# メディア生成の安定性とリトライ戦略

## 📊 **重要な発見**

### ✅ **安定している処理**
- **テキスト生成**: 高い成功率、リトライ不要
  - 脚本作成、ニュース記事生成、プロンプト最適化
  - Claude Code SDK、OpenAI GPT、その他LLMベース処理

### ❌ **不安定な処理（リトライ必須）**
- **画像生成**: API一時エラー頻発
  - Google Imagen3: `"Could not process image"` エラー
  - Flux, DALL-E系も同様の傾向
- **動画生成**: MCP接続とAPI安定性問題
  - Hailuo-02 Pro, Veo3 Fast, その他I2V/T2Vサービス
- **音声生成**: ナレーション・TTS・BGM生成
  - MiniMax Speech, ElevenLabs, Google TTS
- **3D生成**: HunyuanD等の3Dモデル生成

## 🔧 **必須実装パターン**

### **リトライ戦略**
```yaml
# 3-attempt retry logic for all media generation
MEDIA_SUCCESS=false
for attempt in 1 2 3; do
  echo "[$(date)] Media generation attempt $attempt of 3"
  
  if npx @anthropic-ai/claude-code \
    --mcp-config ".claude/mcp-kamuicode.json" \
    --allowedTools "mcp__service__function" \
    -p "$PROMPT"; then
    
    # Check if media was actually generated
    MEDIA_CHECK=$(find "${OUTPUT_DIR}" -name "*.ext" | head -1)
    if [ -n "$MEDIA_CHECK" ] && [ -f "$MEDIA_CHECK" ]; then
      echo "[$(date)] Media SUCCESS on attempt $attempt"
      MEDIA_SUCCESS=true
      break
    else
      echo "[$(date)] Media generation completed but no file found on attempt $attempt"
    fi
  else
    echo "[$(date)] Media FAILED on attempt $attempt"
  fi
  
  if [ $attempt -lt 3 ]; then
    echo "[$(date)] Retrying in 5 seconds..."
    sleep 5
  fi
done

if [ "$MEDIA_SUCCESS" != "true" ]; then
  echo "[$(date)] All 3 attempts failed, using fallback"
  # Implement fallback logic here
fi
```

### **エラーハンドリング**
1. **実行レベル**: コマンド成功/失敗の判定
2. **ファイルレベル**: 実際にファイルが生成されたかの確認
3. **サイズレベル**: 生成ファイルが空でないかの確認（音声・動画）
4. **フォールバック**: 全失敗時の代替手段

## 📋 **実装済みリトライ機能**

### ✅ **現在実装済み**
- **Video Generation (Phase 4)**: 3回リトライ
  - Hailuo-02 Pro を使用したI2V変換
  - ファイル存在確認とサイズ確認
- **BGM Generation**: 3回リトライ
  - Google Lyria使用
  - 音声レベル確認
- **Video Concatenation**: 3回リトライ
  - FFmpeg統合処理
- **Audio Generation (Phase 3A)**: 3回リトライ（新規追加）
  - MiniMax Speech-02-Turbo使用
  - ファイルサイズ確認
- **Image Generation (Phase 3B)**: 3回リトライ（新規追加）
  - Google Imagen3使用
  - 拡張子柔軟対応

### 🔄 **今後実装予定**
- **Opening Creation (Phase 6)**: リトライ未実装
- **3D Model Generation**: リトライ未実装
- **Video Analysis**: 基本的に安定、要監視

## 🎯 **ベストプラクティス**

### **1. MCP接続時間管理**
```yaml
# GitHub Actions doesn't provide run_started_at, track from job start
JOB_START_TIME=$(date +%s)
ELAPSED_MINUTES=$(( ($(date +%s) - JOB_START_TIME) / 60 ))

if [ $ELAPSED_MINUTES -lt 12 ]; then
  # Safe to use MCP tools
else
  # Switch to fallback methods
fi
```

### **2. ログ詳細化**
```yaml
# Detailed logging for debugging
npx @anthropic-ai/claude-code \
  -p "$PROMPT" 2>&1 | tee -a "${PROJECT_DIR}/logs/media-generation-mcp.log"
```

### **3. フォールバック戦略**
- **画像**: Placeholder生成またはテキスト画像
- **動画**: 静止画ズーム効果またはテストパターン  
- **音声**: espeak-ng等のローカルTTS

## 📈 **品質向上効果**

### **リトライ実装前**
- Image 4失敗: 1回のAPI エラーで完全停止
- Video 4失敗: 80%成功率（MCP接続不安定）
- 全体完了率: ~70%

### **リトライ実装後（予想）**
- 画像生成: 95%+ 成功率
- 動画生成: 90%+ 成功率  
- 全体完了率: 85%+ 

### **システム信頼性**
- ワークフロー中断率: 大幅減少
- デバッグ時間: 短縮（詳細ログ）
- ユーザー体験: 向上（自動回復）

## 🚨 **重要な注意事項**

1. **テキスト生成にはリトライ不要**: オーバーヘッドを避ける
2. **メディア生成には必須**: API安定性問題のため
3. **MCP接続時間制限**: 15-20分後自動切断
4. **並列実行時の配慮**: 同時リクエスト数制限
5. **コスト管理**: リトライによる使用量増加に注意

---

**作成日**: 2025-08-08  
**最終更新**: 2025-08-08  
**ベース情報**: Generated News Video Workflow テスト結果  
**検証環境**: GitHub Actions + MCP kamui-code.ai