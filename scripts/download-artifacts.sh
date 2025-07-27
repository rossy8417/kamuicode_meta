#!/bin/bash

# GitHub Actionsのアーティファクトから画像をダウンロードするスクリプト

echo "📦 GitHub Actions Artifact Downloader"
echo "===================================="

# 使用方法をチェック
if [ $# -lt 2 ]; then
    echo "Usage: $0 <run-id> <artifact-name>"
    echo "Example: $0 16551518501 mcp-fixed-test-1"
    exit 1
fi

RUN_ID=$1
ARTIFACT_NAME=$2
REPO="rossy8417/kamuicode_meta"
DOWNLOAD_DIR="./downloaded-artifacts"

echo "Repository: $REPO"
echo "Run ID: $RUN_ID"
echo "Artifact: $ARTIFACT_NAME"
echo ""

# ダウンロードディレクトリを作成
mkdir -p "$DOWNLOAD_DIR"

# アーティファクトをダウンロード
echo "📥 Downloading artifact..."
gh run download "$RUN_ID" \
    --repo "$REPO" \
    --name "$ARTIFACT_NAME" \
    --dir "$DOWNLOAD_DIR/$ARTIFACT_NAME"

if [ $? -eq 0 ]; then
    echo "✅ Download successful!"
    echo ""
    echo "📁 Downloaded files:"
    
    # 画像ファイルを探す
    echo ""
    echo "🎨 Image files found:"
    find "$DOWNLOAD_DIR/$ARTIFACT_NAME" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read -r file; do
        echo "  - ~$(pwd)/$file"
        # ファイルサイズも表示
        echo "    Size: $(ls -lh "$file" | awk '{print $5}')"
    done
    
    # 動画ファイルを探す
    echo ""
    echo "🎬 Video files found:"
    find "$DOWNLOAD_DIR/$ARTIFACT_NAME" -type f \( -name "*.mp4" -o -name "*.avi" -o -name "*.mov" \) | while read -r file; do
        echo "  - ~$(pwd)/$file"
        echo "    Size: $(ls -lh "$file" | awk '{print $5}')"
    done
    
    # 3Dモデルファイルを探す
    echo ""
    echo "🎲 3D model files found:"
    find "$DOWNLOAD_DIR/$ARTIFACT_NAME" -type f \( -name "*.glb" -o -name "*.obj" -o -name "*.fbx" \) | while read -r file; do
        echo "  - ~$(pwd)/$file"
        echo "    Size: $(ls -lh "$file" | awk '{print $5}')"
    done
    
    # JSONファイルも確認
    echo ""
    echo "📄 JSON files found:"
    find "$DOWNLOAD_DIR/$ARTIFACT_NAME" -type f -name "*.json" | while read -r file; do
        echo "  - ~$(pwd)/$file"
    done
    
else
    echo "❌ Download failed!"
    exit 1
fi

echo ""
echo "💡 Tip: To view an image, use: open <file-path> (macOS) or xdg-open <file-path> (Linux)"