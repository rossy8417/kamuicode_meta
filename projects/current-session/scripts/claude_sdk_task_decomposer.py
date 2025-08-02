#!/usr/bin/env python3
"""
Claude Code SDK Task Decomposer
タスクの意図を理解し、適切なミニマルユニットを選択する
"""

import json
import os
import re
from typing import List, Dict, Tuple

class ClaudeTaskDecomposer:
    """Claude Code SDKを模倣したタスク分解クラス"""
    
    def __init__(self):
        # ミニマルユニットの能力定義
        self.unit_capabilities = {
            'web-search': {
                'path': 'minimal-units/planning/web-search.yml',
                'capabilities': ['情報収集', 'トレンド調査', 'データ取得', 'ニュース検索'],
                'outputs': ['search_results', 'data_json'],
                'time': '3-5 minutes'
            },
            'news-planning': {
                'path': 'minimal-units/planning/news-planning.yml',
                'capabilities': ['ニュース企画', 'コンテンツ構成', 'シナリオ作成'],
                'outputs': ['news_script', 'content_plan'],
                'time': '5-7 minutes'
            },
            'image-generation': {
                'path': 'minimal-units/media/image/t2i-imagen3.yml',
                'capabilities': ['画像生成', 'ビジュアル作成', 'サムネイル生成'],
                'outputs': ['generated_images'],
                'time': '4-6 minutes'
            },
            'video-generation': {
                'path': 'minimal-units/media/video/t2v-veo3.yml',
                'capabilities': ['動画生成', 'ビデオ作成', 'アニメーション'],
                'outputs': ['generated_video'],
                'time': '6-8 minutes'
            },
            'audio-generation': {
                'path': 'minimal-units/media/audio/bgm-generate-mcp.yml',
                'capabilities': ['BGM生成', '音楽作成', 'オーディオ生成'],
                'outputs': ['bgm_audio'],
                'time': '4-5 minutes'
            },
            'text-to-speech': {
                'path': 'minimal-units/media/audio/t2s-minimax-turbo-mcp.yml',
                'capabilities': ['音声合成', 'ナレーション生成', 'テキスト読み上げ'],
                'outputs': ['narration_audio'],
                'time': '3-4 minutes'
            },
            'video-editing': {
                'path': 'minimal-units/postprod/video-concat.yml',
                'capabilities': ['動画編集', '映像結合', 'ポストプロダクション'],
                'outputs': ['final_video'],
                'time': '5-7 minutes'
            }
        }
    
    def analyze_intent(self, issue_title: str, issue_body: str) -> Dict:
        """イシューの意図を分析"""
        intent = {
            'main_goal': '',
            'content_type': '',
            'duration': '',
            'components': []
        }
        
        # タイトルから主要な目的を抽出
        if 'ニュース' in issue_title or 'news' in issue_title.lower():
            intent['main_goal'] = 'news_content'
            intent['components'].append('information_gathering')
            intent['components'].append('content_planning')
        
        if '動画' in issue_title or 'video' in issue_title.lower():
            intent['content_type'] = 'video'
            intent['components'].append('video_creation')
        
        # 本文から詳細な要件を抽出
        body_lower = issue_body.lower()
        
        if 'トレンド' in issue_body or 'trend' in body_lower:
            intent['components'].append('trend_analysis')
        
        if '1分' in issue_body or '60秒' in issue_body:
            intent['duration'] = '60_seconds'
        
        if 'AI' in issue_body or '人工知能' in issue_body:
            intent['components'].append('ai_topic')
        
        return intent
    
    def select_minimal_units(self, intent: Dict) -> List[Dict]:
        """意図に基づいて最適なミニマルユニットを選択"""
        selected_units = []
        added_capabilities = set()
        
        # ニュースコンテンツの場合の標準的なワークフロー
        if intent['main_goal'] == 'news_content':
            # 1. 情報収集
            if 'information_gathering' in intent['components']:
                selected_units.append({
                    'step': 1,
                    'capability': 'web-search',
                    'unit': self.unit_capabilities['web-search'],
                    'reason': 'トレンド情報の収集'
                })
                added_capabilities.add('web-search')
            
            # 2. コンテンツ企画
            if 'content_planning' in intent['components']:
                selected_units.append({
                    'step': 2,
                    'capability': 'news-planning',
                    'unit': self.unit_capabilities['news-planning'],
                    'reason': 'ニュース構成の企画',
                    'depends_on': ['web-search']
                })
                added_capabilities.add('news-planning')
        
        # 動画コンテンツの場合
        if intent['content_type'] == 'video':
            # 3. ビジュアル素材生成
            if 'image-generation' not in added_capabilities:
                selected_units.append({
                    'step': 3,
                    'capability': 'image-generation',
                    'unit': self.unit_capabilities['image-generation'],
                    'reason': 'サムネイルとビジュアル素材の生成',
                    'depends_on': ['news-planning']
                })
                added_capabilities.add('image-generation')
            
            # 4. BGM生成
            if 'audio-generation' not in added_capabilities:
                selected_units.append({
                    'step': 4,
                    'capability': 'audio-generation',
                    'unit': self.unit_capabilities['audio-generation'],
                    'reason': 'バックグラウンド音楽の生成',
                    'parallel_with': ['image-generation']
                })
                added_capabilities.add('audio-generation')
            
            # 5. ナレーション生成
            if 'text-to-speech' not in added_capabilities:
                selected_units.append({
                    'step': 5,
                    'capability': 'text-to-speech',
                    'unit': self.unit_capabilities['text-to-speech'],
                    'reason': 'ニュース原稿の音声化',
                    'depends_on': ['news-planning']
                })
                added_capabilities.add('text-to-speech')
            
            # 6. 動画生成
            if 'video-generation' not in added_capabilities:
                selected_units.append({
                    'step': 6,
                    'capability': 'video-generation',
                    'unit': self.unit_capabilities['video-generation'],
                    'reason': 'メイン動画コンテンツの生成',
                    'depends_on': ['image-generation']
                })
                added_capabilities.add('video-generation')
            
            # 7. 最終編集
            if 'video-editing' not in added_capabilities:
                selected_units.append({
                    'step': 7,
                    'capability': 'video-editing',
                    'unit': self.unit_capabilities['video-editing'],
                    'reason': '全素材の統合と最終編集',
                    'depends_on': ['video-generation', 'audio-generation', 'text-to-speech']
                })
                added_capabilities.add('video-editing')
        
        return selected_units
    
    def generate_workflow_json(self, issue_title: str, issue_body: str, issue_number: str) -> Dict:
        """完全なワークフローJSONを生成"""
        # 意図分析
        intent = self.analyze_intent(issue_title, issue_body)
        
        # ユニット選択
        selected_units = self.select_minimal_units(intent)
        
        # 実行パターンの決定
        has_parallel = any('parallel_with' in unit for unit in selected_units)
        execution_pattern = 'mixed_parallel' if has_parallel else 'sequential'
        
        # ワークフロー構造の生成
        workflow = {
            'metadata': {
                'generated_at': '2025-08-02T04:00:00Z',
                'source_issue': f'#{issue_number}',
                'issue_title': issue_title,
                'intent_analysis': intent,
                'total_units': len(selected_units),
                'execution_pattern': execution_pattern
            },
            'minimal_units': [
                {
                    'capability': unit['capability'],
                    'unit_path': unit['unit']['path'],
                    'estimated_time': unit['unit']['time'],
                    'reason': unit['reason'],
                    'step': unit['step'],
                    'dependencies': unit.get('depends_on', []),
                    'parallel_with': unit.get('parallel_with', [])
                }
                for unit in selected_units
            ],
            'execution_phases': self._group_by_phases(selected_units)
        }
        
        return workflow
    
    def _group_by_phases(self, units: List[Dict]) -> List[Dict]:
        """依存関係に基づいてフェーズにグループ化"""
        phases = []
        processed = set()
        
        # 依存関係のないユニットから開始
        phase_num = 1
        while len(processed) < len(units):
            current_phase = []
            
            for unit in units:
                unit_id = unit['capability']
                if unit_id in processed:
                    continue
                
                # 依存関係をチェック
                deps = unit.get('depends_on', [])
                if all(dep in processed for dep in deps):
                    current_phase.append(unit_id)
            
            if current_phase:
                phases.append({
                    'phase': phase_num,
                    'units': current_phase,
                    'parallel': len(current_phase) > 1
                })
                processed.update(current_phase)
                phase_num += 1
            else:
                # 循環依存を防ぐ
                break
        
        return phases


def main():
    """メイン処理"""
    # 環境変数から入力を取得
    issue_title = os.environ.get('ISSUE_TITLE', '')
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_number = os.environ.get('ISSUE_NUMBER', '60')
    
    # タスク分解実行
    decomposer = ClaudeTaskDecomposer()
    workflow = decomposer.generate_workflow_json(issue_title, issue_body, issue_number)
    
    # 結果を保存
    output_dir = '../metadata'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/claude_sdk_workflow.json', 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Claude SDK Task Decomposition completed")
    print(f"📊 Selected {len(workflow['minimal_units'])} units")
    print(f"🔄 Execution pattern: {workflow['metadata']['execution_pattern']}")
    print(f"📁 Saved to: {output_dir}/claude_sdk_workflow.json")


if __name__ == '__main__':
    main()