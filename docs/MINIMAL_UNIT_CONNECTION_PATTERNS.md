# Minimal Unit Connection Pattern Guide

## Overview
This document defines data passing patterns between minimal units and solutions to common issues.

## 🔴 Major Issues and Solutions

### Issue: Claude Code SDK Output Not Saved

**Cause**: Claude Code SDK executes MCP tools but doesn't save files locally without explicit instructions.

**Solution**:
```bash
# MUST: Include explicit save path in prompt
SAVE_PATH="${PROJECT_DIR}/media/images/scene1.png"
URL_PATH="${PROJECT_DIR}/media/images/scene1-url.txt"

PROMPT="Execute in order:
1. Generate image with mcp__t2i-kamui-imagen3__imagen_t2i
2. Save to ${SAVE_PATH} using Write tool
3. Save URL to ${URL_PATH} using Write tool
4. Verify with ls -la"

npx @anthropic-ai/claude-code \
  --allowedTools "mcp__t2i-*,Write,Bash" \
  -p "$PROMPT"
```

---

## 📊 Data Flow Patterns

### 1. T2I (Text-to-Image) → I2V (Image-to-Video)

#### T2I Output
```yaml
outputs:
  local_file: ${PROJECT_DIR}/media/images/scene1.png
  url_file: ${PROJECT_DIR}/media/images/scene1-url.txt
  gcs_url: https://storage.googleapis.com/...
```

#### I2V Input
```yaml
inputs:
  priority_1: gcs_url (if valid within 15 minutes)
  priority_2: local_file (as fallback)
```

#### Connection Implementation
```bash
# I2V reads T2I output
URL_FILE="${PROJECT_DIR}/media/images/scene1-url.txt"
LOCAL_FILE="${PROJECT_DIR}/media/images/scene1.png"

# Prioritize valid URL
if [ -f "$URL_FILE" ]; then
  URL=$(cat "$URL_FILE")
  if curl -IfsS --max-time 5 "$URL" >/dev/null 2>&1; then
    INPUT_IMAGE="$URL"
  else
    INPUT_IMAGE="$LOCAL_FILE"
  fi
else
  INPUT_IMAGE="$LOCAL_FILE"
fi
```

---

## 🔧 Multi-Pattern File Search

### Implementation (MANDATORY)
```bash
# Pattern 1: Specific filename
FILE=$(find "$PROJECT_DIR" -name "*scene1*.png" 2>/dev/null | head -1)

# Pattern 2: Recent files (within 2 minutes)
[ -z "$FILE" ] && FILE=$(find "$PROJECT_DIR" -name "*.png" -mmin -2 2>/dev/null | head -1)

# Pattern 3: Any PNG file
[ -z "$FILE" ] && FILE=$(find "$PROJECT_DIR" -name "*.png" 2>/dev/null | head -1)

# Only create placeholder as last resort
if [ -z "$FILE" ]; then
  echo "WARNING: Creating placeholder after all searches failed"
  echo "Placeholder" > "$PROJECT_DIR/media/images/scene1.png"
fi
```

---

## 🎯 Critical Points

### 1. URL Expiration (15 minutes)
```bash
# MUST check URL validity before use
if curl -IfsS --max-time 5 "$URL" >/dev/null 2>&1; then
  echo "URL valid"
else
  echo "URL expired, using local file"
fi
```

### 2. File Size Validation
```bash
# Verify actual file, not placeholder
if [ -f "$FILE" ]; then
  SIZE=$(stat -c%s "$FILE" 2>/dev/null || echo 0)
  if [ "$SIZE" -lt 10000 ]; then
    echo "WARNING: File too small, likely placeholder"
  fi
fi
```

### 3. Parallel Processing Data Isolation
```yaml
matrix:
  scene: [1, 2, 3, 4, 5]
  max-parallel: 5

# Each job needs unique output paths
output: ${PROJECT_DIR}/media/scene${matrix.scene}.png
```

---

## 💡 Best Practices

### 1. Always Include Write Tool
```bash
--allowedTools "mcp__t2i-*,Write,Bash"  # Not just mcp__t2i-*
```

### 2. Explicit Path in Every Prompt
```bash
# Good
PROMPT="Save to ${SAVE_PATH}"

# Bad
PROMPT="Generate image"
```

### 3. Immediate URL Download
```bash
# Download right after generation
[ -f "$URL_FILE" ] && curl -L -o "$LOCAL_FILE" "$(cat $URL_FILE)"
```

### 4. Validate Before Processing
```bash
# Check file existence and size
if [ -f "$FILE" ] && [ $(stat -c%s "$FILE") -gt 10000 ]; then
  process_file
else
  handle_error
fi
```

---

## 📐 Pattern Templates

### T2I Generation with Save
```bash
generate_image() {
  local SCENE_NUM=$1
  local SAVE_PATH="${PROJECT_DIR}/media/images/scene${SCENE_NUM}.png"
  local URL_PATH="${PROJECT_DIR}/media/images/scene${SCENE_NUM}-url.txt"
  
  npx @anthropic-ai/claude-code \
    --allowedTools "mcp__t2i-*,Write,Bash" \
    -p "1. Generate image
        2. Save to ${SAVE_PATH}
        3. Save URL to ${URL_PATH}
        4. Run ls -la to verify"
  
  # Immediate download
  [ -f "$URL_PATH" ] && curl -L -o "$SAVE_PATH" "$(cat $URL_PATH)"
  
  # Validate
  if [ ! -f "$SAVE_PATH" ] || [ $(stat -c%s "$SAVE_PATH") -lt 10000 ]; then
    echo "ERROR: Image generation failed"
    return 1
  fi
}
```

### I2V Conversion with URL Handling
```bash
convert_to_video() {
  local SCENE_NUM=$1
  local IMAGE_URL_FILE="${PROJECT_DIR}/media/images/scene${SCENE_NUM}-url.txt"
  local IMAGE_LOCAL="${PROJECT_DIR}/media/images/scene${SCENE_NUM}.png"
  local VIDEO_PATH="${PROJECT_DIR}/media/videos/scene${SCENE_NUM}.mp4"
  
  # Determine input
  if [ -f "$IMAGE_URL_FILE" ]; then
    IMAGE_URL=$(cat "$IMAGE_URL_FILE")
    if curl -IfsS --max-time 5 "$IMAGE_URL" >/dev/null 2>&1; then
      IMAGE_INPUT="$IMAGE_URL"
    else
      IMAGE_INPUT="$IMAGE_LOCAL"
    fi
  else
    IMAGE_INPUT="$IMAGE_LOCAL"
  fi
  
  npx @anthropic-ai/claude-code \
    --allowedTools "mcp__i2v-*,Write,Bash" \
    -p "1. Convert ${IMAGE_INPUT} to video
        2. Save to ${VIDEO_PATH}
        3. Verify with ls -la"
}
```

---

## 🚫 Common Anti-Patterns

### ❌ Missing Save Instructions
```bash
# BAD
-p "Generate image for scene 1"
```

### ❌ Single Pattern Search
```bash
# BAD
IMAGE=$(find . -name "scene1.png")
```

### ❌ No URL Validation
```bash
# BAD
IMAGE_URL=$(cat url.txt)
# Direct use without checking
```

### ❌ Early Placeholder Creation
```bash
# BAD
[ -z "$FILE" ] && echo "Placeholder" > file.png
```

---

## ✅ Validation Checklist

- [ ] All prompts include explicit save paths
- [ ] Write tool included in allowedTools
- [ ] Multi-pattern file search (3+ patterns)
- [ ] URL validity checks before use
- [ ] File size validation (>10KB for images)
- [ ] Immediate URL download after generation
- [ ] Unique paths for parallel processing
- [ ] Placeholder only as last resort

---

## 📚 Related Documents

- [CLAUDE_CODE_DATA_PERSISTENCE_GUIDE.md](./CLAUDE_CODE_DATA_PERSISTENCE_GUIDE.md) - **Consolidated Data Persistence Guide (MUST READ)**
- [MINIMAL_UNIT_DATA_DEPENDENCIES.md](./MINIMAL_UNIT_DATA_DEPENDENCIES.md) - Data dependency specifications
- [YAML_CONSTRUCTION_GUIDELINES.md](./YAML_CONSTRUCTION_GUIDELINES.md) - YAML construction best practices
- [meta/domain-templates/video-production/constraints.yaml](../meta/domain-templates/video-production/constraints.yaml) - Video production constraints