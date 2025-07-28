#!/bin/bash

echo "🎬 動画結合を開始..."

# 現在の場所から実行
cd news_water_pipe

# ファイルの存在確認
echo "📁 利用可能なファイル:"
ls -la *.mp4 *.wav 2>/dev/null

# concat demuxerを使用した結合（音声なし）
echo "📹 動画を結合中..."

# 結合リストの作成
cat > concat_simple.txt << EOF
file 'title_animation.mp4'
file 'anchor_lipsync.mp4'
EOF

# imageioのffmpegを使用
python3 -m imageio_ffmpeg -version && {
    echo "✅ imageio_ffmpegが利用可能"
    
    # 動画結合（音声付き）
    python3 -m imageio_ffmpeg -f concat -safe 0 -i concat_simple.txt -c copy news_combined.mp4
    
    echo "📺 結合完了: news_water_pipe/news_combined.mp4"
}

# または代替案：OpenCVを使用
echo ""
echo "📝 代替案: Pythonで動画情報を確認..."
python3 << 'EOF'
import os
import json

files = ["title_animation.mp4", "anchor_lipsync.mp4", "bgm.wav"]
info = {}

for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024 / 1024
        info[f] = f"{size:.2f} MB"
        print(f"✅ {f}: {size:.2f} MB")
    else:
        print(f"❌ {f}: 見つかりません")

# 動画の基本情報を取得
try:
    import imageio
    for video in ["title_animation.mp4", "anchor_lipsync.mp4"]:
        if os.path.exists(video):
            reader = imageio.get_reader(video)
            meta = reader.get_meta_data()
            print(f"\n📹 {video}:")
            print(f"  - Duration: {meta.get('duration', 'N/A')}s")
            print(f"  - FPS: {meta.get('fps', 'N/A')}")
            print(f"  - Size: {meta.get('size', 'N/A')}")
            reader.close()
except Exception as e:
    print(f"エラー: {e}")

# 最終的な推奨事項
print("\n💡 推奨事項:")
print("1. FFmpegをインストール: apt-get install ffmpeg")
print("2. または動画編集ソフト（OpenShot, Kdenlive等）で結合")
print("3. オンラインツール（Kapwing, Canva等）も利用可能")
EOF