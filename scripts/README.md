# Scripts Directory

## Workflow Results Download System

### 🚀 Universal Workflow Results Downloader
**Primary Script**: `download-workflow-results.sh`

This unified script handles downloading and organizing results from all GitHub Actions workflows with comprehensive execution logging.

**Features:**
- **Universal Support**: All GitHub Actions workflows
- **Comprehensive Logging**: Single detailed execution log per workflow run
- **Smart Organization**: Workflow-specific file organization
- **Interactive Mode**: Easy selection of runs and options
- **ZIP Archives**: Optional compression for easy sharing

**Usage Examples:**
```bash
# Download latest successful run with interactive mode
./scripts/download-workflow-results.sh -i

# Download specific workflow by name
./scripts/download-workflow-results.sh -w "Meta Workflow Executor v9"

# Download specific run ID with logs only
./scripts/download-workflow-results.sh -l 16666636509

# Create ZIP archive of results
./scripts/download-workflow-results.sh -z -w "Video Content Creation Production v8"
```

**Supported Workflows:**
- Meta Workflow Executor v9 (comprehensive meta-workflow with dual-approach generation)
- Video Content Creation Production v8 (multimedia content creation pipeline)
- Simple Test Workflow (basic testing and validation)
- All other GitHub Actions workflows (generic organization)

### Key Features

**Execution Logging:**
- Single comprehensive log file per execution
- GitHub Actions API integration for complete job details
- Performance metrics and timing data
- File generation tracking and structure analysis
- Network and API status monitoring

**File Organization:**
- Workflow-specific directory structures
- Intelligent artifact categorization
- Metadata preservation and analysis
- Download manifest generation

**Integration:**
- Works with existing workflow download infrastructure
- Compatible with the Meta Workflow v9 logging system
- Supports the minimal units workflow execution logger

### Migration Notes

**v2.0 Changes:**
- Consolidated multiple separate scripts into single unified script
- Replaced multi-file logging with single comprehensive log
- Enhanced workflow-specific organization logic
- Added universal workflow support beyond video content

**Deprecated Scripts:**
- `download-meta-workflow-logs.sh` → Integrated into unified script
- `download-workflow-artifacts.sh` → Integrated into unified script

The unified approach provides better maintainability, consistent user experience, and comprehensive logging as requested.