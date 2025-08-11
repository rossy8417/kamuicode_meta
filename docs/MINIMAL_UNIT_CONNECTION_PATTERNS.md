# ミニマルユニット間接続パターンガイド

## 概要

このドキュメントは、ミニマルユニット間でデータを確実に受け渡すための実装パターンを定義します。
特に、Claude Code SDKを使用した生成系タスクにおけるファイル保存とデータ共有の問題を解決します。

## 🔴 主要な問題と解決策

### 問題：Claude Code SDKの出力が保存されない

**症状**：
- MCPツールは実行されるが、ローカルファイルが保存されない
- `find`コマンドでファイルが見つからない
- すべてプレースホルダーファイルになる

**根本原因**：
- Claude Codeへの保存指示が曖昧
- ファイル保存の確認処理が不足
- URLファイルのダウンロード処理が欠落

## 📋 T2I → I2V データ共有パターン

### 必須実装要素

#### 1. 画像生成（T2I）後の処理

```bash
# ===== STEP 1: Claude Code実行 =====
# 明示的な保存パスとURLファイル作成を指示
SAVE_PATH="${PROJECT_DIR}/media/images/scene${SCENE_NUM}.png"
URL_PATH="${PROJECT_DIR}/media/images/scene${SCENE_NUM}-url.txt"

GENERATION_PROMPT="以下の手順で画像を生成してください：
1. MCPツール mcp__t2i-kamui-imagen3__imagen_t2i で画像生成
2. Writeツールで生成画像を ${SAVE_PATH} に保存
3. Google Cloud Storage URLを ${URL_PATH} に保存
4. Bashツールで ls -la ${PROJECT_DIR}/media/images/ を実行して確認
重要：すべてのステップを必ず実行してください"

npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2i-*,Write,Bash" \
  --max-turns 40 \
  --permission-mode "bypassPermissions" \
  -p "$GENERATION_PROMPT"

# ===== STEP 2: 即座の確認とダウンロード =====
echo "=== ファイル生成確認 ==="
ls -la "${PROJECT_DIR}/media/images/" 2>/dev/null || echo "ディレクトリが存在しません"

# URLファイルがあれば即座にダウンロード
for url_file in "${PROJECT_DIR}"/media/images/*url*.txt; do
  if [ -f "$url_file" ]; then
    URL=$(cat "$url_file")
    IMAGE_FILE="${url_file%-url.txt}.png"
    echo "📥 Downloading from: $URL"
    curl -L -o "$IMAGE_FILE" "$URL" || echo "⚠️ Download failed"
  fi
done

# ===== STEP 3: 多段階ファイル検索 =====
# パターン1: 特定のファイル名
IMAGE=$(find "$PROJECT_DIR" -type f -name "*scene*${SCENE_NUM}*.png" 2>/dev/null | head -1)

# パターン2: 2分以内に作成されたファイル
if [ -z "$IMAGE" ]; then
  IMAGE=$(find "$PROJECT_DIR" -type f -name "*.png" -mmin -2 2>/dev/null | head -1)
fi

# パターン3: 任意のPNGファイル
if [ -z "$IMAGE" ]; then
  IMAGE=$(find "$PROJECT_DIR" -type f -name "*.png" 2>/dev/null | head -1)
fi

# ===== STEP 4: プレースホルダー作成（最終手段） =====
if [ -z "$IMAGE" ]; then
  echo "⚠️ WARNING: 画像ファイルが見つかりません。プレースホルダーを作成します"
  IMAGE="${PROJECT_DIR}/media/images/scene${SCENE_NUM}.png"
  mkdir -p "$(dirname "$IMAGE")"
  echo "Placeholder scene ${SCENE_NUM} image" > "$IMAGE"
else
  echo "✅ 画像ファイル発見: $IMAGE"
fi
```

#### 2. 動画変換（I2V）での受け取り

```bash
# ===== URLとローカルパスの両方に対応 =====
URL_FILE="${PROJECT_DIR}/media/images/scene${SCENE_NUM}-url.txt"
LOCAL_IMAGE="${PROJECT_DIR}/media/images/scene${SCENE_NUM}.png"

# URLファイルが存在し、有効な場合は優先使用
if [ -f "$URL_FILE" ]; then
  IMAGE_URL=$(cat "$URL_FILE")
  
  # URLの有効性確認（5秒タイムアウト）
  if curl -IfsS --max-time 5 "$IMAGE_URL" >/dev/null 2>&1; then
    IMAGE_REF="$IMAGE_URL"
    echo "✅ Using Google Cloud Storage URL: $IMAGE_URL"
  else
    IMAGE_REF="$LOCAL_IMAGE"
    echo "⚠️ URL expired or invalid, using local path: $LOCAL_IMAGE"
  fi
else
  IMAGE_REF="$LOCAL_IMAGE"
  echo "ℹ️ No URL file found, using local path: $LOCAL_IMAGE"
fi

# I2V変換実行
I2V_PROMPT="以下の画像を動画に変換してください：
入力画像: ${IMAGE_REF}
出力先: ${PROJECT_DIR}/media/videos/scene${SCENE_NUM}.mp4
要件: 6-8秒の動画、スムーズな動き"

npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__i2v-*,Write,Bash" \
  --max-turns 80 \
  --permission-mode "bypassPermissions" \
  -p "$I2V_PROMPT"
```

## 🔄 その他の接続パターン

### T2S（テキスト→音声）パターン

```bash
# 音声生成
AUDIO_PATH="${PROJECT_DIR}/media/audio/narration.mp3"
TTS_PROMPT="テキストを音声に変換：
テキスト: '${NARRATION_TEXT}'
出力: ${AUDIO_PATH}
音声設定: 日本語、女性、ニュースキャスター風"

npx @anthropic-ai/claude-code \
  --allowedTools "mcp__t2s-*,Write,Bash" \
  -p "$TTS_PROMPT"

# 確認
ls -la "${PROJECT_DIR}/media/audio/"
```

### 並列処理での共有（Artifacts使用）

```yaml
# ジョブ1: 生成
- name: Upload Generated Files
  uses: actions/upload-artifact@v4
  with:
    name: scene-images
    path: ${{ env.PROJECT_DIR }}/media/images/

# ジョブ2: 利用
- name: Download Generated Files
  uses: actions/download-artifact@v4
  with:
    name: scene-images
    path: ${{ env.PROJECT_DIR }}/media/images/
```

## ✅ チェックリスト

### Claude Code実行時
- [ ] 明示的な保存パス指定（`${PROJECT_DIR}/media/...`）
- [ ] URLファイル作成指示（`*-url.txt`）
- [ ] 保存確認コマンド（`ls -la`）
- [ ] Writeツールの許可（`--allowedTools`に含める）

### ファイル取得時
- [ ] 即座のURLダウンロード（`curl -L -o`）
- [ ] 多段階検索（最低3パターン）
- [ ] URL有効性確認（`curl -IfsS`）
- [ ] フォールバック処理

### デバッグ時
- [ ] 各ステップでのログ出力
- [ ] ファイル存在確認
- [ ] エラーハンドリング

## 🚨 よくある失敗パターンと対策

### ❌ 失敗パターン1: 曖昧な保存指示
```bash
# 問題のあるコード
npx @anthropic-ai/claude-code -p "画像を生成してください"
```

### ✅ 解決策
```bash
# 明示的な指示
npx @anthropic-ai/claude-code -p "画像生成→${PATH}に保存→確認"
```

### ❌ 失敗パターン2: ファイル検索が単一パターン
```bash
# 問題のあるコード
IMAGE=$(find . -name "image.png")
```

### ✅ 解決策
```bash
# 多段階検索
IMAGE=$(find "$DIR" -name "*scene*.png" | head -1)
[ -z "$IMAGE" ] && IMAGE=$(find "$DIR" -name "*.png" -mmin -2 | head -1)
[ -z "$IMAGE" ] && IMAGE=$(find "$DIR" -name "*.png" | head -1)
```

### ❌ 失敗パターン3: URL期限切れ未対応
```bash
# 問題のあるコード
IMAGE_URL=$(cat url.txt)
# 直接使用（期限切れの可能性）
```

### ✅ 解決策
```bash
# 有効性確認とフォールバック
if curl -IfsS "$IMAGE_URL" >/dev/null 2>&1; then
  use_url
else
  use_local_file
fi
```

## 📚 関連ドキュメント

- [MINIMAL_UNIT_DATA_DEPENDENCIES.md](./MINIMAL_UNIT_DATA_DEPENDENCIES.md) - データ依存関係の仕様
- [YAML_CONSTRUCTION_GUIDELINES.md](./YAML_CONSTRUCTION_GUIDELINES.md) - YAML構築のベストプラクティス
- [meta/domain-templates/video-production/constraints.yaml](../meta/domain-templates/video-production/constraints.yaml) - 動画制作の制約条件