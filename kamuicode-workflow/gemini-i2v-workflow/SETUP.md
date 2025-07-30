# セットアップガイド

Gemini Image-to-Video Generation & Analysis Workflowのセットアップ手順

## 📋 前提条件

- GitHub リポジトリ（Actions有効）
- Gemini API アクセス
- kamuicode MCP サーバー設定

## 🔧 ステップ1: リポジトリのクローンと設定

### 1.1 リポジトリのクローン

```bash
# リポジトリをクローン
git clone https://github.com/KentaHomma/kamuicode-workflow.git
```

### 1.2 ワークフローファイルの配置

```bash
# ワークフローディレクトリを作成
mkdir -p .github/workflows

# ワークフローファイルをコピー
cp kamuicode-workflow/gemini-i2v-workflow/gemini-i2v-generation-analysis.yml .github/workflows/

# ファイルが正しくコピーされたか確認
ls -la .github/workflows/
```

### 1.3 kamuicode MCP設定（重要）

#### MCP設定ファイルの配置

```bash
# Gemini設定ディレクトリを作成
mkdir -p .gemini

# kamuicode MCP設定ファイルを配置
# .gemini/settings.json の設定が必要
```

**⚠️ 重要**: `.gemini/settings.json`ファイルを手動で作成する必要があります。

#### kamuicode MCP設定の作成

`.gemini/settings.json`ファイルを作成し、以下の内容を記載してください：

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

**⚠️ 注意**: 
- `[kamuicode提供のURL]`部分は実際のkamuicode MCPサーバーURLに置き換えてください
- このファイルはユーザー環境によって異なる設定が必要です
- `timeout`は300000（5分）に設定してください

#### 使用するMCPツールの限定設定

**重要**: 全てのMCPツールを設定すると、gemini特有の問題で利用できないツールがある場合にエラーになります。
（Gemini CLI actionがSettings.jsonを読み込む際に、MCPツールの有効性を全部確認しているようです。）

このワークフローでは以下のツールのみを使用するため、限定的な設定を推奨します：

**必要なMCPツール:**
- `mcp__t2i-fal-imagen4-fast__imagen4_fast_submit`
- `mcp__t2i-fal-imagen4-fast__imagen4_fast_status`
- `mcp__t2i-fal-imagen4-fast__imagen4_fast_result`
- `mcp__i2v-fal-hailuo-02-pro__hailuo_02_submit`
- `mcp__i2v-fal-hailuo-02-pro__hailuo_02_status`
- `mcp__i2v-fal-hailuo-02-pro__hailuo_02_result`


#### 追加設定（必要に応じて）

**⚠️ 重要**: このワークフローはGemini CLI actionを使用しており、追加の権限設定は基本的に不要です。

## 🔐 ステップ2: Secrets設定

### 2.1 必要なSecrets

以下のキーの設定が必要です：

| Secret名 | 説明 | 取得方法 |
|---------|------|----------|
| `GEMINI_API_KEY` | Gemini API Key (必須) | [Google AI Studio](https://aistudio.google.com/)でAPI Keyを作成 |
| `PAT_TOKEN` | GitHub Personal Access Token (オプション) | Settings → Developer settings → Personal access tokens → Tokens (classic) |

### 2.2 GEMINI_API_KEYの取得方法

1. [Google AI Studio](https://aistudio.google.com/)にアクセス
2. Googleアカウントでログイン
3. 左側メニューの「Get API key」をクリック
4. 「Create API key」をクリック
5. 作成されたAPIキーをコピー

### 2.3 PAT_TOKENの取得方法（オプション）

1. GitHubにログイン
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. 「Generate new token (classic)」をクリック
4. 以下の権限を選択：
   - `repo` (リポジトリへの完全アクセス)
   - `workflow` (GitHub Actionsワークフローの更新)
5. 「Generate token」をクリック
6. 作成されたトークンをコピー（⚠️この画面でしか表示されません）

### 2.4 Secrets設定手順

**2つの方法があります：**

#### 方法1: GitHub CLI（推奨・簡単）

```bash
# カレントディレクトリがリポジトリ内の場合
gh secret set GEMINI_API_KEY --app actions
# ↑ 実行後、APIキーを安全に入力（画面に表示されません）

# PAT_TOKEN（必要に応じて）
gh secret set PAT_TOKEN --app actions

# 設定確認
gh secret list --app actions
```

#### 方法2: GitHub Web UI（従来通り）

1. **GitHubリポジトリページ**にアクセス
2. **Settings**タブをクリック
3. 左サイドバーの**Secrets and variables** → **Actions**をクリック
4. **New repository secret**をクリック
5. 以下を順番に追加：

**GEMINI_API_KEYの追加：**
- **Name**: `GEMINI_API_KEY`
- **Secret**: 先ほどコピーしたGemini APIキー
- **Add secret**をクリック

**PAT_TOKENの追加（必要に応じて）：**
- **Name**: `PAT_TOKEN`  
- **Secret**: 先ほどコピーしたPersonal Access Token
- **Add secret**をクリック

### 2.5 設定確認

設定完了後、Secretsページに以下が表示されることを確認：
- ✅ `GEMINI_API_KEY` (Updated X minutes ago)
- ✅ `PAT_TOKEN` (Updated X minutes ago) ※設定した場合

## 📁 ステップ3: ディレクトリ構造

```
your-repo/
├── .github/
│   └── workflows/
│       └── gemini-i2v-generation-analysis.yml
├── .gemini/
│   └── settings.json
├── README.md
└── (他のファイル)
```

## 🎛️ ステップ4: GitHub権限設定（必要に応じて）

**ほとんどの場合、新しいリポジトリでは標準でONになっているため設定不要です。**

ワークフローが権限エラーで失敗する場合のみ、以下を確認してください：

**Settings** → **Actions** → **General** → **Workflow permissions**
- ✅ "Read and write permissions" を選択
- ✅ "Allow GitHub Actions to create and approve pull requests" をチェック

## 🧪 ステップ5: テスト実行

### 5.1 手動テスト

1. **Actions**タブに移動
2. **Gemini Image-to-Video Generation & Analysis**ワークフローを選択
3. **Run workflow**をクリック
4. 基本生成プロンプトを入力（例: "美しい桜の木の下で猫が遊んでいる様子"）
5. **Run workflow**を実行

### 5.2 動作確認

実行後、以下を確認：

- [ ] プロンプト計画が作成されている
- [ ] 画像が生成されている（Imagen4 Fast）
- [ ] 動画が生成されている（Hailuo-02 Pro）
- [ ] 動画分析が実行されている（Gemini Vision）
- [ ] Pull Requestが自動作成されている

---

**サポート:**
- Issue報告: GitHub Issues
- ドキュメント: README.md