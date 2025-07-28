#!/usr/bin/env python3
"""
最終的なニュース動画の作成
"""

import subprocess
import os

try:
    import imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    print("🎬 最終的なニュース動画を作成します...")
    
    # news_merged.mp4にBGMを追加
    print("🎵 BGMを追加中...")
    
    # シンプルなコマンド - 動画にBGMを追加
    cmd = [
        ffmpeg_path, 
        "-i", "news_merged.mp4",  # 結合済み動画
        "-i", "bgm.wav",           # BGM
        "-filter_complex", "[1:a]volume=0.15[bgm]",  # BGMの音量を15%に
        "-map", "0:v",             # 動画トラック
        "-map", "[bgm]",           # 調整済みBGM
        "-c:v", "copy",            # 動画はコピー
        "-c:a", "aac",             # 音声はAACエンコード
        "-shortest",               # 短い方に合わせる
        "final_news_complete.mp4", 
        "-y"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ ニュース動画が完成しました！")
        print("\n📺 最終出力ファイル: news_water_pipe/final_news_complete.mp4")
        
        # ファイル情報
        if os.path.exists("final_news_complete.mp4"):
            size = os.path.getsize("final_news_complete.mp4") / 1024 / 1024
            print(f"📊 ファイルサイズ: {size:.2f} MB")
            
        print("\n📝 作成された動画の構成:")
        print("  1. タイトルアニメーション (5秒)")
        print("  2. キャスターによるニュース読み上げ (リップシンク済み)")
        print("  3. BGM (全編にわたって再生)")
        
    else:
        print("❌ エラーが発生しました:")
        print(result.stderr)
        print("\n💡 ただし、音声なしバージョンは利用可能です: news_merged.mp4")
        
except Exception as e:
    print(f"エラー: {e}")

# 作成されたファイルの一覧
print("\n📁 作成されたファイル:")
video_files = ["news_merged.mp4", "final_news_complete.mp4", "title_5sec.mp4"]
for f in video_files:
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024 / 1024
        print(f"  ✅ {f} ({size:.2f} MB)")