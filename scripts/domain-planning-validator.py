#!/usr/bin/env python3
"""
Domain-Specific Planning Validation Script
タスク分解後、ワークフロー生成前の計画段階検証
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

class PlanningValidator:
    def __init__(self, task_decomposition_path: str, domain: str):
        self.task_decomposition_path = Path(task_decomposition_path)
        self.domain = domain
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
    def validate_planning(self) -> Dict[str, Any]:
        """計画段階の包括検証"""
        with open(self.task_decomposition_path) as f:
            decomposition = json.load(f)
        
        results = {
            "domain_requirements": self.validate_domain_requirements(decomposition),
            "pipeline_structure": self.validate_planned_pipeline_structure(decomposition), 
            "url_expiration_strategy": self.validate_url_expiration_strategy(decomposition),
            "parallel_optimization": self.validate_parallel_planning(decomposition),
            "mcp_usage_planning": self.validate_mcp_planning(decomposition),
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
            "requires_modification": len(self.issues) > 0
        }
        
        return results
    
    def validate_domain_requirements(self, decomposition: Dict) -> bool:
        """ドメイン要件検証"""
        if self.domain == "video-production":
            return self.validate_video_production_requirements(decomposition)
        elif self.domain == "article-blog":
            return self.validate_article_requirements(decomposition)
        return True
    
    def validate_video_production_requirements(self, decomposition: Dict) -> bool:
        """動画制作ドメイン要件検証"""
        tasks = decomposition.get("tasks", [])
        
        # 必須要素チェック
        required_elements = {
            "image_generation": False,
            "video_conversion": False,
            "audio_generation": False,
            "video_editing": False
        }
        
        for task in tasks:
            task_desc = task.get("description", "").lower()
            task_name = task.get("name", "").lower()
            combined = f"{task_name} {task_desc}"
            
            if "画像" in combined or "image" in combined:
                required_elements["image_generation"] = True
            if "動画" in combined and ("変換" in combined or "生成" in combined or "i2v" in combined):
                required_elements["video_conversion"] = True
            if "音声" in combined or "audio" in combined or "ナレーション" in combined:
                required_elements["audio_generation"] = True
            if "編集" in combined or "合成" in combined or "composition" in combined:
                required_elements["video_editing"] = True
        
        missing = [k for k, v in required_elements.items() if not v]
        if missing:
            self.issues.append(f"❌ Missing essential video production elements: {', '.join(missing)}")
            return False
        
        return True
    
    def validate_planned_pipeline_structure(self, decomposition: Dict) -> bool:
        """計画されたパイプライン構造検証"""
        tasks = decomposition.get("tasks", [])
        
        # 直列並列パイプライン検出
        image_tasks = []
        video_tasks = []
        
        for i, task in enumerate(tasks):
            task_desc = task.get("description", "").lower()
            task_name = task.get("name", "").lower()
            
            if "画像生成" in f"{task_name} {task_desc}" or "image generation" in f"{task_name} {task_desc}":
                image_tasks.append(i)
            elif ("動画生成" in f"{task_name} {task_desc}" or "video generation" in f"{task_name} {task_desc}" or 
                  "i2v" in f"{task_name} {task_desc}"):
                video_tasks.append(i)
        
        # 直列並列パイプライン推奨
        if len(image_tasks) >= 3 and len(video_tasks) >= 3:
            # 依存関係確認
            proper_dependencies = False
            for video_idx in video_tasks:
                video_task = tasks[video_idx]
                deps = video_task.get("dependencies", [])
                
                # 画像タスクに依存しているか？
                for dep in deps:
                    dep_task_id = dep if isinstance(dep, str) else dep
                    for img_idx in image_tasks:
                        if tasks[img_idx].get("id") == dep_task_id:
                            proper_dependencies = True
                            break
            
            if not proper_dependencies:
                self.issues.append("❌ CRITICAL: No proper image→video dependencies detected for URL expiration handling")
                self.recommendations.append("🔧 Implement serial-parallel pipeline: Individual image generation jobs → Individual video conversion jobs")
                return False
        else:
            self.warnings.append("⚠️ Limited parallel processing detected - may impact efficiency")
        
        return True
    
    def validate_url_expiration_strategy(self, decomposition: Dict) -> bool:
        """URL期限切れ対策検証"""
        tasks = decomposition.get("tasks", [])
        
        # バッチ処理検出（問題パターン）
        batch_processing_detected = False
        for task in tasks:
            desc = task.get("description", "").lower()
            if "全て" in desc and ("画像" in desc or "動画" in desc):
                batch_processing_detected = True
                break
            if "一括" in desc and ("生成" in desc or "変換" in desc):
                batch_processing_detected = True
                break
        
        if batch_processing_detected:
            self.issues.append("❌ CRITICAL: Batch processing detected - high risk of Google URL expiration")
            self.recommendations.append("🔧 Switch to rolling processing: Generate→Convert→Generate→Convert pattern")
            return False
        
        # URL保存戦略確認
        url_strategy_found = False
        for task in tasks:
            desc = task.get("description", "").lower()
            if "url" in desc and ("保存" in desc or "記録" in desc or "save" in desc):
                url_strategy_found = True
                break
        
        if not url_strategy_found:
            self.warnings.append("⚠️ No explicit URL preservation strategy detected")
            self.recommendations.append("💡 Add Google URL saving to text files for each generated asset")
        
        return True
    
    def validate_parallel_planning(self, decomposition: Dict) -> bool:
        """並列処理計画検証"""
        tasks = decomposition.get("tasks", [])
        
        # 並列化可能タスクの検出
        parallelizable_groups = []
        current_group = []
        
        for task in tasks:
            deps = task.get("dependencies", [])
            if not deps:  # 依存関係なし
                current_group.append(task["name"])
            elif len(current_group) > 1:
                parallelizable_groups.append(current_group)
                current_group = [task["name"]]
            else:
                current_group = [task["name"]]
        
        if len(current_group) > 1:
            parallelizable_groups.append(current_group)
        
        # 効率性評価
        total_parallel_potential = sum(len(group) for group in parallelizable_groups if len(group) > 1)
        if total_parallel_potential < 5:
            self.warnings.append("⚠️ Limited parallelization opportunities detected")
            self.recommendations.append("💡 Consider reorganizing independent tasks for better parallel execution")
        
        return True
    
    def validate_mcp_planning(self, decomposition: Dict) -> bool:
        """MCP使用計画検証"""
        tasks = decomposition.get("tasks", [])
        
        mcp_heavy_tasks = 0
        total_estimated_time = 0
        
        for task in tasks:
            desc = task.get("description", "").lower()
            minimal_units = task.get("minimal_units", [])
            estimated = task.get("estimated_duration", "0分")
            
            # 時間抽出
            import re
            time_match = re.search(r'(\d+)分', estimated)
            if time_match:
                total_estimated_time += int(time_match.group(1))
            
            # MCP heavy タスク判定
            if any(unit in ["t2i", "i2v", "t2v", "t2s", "v2v"] for unit in minimal_units):
                mcp_heavy_tasks += 1
        
        # 15分制限チェック
        if total_estimated_time > 15:
            self.warnings.append(f"⚠️ Total estimated time ({total_estimated_time}min) exceeds MCP safe window (15min)")
            self.recommendations.append("🔧 Front-load all MCP operations in first 12 minutes")
        
        if mcp_heavy_tasks > 8:
            self.warnings.append(f"⚠️ High MCP usage ({mcp_heavy_tasks} tasks) - timeout risk")
            self.recommendations.append("🔧 Consider fallback strategies for MCP-heavy operations")
        
        return True
    
    def validate_article_requirements(self, decomposition: Dict) -> bool:
        """記事・ブログドメイン要件検証"""
        tasks = decomposition.get("tasks", [])
        
        required_elements = {
            "research": False,
            "content_generation": False,
            "formatting": False
        }
        
        for task in tasks:
            combined = f"{task.get('name', '')} {task.get('description', '')}".lower()
            
            if "調査" in combined or "research" in combined or "情報収集" in combined:
                required_elements["research"] = True
            if "記事" in combined or "content" in combined or "執筆" in combined:
                required_elements["content_generation"] = True
            if "フォーマット" in combined or "format" in combined or "整形" in combined:
                required_elements["formatting"] = True
        
        missing = [k for k, v in required_elements.items() if not v]
        if missing:
            self.issues.append(f"❌ Missing essential article elements: {', '.join(missing)}")
            return False
        
        return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python domain-planning-validator.py <task_decomposition_path> <domain>")
        sys.exit(1)
    
    task_decomposition_path = sys.argv[1]
    domain = sys.argv[2]
    
    validator = PlanningValidator(task_decomposition_path, domain)
    results = validator.validate_planning()
    
    print("# Domain-Specific Planning Validation Report")
    print()
    
    if results['issues']:
        print("## 🚨 Critical Planning Issues")
        for issue in results['issues']:
            print(f"- {issue}")
        print()
    
    if results['warnings']:
        print("## ⚠️ Planning Warnings")
        for warning in results['warnings']:
            print(f"- {warning}")
        print()
    
    if results['recommendations']:
        print("## 💡 Improvement Recommendations")
        for rec in results['recommendations']:
            print(f"- {rec}")
        print()
    
    print("## 📊 Planning Validation Results")
    for category, result in results.items():
        if category not in ['issues', 'warnings', 'recommendations', 'requires_modification']:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"- **{category.replace('_', ' ').title()}**: {status}")
    
    if results['requires_modification']:
        print("\n## 🔧 **ACTION REQUIRED: PLANNING MODIFICATION NEEDED**")
        sys.exit(1)
    else:
        print("\n## ✅ **PLANNING VALIDATION: APPROVED FOR GENERATION**")
        sys.exit(0)

if __name__ == "__main__":
    main()