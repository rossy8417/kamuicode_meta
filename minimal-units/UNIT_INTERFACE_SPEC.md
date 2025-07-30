# 最小単位ユニット インターフェース仕様書

このドキュメントは、各最小単位ユニットの入出力インターフェースを定義し、ユニット間の接続方法を明確にします。

## 📐 基本インターフェース構造

### 標準入力パラメータ
```yaml
inputs:
  # 必須: 処理対象のファイルパスまたはコンテンツ
  [target]_path/[target]:
    required: true
    type: string
    
  # 必須: 出力先ディレクトリ
  output_dir:
    required: true
    type: string
    
  # オプション: 処理パラメータ
  [parameter_name]:
    required: false
    type: string/boolean/number
    default: [default_value]
```

### 標準出力パラメータ
```yaml
outputs:
  # 必須: 生成されたファイルパス
  [result]_path:
    value: ${{ jobs.[job_name].outputs.[result]_path }}
    
  # オプション: 処理結果のURL
  [result]_url:
    value: ${{ jobs.[job_name].outputs.[result]_url }}
    
  # オプション: メタデータ
  [metadata]:
    value: ${{ jobs.[job_name].outputs.[metadata] }}
```

## 🔗 ユニット接続パターン

### パターン1: 直列接続
```yaml
# Unit A の出力を Unit B の入力に接続
unit_a:
  outputs:
    image_path: /path/to/image.png

unit_b:
  inputs:
    image_path: ${{ needs.unit_a.outputs.image_path }}
```

### パターン2: 並列処理
```yaml
# 複数ユニットを並列実行
parallel_units:
  strategy:
    matrix:
      unit: [unit_a, unit_b, unit_c]
  uses: ./.github/workflows/${{ matrix.unit }}.yml
```

### パターン3: 条件分岐
```yaml
# 条件に応じてユニットを選択
if: ${{ needs.check_unit.outputs.condition == 'true' }}
uses: ./.github/workflows/unit_a.yml
else:
uses: ./.github/workflows/unit_b.yml
```

## 📊 カテゴリ別インターフェース詳細

### 🎯 企画・計画系

#### planning-ccsdk
```yaml
inputs:
  concept: string          # ユーザーコンセプト
  output_dir: string       # 出力ディレクトリ
  model_preference: string # モデル優先度
outputs:
  plan_path: string        # 企画書パス
  image_prompts: array     # 画像プロンプト配列
  video_concepts: array    # 動画コンセプト配列
  audio_scripts: array     # 音声スクリプト配列
```

#### web-search
```yaml
inputs:
  query: string           # 検索クエリ
  output_dir: string      # 出力ディレクトリ
  max_results: string     # 最大結果数
outputs:
  search_results: string  # 検索結果
  sources: string         # ソースURL一覧
  summary: string         # サマリー
```

### 🖼️ 画像系

#### image-t2i / t2i-* variants
```yaml
inputs:
  prompt: string          # 画像生成プロンプト
  output_dir: string      # 出力ディレクトリ
  negative_prompt: string # ネガティブプロンプト
  width: string          # 画像幅
  height: string         # 画像高さ
outputs:
  image_path: string     # 生成画像パス
  image_url: string      # 画像URL
```

#### i2i-flux-kontext
```yaml
inputs:
  image_path: string     # 入力画像パス
  prompt: string         # 変換プロンプト
  output_dir: string     # 出力ディレクトリ
  strength: string       # 変換強度
outputs:
  image_path: string     # 変換画像パス
  image_url: string      # 画像URL
```

### 🎥 動画系

#### video-generation
```yaml
inputs:
  mode: string           # 生成モード (i2v/t2v)
  input_path: string     # 入力パス（画像/プロンプト）
  prompt: string         # 動画プロンプト
  output_dir: string     # 出力ディレクトリ
outputs:
  video_path: string     # 生成動画パス
  video_url: string      # 動画URL
  metadata: object       # メタデータ
```

#### v2v-* variants
```yaml
inputs:
  video_path: string     # 入力動画パス
  output_dir: string     # 出力ディレクトリ
  [style_params]: varies # スタイルパラメータ
outputs:
  video_path: string     # 変換動画パス
  video_url: string      # 動画URL
```

### 🔊 音声系

#### audio-* / t2s-* variants
```yaml
inputs:
  text: string           # 音声化テキスト
  output_dir: string     # 出力ディレクトリ
  voice_id: string       # 音声ID/設定
  [voice_params]: varies # 音声パラメータ
outputs:
  audio_path: string     # 生成音声パス
  audio_url: string      # 音声URL
  duration: string       # 音声長さ
```

#### bgm-overlay
```yaml
inputs:
  video_path: string     # 入力動画パス
  bgm_path: string       # BGMファイルパス
  output_dir: string     # 出力ディレクトリ
  bgm_volume: string     # BGM音量
outputs:
  video_path: string     # BGM付き動画パス
```

### 👄 リップシンク系

#### lipsync-pixverse
```yaml
inputs:
  video_path: string     # 入力動画パス
  audio_path: string     # 音声ファイルパス
  output_dir: string     # 出力ディレクトリ
outputs:
  video_path: string     # リップシンク動画パス
  video_url: string      # 動画URL
  sync_score: string     # 同期スコア
```

#### subtitle-overlay
```yaml
inputs:
  video_path: string     # 入力動画パス
  srt_path: string       # SRTファイルパス
  output_dir: string     # 出力ディレクトリ
  style: object          # 字幕スタイル
outputs:
  video_path: string     # 字幕付き動画パス
```

### 🔧 アセンブリ系

#### video-concat
```yaml
inputs:
  video_paths: string    # 動画パス（カンマ区切り）
  output_dir: string     # 出力ディレクトリ
  bgm_path: string       # BGMパス（オプション）
outputs:
  video_path: string     # 連結動画パス
  total_duration: string # 総時間
```

#### fal-upload
```yaml
inputs:
  asset_path: string     # アップロードファイルパス
  output_dir: string     # 出力ディレクトリ
  asset_type: string     # アセットタイプ
outputs:
  asset_url: string      # アップロードURL
  upload_info: object    # アップロード情報
```

## 🔄 データフロー例

### 例1: 画像→動画→音声付き動画
```yaml
flow:
  1. planning-ccsdk
     outputs: image_prompt, video_concept, audio_script
     
  2. image-t2i
     inputs: prompt = image_prompt
     outputs: image_path
     
  3. video-generation
     inputs: mode = "i2v", input_path = image_path
     outputs: video_path
     
  4. audio-minimax
     inputs: text = audio_script
     outputs: audio_path
     
  5. subtitle-overlay
     inputs: video_path, audio_path
     outputs: final_video_path
```

### 例2: 並列生成→合成
```yaml
flow:
  1. planning-ccsdk
     outputs: prompts[], scripts[]
     
  2. parallel:
     - image-t2i (foreach prompt)
       outputs: image_paths[]
     - t2s-google (foreach script)
       outputs: audio_paths[]
       
  3. video-generation (foreach image)
     inputs: image_paths[]
     outputs: video_paths[]
     
  4. video-concat
     inputs: video_paths
     outputs: final_video_path
```

## ⚙️ パラメータ変換ガイド

### 文字列配列の受け渡し
```yaml
# 出力側: カンマ区切り文字列として出力
outputs:
  file_list: "file1.mp4,file2.mp4,file3.mp4"

# 入力側: カンマ区切り文字列として受け取り
inputs:
  video_paths: ${{ needs.previous.outputs.file_list }}
```

### JSONオブジェクトの受け渡し
```yaml
# 出力側: JSON文字列として出力
outputs:
  metadata: '{"width":1920,"height":1080,"fps":30}'

# 入力側: JSON文字列として受け取り、内部でパース
inputs:
  video_specs: ${{ needs.previous.outputs.metadata }}
```

### 条件付きパラメータ
```yaml
# デフォルト値を活用
inputs:
  quality: ${{ inputs.quality || 'standard' }}
  
# 条件による切り替え
inputs:
  model: ${{ inputs.fast_mode == 'true' && 't2i-sdxl' || 't2i-imagen3' }}
```

## 📋 チェックリスト

### ユニット作成時
- [ ] 必須入力パラメータを定義
- [ ] 必須出力パラメータを定義
- [ ] デフォルト値を適切に設定
- [ ] エラー時の出力を定義
- [ ] ドキュメントにインターフェースを記載

### ユニット接続時
- [ ] 出力と入力の型が一致
- [ ] 必須パラメータが提供されている
- [ ] エラーハンドリングが適切
- [ ] 並列実行の可否を確認
- [ ] リソース競合がないか確認

このインターフェース仕様を参照して、ユニット間の適切な接続を実現してください。