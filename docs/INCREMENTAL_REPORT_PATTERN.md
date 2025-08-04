# Incremental Report Generation Pattern for GitHub Actions

This document describes how to implement incremental report generation where each job updates the report as it completes.

## 🎯 Goal

Instead of generating a final report only at the end, update the report incrementally as each job completes to provide real-time progress visibility.

## 📋 Implementation Pattern

### 1. Initialize Report Structure

```yaml
initialize-report:
  runs-on: ubuntu-latest
  outputs:
    report_initialized: ${{ steps.init.outputs.done }}
  steps:
    - name: Initialize Report
      id: init
      run: |
        mkdir -p reports
        
        # Create initial report structure
        cat > reports/workflow-report.md << 'REPORT_EOF'
        # Workflow Execution Report
        
        **Workflow**: ${{ github.workflow }}
        **Run Number**: ${{ github.run_number }}
        **Started**: $(date -Iseconds)
        **Status**: 🔄 In Progress
        
        ## Job Execution Timeline
        
        | Job | Status | Start Time | End Time | Duration | Notes |
        |-----|--------|------------|----------|----------|-------|
        REPORT_EOF
        
        echo "done=true" >> $GITHUB_OUTPUT
        
    - name: Upload Initial Report
      uses: actions/upload-artifact@v4
      with:
        name: workflow-report
        path: reports/
        retention-days: 7
```

### 2. Update Report After Each Job

```yaml
job-with-report-update:
  runs-on: ubuntu-latest
  needs: [initialize-report, previous-job]
  steps:
    # Main job tasks here
    - name: Execute Job Tasks
      id: main
      run: |
        START_TIME=$(date -Iseconds)
        
        # Your job logic here
        echo "Executing main tasks..."
        
        # Capture results
        echo "status=success" >> $GITHUB_OUTPUT
        echo "start_time=$START_TIME" >> $GITHUB_OUTPUT
        echo "end_time=$(date -Iseconds)" >> $GITHUB_OUTPUT
        
    # Update report
    - name: Download Current Report
      uses: actions/download-artifact@v4
      with:
        name: workflow-report
        path: reports/
        
    - name: Update Report
      run: |
        JOB_NAME="${{ github.job }}"
        STATUS="${{ steps.main.outputs.status }}"
        START="${{ steps.main.outputs.start_time }}"
        END="${{ steps.main.outputs.end_time }}"
        
        # Calculate duration
        START_TS=$(date -d "$START" +%s)
        END_TS=$(date -d "$END" +%s)
        DURATION=$((END_TS - START_TS))
        
        # Determine status emoji
        case "$STATUS" in
          "success") EMOJI="✅" ;;
          "failed") EMOJI="❌" ;;
          "skipped") EMOJI="⏭️" ;;
          *) EMOJI="🔄" ;;
        esac
        
        # Append to report
        echo "| $JOB_NAME | $EMOJI $STATUS | $START | $END | ${DURATION}s | - |" >> reports/workflow-report.md
        
    - name: Upload Updated Report
      uses: actions/upload-artifact@v4
      with:
        name: workflow-report
        path: reports/
        overwrite: true
```

### 3. Add Job-Specific Details

```yaml
- name: Add Detailed Results
  run: |
    # Add job-specific section to report
    cat >> reports/workflow-report.md << 'DETAILS_EOF'
    
    ### ${{ github.job }} Details
    
    **Generated Files**:
    DETAILS_EOF
    
    # List generated files
    find "$PROJECT_DIR" -type f -name "*.mp4" -o -name "*.json" | while read -r file; do
      echo "- \`$file\` ($(stat -c%s "$file" | numfmt --to=iec-i --suffix=B))" >> reports/workflow-report.md
    done
    
    # Add metrics
    cat >> reports/workflow-report.md << METRICS_EOF
    
    **Metrics**:
    - Processing Time: ${DURATION}s
    - Files Generated: $(find "$PROJECT_DIR" -type f | wc -l)
    - Total Size: $(du -sh "$PROJECT_DIR" | cut -f1)
    
    ---
    METRICS_EOF
```

### 4. Final Report Completion

```yaml
finalize-report:
  runs-on: ubuntu-latest
  needs: [all-previous-jobs]
  if: always()
  steps:
    - name: Download Report
      uses: actions/download-artifact@v4
      with:
        name: workflow-report
        path: reports/
        
    - name: Finalize Report
      run: |
        # Update status
        if [ "${{ needs.all-previous-jobs.result }}" == "success" ]; then
          sed -i 's/Status: 🔄 In Progress/Status: ✅ Completed Successfully/' reports/workflow-report.md
        else
          sed -i 's/Status: 🔄 In Progress/Status: ❌ Failed/' reports/workflow-report.md
        fi
        
        # Add completion time
        echo "" >> reports/workflow-report.md
        echo "**Completed**: $(date -Iseconds)" >> reports/workflow-report.md
        
        # Add summary
        echo "" >> reports/workflow-report.md
        echo "## Summary" >> reports/workflow-report.md
        echo "" >> reports/workflow-report.md
        echo "- Total Jobs: $(grep -c '^|' reports/workflow-report.md)" >> reports/workflow-report.md
        echo "- Successful: $(grep -c '✅' reports/workflow-report.md)" >> reports/workflow-report.md
        echo "- Failed: $(grep -c '❌' reports/workflow-report.md)" >> reports/workflow-report.md
        
    - name: Display Final Report
      run: cat reports/workflow-report.md
      
    - name: Upload Final Report
      uses: actions/upload-artifact@v4
      with:
        name: final-workflow-report
        path: reports/
```

## 🔄 Alternative: Using GitHub API

For more advanced reporting, use GitHub API to update a comment on the issue:

```yaml
- name: Update Issue Comment
  uses: actions/github-script@v7
  with:
    script: |
      const jobName = '${{ github.job }}';
      const status = '${{ steps.main.outputs.status }}';
      const issueNumber = ${{ github.event.issue.number }};
      
      // Find existing comment or create new
      const comments = await github.rest.issues.listComments({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: issueNumber
      });
      
      const reportComment = comments.data.find(c => 
        c.body.includes('<!-- workflow-report -->'));
      
      const newBody = reportComment ? 
        reportComment.body + `\n- ${jobName}: ${status}` :
        `<!-- workflow-report -->\n## Workflow Progress\n- ${jobName}: ${status}`;
      
      if (reportComment) {
        await github.rest.issues.updateComment({
          owner: context.repo.owner,
          repo: context.repo.repo,
          comment_id: reportComment.id,
          body: newBody
        });
      } else {
        await github.rest.issues.createComment({
          owner: context.repo.owner,
          repo: context.repo.repo,
          issue_number: issueNumber,
          body: newBody
        });
      }
```

## 📊 Benefits

1. **Real-time Visibility**: See progress as jobs complete
2. **Failure Analysis**: Know exactly where workflow failed
3. **Performance Metrics**: Track execution times for optimization
4. **Audit Trail**: Complete record of workflow execution

## ⚠️ Considerations

1. **Artifact Overwrite**: Use `overwrite: true` to update the same artifact
2. **Concurrency**: If jobs run in parallel, consider using job-specific report files that get merged
3. **File Locking**: No built-in file locking in artifacts, so avoid simultaneous writes
4. **Size Limits**: Keep reports concise to avoid artifact size limits