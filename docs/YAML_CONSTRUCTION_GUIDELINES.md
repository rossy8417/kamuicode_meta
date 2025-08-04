# GitHub Actions YAML Construction Guidelines

This document provides essential guidelines for YAML construction that Meta Workflow must follow when generating workflows.

## 🚨 Critical Principles

1. **NEVER use HEREDOC**
2. **Safely handle GitHub Actions variables**
3. **ALWAYS use artifacts for data sharing between jobs**
4. **Clearly define dependencies**
5. **NEVER use backslash (\) line continuation in YAML strings - use YAML literal block scalars (|) or folded scalars (>) instead**
6. **Handle trigger-specific inputs correctly (workflow_dispatch vs issue_comment)**
7. **Use proper YAML multiline string syntax for complex prompts**

## 📋 YAML Construction Checklist

### 1. Required Basic Structure Elements
```yaml
name: "Workflow Name"          # ✅ Required
on:                           # ✅ Required
  workflow_dispatch:          # ✅ Required
    inputs:                   # For dynamic parameters
      parameter_name:
        description: "Description"
        required: true
        default: "default_value"

jobs:                         # ✅ Required
  job-name:                   # ✅ Required
    runs-on: ubuntu-latest    # ✅ Required
    needs: [prerequisite-job] # Explicit dependencies
    outputs:                  # Data passing to subsequent jobs
      output_name: ${{ steps.step-id.outputs.value }}
    steps:                    # ✅ Required
      - name: Step Name       # ✅ Required
        id: step-id           # Required when using outputs
```

### 2. ❌ Patterns to Absolutely Avoid

#### HEREDOC Usage (Most Dangerous)
```bash
# ❌ NEVER DO THIS
cat > file.yml << 'EOF'
name: workflow
on: workflow_dispatch
EOF

# ✅ Correct Method
echo 'name: workflow' > file.yml
echo 'on: workflow_dispatch' >> file.yml
```

#### Direct Embedding of GitHub Actions Variables
```bash
# ❌ GitHub Actions variables inside HEREDOC
cat > summary.md << 'EOF'
Topic: ${{ inputs.topic }}
EOF

# ✅ Correct Method
TOPIC="${{ inputs.topic }}"
echo "Topic: $TOPIC" > summary.md
```

#### Incomplete Multi-line Commands
```bash
# ❌ YAML Parser Error - Missing backslash
run: |
  npx @anthropic-ai/claude-code \
    --mcp-config ".claude/mcp-kamuicode.json" \
    --allowedTools "WebSearch,Write" \
    --permission-mode "acceptEdits"
    -p "$PROMPT"  # Error: This line is not part of the command!

# ✅ Correct - Every continuation line ends with backslash
run: |
  npx @anthropic-ai/claude-code \
    --mcp-config ".claude/mcp-kamuicode.json" \
    --allowedTools "WebSearch,Write" \
    --permission-mode "acceptEdits" \
    -p "$PROMPT"
```

#### Incorrect GitHub Actions Variable Usage
```bash
# ❌ Wrong - Using job outputs when inputs should be used
run: |
  ISSUE_NUMBER="${{ needs.some-job.outputs.issue_number }}"
  # Results in empty value for workflow_dispatch triggers

# ✅ Correct - Handle different trigger types appropriately
run: |
  if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
    ISSUE_NUMBER="${{ inputs.issue_number }}"
  else
    ISSUE_NUMBER="${{ needs.some-job.outputs.issue_number }}"
  fi
```

### 3. ✅ Recommended Patterns

#### Multi-line Command Continuation
```bash
# ❌ WRONG - Missing backslash causes YAML parsing error
npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "WebSearch,Write" \
  --max-turns 10 \
  --permission-mode "acceptEdits"
  # Next line is not part of the command!

# ✅ CORRECT - All continuation lines must end with backslash
npx @anthropic-ai/claude-code \
  --mcp-config ".claude/mcp-kamuicode.json" \
  --allowedTools "WebSearch,Write" \
  --max-turns 10 \
  --permission-mode "acceptEdits" \
  -p "$PROMPT"

# ✅ ALTERNATIVE - Single line (for shorter commands)
npx @anthropic-ai/claude-code --mcp-config ".claude/mcp-kamuicode.json" --allowedTools "WebSearch,Write" -p "$PROMPT"
```

#### Trigger-Specific Variable Handling
```bash
# Handle different trigger types correctly
run: |
  # Method 1: Direct conditional assignment
  if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
    ISSUE_NUMBER="${{ inputs.issue_number }}"
    TOPIC="${{ inputs.topic }}"
  elif [ "${{ github.event_name }}" == "issue_comment" ]; then
    ISSUE_NUMBER="${{ github.event.issue.number }}"
    TOPIC="${{ needs.extract-job.outputs.topic }}"
  fi
  
  # Method 2: Using job outputs with fallback
  ISSUE_NUMBER="${{ needs.validation-job.outputs.issue_number }}"
  if [ -z "$ISSUE_NUMBER" ] || [ "$ISSUE_NUMBER" == "null" ]; then
    ISSUE_NUMBER="${{ inputs.issue_number }}"
  fi
```

#### File Generation (echo method)
```bash
# YAML file generation
echo 'name: "Generated Workflow"' > workflow.yml
echo 'on:' >> workflow.yml
echo '  workflow_dispatch:' >> workflow.yml
echo '' >> workflow.yml
echo 'jobs:' >> workflow.yml
echo '  main:' >> workflow.yml
echo '    runs-on: ubuntu-latest' >> workflow.yml
echo '    steps:' >> workflow.yml
echo '      - name: Execute' >> workflow.yml
echo '        run: echo "Hello"' >> workflow.yml
```

#### Multi-line Text Generation
```bash
# Expand variables first
PROJECT_NAME="${{ inputs.project_name }}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Write to file
{
  echo "# Project Report"
  echo "Project: $PROJECT_NAME"
  echo "Generated: $TIMESTAMP"
  echo ""
  echo "## Results"
  echo "Status: Success"
} > report.md
```

### 4. 📊 Data Sharing Patterns Between Jobs

#### Basic Data Sharing
```yaml
job1:
  outputs:
    project_dir: ${{ steps.setup.outputs.project_dir }}
    data_file: ${{ steps.process.outputs.data_file }}
  steps:
    - id: setup
      run: |
        PROJECT_DIR="projects/run-${{ github.run_number }}"
        echo "project_dir=$PROJECT_DIR" >> $GITHUB_OUTPUT
        
    - id: process
      run: |
        echo '{"status": "success"}' > data.json
        echo "data_file=data.json" >> $GITHUB_OUTPUT

job2:
  needs: job1
  steps:
    - name: Use outputs
      run: |
        PROJECT_DIR="${{ needs.job1.outputs.project_dir }}"
        DATA_FILE="${{ needs.job1.outputs.data_file }}"
```

#### File Sharing via Artifacts
```yaml
job1:
  steps:
    - name: Generate files
      run: |
        mkdir -p output
        echo "data" > output/file.txt
        
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: job1-output
        path: output/

job2:
  needs: job1
  steps:
    - name: Download artifacts
      uses: actions/download-artifact@v4
      with:
        name: job1-output
        path: input/
        
    - name: Use files
      run: |
        cat input/file.txt
```

### 5. 🔗 Dependency Management

#### Clear Dependency Definition
```yaml
# Phase 1: Information Gathering
gather-info:
  outputs:
    info_path: ${{ steps.gather.outputs.path }}

# Phase 2: Analysis (depends on Phase 1)
analyze:
  needs: gather-info
  outputs:
    analysis_result: ${{ steps.analyze.outputs.result }}

# Phase 3: Parallel Processing (depends on Phase 2)
process-a:
  needs: analyze
  # Process A

process-b:
  needs: analyze
  # Process B (can run in parallel with A)

# Phase 4: Integration (depends on all processes)
integrate:
  needs: [process-a, process-b]
  # Integrate all results
```

### 6. 🛡️ Error Handling

#### File Existence Check
```bash
# Handle case when file doesn't exist
if [ -f "$EXPECTED_FILE" ]; then
  echo "✅ File found: $EXPECTED_FILE"
  # Continue processing
else
  echo "⚠️ File not found, creating default"
  echo '{"status": "pending"}' > "$EXPECTED_FILE"
fi
```

#### Dynamic Filename Handling
```bash
# Handle dynamically generated filenames
VIDEO_FILE=$(find . -name "*.mp4" -type f | head -1)
if [ -z "$VIDEO_FILE" ]; then
  echo "❌ No video file found"
  exit 1
fi
echo "✅ Found video: $VIDEO_FILE"
```

### 7. 🏷️ Naming Conventions and Path Management

#### Project Directory Structure
```bash
# Standard directory structure
PROJECT_DIR="projects/issue-${{ github.event.issue.number }}-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$PROJECT_DIR"/{metadata,logs,media/{images,videos,audio},final}

# Usage in each phase
echo "data" > "$PROJECT_DIR/metadata/info.json"
echo "[$(date)] Processing" >> "$PROJECT_DIR/logs/execution.log"
```

## 🔄 Minimal Unit Integration Considerations

### 1. Data Flow Between Units
```bash
# Check output from previous unit
PREVIOUS_OUTPUT="${{ needs.previous-job.outputs.result_path }}"
if [ ! -f "$PREVIOUS_OUTPUT" ]; then
  echo "❌ Previous output not found"
  exit 1
fi

# Load and process data
INPUT_DATA=$(cat "$PREVIOUS_OUTPUT")
```

### 2. Parallel Execution Feasibility
- Processes independent of input data can be parallelized
- Processes not accessing the same resources can be parallelized
- Maximum 5 parallel executions considering API limits

### 3. Output Standardization
```bash
# Unified output format
OUTPUT_JSON=$(cat << 'JSON'
{
  "status": "success",
  "timestamp": "$(date -Iseconds)",
  "data": {
    "path": "$OUTPUT_PATH",
    "type": "$OUTPUT_TYPE"
  }
}
JSON
)
echo "$OUTPUT_JSON" > "$PROJECT_DIR/metadata/unit-output.json"
```

## 📝 Essential Checks for Meta Workflow Implementation

1. **Each job runs on an independent runner**
   - File systems are not shared
   - All necessary data must be shared via artifacts

2. **GitHub Actions Limitations**
   - Workflow execution time: Maximum 6 hours
   - Job execution time: Maximum 6 hours
   - API calls: Rate limited
   - Artifact size: Maximum 5GB

3. **URL Expiration Handling**
   - Image URLs: Expire after 15 minutes
   - Move to next process immediately after generation
   - Rolling processing preferred over batch processing

4. **Trigger-Specific Input Validation**
   - Always validate trigger type before using inputs
   - Provide fallbacks for missing or null values
   - Test both workflow_dispatch and issue_comment scenarios

5. **Multi-line Command Validation**
   - Check that all continuation lines end with backslash
   - Validate command structure before deployment
   - Test YAML parsing with python yaml.safe_load()

6. **Debug Information Logging**
   ```bash
   echo "[$(date)] Job: ${{ github.job }}, Step: ${{ github.action }}" >> debug.log
   echo "Input received: $INPUT_DATA" >> debug.log
   echo "Output generated: $OUTPUT_PATH" >> debug.log
   echo "Trigger: ${{ github.event_name }}" >> debug.log
   ```

This guideline is regularly updated and will be amended when new patterns or issues are discovered.