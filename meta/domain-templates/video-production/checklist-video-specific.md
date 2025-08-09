# Video Generation Domain-Specific Checklist

**Created**: 2025-08-08  
**Purpose**: Video generation specific problem-solution patterns extracted from workflow-execution-logs  
**Target**: News videos, promotional videos, educational content, and other video production workflows

---

## 🎬 **Video Generation Specific Constraints & Requirements**

### **⏱️ Video Length Limitation Handling**
- [ ] **MCP Service Video Length Limit**: 5-8 seconds/clip (current i2v services)
- [ ] **Target Video Length Calculation**: 60s target → 10-12 clips required
- [ ] **Buffer Consideration**: Generate 2-3 extra clips (defective product countermeasure)

### **🔗 Parallel Pipeline Design**
- [ ] **Image→Video Immediate Conversion**: URL expiration (15min) countermeasure
- [ ] **Rolling Process Implementation**: Batch1 (Image1-5→Video1-5) → Batch2 (Image6-10→Video6-10)
- [ ] **Parallel Degree Limitation**: Max 5 parallel (API limitation consideration)

```bash
# ✅ Recommended pattern: Immediate conversion
Phase 3A: Generate Images 1-5 → Phase 4A: Immediate Video1-5 conversion
Phase 3B: Generate Images 6-10 → Phase 4B: Immediate Video6-10 conversion

# ❌ Pattern to avoid: Batch processing
Phase 3: Generate all images → (time elapsed・URL expiration) → Phase 4: Video conversion failure
```

### **📊 Quality & Consistency Assurance**
- [ ] **Style Consistency**: Use same seed value, unified prompt template
- [ ] **Resolution Unification**: Fixed 1920x1080 (subsequent editing support)
- [ ] **Frame Rate Unification**: Fixed 30fps
- [ ] **Video Duration Unification**: 6-8s per clip (adjustable range for editing)

---

## 🔧 **Technical Implementation Specific Patterns**

### **URL Management & Expiration Countermeasures**
- [ ] **Google Cloud Storage URL Storage**: Persistence via text file
- [ ] **URL vs File Path Judgment**: Google URL for MCP service, local path for fallback
- [ ] **Expiration Detection**: Processing within 15 minutes after URL generation mandatory

```bash
# ✅ URL expiration countermeasure implementation pattern
IMAGE_URL_FILE="${PROJECT_DIR}/media/images/image1-url.txt"
if [ -f "$IMAGE_URL_FILE" ]; then
  IMAGE1_URL=$(cat "$IMAGE_URL_FILE")
  # Prioritize Google URL usage
  if [[ "$IMAGE1_URL" =~ ^https://storage\.googleapis\.com ]]; then
    USE_GOOGLE_URL=true
  fi
fi
```

### **Video Generation MCP Service Selection**
- [ ] **Service Stability Verification**: Availability check in `.claude/mcp-kamuicode.json`
- [ ] **Fallback Strategy**: Alternative service when primary fails
- [ ] **Quality vs Speed Tradeoff**: Service selection according to requirements

**Proven Service Selection Patterns**:
```yaml
# Quality & stability focused
primary: i2v-kamui-hailuo-02-pro    # High quality, somewhat slow
fallback: i2v-kamui-veo3-fast       # Medium quality, fast

# Speed focused  
primary: i2v-kamui-veo3-fast        # Fast, medium quality
fallback: i2v-kamui-seedance-v1-lite # Fast, lightweight
```

### **Audio & BGM Synchronization**
- [ ] **Audio Length Pre-generation**: Duration determination before video editing
- [ ] **BGM Loop Support**: Automatic adjustment to video length
- [ ] **Audio Level Normalization**: -14 LUFS (YouTube optimization)
- [ ] **Lipsync Support**: Video-to-video processing when required

---

## 📋 **Video Editing Planning Phase Specific**

### **Claude Code SDK Utilization Patterns**
- [ ] **Editing Plan Development**: All material analysis → Timeline design → FFmpeg command generation
- [ ] **Transition Optimization**: Natural transition planning between scenes
- [ ] **Audio Sync Calculation**: Balance of narration, BGM, sound effects

```bash
# ✅ Editing planning phase implementation
EDITING_PLAN_PROMPT="Analyze all generated materials:
- Videos: scene1_video.mp4 through scene10_video.mp4 (6-8s each)  
- Audio: narration.mp3 (60s target)
- BGM: background.wav

Create comprehensive editing plan:
1. Timeline structure with precise timing
2. Transition recommendations between scenes  
3. Audio mixing levels and synchronization
4. Final FFmpeg command sequence

Output structured plan as JSON with timeline, commands, and quality checks."
```

### **Quality Verification & QA**
- [ ] **All Clips Existence Check**: File existence, size, format verification
- [ ] **Duration Calculation Verification**: Total length within target range (±5s)
- [ ] **Quality Consistency**: Resolution, FPS, codec unification verification
- [ ] **Audio Quality**: Peak level, LUFS, noise verification

---

## ⚠️ **Video Generation Specific Failure Pattern Avoidance**

### **"False Success" Detection - Enhanced Validation**
```bash
# ✅ Enhanced validation with strict file size requirements
validate_video_output() {
  local video_file="$1"
  local min_size="${2:-300000}"  # Default 300KB minimum
  
  if [ -f "$video_file" ] && [ -s "$video_file" ]; then
    local file_size=$(stat -c%s "$video_file" 2>/dev/null || echo 0)
    
    # Size validation first
    if [ "$file_size" -lt "$min_size" ]; then
      echo "❌ FILE TOO SMALL: $video_file (${file_size} bytes < ${min_size})"
      return 1
    fi
    
    # Format validation
    if ffprobe "$video_file" >/dev/null 2>&1; then
      duration=$(ffprobe -v quiet -show_entries format=duration -of csv="p=0" "$video_file")
      if (( $(echo "$duration >= 5.0" | bc -l) )); then
        echo "✅ VALID VIDEO: $video_file (${file_size} bytes, ${duration}s)"
        return 0
      fi
    fi
  fi
  echo "❌ INVALID VIDEO: $video_file"
  return 1
}
```

### **Google URL vs Local Path Priority Pattern** ⭐ **NEW**
```bash
# ✅ Prioritize Google Cloud Storage URLs over local paths
generate_video_with_url_priority() {
  local image_url="$1"
  local image_path="$2"
  local output_file="$3"
  
  # Check if Google URL is available and valid
  if [ -n "$image_url" ] && [ "$image_url" != "" ]; then
    # Verify Google URL accessibility
    if curl -IfsS --max-time 10 "$image_url" >/dev/null 2>&1; then
      echo "✅ Using Google URL: $image_url"
      VIDEO_PROMPT="Convert image to video. image_url: '${image_url}', duration: 8s"
    else
      echo "⚠️ Google URL inaccessible, using local path"
      VIDEO_PROMPT="Convert image to video. image_url: ${image_path}, duration: 8s"
    fi
  else
    echo "ℹ️ Google URL not available, using local path"
    VIDEO_PROMPT="Convert image to video. image_url: ${image_path}, duration: 8s"
  fi
  
  # Execute MCP I2V with appropriate URL
  npx @anthropic-ai/claude-code \
    --max-turns 80 \
    --mcp-config ".claude/mcp-kamuicode.json" \
    --allowedTools "mcp__i2v-*" \
    -p "$VIDEO_PROMPT"
}
```

### **URL Expiration Mass Failure**
- **Symptom**: All video generation in Phase 4 shows "Invalid base64 data" error
- **Cause**: URL expiration due to time elapsed after Phase 3 completion  
- **Countermeasure**: Force apply immediate conversion pattern

### **Video Quality Inconsistency**
- **Symptom**: Resolution, FPS, quality varies per clip
- **Cause**: Setting differences between MCP services
- **Countermeasure**: Define and verify unified parameter set

---

## 🎯 **Video Generation Metrics Targets - Updated**

### **Quality Targets - Proven Achievable**
- **Video Generation Success Rate**: 80%+ (4+ clips successful out of 5) ← *Proven achievable*
- **Quality Consistency**: Resolution, FPS, length standard deviation < 5%
- **URL Within-Expiration Processing Rate**: 100% (Zero failures due to expiration)
- **File Size Quality**: 300KB+ minimum per clip (eliminates false positives)

### **Efficiency Targets - Actual Performance**  
- **Parallel Processing Efficiency**: 35-40min completion with 5 parallel ← *Realistic estimate*
- **Resource Usage Rate**: MCP connection within 12min (safe window), fallback rate < 20%
- **Re-execution Rate**: < 10% (with 3-retry logic implementation)
- **Reporting Coverage**: 100% progressive reporting with `if: always()`

### **Technical Targets - Enhanced**
- **Editing Plan Accuracy**: Claude SDK automatic timeline accuracy > 90%
- **Audio Sync Accuracy**: Lipsync deviation < 100ms
- **Final Quality**: Complete compliance with YouTube recommended quality standards
- **Max Turns Sufficiency**: 80+ turns for I2V processing (vs previous 40 limit)
- **Artifact Preservation**: 100% artifact upload even on job failures

---

## 📝 **Continuous Improvement Process**

### **Log Accumulation & Analysis**
- Record results in `projects/workflow-execution-logs/video-generation-YYYY-MM-DD.md` after each video generation execution
- Continuously update failure patterns, new constraints, improvement points
- Template and reuse successful patterns

### **Domain Template Updates**
- Update selection criteria when new MCP services are added
- Optimize quality vs speed tradeoffs
- Expand error recovery patterns

---

**This video generation specific checklist is saved as `meta/domain-templates/video-production/checklist-video-specific.md` and utilized through domain detection → applicable checklist application flow during meta-workflow execution.**