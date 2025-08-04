# Task Order Optimization with Mermaid Diagram Generation

## 🎯 Mission
You are a professional workflow optimization expert. Analyze the provided task decomposition data and generate:
1. An optimized task execution order JSON file
2. A perfect Mermaid diagram showing the execution flow

## 📋 Input Data
Please read the task decomposition JSON file from:
**`artifacts/task-decomposition/professional_task_decomposition.json`**

**Alternative locations to check if the primary path is not found**:
- `task-decomposition/professional_task_decomposition.json`
- `artifacts/professional_task_decomposition.json`
- `professional_task_decomposition.json`

This file contains:
- Tasks with dependencies, estimated durations, and minimal units
- Professional analysis and domain-specific constraints
- Workflow optimization requirements

**EXECUTION STEPS**:
1. **Find and read the input file**: 
   - First try: `artifacts/task-decomposition/professional_task_decomposition.json`
   - If not found, search for: `task-decomposition/professional_task_decomposition.json`
   - Or any `professional_task_decomposition.json` file in the current directory structure
2. **Analyze the task structure**: Extract tasks, dependencies, durations from the found file
3. **Generate optimized order**: Create `artifacts/optimized_task_order.json`
4. **Create Mermaid diagram**: Create `artifacts/task_order_mermaid.mmd`

## 🔄 Task Analysis Requirements

### 1. Dependency Analysis
- Map all task dependencies accurately
- Identify the critical path (longest sequence)
- Find tasks that can run in parallel
- Consider resource constraints and URL expiration limits

### 2. Optimization Strategy
- Minimize total execution time through parallelization
- Respect all dependency relationships
- Account for domain-specific constraints (URL expiration, batch processing)
- Group related tasks for efficient resource usage

### 3. Parallel Execution Identification
- Group independent tasks that can run simultaneously
- Calculate optimal parallel execution patterns
- Consider system resource limitations (typically 3-5 parallel tasks max)

## 📊 Output Requirements

### 1. Optimized Task Order JSON
Save to: `artifacts/optimized_task_order.json`

```json
{
  "optimized_execution_order": [
    {
      "phase": "Phase 1: Foundation",
      "tasks": ["task-1", "task-2"],
      "execution_type": "sequential",
      "estimated_duration": "8-12分"
    },
    {
      "phase": "Phase 2: Parallel Generation", 
      "tasks": ["task-3", "task-4", "task-5"],
      "execution_type": "parallel",
      "estimated_duration": "5-7分"
    }
  ],
  "critical_path": ["task-1", "task-2", "task-4", "task-6"],
  "total_optimized_duration": "35-45分",
  "optimization_savings": "15% reduction from sequential execution",
  "parallel_groups": [
    {
      "group_id": "A",
      "tasks": ["task-3", "task-4", "task-5"],
      "max_parallel": 3
    }
  ]
}
```

### 2. Mermaid Diagram
Save to: `artifacts/task_order_mermaid.mmd`

**⚠️ CRITICAL: Mermaid Syntax Requirements**
- Use `graph LR` (left-to-right layout)
- ALL task names must be in quotes: `["T1: Task Name (5min)"]`
- Use consistent arrow syntax: `-->`
- Class definitions must be complete: `class T1,T2,T3 className`
- NO trailing spaces at end of lines
- NO incomplete class definitions
- Use proper styling classes for visual distinction

**Dynamic Mermaid Generation Requirements:**

**⚠️ CRITICAL: NO HARDCODING - Generate from actual task data**

Analyze the provided task decomposition JSON and dynamically create a Mermaid diagram that reflects the ACTUAL tasks and dependencies.

**Dynamic Structure Guidelines:**
1. **Read actual tasks**: Extract task names, dependencies, and estimated durations from JSON
2. **Map dependencies**: Create arrows based on actual task.dependencies arrays
3. **Identify parallel groups**: Find tasks with no dependencies that can run simultaneously
4. **Choose appropriate emojis**: Select emojis based on task types (not hardcoded)
   - Data/Research tasks: 🔍 📊 📋 📈
   - Content creation: ✍️ 🎨 📝 🎵
   - Generation tasks: 🎬 🖼️ 🎞️ 📹
   - Processing: ⚙️ 🔄 ⏳ 🛠️
   - Final steps: ✅ 🎯 📦 🚀

**Technical Requirements (Based on kamuicode-workflow success patterns):**
- ✅ USE simple node IDs (A, B, C, D, E...)
- ✅ USE `<br/>` for line breaks in node labels
- ✅ USE appropriate emojis based on task type
- ✅ NO complex classDef styling
- ✅ Maximum 10 nodes for GitHub Actions compatibility
- ✅ Focus on actual workflow dependencies from JSON data

**Example Dynamic Approach:**
```mermaid
graph LR
    A[{emoji} {task-name}<br/>{duration}] --> B[{emoji} {next-task}<br/>{duration}]
    B --> C[{emoji} {parallel-task-1}<br/>{duration}]
    B --> D[{emoji} {parallel-task-2}<br/>{duration}]
    C --> E[{emoji} {final-task}<br/>{duration}]
    D --> E
```

Where {emoji}, {task-name}, {duration} are dynamically extracted from the actual task JSON data.

## 🎨 Visual Design Requirements

### Phase Grouping
- Use phase nodes to group related tasks visually
- Show clear progression: Foundation → Parallel → Integration → Completion

### Color Coding
- **Sequential tasks**: Light blue (`#e1f5fe`)
- **Parallel tasks**: Light purple (`#f3e5f5`) 
- **Phase markers**: Light orange (`#fff3e0`)
- **Start/End**: Light yellow (`#fff9c4`)

### Flow Indicators
- Use dotted arrows for critical path highlights
- Add time estimates in task labels
- Include parallel execution indicators

## 🔍 Quality Assurance

### Before Saving Files
1. **JSON Validation**: Ensure valid JSON syntax
2. **Mermaid Syntax Check**: Verify all class definitions are complete
3. **Dependency Verification**: Confirm all dependencies are respected
4. **Duration Calculations**: Verify time estimates are realistic

### Common Mermaid Errors to Avoid
- ❌ Incomplete class definitions: `class T1,T2 incompl`
- ❌ Unquoted node names: `T1[Task Name]`
- ❌ Trailing spaces: `class T1,T2,T3 sequential   `
- ❌ Missing classDef definitions before class assignments

## 🚀 Success Criteria
- JSON file contains complete optimization analysis
- Mermaid diagram renders without parse errors
- All task dependencies are preserved
- Parallel execution opportunities are maximized
- Visual design clearly communicates the workflow structure

Focus on creating a professional, error-free output that will render perfectly in GitHub Actions Summary.