#!/bin/bash

# MCPで生成されたコンテンツをダウンロードするスクリプト

echo "🎨 MCP Generated Content Downloader"
echo "=================================="

# 現在のディレクトリを表示
CURRENT_DIR=$(pwd)
echo "Current directory: $CURRENT_DIR"
echo ""

# 例: Google Imagen3からの画像URL（長いURL）
download_google_image() {
    local full_url="$1"
    local filename="$2"
    
    echo "📥 Downloading from Google Storage..."
    echo "URL: $full_url"
    
    # フルURLを使用してダウンロード（省略しない）
    wget -O "$filename" "$full_url"
    
    if [ $? -eq 0 ]; then
        echo "✅ Downloaded: ~$CURRENT_DIR/$filename"
        echo "File size: $(ls -lh "$filename" | awk '{print $5}')"
    else
        echo "❌ Download failed"
    fi
}

# 例: Falからの動画URL（短いURL）
download_fal_video() {
    local full_url="$1"
    local filename="$2"
    
    echo "📥 Downloading from Fal..."
    echo "URL: $full_url"
    
    # フルURLを使用してダウンロード
    wget -O "$filename" "$full_url"
    
    if [ $? -eq 0 ]; then
        echo "✅ Downloaded: ~$CURRENT_DIR/$filename"
        echo "File size: $(ls -lh "$filename" | awk '{print $5}')"
    else
        echo "❌ Download failed"
    fi
}

# 使用例
if [ "$1" == "test" ]; then
    # テスト用のプレースホルダーURL
    echo "🧪 Test mode - using placeholder URLs"
    
    # Google画像の例（実際は認証付きの長いURL）
    download_google_image "https://storage.googleapis.com/example-bucket/path/to/image.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=..." "test-image.png"
    
    # Fal動画の例（短いURL）
    download_fal_video "https://fal.ai/result/abc123" "test-video.mp4"
else
    echo "Usage: $0 [test]"
    echo ""
    echo "In actual use:"
    echo "1. Get the full authenticated URL from MCP response"
    echo "2. Call download functions with FULL URLs (no abbreviation)"
    echo "3. Files will be saved to current directory"
    echo "4. Full paths will be displayed as ~$CURRENT_DIR/filename"
fi