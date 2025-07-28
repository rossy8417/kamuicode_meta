#!/usr/bin/env python3
"""
音声なし動画にBGMを追加
"""

import subprocess
import os

try:
    import imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    print("🎵 BGMを動画に追加します...")
    
    # BGMの音量を下げる（20%に）
    print("📉 BGMの音量を調整中...")
    cmd1 = [ffmpeg_path, "-i", "bgm.wav", "-filter:a", "volume=0.2", 
            "bgm_quiet.wav", "-y"]
    subprocess.run(cmd1, capture_output=True)
    
    # 動画の長さを取得
    probe_cmd = [ffmpeg_path, "-i", "news_merged.mp4", "-hide_banner"]
    result = subprocess.run(probe_cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
    
    # 動画にBGMを追加（音声トラックがない場合）
    print("🎬 動画にBGMを追加中...")
    cmd2 = [ffmpeg_path, "-i", "news_merged.mp4", "-i", "bgm_quiet.wav",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            "-map", "0:v", "-map", "1:a",
            "final_news_video_with_bgm.mp4", "-y"]
    
    result = subprocess.run(cmd2, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ BGM追加成功！")
        print("\n🎉 ニュース動画が完成しました！")
        print("📺 出力ファイル: news_water_pipe/final_news_video_with_bgm.mp4")
        
        # ファイルサイズ確認
        if os.path.exists("final_news_video_with_bgm.mp4"):
            size = os.path.getsize("final_news_video_with_bgm.mp4") / 1024 / 1024
            print(f"📊 ファイルサイズ: {size:.2f} MB")
            
            # 再生時間を表示
            duration_cmd = [ffmpeg_path, "-i", "final_news_video_with_bgm.mp4", "-hide_banner"]
            duration_result = subprocess.run(duration_cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
            for line in duration_result.stdout.split('\n'):
                if 'Duration:' in line:
                    print(f"⏱️ {line.strip()}")
                    break
    else:
        print("❌ エラーが発生しました")
        print(result.stderr)
        
    # クリーンアップオプション
    print("\n🧹 一時ファイルのクリーンアップ...")
    temp_files = ["title_5sec.mp4", "merge_list.txt", "bgm_quiet.wav"]
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"  - {f} を削除")
            
except Exception as e:
    print(f"エラー: {e}")