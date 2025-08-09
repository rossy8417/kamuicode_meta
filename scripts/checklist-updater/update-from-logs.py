#!/usr/bin/env python3
"""
ログ履歴からチェックリストドキュメントを自動更新するスクリプト

このスクリプトは以下のドキュメントを更新します：
1. projects/workflow-execution-logs/meta-workflow-construction-checklist.md (汎用)
2. meta/domain-templates/[domain]/checklist-[domain]-specific.md (ドメイン特有)
"""

import os
import sys
import re
import json
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ChecklistUpdater:
    def __init__(self, base_dir: Path = Path(".")):
        self.base_dir = base_dir
        self.logs_dir = base_dir / "projects" / "workflow-execution-logs"
        self.domain_templates_dir = base_dir / "meta" / "domain-templates"
        self.updates_made = []
        
    def parse_execution_log(self, log_file: Path) -> Dict:
        """実行ログをパースして問題と解決策を抽出"""
        issues = []
        solutions = []
        domain = None
        
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # ドメイン検出
            domain_match = re.search(r'Domain:\s*(\w+[-\w]*)', content)
            if domain_match:
                domain = domain_match.group(1)
            
            # エラーパターン検出
            error_patterns = [
                r'ERROR:\s*(.+?)(?:\n|$)',
                r'❌\s*(.+?)(?:\n|$)',
                r'Failed:\s*(.+?)(?:\n|$)',
                r'Issue:\s*(.+?)(?:\n|$)'
            ]
            
            for pattern in error_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                for match in matches:
                    issues.append(match.strip())
            
            # 解決策パターン検出
            solution_patterns = [
                r'Solution:\s*(.+?)(?:\n|$)',
                r'Fixed by:\s*(.+?)(?:\n|$)',
                r'✅\s*Fixed:\s*(.+?)(?:\n|$)',
                r'Action:\s*(.+?)(?:\n|$)'
            ]
            
            for pattern in solution_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                for match in matches:
                    solutions.append(match.strip())
                    
        return {
            'domain': domain,
            'issues': issues,
            'solutions': solutions,
            'log_file': log_file.name
        }
    
    def categorize_issues(self, issues: List[Dict]) -> Dict[str, List]:
        """問題を汎用的とドメイン特有に分類"""
        generic_issues = []
        domain_specific = {}
        
        # 汎用的な問題パターン
        generic_patterns = [
            'YAML syntax',
            'HEREDOC',
            'GitHub Actions',
            'artifact',
            'timeout',
            'MCP config',
            'file path',
            'uses:',
            'max-turns',
            'validation'
        ]
        
        for issue_data in issues:
            for issue in issue_data['issues']:
                is_generic = any(pattern.lower() in issue.lower() for pattern in generic_patterns)
                
                if is_generic:
                    generic_issues.append({
                        'issue': issue,
                        'solutions': issue_data.get('solutions', []),
                        'source': issue_data['log_file']
                    })
                elif issue_data['domain']:
                    if issue_data['domain'] not in domain_specific:
                        domain_specific[issue_data['domain']] = []
                    domain_specific[issue_data['domain']].append({
                        'issue': issue,
                        'solutions': issue_data.get('solutions', []),
                        'source': issue_data['log_file']
                    })
                    
        return {
            'generic': generic_issues,
            'domain_specific': domain_specific
        }
    
    def update_generic_checklist(self, issues: List[Dict]):
        """汎用チェックリストを更新"""
        checklist_path = self.logs_dir / "meta-workflow-construction-checklist.md"
        
        if not checklist_path.exists():
            print(f"Creating new generic checklist at {checklist_path}")
            checklist_path.parent.mkdir(parents=True, exist_ok=True)
            content = self._create_generic_checklist_template()
        else:
            with open(checklist_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # 新しい問題パターンを追加
        new_patterns = []
        for issue_data in issues:
            pattern = self._extract_pattern(issue_data['issue'])
            if pattern and pattern not in content:
                new_patterns.append({
                    'pattern': pattern,
                    'solution': issue_data['solutions'][0] if issue_data['solutions'] else 'Manual investigation required',
                    'source': issue_data['source']
                })
        
        if new_patterns:
            # 既存のセクションを探して追加
            update_section = self._generate_update_section(new_patterns, 'generic')
            
            # Auto-generated sectionsマーカーを探す
            marker = "<!-- AUTO-GENERATED-PATTERNS -->"
            if marker in content:
                content = content.replace(marker, f"{marker}\n\n{update_section}")
            else:
                # マーカーがない場合は最後に追加
                content += f"\n\n{marker}\n\n{update_section}"
            
            # ファイルを更新
            with open(checklist_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.updates_made.append(f"Updated generic checklist: {len(new_patterns)} new patterns")
            print(f"✅ Updated generic checklist with {len(new_patterns)} new patterns")
    
    def update_domain_checklist(self, domain: str, issues: List[Dict]):
        """ドメイン特有チェックリストを更新"""
        domain_dir = self.domain_templates_dir / domain
        if not domain_dir.exists():
            print(f"Warning: Domain directory not found: {domain_dir}")
            return
            
        checklist_path = domain_dir / f"checklist-{domain}-specific.md"
        
        if not checklist_path.exists():
            print(f"Creating new domain checklist at {checklist_path}")
            content = self._create_domain_checklist_template(domain)
        else:
            with open(checklist_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # 新しいドメイン特有パターンを追加
        new_patterns = []
        for issue_data in issues:
            pattern = self._extract_pattern(issue_data['issue'])
            if pattern and pattern not in content:
                new_patterns.append({
                    'pattern': pattern,
                    'solution': issue_data['solutions'][0] if issue_data['solutions'] else 'Domain-specific investigation required',
                    'source': issue_data['source']
                })
        
        if new_patterns:
            update_section = self._generate_update_section(new_patterns, domain)
            
            marker = f"<!-- AUTO-GENERATED-{domain.upper()}-PATTERNS -->"
            if marker in content:
                content = content.replace(marker, f"{marker}\n\n{update_section}")
            else:
                content += f"\n\n{marker}\n\n{update_section}"
            
            with open(checklist_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.updates_made.append(f"Updated {domain} checklist: {len(new_patterns)} new patterns")
            print(f"✅ Updated {domain} checklist with {len(new_patterns)} new patterns")
    
    def _extract_pattern(self, issue: str) -> Optional[str]:
        """問題から再利用可能なパターンを抽出"""
        # 具体的な値を一般化
        pattern = issue
        pattern = re.sub(r'\d+', 'N', pattern)  # 数字を N に置換
        pattern = re.sub(r'issue-\d+', 'issue-NUMBER', pattern)
        pattern = re.sub(r'/[\w/.-]+\.(yml|yaml|json)', '/PATH/FILE.EXT', pattern)
        
        # パターンが短すぎる場合は無視
        if len(pattern) < 10:
            return None
            
        return pattern
    
    def _generate_update_section(self, patterns: List[Dict], context: str) -> str:
        """更新セクションを生成"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        section = f"### 🔄 Auto-Updated Patterns ({timestamp})\n\n"
        
        for i, pattern_data in enumerate(patterns, 1):
            section += f"#### Pattern {context.upper()}-AUTO-{i:03d}\n"
            section += f"- **Issue**: {pattern_data['pattern']}\n"
            section += f"- **Solution**: {pattern_data['solution']}\n"
            section += f"- **Source**: {pattern_data['source']}\n"
            section += f"- **Auto-detected**: {timestamp}\n\n"
            
        return section
    
    def _create_generic_checklist_template(self) -> str:
        """汎用チェックリストのテンプレート作成"""
        return """# Meta Workflow Construction Checklist (Auto-Updated)

## 🚨 Common Issues and Solutions

This document is automatically updated from workflow execution logs.

### Critical YAML Construction Issues
1. **HEREDOC in GitHub Actions**: Never use HEREDOC, use echo commands
2. **File path references**: Always use relative paths with variables
3. **MCP configuration**: Include --mcp-config for all MCP tools

### Validation Requirements
1. **Max turns for I2V**: Must be >= 80
2. **File size validation**: Check for files > 300KB
3. **Progressive reporting**: Use if: always() in at least 5 places

<!-- AUTO-GENERATED-PATTERNS -->

## 📝 Manual Entries

Add any manual observations below this line.
"""
    
    def _create_domain_checklist_template(self, domain: str) -> str:
        """ドメイン特有チェックリストのテンプレート作成"""
        return f"""# {domain.replace('-', ' ').title()} Domain-Specific Checklist

## 🎯 Domain-Specific Patterns

This document is automatically updated from {domain} workflow execution logs.

### Domain Requirements
- Specific to {domain} workflows
- Auto-detected patterns from execution

<!-- AUTO-GENERATED-{domain.upper()}-PATTERNS -->

## 📝 Manual Domain Insights

Add domain-specific insights below this line.
"""
    
    def scan_recent_logs(self, hours: int = 24) -> List[Dict]:
        """最近のログファイルをスキャン"""
        if not self.logs_dir.exists():
            print(f"Logs directory not found: {self.logs_dir}")
            return []
            
        log_files = list(self.logs_dir.glob("execution-log-*.md"))
        log_files.extend(list(self.logs_dir.glob("*.log")))
        
        issues = []
        for log_file in log_files:
            # ファイルの更新時刻をチェック（オプション）
            parsed = self.parse_execution_log(log_file)
            if parsed['issues']:
                issues.append(parsed)
                
        return issues
    
    def run(self, scan_hours: int = 24):
        """メイン実行"""
        print("🔍 Scanning execution logs...")
        all_issues = self.scan_recent_logs(scan_hours)
        
        if not all_issues:
            print("No issues found in recent logs")
            return
            
        print(f"Found {len(all_issues)} log files with issues")
        
        # 問題を分類
        categorized = self.categorize_issues(all_issues)
        
        # 汎用チェックリスト更新
        if categorized['generic']:
            self.update_generic_checklist(categorized['generic'])
        
        # ドメイン特有チェックリスト更新
        for domain, domain_issues in categorized['domain_specific'].items():
            self.update_domain_checklist(domain, domain_issues)
        
        # サマリー表示
        if self.updates_made:
            print("\n📊 Update Summary:")
            for update in self.updates_made:
                print(f"  - {update}")
        else:
            print("\n✅ All checklists are up to date")


def main():
    parser = argparse.ArgumentParser(description='Update checklists from execution logs')
    parser.add_argument('--hours', type=int, default=24,
                       help='Scan logs from past N hours (default: 24)')
    parser.add_argument('--base-dir', type=str, default='.',
                       help='Base directory of the project')
    
    args = parser.parse_args()
    
    updater = ChecklistUpdater(Path(args.base_dir))
    updater.run(args.hours)


if __name__ == "__main__":
    main()