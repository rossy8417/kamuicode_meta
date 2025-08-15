# News Video Checklist (MUST/SHOULD)

## MUST
- **CRITICAL: T2I→I2V Serial Execution**: Each scene MUST execute T2I and I2V in the SAME job
  - This prevents Google Cloud Storage URL expiration (15 minutes limit)
  - Structure: matrix.scene → each job does: T2I → save → I2V → save
  - NEVER split T2I and I2V into separate job phases
- **Workflow Start Time**: Setup job MUST record workflow start time
  - Use: echo "workflow_start=$(date -Iseconds)" >> $GITHUB_OUTPUT
  - NOT github.run_started_at (may be empty or cause parsing errors)
- **I2V Error Handling**: Implement graceful fallback for I2V failures
  - If I2V fails, continue workflow (don't fail entire job)
  - Log as warning: echo "::warning::I2V failed for scene X, using image only"
  - Upload available assets even if video generation fails
- **T2I Error Recovery**: Add retry logic for image generation failures
  - Check image file size: must be > 10KB for valid generation
  - If T2I fails (file < 10KB), retry once with different seed
  - Add explicit error checking after Claude Code SDK execution
  - Consider staggering parallel executions to avoid API rate limits
- **Separated Anchor System**: キャスターと背景を完全分離した本格的ニュース映像
  - Background scenes: キャスター無しの背景のみ生成（ニューススタジオ、現場映像、資料映像等）
  - Anchor generation: 1人のみ、透過背景またはグリーンスクリーン背景で生成（seed: 42固定）
  - Professional appearance: ビジネススーツ、正面向き、信頼感のある表情
  - Japanese language: 日本語ナレーション優先、プロンプトも日本語対応

- **Lip-sync Pipeline**: 5秒セグメント単位のリップシンク処理
  1. ナレーション音声を5秒セグメントに分割（FFmpeg使用）
  2. 各セグメントでキャスターのリップシンク動画生成（mcp__v2v-kamui-pixverse-lipsync）
  3. FFmpegで背景動画とキャスター動画を合成（overlay filter使用）
  4. Position: 画面右下1/3サイズ、または全画面中央配置
  
- **Composition Structure**: レイヤー構造での映像合成
  - Layer 1 (底層): 背景動画（ニューススタジオ、現場映像等）
  - Layer 2 (中層): キャスターリップシンク動画（位置固定）
  - Layer 3 (上層): テロップ、字幕、ニューステロップ等
- **Scene Calculation for News**: 動的シーン計算（5秒/シーン）
  - Formula: `SCENE_COUNT = ceil(duration / 5)`
  - 30秒 = 6シーン、60秒 = 12シーン、90秒 = 18シーン
  - Each scene = 5秒の背景動画 + 5秒のリップシンクセグメント
- Use professional presenter style with stable identity (no face change).
- Keep 1920x1080 resolution and 30fps for all clips.
- Maintain audio loudness around -14 LUFS.
- Include clear Hook -> Main -> CTA structure within target duration.
- Save files under `${PROJECT_DIR}` and share between jobs via artifacts.

## SHOULD
- Blue-leaning palette for credibility unless brand overrides.
- Smooth transitions; avoid excessive motion for news tone.
- Keep per-scene descriptive metadata (for QA).
