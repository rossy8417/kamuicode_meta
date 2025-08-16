# Error Recovery Generator Prompt

## Instructions
For any workflow with parallel generation tasks, you MUST include error recovery mechanisms following these patterns:

## Required Components

### 1. Main Generation Job Configuration
```yaml
# MANDATORY settings for parallel tasks
strategy:
  fail-fast: false  # Continue other tasks if one fails
continue-on-error: true  # Allow workflow to continue
outputs:
  failed_items: ${{ steps.collect.outputs.failed_items }}
  [item]_status: ${{ steps.verify.outputs.status }}
```

### 2. Status Verification Step
Every generation task MUST include verification:
```yaml
- name: Verify Output
  id: verify
  run: |
    if [ OUTPUT_EXISTS_AND_VALID ]; then
      echo "status=success" >> $GITHUB_OUTPUT
    else
      echo "status=failed" >> $GITHUB_OUTPUT
      echo "ITEM_ID" >> failed_items.txt
    fi
```

### 3. Recovery Job Pattern
Create a dedicated recovery job for EVERY parallel generation:
```yaml
[task]-recovery:
  name: "Failed [Task] Recovery"
  needs: [main-generation-job]
  if: |
    always() && 
    needs.[main-job].outputs.failed_items != '[]'
  strategy:
    matrix:
      item: ${{ fromJson(needs.[main-job].outputs.failed_items) }}
    max-parallel: 3
  steps:
    # Attempt 1: Alternative approach
    # Attempt 2: Simplified parameters
    # Attempt 3: Basic fallback
```

### 4. Final Assembly Adjustment
Final assembly must wait for recovery:
```yaml
final-job:
  needs: [main-generation, recovery-generation]
  if: always() && (main.result != 'cancelled')
```

## Domain-Specific Recovery Strategies

### Video Production
- Recovery 1: Alternative I2V model (e.g., vidu-q1 instead of hailuo)
- Recovery 2: Reduced resolution/duration
- Recovery 3: Static image with motion effect

### Image Generation
- Recovery 1: Different model (e.g., flux instead of imagen)
- Recovery 2: Simplified prompt
- Recovery 3: Lower resolution

### Audio Generation
- Recovery 1: Alternative TTS service
- Recovery 2: Different voice/settings
- Recovery 3: Basic synthesis

### Data Processing
- Recovery 1: Smaller batch size
- Recovery 2: Alternative data source
- Recovery 3: Cached/default data

## Implementation Rules

1. **ALWAYS** add recovery job for parallel tasks (scenes, images, data chunks)
2. **NEVER** let single failure stop entire workflow
3. **COLLECT** failure information in outputs
4. **LIMIT** recovery attempts to 3 max
5. **PROGRESSIVE** degradation (best → acceptable → minimal)

## Example for Scene Generation

```yaml
scene-generation:
  strategy:
    matrix:
      scene: [1,2,3,4,5,6,7,8,9,10,11,12]
    fail-fast: false
  continue-on-error: true
  outputs:
    failed_scenes: ${{ steps.collect.outputs.failed_scenes }}
  steps:
    - name: Generate Scene
      # ... generation logic ...
    - name: Verify Scene
      id: verify
      run: |
        if [ -f "scene${{ matrix.scene }}.mp4" ]; then
          echo "status=success" >> $GITHUB_OUTPUT
        else
          echo "status=failed" >> $GITHUB_OUTPUT
          echo "${{ matrix.scene }}" >> failed_scenes.txt
        fi
    - name: Collect Failures
      if: always()
      run: |
        # Create JSON array of failed scenes

scene-recovery:
  needs: scene-generation
  if: always() && needs.scene-generation.outputs.failed_scenes != '[]'
  strategy:
    matrix:
      scene: ${{ fromJson(needs.scene-generation.outputs.failed_scenes) }}
  steps:
    - name: Retry with Vidu Q1
    - name: Retry with lower quality
    - name: Create from static image
```

## CRITICAL: This pattern is MANDATORY for:
- Scene generation in video workflows
- Image generation in gallery workflows
- Audio segment generation
- Data chunk processing
- Any parallel matrix strategy jobs