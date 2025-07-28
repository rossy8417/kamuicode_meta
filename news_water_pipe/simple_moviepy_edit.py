#!/usr/bin/env python3
"""
シンプルなMoviePy編集 - 基本的な結合とエフェクト
"""

import sys
import os

# MoviePyのインストール確認
try:
    import moviepy
    print(f"✅ MoviePy version: {moviepy.__version__}")
except ImportError:
    print("❌ MoviePyがインストールされていません")
    print("実行: pip install moviepy")
    sys.exit(1)

# 必要なモジュールをインポート
try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, CompositeAudioClip
    from moviepy.video.fx.fadein import fadein
    from moviepy.video.fx.fadeout import fadeout
    import moviepy.audio.fx.all as afx
except ImportError as e:
    print(f"❌ インポートエラー: {e}")
    print("MoviePyが正しくインストールされていない可能性があります")
    sys.exit(1)

print("🎬 MoviePyでシンプルな編集を開始...")

try:
    # 1. 動画を読み込み
    print("📹 動画を読み込み中...")
    
    # タイトル（5秒）
    title = VideoFileClip("title_animation.mp4").subclip(0, 5)
    print(f"  - タイトル: {title.duration}秒")
    
    # キャスター映像
    anchor = VideoFileClip("anchor_lipsync.mp4")
    print(f"  - キャスター: {anchor.duration}秒")
    
    # BGM
    bgm = AudioFileClip("bgm.wav").fx(afx.volumex, 0.1)
    print(f"  - BGM: {bgm.duration}秒")
    
    # 2. 基本的なフェード効果
    print("✨ フェード効果を追加...")
    
    # タイトルにフェードアウト
    title_fade = title.fx(fadeout, 1.0)
    
    # キャスターにフェードイン
    anchor_fade = anchor.fx(fadein, 1.0)
    
    # 3. 動画を結合
    print("🎞️ 動画を結合中...")
    final_video = concatenate_videoclips([title_fade, anchor_fade])
    
    # 4. BGMを追加
    print("🎵 BGMを追加中...")
    
    # BGMをループ
    bgm_looped = bgm.fx(afx.audio_loop, duration=final_video.duration)
    
    # 音声をミックス
    if final_video.audio:
        final_audio = CompositeAudioClip([final_video.audio, bgm_looped])
        final_video = final_video.set_audio(final_audio)
    else:
        final_video = final_video.set_audio(bgm_looped)
    
    # 5. エクスポート
    print("💾 動画を出力中（これには時間がかかります）...")
    
    output_file = "news_moviepy_simple.mp4"
    final_video.write_videofile(
        output_file,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        logger=None  # プログレスバーを簡素化
    )
    
    print(f"\n✅ 完成！")
    print(f"📺 出力ファイル: {output_file}")
    
    # ファイルサイズ
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024 / 1024
        print(f"📊 ファイルサイズ: {size:.2f} MB")
        print(f"⏱️ 動画の長さ: {final_video.duration:.1f}秒")
    
    # リソースを解放
    title.close()
    anchor.close()
    bgm.close()
    final_video.close()
    
    print("\n💡 MoviePyの特徴:")
    print("  - フェードイン/アウト効果")
    print("  - 音声の自動ミックス")
    print("  - より滑らかなトランジション")
    
except FileNotFoundError as e:
    print(f"❌ ファイルが見つかりません: {e}")
    print("必要なファイル: title_animation.mp4, anchor_lipsync.mp4, bgm.wav")
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()