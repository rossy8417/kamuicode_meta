# News Video Checklist (MUST/SHOULD)

## MUST
- Use professional presenter style with stable identity (no face change).
- Keep 1920x1080 resolution and 30fps for all clips.
- Maintain audio loudness around -14 LUFS.
- Include clear Hook -> Main -> CTA structure within target duration.
- If i2v clip length is limited (5–8s), ensure enough scenes: ceil(duration_sec / per_scene_sec).
- Save files under `${PROJECT_DIR}` and share between jobs via artifacts.

## SHOULD
- Blue-leaning palette for credibility unless brand overrides.
- Smooth transitions; avoid excessive motion for news tone.
- Keep per-scene descriptive metadata (for QA).
