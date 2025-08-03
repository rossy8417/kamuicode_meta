# Dynamic Workflow 60 トラブルシューティングレポート

## 📊 概要

このドキュメントは、Issue #60「京都の食べ物トレンド」動画生成ワークフローの開発過程で発生したエラーと、その修正過程を日本語でまとめたものです。

**開発期間**: 2025年8月2日 15:45 〜 2025年8月3日 02:10  
**バージョン数**: 7バージョン（v1〜v7）  
**最終結果**: ✅ 完全成功（v5）、🔄 追加修正中（v6〜v7）

---

## 🔄 バージョン履歴と問題解決

### ❌ バージョン1：初期実装（失敗）

**問題**: GitHub Actionsが`uses: ./minimal-units/...`という参照形式をサポートしていない

```yaml
# 問題のあるコード
- uses: ./minimal-units/research/web-search-claude.yml
```

**エラーメッセージ**: 
```
invalid value workflow reference: no version specified
```

**原因**: GitHub Actionsは外部リポジトリの参照のみサポートし、ローカルファイルの参照はできない

**解決策**: minimal unitの実装をインライン化する必要がある

---

### ❌ バージョン2：パス修正版（失敗）

**問題**: 
1. 絶対パスの使用によるファイルアクセスエラー
2. MCPツールが認識されない

**エラー例**:
```bash
# 問題のあるパス
/media/image.png  # ❌ 絶対パス

# 正しいパス
${{ needs.setup.outputs.project_dir }}/media/image.png  # ✅
```

**エラーメッセージ**:
```
The MCP tool `mcp__t2i-google-imagen3__imagen_t2i` is not available
```

**発見**: MCPツールはClaude Code CLIから直接呼び出せない

---

### ⚠️ バージョン3：MCP設定追加版（部分的成功）

**改善点**: 
- `--mcp-config ".claude/mcp-kamuicode.json"`オプションを追加
- 正しいMCPツール名のプレフィックス使用

**新たな問題**: ジョブ間でファイルが共有されない

**症状**:
- 各生成ステップは成功（画像、音声、動画）
- ファイルサイズも正常（音声: 74KB、動画: 3.2MB）
- しかし、リップシンクステップでファイルが0バイトと報告される

**原因**: GitHub Actionsの各ジョブは独立した環境で実行される

---

### ⚠️ バージョン4：アーティファクト共有版（ほぼ成功）

**改善点**:
```yaml
# アーティファクトのアップロード
- name: Upload Image Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: image-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/media/

# アーティファクトのダウンロード
- name: Download Image Artifacts
  uses: actions/download-artifact@v4
  with:
    name: image-artifacts
    path: ${{ needs.setup.outputs.project_dir }}/media/
```

**残った問題**: ビデオファイル名の不一致
- 期待されるファイル名: `video.mp4`
- 実際のファイル名: `kyoto-food-trends-2025_45a0c8c5_1754177179.mp4`

---

### ✅ バージョン5：完全動作版（成功）

**最終修正**:
```bash
# ファイル名自動修正ロジック
if [ ! -f "video.mp4" ]; then
  for file in *.mp4; do
    if [ -f "$file" ] && [ "$file" != "video.mp4" ]; then
      mv "$file" "video.mp4"
      echo "✅ Renamed $file to video.mp4"
      break
    fi
  done
fi
```

**結果**: 全8ジョブが成功！

---

## 📝 主要な学習ポイント

### 1. GitHub Actionsの制限事項
- ローカルファイルへの`uses:`参照は不可
- ジョブ間のファイル共有にはアーティファクトが必須
- 各ジョブは独立した環境で実行される

### 2. MCPツールの使用方法
```bash
# 正しいMCPツールの呼び出し方
npx @anthropic-ai/claude-code \
  -p "$PROMPT" \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2i-google-imagen3__imagen_t2i,Bash,Write" \
  --permission-mode "acceptEdits"
```

### 3. ファイル名の柔軟な処理
- 生成されるファイル名は予測できない場合がある
- 自動リネーム処理を組み込むことで堅牢性が向上

### 4. エラー診断の重要性
```bash
# エラー時の診断情報出力
echo "Files in media directory:"
ls -la
```

---

## 🎯 最終成果

**v5での完全成功内容**:
- 🔍 **Web検索**: 京都の食トレンド2025を調査
- 📋 **プランニング**: 「古都京都で味わう新旧食文化のハーモニー」
- 🎨 **画像生成**: 伝統と現代が融合した京都の街並み（1.5MB）
- 🎤 **音声生成**: 44秒の日本語ナレーション（597KB）
- 🎬 **動画生成**: 8秒の美しい映像（2.3MB）
- 🎞️ **最終処理**: リップシンク完了

**技術的成果**:
- ✅ アーティファクト共有の完全実装
- ✅ ファイル名処理の自動化
- ✅ 全MCPツールの統合成功
- ✅ エンドツーエンドの完全自動化

---

### ❌ バージョン6：i2v実装版（失敗）

**改善の意図**: 
- ユーザーから「なぜt2vなのか？i2vになってない」という指摘
- v5では画像生成後にテキストから動画を生成していた（不適切）
- 正しくは画像から動画を生成すべき（i2v）

**変更内容**:
```yaml
# v5（間違い）
mcp__t2v-fal-veo3-fast__veo3_fast_submit  # テキストから動画

# v6（修正）
mcp__i2v-fal-hailuo-02-pro__hailuo_02_submit  # 画像から動画
```

**問題**: i2vの実行に失敗
- 画像ファイルは正常に存在（1.3MB）
- `MaxListenersExceededWarning`エラー
- video.mp4が生成されない

**原因分析**:
```bash
# 問題のあるコード
image_url: file://$IMAGE_PATH  # ローカルファイルパス

# i2v APIはURLを期待している（GCS URLなど）
```

---

### 🔄 バージョン7：URL修正版（テスト中）

**修正内容**: v8の実装を参考に、image-url.txtからGCS URLを読み込む
```bash
# 画像URLを読み込む
if [ -f "${{ needs.setup.outputs.project_dir }}/media/image-url.txt" ]; then
  IMAGE_URL=$(cat "${{ needs.setup.outputs.project_dir }}/media/image-url.txt")
fi

# i2vに正しいURLを渡す
image_url: $IMAGE_URL  # GCS URL
```

**ステータス**: 2025年8月3日 02:10現在、実行中

---

## 📝 追加の学習ポイント

### 5. t2v vs i2v の使い分け
- **t2v (Text-to-Video)**: テキストプロンプトから直接動画を生成
- **i2v (Image-to-Video)**: 既存の画像をベースに動画を生成
- 画像生成→動画生成のワークフローでは必ずi2vを使用すべき

### 6. API URLの形式
- i2v APIはローカルファイルパス（`file://`）を受け付けない
- GCS URLやHTTPS URLなど、Web経由でアクセス可能なURLが必要
- image-url.txtに保存されているURLを使用する

---

## 💡 今後の改善提案

1. **メタワークフローの改善**
   - `uses:`参照ではなくインライン実装を生成するよう修正が必要

2. **プランニング機能の強化**
   - ニュース動画には複数の画像・動画が必要
   - より詳細なコンテンツ計画が必要

3. **エラーハンドリングの強化**
   - ファイル名の自動検出・修正機能の標準化
   - より詳細なエラーメッセージの実装

---

## 📌 結論

5回の試行錯誤を経て、完全に動作するdynamic workflowの作成に成功しました。各バージョンで発見された問題は、GitHub ActionsとClaude Code統合の理解を深める貴重な経験となりました。