#!/usr/bin/env python3
"""
Workflow Inputs Generator
専門家視点でのworkflow_dispatch inputs生成
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

class WorkflowInputsGenerator:
    def __init__(self, templates_dir: str = "meta/domain-templates"):
        self.templates_dir = Path(templates_dir)
        # GitHub Actions inputsの制限
        self.MAX_INPUTS = 10
        self.MAX_DESCRIPTION_LENGTH = 1000
        self.VALID_INPUT_TYPES = ['string', 'boolean', 'choice', 'environment']
        
    def load_domain_input_schema(self, domain: str) -> Dict[str, Any]:
        """ドメインのinput-schema.yamlを読み込む"""
        schema_path = self.templates_dir / domain / "input-schema.yaml"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Input schema not found for domain: {domain}")
            
        with open(schema_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def prioritize_inputs(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """入力項目を優先順位付けして最大10個に絞り込む"""
        all_inputs = []
        
        # 必須パラメータ（最優先）
        if 'inputs' in schema and 'required' in schema['inputs']:
            for param_name, param_info in schema['inputs']['required'].items():
                all_inputs.append({
                    'name': param_name,
                    'info': param_info,
                    'priority': 1,
                    'required': True
                })
        
        # 推奨パラメータ（中優先）
        if 'inputs' in schema and 'recommended' in schema['inputs']:
            for param_name, param_info in schema['inputs']['recommended'].items():
                # 最も重要そうなものを選択
                if self._is_important_param(param_name, param_info):
                    all_inputs.append({
                        'name': param_name,
                        'info': param_info,
                        'priority': 2,
                        'required': False
                    })
        
        # 優先順位でソートして最大10個に制限
        all_inputs.sort(key=lambda x: (x['priority'], x['name']))
        return all_inputs[:self.MAX_INPUTS]
    
    def _is_important_param(self, name: str, info: Dict[str, Any]) -> bool:
        """パラメータの重要度を判定"""
        # 重要なキーワードを含むパラメータ
        important_keywords = [
            'type', 'style', 'mode', 'format', 'duration',
            'quality', 'size', 'count', 'target', 'method'
        ]
        
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in important_keywords)
    
    def convert_to_github_input(self, param_name: str, param_info: Dict[str, Any], 
                                is_required: bool) -> Dict[str, Any]:
        """ドメインパラメータをGitHub Actions input形式に変換"""
        github_input = {
            'description': self._create_description(param_info),
            'required': is_required,
            'type': 'string'  # デフォルト
        }
        
        # enumがある場合はchoice型に変換
        if 'enum' in param_info:
            github_input['type'] = 'choice'
            github_input['options'] = param_info['enum']
            if 'default' in param_info:
                github_input['default'] = str(param_info['default'])
        
        # boolean型の場合
        elif param_info.get('type') == 'boolean':
            github_input['type'] = 'boolean'
            if 'default' in param_info:
                github_input['default'] = param_info['default']
        
        # string型の場合
        elif param_info.get('type') == 'string':
            if 'default' in param_info:
                github_input['default'] = param_info['default']
        
        # number/integer型の場合はstring型に変換（選択肢として）
        elif param_info.get('type') in ['number', 'integer']:
            if 'range' in param_info:
                # 範囲から選択肢を生成
                min_val, max_val = param_info['range']
                github_input['type'] = 'choice'
                github_input['options'] = self._generate_number_choices(
                    min_val, max_val, param_info.get('type')
                )
                if 'default' in param_info:
                    github_input['default'] = str(param_info['default'])
            else:
                # 範囲がない場合は通常のstring
                if 'default' in param_info:
                    github_input['default'] = str(param_info['default'])
        
        # object/array型は処理をスキップまたは簡略化
        elif param_info.get('type') in ['object', 'array']:
            # JSON文字列として扱う
            github_input['description'] += ' (JSON形式で入力)'
            if 'example' in param_info:
                github_input['default'] = json.dumps(
                    param_info['example'], 
                    ensure_ascii=False
                )
        
        return github_input
    
    def _create_description(self, param_info: Dict[str, Any]) -> str:
        """パラメータの説明文を生成（最大1000文字）"""
        description_parts = []
        
        # 基本説明
        if 'description' in param_info:
            description_parts.append(param_info['description'])
        
        # 例を追加
        if 'example' in param_info:
            example_str = str(param_info['example'])
            if len(example_str) < 100:  # 長すぎる例は除外
                description_parts.append(f"例: {example_str}")
        
        # バリデーション情報
        if 'validation' in param_info:
            description_parts.append(f"制約: {param_info['validation']}")
        
        # 影響範囲
        if 'impacts' in param_info and isinstance(param_info['impacts'], list):
            impacts_str = ', '.join(param_info['impacts'][:3])  # 最大3つ
            description_parts.append(f"影響: {impacts_str}")
        
        # 結合して文字数制限
        full_description = ' | '.join(description_parts)
        if len(full_description) > self.MAX_DESCRIPTION_LENGTH:
            full_description = full_description[:self.MAX_DESCRIPTION_LENGTH-3] + '...'
        
        return full_description
    
    def _generate_number_choices(self, min_val: float, max_val: float, 
                                num_type: str) -> List[str]:
        """数値範囲から適切な選択肢を生成"""
        if num_type == 'integer':
            # 整数の場合
            if max_val - min_val <= 10:
                # 範囲が狭い場合は全て列挙
                return [str(i) for i in range(int(min_val), int(max_val) + 1)]
            else:
                # 範囲が広い場合は代表値を選択
                values = []
                if min_val <= 1:
                    values.extend(['1', '5', '10'])
                if max_val >= 50:
                    values.extend(['25', '50'])
                if max_val >= 100:
                    values.extend(['100', '500'])
                if max_val >= 1000:
                    values.append('1000')
                
                # 範囲内の値のみ保持
                return [v for v in values if min_val <= int(v) <= max_val]
        else:
            # 小数の場合は代表的な値を返す
            return [str(min_val), str((min_val + max_val) / 2), str(max_val)]
    
    def generate_workflow_inputs(self, domain: str, 
                                issue_content: Optional[str] = None) -> Dict[str, Any]:
        """ドメインに基づいてworkflow_dispatch inputsを生成"""
        # input-schema.yamlを読み込む
        schema = self.load_domain_input_schema(domain)
        
        # 優先順位付けして入力項目を選択
        prioritized_inputs = self.prioritize_inputs(schema)
        
        # GitHub Actions形式に変換
        workflow_inputs = {}
        
        # 常に含めるべき共通入力
        workflow_inputs['project_name'] = {
            'description': 'プロジェクト名',
            'required': True,
            'type': 'string'
        }
        
        # ドメイン固有の入力を追加（最大9個、1個は project_name で使用）
        for i, param_data in enumerate(prioritized_inputs[:9]):
            param_name = param_data['name']
            param_info = param_data['info']
            is_required = param_data['required']
            
            try:
                github_input = self.convert_to_github_input(
                    param_name, param_info, is_required
                )
                workflow_inputs[param_name] = github_input
            except Exception as e:
                print(f"Warning: Failed to convert parameter '{param_name}': {e}")
                continue
        
        return workflow_inputs
    
    def generate_workflow_with_inputs(self, workflow_path: str, inputs: Dict[str, Any]) -> str:
        """既存のワークフローにinputsセクションを追加"""
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_content = f.read()
        
        # workflow_dispatch inputsを生成
        inputs_yaml = self._format_inputs_yaml(inputs)
        
        # 既存のworkflow_dispatchセクションを探して置換
        if 'workflow_dispatch:' in workflow_content:
            if 'inputs:' in workflow_content:
                # 既存のinputsを置換
                import re
                pattern = r'(workflow_dispatch:\s*\n)(\s*inputs:[\s\S]*?)(\n\w|\n\s*$)'
                replacement = f'\\1{inputs_yaml}\\3'
                new_content = re.sub(pattern, replacement, workflow_content)
            else:
                # inputsを追加
                new_content = workflow_content.replace(
                    'workflow_dispatch:',
                    f'workflow_dispatch:\n{inputs_yaml}'
                )
        else:
            # workflow_dispatchセクション自体を追加
            trigger_section = f"""  workflow_dispatch:
{inputs_yaml}"""
            
            # onセクションに追加
            if '\non:' in new_content:
                new_content = new_content.replace('\non:', f'\non:\n{trigger_section}')
            else:
                new_content = f"on:\n{trigger_section}\n\n{new_content}"
        
        return new_content
    
    def _format_inputs_yaml(self, inputs: Dict[str, Any]) -> str:
        """inputsをYAML形式にフォーマット"""
        lines = ['    inputs:']
        
        for input_name, input_config in inputs.items():
            lines.append(f'      {input_name}:')
            
            # description
            lines.append(f'        description: \'{input_config["description"]}\'')
            
            # required
            lines.append(f'        required: {str(input_config["required"]).lower()}')
            
            # type
            if input_config['type'] == 'choice':
                lines.append('        type: choice')
                lines.append('        options:')
                for option in input_config.get('options', []):
                    lines.append(f'          - \'{option}\'')
            else:
                lines.append(f'        type: {input_config["type"]}')
            
            # default
            if 'default' in input_config:
                if input_config['type'] == 'boolean':
                    lines.append(f'        default: {str(input_config["default"]).lower()}')
                else:
                    lines.append(f'        default: \'{input_config["default"]}\'')
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate workflow inputs')
    parser.add_argument('--domain', required=True, help='Domain name')
    parser.add_argument('--workflow', help='Workflow file to update')
    parser.add_argument('--issue', help='Issue content file')
    parser.add_argument('--output', help='Output file')
    parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                        help='Output format')
    
    args = parser.parse_args()
    
    generator = WorkflowInputsGenerator()
    
    # イシュー内容を読み込む（オプション）
    issue_content = None
    if args.issue and os.path.exists(args.issue):
        with open(args.issue, 'r', encoding='utf-8') as f:
            issue_content = f.read()
    
    # inputs生成
    inputs = generator.generate_workflow_inputs(args.domain, issue_content)
    
    # ワークフローファイルが指定されている場合は更新
    if args.workflow:
        updated_workflow = generator.generate_workflow_with_inputs(args.workflow, inputs)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(updated_workflow)
        else:
            print(updated_workflow)
    else:
        # inputsのみ出力
        if args.format == 'yaml':
            output = yaml.dump(inputs, allow_unicode=True, default_flow_style=False)
        else:
            output = json.dumps(inputs, ensure_ascii=False, indent=2)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            print(output)


if __name__ == "__main__":
    main()