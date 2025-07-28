#!/usr/bin/env python3
"""
MoviePyを使用したニュース動画編集スクリプト
事前にインストール: pip install moviepy
"""

import os
from moviepy.editor import *
from moviepy.video.fx import resize
import requests

def download_file(url, filename):
    """URLからファイルをダウンロード"""
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename

# 素材のダウンロード
print("📥 素材をダウンロード中...")

os.makedirs("news_water_pipe", exist_ok=True)
os.chdir("news_water_pipe")

# URLリスト
urls = {
    "title_animation.mp4": "https://v3.fal.media/files/rabbit/nGmdta6D60ReiivHRg5pB_output.mp4",
    "anchor_lipsync.mp4": "https://v3.fal.media/files/panda/oO10ZTDxbkZ4rXLhfkBjx_output.mp4",
    "bgm.wav": "https://storage.googleapis.com/geminicli/lyria_outputs/lyria_output_JdvOgOQNg.wav?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcs-signer%40kamui-445410.iam.gserviceaccount.com%2F20250728%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250728T004854Z&X-Goog-Expires=3599&X-Goog-Signature=58d162dd8e189d696df9ff13be866c3968a356b4c624c2f1aa3b62a3622ae90f5f26d9b1587f77b24d61e5df6a792d3f8020266b4c15e51856714d5d3f4d726489421211fd87f2fe0df78968857aee27c01d9631688df836190dbaf8245d1021e5ba44e7cc88d09099ead135cf7e60a3729e67c448f45a6dc3dd883713ad4684cf2c7b4bba3e1e28f43b2b19bc886962c88a541b252537fd57a14ae6b0e1eb97e209a60d5d9f08835bf7186f8c4fb05fec0a8b5c5b9e6966b3b0331d789c9c0b5bfe8bc397a45b65ed2fdde9d68830f9eca510671b780f7b4a22a9cb01ce9833f40fd03167e9c6f3bdd84efb575f83597c3ec8ee53a12352433430292fc957d9&X-Goog-SignedHeaders=host"
}

# ダウンロード
for filename, url in urls.items():
    download_file(url, filename)

print("✅ ダウンロード完了")

# 動画編集開始
print("🎬 動画編集を開始...")

# 1. タイトルアニメーション（5秒に調整）
title_clip = VideoFileClip("title_animation.mp4").subclip(0, 5)

# 2. キャスター映像（リップシンク済み）
anchor_clip = VideoFileClip("anchor_lipsync.mp4")

# 3. インフォグラフィックがあれば使用、なければテキストオーバーレイ
infographic_files = [f for f in os.listdir('.') if 'infographic' in f and f.endswith('.png')]
if infographic_files:
    # インフォグラフィック画像を5秒の動画に
    infographic = ImageClip(infographic_files[0]).set_duration(5)
else:
    # テキストオーバーレイで統計情報を表示
    infographic = TextClip(
        "水道管の老朽化\n\n40%が耐用年数超過\n年間2万件の漏水事故",
        fontsize=50,
        color='white',
        bg_color='black',
        size=(1920, 1080),
        method='caption'
    ).set_duration(5)

# 4. すべてのクリップを結合
final_video = concatenate_videoclips([title_clip, anchor_clip, infographic])

# 5. BGMを追加（音量を下げて）
bgm = AudioFileClip("bgm.wav").volumex(0.1)  # 音量を10%に
bgm_looped = afx.audio_loop(bgm, duration=final_video.duration)

# 6. 元の音声とBGMをミックス
if anchor_clip.audio:
    final_audio = CompositeAudioClip([final_video.audio, bgm_looped])
else:
    final_audio = bgm_looped

final_video = final_video.set_audio(final_audio)

# 7. エクスポート
print("📹 最終動画を出力中...")
final_video.write_videofile(
    "final_news_video_moviepy.mp4",
    codec="libx264",
    audio_codec="aac",
    fps=30
)

print("✅ 完成！")
print("📺 出力ファイル: news_water_pipe/final_news_video_moviepy.mp4")

# オプション: トランジション効果を追加したバージョン
print("\n🎨 トランジション効果付きバージョンを作成中...")

# フェードトランジションを追加
title_with_fade = title_clip.fadeout(0.5)
anchor_with_fade = anchor_clip.fadein(0.5).fadeout(0.5)
infographic_with_fade = infographic.fadein(0.5)

final_with_transitions = concatenate_videoclips(
    [title_with_fade, anchor_with_fade, infographic_with_fade],
    method="compose"
)

final_with_transitions = final_with_transitions.set_audio(final_audio)

final_with_transitions.write_videofile(
    "final_news_video_with_transitions.mp4",
    codec="libx264",
    audio_codec="aac",
    fps=30
)

print("✅ トランジション効果付きバージョンも完成！")
print("📺 出力ファイル: news_water_pipe/final_news_video_with_transitions.mp4")