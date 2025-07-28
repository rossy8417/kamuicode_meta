#!/usr/bin/env python3
"""
imageio_ffmpegを使用した動画結合
"""

import subprocess
import os

print("🎬 ニュース動画の結合を開始...")

# ファイルの存在確認
files = ["title_animation.mp4", "anchor_lipsync.mp4", "bgm.wav"]
for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024 / 1024
        print(f"✅ {f}: {size:.2f} MB")

# imageio_ffmpegのパスを取得
try:
    import imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"\n📍 FFmpeg path: {ffmpeg_path}")
    
    # Step 1: タイトルを5秒に調整
    print("\n📹 タイトルアニメーションを5秒に調整...")
    cmd1 = [ffmpeg_path, "-i", "title_animation.mp4", "-t", "5", "-c", "copy", "title_5sec.mp4", "-y"]
    subprocess.run(cmd1, capture_output=True)
    
    # Step 2: concat用のファイルリストを作成
    with open("merge_list.txt", "w") as f:
        f.write("file 'title_5sec.mp4'\n")
        f.write("file 'anchor_lipsync.mp4'\n")
    
    # Step 3: 動画を結合（音声含む）
    print("🎞️ 動画を結合中...")
    cmd2 = [ffmpeg_path, "-f", "concat", "-safe", "0", "-i", "merge_list.txt", 
            "-c", "copy", "news_merged.mp4", "-y"]
    result = subprocess.run(cmd2, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 動画結合成功！")
        
        # Step 4: BGMを追加（音量を下げて）
        print("🎵 BGMを追加中...")
        cmd3 = [ffmpeg_path, "-i", "news_merged.mp4", "-i", "bgm.wav",
                "-filter_complex", "[1:a]volume=0.1[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "final_news_video.mp4", "-y"]
        
        result2 = subprocess.run(cmd3, capture_output=True, text=True)
        
        if result2.returncode == 0:
            print("✅ BGM追加成功！")
            print("\n🎉 ニュース動画が完成しました！")
            print("📺 出力ファイル: news_water_pipe/final_news_video.mp4")
            
            # ファイルサイズ確認
            if os.path.exists("final_news_video.mp4"):
                size = os.path.getsize("final_news_video.mp4") / 1024 / 1024
                print(f"📊 ファイルサイズ: {size:.2f} MB")
        else:
            print("⚠️ BGM追加でエラーが発生しました")
            print(result2.stderr)
            print("\n💡 音声なしバージョンは作成されました: news_merged.mp4")
    else:
        print("❌ 動画結合でエラーが発生しました")
        print(result.stderr)
        
except ImportError:
    print("❌ imageio_ffmpegがインストールされていません")
    print("実行: pip install imageio-ffmpeg")
except Exception as e:
    print(f"エラー: {e}")