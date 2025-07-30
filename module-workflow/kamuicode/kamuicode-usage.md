# kamuicode使用方法

## 使用方法
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__t2i-fal-imagen4-fast__imagen4_fast_submit,mcp__t2i-fal-imagen4-fast__imagen4_fast_status,mcp__t2i-fal-imagen4-fast__imagen4_fast_result,Bash" -p "プロンプト"
```

## モデル特徴一覧（参考）

### 画像生成モデル
| モデル名 | 特徴 | 生成速度 | 解像度 | 用途 |
|---------|------|----------|--------|------|
| Google Imagen3 | 高品質・写実的、プロンプト理解力が高い | 中速 | 1024x1024 | 汎用・高品質画像 |
| Imagen4 Ultra | 最高品質、細部まで精密 | 遅い | 最大2048x2048 | アート作品・商用 |
| Imagen4 Fast | バランス型、安定した品質 | 高速 | 1024x1024 | 日常使用・プロトタイプ |
| Flux-1 Schnell | 超高速生成 | 超高速(1-2秒) | 1024x1024 | 即座の確認・ラフ案 |
| Rundiffusion Photo Flux | フォトリアリスティック特化 | 中速 | 高解像度対応 | 人物・風景写真風 |

### 動画生成モデル
| モデル名 | 特徴 | 生成速度 | 解像度/長さ | 用途 |
|---------|------|----------|------------|------|
| Veo3 Fast | テキストから動画、自然な動き | 高速 | 720p/4-6秒 | SNS・プレゼン |
| Hailuo-02 Pro | 画像から動画、高品質 | 中速 | 1080p/4-6秒 | 商用・高品質動画 |
| Luma Ray2 | 動画編集・スタイル変換 | 中速 | 元動画依存 | 動画の修正・変換 |
| Vidu Q1 | 参照動画からの生成 | 中速 | 720p/4秒 | スタイル模倣 |
| Creatify Lipsync | リアルなリップシンク動画 | 高速 | 元動画依存 | トーキングヘッド・プレゼン動画 |
| Pixverse Lipsync | Pixverseリップシンク特化、制限厳格 | 中速 | 制限：5MB/30秒 | 高品質リップシンク（制限内） |

### その他のモデル
| モデル名 | 特徴 | 生成速度 | 出力形式 | 用途 |
|---------|------|----------|----------|------|
| Flux Kontext Max | 画像の高品質化・変換 | 高速 | 画像 | 画像補正・スタイル変換 |
| Flux Kontext LoRA | LoRAサポート付き画像編集 | 高速 | 画像 | 特定スタイル適用・カスタマイズ |
| Hunyuan3D v2.1 | 画像から3Dモデル生成 | 遅い | GLB/OBJ | 3Dモデリング・ゲーム |
| Google Lyria | 高品質音楽生成 | 中速 | MP3/WAV | BGM・効果音 |
| ThinkSound | 動画に合う音声生成 | 高速 | MP3 | 動画音響効果 |
| MiniMax Speech-02 Turbo | 超高速音声合成 | 超高速 | MP3/WAV | ナレーション・読み上げ |
| MiniMax Voice Design | 高品質音声合成・デザイン | 中速 | MP3/WAV | プロ品質音声・キャラクター音声 |
| Bria Background Removal | 動画背景削除 | 中速 | 透過動画 | 動画合成・クロマキー |
| Flux Kontext Trainer | LoRAモデル訓練 | 遅い | LoRA | カスタムモデル作成 |

## 利用可能ツール
### 画像生成
- `mcp__t2i-google-imagen3__imagen_t2i` - Google Imagen3 画像生成（一括実行）
- `mcp__t2i-fal-imagen4-ultra__imagen4_ultra_submit` - Fal.ai Imagen4 Ultra 画像生成開始
- `mcp__t2i-fal-imagen4-ultra__imagen4_ultra_status` - Fal.ai Imagen4 Ultra 生成ステータス確認
- `mcp__t2i-fal-imagen4-ultra__imagen4_ultra_result` - Fal.ai Imagen4 Ultra 生成結果取得
- `mcp__t2i-fal-imagen4-fast__imagen4_fast_submit` - Fal.ai Imagen4 Fast 画像生成開始
- `mcp__t2i-fal-imagen4-fast__imagen4_fast_status` - Fal.ai Imagen4 Fast 生成ステータス確認
- `mcp__t2i-fal-imagen4-fast__imagen4_fast_result` - Fal.ai Imagen4 Fast 生成結果取得
- `mcp__t2i-fal-flux-schnell__flux_schnell_submit` - Fal.ai Flux-1 Schnell 画像生成開始（高速）
- `mcp__t2i-fal-flux-schnell__flux_schnell_status` - Fal.ai Flux-1 Schnell 生成ステータス確認
- `mcp__t2i-fal-flux-schnell__flux_schnell_result` - Fal.ai Flux-1 Schnell 生成結果取得
- `mcp__t2i-fal-rundiffusion-photo-flux__rundiffusion_photo_flux_submit` - Fal.ai Rundiffusion Photo Flux 画像生成開始（フォトリアリスティック）
- `mcp__t2i-fal-rundiffusion-photo-flux__rundiffusion_photo_flux_status` - Fal.ai Rundiffusion Photo Flux 生成ステータス確認
- `mcp__t2i-fal-rundiffusion-photo-flux__rundiffusion_photo_flux_result` - Fal.ai Rundiffusion Photo Flux 生成結果取得

### 画像変換
- `mcp__i2i-fal-flux-kontext-max__flux_kontext_submit` - 画像変換開始（高品質化）
- `mcp__i2i-fal-flux-kontext-max__flux_kontext_status` - 変換ステータス確認
- `mcp__i2i-fal-flux-kontext-max__flux_kontext_result` - 変換結果取得
- `mcp__i2i-fal-flux-kontext-lora__flux_kontext_submit` - LoRA付き画像変換開始
- `mcp__i2i-fal-flux-kontext-lora__flux_kontext_status` - LoRA変換ステータス確認
- `mcp__i2i-fal-flux-kontext-lora__flux_kontext_result` - LoRA変換結果取得

### 動画生成
- `mcp__t2v-fal-veo3-fast__veo3_fast_submit` - テキストから動画生成開始
- `mcp__t2v-fal-veo3-fast__veo3_fast_status` - 動画生成ステータス確認
- `mcp__t2v-fal-veo3-fast__veo3_fast_result` - 動画生成結果取得
- `mcp__i2v-fal-hailuo-02-pro__hailuo_02_submit` - 画像から動画生成開始
- `mcp__i2v-fal-hailuo-02-pro__hailuo_02_status` - 動画生成ステータス確認
- `mcp__i2v-fal-hailuo-02-pro__hailuo_02_result` - 動画生成結果取得

### 動画変換
- `mcp__v2v-fal-luma-ray2-modify__luma_ray2_submit` - 動画変換開始
- `mcp__v2v-fal-luma-ray2-modify__luma_ray2_status` - 変換ステータス確認
- `mcp__v2v-fal-luma-ray2-modify__luma_ray2_result` - 変換結果取得
- `mcp__v2v-fal-bria-background-removal__submit` - 動画背景削除開始
- `mcp__v2v-fal-bria-background-removal__status` - 背景削除ステータス確認
- `mcp__v2v-fal-bria-background-removal__result` - 背景削除結果取得
- `mcp__v2v-fal-creatify-lipsync__lipsync_submit` - リップシンク動画生成開始
- `mcp__v2v-fal-creatify-lipsync__lipsync_status` - リップシンク生成ステータス確認
- `mcp__v2v-fal-creatify-lipsync__lipsync_result` - リップシンク生成結果取得
- `mcp__v2v-fal-pixverse-lipsync__pixverse_lipsync_submit` - Pixverseリップシンク生成開始（制限: 5MB動画/30秒音声）
- `mcp__v2v-fal-pixverse-lipsync__pixverse_lipsync_status` - Pixverseリップシンク生成ステータス確認
- `mcp__v2v-fal-pixverse-lipsync__pixverse_lipsync_result` - Pixverseリップシンク生成結果取得

### 音楽生成
- `mcp__t2m-google-lyria__lyria_generate` - Google Lyria音楽生成（一括実行）

### 動画から音声生成
- `mcp__v2a-fal-thinksound__thinksound_submit` - 動画から音声生成開始
- `mcp__v2a-fal-thinksound__thinksound_status` - 生成ステータス確認
- `mcp__v2a-fal-thinksound__thinksound_result` - 生成結果取得

### 参照動画生成
- `mcp__r2v-fal-vidu-q1__vidu_q1_submit` - 参照動画生成開始
- `mcp__r2v-fal-vidu-q1__vidu_q1_status` - 生成ステータス確認
- `mcp__r2v-fal-vidu-q1__vidu_q1_result` - 生成結果取得

### 3D生成
- `mcp__i2i3d-fal-hunyuan3d-v21__hunyuan3d_submit` - 画像から3Dモデル生成開始
- `mcp__i2i3d-fal-hunyuan3d-v21__hunyuan3d_status` - 3D生成ステータス確認
- `mcp__i2i3d-fal-hunyuan3d-v21__hunyuan3d_result` - 3D生成結果取得

### 音声生成
- `mcp__t2s-fal-minimax-speech-02-turbo__minimax_speech_02_turbo_submit` - テキストから音声生成開始（超高速）
- `mcp__t2s-fal-minimax-speech-02-turbo__minimax_speech_02_turbo_status` - 音声生成ステータス確認
- `mcp__t2s-fal-minimax-speech-02-turbo__minimax_speech_02_turbo_result` - 音声生成結果取得
- `mcp__v2v-fal-minimax-voice-design__voice_design_submit` - MiniMax Voice Design音声生成開始（高品質T2S）
- `mcp__v2v-fal-minimax-voice-design__voice_design_status` - Voice Design音声生成ステータス確認
- `mcp__v2v-fal-minimax-voice-design__voice_design_result` - Voice Design音声生成結果取得

### モデル訓練
- `mcp__train-fal-flux-kontext-trainer__flux_kontext_trainer_submit` - LoRAモデル訓練開始
- `mcp__train-fal-flux-kontext-trainer__flux_kontext_trainer_status` - 訓練ステータス確認
- `mcp__train-fal-flux-kontext-trainer__flux_kontext_trainer_result` - 訓練済みモデル取得

## 重要な注意点
### 動画生成時の必須事項
1. **Google URLの有効期限**: 約1時間で期限切れ
2. **連続実行必須**: 画像生成→動画生成→ダウンロードを中断せずに実行
3. **ローカルファイルパス禁止**: 必ずGoogle提供の認証済URLを使用
4. **全権限を事前付与**: submit/status/result/Bashを最初から許可

### 動画生成の正しい手順
**一括実行は5分以上かかりタイムアウトするため、段階的実行が必要：**

1. **画像生成**
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__t2i-fal-imagen4-fast__imagen4_fast_submit,mcp__t2i-fal-imagen4-fast__imagen4_fast_status,mcp__t2i-fal-imagen4-fast__imagen4_fast_result,Bash" -p "画像生成してGoogle URL取得"
```

2. **動画生成開始**
```bash  
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__i2v-fal-hailuo-02-pro__hailuo_02_submit" -p "Google URL使用して動画生成開始"
```

3. **ステータス確認**（数分後）
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__i2v-fal-hailuo-02-pro__hailuo_02_status" -p "リクエストIDステータス確認"
```

4. **動画ダウンロード・再生**
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__i2v-fal-hailuo-02-pro__hailuo_02_result,Bash" -p "動画ダウンロード・再生"
```

### 音楽生成の正しい手順
**Google Lyriaは一括実行可能：**

1. **音楽生成**
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__t2m-google-lyria__lyria_generate,Bash" -p "音楽生成してローカル保存"
```

**重要**: 音楽生成は段階的実行（submit/status/result）ではなく、`lyria_generate`での一括実行が正しい方法です。

### Pixverseリップシンクの正しい手順
**Pixverseは厳格な制限があるため、事前チェックが必須：**

#### 制限事項
- **動画サイズ**: 5MB以下必須
- **音声長さ**: 30秒以内必須
- **動画形式**: MP4推奨
- **音声形式**: MP3/WAV対応

#### 1. 事前チェック
```bash
# 動画サイズ確認（5MB以下必須）
claude --allowedTools "Bash" -p "動画ファイルサイズ確認: [動画URL]が5MB以下かチェック"

# 音声長さ確認（30秒以内必須）
claude --allowedTools "Bash" -p "音声ファイル長さ確認: [音声URL]が30秒以内かチェック"
```

#### 2. Pixverseリップシンク生成開始
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__v2v-fal-pixverse-lipsync__pixverse_lipsync_submit" -p "Pixverseリップシンク開始: 動画URL=[動画URL] 音声URL=[音声URL]"
```

#### 3. ステータス確認（2-3分後）
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__v2v-fal-pixverse-lipsync__pixverse_lipsync_status" -p "Pixverseリップシンクステータス確認: リクエストID=[ID]"
```

#### 4. 結果ダウンロード・再生
```bash
claude --mcp-config=.claude/mcp-kamuicode.json --allowedTools "mcp__v2v-fal-pixverse-lipsync__pixverse_lipsync_result,Bash" -p "Pixverseリップシンク結果取得・再生: リクエストID=[ID]"
```

#### ⚠️ 重要な注意点
- **制限超過時**: エラーで処理停止、制限内に収める必要あり
- **品質最適化**: 短時間・小サイズでも高品質リップシンクを実現
- **セグメント分割**: 長い動画は複数セグメントに分割して処理
- **事前検証**: 必ず制限チェックしてから実行すること


## t2s-fal-minimax-speech-02-turbo 音声オプション設定

  音声ID (voice_id)

  - Wise_Woman (賢明な女性)
  - Friendly_Person (親しみやすい人)
  - Inspirational_girl (インスピレーショナルな女の子)
  - Deep_Voice_Man (低い声の男性)
  - Calm_Woman (落ち着いた女性)
  - Casual_Guy (カジュアルな男性)
  - Lively_Girl (活発な女の子)
  - Patient_Man (忍耐強い男性)
  - Young_Knight (若い騎士)
  - Determined_Man (決意のある男性)
  - Lovely_Girl (可愛らしい女の子)
  - Decent_Boy (きちんとした男の子)
  - Imposing_Manner (威厳のある態度)
  - Elegant_Man (優雅な男性)
  - Abbess (女子修道院長)
  - Sweet_Girl_2 (甘い女の子2)
  - Exuberant_Girl (陽気な女の子)

  感情設定 (emotion)

  happy, sad, angry, fearful, disgusted, surprised, neutral

  音声品質設定

  - speed: 0.5-2.0 (話速)
  - pitch: -12〜12 (音程)
  - vol: 0-10 (音量)
  - language_boost: Chinese, English, Japanese, auto
  - format: mp3, pcm, flac
  - sample_rate: 8000, 16000, 22050, 24000, 32000, 44100
  - english_normalization: true/false