# 🏰 Balus - KAMUI Complete Reset Protocol

## Magic Word: `バルス`

When "**バルス**" is mentioned in a Claude Code session, the following complete cleanup will be automatically executed.

## 📝 Workflows to Preserve (Updated 2025/08/04)

```
.github/workflows/
├── meta-workflow-executor-v11.yml      # Latest successful meta-workflow
├── meta-workflow-executor-v12.yml.disabled  # Latest improvement (domain templates)
├── dynamic-workflow-60-v10.yml         # Latest dynamic workflow
└── video-content-creation-production-v8.yml # Successful production workflow
```

**Note:** Preserved targets may change. Update this document when changes occur.

## 🔥 Execution Details

### 1. Workflow File Deletion
- Delete all files in `.github/workflows/` except preserved targets
- Remove generated workflows, test files, etc.

### 2. Generated Data Deletion (Logs Preserved)
- `generated/workflows/staging/` - Approach-specific generation results (approach-1,2,3-result-*)
- `generated/workflows/production/` - Production-deployed workflow groups
- `generated/artifacts/` - Generated artifacts
- `generated/evaluation/` - Evaluation result data
- `generated/task-plans/` - Task plan data
- **Preserved:** `generated/workflows/validated/validation-*.log`

### 3. GitHub Actions Complete Reset
- Complete deletion of past workflow runs
- Complete deletion of GitHub Actions cache entries
- Includes failed runs and cached state data

### 4. GitHub Issues Deletion
- Delete Issues created by meta-workflow generation
- Remove workflow-request related Issues

## 🔒 Items Preserved

### Core System
- The 4 workflow files above
- `meta/examples/` - Workflow template group (9 templates)
- `meta/prompts/` - Prompt file group (including stepback analysis)
- `script/` - Script file group

### Documentation & Configuration
- `CLAUDE.md` - Project instruction manual
- `README.md` - Project description
- `CLEANUP_PROTOCOL.md` - This file
- `.git/` - Git history

### Log Files
- `generated/workflows/validated/validation-*.log` - Validation logs

## ⚠️ Important Warnings

1. **Irreversible Operation** - GitHub Actions history and Issues cannot be restored
2. **Backup Recommended** - Backup important data beforehand
3. **Core System Preservation** - Meta-workflow generation system core is maintained
4. **Staged Execution** - Stop on errors and report issues

## 🚀 Usage

### Automatic Execution (Claude Code session)
In Claude Code session:

```
バルス
```

Simply say this word and complete cleanup will be executed automatically.

### Manual Execution (Script)
Direct script execution:

```bash
./scripts/balus-complete.sh
```

The script performs:
- GitHub Actions run history deletion
- GitHub Actions cache deletion  
- Verification and cleanup confirmation

## 📚 Reference

- Magic word from the destruction spell in the movie "Castle in the Sky"
- Adopted as a magical word to instantly erase generated data
- Purpose: Periodically reset unnecessary data accumulation during system development

# 📁 Organization Guidelines

## 🎯 Basic Organization Policy

### **Project-Centric Approach**
- Content-based classification → Project-based classification
- Use `projects/current-session/` for current session
- Manage past projects with `projects/project-name/`

### **Duplication Elimination Principle**
- Merge directories with same purpose (`downloads/` + `generated/` → `projects/`)
- Move single-file directories up (`meta/prompts/templates/` → `meta/prompts/`)
- Delete empty directories (`docs/system-analysis/`)

### **Simple Structure Principle**
- Avoid excessive subdirectories (`active/staging/archive/` → flat structure)
- Maximum 3 levels of directory hierarchy
- Avoid temporary directories like `temp-*`, place in appropriate locations

## 📋 Organization Target Criteria

### **🔴 Deletion Targets**
1. **Temporary debug directories** (`v4-debug/`, `temp-*`)
2. **Duplicate function directories** (`downloads/` when `projects/` exists)  
3. **Single-file directories**
4. **Empty directories**
5. **Unused scripts** (not referenced)

### **🟡 Integration Targets**
1. **Multiple directories with same purpose**
2. **Scattered files of same type**
3. **Overly deep directory hierarchies**

### **🟢 Preservation Targets**
1. **System essential files** (`CLAUDE.md`, `README.md`)
2. **Configuration files** (`.claude/`, `requirements.txt`)
3. **Referenced files/directories**
4. **General tools** (reusable items in `scripts/`)

## 🛠️ Execution Checklist

### **Pre-Organization Check**
- [ ] Check file references (search usage with grep etc.)
- [ ] Check references in CLAUDE.md
- [ ] Check references in workflows

### **Post-Organization Updates**
- [ ] Update path references in CLAUDE.md
- [ ] Update workflow paths
- [ ] Update documentation like README

### **Organization Implementation Record**
- [x] Record what was integrated/deleted
- [x] Document new structure
- [x] Clarify criteria for future reference

## 📚 Completed Organization Patterns

### **2025/07/28 Organization**

#### **meta/ Directory Organization**
- `meta/docs/claude-code-vs-mcp-guidelines.md` → `docs/claude-code-vs-mcp-guidelines.md`
- `meta/successful-workflow-patterns.md` → `docs/analysis/successful-workflow-patterns.md`  
- `meta/patterns.json` (empty file) → deleted
- `meta/docs/` (empty directory) → deleted

#### **Applied Organization Principles**
1. **Purpose-based placement**: MCP guidelines placed in `docs/` as general documentation
2. **Analysis data integration**: Workflow analysis integrated into `docs/analysis/`
3. **Empty file deletion**: Meaningless `{"patterns": []}` file deleted
4. **Single-file directory resolution**: Moved 1 file from `meta/docs/` up then deleted directory

### **2025/08/04 Organization** 

#### **Workflow Preservation Strategy**
- **保持基準**: 最後に成功したバージョン + 最新の改良版のみ
- **削除基準**: 古いバージョン番号のワークフロー（v1-v9など）
- **例外**: .disabled拡張子の最新版は保持（テスト待ち）

#### **Root Directory Cleanup**
- **成果物移動**: ルートディレクトリのメディアファイル → `projects/current-session/final/`
- **対象ファイル**: `*.mp4`, `*.mp3`, `*.png`, `*.jpg`, `*-log.txt`
- **移動後処理**: README.mdを作成して移動履歴を記録

#### **projects/ Directory Structure**
```
projects/
├── archive/YYYY-MM/        # 古い実行結果（月別管理）
├── current-session/        # 現在のセッション成果物
│   └── final/             # ルートから移動した最終成果物
├── production/            # 本番環境で成功した結果
│   ├── issue-XX/         # Issue番号別
│   └── workflow-name/    # ワークフロー名別
├── test-runs/            # テスト実行結果
├── meta-workflow-vXX-analysis/  # 分析結果（保持）
└── workflow-execution-logs/     # 実行ログ（常に保持）
```

#### **Backup Policy Change**
- **2025/08/04以降**: バックアップ作成なし（ユーザー要請）
- **理由**: Gitで履歴管理されているため重複
- **注意**: 重要な変更前は手動でバックアップ推奨

### **Future Reference Criteria**
1. **Function-based > Content-based**: Files related to functionality are consolidated in function directories
2. **Analysis data consolidation**: All analysis results integrated into `docs/analysis/`
3. **Immediate empty file deletion**: Don't preserve meaningless placeholder files
4. **Single-file directory prohibition**: Don't create directories for just one file
5. **Latest Success Priority**: Always preserve the latest successful version of workflows
6. **Root Directory Clean**: No media files should remain in root directory

---

**🤖 Generated by Kamui Rossy Meta Workflow System**  
**⚡ Protocol Version: 1.3**  
**📅 Last Updated: 2025/08/04**  
**🔄 Updated for: Workflow preservation strategy + Root directory cleanup policy**