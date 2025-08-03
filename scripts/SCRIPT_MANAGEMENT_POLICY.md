# Script Management Policy

## 🎯 Core Principles

### 1. Pre-Creation Verification Process

#### Step 1: Search Existing Scripts
```bash
# Search by functionality keywords
grep -l "keyword" scripts/*.{sh,py}

# Search by script name patterns
ls scripts/*download* scripts/*artifact*

# Check SCRIPT_CATALOG.md
grep -i "functionality" scripts/SCRIPT_CATALOG.md
```

#### Step 2: Similarity Assessment
- **Same Direction**: Modify/extend existing script
- **Different Direction**: Consider new creation
- **Partial Overlap**: Extract common parts into shared library

#### Step 3: Decision Criteria
```
Same Direction Examples:
- download-workflow-results.sh vs download-workflow-artifacts.sh
  → Merge into single script

Different Direction Examples:
- fal_upload_helper.py (CI/CD) vs local_fal_upload.py (local use)
  → Keep separate due to different use cases (but share common code)
```

## 📝 Script Creation/Update Rules

### 1. Pre-Creation Checklist
- [ ] Check SCRIPT_CATALOG.md for existing functionality
- [ ] Search for similar features using grep
- [ ] Consider if existing script can be extended
- [ ] Document clear reason if new creation is necessary

### 2. Naming Convention
```
function-detail-version.extension

Good Examples:
- download-artifacts.sh
- generate-mcp-config.py
- analyze-workflow.py

Bad Examples:
- script1.sh
- test.py
- new-download.sh (when download already exists)
```

### 3. Documentation Requirements
```bash
# After script creation:
1. Add to SCRIPT_CATALOG.md
2. Include usage examples
3. Document dependencies

# When deleting script:
1. Remove from SCRIPT_CATALOG.md
2. Document deletion reason
3. Specify alternative solution
```

## 🔄 Regular Maintenance

### Monthly Review (1st of each month)
1. Identify unused scripts
   ```bash
   # Check references
   for script in scripts/*.{sh,py}; do
     refs=$(grep -r "$(basename $script)" . --exclude-dir=scripts | wc -l)
     echo "$script: $refs references"
   done
   ```

2. Consider consolidating duplicate functionality
3. Evaluate deprecation candidates

### Deletion Criteria
- No usage for 3+ months
- Clear duplication exists
- Better alternative available
- High maintenance cost

## 🗂️ Directory Structure

```
scripts/
├── SCRIPT_CATALOG.md           # Script inventory with descriptions
├── SCRIPT_MANAGEMENT_POLICY.md # This file
├── active/                     # Currently in use (default)
├── deprecated/                 # Deprecated but not deleted
└── archive/                    # Kept for reference
```

## 🚀 Implementation Examples

### Merging Similar Functions
```python
# Existing: download-workflow-results.sh
# New request: Prevent duplicate artifact downloads

# ❌ Bad: Create new smart-artifact-download.sh

# ✅ Good: Add --no-duplicates option to download-workflow-results.sh
```

### Documenting Extensions
```bash
# Record in scripts/CHANGELOG.md
## 2025-08-04
- download-workflow-results.sh: Added duplicate prevention feature
- Merged functionality from old smart-artifact-download.sh
```

## 📋 Checklist Templates

### New Script Creation
```markdown
- [ ] Searched existing scripts
- [ ] No similar functionality OR merge not feasible
- [ ] Follows naming convention
- [ ] Updated SCRIPT_CATALOG.md
- [ ] Added usage examples
- [ ] Tested thoroughly
```

### Script Deletion
```markdown
- [ ] Verified zero references
- [ ] Alternative solution ready
- [ ] Updated SCRIPT_CATALOG.md
- [ ] Documented deletion reason
- [ ] Moved to deprecated OR deleted
```

## 🔑 Key Principle

**"Enhance existing scripts rather than creating new ones"**

This policy ensures script maintainability and prevents repository bloat.