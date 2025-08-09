# 厳格検証要件リスト (Strict Validation Requirements)

## 🚨 CRITICAL REQUIREMENTS (必須・1つでも失敗したら即FAIL)

### CR001: Max Turns for I2V Processing
- **検証対象**: `i2v` または `image.*to.*video` を含む処理
- **必須値**: `--max-turns 80` 以上
- **エラー時**: "❌ CRITICAL: I2V処理のmax-turnsが80未満 (検出値: XX)"

### CR002: MCP Configuration
- **検証対象**: 全ての `npx @anthropic-ai/claude-code` 呼び出し
- **必須文字列**: `--mcp-config ".claude/mcp-kamuicode.json"`
- **エラー時**: "❌ CRITICAL: MCP設定ファイル指定が欠落"

### CR003: File Size Validation (300KB+)
```bash
# 必須パターン例
if [ -f "$video_file" ] && [ -s "$video_file" ]; then
  file_size=$(stat -c%s "$video_file" 2>/dev/null || stat -f%z "$video_file" 2>/dev/null || echo 0)
  if [ "$file_size" -lt 300000 ]; then
    echo "❌ Video file too small: ${file_size} bytes"
    exit 1
  fi
fi
```
- **エラー時**: "❌ CRITICAL: 300KB以上のファイルサイズ検証が未実装"

### CR004: Serial-Parallel Pipeline Structure
- **必須構造**: 
  1. Phase 1: 情報収集・スクリプト作成（直列）
  2. Phase 2: 並列生成（presenter, narration, visuals, graphics）
  3. Phase 3A: 画像→動画変換（URL期限対策・即座実行）
  4. Phase 3B以降: 統合処理
- **エラー時**: "❌ CRITICAL: 直列並列パイプライン構造が不正"

### CR005: URL Expiration Mitigation
- **必須キーワード**: `just-in-time`, `rolling`, `immediate`, `URL期限`
- **最小出現回数**: 3箇所
- **エラー時**: "❌ CRITICAL: URL期限切れ対策の記述が不足"

### CR006: Progressive Reporting with if:always()
```yaml
# 必須パターン
- name: Report Progress
  if: always()
  run: echo "Status report" >> $GITHUB_STEP_SUMMARY
```
- **最小実装数**: 5箇所
- **エラー時**: "❌ CRITICAL: プログレッシブレポート実装が不足"

### CR007: Google URL vs Local Path Priority
```bash
# 必須パターン
if [ -n "$google_url" ] && curl -IfsS --max-time 10 "$google_url" >/dev/null 2>&1; then
  VIDEO_URL="$google_url"
  echo "Using Google Cloud URL"
else
  VIDEO_URL="file://${local_path}"
  echo "Fallback to local path"
fi
```
- **エラー時**: "❌ CRITICAL: Google URL優先処理が未実装"

### CR008: Retry Logic Implementation
```bash
# 必須パターン
for attempt in {1..3}; do
  if command_to_retry; then
    break
  fi
  echo "Retry $attempt/3..."
  sleep $((attempt * 5))
done
```
- **最小実装数**: 3箇所（主要処理）
- **エラー時**: "❌ CRITICAL: リトライロジックが不足"

### CR009: Error Exit Codes
- **必須**: エラー時に `exit 1` または `return 1`
- **検証箇所**: ファイル検証失敗、API呼び出し失敗、タイムアウト
- **エラー時**: "❌ CRITICAL: エラー終了コードが未設定"

### CR010: Artifact Management
- **必須**: 全てのジョブ間データ共有は `upload-artifact` → `download-artifact`
- **禁止**: GitHub Outputsでの大容量データ共有
- **エラー時**: "❌ CRITICAL: アーティファクト管理が不適切"

## ⚠️ DOMAIN SPECIFIC - Video Production (80%以上必須)

### DSV001: Video Duration (6-8 seconds)
- **検証文字列**: `duration: "6s"`, `duration: "8s"`, `6-8 seconds`

### DSV002: Resolution (1920x1080)
- **検証文字列**: `1920x1080`, `1080p`, `Full HD`
- **最小出現**: 5箇所

### DSV003: Frame Rate (30fps)
- **検証文字列**: `30fps`, `30 fps`, `frame_rate: 30`

### DSV004: Broadcast Audio Standard (-14 LUFS)
- **検証文字列**: `-14 LUFS`, `broadcast standard`, `放送品質`

### DSV005: Parallel Processing Groups (3+ concurrent)
- **検証**: 同じ `needs:` 依存関係を持つジョブが3つ以上

## 📊 採点基準

```
総合判定 = {
  if (CRITICAL失敗 > 0) return "❌ FAILED - Critical要件違反"
  if (DOMAIN得点 < 80%) return "❌ FAILED - Domain要件不足"
  if (CRITICAL全合格 && DOMAIN >= 80%) return "✅ PASSED"
}
```

## 🔧 自動修正トリガー

| 検出パターン | 自動修正アクション |
|------------|-----------------|
| max-turns < 80 | 値を80に置換 |
| ファイルサイズ検証なし | 検証関数を挿入 |
| if:always()なし | プログレッシブレポート追加 |
| リトライなし | retry wrapperで囲む |

## 📝 検証結果フォーマット

```markdown
# ワークフロー検証結果

## Critical Requirements (必須)
- [✅/❌] CR001: Max Turns for I2V = 80 (検出値: XX)
- [✅/❌] CR002: MCP Configuration = 全箇所OK
- [✅/❌] CR003: File Size Validation = 実装済み
...

## Domain Specific (Video)
- [✅/❌] DSV001: Video Duration = 6-8秒指定あり
- [✅/❌] DSV002: Resolution = 1920x1080指定 (5箇所)
...

## 総合判定
**[✅ PASSED / ❌ FAILED]**
- Critical: 10/10 (100%)
- Domain: 4/5 (80%)
- 総合スコア: 90%

## 要修正項目
1. [CR001] Max Turnsを40→80に修正必要
2. [DSV002] 解像度指定を追加（現在3箇所→5箇所必要）
```