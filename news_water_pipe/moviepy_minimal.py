#!/usr/bin/env python3
"""
MoviePy 2.x 最小限の実装
"""

import os

print("🎬 MoviePyで動画を編集します...")

try:
    # MoviePy 2.xの基本インポート
    from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
    
    # 1. 動画を読み込み
    print("📹 動画を読み込み中...")
    title = VideoFileClip("title_animation.mp4").subclipped(0, 5)
    anchor = VideoFileClip("anchor_lipsync.mp4")
    bgm = AudioFileClip("bgm.wav")
    
    print(f"  タイトル: {title.duration}秒")
    print(f"  キャスター: {anchor.duration}秒")
    print(f"  BGM: {bgm.duration}秒")
    
    # 2. フェード効果を追加
    print("✨ フェード効果を追加...")
    # fade_in/fade_outメソッドを直接使用
    title_fade = title.with_effects([
        lambda clip: clip.crossfadeout(1.0)
    ])
    
    anchor_fade = anchor.with_effects([
        lambda clip: clip.crossfadein(1.0)
    ])
    
    # 3. 動画を結合
    print("🎞️ 動画を結合...")
    video = concatenate_videoclips([title, anchor])
    
    # 4. BGMを調整して追加
    print("🎵 BGMを追加...")
    # BGMの音量を下げる
    bgm_quiet = bgm.multiply_volume(0.08)
    
    # BGMをループ
    bgm_looped = bgm_quiet.loop(duration=video.duration)
    
    # 音声をミックス
    if video.audio:
        audio = CompositeAudioClip([video.audio, bgm_looped])
        video = video.with_audio(audio)
    else:
        video = video.with_audio(bgm_looped)
    
    # 5. エクスポート
    print("💾 動画を出力中...")
    output = "news_moviepy_output.mp4"
    
    video.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=24
    )
    
    print(f"\n✅ 完成！")
    print(f"📺 出力: {output}")
    
    if os.path.exists(output):
        size = os.path.getsize(output) / 1024 / 1024
        print(f"📊 サイズ: {size:.2f} MB")
    
    # クリーンアップ
    title.close()
    anchor.close()
    bgm.close()
    video.close()
    
except AttributeError as e:
    print(f"❌ MoviePy APIエラー: {e}")
    print("\n💡 代替案: imageio_ffmpegを使用した編集が成功しています")
    print("完成ファイル:")
    print("  - FINAL_NEWS_VIDEO_COMPLETE.mp4 (音声付き)")
    print("  - final_news_with_voice_and_bgm.mp4 (音声付き)")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()

print("\n📊 MoviePyとFFmpegの比較:")
print("MoviePy:")
print("  ✅ Pythonネイティブな操作")
print("  ✅ 高度なエフェクト（フェード、テキスト、変形）")
print("  ✅ フレーム単位の処理")
print("  ❌ 処理速度が遅い")
print("  ❌ メモリ使用量が多い")
print("\nFFmpeg (imageio_ffmpeg):")
print("  ✅ 高速処理")
print("  ✅ メモリ効率が良い")
print("  ✅ プロ仕様のコーデック対応")
print("  ❌ 複雑なエフェクトは難しい")
print("  ❌ コマンドライン的な操作")