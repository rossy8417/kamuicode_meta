# MCP (Model Context Protocol) サービス一覧

このドキュメントでは、ニュース動画生成で使用するMCPサービスの詳細を説明します。

## 📋 サービス概要

MCPサービスは、Claude AIが外部のAI生成サービスと連携するためのプロトコルです。各サービスは特定のタスク（画像生成、音声生成など）に特化しています。

## 🎨 画像生成 (Text-to-Image)

### t2i-fal-imagen4-ultra ⭐
- **用途**: 高品質な画像生成
- **特徴**: 
  - 最高品質の出力
  - 詳細なプロンプト対応
  - 処理時間: 30-60秒
- **パラメータ**:
  ```python
  {
      "prompt": "詳細なプロンプト",
      "aspect_ratio": "16:9",  # 1:1, 9:16, 16:9, 3:4, 4:3
      "num_images": 1,         # 1-4
      "guidance_scale": 3.5,   # 1-20
      "safety_tolerance": 2    # 1-6
  }
  ```

### t2i-fal-imagen4-fast ⭐
- **用途**: 高速な画像生成
- **特徴**:
  - バランスの取れた品質と速度
  - 処理時間: 10-20秒
- **使用例**:
  ```python
  # タイトル画像の生成
  request_id = imagen4_fast_submit(
      prompt="Professional news title screen",
      aspect_ratio="16:9"
  )
  image_url = imagen4_fast_result(request_id)
  ```

## 🎬 動画生成 (Image-to-Video)

### i2v-fal-hailuo-02-pro ⭐
- **用途**: 静止画から高品質な動画を生成
- **特徴**:
  - プロフェッショナル品質
  - カメラワーク対応
  - 処理時間: 2-5分
- **パラメータ**:
  ```python
  {
      "image_url": "入力画像URL",
      "prompt": "動きの説明",
      "prompt_optimizer": True  # プロンプト最適化
  }
  ```

### i2v-fal-bytedance-seedance-v1-lite ⭐
- **用途**: 軽量・高速な動画生成
- **特徴**:
  - 短時間で結果を取得
  - 基本的な動きに対応
- **パラメータ**:
  ```python
  {
      "image_url": "入力画像URL",
      "prompt": "動きの説明",
      "duration": "10",        # 3-12秒
      "resolution": "720p",    # 480p, 720p, 1080p
      "camera_fixed": False    # カメラ固定
  }
  ```

## 🎙️ 音声生成 (Text-to-Speech)

### t2s-fal-minimax-speech-02-turbo ⭐
- **用途**: 自然な音声合成
- **特徴**:
  - 日本語完全対応
  - 多様な声質
  - 感情表現対応
- **パラメータ**:
  ```python
  {
      "text": "読み上げテキスト",
      "voice_id": "Calm_Woman",     # 声質選択
      "speed": 0.95,                # 0.5-2.0
      "pitch": 0,                   # -12 to 12
      "emotion": "neutral",         # happy, sad, angry等
      "language_boost": "Japanese"
  }
  ```
- **利用可能な声質**:
  - Calm_Woman (落ち着いた女性)
  - Friendly_Person (親しみやすい声)
  - Deep_Voice_Man (深い男性声)
  - Young_Knight (若い男性)
  - など17種類

## 👄 リップシンク (Video-to-Video)

### v2v-fal-creatify-lipsync ⭐
- **用途**: 音声に合わせた口の動き生成
- **特徴**:
  - 高速処理
  - 自然な口の動き
  - ループ対応
- **パラメータ**:
  ```python
  {
      "video_url": "キャラクター動画",
      "audio_url": "音声ファイル",
      "loop": True  # ループ再生
  }
  ```

### v2v-fal-pixverse-lipsync ⭐
- **用途**: 高品質リップシンク（代替）
- **特徴**:
  - より精密な口の動き
  - 表情変化対応

## 🎵 音楽生成 (Text-to-Music)

### t2m-google-lyria ⭐
- **用途**: BGM生成
- **特徴**:
  - 多様なジャンル対応
  - 指定秒数で生成
  - プロ品質の音楽
- **パラメータ**:
  ```python
  {
      "prompt": "音楽の説明",
      "duration": 60,          # 5-120秒
      "style": "electronic",   # classical, jazz等
      "tempo": "medium"        # slow, medium, fast
  }
  ```

## 🔄 その他の便利なサービス

### v2v-fal-bria-background-removal ⭐
- **用途**: 動画の背景除去
- **特徴**: 透明背景の動画生成

### i2i3d-fal-hunyuan3d-v21 ⭐
- **用途**: 画像から3Dモデル生成
- **特徴**: ニュースグラフィックス用

### train-fal-flux-kontext-trainer ⭐
- **用途**: カスタムLoRA学習
- **特徴**: 特定のスタイル学習

## 📝 使用上の注意

### API制限
- 各サービスには呼び出し制限があります
- 同時実行数に注意
- タイムアウト設定を適切に

### エラーハンドリング
```python
try:
    request_id = service.submit(params)
    # ステータス確認
    while True:
        status = service.status(request_id)
        if status == "COMPLETED":
            break
        elif status == "FAILED":
            raise Exception("生成失敗")
        time.sleep(5)
    
    result = service.result(request_id)
except Exception as e:
    # フォールバック処理
    print(f"エラー: {e}")
```

### 最適な組み合わせ

**高品質重視**:
- imagen4-ultra → hailuo-02-pro → creatify-lipsync

**速度重視**:
- imagen4-fast → bytedance-seedance → pixverse-lipsync

**バランス型**:
- imagen4-fast → hailuo-02-pro → creatify-lipsync

## 🚀 実践的なワークフロー

```python
# 1. 並列処理で時間短縮
async def generate_assets():
    tasks = [
        generate_title_image(),
        generate_anchor_image(),
        generate_bgm(),
        generate_narration()
    ]
    results = await asyncio.gather(*tasks)
    return results

# 2. フォールバック戦略
def generate_video_with_fallback(image):
    try:
        return hailuo_02_pro(image)
    except:
        return bytedance_seedance(image)

# 3. 品質チェック
def validate_generation(result):
    if result.size < 1000:  # 1KB未満
        raise ValueError("生成失敗の可能性")
    return result
```

## 📊 パフォーマンス指標

| サービス | 平均処理時間 | 成功率 | 推奨用途 |
|---------|------------|--------|---------|
| imagen4-ultra | 45秒 | 95% | ヒーロー画像 |
| imagen4-fast | 15秒 | 98% | 大量生成 |
| hailuo-02-pro | 180秒 | 90% | メイン動画 |
| minimax-speech | 10秒 | 99% | ナレーション |
| creatify-lipsync | 60秒 | 95% | キャラクター |
| google-lyria | 20秒 | 97% | BGM |