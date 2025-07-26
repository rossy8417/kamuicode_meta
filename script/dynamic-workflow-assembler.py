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
    
    def create_workflow_from_requirements_enhanced(self, 
                                                 requirements: List[str], 
                                                 enhanced_context: dict = None,
                                                 workflow_name: str = "dynamic-enhanced-workflow",
                                                 description: str = "Enhanced dynamically generated workflow") -> Dict[str, Any]:
        """強化されたコンテクストを使用してワークフローを動的生成"""
        
        print(f"🚀 Creating enhanced workflow: {workflow_name}")
        if enhanced_context:
            clarity_score = enhanced_context.get('clarity_score', 7)
            print(f"📊 Enhanced context: clarity={clarity_score}/10")
        
        # 強化されたコンテクストでノード選択
        selected_nodes = self.find_nodes_for_requirements(requirements, enhanced_context)
        execution_stages = self.generate_dependency_order(selected_nodes)
        
        print(f"📋 Selected {len(selected_nodes)} task nodes")
        print(f"⚡ {len(execution_stages)} execution stages")
        
        # ワークフロー基本構造（既存と同じ）
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
                'WORKFLOW_TYPE': 'dynamic-enhanced',
                'GENERATED_AT': '$(date -u +"%Y-%m-%dT%H:%M:%SZ")',
                'REQUIREMENTS': ' | '.join(requirements),
                'CLARITY_SCORE': str(enhanced_context.get('clarity_score', 7) if enhanced_context else 7)
            },
            'jobs': {}
        }
        
        # 各ステージをジョブとして生成（既存ロジック使用）
        for stage_idx, stage_nodes in enumerate(execution_stages):
            stage_name = f"stage_{stage_idx + 1}"
            
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
                    MCP_SERVICE="{mcp_services[0] if mcp_services else 't2i-fal-imagen4-ultra'}"
                    echo "Using MCP service: $MCP_SERVICE"
                    
                    # Claude Code + MCP で画像生成
                    claude --continue "テキストから画像を生成してください: ${{{{ inputs.user_prompt || env.REQUIREMENTS }}}}" \\
                        --mcp "$MCP_SERVICE" \\
                        --output-format json > outputs/image_generation_result.json
                    
                    # 生成結果から画像パスを抽出
                    IMAGE_PATH=$(jq -r '.image_url // .file_path // "none"' outputs/image_generation_result.json 2>/dev/null)
                    
                    if [ "$IMAGE_PATH" != "none" ]; then
                        echo "✅ Image generated: $IMAGE_PATH"
                        echo "$IMAGE_PATH" > outputs/generated_image_path.txt
                        echo "IMAGE_PATH=$IMAGE_PATH" >> $GITHUB_ENV
                    else
                        echo "❌ Image generation failed"
                        exit 1
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
    
    def find_nodes_for_requirements(self, requirements: List[str], enhanced_context: dict = None) -> List[str]:
        """要求に基づいて適切なタスクノードを選択（強化されたコンテクスト対応）"""
        selected_nodes = []
        
        # 強化されたコンテキストを考慮
        clarity_score = 7
        fallback_assumptions = []
        if enhanced_context:
            clarity_score = enhanced_context.get('clarity_score', 7)
            fallback_assumptions = enhanced_context.get('fallback_assumptions', [])
            print(f"📊 Using enhanced context: clarity={clarity_score}/10, assumptions={len(fallback_assumptions)}")
        
        # 論理フロー重視の要求分析マッピング
        requirement_flow_mapping = [
            # Stage 1: テキスト処理・画像生成
            (['テキストから画像', '画像生成', 'text.*image', 'テキスト.*画像'], 'text_to_image', 1),
            
            # Stage 2: 画像から動画生成  
            (['画像から動画', '動画生成', 'image.*video', '画像.*動画'], 'image_to_video', 2),
            
            # Stage 3: 音楽・オーディオ生成（並行可能）
            (['テキストから音楽', '音楽生成', 'BGM', 'text.*music', 'テキスト.*音楽'], 'text_to_music', 3),
            
            # Stage 4: 動画から音声抽出
            (['動画から音声', '音声抽出', 'video.*audio', '動画.*音声', 'ナレーション', 'セリフ'], 'video_to_audio', 4)
        ]
        
        # 要求を論理フロー順に分析
        matched_stages = {}
        
        for requirement in requirements:
            req_lower = requirement.lower()
            
            for keywords, capability, stage in requirement_flow_mapping:
                for keyword in keywords:
                    if keyword.lower() in req_lower or (len(keyword.split('.*')) == 2 and 
                        all(part in req_lower for part in keyword.split('.*'))):
                        
                        if stage not in matched_stages:
                            matched_stages[stage] = []
                        
                        if capability in self.capabilities_index:
                            stage_nodes = self.capabilities_index[capability]
                            matched_stages[stage].extend(stage_nodes)
                            print(f"🎯 Stage {stage}: '{requirement}' → {capability} → {len(stage_nodes)} nodes")
                        break
        
        # 論理フロー順（stage順）でノードを選択
        for stage in sorted(matched_stages.keys()):
            stage_nodes = list(set(matched_stages[stage]))  # 重複除去
            
            # 明確度が低い場合は安全なノードのみ選択
            if clarity_score < 6:
                # 複雑度の低いノードを優先
                stage_nodes = sorted(stage_nodes, key=lambda n: (
                    self.task_nodes[n]['complexity'],
                    self.task_nodes[n]['duration_estimate']
                ))[:3]  # 最大3ノードに制限
                print(f"⚠️ Low clarity: limiting stage {stage} to {len(stage_nodes)} safe nodes")
            
            selected_nodes.extend(stage_nodes)
        
        # フォールバック仮定に基づく追加ノード選択
        if fallback_assumptions and len(selected_nodes) < 5:
            print("🔧 Applying fallback assumptions for node enhancement...")
            for assumption in fallback_assumptions:
                if '標準品質' in assumption and 'text_to_image' in self.capabilities_index:
                    additional_nodes = self.capabilities_index['text_to_image'][:2]
                    selected_nodes.extend(additional_nodes)
                    print(f"🎯 Fallback: Added {len(additional_nodes)} standard quality nodes")
        
        # 最終的な重複除去と優先度ソート
        unique_nodes = list(set(selected_nodes))
        sorted_nodes = sorted(unique_nodes, key=lambda n: (
            self.task_nodes[n]['stage'],
            self.task_nodes[n]['complexity'],
            self.task_nodes[n]['duration_estimate']
        ))
        
        print(f"✅ Selected {len(sorted_nodes)} nodes across {len(matched_stages)} stages")
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
    """メイン実行関数（環境変数からコンテクストを読み込み）"""
    import os
    import json
    
    assembler = DynamicWorkflowAssembler()
    
    # 環境変数から強化コンテクストを読み込み
    enhanced_context_file = os.getenv('ENHANCED_CONTEXT_FILE')
    workflow_type = os.getenv('WORKFLOW_TYPE', 'custom')
    
    enhanced_context = {}
    if enhanced_context_file and os.path.exists(enhanced_context_file):
        try:
            with open(enhanced_context_file, 'r', encoding='utf-8') as f:
                enhanced_context = json.load(f)
            print(f"✅ Loaded enhanced context from {enhanced_context_file}")
            print(f"📊 Clarity Score: {enhanced_context.get('clarity_score', 'N/A')}/10")
        except Exception as e:
            print(f"⚠️ Failed to load enhanced context: {e}")
    
    # ワークフロータイプに基づく要求設定
    if workflow_type == "custom":
        # デフォルト要求（テスト用）
        requirements = [
            "テキストから画像生成",
            "画像から動画生成", 
            "テキストから音楽生成",
            "動画から音声抽出"
        ]
    else:
        # ワークフロータイプ別の要求マッピング
        type_mapping = {
            "image-generation": ["テキストから画像生成", "画像品質向上"],
            "video-generation": ["テキストから画像生成", "画像から動画生成"],
            "audio-generation": ["テキストから音楽生成", "音声品質向上"],
            "news-article": ["ニュース分析", "記事生成"],
            "news-video": ["ニュース分析", "画像生成", "動画生成"],
            "social-integration": ["コンテンツ生成", "SNS最適化"]
        }
        requirements = type_mapping.get(workflow_type, ["基本ワークフロー生成"])
    
    print(f"🚀 Creating dynamic {workflow_type} workflow...")
    print(f"📋 Requirements: {', '.join(requirements)}")
    
    # 強化されたコンテクストでワークフロー生成
    workflow = assembler.create_workflow_from_requirements_enhanced(
        requirements=requirements,
        enhanced_context=enhanced_context,
        workflow_name=f"dynamic-{workflow_type}-generation",
        description=f"Dynamically assembled {workflow_type} workflow with enhanced context"
    )
    
    # ステージング環境に保存
    output_path = f"generated/workflows/staging/dynamic-{workflow_type}-generation.yml"
    assembler.save_workflow(workflow, output_path)
    
    print(f"🎯 Generated workflow with {len(workflow['jobs'])} jobs")
    print(f"📁 Saved to: {output_path}")
    
    # 使用したノード数を出力（GitHub Actionsで解析用）
    if 'jobs' in workflow:
        job_count = len([job for job_name, job in workflow['jobs'].items() 
                        if not job_name.startswith(('autofix', 'monitor'))])
        print(f"Selected {job_count} task nodes")

if __name__ == "__main__":
    main()