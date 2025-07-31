# Minimal Unit Selector Prompt

ユーザーの要求とタスク分解結果に基づいて、適切なミニマルユニットを選択してください。

## 入力情報
- ユーザー要求: {{USER_REQUEST}}
- 分解されたタスク: {{DECOMPOSED_TASKS}}
- ワークフロータイプ: {{WORKFLOW_TYPE}}

## 利用可能なミニマルユニット

### 企画・分析
- planning-ccsdk: Claude Code SDKによる企画立案
- web-search: Web検索による情報収集
- markdown-summary: Markdownサマリー生成

### 画像生成・処理
- image-t2i: 汎用Text-to-Image（複数モデル対応）
- t2i-imagen3: Google Imagen3による高品質画像生成
- image-analysis: 画像内容の分析
- banner-text: バナー画像にテキスト追加

### 動画生成・処理
- video-generation: 汎用動画生成（i2v/t2v対応）
- t2v-veo3: Google Veo3によるText-to-Video
- i2v-seedance: SeeDanceによるImage-to-Video
- video-concat: 複数動画の結合
- upscale-topaz: 動画アップスケール

### 音声・音楽
- bgm-generate-mcp: MCPによるBGM生成
- t2s-google: Google Text-to-Speech
- t2s-minimax-turbo: MiniMax Turbo TTS
- bgm-overlay: BGMのオーバーレイ

### 統合・配信
- local-save: プロジェクトディレクトリへの保存
- git-pr-create: プルリクエスト作成
- sns-publish: SNS投稿

## 選択基準
1. **機能マッチング**: タスクの要求とユニットの機能が一致
2. **依存関係**: 前後のタスクとの連携可能性
3. **並列可能性**: 同時実行できるユニットの組み合わせ
4. **品質要求**: ユーザーの品質設定に適したユニット

## 出力形式
```json
{
  "selected_units": [
    {
      "task_id": "task-001",
      "unit_name": "planning-ccsdk",
      "unit_path": "minimal-units/planning/planning-ccsdk.yml",
      "inputs": {
        "prompt": "ユーザー要求から生成されたプロンプト"
      },
      "dependencies": []
    },
    {
      "task_id": "task-002",
      "unit_name": "image-t2i",
      "unit_path": "minimal-units/image/image-t2i.yml",
      "inputs": {
        "prompt": "画像生成プロンプト",
        "model": "t2i-google-imagen3"
      },
      "dependencies": ["task-001"]
    }
  ],
  "parallel_groups": [
    ["task-002", "task-003"],
    ["task-004"]
  ],
  "new_units_needed": []
}