# 依存関係ドキュメント

このドキュメントでは、ニュース動画生成システムの全依存関係について詳しく説明します。

## 🐍 Python依存関係

### 必須パッケージ

```bash
pip install imageio-ffmpeg requests
```

#### imageio-ffmpeg
- **バージョン**: 0.4.0以上
- **用途**: FFmpegバイナリの自動ダウンロードと管理
- **理由**: システムにFFmpegがインストールされていない環境でも動作可能にする

```python
import imageio_ffmpeg
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
```

#### requests
- **バージョン**: 2.25.0以上
- **用途**: MCPサービスとのHTTP通信
- **理由**: API呼び出しとファイルダウンロード

### オプションパッケージ

```bash
# 高度な動画編集用
pip install moviepy==2.0.0  # 注: v2.xはAPIが大きく変更されている

# 画像処理用
pip install pillow numpy

# プログレスバー表示
pip install tqdm

# 設定管理
pip install python-dotenv pyyaml
```

## 🎥 システム依存関係

### FFmpeg

#### インストール方法

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**CentOS/RHEL:**
```bash
sudo yum install epel-release
sudo yum install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. [FFmpeg公式サイト](https://ffmpeg.org/download.html)からダウンロード
2. PATHに追加

#### 必要なコーデック

- **libx264**: H.264ビデオエンコード
- **aac**: AACオーディオエンコード
- **libmp3lame**: MP3エンコード（オプション）

### 日本語フォント（テキストオーバーレイ用）

**Ubuntu/Debian:**
```bash
sudo apt-get install fonts-noto-cjk
```

**macOS:**
```bash
brew tap homebrew/cask-fonts
brew install font-noto-sans-cjk-jp
```

## 🌐 MCP (Model Context Protocol) 依存関係

### 必要なMCPサービス

1. **画像生成**
   - `t2i-fal-imagen4-fast`: 高速画像生成
   - `t2i-fal-imagen4-ultra`: 高品質画像生成

2. **動画生成**
   - `i2v-fal-hailuo-02-pro`: プロ品質の画像→動画変換
   - `i2v-fal-bytedance-seedance-v1-lite`: 軽量版（代替）

3. **音声生成**
   - `t2s-fal-minimax-speech-02-turbo`: 日本語対応TTS

4. **動画編集**
   - `v2v-fal-creatify-lipsync`: リップシンク
   - `v2v-fal-pixverse-lipsync`: リップシンク（代替）

5. **音楽生成**
   - `t2m-google-lyria`: BGM生成

### MCP設定ファイル

`.claude/mcp-kamuicode.json`:
```json
{
  "mcpServers": {
    "t2i-fal-imagen4-fast": {
      "type": "http",
      "url": "https://mcp-endpoint.example.com/t2i/fal/imagen4/fast",
      "description": "Fast image generation"
    },
    // ... 他のサービス
  }
}
```

## 📦 Dockerコンテナ化

### Dockerfile例

```dockerfile
FROM python:3.9-slim

# FFmpegインストール
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコピー
COPY . /app
WORKDIR /app

CMD ["python", "mcp_news_video_generator.py"]
```

### requirements.txt

```
imageio-ffmpeg>=0.4.0
requests>=2.25.0
tqdm>=4.60.0
python-dotenv>=0.19.0
pyyaml>=5.4.0
```

## 🔍 バージョン互換性

### Python
- **最小バージョン**: 3.6
- **推奨バージョン**: 3.8以上
- **テスト済み**: 3.8, 3.9, 3.10, 3.11

### FFmpeg
- **最小バージョン**: 4.0
- **推奨バージョン**: 4.4以上
- **必須機能**: libx264, aac

### 依存関係の確認スクリプト

```python
#!/usr/bin/env python3
"""依存関係チェッカー"""

import sys
import subprocess
import importlib

def check_python_version():
    """Pythonバージョンチェック"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6以上が必要です")
        return False
    print(f"✅ Python {sys.version}")
    return True

def check_python_packages():
    """Pythonパッケージチェック"""
    required = ['imageio_ffmpeg', 'requests']
    optional = ['moviepy', 'PIL', 'numpy', 'tqdm']
    
    for package in required:
        try:
            importlib.import_module(package)
            print(f"✅ {package} インストール済み")
        except ImportError:
            print(f"❌ {package} が必要です: pip install {package}")
            return False
    
    for package in optional:
        try:
            importlib.import_module(package)
            print(f"✅ {package} インストール済み（オプション）")
        except ImportError:
            print(f"ℹ️ {package} は未インストール（オプション）")
    
    return True

def check_ffmpeg():
    """FFmpegチェック"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg: {version}")
            return True
    except FileNotFoundError:
        pass
    
    # imageio_ffmpegのFFmpegを試す
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        result = subprocess.run([ffmpeg, '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ FFmpeg (imageio_ffmpeg): {ffmpeg}")
            return True
    except:
        pass
    
    print("❌ FFmpegが見つかりません")
    return False

def main():
    """メインチェック関数"""
    print("🔍 依存関係をチェック中...\n")
    
    checks = [
        check_python_version(),
        check_python_packages(),
        check_ffmpeg()
    ]
    
    if all(checks):
        print("\n✅ すべての依存関係が満たされています！")
    else:
        print("\n❌ 依存関係に問題があります。上記を確認してください。")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 🚨 トラブルシューティング

### imageio_ffmpegがFFmpegをダウンロードできない

```python
# プロキシ設定
import os
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.example.com:8080'
```

### メモリ不足エラー

```bash
# スワップ領域を増やす（Linux）
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### コーデックエラー

```bash
# 完全版FFmpegをインストール
# Ubuntu/Debian
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt-get update
sudo apt-get install ffmpeg
```