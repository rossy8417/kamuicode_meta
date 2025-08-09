#!/usr/bin/env python3
"""
Comprehensive Workflow Validation Script
Meta Workflow Executor v12用の包括的検証
"""

import yaml
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

class WorkflowValidator:
    def __init__(self, workflow_path: str, domain: str):
        self.workflow_path = Path(workflow_path)
        self.domain = domain
        self.issues = []
        self.warnings = []
        self.validation_score = 0
        self.max_score = 0
        
    def validate_all(self) -> Dict[str, Any]:
        """包括的検証実行"""
        results = {
            "basic_structure": self.validate_basic_structure(),
            "domain_specific": self.validate_domain_specific(),
            "universal_patterns": self.validate_universal_patterns(),
            "pipeline_structure": self.validate_pipeline_structure(),
            "url_expiration_handling": self.validate_url_expiration(),
            "mcp_configuration": self.validate_mcp_configuration(),
            "issues": self.issues,
            "warnings": self.warnings,
            "score": f"{self.validation_score}/{self.max_score}",
            "percentage": round((self.validation_score / max(self.max_score, 1)) * 100, 1)
        }
        return results
    
    def validate_basic_structure(self) -> bool:
        """基本構造検証"""
        try:
            with open(self.workflow_path) as f:
                workflow = yaml.safe_load(f)
            
            required_fields = ['name', 'on', 'jobs']
            for field in required_fields:
                if field not in workflow:
                    self.issues.append(f"Missing required field: {field}")
                    return False
                else:
                    self.validation_score += 1
                    
            self.max_score += len(required_fields)
            return True
            
        except Exception as e:
            self.issues.append(f"YAML parsing error: {str(e)}")
            return False
    
    def validate_domain_specific(self) -> bool:
        """ドメイン特化検証"""
        if self.domain == "video-production":
            return self.validate_video_production_specific()
        return True
    
    def validate_video_production_specific(self) -> bool:
        """動画制作ドメイン特化検証"""
        issues_found = 0
        self.max_score += 5  # 5つの重要項目
        
        with open(self.workflow_path) as f:
            content = f.read()
        
        # 1. URL期限切れ対策（直列並列パイプライン）
        if self.check_serial_parallel_pipeline(content):
            self.validation_score += 1
        else:
            self.issues.append("❌ CRITICAL: No serial-parallel pipeline for URL expiration handling")
            issues_found += 1
        
        # 2. Google URL保存確認
        if "Google" in content and ("url.txt" in content or "URL" in content):
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ No explicit Google URL preservation detected")
        
        # 3. リトライロジック
        if "attempt" in content and "retry" in content.lower():
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ Limited retry logic detected")
            
        # 4. ファイルサイズ検証
        if "300000" in content or "300KB" in content:
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ No strict file size validation (300KB+)")
            
        # 5. MCP Max-turns設定
        if "--max-turns 80" in content:
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ I2V processing may fail due to insufficient max-turns")
        
        return issues_found == 0
    
    def check_serial_parallel_pipeline(self, content: str) -> bool:
        """直列並列パイプライン構造確認"""
        # パターン1: 個別画像生成ジョブ
        image_jobs = re.findall(r'^\s*[a-zA-Z0-9_-]*image[0-9]+[a-zA-Z0-9_-]*:', content, re.MULTILINE)
        
        # パターン2: 個別動画生成ジョブ
        video_jobs = re.findall(r'^\s*[a-zA-Z0-9_-]*video[0-9]+[a-zA-Z0-9_-]*:', content, re.MULTILINE)
        
        # パターン3: needs依存関係での直列並列確認
        image_to_video_deps = 0
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'needs:' in line and i < len(lines) - 1:
                needs_content = line + lines[i+1] if i < len(lines) - 1 else line
                if any(f'image{j}' in needs_content for j in range(1, 10)):
                    image_to_video_deps += 1
        
        # 判定
        has_individual_jobs = len(image_jobs) >= 3 and len(video_jobs) >= 3
        has_proper_deps = image_to_video_deps >= 3
        
        return has_individual_jobs and has_proper_deps
    
    def validate_universal_patterns(self) -> bool:
        """汎用パターン検証"""
        with open(self.workflow_path) as f:
            content = f.read()
        
        self.max_score += 4
        
        # HEREDOC回避
        if "<<" not in content and "EOF" not in content:
            self.validation_score += 1
        else:
            self.issues.append("❌ HEREDOC usage detected (causes YAML errors)")
        
        # if: always()パターン
        if "if: always()" in content:
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ Limited 'if: always()' usage for artifact preservation")
        
        # プログレッシブレポート
        if "$GITHUB_STEP_SUMMARY" in content:
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ No progressive reporting detected")
        
        # プロジェクトディレクトリ構造
        if "projects/" in content and not any(bad in content for bad in ["./output/", "./downloads/", "./generated/"]):
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ Suboptimal directory structure")
            
        return True
    
    def validate_pipeline_structure(self) -> bool:
        """パイプライン構造検証"""
        # 既にdomain_specificで確認済み
        return True
    
    def validate_url_expiration(self) -> bool:
        """URL期限切れ対策検証"""
        # 既にdomain_specificで確認済み
        return True
    
    def validate_mcp_configuration(self) -> bool:
        """MCP設定検証"""
        with open(self.workflow_path) as f:
            content = f.read()
        
        self.max_score += 3
        
        # MCP config指定
        if "--mcp-config" in content:
            self.validation_score += 1
        else:
            self.issues.append("❌ Missing MCP config specification")
        
        # 適切なツール名
        mcp_tools = re.findall(r'mcp__[a-zA-Z0-9_-]+__[a-zA-Z0-9_-]+', content)
        if len(mcp_tools) >= 3:
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ Limited MCP tool usage")
        
        # 環境変数
        required_env_vars = ["CLAUDE_CODE_CI_MODE", "CLAUDE_CODE_AUTO_APPROVE_MCP"]
        if all(var in content for var in required_env_vars):
            self.validation_score += 1
        else:
            self.warnings.append("⚠️ Missing required MCP environment variables")
        
        return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python comprehensive-workflow-validator.py <workflow_path> <domain>")
        sys.exit(1)
    
    workflow_path = sys.argv[1]
    domain = sys.argv[2]
    
    validator = WorkflowValidator(workflow_path, domain)
    results = validator.validate_all()
    
    print("# Comprehensive Workflow Validation Report")
    print()
    print(f"**Overall Score**: {results['score']} ({results['percentage']}%)")
    print()
    
    if results['issues']:
        print("## 🚨 Critical Issues")
        for issue in results['issues']:
            print(f"- {issue}")
        print()
    
    if results['warnings']:
        print("## ⚠️ Warnings")
        for warning in results['warnings']:
            print(f"- {warning}")
        print()
    
    print("## 📊 Validation Details")
    for category, result in results.items():
        if category not in ['issues', 'warnings', 'score', 'percentage']:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"- **{category.replace('_', ' ').title()}**: {status}")
    
    # 合格判定
    if results['percentage'] >= 80 and not results['issues']:
        print("\n## ✅ **VALIDATION RESULT: PASS**")
        sys.exit(0)
    else:
        print("\n## ❌ **VALIDATION RESULT: FAIL**")
        sys.exit(1)

if __name__ == "__main__":
    main()