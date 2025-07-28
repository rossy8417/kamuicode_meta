#!/usr/bin/env python3
"""
音声付きでニュース動画を再結合
"""

import subprocess
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

print("🎬 音声付きでニュース動画を再作成します...")

# Step 1: タイトルアニメーションを5秒に調整（音声なし）
print("📹 タイトルアニメーションを処理中...")
cmd1 = [ffmpeg_path, "-i", "title_animation.mp4", "-t", "5", "-c", "copy", "title_5sec_new.mp4", "-y"]
subprocess.run(cmd1, capture_output=True)

# Step 2: 動画を結合（音声トラックも含めて）
print("🎞️ 動画を音声付きで結合中...")

# concat用のファイルリストを作成
with open("concat_with_audio.txt", "w") as f:
    f.write("file 'title_5sec_new.mp4'\n")
    f.write("file 'anchor_lipsync.mp4'\n")

# 音声も含めて結合
cmd2 = [ffmpeg_path, "-f", "concat", "-safe", "0", "-i", "concat_with_audio.txt", 
        "-c", "copy", "news_with_voice.mp4", "-y"]
result = subprocess.run(cmd2, capture_output=True, text=True)

if result.returncode == 0:
    print("✅ 音声付き動画の結合成功！")
    
    # Step 3: BGMをミックス（ナレーション音声を優先）
    print("🎵 ナレーション音声とBGMをミックス中...")
    
    # BGMの音量を大幅に下げる（10%）
    cmd3 = [
        ffmpeg_path,
        "-i", "news_with_voice.mp4",  # ナレーション音声付き動画
        "-i", "bgm.wav",              # BGM
        "-filter_complex", 
        "[1:a]volume=0.1,aloop=loop=-1:size=2e+09[bgm];"  # BGMをループ&音量調整
        "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=3[mixed]",  # ミックス
        "-map", "0:v",                 # 動画トラック
        "-map", "[mixed]",             # ミックスした音声
        "-c:v", "copy",                # 動画はコピー
        "-c:a", "aac",                 # 音声はAAC
        "-shortest",                   # 短い方に合わせる
        "final_news_with_voice_and_bgm.mp4",
        "-y"
    ]
    
    result2 = subprocess.run(cmd3, capture_output=True, text=True)
    
    if result2.returncode == 0:
        print("✅ 完成！ナレーション音声とBGMが含まれています！")
        print("\n📺 最終出力: news_water_pipe/final_news_with_voice_and_bgm.mp4")
        
        # ファイル情報
        size = subprocess.run([ffmpeg_path, "-i", "final_news_with_voice_and_bgm.mp4", "-hide_banner"], 
                            stderr=subprocess.PIPE, text=True).stderr
        for line in size.split('\n'):
            if 'Duration:' in line:
                print(f"⏱️ {line.strip()}")
            elif 'Audio:' in line and 'Stream' in line:
                print(f"🔊 {line.strip()}")
                
    else:
        print("❌ BGMミックスでエラー:")
        print(result2.stderr)
        print("\n💡 ただし、ナレーション音声のみのバージョンは作成されました: news_with_voice.mp4")
else:
    print("❌ 動画結合でエラー:")
    print(result.stderr)

# クリーンアップ
print("\n🧹 一時ファイルを削除中...")
temp_files = ["title_5sec_new.mp4", "concat_with_audio.txt"]
for f in temp_files:
    subprocess.run(["rm", "-f", f], capture_output=True)