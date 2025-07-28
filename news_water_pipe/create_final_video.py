#!/usr/bin/env python3
"""
最終的なニュース動画を音声付きで作成
"""

import subprocess
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

print("🎬 最終的なニュース動画を作成します...")

# Step 1: タイトルアニメーションに無音の音声トラックを追加
print("🔇 タイトルアニメーションに無音トラックを追加...")
cmd1 = [
    ffmpeg_path,
    "-i", "title_animation.mp4",
    "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
    "-t", "5",
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    "title_with_silence.mp4",
    "-y"
]
subprocess.run(cmd1, capture_output=True)

# Step 2: 動画を結合
print("🎞️ 動画を結合中...")
with open("final_concat.txt", "w") as f:
    f.write("file 'title_with_silence.mp4'\n")
    f.write("file 'anchor_lipsync.mp4'\n")

cmd2 = [ffmpeg_path, "-f", "concat", "-safe", "0", "-i", "final_concat.txt", 
        "-c", "copy", "news_complete_with_narration.mp4", "-y"]
result = subprocess.run(cmd2, capture_output=True, text=True)

if result.returncode == 0:
    print("✅ 音声付き動画の結合成功！")
    
    # Step 3: BGMを追加（ナレーション音声より小さく）
    print("🎵 BGMを追加中...")
    
    cmd3 = [
        ffmpeg_path,
        "-i", "news_complete_with_narration.mp4",
        "-stream_loop", "-1", "-i", "bgm.wav",
        "-filter_complex",
        "[1:a]volume=0.08[bgm];"  # BGMの音量を8%に
        "[0:a][bgm]amerge=inputs=2[mixed]",  # 音声をマージ
        "-map", "0:v",
        "-map", "[mixed]",
        "-ac", "2",  # ステレオに変換
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "FINAL_NEWS_VIDEO_COMPLETE.mp4",
        "-y"
    ]
    
    result2 = subprocess.run(cmd3, capture_output=True, text=True)
    
    if result2.returncode == 0:
        print("✅ 完璧！すべての要素が含まれたニュース動画が完成しました！")
        print("\n🎉 最終出力: news_water_pipe/FINAL_NEWS_VIDEO_COMPLETE.mp4")
        print("\n📝 動画の内容:")
        print("  1. タイトルアニメーション（5秒）")
        print("  2. キャスターによるニュース読み上げ（リップシンク済み、約1分）")
        print("  3. ナレーション音声（はっきりと聞こえる）")
        print("  4. BGM（控えめな音量で全編に流れる）")
        
        # ファイル情報を表示
        info_cmd = [ffmpeg_path, "-i", "FINAL_NEWS_VIDEO_COMPLETE.mp4", "-hide_banner"]
        info_result = subprocess.run(info_cmd, stderr=subprocess.PIPE, text=True)
        
        for line in info_result.stderr.split('\n'):
            if 'Duration:' in line:
                print(f"\n⏱️ {line.strip()}")
            elif 'Stream' in line and 'Audio:' in line:
                print(f"🔊 {line.strip()}")
                
        # ファイルサイズ
        import os
        if os.path.exists("FINAL_NEWS_VIDEO_COMPLETE.mp4"):
            size = os.path.getsize("FINAL_NEWS_VIDEO_COMPLETE.mp4") / 1024 / 1024
            print(f"📊 ファイルサイズ: {size:.2f} MB")
            
    else:
        print("❌ BGM追加でエラー:")
        print(result2.stderr[:500])
        print("\n💡 ナレーション音声のみのバージョン: news_complete_with_narration.mp4")
else:
    print("❌ 動画結合でエラー:")
    print(result.stderr)

# 確認用: news_with_voice.mp4がある場合はそれも音声チェック
print("\n🔍 作成された動画の音声を確認中...")
check_videos = ["news_complete_with_narration.mp4", "FINAL_NEWS_VIDEO_COMPLETE.mp4", "news_with_voice.mp4"]
for video in check_videos:
    import os
    if os.path.exists(video):
        print(f"\n📹 {video}:")
        cmd = [ffmpeg_path, "-i", video, "-hide_banner"]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        has_audio = False
        for line in result.stderr.split('\n'):
            if 'Audio:' in line and 'Stream' in line:
                has_audio = True
                print(f"  ✅ 音声あり: {line.strip()}")
        if not has_audio:
            print("  ❌ 音声なし")