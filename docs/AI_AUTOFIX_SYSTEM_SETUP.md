# AI-Powered Auto-Fix System Setup Guide

## Overview
An advanced automatic correction system utilizing the Claude Code SDK has been implemented.

## Major Improvements

### 1. **AI-Driven Deep Analysis**
- From fixed pattern matching to AI analysis that understands context
- Complete understanding of error logs and identification of root causes
- Decision making based on confidence scores

### 2. **Dynamic Fix Generation**
- From predefined fixes to situational fix proposals
- Automatic implementation of code changes
- Parallel application of multiple fix proposals

### 3. **Continuous Learning**
- Accumulation of learning data for each incident
- Improvement of pattern recognition
- Automatic generation of future problem prevention measures

## Setup Method

### 1. Setting Required Secrets

Add the following to GitHub Secrets:

- `CLAUDE_CODE_OAUTH_TOKEN`: Claude Pro/Max token

### 2. Token Generation Method

```bash
# Run locally
claude setup-token
# Add the generated token to GitHub Secrets
```

### 3. Learning Data Initialization

Already initialized:
- `meta/ai-learning/patterns.json` - Pattern library

## Expected Effects

- **Improved fix accuracy**: Automatic fixes with 70%+ confidence
- **Learning-based improvement**: Gets smarter with each incident
- **Reduced workload**: Significant reduction in manual debugging time
- **Preventive improvements**: Proposals to prevent future problems

## System Configuration

### Phase 1: AI-Powered Failure Analysis
- Deep contextual understanding through MCP server configuration
- Complete analysis of failure logs
- Intelligent analysis using Claude Code SDK

### Phase 2: AI-Driven Fix Implementation
- Implementation of dynamic fix proposals
- Code verification
- Automatic PR creation

### Phase 3: AI Learning and Improvement
- Learning from incidents
- Pattern library updates
- Generation of improvement reports

## MCP Servers Used

- `@modelcontextprotocol/server-github`: GitHub API integration
- `@modelcontextprotocol/server-filesystem`: File system access

## Troubleshooting

1. **Claude Code SDK Not Installed**
   - Automatic installation will be executed

2. **Invalid OAuth Token**
   - Regenerate with `claude setup-token`

3. **MCP Connection Error**
   - Automatic installation via NPX will be executed

## Next Workflow Failure

The system will automatically:
1. Detect and analyze failures
2. Propose and implement AI-driven fixes
3. Create PRs and request reviews
4. Update learning data

Only manual confirmation and merging are required.