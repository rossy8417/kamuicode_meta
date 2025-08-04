# Domain Template Unified Improvement Plan

## 現状の課題

1. **データ受け渡しの問題**
   - 複雑なJSONデータがenvsubstで正しく処理されない
   - タスク分解に必要な情報の構造が不明確

2. **統一性の必要性**
   - 24個のドメインテンプレートすべてに同じ改善を適用
   - 一貫性のあるデータフォーマット

## 改善方針

### 1. 情報量を保持しながら構造化

```python
def get_domain_summary_for_task_decomposition(self, domain: str) -> Dict[str, Any]:
    """タスク分解用に整理されたドメインサマリー（詳細情報を保持）"""
    
    # 各YAMLファイルから完全な情報を読み込み
    expert_knowledge = self.load_template_chunk(domain, "expert-knowledge")
    constraints = self.load_template_chunk(domain, "constraints")
    workflow_patterns = self.load_template_chunk(domain, "workflow-patterns")
    
    return {
        # ドメイン専門家の詳細情報（削減しない）
        "expert_context": {
            "domain": domain,
            "full_expert_knowledge": expert_knowledge,  # 完全な専門知識を保持
            "expert_mindset": self._extract_expert_mindset(expert_knowledge),
            "decision_factors": self._extract_decision_factors(expert_knowledge)
        },
        
        # タスク分解の思考プロセス支援情報（詳細を保持）
        "task_decomposition_context": {
            "workflow_patterns": workflow_patterns,  # 完全なパターンを保持
            "typical_workflow_sequence": self._extract_workflow_sequence(workflow_patterns),
            "parallel_optimization_hints": self._extract_parallel_hints(workflow_patterns),
            "dependency_patterns": self._extract_dependency_patterns(workflow_patterns),
            "professional_considerations": self._extract_professional_considerations(expert_knowledge)
        },
        
        # 制約と要件（完全な情報）
        "constraints_and_requirements": {
            "full_constraints": constraints,  # 完全な制約情報
            "technical_constraints": self._categorize_constraints(constraints, "technical"),
            "quality_constraints": self._categorize_constraints(constraints, "quality"),
            "resource_constraints": self._categorize_constraints(constraints, "resource")
        },
        
        # 実装リソース（詳細情報）
        "implementation_resources": {
            "minimal_units_with_descriptions": self._get_units_with_descriptions(domain),
            "recommended_combinations": self._get_recommended_combinations(domain),
            "alternative_approaches": self._get_alternative_approaches(domain)
        },
        
        # 複雑な思考プロセスのガイド
        "complex_thinking_guide": {
            "pre_production_thinking": "このドメインでは、実装前に以下を検討...",
            "quality_assurance_thinking": "品質保証の観点から、以下を確認...",
            "optimization_thinking": "効率化のために、以下の並列化を検討..."
        }
    }
```

### 2. メタワークフローでの使用方法（情報量を保持）

```bash
# Step 1: ドメインサマリーを別ファイルとして保存
python scripts/domain-template-loader.py \
  --action summary-for-decomposition \
  --domain "$PRIMARY_DOMAIN" \
  --output artifacts/detailed_domain_context.json

# Step 2: プロンプトはファイル参照方式で構築
cat > decomposition_prompt.txt << 'EOF'
あなたは専門家として、以下のドメインコンテキストを完全に理解し、
複雑な思考プロセスを経てタスクを分解してください。

ドメインコンテキスト（詳細）: artifacts/detailed_domain_context.json
ユーザーリクエスト: artifacts/issue_content.txt

以下の手順で分解してください：

1. ドメインコンテキストの expert_context を読み込み、専門家の視点を完全に理解
2. task_decomposition_context の workflow_patterns から典型的な作業フローを把握
3. constraints_and_requirements からすべての制約を考慮
4. complex_thinking_guide に従って、複雑な思考プロセスを実行
5. implementation_resources から最適なリソースを選択

出力形式:
{
  "expert_analysis": {
    "understanding": "リクエストの専門的理解（詳細）",
    "considerations": ["考慮事項1", "考慮事項2", ...],
    "thinking_process": "思考プロセスの詳細な記録"
  },
  "tasks": [
    {
      "id": "task-1",
      "name": "タスク名",
      "description": "詳細な説明",
      "reasoning": "なぜこのタスクが必要か",
      "minimal_units": ["unit1", "unit2"],
      "dependencies": [],
      "estimated_duration": "5-10分",
      "professional_notes": "専門的な注意点",
      "quality_criteria": "品質基準"
    }
  ],
  "workflow_optimization": {
    "parallel_groups": [...],
    "critical_path": [...],
    "optimization_rationale": "最適化の理由"
  }
}
EOF

# Step 3: Claude Codeに両方のファイルを読み込ませて実行
npx @anthropic-ai/claude-code \
  -p "$(cat decomposition_prompt.txt)" \
  --allowedTools "Read,Write" \
  --permission-mode "acceptEdits"
```

### 3. 全ドメインテンプレートへの適用計画

1. **domain-template-loader.py の拡張**
   - 新しいアクション `summary-for-decomposition` を追加
   - 既存の機能は保持（後方互換性）

2. **統一的な処理**
   - すべてのドメインで同じ抽出ロジックを使用
   - ドメイン固有の特性も保持

3. **検証プロセス**
   - 各ドメインで生成されるJSONの構造を確認
   - 情報の欠落がないかチェック

### 4. 実装の優先順位

1. **Phase 1**: domain-template-loader.py に新メソッド追加
2. **Phase 2**: 1つのドメイン（video-production）でテスト
3. **Phase 3**: メタワークフローv12の修正
4. **Phase 4**: 全ドメインでの動作確認

## 期待される効果

1. **情報の完全性**: 専門知識が削減されることなく伝達
2. **複雑な思考**: タスク分解時に専門家の思考プロセスを再現
3. **安定性**: JSONエスケープ問題を回避
4. **統一性**: すべてのドメインで一貫した処理

## 注意点

- 情報量は多くなるが、構造化により処理しやすくなる
- ファイルサイズが大きくなる可能性があるが、品質を優先
- すべてのドメインテンプレートが同じ構造を持つことを前提