#!/usr/bin/env python3
"""
シンプルな動画結合スクリプト
ImageIOとnumpyのみを使用
"""

import os
import imageio
import numpy as np

print("🎬 シンプルな動画結合を開始...")

# ディレクトリ移動
os.chdir("news_water_pipe")

# 動画ファイルのリスト
video_files = [
    "title_animation.mp4",
    "anchor_lipsync.mp4"
]

# 出力動画の準備
output_path = "combined_news_video.mp4"
fps = 30

print("📹 動画を読み込み中...")

# すべてのフレームを収集
all_frames = []

for video_file in video_files:
    if os.path.exists(video_file):
        print(f"  - {video_file} を処理中...")
        reader = imageio.get_reader(video_file)
        
        # タイトルアニメーションは5秒（150フレーム）に制限
        if video_file == "title_animation.mp4":
            frame_count = 0
            for frame in reader:
                all_frames.append(frame)
                frame_count += 1
                if frame_count >= 150:  # 5秒分
                    break
        else:
            # その他の動画は全フレーム
            for frame in reader:
                all_frames.append(frame)
        
        reader.close()

print(f"✅ 合計 {len(all_frames)} フレームを収集")

# 動画を書き出し
print("📝 結合動画を出力中...")
writer = imageio.get_writer(output_path, fps=fps)

for i, frame in enumerate(all_frames):
    writer.append_data(frame)
    if i % 100 == 0:
        print(f"  進捗: {i}/{len(all_frames)} フレーム")

writer.close()

print(f"✅ 動画結合完了！")
print(f"📺 出力ファイル: news_water_pipe/{output_path}")
print(f"⚠️  注意: この方法では音声は含まれません。")

# ファイル情報を表示
file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
print(f"📊 ファイルサイズ: {file_size:.2f} MB")
print(f"📊 総フレーム数: {len(all_frames)}")
print(f"📊 再生時間: 約{len(all_frames)/fps:.1f}秒")