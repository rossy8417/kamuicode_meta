#!/usr/bin/env python3
"""
Domain Template Loader
GitHub Actions文字数制限を考慮したテンプレート読み込みシステム
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# GitHub Actionsのステップあたりの文字数制限
MAX_CHARS_PER_STEP = 21000
# 安全マージン（YAMLシンタックスやエスケープ文字のため）
SAFETY_MARGIN = 2000
EFFECTIVE_LIMIT = MAX_CHARS_PER_STEP - SAFETY_MARGIN

class DomainTemplateLoader:
    def __init__(self, templates_dir: str = "meta/domain-templates"):
        self.templates_dir = Path(templates_dir)
        self.index_path = self.templates_dir / "index.yaml"
        self.index_data = self._load_index()
    
    def _load_index(self) -> Dict[str, Any]:
        """インデックスファイルを読み込む"""
        with open(self.index_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def detect_domain(self, issue_content: str) -> List[str]:
        """イシュー内容から関連ドメインを検出"""
        detected_domains = []
        issue_lower = issue_content.lower()
        
        # 単一ドメイン検出
        for rule in self.index_data['detection_rules']:
            keywords = rule['if_contains']
            if any(keyword.lower() in issue_lower for keyword in keywords):
                detected_domains.append({
                    'domain': rule['then_domain'],
                    'confidence': rule['confidence']
                })
        
        # 複合ドメイン検出
        for pattern in self.index_data['multi_domain_patterns']:
            keywords = pattern['pattern']
            if all(keyword.lower() in issue_lower for keyword in keywords):
                priority = pattern.get('priority', 0.8)
                for domain in pattern['domains']:
                    # 既存のドメインがある場合は信頼度を更新
                    existing = next((d for d in detected_domains if d['domain'] == domain), None)
                    if existing:
                        existing['confidence'] = max(existing['confidence'], priority)
                    else:
                        detected_domains.append({
                            'domain': domain,
                            'confidence': priority
                        })
        
        # 信頼度でソート
        detected_domains.sort(key=lambda x: x['confidence'], reverse=True)
        
        return detected_domains
    
    def load_template_chunk(self, domain: str, chunk_type: str, section: Optional[str] = None) -> Dict[str, Any]:
        """テンプレートの特定チャンクを読み込む"""
        domain_path = self.templates_dir / domain
        
        if chunk_type == "constraints":
            file_path = domain_path / "constraints.yaml"
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            # セクションが指定されている場合は特定部分のみ返す
            if section:
                return data.get(section, {})
            return data
            
        elif chunk_type == "input_schema":
            file_path = domain_path / "input-schema.yaml"
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if section:
                return data.get(section, {})
            return data
            
        elif chunk_type == "readme":
            file_path = domain_path / "README.md"
            with open(file_path, 'r', encoding='utf-8') as f:
                return {"content": f.read()}
        
        elif chunk_type == "expert-knowledge":
            file_path = domain_path / "expert-knowledge.yaml"
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if section:
                return data.get(section, {})
            return data
        
        elif chunk_type == "workflow-patterns":
            file_path = domain_path / "workflow-patterns.yaml"
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if section:
                return data.get(section, {})
            return data
        
        else:
            raise ValueError(f"Unknown chunk type: {chunk_type}")
    
    def split_template_data(self, domain: str) -> List[Dict[str, Any]]:
        """テンプレートデータを文字数制限に収まるチャンクに分割"""
        chunks = []
        
        # 1. READMEは独立したチャンク
        readme_data = self.load_template_chunk(domain, "readme")
        chunks.append({
            "id": f"{domain}_readme",
            "type": "readme",
            "size": len(json.dumps(readme_data)),
            "data": readme_data
        })
        
        # 2. Constraintsを主要セクションごとに分割
        constraints = self.load_template_chunk(domain, "constraints")
        for section_name, section_data in constraints.items():
            section_json = json.dumps({section_name: section_data}, ensure_ascii=False)
            if len(section_json) > EFFECTIVE_LIMIT:
                # さらに細かく分割が必要
                sub_chunks = self._split_large_section(section_name, section_data, domain, "constraints")
                chunks.extend(sub_chunks)
            else:
                chunks.append({
                    "id": f"{domain}_constraints_{section_name}",
                    "type": "constraints",
                    "section": section_name,
                    "size": len(section_json),
                    "data": {section_name: section_data}
                })
        
        # 3. Input Schemaも同様に分割
        input_schema = self.load_template_chunk(domain, "input_schema")
        for section_name, section_data in input_schema.items():
            section_json = json.dumps({section_name: section_data}, ensure_ascii=False)
            if len(section_json) > EFFECTIVE_LIMIT:
                sub_chunks = self._split_large_section(section_name, section_data, domain, "input_schema")
                chunks.extend(sub_chunks)
            else:
                chunks.append({
                    "id": f"{domain}_input_schema_{section_name}",
                    "type": "input_schema",
                    "section": section_name,
                    "size": len(section_json),
                    "data": {section_name: section_data}
                })
        
        return chunks
    
    def _split_large_section(self, section_name: str, section_data: Any, domain: str, data_type: str) -> List[Dict[str, Any]]:
        """大きなセクションをさらに細かく分割"""
        sub_chunks = []
        
        if isinstance(section_data, dict):
            # 辞書の場合はキーごとに分割
            current_chunk = {}
            current_size = 0
            chunk_index = 0
            
            for key, value in section_data.items():
                item_json = json.dumps({key: value}, ensure_ascii=False)
                item_size = len(item_json)
                
                if current_size + item_size > EFFECTIVE_LIMIT:
                    # 現在のチャンクを保存
                    if current_chunk:
                        sub_chunks.append({
                            "id": f"{domain}_{data_type}_{section_name}_part{chunk_index}",
                            "type": data_type,
                            "section": section_name,
                            "part": chunk_index,
                            "size": current_size,
                            "data": {section_name: current_chunk}
                        })
                        chunk_index += 1
                    
                    current_chunk = {key: value}
                    current_size = item_size
                else:
                    current_chunk[key] = value
                    current_size += item_size
            
            # 最後のチャンクを保存
            if current_chunk:
                sub_chunks.append({
                    "id": f"{domain}_{data_type}_{section_name}_part{chunk_index}",
                    "type": data_type,
                    "section": section_name,
                    "part": chunk_index,
                    "size": current_size,
                    "data": {section_name: current_chunk}
                })
        
        elif isinstance(section_data, list):
            # リストの場合は要素ごとに分割
            current_chunk = []
            current_size = 0
            chunk_index = 0
            
            for item in section_data:
                item_json = json.dumps(item, ensure_ascii=False)
                item_size = len(item_json)
                
                if current_size + item_size > EFFECTIVE_LIMIT:
                    if current_chunk:
                        sub_chunks.append({
                            "id": f"{domain}_{data_type}_{section_name}_part{chunk_index}",
                            "type": data_type,
                            "section": section_name,
                            "part": chunk_index,
                            "size": current_size,
                            "data": {section_name: current_chunk}
                        })
                        chunk_index += 1
                    
                    current_chunk = [item]
                    current_size = item_size
                else:
                    current_chunk.append(item)
                    current_size += item_size
            
            if current_chunk:
                sub_chunks.append({
                    "id": f"{domain}_{data_type}_{section_name}_part{chunk_index}",
                    "type": data_type,
                    "section": section_name,
                    "part": chunk_index,
                    "size": current_size,
                    "data": {section_name: current_chunk}
                })
        
        return sub_chunks
    
    def get_domain_summary(self, domain: str) -> Dict[str, Any]:
        """ドメインの要約情報を取得"""
        domain_info = self.index_data['domains'].get(domain, {})
        
        # 基本情報
        summary = {
            "domain": domain,
            "name": domain_info.get('name', ''),
            "expert": domain_info.get('expert', ''),
            "keywords": domain_info.get('keywords', []),
            "minimal_units": domain_info.get('minimal_units', []),
            "file_sizes": domain_info.get('file_size', {})
        }
        
        # 主要な制約を抽出
        try:
            constraints = self.load_template_chunk(domain, "constraints")
            summary["key_constraints"] = self._extract_key_constraints(constraints)
        except:
            summary["key_constraints"] = {}
        
        return summary
    
    def _extract_key_constraints(self, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """制約から重要な情報を抽出"""
        key_info = {}
        
        # 各ドメイン特有の重要情報を抽出
        for section_name, section_data in constraints.items():
            if isinstance(section_data, dict):
                # 数値的な制約を探す
                for key, value in section_data.items():
                    if any(keyword in key.lower() for keyword in ['limit', 'max', 'min', 'target', 'threshold']):
                        key_info[f"{section_name}.{key}"] = value
        
        return key_info
    
    def get_domain_summary_for_task_decomposition(self, domain: str) -> Dict[str, Any]:
        """タスク分解用に詳細な情報を保持したドメインサマリーを取得"""
        
        # 各YAMLファイルから完全な情報を読み込み
        constraints = self.load_template_chunk(domain, "constraints")
        expert_knowledge = self.load_template_chunk(domain, "expert-knowledge")
        workflow_patterns = self.load_template_chunk(domain, "workflow-patterns")
        
        # ドメイン情報の取得
        domain_info = self.index_data['domains'].get(domain, {})
        
        return {
            # ドメイン基本情報
            "domain_info": {
                "domain": domain,
                "name": domain_info.get('name', ''),
                "expert": domain_info.get('expert', ''),
                "keywords": domain_info.get('keywords', []),
                "minimal_units": domain_info.get('minimal_units', [])
            },
            
            # 専門家の知識（完全版）
            "expert_context": {
                "full_expert_knowledge": expert_knowledge,
                "professional_insights": expert_knowledge.get('professional_insights', {}),
                "workflow_optimization": expert_knowledge.get('workflow_optimization', {}),
                "quality_control": expert_knowledge.get('quality_control', {}),
                "platform_specific": expert_knowledge.get('platform_specific', {})
            },
            
            # タスク分解支援情報（詳細版）
            "task_decomposition_context": {
                "workflow_patterns": workflow_patterns.get('workflow_patterns', {}),
                "optimization_patterns": workflow_patterns.get('optimization_patterns', {}),
                "conditional_patterns": workflow_patterns.get('conditional_patterns', {}),
                "error_recovery_patterns": workflow_patterns.get('error_recovery_patterns', {})
            },
            
            # 制約と要件（完全版）
            "constraints_and_requirements": {
                "full_constraints": constraints,
                "timing_constraints": constraints.get('timing_constraints', {}),
                "technical_constraints": constraints.get('technical_constraints', {}),
                "parallel_processing": constraints.get('parallel_processing', {}),
                "audio_video_sync": constraints.get('audio_video_sync', {}),
                "quality_assurance": constraints.get('quality_assurance', {}),
                "failure_recovery": constraints.get('failure_recovery', {})
            },
            
            # 実装リソース情報
            "implementation_resources": {
                "minimal_units_list": domain_info.get('minimal_units', []),
                "recommended_mcp_services": self._get_recommended_mcp_services(domain),
                "external_apis": self._get_recommended_external_apis(domain)
            },
            
            # 思考プロセスガイド
            "complex_thinking_guide": {
                "pre_production_thinking": f"{domain}ドメインでは、実装前に専門的な観点から要件を分析し、最適なワークフローを設計することが重要です。",
                "quality_assurance_thinking": "品質保証の観点から、各タスクの出力が期待される基準を満たしているか継続的に確認します。",
                "optimization_thinking": "効率化のために、依存関係のないタスクを特定し、適切な並列化を検討します。",
                "error_handling_thinking": "各タスクで発生しうるエラーを予測し、適切なリカバリー戦略を事前に計画します。"
            }
        }
    
    def _get_recommended_mcp_services(self, domain: str) -> List[str]:
        """ドメインに応じて推奨されるMCPサービスを返す"""
        mcp_mapping = {
            "video-production": ["t2i-google-imagen3", "i2v-fal-hailuo-02-pro", "t2s-fal-minimax-speech-02-turbo", "v2v-fal-creatify-lipsync"],
            "3d-modeling": ["t2i-google-imagen3", "i2i3d-fal-hunyuan3d-v21"],
            "audio-production": ["t2m-google-lyria", "t2s-fal-minimax-speech-02-turbo", "v2a-fal-thinksound"],
            "image-generation": ["t2i-google-imagen3", "t2i-fal-imagen4-ultra", "i2i-fal-flux-kontext-max"],
            "animation": ["t2v-fal-veo3-fast", "i2v-fal-bytedance-seedance-v1-lite", "r2v-fal-vidu-q1"],
            "news-content": ["WebSearch", "t2i-google-imagen3", "t2s-fal-minimax-speech-02-turbo"],
            "social-media": ["t2i-fal-imagen4-fast", "t2v-fal-veo3-fast", "t2s-fal-minimax-speech-02-turbo"],
            "educational": ["t2i-google-imagen3", "t2s-google", "i2v-fal-hailuo-02-pro"],
            "marketing": ["t2i-fal-imagen4-ultra", "t2v-fal-veo3-fast", "t2s-fal-minimax-speech-02-turbo"],
            "technical-documentation": ["t2i-google-imagen3", "WebSearch"],
            "data-visualization": ["t2i-google-imagen3", "WebSearch"],
            "scientific-research": ["WebSearch", "t2i-google-imagen3"],
            "creative-writing": ["t2i-google-imagen3", "t2m-google-lyria"],
            "game-development": ["t2i-google-imagen3", "i2i3d-fal-hunyuan3d-v21", "t2m-google-lyria"],
            "architectural-design": ["t2i-google-imagen3", "i2i3d-fal-hunyuan3d-v21"],
            "fashion-design": ["t2i-fal-imagen4-ultra", "i2i-fal-flux-kontext-max"],
            "music-production": ["t2m-google-lyria", "v2a-fal-thinksound"],
            "podcast-production": ["t2s-fal-minimax-speech-02-turbo", "v2v-fal-minimax-voice-design"],
            "live-streaming": ["t2s-fal-minimax-speech-02-turbo", "v2v-fal-creatify-lipsync"],
            "vr-content": ["i2i3d-fal-hunyuan3d-v21", "t2v-fal-veo3-fast"],
            "medical-visualization": ["t2i-google-imagen3", "i2i3d-fal-hunyuan3d-v21"],
            "legal-documentation": ["WebSearch"],
            "financial-reporting": ["WebSearch", "t2i-google-imagen3"]
        }
        return mcp_mapping.get(domain, ["t2i-google-imagen3", "WebSearch"])
    
    def _get_recommended_external_apis(self, domain: str) -> List[str]:
        """ドメインに応じて推奨される外部APIを返す"""
        api_mapping = {
            "video-production": ["youtube", "openai"],
            "news-content": ["newsapi", "openai", "twitter"],
            "social-media": ["twitter", "instagram", "youtube"],
            "marketing": ["google-sheets", "sendgrid", "slack"],
            "data-visualization": ["google-sheets", "finnhub"],
            "scientific-research": ["arxiv", "openai"],
            "financial-reporting": ["finnhub", "google-sheets"],
            "podcast-production": ["elevenlabs", "youtube"],
            "live-streaming": ["youtube", "twitch"]
        }
        return api_mapping.get(domain, [])


def main():
    parser = argparse.ArgumentParser(description='Domain Template Loader')
    parser.add_argument('--action', choices=['detect', 'load', 'split', 'summary', 'summary-for-decomposition'], required=True,
                        help='Action to perform')
    parser.add_argument('--issue', type=str, help='Issue content for domain detection')
    parser.add_argument('--domain', type=str, help='Domain name')
    parser.add_argument('--chunk', type=str, help='Chunk type to load')
    parser.add_argument('--section', type=str, help='Specific section to load')
    parser.add_argument('--output', type=str, help='Output file path')
    
    args = parser.parse_args()
    
    loader = DomainTemplateLoader()
    
    if args.action == 'detect':
        if not args.issue:
            print("Error: --issue is required for detect action")
            sys.exit(1)
            
        # イシュー内容を読み込む（ファイルパスまたは直接テキスト）
        if os.path.exists(args.issue):
            with open(args.issue, 'r', encoding='utf-8') as f:
                issue_content = f.read()
        else:
            issue_content = args.issue
        
        domains = loader.detect_domain(issue_content)
        result = {
            "detected_domains": domains,
            "primary_domain": domains[0]['domain'] if domains else None
        }
        
    elif args.action == 'load':
        if not args.domain or not args.chunk:
            print("Error: --domain and --chunk are required for load action")
            sys.exit(1)
        
        result = loader.load_template_chunk(args.domain, args.chunk, args.section)
        
    elif args.action == 'split':
        if not args.domain:
            print("Error: --domain is required for split action")
            sys.exit(1)
        
        chunks = loader.split_template_data(args.domain)
        result = {
            "domain": args.domain,
            "total_chunks": len(chunks),
            "chunks": chunks
        }
        
    elif args.action == 'summary':
        if not args.domain:
            print("Error: --domain is required for summary action")
            sys.exit(1)
        
        result = loader.get_domain_summary(args.domain)
    
    elif args.action == 'summary-for-decomposition':
        if not args.domain:
            print("Error: --domain is required for summary-for-decomposition action")
            sys.exit(1)
        
        result = loader.get_domain_summary_for_task_decomposition(args.domain)
    
    # 結果を出力
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()