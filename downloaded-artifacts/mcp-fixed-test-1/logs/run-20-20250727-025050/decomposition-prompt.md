# Stepback Answers to Task Plan Generator

ユーザーのステップバック回答を分析して、具体的なタスクプランに変換します。

## 入力データ

### ワークフロータイプ
```
image-generation
```

### ステップバック回答
以下に実際のユーザー回答が追記されます:

## 分析指示

以下のステップバック回答を分析し、ユーザーの要求に最適化されたタスクプランを生成してください：

### 分析ポイント
1. **Q1（構造・アーキテクチャ）** → 処理方式・段階設計に反映
2. **Q2（品質・パフォーマンス）** → 品質設定・並列処理設計に反映
3. **Q3（エラー処理）** → フォールバック戦略・リトライ設定に反映
4. **Q4（出力・保存）** → 出力形式・中間ファイル保存に反映
5. **Q5（拡張性）** → 監視・ログ設定に反映

## 必須出力形式

以下のJSON形式で `generated/metadata/task-decomposition/task-plan.json` に出力してください：

```json
{
  "workflow_type": "image-generation",
  "estimated_duration_minutes": 数値,
  "user_requirements": {
    "architecture": "ユーザー指定の構造設計",
    "quality_priority": "品質優先度",
    "error_handling": "エラー対応方式",
    "output_format": "出力要求",
    "extensibility": "拡張性要求"
  },
  "tasks": [
    {
      "id": "task-001",
      "name": "具体的なタスク名",
      "description": "ユーザー要求を反映した詳細説明",
      "type": "mcp_generation|processing|integration|validation",
      "dependencies": ["依存するタスクID"],
      "required_tools": ["t2i-google-imagen3", "i2v-fal-hailuo-02-pro"],
      "quality_settings": {
        "priority": "high|medium|low",
        "timeout_minutes": 数値,
        "retry_count": 数値
      },
      "error_handling": {
        "strategy": "retry|fallback|skip|abort",
        "fallback_service": "代替サービス名（該当時）"
      },
      "outputs": {
        "save_intermediate": true/false,
        "formats": ["形式1", "形式2"],
        "metadata_level": "basic|detailed|custom"
      }
    }
  ],
  "execution_flow": [
    {
      "stage": 1,
      "parallel": false,
      "tasks": ["task-001"],
      "quality_gate": "必須品質条件"
    }
  ],
  "monitoring": {
    "log_level": "basic|detailed|debug",
    "metrics_tracking": true/false,
    "progress_reporting": true/false
  }
}
```

## タスク生成例

### video-generation の場合
ユーザーが「T2I→I2V複合処理、最高品質、エラー時サービス切り替え、中間ファイル保存」と回答した場合：

```json
{
  "workflow_type": "video-generation",
  "estimated_duration_minutes": 60,
  "tasks": [
    {
      "id": "task-001",
      "name": "高品質画像生成（T2I）",
      "type": "mcp_generation",
      "required_tools": ["t2i-google-imagen3"],
      "quality_settings": {
        "priority": "high",
        "timeout_minutes": 15,
        "retry_count": 3
      },
      "error_handling": {
        "strategy": "fallback",
        "fallback_service": "t2i-fal-imagen4-ultra"
      },
      "outputs": {
        "save_intermediate": true,
        "formats": ["png", "jpg"],
        "metadata_level": "detailed"
      }
    },
    {
      "id": "task-002", 
      "name": "画像から動画生成（I2V）",
      "type": "mcp_generation",
      "dependencies": ["task-001"],
      "required_tools": ["i2v-fal-hailuo-02-pro"],
      "quality_settings": {
        "priority": "high",
        "timeout_minutes": 20,
        "retry_count": 2
      }
    }
  ]
}
```

## 重要な指針

1. **ユーザー回答の最大活用**: フォールバックではなく、回答内容を具体的に反映
2. **品質とパフォーマンスのバランス**: ユーザーの優先度に応じて調整
3. **エラー対応の具体化**: 抽象的ではなく、実行可能な戦略を指定
4. **段階的実行**: 依存関係を考慮した効率的な実行順序
5. **監視可能性**: 進行状況とエラーを追跡可能な設計

## フォールバック処理

ステップバック回答が不十分な場合のみ、以下のデフォルト設定を使用：
- 品質優先度: medium
- エラー処理: retry (3回)
- 出力: 最終結果のみ保存
- ログレベル: basic## ユーザーのステップバック回答

**回答：**
T2I→I2V複合処理を採用します。テキストのみを入力として受け取り、まずテキストから高品質画像を生成し、その画像を基に動画を作成する2段階処理を実装します。必要に応じて処理段階を柔軟に調整可能な設計とし、品質向上のための追加処理ステップも組み込める構造にします。

**Q2: 品質・パフォーマンス設計**
--
**回答：**
最高品質設定を採用し、実行時間制限は設けません。T2I処理完了後にI2VとT2M処理を並列実行することで効率化を図ります。品質を最優先とし、各段階で最適なMCPサービス設定を使用します。必要に応じて並列処理数の調整も可能な柔軟な設計とします。

**Q3: エラー処理・フォールバック設計**
--
**回答：**
エラー発生時は即座に停止して状況を確認し、異なるMCPサービスへの切り替えで処理継続を図ります。各段階で中間ファイルを保存しているため、失敗した段階から再開または完全再実行の選択が可能です。柔軟な復旧戦略により、ユーザーのニーズに応じた対応を実現します。

**Q4: 出力・保存設計**
--
**回答：**
画像・動画はURLベースでプレビュー可能とし、保存時はダウンロード形式で提供します。最終成果物は完全に保存し、中間ファイルも参考用として保持します。基本的なメタデータ（生成時刻、使用サービス、品質設定等）も合わせて記録します。

**Q5: 拡張性・統合設計**
--
**回答：**
現在の要件に集中した単独完結型として設計し、詳細な監視・ログ機能を組み込みます。各段階の実行状況、使用リソース、品質メトリクス、エラー情報などを詳細に記録し、将来的な改善やデバッグに活用できる基盤を構築します。

---
--
