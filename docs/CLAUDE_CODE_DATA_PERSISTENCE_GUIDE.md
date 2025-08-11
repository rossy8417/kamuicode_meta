# Claude Code Data Persistence Guide

**Consolidated Document**: This guide consolidates the following documents:
- `minimal-units/CLAUDE_CODE_EXECUTION_PATTERNS.md`
- `meta/prompts/claude-code-execution-patterns.md`
- `docs/MINIMAL_UNIT_CONNECTION_PATTERNS.md` (relevant sections)
- `docs/YAML_CONSTRUCTION_GUIDELINES.md` (Section 7)

---

## 🚨 Critical: Root Cause and Solution for Placeholder Issues

### The Core Problem
Claude Code SDK **successfully executes MCP tools** but **doesn't create local files without explicit save instructions**.
This results in all generated content becoming placeholder files (27-byte text files), causing subsequent processing to fail.

### Failure Mechanism
```yaml
1. Claude Code executes MCP tool ✅
2. File NOT saved locally ❌ (no save instruction)
3. Find command returns nothing ❌
4. Placeholder text file created ❌
5. Next step fails: "Could not process image" ❌
```

---

## 📋 Mandatory Implementation Patterns

### 1. T2I (Text-to-Image) Generation

#### ✅ Correct Pattern (MANDATORY)
```bash
# STEP 1: Define explicit save paths
SAVE_PATH="${PROJECT_DIR}/media/images/scene${SCENE_NUM}.png"
URL_PATH="${PROJECT_DIR}/media/images/scene${SCENE_NUM}-url.txt"

# STEP 2: Prompt with detailed instructions
GENERATION_PROMPT="Generate image following these steps:
1. Generate image using MCP tool mcp__t2i-kamui-imagen3__imagen_t2i
2. Save generated image to ${SAVE_PATH} using Write tool
3. Save Google Cloud Storage URL to ${URL_PATH}
4. Execute ls -la ${PROJECT_DIR}/media/images/ using Bash tool to verify
Important: Execute all steps in order"

# STEP 3: Include Write and Bash tools
npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2i-*,Write,Bash" \
  --max-turns 40 \
  --permission-mode "bypassPermissions" \
  -p "$GENERATION_PROMPT"

# STEP 4: Immediate verification and download
ls -la "${PROJECT_DIR}/media/images/"
[ -f "$URL_PATH" ] && curl -L -o "$SAVE_PATH" "$(cat $URL_PATH)"

# STEP 5: Multi-pattern file search (3+ patterns)
IMAGE=$(find "$PROJECT_DIR" -type f -name "*scene*${SCENE_NUM}*.png" 2>/dev/null | head -1)
[ -z "$IMAGE" ] && IMAGE=$(find "$PROJECT_DIR" -type f -name "*.png" -mmin -2 2>/dev/null | head -1)
[ -z "$IMAGE" ] && IMAGE=$(find "$PROJECT_DIR" -type f -name "*.png" 2>/dev/null | head -1)

# STEP 6: File size validation
if [ -n "$IMAGE" ] && [ -f "$IMAGE" ]; then
  FILE_SIZE=$(stat -c%s "$IMAGE" 2>/dev/null || echo 0)
  if [ "$FILE_SIZE" -gt 10000 ]; then
    echo "✅ Image generated successfully: $IMAGE (${FILE_SIZE} bytes)"
  else
    echo "⚠️ File too small: $IMAGE (${FILE_SIZE} bytes)"
  fi
fi
```

#### ❌ Wrong Pattern (AVOID)
```bash
# ❌ BAD: Ambiguous save instruction
npx @anthropic-ai/claude-code \
  --allowedTools "mcp__t2i-*" \
  -p "Generate an image"

# File not found, creates placeholder
IMAGE=$(find . -name "*.png" | head -1)
if [ -z "$IMAGE" ]; then
  echo "Placeholder" > image.png  # THIS IS THE PROBLEM!
fi
```

### 2. I2V (Image-to-Video) Conversion

```bash
# Handle both URL and local path
URL_FILE="${PROJECT_DIR}/media/images/scene${SCENE_NUM}-url.txt"
LOCAL_IMAGE="${PROJECT_DIR}/media/images/scene${SCENE_NUM}.png"

# URL validity check (15-minute window)
if [ -f "$URL_FILE" ]; then
  IMAGE_URL=$(cat "$URL_FILE")
  if curl -IfsS --max-time 5 "$IMAGE_URL" >/dev/null 2>&1; then
    IMAGE_REF="$IMAGE_URL"
    echo "✅ Using Google Cloud Storage URL"
  else
    IMAGE_REF="$LOCAL_IMAGE"
    echo "⚠️ URL expired, using local path"
  fi
else
  IMAGE_REF="$LOCAL_IMAGE"
fi

# Prompt with explicit save path
VIDEO_PATH="${PROJECT_DIR}/media/videos/scene${SCENE_NUM}.mp4"
I2V_PROMPT="Convert image to video:
Input: ${IMAGE_REF}
Output: ${VIDEO_PATH}
Requirements: 6-8s duration, 1920x1080, 30fps
Steps: 1.Convert with MCP 2.Save with Write 3.Verify with ls -la"

npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__i2v-*,Write,Bash" \
  --max-turns 80 \
  --permission-mode "bypassPermissions" \
  -p "$I2V_PROMPT"
```

### 3. T2S (Text-to-Speech) Generation

```bash
AUDIO_PATH="${PROJECT_DIR}/media/audio/narration.mp3"

TTS_PROMPT="Convert text to speech:
Text: '${NARRATION_TEXT}'
Output: ${AUDIO_PATH}
Voice: English, Female, News anchor style
Steps: 1.Generate with MCP 2.Save with Write 3.Verify with ls -la"

npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "mcp__t2s-*,Write,Bash" \
  --permission-mode "bypassPermissions" \
  -p "$TTS_PROMPT"

# Verify
ls -la "${PROJECT_DIR}/media/audio/"
```

---

## 🔍 File Search Patterns (MANDATORY)

### Multi-Stage Search Strategy
```bash
# ❌ NEVER: Single pattern search
find . -name "image.png"  # Too specific!

# ✅ ALWAYS: 3+ search patterns
# Pattern 1: Specific filename
FILE=$(find "$PROJECT_DIR" -name "*${IDENTIFIER}*" -type f 2>/dev/null | head -1)

# Pattern 2: Recently created files (within 2 minutes)
[ -z "$FILE" ] && FILE=$(find "$PROJECT_DIR" -name "*.${EXT}" -mmin -2 2>/dev/null | head -1)

# Pattern 3: Any matching extension
[ -z "$FILE" ] && FILE=$(find "$PROJECT_DIR" -name "*.${EXT}" 2>/dev/null | head -1)

# Pattern 4: Recursive search from parent
[ -z "$FILE" ] && FILE=$(find "$(dirname $PROJECT_DIR)" -name "*${IDENTIFIER}*" 2>/dev/null | head -1)
```

---

## ✅ Validation Requirements

### File Size Validation
```bash
validate_file() {
  local FILE="$1"
  local MIN_SIZE="${2:-10000}"
  
  if [ -f "$FILE" ]; then
    SIZE=$(stat -c%s "$FILE" 2>/dev/null || echo 0)
    if [ "$SIZE" -gt "$MIN_SIZE" ]; then
      echo "✅ Valid: $FILE ($SIZE bytes)"
      return 0
    fi
  fi
  echo "❌ Invalid: $FILE"
  return 1
}

# Usage
validate_file "$IMAGE" 10000      # Images: 10KB minimum
validate_file "$VIDEO" 300000     # Videos: 300KB minimum
validate_file "$AUDIO" 50000      # Audio: 50KB minimum
```

### Format Validation
```bash
# Image validation
file "$IMAGE" | grep -E "PNG|JPEG" || echo "Invalid image format"

# Video validation
ffprobe -v error -show_format "$VIDEO" 2>/dev/null || echo "Invalid video"

# Audio validation
ffprobe -v error -show_streams "$AUDIO" 2>/dev/null | grep audio || echo "Invalid audio"
```

---

## 📊 Data Flow Connection Patterns

### T2I → I2V Pipeline
```yaml
T2I Output:
  - Local file: ${PROJECT_DIR}/media/images/scene1.png
  - URL file: ${PROJECT_DIR}/media/images/scene1-url.txt
  - Google Cloud URL: https://storage.googleapis.com/...

I2V Input:
  - Priority 1: Valid Google Cloud URL (within 15 minutes)
  - Priority 2: Local file path
  - Validation: curl -IfsS for URL check

Critical Point:
  - URLs expire after 15 minutes
  - Always validate before use
  - Fallback to local file is mandatory
```

### Parallel Processing Considerations
```yaml
Matrix Strategy:
  scene: [1, 2, 3, ..., 12]
  max-parallel: 12

Data Sharing:
  - Each job runs on separate machine
  - artifacts usage is mandatory
  - Ensure filename uniqueness
```

---

## 🚫 Common Failures and Solutions

### Failure Pattern 1: Ambiguous Prompts
```bash
# ❌ BAD
-p "Generate an image"

# ✅ GOOD
-p "1.Generate with MCP 2.Save to ${PATH} 3.Save URL to ${URL_PATH} 4.Verify with ls -la"
```

### Failure Pattern 2: Missing Write Tool
```bash
# ❌ BAD
--allowedTools "mcp__t2i-*"

# ✅ GOOD
--allowedTools "mcp__t2i-*,Write,Bash"
```

### Failure Pattern 3: URL Expiration
```bash
# ❌ BAD: Direct use
IMAGE_URL=$(cat url.txt)

# ✅ GOOD: Validity check
if curl -IfsS "$IMAGE_URL" >/dev/null 2>&1; then
  use_url
else
  use_local_file
fi
```

### Failure Pattern 4: Early Placeholder Creation
```bash
# ❌ BAD: Immediate placeholder
[ -z "$FILE" ] && echo "Placeholder" > file.txt

# ✅ GOOD: After 4 search patterns
# ... 4 search patterns ...
if [ -z "$FILE" ]; then
  echo "⚠️ WARNING: Creating placeholder as last resort"
  echo "Placeholder" > file.txt
fi
```

---

## 📋 Implementation Checklist

### Claude Code Execution
- [ ] Explicit save path (`${PROJECT_DIR}/media/...`)
- [ ] URL file creation (`*-url.txt`)
- [ ] Verification command (`ls -la`)
- [ ] Write tool permission (include in `--allowedTools`)
- [ ] Bash tool permission (include in `--allowedTools`)
- [ ] Step-by-step instructions (1,2,3... steps)

### File Retrieval
- [ ] Immediate URL download (`curl -L -o`)
- [ ] Multi-stage search (3+ patterns)
- [ ] URL validity check (`curl -IfsS`)
- [ ] Fallback handling (URL→local)

### Validation
- [ ] File size check
- [ ] Format validation
- [ ] Error logging
- [ ] GitHub Step Summary recording

---

## 📚 Reference Implementations

### Complete Implementation Examples
- `meta/examples/claude-code-t2i-correct-pattern.yml`

### Meta-Workflow Configuration
- `.github/workflows/meta-workflow-executor-v12.yml` (Lines 685-722)

### Domain-Specific Constraints
- `meta/domain-templates/video-production/constraints.yaml`
- `meta/domain-templates/video-production/checklist-video-specific.md`

---

## 🔄 GitHub Actions YAML Construction Notes

### Avoid HEREDOC
```bash
# ❌ BAD: HEREDOC usage
cat > file.yml << 'EOF'
name: workflow
EOF

# ✅ GOOD: Echo-based
echo 'name: workflow' > file.yml
echo 'on: workflow_dispatch' >> file.yml
```

### Safe Variable Expansion
```bash
# ❌ BAD: Direct expansion
echo "issue: ${{ github.event.issue.number }}"

# ✅ GOOD: Via variable
ISSUE_NUMBER="${{ github.event.issue.number }}"
echo "issue: $ISSUE_NUMBER"
```

---

**Version**: 2.0 (Consolidated)  
**Last Updated**: 2025-08-11  
**Status**: MANDATORY for all Claude Code executions  
**Consolidated from**: 4 separate documents → 1 unified guide