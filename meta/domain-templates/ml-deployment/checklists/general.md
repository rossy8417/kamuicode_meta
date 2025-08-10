# ML Deployment Checklist (MUST/SHOULD)

## MUST
- All outputs under `${PROJECT_DIR}`
- Use artifacts between jobs
- No local path in `uses:`
- Model and manifests saved to `${PROJECT_DIR}/models/` and `${PROJECT_DIR}/final/`

## SHOULD
- Build image under `${PROJECT_DIR}/build/`
