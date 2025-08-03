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
                for domain in pattern['domains']:
                    if domain not in [d['domain'] for d in detected_domains]:
                        detected_domains.append({
                            'domain': domain,
                            'confidence': 0.8
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


def main():
    parser = argparse.ArgumentParser(description='Domain Template Loader')
    parser.add_argument('--action', choices=['detect', 'load', 'split', 'summary'], required=True,
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
    
    # 結果を出力
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()