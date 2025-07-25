# Meta Workflow Examples

このディレクトリには、メタワークフロージェネレーターシステムで使用される参考ワークフローテンプレートが格納されています。

## 概要

各ワークフローは**超詳細タスク分解**により、AIが確実に実行できる粒度まで分解された完全なワークフロー定義です。メタワークフロージェネレーターは、ユーザーリクエストに基づいてこれらのテンプレートから適切なものを選択し、カスタマイズして新しいワークフローを生成します。

## ワークフロー一覧

### 🎥 **動画・映像制作系**

#### `video-content-creation.yml` - フロー図

```mermaid
graph TD
    A[メディア生成サービス接続テスト] --> B[動画コンセプト・企画立案]
    B --> C[台本・絵コンテ作成]
    C --> D[キーフレーム画像生成]
    D --> E[ビジュアル一貫性チェック・調整]
    E --> F[メイン動画生成]
    F --> G[BGM・効果音生成]
    G --> H[動画品質向上・最終調整]
    H --> I[最終パッケージング・配信準備]
    
    %% 並列処理の表示
    F -.-> G
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef planNode fill:#f3e5f5
    classDef createNode fill:#e8f5e8
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C planNode
    class D,E,F,G,H createNode
    class I finalNode
```

#### `video-content-creation.yml`
- **概要**: テキスト→画像→動画→音声の完全な動画コンテンツ制作フロー
- **複雑度**: Level 5 (最高)
- **所要時間**: 45分
- **主要MCP**: T2V (veo3-fast), I2V (hailuo-02-pro), V2A (metavoice-v1)
- **タスク数**: 14タスク
- **適用場面**: YouTubeコンテンツ、プロモーション動画、教育動画

#### `multimedia-ad-campaign.yml` - フロー図

```mermaid
graph TD
    A[マルチメディアサービス接続テスト] --> B[キャンペーン戦略開発]
    B --> C[クリエイティブコンセプト企画]
    C --> D[アセット仕様計画]
    D --> E[ヒーロー画像作成]
    E --> F[動画コンテンツ制作]
    E --> G[3Dイマーシブコンテンツ作成]
    F --> H[音楽・オーディオ作成]
    H --> I[クロスメディア最適化]
    G --> I
    I --> J[キャンペーン品質保証]
    J --> K[統合配信・展開]
    
    %% 並列処理の表示
    E -.-> F
    E -.-> G
    H -.-> I
    G -.-> I
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef strategyNode fill:#f3e5f5
    classDef contentNode fill:#e8f5e8
    classDef optimizeNode fill:#fff8e1
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C,D strategyNode
    class E,F,G,H contentNode
    class I,J optimizeNode
    class K finalNode
```

#### `multimedia-ad-campaign.yml`
- **概要**: 統合マルチメディア広告キャンペーン制作（全メディア対応）
- **複雑度**: Level 5 (最高)
- **所要時間**: 60分
- **主要MCP**: 全MCP統合 (T2I, T2V, I2V, T2M, V2A, I2I3D)
- **タスク数**: 16タスク
- **適用場面**: 企業広告キャンペーン、ブランディング、商品プロモーション

### 🖼️ **画像・3D制作系**

#### `3d-model-creation.yml` - フロー図

```mermaid
graph TD
    A[3Dサービス接続テスト] --> B[3Dコンセプト開発]
    B --> C[参照画像準備]
    C --> D[プライマリ3Dモデル生成]
    D --> E[3Dモデル最適化]
    E --> F[レンダリング・可視化設定]
    F --> G[3D配信パッケージング]
    G --> H[最終3Dプロジェクトパッケージング]
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef planNode fill:#f3e5f5
    classDef createNode fill:#e8f5e8
    classDef optimizeNode fill:#fff8e1
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C planNode
    class D,E createNode
    class F optimizeNode
    class G,H finalNode
```

#### `3d-model-creation.yml`
- **概要**: 2D画像から3Dモデル生成・最適化
- **複雑度**: Level 4
- **所要時間**: 30分
- **主要MCP**: I2I3D (hunyuan3d-v21), T2I (imagen3)
- **タスク数**: 10タスク
- **適用場面**: プロダクトデザイン、ゲーム開発、建築可視化

#### `image-generation.yml` - フロー図

```mermaid
graph TD
    A[画像生成サービス接続テスト] --> B[画像コンセプト・要件定義]
    B --> C[プロンプト詳細設計]
    C --> D[高品質画像生成]
    D --> E[画像品質チェック・調整]
    E --> F[複数バリエーション生成]
    F --> G[画像最適化・後処理]
    G --> H[最終画像パッケージング]
    
    %% 並列処理
    E -.-> F
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef planNode fill:#f3e5f5
    classDef createNode fill:#e8f5e8
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C planNode
    class D,E,F,G createNode
    class H finalNode
```

#### `image-generation.yml`
- **概要**: テキストプロンプトからの高品質画像生成
- **複雑度**: Level 3
- **所要時間**: 20分
- **主要MCP**: T2I (imagen3, imagen4-ultra)
- **タスク数**: 8タスク
- **適用場面**: イラスト制作、コンセプトアート、マーケティング素材

### 🎵 **音楽・音声制作系**

#### `audio-music-creation.yml` - フロー図

```mermaid
graph TD
    A[音楽サービス接続テスト] --> B[音楽コンセプト・ムード設定]
    B --> C[楽曲構成・アレンジ設計]
    C --> D[メインメロディ・リズム生成]
    D --> E[ハーモニー・コード進行作成]
    E --> F[楽器パート別音源生成]
    F --> G[ミキシング・マスタリング]
    G --> H[音質向上・最終調整]
    H --> I[音楽配信パッケージ作成]
    
    %% 並列処理
    D -.-> E
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef planNode fill:#f3e5f5
    classDef createNode fill:#e8f5e8
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C planNode
    class D,E,F,G,H createNode
    class I finalNode
```

#### `audio-music-creation.yml`
- **概要**: 音楽作曲・音声コンテンツ制作
- **複雑度**: Level 4
- **所要時間**: 35分
- **主要MCP**: T2M (google-lyria), V2A (metavoice-v1)
- **タスク数**: 11タスク
- **適用場面**: BGM制作、ポッドキャスト、音声ガイド

### 📊 **ビジネス・分析系**

#### `presentation-slide-creation.yml` - フロー図

```mermaid
graph TD
    A[プレゼンサービス接続テスト] --> B[プレゼン構成・ストーリー設計]
    B --> C[スライドコンテンツ作成]
    C --> D[ビジュアルデザイン・画像生成]
    D --> E[スライドテンプレート適用]
    E --> F[レイアウト・フォーマット最適化]
    F --> G[プレゼン品質チェック]
    G --> H[配信用ファイル生成]
    
    %% 並列処理
    C -.-> D
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef planNode fill:#f3e5f5
    classDef createNode fill:#e8f5e8
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C planNode
    class D,E,F createNode
    class G,H finalNode
```

#### `presentation-slide-creation.yml`
- **概要**: ビジネスプレゼンテーション作成（コンテンツ＋デザイン）
- **複雑度**: Level 3
- **所要時間**: 40分
- **主要MCP**: T2I (imagen3), 外部API (Google Slides)
- **タスク数**: 12タスク
- **適用場面**: 企業プレゼン、提案書、報告資料

#### `data-analysis-visualization.yml` - フロー図

```mermaid
graph TD
    A[データソース接続テスト] --> B[データ収集・統合]
    B --> C[データクリーニング・前処理]
    C --> D[統計分析・パターン検出]
    D --> E[可視化チャート・グラフ作成]
    E --> F[レポート生成・洞察抽出]
    F --> G[ダッシュボード統合]
    G --> H[最終レポート配信]
    
    %% 並列処理
    D -.-> E
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef processNode fill:#f3e5f5
    classDef analyzeNode fill:#e8f5e8
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C processNode
    class D,E,F analyzeNode
    class G,H finalNode
```

#### `data-analysis-visualization.yml`
- **概要**: データ収集から可視化・レポート生成
- **複雑度**: Level 4
- **所要時間**: 45分
- **主要MCP**: T2I (グラフ・チャート生成), 外部API (GitHub)
- **タスク数**: 8タスク
- **適用場面**: 業績レポート、分析ダッシュボード、KPI追跡

### 📰 **コンテンツ制作系**

#### `news-summarization.yml` - フロー図

```mermaid
graph TD
    A[ニュースソース接続テスト] --> B[ニュース収集・RSS解析]
    B --> C[記事フィルタリング・選別]
    C --> D[要約・サマリー生成]
    D --> E[記事分類・タグ付け]
    E --> F[配信フォーマット作成]
    
    %% 並列処理
    C -.-> D
    C -.-> E
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef collectNode fill:#f3e5f5
    classDef processNode fill:#e8f5e8
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C collectNode
    class D,E processNode
    class F finalNode
```

#### `news-summarization.yml`
- **概要**: ニュース収集・要約・配信
- **複雑度**: Level 2
- **所要時間**: 25分
- **主要MCP**: なし (外部API使用)
- **タスク数**: 6タスク
- **適用場面**: ニュースレター、業界レポート、情報収集

#### `blog-article-creation.yml` - フロー図

```mermaid
graph TD
    A[コンテンツサービス接続テスト] --> B[記事トピック・構成計画]
    B --> C[リサーチ・情報収集]
    C --> D[記事執筆・文章作成]
    D --> E[アイキャッチ画像生成]
    D --> F[記事校正・編集]
    E --> G[SEO最適化・メタデータ設定]
    F --> G
    G --> H[記事公開・配信準備]
    
    %% 並列処理
    D -.-> E
    D -.-> F
    
    %% スタイリング
    classDef testNode fill:#e1f5fe
    classDef planNode fill:#f3e5f5
    classDef createNode fill:#e8f5e8
    classDef optimizeNode fill:#fff8e1
    classDef finalNode fill:#fff3e0
    
    class A testNode
    class B,C planNode
    class D,E,F createNode
    class G optimizeNode
    class H finalNode
```

#### `blog-article-creation.yml`
- **概要**: ブログ記事・記事コンテンツ制作
- **複雑度**: Level 3
- **所要時間**: 35分
- **主要MCP**: T2I (アイキャッチ画像)
- **タスク数**: 9タスク
- **適用場面**: ブログ運営、コンテンツマーケティング、記事執筆

## 技術仕様

### MCP (Model Context Protocol) サービス

各ワークフローで使用される主要なMCPサービス：

- **T2I (Text-to-Image)**
  - `t2i-google-imagen3`: Google Imagen 3
  - `t2i-fal-imagen4-ultra`: Fal.ai Imagen 4 Ultra
  - `t2i-fal-imagen4-fast`: Fal.ai Imagen 4 Fast

- **T2V (Text-to-Video)**  
  - `t2v-fal-veo3-fast`: Fal.ai Veo3 Fast

- **I2V (Image-to-Video)**
  - `i2v-fal-hailuo-02-pro`: Fal.ai Hailuo 0.2 Pro

- **T2M (Text-to-Music)**
  - `t2m-google-lyria`: Google Lyria

- **V2A (Video-to-Audio)**
  - `v2a-fal-metavoice-v1`: Fal.ai MetaVoice v1

- **V2V (Video-to-Video)**
  - `v2v-fal-cogvideo-1_5`: Fal.ai CogVideo 1.5

- **I2I3D (Image-to-3D)**
  - `i2i3d-fal-hunyuan3d-v21`: Fal.ai HunYuan3D v2.1

### ファイル構造パターン

全ワークフローは一貫したファイルパス参照パターンを使用：

```bash
# MCP出力からのファイルパス取得
IMAGE_PATH=$(jq -r '.image_url // .file_path // "none"' "$ref_file")
VIDEO_PATH=$(jq -r '.video_url // .file_path // "none"' "$video_file") 
AUDIO_PATH=$(jq -r '.audio_url // .file_path // "none"' "$audio_file")
```

### GitHub Actions 統合

各ワークフローは以下の構造に従います：

- **Artifacts**: 30日間保持
- **並列実行**: 最大3ジョブ
- **エラーハンドリング**: リトライ機能付き
- **品質チェック**: 各段階での検証
- **ログ記録**: 詳細な実行ログ

## 使用方法

### 1. メタワークフロージェネレーター経由（推奨）

```yaml
- name: メタワークフロー実行
  uses: ./.github/workflows/kamuicode-meta-generator.yml
  with:
    workflow_type: "video-generation"
    description: "商品紹介動画を作成してください"
```

### 2. 直接使用

```bash
# テンプレートをコピーしてカスタマイズ
cp meta/examples/video-content-creation.yml .github/workflows/my-video-workflow.yml

# GitHub Actions として実行
gh workflow run my-video-workflow.yml
```

### 3. カスタマイズ

各ワークフローは以下の箇所をカスタマイズ可能：

- **タイトル・説明**: ワークフロー名とdescription
- **パラメータ**: inputs セクションのデフォルト値
- **MCP設定**: 使用するAI生成サービスの選択
- **並列度**: parallel_group の調整
- **品質基準**: validation セクションの要件

## 品質保証

### 段階的格納システム

1. **Staging**: `generated/workflows/staging/` でテンプレート生成
2. **Validation**: YAML構文・GitHub Actions構造・MCP参照チェック
3. **Production**: 検証合格後 `.github/workflows/` に配置

### 検証項目

- ✅ YAML構文チェック (yamllint)
- ✅ GitHub Actions構造検証
- ✅ MCPサービス参照検証
- ✅ 依存関係チェック（循環参照防止）
- ✅ 総合スコア判定 (75点以上で合格)

## 拡張・カスタマイズ

### 新しいワークフロー追加

1. 既存テンプレートをベースに作成
2. 超詳細タスク分解を適用
3. MCP統合とファイルパス参照パターンを実装
4. `README.md` に追加

### 品質向上

- **並列実行最適化**: タスクの依存関係を最小化
- **エラーハンドリング強化**: フォールバック戦略の追加
- **MCP統合拡張**: 新しいAI生成サービスの組み込み
- **外部API連携**: より多くのサードパーティサービス統合

---

Generated by Meta Workflow Generator v3 (Staged Deployment) 🤖🔄✅

**開発者**: [Kamui Rossy System](https://github.com/username/kamui_rossy)  
**最終更新**: 2025-07-25