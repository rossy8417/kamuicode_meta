# 最小単位ユニット依存関係マップ

このドキュメントは、メタワークフローで新しいワークフローを作成する際の参照ガイドです。
最小単位ユニット → モジュール → オーケストレーターの依存関係と組み合わせパターンを示します。

## 📋 目次

1. [基本構造](#基本構造)
2. [ユニットカテゴリ別一覧](#ユニットカテゴリ別一覧)
3. [典型的な組み合わせパターン](#典型的な組み合わせパターン)
4. [オーケストレーター実装例](#オーケストレーター実装例)
5. [依存関係フローチャート](#依存関係フローチャート)

## 基本構造

```
オーケストレーター（最上位）
  └── モジュール（中間層）
      └── 最小単位ユニット（基本要素）
```

### レイヤー説明
- **最小単位ユニット**: 単一の機能を実行する最小コンポーネント
- **モジュール**: 複数のユニットを組み合わせた機能グループ
- **オーケストレーター**: 複数のモジュールを調整して完全なワークフローを実現

## ユニットカテゴリ別一覧

### 🎯 企画・計画系ユニット
```yaml
planning/:
  - planning-ccsdk.yml         # AI動画制作計画立案
  - web-search.yml            # Web検索
  - article-generation.yml    # 記事生成
  - markdown-summary.yml      # Markdownサマリー生成

news/:
  - news-planning.yml         # ニュース制作計画
  - news-summary.yml          # ニュース要約

banner/:
  - banner-planning.yml       # バナー制作計画

blog/:
  - blog-generation.yml       # ブログ記事生成

presentation/:
  - slide-generation.yml      # スライド生成
```

### 🖼️ 画像系ユニット
```yaml
image/:
  - image-t2i.yml             # 汎用Text-to-Image
  - t2i-imagen3.yml           # Google Imagen3
  - t2i-sdxl.yml              # Stable Diffusion XL
  - i2i-flux-kontext.yml      # Flux Kontext画像変換
  - banner-text.yml           # バナーテキストオーバーレイ
  - image-analysis.yml        # 画像分析
```

### 🎥 動画系ユニット
```yaml
video/:
  - video-generation.yml      # 汎用動画生成（i2v/t2v）
  - t2v-veo3.yml             # FAL Veo3 T2V
  - t2v-wan.yml              # FAL WAN V2 T2V
  - i2v-seedance.yml         # ByteDance SeedDance I2V
  - r2v-vidu.yml             # FAL Vidu Q1 R2V
  - v2v-luma-ray2.yml        # Luma Ray2動画変換
  - v2v-creatify.yml         # Creatifyリップシンク
  - upscale-topaz.yml        # Topazアップスケール
  - title-composition.yml     # タイトルフレーム合成
  - video-prompt-opt.yml      # 動画プロンプト最適化
  - video-analysis.yml        # 動画分析
```

### 🔊 音声系ユニット
```yaml
audio/:
  - audio-minimax.yml         # MiniMax音声生成
  - audio-elevenlabs.yml      # ElevenLabs音声生成
  - t2s-google.yml           # Google TTS
  - t2s-openai.yml           # OpenAI TTS
  - t2s-minimax-turbo.yml    # MiniMax Turbo
  - t2s-minimax-voice.yml    # MiniMax Voice Design
  - bgm-generate.yml         # BGM生成
  - bgm-overlay.yml          # BGMオーバーレイ
  - wav-segmentation.yml     # 音声セグメンテーション
```

### 👄 リップシンク系ユニット
```yaml
lipsync/:
  - lipsync-pixverse.yml      # Pixverseリップシンク
  - pixverse-quota-guard.yml  # Pixverse利用枠チェック
  - srt-make.yml             # SRT字幕生成
  - subtitle-overlay.yml      # 字幕オーバーレイ

subtitle/:
  - srt-translate.yml        # SRT翻訳
  - srt-sync.yml             # SRTタイミング同期
```

### 🔧 アセンブリ系ユニット
```yaml
assembly/:
  - video-concat.yml         # 動画連結
  - fal-upload.yml          # FALアップロード
```

### 📊 データ系ユニット
```yaml
data/:
  - data-analysis.yml        # データ分析
  - data-visualization.yml   # データ可視化
```

### 🔗 外部連携系ユニット
```yaml
external/:
  - git-pr-create.yml        # GitHubプルリクエスト作成
  - pdf-create.yml          # PDF作成
  - sns-publish.yml         # SNS投稿

git-ops/:
  - git-branch-setup.yml     # Gitブランチセットアップ
  - cleanup-branch.yml       # ブランチクリーンアップ
```

### 🎨 3D系ユニット
```yaml
3d/:
  - i2i3d-hunyuan.yml       # HunYuan3D画像→3Dモデル
```

## 典型的な組み合わせパターン

### パターン1: AI動画制作（基本）
```yaml
workflow: AI動画制作基本フロー
steps:
  1. git-branch-setup        # ブランチ準備
  2. planning-ccsdk          # 企画立案
  3. image-t2i               # 画像生成
  4. video-generation        # 動画生成（i2v）
  5. audio-minimax           # 音声生成
  6. subtitle-overlay        # 字幕合成
  7. video-concat            # 動画連結
  8. fal-upload             # アップロード
  9. git-pr-create          # PR作成
```

### パターン2: リップシンク動画制作
```yaml
workflow: リップシンク動画制作フロー
steps:
  1. git-branch-setup        # ブランチ準備
  2. planning-ccsdk          # 企画立案
  3. image-t2i               # 人物画像生成
  4. video-generation        # ベース動画生成
  5. audio-minimax           # 音声生成
  6. pixverse-quota-guard    # 利用枠確認
  7. lipsync-pixverse        # リップシンク生成
  8. srt-make               # 字幕生成
  9. subtitle-overlay        # 字幕オーバーレイ
  10. video-concat          # 最終動画結合
  11. fal-upload            # アップロード
```

### パターン3: ニュース動画制作
```yaml
workflow: ニュース動画制作フロー
steps:
  1. web-search             # 情報収集
  2. news-planning          # ニュース企画
  3. news-summary           # 要約作成
  4. image-t2i              # サムネイル生成
  5. video-generation       # 動画生成
  6. t2s-google            # ナレーション生成
  7. bgm-generate          # BGM生成
  8. bgm-overlay           # BGMミックス
  9. title-composition     # タイトル挿入
  10. video-analysis       # 品質確認
```

### パターン4: バナー広告制作
```yaml
workflow: バナー広告制作フロー
steps:
  1. banner-planning        # バナー企画
  2. image-t2i              # ベース画像生成
  3. i2i-flux-kontext      # スタイル変換
  4. banner-text           # テキストオーバーレイ
  5. image-analysis        # 品質確認
  6. fal-upload            # アップロード
```

### パターン5: データ分析レポート
```yaml
workflow: データ分析レポートフロー
steps:
  1. data-analysis         # データ分析
  2. data-visualization    # グラフ生成
  3. markdown-summary      # サマリー作成
  4. slide-generation      # スライド生成
  5. pdf-create           # PDF出力
```

## オーケストレーター実装例

### 例1: 動画コンテンツ制作オーケストレーター
```yaml
name: video-content-orchestrator
description: 動画コンテンツ制作の完全自動化

modules:
  - planning-module:
      units:
        - planning-ccsdk
        - web-search
        - article-generation
      
  - image-generation-module:
      units:
        - image-t2i (parallel)
        - image-analysis
        - video-prompt-opt
      
  - video-production-module:
      units:
        - video-generation
        - v2v-luma-ray2 (optional)
        - upscale-topaz (optional)
      
  - audio-production-module:
      units:
        - audio-minimax
        - bgm-generate
        - bgm-overlay
      
  - post-production-module:
      units:
        - srt-make
        - subtitle-overlay
        - title-composition
        - video-concat
      
  - delivery-module:
      units:
        - video-analysis
        - fal-upload
        - git-pr-create
```

### 例2: マルチメディア広告キャンペーン
```yaml
name: multimedia-ad-campaign-orchestrator
description: 複数メディア向け広告素材の一括制作

parallel-modules:
  - video-ad-module:
      units:
        - planning-ccsdk
        - t2v-veo3
        - audio-elevenlabs
        - video-concat
      
  - banner-ad-module:
      units:
        - banner-planning
        - t2i-imagen3 (multiple sizes)
        - banner-text
      
  - social-media-module:
      units:
        - t2i-sdxl (square format)
        - v2v-creatify
        - sns-publish
      
  - documentation-module:
      units:
        - markdown-summary
        - pdf-create
```

## 依存関係フローチャート

### 基本的な依存関係
```
[Git Setup] → [Planning] → [Content Generation] → [Post-Production] → [Delivery]
     ↓            ↓                ↓                      ↓                ↓
git-branch    planning-*      image/video/audio      assembly/*       upload/PR
```

### 並列実行可能なユニット
```
                    ┌─→ image-t2i ─┐
planning-ccsdk ─────┼─→ t2s-*     ─┼─→ assembly
                    └─→ bgm-*     ─┘
```

### 条件付き実行
```
pixverse-quota-guard ─→ (quota OK?) ─→ lipsync-pixverse
                            ↓
                        (quota NG) ─→ fallback to subtitle-only
```

## 使用上の注意事項

### 1. 必須の前提条件
- Git操作系は常に最初に実行
- ファイルアップロードは最後に実行
- 分析系は生成後に実行

### 2. 並列実行の推奨
- 画像・音声・BGM生成は並列実行可能
- 異なるサイズのバナーは並列生成推奨
- Web検索と企画は並列実行可能

### 3. エラーハンドリング
- quota-guard系は必ず使用前にチェック
- video-analysisで品質確認
- 各ステップでのリトライ設定

### 4. リソース最適化
- 大きなファイルは早めにアップロード
- 不要な中間ファイルはクリーンアップ
- 並列度は実行環境に応じて調整

## メタワークフロー作成のベストプラクティス

1. **目的を明確に定義**: 何を作りたいかを具体的に決める
2. **既存パターンを参考に**: 類似のワークフローパターンから始める
3. **最小構成から開始**: 必要最小限のユニットから始めて拡張
4. **並列化を活用**: 独立したタスクは並列実行で高速化
5. **エラー処理を追加**: 各ステップに適切なエラーハンドリング
6. **品質確認を組み込む**: analysis系ユニットで品質チェック
7. **ドキュメント化**: markdown-summaryで実行結果を記録

このマップを参照しながら、目的に応じた最適なワークフローを構築してください。