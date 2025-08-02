# Stepback Answer Summarizer

Summarize the user's detailed stepback answers into a concise, meaningful format for GitHub Actions extraction.

## Input: User's Detailed Answers

{{DETAILED_ANSWERS}}

## Summarization Instructions

Follow these rules to summarize each answer into a **meaningful and concise format**:

### Summarization Rules
1. **Ensure the summary makes sense as a complete thought, not just keywords**
2. **Include important keywords and decision content**
3. **Express in one line (approximately 100 characters maximum)**
4. **Keep technical details while being concise**

### Target Question Categories
- **Q1: Workflow Structure/Architecture**
- **Q2: Quality/Performance Design**  
- **Q3: Error Handling/Fallback Design**
- **Q4: Output/Storage Design**
- **Q5: Extensibility/Integration Design**

## Required Output Format

Generate summaries in the following format:

```
Q1 Answer: [Concise, meaningful summary about workflow structure]
Q2 Answer: [Concise, meaningful summary about quality/performance]  
Q3 Answer: [Concise, meaningful summary about error handling]
Q4 Answer: [Concise, meaningful summary about output/storage]
Q5 Answer: [Concise, meaningful summary about extensibility]
```

## Summary Examples

### Detailed Answer Example:
```
Q1: We will adopt T2I→I2V composite processing. Taking only text as input, we'll first generate high-quality images from text, then create videos based on those images in a two-stage process. The design allows flexible adjustment of processing stages as needed, with a structure that can incorporate additional processing steps for quality improvement.
```

### Concise Summary Example:
```
Q1 Answer: T2I→I2V composite processing, text input, two-stage processing with flexible quality adjustment
```

## Usage

1. **Paste user's detailed answers in the {{DETAILED_ANSWERS}} section above**
2. **Execute summarization with Claude Code**
3. **Add generated concise format to Issue**
4. **Automatic extraction/processing by GitHub Actions**

## Important Notes

- **Be concise without losing meaning**
- **Always include technically important elements**
- **Conform to GitHub Actions extraction pattern `Q[1-5] Answer:`**
- **Each line should be independently understandable**