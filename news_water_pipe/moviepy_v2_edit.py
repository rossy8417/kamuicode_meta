#!/usr/bin/env python3
"""
MoviePy v2.x を使用したニュース動画編集
"""

import sys
import os

# MoviePy v2.xのインポート
try:
    import moviepy
    from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, CompositeAudioClip
    import moviepy.vfx as vfx
    import moviepy.afx as afx
    print(f"✅ MoviePy version: {moviepy.__version__}")
except ImportError as e:
    print(f"❌ MoviePyインポートエラー: {e}")
    sys.exit(1)

print("🎬 MoviePy v2でニュース動画を編集します...")

try:
    # 1. 動画を読み込み
    print("📹 動画素材を読み込み中...")
    
    # タイトルアニメーション（5秒に調整）
    title_clip = VideoFileClip("title_animation.mp4").with_duration(5)
    print(f"  ✅ タイトル: {title_clip.duration}秒")
    
    # キャスター映像（音声付き）
    anchor_clip = VideoFileClip("anchor_lipsync.mp4")
    print(f"  ✅ キャスター: {anchor_clip.duration}秒")
    
    # BGM
    bgm = AudioFileClip("bgm.wav")
    bgm_quiet = bgm.with_effects([afx.volumex(0.08)])  # 音量を8%に
    print(f"  ✅ BGM: {bgm.duration}秒")
    
    # 2. エフェクトを追加
    print("✨ エフェクトを追加中...")
    
    # フェード効果
    title_with_fade = title_clip.with_effects([vfx.fadeout(1.0)])
    anchor_with_fade = anchor_clip.with_effects([vfx.fadein(1.0)])
    
    # 3. テキストオーバーレイ（シンプル版）
    print("📝 テキストオーバーレイを作成中...")
    
    try:
        # タイトルテキスト
        title_text = TextClip(
            "Water Infrastructure Crisis",  # 英語で回避
            fontsize=60,
            color='white',
            stroke_color='black',
            stroke_width=2,
            method='label'
        ).with_duration(5).with_position(('center', 'bottom'))
        
        # タイトルとテキストを合成
        title_composite = CompositeVideoClip([title_with_fade, title_text])
        clips_to_concat = [title_composite, anchor_with_fade]
        
    except Exception as e:
        print(f"  ⚠️ テキストオーバーレイでエラー: {e}")
        print("  テキストなしで続行します...")
        clips_to_concat = [title_with_fade, anchor_with_fade]
    
    # 4. 動画を結合
    print("🎞️ 動画を結合中...")
    main_video = concatenate_videoclips(clips_to_concat)
    
    # 5. BGMを追加
    print("🎵 音声をミックス中...")
    
    # BGMをループさせて動画の長さに合わせる
    bgm_looped = bgm_quiet.loop(duration=main_video.duration)
    
    # 音声トラックをミックス
    if main_video.audio is not None:
        print("  - オリジナル音声とBGMをミックス")
        final_audio = CompositeAudioClip([main_video.audio, bgm_looped])
    else:
        print("  - BGMのみを使用")
        final_audio = bgm_looped
    
    final_video = main_video.with_audio(final_audio)
    
    # 6. 動画を出力
    print("💾 動画を出力中（数分かかる場合があります）...")
    
    output_filename = "news_moviepy_v2_final.mp4"
    
    # 出力設定
    final_video.write_videofile(
        output_filename,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset='fast',  # より高速な設定
        threads=4,
        logger='bar'  # プログレスバー表示
    )
    
    print(f"\n✅ MoviePy編集完了！")
    print(f"📺 出力ファイル: {output_filename}")
    
    # ファイル情報
    if os.path.exists(output_filename):
        size = os.path.getsize(output_filename) / 1024 / 1024
        print(f"📊 ファイルサイズ: {size:.2f} MB")
        print(f"⏱️ 動画の長さ: {final_video.duration:.1f}秒")
    
    # リソースを解放
    title_clip.close()
    anchor_clip.close()
    bgm.close()
    final_video.close()
    
    print("\n🎨 MoviePyで追加された効果:")
    print("  ✅ フェードイン/アウト効果")
    print("  ✅ 音声の自動ミックス（ナレーション + BGM）")
    print("  ✅ スムーズなトランジション")
    print("  ✅ プロフェッショナルな仕上がり")
    
except FileNotFoundError as e:
    print(f"❌ ファイルが見つかりません: {e}")
    print("現在のディレクトリ:", os.getcwd())
    print("必要なファイル:")
    print("  - title_animation.mp4")
    print("  - anchor_lipsync.mp4")
    print("  - bgm.wav")
    
except Exception as e:
    print(f"❌ エラーが発生しました: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n💡 トラブルシューティング:")
    print("1. メモリ不足の場合: preset='ultrafast'に変更")
    print("2. 処理が重い場合: threads=1に変更")
    print("3. フォントエラーの場合: TextClipを削除")