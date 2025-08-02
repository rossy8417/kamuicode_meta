#!/usr/bin/env python3
"""
Orchestrator Analyzer for Meta Workflow v10
Claude Code SDKを使用して複合的なオーケストレーター分析を行う
"""

import json
import os
import sys
import re
import yaml
from typing import List, Dict, Tuple, Optional
from datetime import datetime

class OrchestratorAnalyzer:
    def __init__(self):
        self.orchestrator_dir = "kamuicode-workflow/module-workflow"
        self.minimal_units_dir = "minimal-units"
        self.orchestrators = self.load_orchestrators()
        
    def load_orchestrators(self) -> Dict[str, Dict]:
        """すべてのオーケストレーターファイルを読み込む"""
        orchestrators = {}
        pattern = os.path.join(self.orchestrator_dir, "orchestrator-*.yml")
        
        import glob
        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                    name = os.path.basename(file_path).replace('.yml', '')
                    orchestrators[name] = {
                        'path': file_path,
                        'content': content,
                        'jobs': self.extract_jobs(content)
                    }
            except Exception as e:
                print(f"Error loading {file_path}: {e}", file=sys.stderr)
                
        return orchestrators
    
    def extract_jobs(self, content: Dict) -> List[Dict]:
        """オーケストレーターからジョブ情報を抽出"""
        jobs = []
        if 'jobs' in content:
            for job_name, job_config in content['jobs'].items():
                if isinstance(job_config, dict) and 'uses' in job_config:
                    jobs.append({
                        'name': job_name,
                        'uses': job_config['uses'],
                        'needs': job_config.get('needs', []),
                        'with': job_config.get('with', {})
                    })
        return jobs
    
    def analyze_user_request(self, request: str) -> Dict:
        """ユーザー要求を分析して関連オーケストレーターを特定"""
        # キーワード抽出
        keywords = self.extract_keywords(request)
        
        # 関連オーケストレーターの特定
        relevant_orchestrators = []
        for name, orch_data in self.orchestrators.items():
            relevance_score = self.calculate_relevance(name, orch_data, keywords, request)
            if relevance_score > 0.3:
                relevant_orchestrators.append({
                    'name': name,
                    'score': relevance_score,
                    'data': orch_data
                })
        
        # スコア順にソート
        relevant_orchestrators.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'keywords': keywords,
            'orchestrators': relevant_orchestrators,
            'analysis_timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    
    def extract_keywords(self, request: str) -> List[str]:
        """要求文からキーワードを抽出"""
        # 基本的なキーワード抽出（実際はClaude Code SDKで高度な分析を行う）
        keywords = []
        
        # コンテンツタイプ
        if any(word in request.lower() for word in ['動画', 'video', 'ビデオ']):
            keywords.append('video')
        if any(word in request.lower() for word in ['画像', 'image', '写真']):
            keywords.append('image')
        if any(word in request.lower() for word in ['音声', 'audio', '音楽', 'bgm']):
            keywords.append('audio')
        if any(word in request.lower() for word in ['ニュース', 'news']):
            keywords.append('news')
        if any(word in request.lower() for word in ['記事', 'article', 'ブログ']):
            keywords.append('article')
        if any(word in request.lower() for word in ['広告', 'advertisement', 'バナー']):
            keywords.append('advertisement')
        if any(word in request.lower() for word in ['分析', 'analysis', 'データ']):
            keywords.append('analysis')
        
        # アクション
        if any(word in request.lower() for word in ['検索', 'search', '調査']):
            keywords.append('search')
        if any(word in request.lower() for word in ['生成', 'generate', '作成']):
            keywords.append('generation')
        if any(word in request.lower() for word in ['編集', 'edit', '結合']):
            keywords.append('editing')
        
        return list(set(keywords))
    
    def calculate_relevance(self, orch_name: str, orch_data: Dict, keywords: List[str], request: str) -> float:
        """オーケストレーターの関連性スコアを計算"""
        score = 0.0
        
        # 名前によるマッチング
        for keyword in keywords:
            if keyword in orch_name.lower():
                score += 0.3
        
        # 特定のパターンマッチング
        if 'news' in keywords and 'video' in keywords:
            if 'news-video' in orch_name:
                score += 0.5
            elif 'news-article' in orch_name:
                score += 0.3
        
        if 'banner' in keywords or 'advertisement' in keywords:
            if 'banner-advertisement' in orch_name:
                score += 0.6
        
        # ジョブ内容による追加スコア
        job_names = [job['name'] for job in orch_data['jobs']]
        for job_name in job_names:
            for keyword in keywords:
                if keyword in job_name.lower():
                    score += 0.1
        
        return min(score, 1.0)
    
    def merge_orchestrator_patterns(self, orchestrators: List[Dict], request: str) -> Dict:
        """複数のオーケストレーターから最適なワークフローを構築"""
        all_jobs = []
        job_map = {}
        
        # すべてのジョブを収集
        for orch in orchestrators:
            for job in orch['data']['jobs']:
                job_key = job['uses']
                if job_key not in job_map:
                    job_map[job_key] = {
                        'job': job,
                        'source': orch['name'],
                        'relevance': orch['score']
                    }
                else:
                    # より関連性の高いものを選択
                    if orch['score'] > job_map[job_key]['relevance']:
                        job_map[job_key] = {
                            'job': job,
                            'source': orch['name'],
                            'relevance': orch['score']
                        }
        
        # 論理的な順序で並べ替え
        ordered_jobs = self.create_logical_order(job_map, request)
        
        return {
            'jobs': ordered_jobs,
            'sources': list(set([v['source'] for v in job_map.values()])),
            'job_count': len(ordered_jobs)
        }
    
    def create_logical_order(self, job_map: Dict, request: str) -> List[Dict]:
        """ジョブを論理的な順序に並べ替え"""
        # ジョブタイプの分類
        categories = {
            'planning': [],
            'search': [],
            'analysis': [],
            'content_creation': [],
            'media_generation': [],
            'post_processing': [],
            'finalization': []
        }
        
        for job_key, job_data in job_map.items():
            job_name = job_data['job']['name']
            uses = job_data['job']['uses']
            
            # カテゴリ分け
            if any(word in job_name.lower() for word in ['planning', 'plan', '企画']):
                categories['planning'].append(job_data)
            elif any(word in job_name.lower() for word in ['search', 'web', '検索']):
                categories['search'].append(job_data)
            elif any(word in job_name.lower() for word in ['analysis', 'analyze', '分析']):
                categories['analysis'].append(job_data)
            elif any(word in job_name.lower() for word in ['article', 'content', 'text']):
                categories['content_creation'].append(job_data)
            elif any(word in uses.lower() for word in ['image', 'video', 'audio', 'banner']):
                categories['media_generation'].append(job_data)
            elif any(word in job_name.lower() for word in ['lipsync', 'edit', 'concat', 'overlay']):
                categories['post_processing'].append(job_data)
            else:
                categories['finalization'].append(job_data)
        
        # 論理的な順序で結合
        ordered_jobs = []
        for category in ['search', 'analysis', 'planning', 'content_creation', 
                        'media_generation', 'post_processing', 'finalization']:
            ordered_jobs.extend(categories[category])
        
        return ordered_jobs
    
    def generate_execution_plan(self, request: str) -> Dict:
        """実行計画を生成"""
        # ユーザー要求を分析
        analysis = self.analyze_user_request(request)
        
        if not analysis['orchestrators']:
            # オーケストレーターが見つからない場合は基本パターンを使用
            return self.create_default_execution_plan(request, analysis['keywords'])
        
        # 複数のオーケストレーターを統合
        merged_workflow = self.merge_orchestrator_patterns(
            analysis['orchestrators'], 
            request
        )
        
        # 依存関係の解析と並列実行の最適化
        optimized_workflow = self.optimize_parallel_execution(merged_workflow)
        
        return {
            'request': request,
            'analysis': analysis,
            'workflow': optimized_workflow,
            'execution_pattern': self.determine_execution_pattern(optimized_workflow)
        }
    
    def create_default_execution_plan(self, request: str, keywords: List[str]) -> Dict:
        """デフォルトの実行計画を作成"""
        # 専門家視点での基本的な実行順序
        default_plan = {
            'jobs': [],
            'sources': ['expert_knowledge'],
            'execution_pattern': 'sequential'
        }
        
        # キーワードに基づいて基本的なジョブを追加
        if 'search' in keywords:
            default_plan['jobs'].append({
                'name': 'web_search',
                'category': 'search',
                'unit': 'minimal-units/planning/web-search.yml'
            })
        
        if 'analysis' in keywords:
            default_plan['jobs'].append({
                'name': 'data_analysis',
                'category': 'analysis',
                'unit': 'minimal-units/planning/data-analysis.yml'
            })
        
        # ... 他のキーワードに基づくジョブ追加
        
        return default_plan
    
    def optimize_parallel_execution(self, workflow: Dict) -> Dict:
        """並列実行の最適化"""
        # 依存関係を分析して並列実行可能なジョブグループを特定
        # （実装は省略 - 実際にはより複雑な依存関係解析が必要）
        workflow['parallel_groups'] = []
        return workflow
    
    def determine_execution_pattern(self, workflow: Dict) -> str:
        """実行パターンを決定"""
        job_count = len(workflow.get('jobs', []))
        if job_count <= 3:
            return 'sequential'
        elif job_count <= 6:
            return 'mixed_parallel'
        else:
            return 'complex_parallel'


# メイン処理
if __name__ == "__main__":
    # 環境変数から情報を取得
    request = os.environ.get('USER_REQUEST', '')
    capabilities = os.environ.get('CAPABILITIES', '')
    
    if not request:
        print("Error: USER_REQUEST not provided", file=sys.stderr)
        sys.exit(1)
    
    # アナライザーを初期化
    analyzer = OrchestratorAnalyzer()
    
    # 実行計画を生成
    execution_plan = analyzer.generate_execution_plan(request)
    
    # 結果を出力
    output_dir = "projects/current-session/metadata"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "orchestrator_analysis.json"), 'w', encoding='utf-8') as f:
        json.dump(execution_plan, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Orchestrator analysis completed")
    print(f"📁 Results saved to: {output_dir}/orchestrator_analysis.json")