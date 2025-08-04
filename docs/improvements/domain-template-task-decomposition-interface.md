# Domain Template → Task Decomposition Interface Improvement

## 問題点

1. **現在の構造**
   - Domain summaryがそのままJSONとして埋め込まれている
   - envsubstで複雑なJSONが正しく展開されない
   - タスク分解に必要な情報が整理されていない

2. **データフロー**
   ```
   Domain Template → get_domain_summary() → JSON → Shell Variable → envsubst → Prompt
   ```
   この過程でJSONの特殊文字やネストが問題を起こす

## 改善案

### 1. Domain Template Loader の出力形式を整理

```python
def get_domain_summary_for_task_decomposition(self, domain: str) -> Dict[str, Any]:
    """タスク分解用に整理されたドメインサマリーを取得"""
    
    return {
        # 基本情報
        "domain_info": {
            "domain": domain,
            "expert_role": self._get_expert_role(domain),  # "動画制作の専門家"
            "expertise_areas": self._get_expertise_areas(domain)  # ["企画", "撮影", "編集"]
        },
        
        # タスク分解に必要な情報
        "task_decomposition_hints": {
            "workflow_phases": self._get_workflow_phases(domain),  # ["企画", "制作", "配信"]
            "required_outputs": self._get_required_outputs(domain),  # ["動画ファイル", "サムネイル"]
            "typical_duration": self._get_typical_duration(domain),  # "30-60分"
            "parallel_tasks": self._get_parallel_task_hints(domain)  # ["音声生成", "画像生成"]
        },
        
        # 利用可能なリソース
        "available_resources": {
            "minimal_units": self._get_relevant_units(domain),
            "recommended_tools": self._get_recommended_tools(domain),
            "constraints": self._get_simplified_constraints(domain)  # シンプルなkey-value
        },
        
        # プロンプト用テキスト（エスケープ不要）
        "prompt_snippets": {
            "expert_introduction": f"{domain}分野の専門家として、",
            "workflow_guidance": "一般的な作業フローに従って、",
            "quality_criteria": "プロフェッショナルな品質基準を満たすように"
        }
    }
```

### 2. メタワークフローでの使用方法

```bash
# JSONから必要な部分だけを抽出
EXPERT_ROLE=$(jq -r '.domain_info.expert_role' artifacts/domain_summary.json)
WORKFLOW_PHASES=$(jq -r '.task_decomposition_hints.workflow_phases | join(", ")' artifacts/domain_summary.json)
MINIMAL_UNITS=$(jq -r '.available_resources.minimal_units | join(", ")' artifacts/domain_summary.json)

# ファイルベースでプロンプトを構築
cat > decomposition_prompt.txt << EOF
あなたは${EXPERT_ROLE}です。

以下のワークフローフェーズに従ってタスクを分解してください：
${WORKFLOW_PHASES}

利用可能なミニマルユニット：
${MINIMAL_UNITS}

ユーザーのリクエスト：
$(cat artifacts/issue_content.txt)
EOF

# または、JSONファイルを直接参照
cat > decomposition_prompt.txt << EOF
ドメイン分析結果を参照してタスク分解を行ってください。

ドメイン分析結果: artifacts/domain_summary_for_decomposition.json
ユーザーリクエスト: artifacts/issue_content.txt

上記のファイルを読み込み、適切なタスク分解を行ってください。
EOF
```

### 3. データ検証の追加

```bash
# Domain summaryの検証
if ! jq -e '.domain_info.expert_role' artifacts/domain_summary.json > /dev/null; then
    echo "Error: Invalid domain summary format"
    exit 1
fi

# 中間ファイルの生成と検証
jq '.task_decomposition_hints' artifacts/domain_summary.json > artifacts/task_hints.json
```

## 実装手順

1. **domain-template-loader.py の拡張**
   - `get_domain_summary_for_task_decomposition()` メソッドを追加
   - 既存の `get_domain_summary()` はそのまま残す

2. **メタワークフローの修正**
   - envsubstの使用を最小限に
   - ファイルベースのデータ受け渡しを優先
   - JSONデータはjqで必要な部分だけ抽出

3. **エラーハンドリングの強化**
   - 各段階でデータ形式を検証
   - Claude Code実行前後でファイル存在確認

## 期待される効果

1. **安定性向上**: JSONの特殊文字による問題を回避
2. **保守性向上**: データフローが明確に
3. **デバッグ容易性**: 中間ファイルで各段階の出力を確認可能
4. **拡張性**: 新しいドメインへの対応が容易