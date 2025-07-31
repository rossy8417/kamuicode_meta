# Comprehensive Minimal Unit Selection

Select minimal units from the complete catalog to implement the task plan:

## Task Plan
$(cat generated/metadata/task-decomposition/task-plan.json)

## Available Units (55 total)
$(cat generated/metadata/unit-selection/unit-catalog.md)

## Selection Strategy

### 1. Comprehensive Coverage
- Ensure ALL required functionality is covered
- Select multiple units for complex tasks
- Include preparation, execution, and validation units

### 2. Parallel Optimization
- Identify 3-way parallel opportunities (e.g., multiple image generations)
- Identify 4-way parallel opportunities (e.g., variations generation)
- Identify 5-way parallel opportunities (e.g., comprehensive analysis)
- Balance parallel execution with dependencies

### 3. Human-like Selection
- Include units for research and planning phases
- Add quality check and validation units
- Include refinement and optimization units
- Add documentation and summary units

### 4. Unit Mapping Guidelines
For each task in the plan:
- Map primary functionality to core units
- Add supporting units for pre/post processing
- Include validation and quality units
- Consider fallback and alternative units

Output as JSON in generated/metadata/unit-selection/selected-units.json:
```json
{
  "selected_units": [
    {
      "task_id": "task-001",
      "unit_name": "planning-ccsdk",
      "unit_path": "minimal-units/planning/planning-ccsdk.yml",
      "purpose": "Initial project planning and structure",
      "inputs": {
        "prompt": "Generated from user requirements"
      },
      "dependencies": [],
      "parallel_group": 1,
      "execution_order": 1
    }
  ],
  "parallel_optimization": {
    "strategy": "4-way parallel for main generation, 3-way for analysis",
    "groups": {
      "1": {"units": 3, "type": "research"},
      "2": {"units": 4, "type": "generation"},
      "3": {"units": 2, "type": "validation"}
    }
  },
  "unit_statistics": {
    "total_selected": 25,
    "by_category": {
      "planning": 5,
      "image": 6,
      "video": 8,
      "audio": 4,
      "utility": 2
    }
  }
}
```
