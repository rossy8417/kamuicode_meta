#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task Node Extraction System
既存テンプレートからタスクノードを抽出し、動的ワークフロー組み立てに使用
"""

import yaml
import json
import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path

class TaskNodeExtractor:
    def __init__(self, templates_dir: str = "meta/examples"):
        self.templates_dir = Path(templates_dir)
        self.task_nodes = {}
        self.capabilities = {}
        
    def extract_all_nodes(self) -> Dict[str, Any]:
        """全テンプレートからタスクノードを抽出"""
        for template_file in self.templates_dir.glob("*.yml"):
            if template_file.name == "README.md":
                continue
                
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = yaml.safe_load(f)
                
                template_name = template_file.stem
                self.extract_nodes_from_template(template_name, template_data)
                
            except Exception as e:
                print(f"⚠️ Error processing {template_file}: {e}")
        
        return self.task_nodes
    
    def extract_nodes_from_template(self, template_name: str, template_data: Dict) -> None:
        """個別テンプレートからタスクノード抽出"""
        if 'tasks' not in template_data:
            return
            
        for task in template_data.get('tasks', []):
            node_id = f"{template_name}_{task.get('stage', 0)}_{len(self.task_nodes)}"
            
            # タスクノードの標準化
            task_node = {
                'id': node_id,
                'source_template': template_name,
                'stage': task.get('stage', 0),
                'name': task.get('name', 'Unknown Task'),
                'parallel': task.get('parallel', False),
                'jobs': task.get('jobs', []),
                'capabilities': self.extract_capabilities(task),
                'mcp_services': self.extract_mcp_services(template_data, task),
                'dependencies': task.get('depends_on', []),
                'duration_estimate': task.get('duration_minutes', 5),
                'complexity': task.get('complexity', 1)
            }
            
            self.task_nodes[node_id] = task_node
            
            # 機能別インデックス作成
            for capability in task_node['capabilities']:
                if capability not in self.capabilities:
                    self.capabilities[capability] = []
                self.capabilities[capability].append(node_id)
    
    def extract_capabilities(self, task: Dict) -> List[str]:
        """タスクの機能を推定（日本語対応強化）"""
        capabilities = []
        name = task.get('name', '').lower()
        jobs = [j.lower() for j in task.get('jobs', [])]
        
        # 多言語キーワードベース機能推定
        capability_keywords = {
            'text_to_image': [
                'image', 'generation', 'picture', 'visual', 't2i', 'imagen',
                '画像', '生成', 'イメージ', 'ビジュアル', '描画', '作画'
            ],
            'image_to_video': [
                'video', 'animation', 'motion', 'i2v', 'movie', 'clip',
                '動画', 'ビデオ', 'アニメーション', '映像', 'ムービー'
            ],
            'text_to_music': [
                'music', 'audio', 'sound', 'bgm', 't2m', 'lyria', 'composition',
                '音楽', '音声', 'サウンド', 'オーディオ', '作曲', 'BGM'
            ],
            'video_to_audio': [
                'audio', 'extract', 'voice', 'v2a', 'sound', 'narration',
                '音声', '抽出', 'ボイス', 'ナレーション', 'セリフ', 'SE'
            ],
            'text_analysis': [
                'analysis', 'processing', 'nlp', 'prompt', 'planning', 'concept',
                '分析', '解析', 'プロンプト', '計画', 'コンセプト', '企画'
            ],
            'quality_control': [
                'validation', 'quality', 'check', 'review', 'test', 'verify',
                '検証', '品質', 'チェック', 'レビュー', 'テスト', '確認'
            ],
            'file_management': [
                'package', 'format', 'output', 'save', 'export', 'compile',
                'パッケージ', 'フォーマット', '出力', '保存', '書き出し', 'エクスポート'
            ],
            '3d_generation': [
                '3d', 'model', 'three-dimensional', 'mesh', 'render',
                '3D', 'モデル', '立体', 'レンダリング'
            ]
        }
        
        text_to_analyze = f"{name} {' '.join(jobs)}"
        
        for capability, keywords in capability_keywords.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                capabilities.append(capability)
        
        return capabilities if capabilities else ['general']
    
    def extract_mcp_services(self, template_data: Dict, task: Dict) -> List[str]:
        """使用するMCPサービスを抽出"""
        mcp_services = []
        
        # テンプレート全体からMCP参照を探す
        template_str = str(template_data)
        mcp_patterns = [
            r'--mcp\s+([a-zA-Z0-9-_]+)',
            r'mcp[_-]([a-zA-Z0-9-_]+)',
            r't2i-([a-zA-Z0-9-_]+)',
            r'i2v-([a-zA-Z0-9-_]+)',
            r't2m-([a-zA-Z0-9-_]+)',
            r'v2a-([a-zA-Z0-9-_]+)'
        ]
        
        for pattern in mcp_patterns:
            matches = re.findall(pattern, template_str)
            mcp_services.extend(matches)
        
        return list(set(mcp_services))
    
    def find_nodes_for_requirements(self, requirements: List[str]) -> List[str]:
        """要求に基づいて適切なタスクノードを選択（改良版）"""
        selected_nodes = []
        
        # 要求キーワードマップ（日本語→英語機能）
        requirement_mapping = {
            'テキストから画像': 'text_to_image',
            'テキストから画像生成': 'text_to_image', 
            '画像生成': 'text_to_image',
            '画像から動画': 'image_to_video',
            '画像から動画生成': 'image_to_video',
            '動画生成': 'image_to_video',
            'テキストから音楽': 'text_to_music',
            'テキストから音楽生成': 'text_to_music',
            '音楽生成': 'text_to_music',
            'BGM': 'text_to_music',
            '動画から音声': 'video_to_audio',
            '動画から音声抽出': 'video_to_audio',
            '音声抽出': 'video_to_audio',
            'ナレーション': 'video_to_audio',
            'セリフ': 'video_to_audio',
            'SE': 'video_to_audio',
            '3D': '3d_generation',
            '3d': '3d_generation',
            '品質': 'quality_control',
            'ファイル': 'file_management',
            '分析': 'text_analysis'
        }
        
        for requirement in requirements:
            req_lower = requirement.lower()
            
            # 直接マッピングチェック
            matched_capability = None
            for req_key, capability in requirement_mapping.items():
                if req_key.lower() in req_lower:
                    matched_capability = capability
                    break
            
            if matched_capability and matched_capability in self.capabilities:
                selected_nodes.extend(self.capabilities[matched_capability])
                print(f"🎯 '{requirement}' → {matched_capability} → {len(self.capabilities[matched_capability])} nodes")
            else:
                # フォールバック：部分キーワードマッチング
                for capability, node_ids in self.capabilities.items():
                    capability_keywords = capability.split('_')
                    if any(keyword in req_lower for keyword in capability_keywords):
                        selected_nodes.extend(node_ids)
                        print(f"🔍 '{requirement}' → {capability} (partial) → {len(node_ids)} nodes")
        
        # 重複除去
        unique_nodes = list(set(selected_nodes))
        
        # 優先度ソート（複雑さ、ステージ、継続時間）
        sorted_nodes = sorted(unique_nodes, key=lambda n: (
            self.task_nodes[n]['stage'],
            self.task_nodes[n]['complexity'],
            self.task_nodes[n]['duration_estimate']
        ))
        
        return sorted_nodes
    
    def generate_dependency_order(self, selected_nodes: List[str]) -> List[List[str]]:
        """選択されたノードの依存関係に基づく実行順序を生成"""
        stages = {}
        
        for node_id in selected_nodes:
            node = self.task_nodes[node_id]
            stage = node['stage']
            
            if stage not in stages:
                stages[stage] = []
            stages[stage].append(node_id)
        
        # ステージ順でソート
        ordered_stages = [stages[stage] for stage in sorted(stages.keys())]
        
        return ordered_stages
    
    def save_node_database(self, output_file: str = ".meta/task-nodes.json"):
        """抽出したノードデータベースを保存"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        database = {
            'task_nodes': self.task_nodes,
            'capabilities_index': self.capabilities,
            'extraction_metadata': {
                'total_nodes': len(self.task_nodes),
                'total_capabilities': len(self.capabilities),
                'source_templates': list(set(node['source_template'] for node in self.task_nodes.values()))
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Task node database saved: {output_file}")
        print(f"📊 Total nodes: {len(self.task_nodes)}")
        print(f"🎯 Capabilities: {list(self.capabilities.keys())}")

def main():
    """メイン実行関数"""
    extractor = TaskNodeExtractor()
    
    print("🔍 Extracting task nodes from templates...")
    extractor.extract_all_nodes()
    
    print("💾 Saving task node database...")
    extractor.save_node_database()
    
    # テスト用: マルチメディア要求での選択テスト
    test_requirements = [
        "テキストから画像生成",
        "画像から動画生成", 
        "テキストから音楽生成",
        "動画から音声抽出"
    ]
    
    print(f"\n🧪 Testing node selection for: {test_requirements}")
    selected = extractor.find_nodes_for_requirements(test_requirements)
    execution_order = extractor.generate_dependency_order(selected)
    
    print(f"📋 Selected nodes: {len(selected)}")
    print(f"⚡ Execution stages: {len(execution_order)}")
    
    for i, stage in enumerate(execution_order):
        print(f"  Stage {i+1}: {[extractor.task_nodes[n]['name'] for n in stage]}")

if __name__ == "__main__":
    main()