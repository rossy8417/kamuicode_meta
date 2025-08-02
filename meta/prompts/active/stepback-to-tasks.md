# Stepback Answers to Task Plan Generator

Analyze user's stepback answers and convert them into a concrete task plan.

## Input Data

### Workflow Type
```
{{WORKFLOW_TYPE}}
```

### Stepback Answers
Actual user answers will be appended below:

## Analysis Instructions

Analyze the following stepback answers and generate a task plan optimized for the user's requirements:

### Analysis Points
1. **Q1 (Structure/Architecture)** → Reflect in processing method/stage design
2. **Q2 (Quality/Performance)** → Reflect in quality settings/parallel processing design
3. **Q3 (Error Handling)** → Reflect in fallback strategy/retry settings
4. **Q4 (Output/Storage)** → Reflect in output format/intermediate file storage
5. **Q5 (Extensibility)** → Reflect in monitoring/log settings

## Required Output Format

Output in the following JSON format to `generated/metadata/task-decomposition/task-plan.json`:

```json
{
  "workflow_type": "{{WORKFLOW_TYPE}}",
  "estimated_duration_minutes": number,
  "user_requirements": {
    "architecture": "User-specified structural design",
    "quality_priority": "Quality priority",
    "error_handling": "Error response method",
    "output_format": "Output requirements",
    "extensibility": "Extensibility requirements"
  },
  "tasks": [
    {
      "id": "task-001",
      "name": "Specific task name",
      "description": "Detailed description reflecting user requirements",
      "type": "mcp_generation|processing|integration|validation",
      "dependencies": ["Dependent task IDs"],
      "required_tools": ["t2i-google-imagen3", "i2v-fal-hailuo-02-pro"],
      "quality_settings": {
        "priority": "high|medium|low",
        "timeout_minutes": number,
        "retry_count": number
      },
      "error_handling": {
        "strategy": "retry|fallback|skip|abort",
        "fallback_service": "Alternative service name (if applicable)"
      },
      "outputs": {
        "save_intermediate": true/false,
        "formats": ["format1", "format2"],
        "metadata_level": "basic|detailed|custom"
      }
    }
  ],
  "execution_flow": [
    {
      "stage": 1,
      "parallel": false,
      "tasks": ["task-001"],
      "quality_gate": "Required quality conditions"
    }
  ],
  "monitoring": {
    "log_level": "basic|detailed|debug",
    "metrics_tracking": true/false,
    "progress_reporting": true/false
  }
}
```

## Task Generation Examples

### For video-generation
When user answers "T2I→I2V composite processing, highest quality, service switching on error, save intermediate files":

```json
{
  "workflow_type": "video-generation",
  "estimated_duration_minutes": 60,
  "tasks": [
    {
      "id": "task-001",
      "name": "High-quality image generation (T2I)",
      "type": "mcp_generation",
      "required_tools": ["t2i-google-imagen3"],
      "quality_settings": {
        "priority": "high",
        "timeout_minutes": 15,
        "retry_count": 3
      },
      "error_handling": {
        "strategy": "fallback",
        "fallback_service": "t2i-fal-imagen4-ultra"
      },
      "outputs": {
        "save_intermediate": true,
        "formats": ["png", "jpg"],
        "metadata_level": "detailed"
      }
    },
    {
      "id": "task-002", 
      "name": "Image to video generation (I2V)",
      "type": "mcp_generation",
      "dependencies": ["task-001"],
      "required_tools": ["i2v-fal-hailuo-02-pro"],
      "quality_settings": {
        "priority": "high",
        "timeout_minutes": 20,
        "retry_count": 2
      }
    }
  ]
}
```

## Important Guidelines

1. **Maximize use of user answers**: Specifically reflect answer content rather than fallbacks
2. **Balance quality and performance**: Adjust according to user's priority
3. **Concrete error handling**: Specify executable strategies, not abstract ones
4. **Staged execution**: Efficient execution order considering dependencies
5. **Observability**: Design to track progress and errors

## Fallback Processing

Use the following default settings only when stepback answers are insufficient:
- Quality priority: medium
- Error handling: retry (3 times)
- Output: Save final results only
- Log level: basic