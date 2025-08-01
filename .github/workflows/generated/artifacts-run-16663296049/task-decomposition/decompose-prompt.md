# Ultra-Detailed Task Decomposition Request

Based on the following user request, perform an ULTRA-DETAILED task decomposition that mimics human unconscious thought processes:

## User Request
## ワークフローの目的・背景

最新の地震情報を Web 検索で収集し、1分程度の日本語ニュース動画を自動生成する。字幕付きで分かりやすく、迅速な情報発信を目的とする。

## 期待する処理フロー
1. Web検索により最新の地震情報を収集・分析
2. 収集した情報から日本語ニュース原稿を生成
3. 地震関連の画像を生成（震源地、被害状況等）
4. 画像から動画を生成（1分程度）
5. 日本語ナレーション音声を生成
6. 日本語字幕を生成・動画にオーバーレイ
7. BGM追加・最終合成

## 最終成果物
- 1分程度の地震ニュース動画（MP4、1920x1080、日本語字幕付き）
- 日本語ナレーション音声ファイル
- 字幕ファイル（SRT）
- ニュース原稿テキスト

## 出力形式・品質

## Stepback Answers


## Workflow Type
video-generation

## Decomposition Requirements

### 1. Think Like a Human
Decompose tasks as a human would naturally think about them, including:
- Preparation tasks (checking requirements, setting up environment)
- Research tasks (looking for references, examples)
- Planning tasks (organizing approach, creating outlines)
- Main execution tasks
- Quality check tasks
- Refinement tasks
- Documentation tasks

### 2. Ultra-Fine Granularity
Break down each major task into 3-7 subtasks. For example:
- "Generate image" should become:
  - "Research visual style references"
  - "Draft initial prompt"
  - "Optimize prompt for model"
  - "Generate test image"
  - "Evaluate quality"
  - "Refine and regenerate"
  - "Select best version"

### 3. Parallel Processing Optimization
Identify opportunities for:
- 3-way parallel (common for independent generation tasks)
- 4-way parallel (for multiple variations)
- 5-way parallel (for comprehensive coverage)
- Sequential dependencies where necessary

### 4. Human-like Workflow Patterns
Include natural human behaviors:
- Iterative refinement cycles
- Quality checks after each major step
- Alternative approaches for fallback
- Documentation and note-taking
- Progress tracking

### 5. Comprehensive Coverage
Ensure the decomposition covers:
- Pre-processing (20-30% of tasks)
- Main processing (40-50% of tasks)
- Post-processing (20-30% of tasks)
- Quality assurance (10% of tasks)

Output as JSON in generated/metadata/task-decomposition/task-plan.json with structure:
```json
{
  "tasks": [
    {
      "id": "task-001",
      "name": "Research Visual References",
      "type": "research",
      "description": "Search for visual style references and examples",
      "subtasks": ["web search", "style analysis", "reference collection"],
      "dependencies": [],
      "parallel_group": 1,
      "estimated_duration": "3-5 minutes",
      "required_units": ["web-search", "image-analysis"],
      "human_behavior": "natural exploration phase"
    }
  ],
  "parallel_groups": {
    "1": ["task-001", "task-002", "task-003"],
    "2": ["task-004", "task-005"],
    "3": ["task-006", "task-007", "task-008", "task-009"]
  },
  "total_estimated_duration": "45-60 minutes",
  "optimization_notes": "3-way parallel for research, 4-way for generation"
}
```
