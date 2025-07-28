# Claude MCP Helper Functions

このファイルは、Claude CodeでMCPツールを使用する際の便利な設定やヘルパー関数をまとめています。

## デフォルト出力ディレクトリ

### 画像生成時
```
output_directory: "./cli_generated/media/images"
filename_prefix: "claude_generated"
auto_open: true
```

### 動画生成時
```
output_directory: "./cli_generated/media/videos"
filename_prefix: "claude_generated"
auto_open: true
```

### 音声生成時
```
output_directory: "./cli_generated/media/audio"
filename_prefix: "claude_generated"
auto_open: true
```

### 3Dモデル生成時  
```
output_directory: "./cli_generated/media/3d"
filename_prefix: "claude_generated"
auto_open: true
```

## 使用例

### 画像生成（Imagen4 Fast）
```yaml
mcp__t2i-fal-imagen4-fast__imagen4_fast_submit:
  prompt: "your prompt here"
  output_directory: "./cli_generated/media/images"
  filename_prefix: "claude_img"
  aspect_ratio: "1:1"
  num_images: 1
```

### 動画生成（I2V Hailuo-02）
```yaml
mcp__i2v-fal-hailuo-02-pro__hailuo_02_submit:
  image_url: "image_url_here"
  prompt: "your animation prompt"
  output_directory: "./cli_generated/media/videos"
  filename_prefix: "claude_video"
```

### 音声生成（MiniMax Speech）
```yaml
mcp__t2s-fal-minimax-speech-02-turbo__minimax_speech_02_turbo_submit:
  text: "your text here"
  output_directory: "./cli_generated/media/audio"
  filename_prefix: "claude_audio"
```

## 注意事項

- 必ず `./cli_generated/media/` 配下を使用する
- GitHub Actionsの `./generated/media/` とは区別する
- ファイル名にプレフィックスを付けて識別しやすくする