# Kamui Rossy データストレージ分析レポート

## 🔍 分析概要
プロジェクト全体のデータ格納場所、ファイルパス依存関係、不要なディレクトリ・ファイルを詳細分析

## 📁 主要データストレージ構造

### 1. **Core Storage Directories**

#### A. `generated/` - 動的生成データ（永続ストレージ）
```
generated/
├── audio/                    # 音楽生成結果
│   └── music.json           # [既存] 音楽データ
├── final/                   # 最終成果物
│   └── package.json         # [既存] パッケージ情報
├── images/                  # 画像生成結果
│   └── results.json         # [既存] 画像データ
├── logs/                    # 実行ログ（重要）
│   └── run-20-20250727-025050/
│       ├── execution-phases.log
│       ├── selected-workflow.json
│       ├── task-plan.json
│       └── *.yml files
├── metadata/                # メタデータ（重要）
│   ├── evaluation/
│   ├── requirement-analysis/
│   ├── stepback-analysis/
│   └── task-decomposition/
└── news_video_scripts/      # 特定用途データ
    ├── docs/
    ├── examples/
    └── scripts/
```

#### B. `meta/` - システム設定・テンプレート（永続）
```
meta/
├── ai-learning/             # 🆕 AI学習データ
│   └── patterns.json        # 学習パターン
├── docs/                    # ドキュメント
├── examples/                # ワークフローテンプレート（重要）
│   ├── 3d-model-creation.yml
│   ├── audio-music-creation.yml
│   ├── blog-article-creation.yml
│   ├── data-analysis-visualization.yml
│   ├── educational-content.yml
│   ├── game-asset-creation.yml
│   ├── image-generation.yml
│   ├── interactive-web-content.yml
│   ├── multimedia-ad-campaign.yml
│   ├── news-summarization.yml
│   ├── podcast-creation.yml
│   ├── presentation-slide-creation.yml
│   ├── social-media-content.yml
│   └── video-content-creation.yml
├── prompts/                 # プロンプトテンプレート
│   ├── deprecated/          # ⚠️ 廃止予定
│   └── templates/
└── successful-workflow-patterns.md  # 成功パターン
```

#### C. `.github/workflows/` - 実行可能ワークフロー
```
.github/workflows/
├── generated/               # 🆕 生成ワークフロー配置
│   ├── active/             # 本番稼働中
│   ├── staging/            # 検証待ち (.disabled)
│   └── archive/            # 履歴保存
├── meta-workflow-executor-v8.yml     # メインワークフロー
├── auto-fix-deployment.yml          # 🆕 AI自動修正システム
├── continuous-system-monitor.yml    # システム監視
└── [多数のワークフローファイル]
```

## 🔗 ワークフロー出力依存関係マップ

### **主要ワークフローの出力パス依存**

#### 1. **Meta Workflow Executor v8** → `generated/` 全体
- `generated/metadata/requirement-analysis/`
- `generated/metadata/stepback-analysis/`
- `generated/metadata/task-decomposition/`
- `generated/metadata/evaluation/`
- `generated/logs/run-{number}-{timestamp}/`
- `.github/workflows/generated/staging/` (新規)

#### 2. **AI Auto-Fix System** → `generated/auto-fix/`
- `generated/auto-fix/analysis/`
- `generated/auto-fix/patterns/`
- `generated/auto-fix/strategies/`
- `generated/auto-fix/claude-insights/`
- `generated/ai-analysis-prompt.md`
- `generated/ai-analysis-result.json`
- `generated/learning-insights.json`
- `generated/improvement-report.md`
- `meta/ai-learning/incident-*.json`

#### 3. **Template Workflows** → 各種 `generated/` サブディレクトリ
各テンプレートが以下のパスを動的作成：
- **Image Generation**: `generated/{service-check,prompts,concepts,images,quality,final}`
- **Video Creation**: `generated/{concept,storyboard,keyframes,video,audio,sync,enhanced,final}`
- **3D Models**: `generated/{concepts,references,models,optimization,rendering,final}`
- **Audio/Music**: `generated/{concepts,composition,audio,processing,mastering,final}`

## ⚠️ 問題のあるファイル・ディレクトリ

### **1. 重複・古いワークフローファイル（削除推奨）**
```
.github/workflows/
├── video-content-creation.yml           # 基本版
├── video-content-creation-cli.yml       # CLI版
├── video-content-creation-direct.yml    # 直接版
├── video-content-creation-download.yml  # ダウンロード版
├── video-content-creation-fixed.yml     # 修正版
├── video-content-creation-mock.yml      # モック版
├── video-content-creation-production.yml     # 本番版
├── video-content-creation-production-v2.yml  # 本番v2
├── video-content-creation-production-v3.yml  # 本番v3
├── video-content-creation-secure.yml         # セキュア版
└── video-content-creation-with-download.yml  # ダウンロード付き
```
**推奨**: 最新の production-v3 のみ残し、他を削除

### **2. テスト用ワークフロー（整理推奨）**
```
├── test-comment-trigger.yml
├── test-direct-mcp-call.yml
├── test-mcp-method-patterns.yml
├── test-mcp-permissions.yml
├── test-mcp-services-detail.yml
├── test-mcp-settings-parameter.yml
└── test-mcp-with-permissions.yml
```
**推奨**: テスト完了後、archive または削除

### **3. 廃止予定プロンプト（削除推奨）**
```
meta/prompts/deprecated/
├── documentation-generation.md
├── script-generation.md
├── task-decomposition.md
└── workflow-generation.md
```
**推奨**: 完全に削除

### **4. 古い生成データ（クリーンアップ推奨）**
```
generated/logs/run-20-20250727-025050/  # 古い実行ログ
generated/news_video_scripts/           # 特定用途（用途不明）
```

### **5. 未使用ディレクトリ**
テンプレートが作成予定だが実際には使われていない：
```
generated/metadata/evaluation/          # 空
generated/metadata/requirement-analysis/ # 空
generated/metadata/stepback-analysis/   # 空
generated/metadata/task-decomposition/  # 空
```

## 📊 ストレージ使用状況

### **Essential (保持必須)**
- `meta/examples/` - 9つのテンプレート（コアロジック）
- `meta/ai-learning/` - AI学習データ
- `generated/logs/` - 実行履歴（最新のみ）
- `generated/metadata/` - メタデータ
- `.github/workflows/meta-workflow-executor-v8.yml`
- `.github/workflows/auto-fix-deployment.yml`
- `.github/workflows/continuous-system-monitor.yml`

### **Redundant (削除推奨)**
- Video関連ワークフロー: 10個 → 1-2個
- Test関連ワークフロー: 7個 → 0個（完了後）
- Deprecated prompts: 4個 → 0個

### **Clean-up Candidates (整理推奨)**
- 古い実行ログ: 7日以上前
- 空のメタデータディレクトリ
- 特定用途の古いスクリプト

## 🔧 推奨改善アクション

### **Phase 1: Immediate Cleanup**
1. **重複ワークフロー削除**: video-* 系を1-2個に統合
2. **テストファイル整理**: test-* 系の用途確認・削除
3. **廃止プロンプト削除**: `meta/prompts/deprecated/`

### **Phase 2: Structure Optimization**
1. **ログローテーション**: 7日以上の古いログ削除
2. **空ディレクトリ整理**: 未使用metadata サブディレクトリ
3. **生成データ整理**: 特定用途データの見直し

### **Phase 3: Monitoring Setup**
1. **自動クリーンアップ**: 古いログの定期削除
2. **ストレージ使用量監視**: 容量増加の追跡
3. **依存関係検証**: 削除前の影響確認

## 📈 期待される効果

- **ストレージ削減**: 約40-50%の容量削減見込み
- **保守性向上**: 重複排除による管理簡素化
- **パフォーマンス**: 不要ファイル削除による処理高速化
- **セキュリティ**: テストファイル削除による情報漏洩リスク削減

---

**注意**: 削除実行前に必ず依存関係を再確認し、バックアップを作成してください。