#!/usr/bin/env python3
"""
動画の音声トラックを確認
"""

import subprocess
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

print("🔍 各動画の音声トラックを確認します...\n")

videos = ["anchor_lipsync.mp4", "news_merged.mp4", "final_news_complete.mp4"]

for video in videos:
    print(f"📹 {video}:")
    cmd = [ffmpeg_path, "-i", video, "-hide_banner"]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    
    # ストリーム情報を抽出
    has_audio = False
    for line in result.stderr.split('\n'):
        if 'Stream' in line:
            if 'Audio:' in line:
                has_audio = True
                print(f"  🔊 {line.strip()}")
            elif 'Video:' in line:
                print(f"  🎬 {line.strip()}")
    
    if not has_audio:
        print("  ❌ 音声トラックなし")
    print()

print("\n💡 リップシンク動画に音声が含まれているか確認中...")
print("もし音声がない場合は、ナレーション音声を別途追加する必要があります。")