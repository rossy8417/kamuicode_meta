# Web Development Checklist (MUST/SHOULD)

## MUST
- All outputs under `${PROJECT_DIR}`
- Use `actions/upload-artifact` / `actions/download-artifact` for sharing
- No local path in `uses:`
- Build artifacts under `${PROJECT_DIR}/build/` and test reports under `${PROJECT_DIR}/reports/`

## SHOULD
- Cache dependencies where possible
- Include environment metadata under `${PROJECT_DIR}/metadata/`
