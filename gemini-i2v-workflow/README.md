# Gemini Image-to-Video Generation & Analysis Workflow

GeminiとAIを活用した画像から動画への変換と分析を自動化するワークフロー

## 🎬 概要

このGitHub Actionsワークフローは、**テキストプロンプト**から最適化された画像を生成し、それを動画に変換して品質分析を行います。

### 🎯 処理フロー

1. **📋 プロンプト計画** - Geminiが画像・動画生成用プロンプトを最適化
2. **🖼️ 画像生成** - Imagen4 Fastで高品質画像を生成
3. **🎬 動画生成** - Hailuo-02 Proで画像から動画を生成
4. **📊 品質分析** - Gemini Visionで動画の品質を分析
5. **📝 レポート作成** - 全体的な評価とレポートを自動生成

### 🔧 技術スタック

- **プロンプト最適化**: Gemini（Google）
- **画像生成**: Imagen4 Fast（高速・高品質）
- **動画生成**: Hailuo-02 Pro（Image-to-Video）
- **品質分析**: Gemini Vision（視覚的評価）
- **AI統合**: Gemini CLI Action + kamuicode MCP

## 🚀 使用方法

### 手動実行

1. リポジトリの**Actions**タブに移動
2. **Gemini Image-to-Video Generation & Analysis**ワークフローを選択
3. **Run workflow**ボタンをクリック
4. 基本生成プロンプトを入力（例: "美しい桜の木の下で猫が遊んでいる様子"）
5. **Run workflow**を実行

## 📁 出力構造

```
video-[タイムスタンプ]/
├── planning/
│   ├── image-prompt.md              # 最適化された画像生成プロンプト
│   ├── video-prompt.md              # 最適化された動画生成プロンプト
│   └── planning-strategy.md         # 計画戦略
├── images/
│   ├── generated-image.jpg          # 生成された画像
│   └── image-url.txt               # 画像のURL(情報伝達用で保存されない）
├── videos/
│   ├── generated-video.mp4          # 生成された動画
│   └── video-url.txt               # 動画のURL(機報伝達用で保存されない)
├── analysis/
│   └── video-analysis.md           # 詳細な品質分析レポート
└── README.md                       # 処理詳細とサマリー
```

## 🎨 生成プロンプト例

### 🐱 動物系
```
"美しい桜の木の下で猫が遊んでいる様子"
"夕日の海辺で犬が走っている"
"森の中で鳥が歌っている"
```

### 🌸 自然系
```
"風に舞う桜の花びらと青空"
"雲が流れる山の風景"
"静かな湖面に映る月"
```

### 🎨 アート系
```
"水彩画のような雨の街角"
"油絵のような田園風景"
"パステルカラーの夢の世界"
```

## 📊 品質分析内容

### 視覚的品質評価（1-10点）
- 映像のクリアさ・鮮明度
- 色彩の豊かさと自然さ
- 動きの滑らかさ
- 構図とフレーミング
- 照明とコントラスト

### プロンプト適合度評価（1-10点）
- 基本プロンプトとの一致度
- 画像プロンプトとの一致度
- 動画プロンプトとの一致度
- 創造的な解釈の質

### 技術的品質評価（1-10点）
- 動画の安定性（手ぶれ等）
- フレーム間の連続性
- アーティファクトの有無
- 全体的な制作品質

## 🔧 セットアップ要件

### 必要なSecrets

```yaml
GEMINI_API_KEY: # Google Gemini API Key
PAT_TOKEN: # GitHub Personal Access Token
```

### 必要なファイル

```
.github/
└── workflows/
    └── gemini-i2v-generation-analysis.yml  # ワークフローファイル
.gemini/
└── settings.json         # kamuicode MCP設定
```

### ⚠️ 重要な設定事項

#### kamuicode MCP設定

**必須**: `.gemini/settings.json`ファイルを手動で作成する必要があります。

```json
{
  "mcpServers": {
    "t2i-fal-imagen4-fast": {
      "httpUrl": "[kamuicode提供のURL]",
      "timeout": 300000
    },
    "i2v-fal-hailuo-02-pro": {
      "httpUrl": "[kamuicode提供のURL]",
      "timeout": 300000
    }
  },
  "coreTools": [
    "ReadFileTool",
    "WriteFileTool", 
    "EditFileTool",
    "ShellTool"
  ]
}
```

**注意点:**
- `[kamuicode提供のURL]`部分は実際のkamuicode MCPサーバーURLに置き換えてください
- このファイルはユーザー環境によって設定が異なります
- `timeout`は300000（5分）に設定してください

#### MCPツールの限定設定

**重要**: 全てのMCPツールを設定すると、gemini特有の問題で利用できないツールがある場合にエラーになります。
（Gemini CLI actionがSettings.jsonを読み込む際に、MCPツールの有効性を全部確認しているようです。）

このワークフローでは以下のツールのみを使用：
- Imagen4 Fast（画像生成）
- Hailuo-02 Pro（動画生成）

### 権限設定

```yaml
permissions:
  contents: write
  pull-requests: write
```

## 🤖 技術的詳細

### AI Agent構成
- **Planning Agent**: Gemini（プロンプト最適化）
- **Image Generation Agent**: Imagen4 Fast実行
- **Video Generation Agent**: Hailuo-02 Pro実行
- **Analysis Agent**: Gemini Vision（品質分析）

## 📄 ライセンス

MIT License

## 👥 貢献

Issues、Pull Requests大歓迎です！

---

🎬 **Gemini Image-to-Video Generation & Analysis Workflow** - 🤖 Powered by [Gemini CLI Action](https://github.com/google-gemini/gemini-cli-action) & [kamuicode MCP](https://www.kamui.ai/ja)