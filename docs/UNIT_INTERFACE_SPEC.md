# Minimal Unit Interface Specification

This document defines the input/output interfaces for each minimal unit and clarifies how to connect units.

## 📐 Basic Interface Structure

### Standard Input Parameters
```yaml
inputs:
  # Required: Target file path or content for processing
  [target]_path/[target]:
    required: true
    type: string
    
  # Required: Output directory
  output_dir:
    required: true
    type: string
    
  # Optional: Processing parameters
  [parameter_name]:
    required: false
    type: string/boolean/number
    default: [default_value]
```

### Standard Output Parameters
```yaml
outputs:
  # Required: Generated file path
  [result]_path:
    value: ${{ jobs.[job_name].outputs.[result]_path }}
    
  # Optional: Processing result URL
  [result]_url:
    value: ${{ jobs.[job_name].outputs.[result]_url }}
    
  # Optional: Metadata
  [metadata]:
    value: ${{ jobs.[job_name].outputs.[metadata] }}
```

## 🔗 Unit Connection Patterns

### Pattern 1: Serial Connection
```yaml
# Connect Unit A's output to Unit B's input
unit_a:
  outputs:
    image_path: /path/to/image.png

unit_b:
  inputs:
    image_path: ${{ needs.unit_a.outputs.image_path }}
```

### Pattern 2: Parallel Processing
```yaml
# Execute multiple units in parallel
parallel_units:
  strategy:
    matrix:
      unit: [unit_a, unit_b, unit_c]
  uses: ./.github/workflows/${{ matrix.unit }}.yml
```

### Pattern 3: Conditional Branching
```yaml
# Select unit based on condition
if: ${{ needs.check_unit.outputs.condition == 'true' }}
uses: ./.github/workflows/unit_a.yml
else:
uses: ./.github/workflows/unit_b.yml
```

## 📊 Category-Specific Interface Details

### 🎯 Planning & Analysis

#### planning-ccsdk
```yaml
inputs:
  concept: string          # User concept
  output_dir: string       # Output directory
  model_preference: string # Model preference
outputs:
  plan_path: string        # Plan document path
  image_prompts: array     # Image prompt array
  video_concepts: array    # Video concept array
  audio_scripts: array     # Audio script array
```

#### web-search
```yaml
inputs:
  query: string           # Search query
  output_dir: string      # Output directory
  max_results: string     # Maximum results
outputs:
  search_results: string  # Search results
  sources: string         # Source URL list
  summary: string         # Summary
```

### 🖼️ Image System

#### image-t2i / t2i-* variants
```yaml
inputs:
  prompt: string          # Image generation prompt
  output_dir: string      # Output directory
  negative_prompt: string # Negative prompt
  width: string          # Image width
  height: string         # Image height
outputs:
  image_path: string     # Generated image path
  image_url: string      # Image URL
```

#### i2i-flux-kontext
```yaml
inputs:
  image_path: string     # Input image path
  prompt: string         # Transformation prompt
  output_dir: string     # Output directory
  strength: string       # Transformation strength
outputs:
  image_path: string     # Transformed image path
  image_url: string      # Image URL
```

### 🎥 Video System

#### video-generation
```yaml
inputs:
  mode: string           # Generation mode (i2v/t2v)
  input_path: string     # Input path (image/prompt)
  prompt: string         # Video prompt
  output_dir: string     # Output directory
outputs:
  video_path: string     # Generated video path
  video_url: string      # Video URL
  metadata: object       # Metadata
```

#### v2v-* variants
```yaml
inputs:
  video_path: string     # Input video path
  output_dir: string     # Output directory
  [style_params]: varies # Style parameters
outputs:
  video_path: string     # Transformed video path
  video_url: string      # Video URL
```

### 🔊 Audio System

#### audio-* / t2s-* variants
```yaml
inputs:
  text: string           # Text to speech
  output_dir: string     # Output directory
  voice_id: string       # Voice ID/settings
  [voice_params]: varies # Voice parameters
outputs:
  audio_path: string     # Generated audio path
  audio_url: string      # Audio URL
  duration: string       # Audio duration
```

#### bgm-overlay
```yaml
inputs:
  video_path: string     # Input video path
  bgm_path: string       # BGM file path
  output_dir: string     # Output directory
  bgm_volume: string     # BGM volume
outputs:
  video_path: string     # Video with BGM path
```

### 👄 Lipsync System

#### lipsync-pixverse
```yaml
inputs:
  video_path: string     # Input video path
  audio_path: string     # Audio file path
  output_dir: string     # Output directory
outputs:
  video_path: string     # Lipsynced video path
  video_url: string      # Video URL
  sync_score: string     # Sync score
```

#### subtitle-overlay
```yaml
inputs:
  video_path: string     # Input video path
  srt_path: string       # SRT file path
  output_dir: string     # Output directory
  style: object          # Subtitle style
outputs:
  video_path: string     # Video with subtitles path
```

### 🔧 Assembly System

#### video-concat
```yaml
inputs:
  video_paths: string    # Video paths (comma-separated)
  output_dir: string     # Output directory
  bgm_path: string       # BGM path (optional)
outputs:
  video_path: string     # Concatenated video path
  total_duration: string # Total duration
```

#### fal-upload
```yaml
inputs:
  asset_path: string     # Upload file path
  output_dir: string     # Output directory
  asset_type: string     # Asset type
outputs:
  asset_url: string      # Upload URL
  upload_info: object    # Upload information
```

## 🔄 Data Flow Examples

### Example 1: Image → Video → Video with Audio
```yaml
flow:
  1. planning-ccsdk
     outputs: image_prompt, video_concept, audio_script
     
  2. image-t2i
     inputs: prompt = image_prompt
     outputs: image_path
     
  3. video-generation
     inputs: mode = "i2v", input_path = image_path
     outputs: video_path
     
  4. audio-minimax
     inputs: text = audio_script
     outputs: audio_path
     
  5. subtitle-overlay
     inputs: video_path, audio_path
     outputs: final_video_path
```

### Example 2: Parallel Generation → Synthesis
```yaml
flow:
  1. planning-ccsdk
     outputs: prompts[], scripts[]
     
  2. parallel:
     - image-t2i (foreach prompt)
       outputs: image_paths[]
     - t2s-google (foreach script)
       outputs: audio_paths[]
       
  3. video-generation (foreach image)
     inputs: image_paths[]
     outputs: video_paths[]
     
  4. video-concat
     inputs: video_paths
     outputs: final_video_path
```

## ⚙️ Parameter Conversion Guide

### String Array Passing
```yaml
# Output side: Output as comma-separated string
outputs:
  file_list: "file1.mp4,file2.mp4,file3.mp4"

# Input side: Receive as comma-separated string
inputs:
  video_paths: ${{ needs.previous.outputs.file_list }}
```

### JSON Object Passing
```yaml
# Output side: Output as JSON string
outputs:
  metadata: '{"width":1920,"height":1080,"fps":30}'

# Input side: Receive as JSON string, parse internally
inputs:
  video_specs: ${{ needs.previous.outputs.metadata }}
```

### Conditional Parameters
```yaml
# Utilize default values
inputs:
  quality: ${{ inputs.quality || 'standard' }}
  
# Conditional switching
inputs:
  model: ${{ inputs.fast_mode == 'true' && 't2i-sdxl' || 't2i-imagen3' }}
```

## 📋 Checklist

### When Creating Units
- [ ] Define required input parameters
- [ ] Define required output parameters
- [ ] Set appropriate default values
- [ ] Define error outputs
- [ ] Document interface

### When Connecting Units
- [ ] Output and input types match
- [ ] Required parameters are provided
- [ ] Error handling is appropriate
- [ ] Confirm parallel execution possibility
- [ ] Check for resource conflicts

Please refer to this interface specification to achieve proper connections between units.