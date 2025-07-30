# ワークフローパターンカタログ

メタワークフロー作成時の実践的なパターン集です。各パターンには、実際のモジュールワークフローとの対応関係を示しています。

## 🎬 動画制作パターン

### パターンA: シンプル動画制作
**用途**: 基本的なAI動画生成
**参考モジュール**: `module-video-generation-kc-multi-model-ccsdk.yml`

```yaml
name: simple-video-production
units:
  - git-branch-setup
  - planning-ccsdk
  - image-t2i
  - video-generation (i2v mode)
  - fal-upload
  - git-pr-create

データフロー:
planning → image_prompt → image_path → video_path → video_url
```

### パターンB: 高品質動画制作（エンハンスメント付き）
**用途**: 商用レベルの動画制作
**参考モジュール**: `orchestrator-video-generation-dual.yml`

```yaml
name: enhanced-video-production
units:
  # Phase 1: 企画
  - git-branch-setup
  - planning-ccsdk
  - video-prompt-opt
  
  # Phase 2: 生成（並列）
  parallel:
    - image-generation-pipeline:
        - image-t2i (quality model)
        - image-analysis
    - audio-generation-pipeline:
        - audio-minimax
        - bgm-generate
  
  # Phase 3: 動画生成と強化
  - video-generation
  - v2v-luma-ray2 (style enhancement)
  - upscale-topaz (resolution enhancement)
  
  # Phase 4: ポストプロダクション
  - bgm-overlay
  - title-composition
  - video-analysis
  
  # Phase 5: 配信
  - fal-upload
  - git-pr-create
```

### パターンC: リップシンク動画制作
**用途**: キャラクター動画、ナレーション動画
**参考モジュール**: `module-lipsync-generation-kc-multi-model-ccsdk.yml`

```yaml
name: lipsync-video-production
units:
  # Phase 1: 企画と準備
  - git-branch-setup
  - planning-ccsdk (lipsync-aware)
  - pixverse-quota-guard
  
  # Phase 2: 素材生成
  - image-t2i (portrait focused)
  - t2s-minimax-voice (character voice)
  - wav-segmentation
  
  # Phase 3: リップシンク生成
  loop_for_each_segment:
    - lipsync-pixverse
    - srt-make
    - subtitle-overlay
  
  # Phase 4: 最終合成
  - video-concat
  - bgm-overlay (lower volume)
  - video-analysis
  - fal-upload
```

## 🎨 画像制作パターン

### パターンD: マルチモデル画像生成
**用途**: 複数のAIモデルで最適な画像を選択
**参考モジュール**: `orchestrator-multi-model-image-test.yml`

```yaml
name: multi-model-image-generation
units:
  - planning-ccsdk
  
  parallel:
    - pipeline-1:
        - t2i-imagen3
        - image-analysis
    - pipeline-2:
        - t2i-sdxl
        - image-analysis
    - pipeline-3:
        - image-t2i (fal-imagen4)
        - image-analysis
  
  - select-best-image (custom logic)
  - i2i-flux-kontext (style refinement)
  - fal-upload
```

### パターンE: バナー広告制作
**用途**: 複数サイズのバナー一括生成
**参考モジュール**: `orchestrator-banner-advertisement-creation.yml`

```yaml
name: banner-ad-production
units:
  - banner-planning
  - web-search (competitor analysis)
  
  # ベース画像生成
  - t2i-imagen3 (high quality)
  - i2i-flux-kontext (brand style)
  
  # サイズ別展開（並列）
  parallel_for_each_size: [1200x628, 300x250, 728x90]
    - banner-text
    - image-analysis
    - fal-upload
  
  - markdown-summary
  - pdf-create (presentation)
```

## 📰 コンテンツ制作パターン

### パターンF: ニュース動画制作
**用途**: 最新ニュースの動画化
**参考モジュール**: `orchestrator-news-video-generation.yml`

```yaml
name: news-video-production
units:
  # Phase 1: 情報収集
  - web-search (multiple queries)
  - news-summary
  - news-planning
  
  # Phase 2: ビジュアル生成
  parallel:
    - thumbnail:
        - t2i-imagen3 (news style)
    - background-videos:
        - t2v-veo3 (abstract backgrounds)
  
  # Phase 3: ナレーション
  - t2s-google (news anchor voice)
  - srt-make
  
  # Phase 4: 編集
  - title-composition
  - subtitle-overlay
  - bgm-overlay (news theme)
  - video-concat
  
  # Phase 5: 配信
  - video-analysis
  - fal-upload
  - sns-publish
```

### パターンG: ブログ記事制作
**用途**: SEO最適化されたブログ記事
**参考モジュール**: `module-article-creation-ccsdk.yml`

```yaml
name: blog-article-production
units:
  - web-search (research)
  - article-generation
  - blog-generation
  
  # ビジュアル素材
  parallel:
    - hero-image:
        - t2i-sdxl
    - infographics:
        - data-visualization
  
  - markdown-summary
  - pdf-create
  - sns-publish (social sharing)
```

## 📊 データ駆動型パターン

### パターンH: データ分析レポート
**用途**: データの可視化とレポート生成
**参考モジュール**: `orchestrator-data-analysis-visualization.yml`

```yaml
name: data-analysis-report
units:
  - data-analysis
  - data-visualization
  
  # レポート生成
  parallel:
    - slide-deck:
        - slide-generation
        - pdf-create
    - video-report:
        - planning-ccsdk (data story)
        - t2v-wan (chart animations)
        - t2s-openai (narration)
        - video-concat
  
  - markdown-summary
  - git-pr-create
```

## 🔄 ハイブリッドパターン

### パターンI: マルチメディアキャンペーン
**用途**: 統合マーケティングキャンペーン
**参考オーケストレーター**: `orchestrator-multimedia-ad-campaign.yml`

```yaml
name: multimedia-campaign
parallel_tracks:
  - video-track:
      - planning-ccsdk
      - t2v-veo3
      - v2v-creatify (product placement)
      - upscale-topaz
      
  - image-track:
      - banner-planning
      - t2i-imagen3 (multiple variations)
      - banner-text
      
  - audio-track:
      - t2s-elevenlabs (brand voice)
      - bgm-generate (jingle)
      - audio-analysis
      
  - social-track:
      - i2i-flux-kontext (social formats)
      - v2v-luma-ray2 (style variations)
      - sns-publish

# 統合フェーズ
integration:
  - video-concat (compilation)
  - markdown-summary (campaign report)
  - pdf-create (presentation)
  - git-pr-create
```

## 🛡️ エラーハンドリングパターン

### パターンJ: フェイルセーフ動画制作
```yaml
name: failsafe-video-production
units:
  - planning-ccsdk
  
  # 画像生成（フォールバック付き）
  - try:
      - t2i-imagen3
    catch:
      - t2i-sdxl
    finally:
      - image-analysis
  
  # リップシンク（クォータチェック付き）
  - pixverse-quota-guard
  - if_quota_available:
      - lipsync-pixverse
    else:
      - subtitle-overlay (text only)
  
  # アップスケール（オプション）
  - if_quality_low:
      - upscale-topaz
  
  - video-analysis
  - quality_check:
      if_score < 70:
        - retry_with_different_params
```

## 💡 ベストプラクティス

### 1. 並列化の活用
```yaml
# Good: 独立したタスクは並列実行
parallel:
  - image-generation
  - audio-generation
  - bgm-generation

# Bad: 依存関係があるタスクの並列化
parallel:
  - image-generation
  - video-generation  # 画像が必要！
```

### 2. 適切なモデル選択
```yaml
# 用途別モデル選択
portraits: t2i-imagen3
artistic: t2i-sdxl  
photorealistic: image-t2i (fal-imagen4)
```

### 3. リソース管理
```yaml
# 大きなファイルは早めにアップロード
- video-generation
- fal-upload  # すぐにアップロード
- other-processing  # その後で他の処理
```

### 4. 品質保証
```yaml
# 各段階で品質チェック
- image-generation
- image-analysis  # 品質確認
- video-generation
- video-analysis  # 品質確認
```

## 📝 カスタマイズのヒント

1. **目的に応じたユニット選択**: 必要な機能だけを選ぶ
2. **パラメータ調整**: 各ユニットのオプションを活用
3. **条件分岐の活用**: 状況に応じた処理の切り替え
4. **エラーハンドリング**: 適切なフォールバック処理
5. **ログとモニタリング**: 実行状況の可視化

このパターンカタログを参考に、目的に最適なワークフローを構築してください。