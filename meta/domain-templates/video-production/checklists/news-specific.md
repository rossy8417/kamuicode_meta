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
- **News Anchor Generation**: Create ONE consistent news anchor/presenter who appears throughout the entire video
  - Use fixed seed value (e.g., seed: 42) for character consistency
  - Generate anchor once, then create multiple lip-sync videos for each scene
  - Anchor should be professional (business attire, neutral expression, credible appearance)
- **Scene Calculation for News**: Use fixed 5-second per scene (60s = 12 scenes, 30s = 6 scenes)
- Use professional presenter style with stable identity (no face change).
- Keep 1920x1080 resolution and 30fps for all clips.
- Maintain audio loudness around -14 LUFS.
- Include clear Hook -> Main -> CTA structure within target duration.
- Save files under `${PROJECT_DIR}` and share between jobs via artifacts.

## SHOULD
- Blue-leaning palette for credibility unless brand overrides.
- Smooth transitions; avoid excessive motion for news tone.
- Keep per-scene descriptive metadata (for QA).
