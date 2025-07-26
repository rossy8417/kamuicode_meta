#!/usr/bin/env python3
"""
Dynamic Workflow Assembler
選択されたタスクノードからGitHub Actionsワークフローを動的生成
"""

import json
import yaml
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
# TaskNodeExtractorクラスを直接組み込み
import re

class DynamicWorkflowAssembler:
    def __init__(self, node_database_path: str = ".meta/task-nodes.json"):
        self.node_database_path = node_database_path
        self.task_nodes = {}
        self.capabilities_index = {}
        self.load_node_database()
        
    def load_node_database(self):
        """ノードデータベースを読み込み"""
        if os.path.exists(self.node_database_path):
            with open(self.node_database_path, 'r', encoding='utf-8') as f:
                database = json.load(f)
                self.task_nodes = database.get('task_nodes', {})
                self.capabilities_index = database.get('capabilities_index', {})
        else:
            print(f"⚠️ Node database not found: {self.node_database_path}")
    
    def create_workflow_from_requirements(self, 
                                        requirements: List[str], 
                                        workflow_name: str = "dynamic-multimedia-workflow",
                                        description: str = "Dynamically generated multimedia workflow") -> Dict[str, Any]:
        """要求からワークフローを動的生成"""
        
        # ノードデータベースから直接選択
        selected_nodes = self.find_nodes_for_requirements(requirements)
        execution_stages = self.generate_dependency_order(selected_nodes)
        
        print(f"🚀 Creating workflow: {workflow_name}")
        print(f"📋 Selected {len(selected_nodes)} task nodes")
        print(f"⚡ {len(execution_stages)} execution stages")
        
        # ワークフロー基本構造
        workflow = {
            'name': workflow_name,
            'on': {
                'workflow_dispatch': {
                    'inputs': {
                        'user_prompt': {
                            'description': 'User requirements for multimedia generation',
                            'required': True,
                            'type': 'string',
                            'default': ' | '.join(requirements)
                        }
                    }
                },
                'issues': {
                    'types': ['opened', 'edited']
                }
            },
            'permissions': {
                'contents': 'write',
                'actions': 'write',
                'issues': 'write',
                'pull-requests': 'write'
            },
            'env': {
                'WORKFLOW_TYPE': 'dynamic-multimedia',
                'GENERATED_AT': '$(date -u +"%Y-%m-%dT%H:%M:%SZ")',
                'REQUIREMENTS': ' | '.join(requirements)
            },
            'jobs': {}
        }
        
        # 各ステージをジョブとして生成
        for stage_idx, stage_nodes in enumerate(execution_stages):
            stage_name = f"stage_{stage_idx + 1}"
            
            # 並列実行可能な場合は複数ジョブ、そうでなければシーケンシャル
            if len(stage_nodes) > 1 and all(self.task_nodes[node_id].get('parallel', False) for node_id in stage_nodes):
                # 並列ジョブ生成
                for node_idx, node_id in enumerate(stage_nodes):
                    job_name = f"{stage_name}_parallel_{node_idx + 1}"
                    workflow['jobs'][job_name] = self.create_job_from_node(node_id, stage_idx)
            else:
                # シーケンシャルジョブ生成
                workflow['jobs'][stage_name] = self.create_combined_job_from_nodes(stage_nodes, stage_idx)
        
        # オートフィックス・モニタリング統合
        workflow['jobs']['autofix_integration'] = self.create_autofix_job()
        workflow['jobs']['monitor_integration'] = self.create_monitor_job()
        
        return workflow
    
    def create_job_from_node(self, node_id: str, stage_idx: int) -> Dict[str, Any]:
        """単一ノードからジョブを生成"""
        node = self.task_nodes[node_id]
        
        job = {
            'runs-on': 'ubuntu-latest',
            'timeout-minutes': node.get('duration_estimate', 10) + 5,  # バッファ追加
            'env': {
                'TASK_NODE_ID': node_id,
                'TASK_NAME': node['name'],
                'STAGE': str(stage_idx + 1),
                'SOURCE_TEMPLATE': node['source_template']
            },
            'steps': [
                {
                    'name': 'Checkout repository',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Setup Claude Code Environment',
                    'run': '''
                        echo "🔧 Setting up Claude Code environment..."
                        mkdir -p .logs outputs artifacts
                        echo "TASK_START_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $GITHUB_ENV
                    '''
                }
            ]
        }
        
        # ノードのジョブを実際のステップに変換
        for job_description in node.get('jobs', []):
            step = self.convert_job_to_step(job_description, node)
            job['steps'].append(step)
        
        # 結果アップロード
        job['steps'].append({
            'name': 'Upload task results',
            'uses': 'actions/upload-artifact@v4',
            'if': 'always()',
            'with': {
                'name': f"task-results-{node_id}",
                'path': 'outputs/',
                'retention-days': 7
            }
        })
        
        return job
    
    def create_combined_job_from_nodes(self, node_ids: List[str], stage_idx: int) -> Dict[str, Any]:
        """複数ノードを統合したジョブを生成"""
        primary_node = self.task_nodes[node_ids[0]]
        
        # 実行時間を合計
        total_duration = sum(self.task_nodes[node_id].get('duration_estimate', 5) for node_id in node_ids)
        
        job = {
            'runs-on': 'ubuntu-latest',
            'timeout-minutes': total_duration + 10,
            'env': {
                'STAGE': str(stage_idx + 1),
                'TASK_NODE_IDS': ','.join(node_ids),
                'TASK_COUNT': len(node_ids)
            },
            'steps': [
                {
                    'name': 'Checkout repository',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Setup Multi-Task Environment',
                    'run': f'''
                        echo "🔧 Setting up multi-task environment for stage {stage_idx + 1}..."
                        mkdir -p .logs outputs artifacts
                        echo "Processing {len(node_ids)} tasks in sequence..."
                        echo "STAGE_START_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $GITHUB_ENV
                    '''
                }
            ]
        }
        
        # 各ノードのジョブを順次実行
        for node_id in node_ids:
            node = self.task_nodes[node_id]
            
            job['steps'].append({
                'name': f"Execute: {node['name']}",
                'run': f'''
                    echo "📝 Starting task: {node['name']}"
                    echo "CURRENT_TASK={node_id}" >> $GITHUB_ENV
                '''
            })
            
            for job_description in node.get('jobs', []):
                step = self.convert_job_to_step(job_description, node)
                job['steps'].append(step)
        
        # ステージ結果アップロード
        job['steps'].append({
            'name': 'Upload stage results',
            'uses': 'actions/upload-artifact@v4',
            'if': 'always()',
            'with': {
                'name': f"stage-{stage_idx + 1}-results",
                'path': 'outputs/',
                'retention-days': 7
            }
        })
        
        return job
    
    def convert_job_to_step(self, job_description: str, node: Dict[str, Any]) -> Dict[str, str]:
        """ジョブ記述を実際のGitHub Actionsステップに変換"""
        
        # MCP サービス検出
        mcp_services = node.get('mcp_services', [])
        capabilities = node.get('capabilities', [])
        
        step_name = job_description[:50] + "..." if len(job_description) > 50 else job_description
        
        # 機能別のコマンド生成
        if 'text_to_image' in capabilities:
            return {
                'name': f"T2I: {step_name}",
                'run': f'''
                    echo "🎨 Executing text-to-image generation..."
                    echo "Job: {job_description}"
                    
                    # MCP サービス使用
                    if [ -n "{','.join(mcp_services)}" ]; then
                        echo "Using MCP services: {','.join(mcp_services)}"
                        claude-code --mcp {mcp_services[0] if mcp_services else 't2i-fal-imagen4-ultra'} \\
                            --prompt "Generate image: ${{{{ inputs.user_prompt || env.REQUIREMENTS }}}}" \\
                            --output "outputs/generated_image_${{{{ github.run_number }}}}.png"
                    else
                        echo "No MCP service available, using external API..."
                        # フォールバック実装
                    fi
                '''
            }
        
        elif 'image_to_video' in capabilities:
            return {
                'name': f"I2V: {step_name}",
                'run': f'''
                    echo "🎬 Executing image-to-video generation..."
                    echo "Job: {job_description}"
                    
                    # 前段階の画像を取得
                    if [ -f "outputs/generated_image_${{{{ github.run_number }}}}.png" ]; then
                        INPUT_IMAGE="outputs/generated_image_${{{{ github.run_number }}}}.png"
                    else
                        INPUT_IMAGE=$(find outputs -name "*.png" -o -name "*.jpg" | head -1)
                    fi
                    
                    if [ -n "$INPUT_IMAGE" ]; then
                        claude-code --mcp {mcp_services[0] if mcp_services else 'i2v-fal-hailuo-02-pro'} \\
                            --input "$INPUT_IMAGE" \\
                            --output "outputs/generated_video_${{{{ github.run_number }}}}.mp4"
                    fi
                '''
            }
        
        elif 'text_to_music' in capabilities:
            return {
                'name': f"T2M: {step_name}",
                'run': f'''
                    echo "🎵 Executing text-to-music generation..."
                    echo "Job: {job_description}"
                    
                    claude-code --mcp {mcp_services[0] if mcp_services else 't2m-google-lyria'} \\
                        --prompt "Generate BGM: ${{{{ inputs.user_prompt || env.REQUIREMENTS }}}}" \\
                        --output "outputs/generated_music_${{{{ github.run_number }}}}.mp3"
                '''
            }
        
        elif 'video_to_audio' in capabilities:
            return {
                'name': f"V2A: {step_name}",
                'run': f'''
                    echo "🔊 Executing video-to-audio extraction..."
                    echo "Job: {job_description}"
                    
                    # 前段階のビデオを取得
                    INPUT_VIDEO=$(find outputs -name "*.mp4" | head -1)
                    
                    if [ -n "$INPUT_VIDEO" ]; then
                        claude-code --mcp {mcp_services[0] if mcp_services else 'v2a-fal-metavoice-v1'} \\
                            --input "$INPUT_VIDEO" \\
                            --output "outputs/extracted_audio_${{{{ github.run_number }}}}.wav"
                    fi
                '''
            }
        
        else:
            # 汎用ステップ
            return {
                'name': f"Execute: {step_name}",
                'run': f'''
                    echo "⚡ Executing general task..."
                    echo "Job: {job_description}"
                    echo "Capabilities: {','.join(capabilities)}"
                    
                    # 汎用実行ロジック
                    mkdir -p "outputs/${{{{ env.CURRENT_TASK || 'general' }}}}"
                    echo "${{{{ github.run_number }}}}" > "outputs/${{{{ env.CURRENT_TASK || 'general' }}}}/execution_id.txt"
                '''
            }
    
    def create_autofix_job(self) -> Dict[str, Any]:
        """AutoFix統合ジョブ"""
        return {
            'needs': [],  # 全ジョブ完了後に実行
            'runs-on': 'ubuntu-latest',
            'if': 'failure()',
            'steps': [
                {
                    'name': 'Trigger AutoFix',
                    'run': '''
                        echo "🔧 Triggering AutoFix system..."
                        # AutoFix システムへの通知
                        echo "AUTOFIX_TRIGGERED=true" >> $GITHUB_ENV
                    '''
                }
            ]
        }
    
    def create_monitor_job(self) -> Dict[str, Any]:
        """Monitor統合ジョブ"""
        return {
            'runs-on': 'ubuntu-latest',
            'if': 'always()',
            'steps': [
                {
                    'name': 'Report to Monitor',
                    'run': '''
                        echo "📊 Reporting to Monitor system..."
                        echo "MONITOR_REPORTED=true" >> $GITHUB_ENV
                    '''
                }
            ]
        }
    
    def save_workflow(self, workflow: Dict[str, Any], output_path: str):
        """生成されたワークフローを保存"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(workflow, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ Dynamic workflow saved: {output_path}")
    
    def find_nodes_for_requirements(self, requirements: List[str]) -> List[str]:
        """要求に基づいて適切なタスクノードを選択"""
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
            'SE': 'video_to_audio'
        }
        
        for requirement in requirements:
            req_lower = requirement.lower()
            
            # 直接マッピングチェック
            matched_capability = None
            for req_key, capability in requirement_mapping.items():
                if req_key.lower() in req_lower:
                    matched_capability = capability
                    break
            
            if matched_capability and matched_capability in self.capabilities_index:
                selected_nodes.extend(self.capabilities_index[matched_capability])
                print(f"🎯 '{requirement}' → {matched_capability} → {len(self.capabilities_index[matched_capability])} nodes")
        
        # 重複除去と優先度ソート
        unique_nodes = list(set(selected_nodes))
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

def main():
    """メイン実行関数"""
    assembler = DynamicWorkflowAssembler()
    
    # テスト要求
    test_requirements = [
        "テキストから画像生成",
        "画像から動画生成", 
        "テキストから音楽生成",
        "動画から音声抽出"
    ]
    
    print("🚀 Creating dynamic multimedia workflow...")
    workflow = assembler.create_workflow_from_requirements(
        requirements=test_requirements,
        workflow_name="dynamic-multimedia-generation",
        description="Dynamically assembled multimedia generation workflow"
    )
    
    # ステージング環境に保存
    output_path = "generated/workflows/staging/dynamic-multimedia-generation.yml"
    assembler.save_workflow(workflow, output_path)
    
    print(f"🎯 Generated workflow with {len(workflow['jobs'])} jobs")
    print(f"📁 Saved to: {output_path}")

if __name__ == "__main__":
    main()