# Workflow Startup Validation Guidelines

## Overview
This document defines validation rules to prevent workflow startup failures.

## Common Startup Errors and Prevention

### 1. Push Event Handling
**Problem**: Workflows with only `workflow_dispatch` trigger fail on push events
**Prevention**: 
- Add conditional jobs that skip on push events
- OR add push trigger with paths-ignore for workflow files

```yaml
on:
  workflow_dispatch:
    inputs: ...
  push:
    paths-ignore:
      - '.github/workflows/**'
```

### 2. Required Inputs Validation
**Problem**: Missing required inputs cause immediate failure
**Prevention**:
- Always provide defaults for required inputs
- Add input validation at job start

```yaml
jobs:
  validate-inputs:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Required Inputs
        run: |
          if [ -z "${{ inputs.required_field }}" ]; then
            echo "Error: required_field is empty"
            exit 1
          fi
```

### 3. Environment Variables
**Problem**: Missing environment variables cause job failures
**Prevention**:
- Define all env vars at workflow level
- Add existence checks before use

```yaml
env:
  CLAUDE_CODE_CI_MODE: true
  CLAUDE_CODE_AUTO_APPROVE_MCP: true
  CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

### 4. Secrets Validation
**Problem**: Using undefined secrets causes errors
**Prevention**:
- Check secret existence before critical operations
- Provide fallback behavior

```yaml
- name: Check Secrets
  run: |
    if [ -z "${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}" ]; then
      echo "Warning: CLAUDE_CODE_OAUTH_TOKEN not set"
      echo "skip_ai_generation=true" >> $GITHUB_OUTPUT
    fi
```

### 5. Artifact Dependencies
**Problem**: Jobs fail when dependent artifacts don't exist
**Prevention**:
- Add `if: always()` conditions
- Check artifact existence before download

```yaml
- name: Download Artifacts
  uses: actions/download-artifact@v4
  continue-on-error: true
  with:
    name: previous-artifacts
    path: ./artifacts/
```

### 6. Job Dependencies
**Problem**: Circular or missing dependencies
**Prevention**:
- Validate dependency chain
- Add timeout-minutes to prevent hanging

```yaml
jobs:
  job-a:
    timeout-minutes: 30
    needs: [setup]  # Clear dependency
```

### 7. Matrix Strategy Validation
**Problem**: Empty matrix causes job skip
**Prevention**:
- Add fallback for empty matrix
- Validate matrix data before use

```yaml
strategy:
  matrix:
    item: ${{ fromJson(needs.setup.outputs.items || '["default"]') }}
  fail-fast: false
```

## Mandatory Workflow Structure

Every generated workflow MUST include:

```yaml
name: Workflow Name
on:
  workflow_dispatch:
    inputs:
      # All inputs with defaults
  push:
    paths-ignore:
      - '.github/workflows/**'

env:
  # All required environment variables

jobs:
  setup:
    name: Setup and Validation
    runs-on: ubuntu-latest
    outputs:
      should_continue: ${{ steps.validate.outputs.should_continue }}
    steps:
      - name: Validate Environment
        id: validate
        run: |
          # Check all prerequisites
          echo "should_continue=true" >> $GITHUB_OUTPUT
  
  main-job:
    needs: setup
    if: needs.setup.outputs.should_continue == 'true'
    # ... rest of job
```

## Pre-deployment Checklist

Before deploying any generated workflow:

1. ✅ Has both workflow_dispatch and push triggers
2. ✅ All required inputs have defaults
3. ✅ Environment variables defined at workflow level
4. ✅ Setup job validates prerequisites
5. ✅ All jobs have timeout-minutes
6. ✅ Error recovery jobs use `if: always()`
7. ✅ Matrix strategies have fallbacks
8. ✅ No hardcoded credentials
9. ✅ Artifact operations have error handling
10. ✅ Job dependency chain is valid

## Integration with Meta-Workflow

The meta-workflow MUST:
1. Apply these validations during workflow generation
2. Add startup validation job automatically
3. Include push event handling
4. Set reasonable defaults for all inputs
5. Add environment variable declarations