#!/usr/bin/env python3
"""
Optimized Workflow Generator for Meta Workflow v10
オーケストレーター分析結果を基に最適化されたワークフローを生成
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Tuple

def load_orchestrator_analysis():
    """オーケストレーター分析結果を読み込む"""
    analysis_path = "../metadata/orchestrator_analysis.json"
    if os.path.exists(analysis_path):
        with open(analysis_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_capabilities():
    """検出された能力を読み込む"""
    capabilities = os.environ.get('CAPABILITIES', '').strip(',')
    if capabilities:
        return capabilities.split(',')
    return []

def create_logical_job_order(capabilities: List[str], orchestrator_analysis: Dict = None) -> List[Dict]:
    """論理的なジョブ順序を作成"""
    
    # 基本的なユニットマッピング
    unit_mapping = {
        'web-search': {
            'path': 'minimal-units/planning/web-search.yml',
            'category': 'research',
            'priority': 1
        },
        'data-analysis': {
            'path': 'minimal-units/planning/data-analysis.yml',
            'category': 'research',
            'priority': 2
        },
        'planning': {
            'path': 'minimal-units/planning/planning-ccsdk.yml',
            'category': 'planning',
            'priority': 3
        },
        'content-planning': {
            'path': 'minimal-units/planning/content-planning.yml',
            'category': 'planning',
            'priority': 3.1
        },
        'narration-creation': { 
            'path': 'minimal-units/planning/narration-creation.yml',
            'category': 'planning',
            'priority': 3.2
        },
        'scene-composition': {
            'path': 'minimal-units/planning/scene-composition.yml',
            'category': 'planning', 
            'priority': 3.3
        },
        'image-generation': {
            'path': 'minimal-units/media/image/t2i-imagen3.yml',
            'category': 'media_generation',
            'priority': 5
        },
        'audio-generation': {
            'path': 'minimal-units/media/audio/bgm-generate-mcp.yml',
            'category': 'media_generation',
            'priority': 5
        },
        'text-to-speech': {
            'path': 'minimal-units/media/audio/t2s-minimax-turbo-mcp.yml',
            'category': 'media_generation',
            'priority': 6
        },
        'video-generation': {
            'path': 'minimal-units/media/video/t2v-veo3.yml',
            'category': 'media_generation',
            'priority': 7
        },
        'video-editing': {
            'path': 'minimal-units/postprod/video-concat.yml',
            'category': 'post_processing',
            'priority': 8
        },
        # External APIs
        'youtube-upload': {
            'path': 'minimal-units/external/youtube-upload.yml',
            'category': 'external_api',
            'priority': 9
        },
        'youtube-info': {
            'path': 'minimal-units/external/youtube-video-info.yml',
            'category': 'external_api',
            'priority': 2
        },
        'newsapi': {
            'path': 'minimal-units/external/newsapi-fetch.yml',
            'category': 'external_api',
            'priority': 1
        },
        'weather': {
            'path': 'minimal-units/external/weather-fetch.yml',
            'category': 'external_api',
            'priority': 1
        },
        'openai-summarize': {
            'path': 'minimal-units/external/openai-summarize.yml',
            'category': 'external_api',
            'priority': 4
        },
        'openai-translate': {
            'path': 'minimal-units/external/openai-translate.yml',
            'category': 'external_api',
            'priority': 4
        },
        'openai-image': {
            'path': 'minimal-units/external/openai-image-gen.yml',
            'category': 'external_api',
            'priority': 5
        },
        'slack-notify': {
            'path': 'minimal-units/external/slack-notify.yml',
            'category': 'external_api',
            'priority': 9
        },
        'twitter-post': {
            'path': 'minimal-units/external/twitter-post.yml',
            'category': 'external_api',
            'priority': 9
        },
        'google-sheets-read': {
            'path': 'minimal-units/external/google-sheets-read.yml',
            'category': 'external_api',
            'priority': 1
        },
        'google-sheets-write': {
            'path': 'minimal-units/external/google-sheets-write.yml',
            'category': 'external_api',
            'priority': 9
        }
    }
    
    jobs = []
    
    # オーケストレーター分析結果がある場合
    if orchestrator_analysis and 'workflow' in orchestrator_analysis:
        orch_jobs = orchestrator_analysis['workflow'].get('jobs', [])
        
        # オーケストレーターのジョブ順序を参考に
        for idx, orch_job in enumerate(orch_jobs):
            # 対応する能力を見つける
            for cap in capabilities:
                if cap in orch_job.get('name', '').lower() or cap in orch_job.get('category', '').lower():
                    if cap in unit_mapping:
                        jobs.append({
                            'capability': cap,
                            'unit_path': unit_mapping[cap]['path'],
                            'category': unit_mapping[cap]['category'],
                            'priority': idx + 1,  # オーケストレーターの順序を優先
                            'estimated_time': '3-5 minutes'
                        })
                        break
    
    # オーケストレーター分析がない場合、または不足している能力がある場合
    existing_caps = set([job['capability'] for job in jobs])
    missing_caps = set(capabilities) - existing_caps
    
    for cap in missing_caps:
        if cap in unit_mapping:
            jobs.append({
                'capability': cap,
                'unit_path': unit_mapping[cap]['path'],
                'category': unit_mapping[cap]['category'],
                'priority': unit_mapping[cap]['priority'],
                'estimated_time': '3-5 minutes'
            })
    
    # 優先度順にソート
    jobs.sort(key=lambda x: x['priority'])
    
    return jobs

def determine_execution_pattern(jobs: List[Dict]) -> Dict:
    """実行パターンを決定（依存関係と並列実行の最適化）"""
    
    # カテゴリごとにグループ化
    categories = {}
    for job in jobs:
        cat = job['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(job)
    
    # 実行フェーズを作成
    phases = []
    
    # フェーズ1: 調査・分析（順次実行）
    if 'research' in categories:
        phases.append({
            'name': 'research_phase',
            'jobs': categories['research'],
            'parallel': False
        })
    
    # フェーズ2: 企画・計画（順次実行）
    if 'planning' in categories:
        phases.append({
            'name': 'planning_phase',
            'jobs': categories['planning'],
            'parallel': False
        })
    
    # フェーズ3: メディア生成（並列実行可能）
    if 'media_generation' in categories:
        media_jobs = categories['media_generation']
        
        # 画像、BGM、テキスト音声は並列実行可能
        parallel_jobs = [j for j in media_jobs if j['capability'] in ['image-generation', 'audio-generation', 'text-to-speech']]
        sequential_jobs = [j for j in media_jobs if j['capability'] not in ['image-generation', 'audio-generation', 'text-to-speech']]
        
        if parallel_jobs:
            phases.append({
                'name': 'media_generation_parallel',
                'jobs': parallel_jobs,
                'parallel': True
            })
        
        if sequential_jobs:
            phases.append({
                'name': 'media_generation_sequential',
                'jobs': sequential_jobs,
                'parallel': False
            })
    
    # フェーズ4: 後処理（順次実行）
    if 'post_processing' in categories:
        phases.append({
            'name': 'post_processing_phase',
            'jobs': categories['post_processing'],
            'parallel': False
        })
    
    # フェーズ5: 外部API（並列/順次混合）
    if 'external_api' in categories:
        api_jobs = categories['external_api']
        
        # 入力系API（並列実行可能）
        input_apis = [j for j in api_jobs if j['capability'] in ['newsapi', 'weather', 'youtube-info', 'google-sheets-read']]
        # 処理系API（順次実行）
        process_apis = [j for j in api_jobs if j['capability'] in ['openai-summarize', 'openai-translate', 'openai-image']]
        # 出力系API（並列実行可能）
        output_apis = [j for j in api_jobs if j['capability'] in ['youtube-upload', 'slack-notify', 'twitter-post', 'google-sheets-write']]
        
        if input_apis:
            phases.append({
                'name': 'external_api_input',
                'jobs': input_apis,
                'parallel': True
            })
        
        if process_apis:
            phases.append({
                'name': 'external_api_process',
                'jobs': process_apis,
                'parallel': False
            })
        
        if output_apis:
            phases.append({
                'name': 'external_api_output',
                'jobs': output_apis,
                'parallel': True
            })
    
    # 実行パターンを決定
    total_jobs = len(jobs)
    has_parallel = any(phase['parallel'] for phase in phases)
    
    if total_jobs <= 3:
        pattern = 'sequential'
    elif has_parallel:
        pattern = 'mixed_parallel'
    else:
        pattern = 'sequential'
    
    return {
        'pattern': pattern,
        'phases': phases,
        'total_phases': len(phases)
    }

def generate_workflow_json(capabilities: List[str], orchestrator_analysis: Dict = None) -> Dict:
    """最適化されたワークフローJSONを生成"""
    
    # 論理的なジョブ順序を作成
    jobs = create_logical_job_order(capabilities, orchestrator_analysis)
    
    # 実行パターンを決定
    execution_info = determine_execution_pattern(jobs)
    
    # 複雑さの判定
    job_count = len(jobs)
    if job_count <= 3:
        complexity = 'simple'
    elif job_count <= 6:
        complexity = 'medium'
    else:
        complexity = 'complex'
    
    workflow = {
        'metadata': {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'complexity': complexity,
            'total_units': len(jobs),
            'capabilities_detected': capabilities,
            'orchestrator_used': bool(orchestrator_analysis),
            'execution_pattern': execution_info['pattern'],
            'execution_phases': execution_info['phases']
        },
        'minimal_units': jobs,
        'execution_pattern': execution_info['pattern']
    }
    
    return workflow

if __name__ == "__main__":
    # 環境変数から情報を取得
    capabilities = load_capabilities()
    
    if not capabilities:
        print("Warning: No capabilities detected", file=sys.stderr)
        capabilities = []
    
    print(f"Debug - Capabilities: {capabilities}")
    
    # オーケストレーター分析結果を読み込む
    orchestrator_analysis = load_orchestrator_analysis()
    
    if orchestrator_analysis:
        print("✅ Using orchestrator analysis for optimization")
        sources = orchestrator_analysis.get('analysis', {}).get('orchestrators', [])
        if sources:
            print(f"📚 Reference orchestrators: {[s['name'] for s in sources[:3]]}")
    else:
        print("ℹ️ No orchestrator analysis found, using expert logic")
    
    # ワークフローを生成
    workflow = generate_workflow_json(capabilities, orchestrator_analysis)
    
    # 結果を保存
    os.makedirs('../metadata', exist_ok=True)
    with open('../metadata/dynamic_workflow.json', 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Optimized workflow generated with {len(workflow['minimal_units'])} units")
    print(f"📊 Execution pattern: {workflow['execution_pattern']}")
    print(f"📁 Saved to: ../metadata/dynamic_workflow.json")