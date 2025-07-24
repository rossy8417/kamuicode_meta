# Task: {{task_name}}

## Objective
{{task_description}}

## Context
- Task ID: {{task_id}}
- Stage: {{stage}}
- Dependencies: {{dependencies}}

## Instructions
{{specific_instructions}}

## Expected Output
- Format: {{output_format}}
- Location: {{output_location}}
- Validation: {{validation_criteria}}

## Parameters
{{#each parameters}}
- {{@key}}: {{this}}
{{/each}}

## Error Handling
If the task cannot be completed:
1. Log the specific error
2. {{fallback_strategy}}
3. Continue with remaining tasks if possible