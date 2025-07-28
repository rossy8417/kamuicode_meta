#!/usr/bin/env python3
"""
MoviePyを使用した高度なニュース動画編集
"""

import os
from moviepy.editor import *
from moviepy.video.fx import fadeout, fadein
import numpy as np

print("🎬 MoviePyでニュース動画を編集します...")

# 作業ディレクトリの確認
if not os.path.exists("title_animation.mp4"):
    print("❌ ファイルが見つかりません。正しいディレクトリで実行してください。")
    exit(1)

try:
    # 1. 動画素材を読み込み
    print("📹 動画素材を読み込み中...")
    
    # タイトルアニメーション（5秒に調整）
    title_clip = VideoFileClip("title_animation.mp4").subclip(0, 5)
    
    # キャスター映像（リップシンク済み、音声付き）
    anchor_clip = VideoFileClip("anchor_lipsync.mp4")
    
    # BGMを読み込み
    bgm = AudioFileClip("bgm.wav").volumex(0.08)  # 音量を8%に
    
    # 2. トランジション効果を追加
    print("✨ トランジション効果を追加中...")
    
    # タイトルをフェードアウト
    title_with_fade = title_clip.fadeout(1.0)
    
    # キャスター映像をフェードイン・フェードアウト
    anchor_with_fade = anchor_clip.fadein(1.0).fadeout(1.0)
    
    # 3. テキストオーバーレイを追加
    print("📝 テキストオーバーレイを作成中...")
    
    # ニュースタイトルのテキスト
    title_text = TextClip(
        "水道インフラの危機",
        fontsize=70,
        color='white',
        font='Noto-Sans-CJK-JP',
        stroke_color='black',
        stroke_width=2
    ).set_position(('center', 'bottom')).set_duration(5).fadein(0.5).fadeout(0.5)
    
    # サブタイトル
    subtitle_text = TextClip(
        "老朽化する日本の水道管",
        fontsize=50,
        color='white',
        font='Noto-Sans-CJK-JP',
        stroke_color='black',
        stroke_width=2
    ).set_position(('center', 100)).set_duration(5).set_start(0.5).fadein(0.5).fadeout(0.5)
    
    # 統計情報のテキスト（中盤で表示）
    stats_text = TextClip(
        "全国の水道管の40%が\n法定耐用年数を超過",
        fontsize=60,
        color='yellow',
        font='Noto-Sans-CJK-JP',
        stroke_color='black',
        stroke_width=3,
        method='caption',
        size=(1200, None),
        align='center'
    ).set_position(('center', 'center')).set_duration(4).set_start(25).fadein(0.5).fadeout(0.5)
    
    # 4. すべてのクリップを結合
    print("🎞️ クリップを結合中...")
    
    # タイトル部分にテキストオーバーレイを合成
    title_with_text = CompositeVideoClip([
        title_with_fade,
        title_text,
        subtitle_text
    ])
    
    # メイン動画を結合
    main_video = concatenate_videoclips([title_with_text, anchor_with_fade])
    
    # 統計情報のオーバーレイを追加
    final_video = CompositeVideoClip([main_video, stats_text])
    
    # 5. 音声処理
    print("🎵 音声を処理中...")
    
    # BGMをループさせて動画の長さに合わせる
    bgm_looped = afx.audio_loop(bgm, duration=final_video.duration)
    
    # オリジナル音声とBGMをミックス
    if final_video.audio:
        final_audio = CompositeAudioClip([final_video.audio, bgm_looped])
    else:
        final_audio = bgm_looped
    
    final_video = final_video.set_audio(final_audio)
    
    # 6. エクスポート
    print("💾 動画を出力中...")
    output_filename = "news_video_moviepy_enhanced.mp4"
    
    final_video.write_videofile(
        output_filename,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset='medium',
        threads=4
    )
    
    print(f"\n✅ MoviePy編集完了！")
    print(f"📺 出力ファイル: {output_filename}")
    
    # 7. 追加バージョン：ニュース番組風のロワーサード（下部情報表示）
    print("\n🎨 ロワーサード付きバージョンも作成中...")
    
    # 下部の情報バー背景
    lower_third_bg = (ColorClip(size=(1920, 150), color=(0, 0, 0))
                     .set_opacity(0.7)
                     .set_position(('center', 'bottom'))
                     .set_duration(anchor_clip.duration)
                     .set_start(5))  # タイトル後から表示
    
    # 下部のテキスト情報
    lower_third_text = TextClip(
        "特別報道：日本の水道インフラ問題",
        fontsize=40,
        color='white',
        font='Noto-Sans-CJK-JP'
    ).set_position((50, 950)).set_duration(anchor_clip.duration).set_start(5)
    
    # 日時表示
    date_text = TextClip(
        "2025年1月28日",
        fontsize=30,
        color='white',
        font='Noto-Sans-CJK-JP'
    ).set_position(('right', 950)).set_duration(anchor_clip.duration).set_start(5).margin(right=50)
    
    # すべての要素を合成
    final_with_lower_third = CompositeVideoClip([
        final_video,
        lower_third_bg,
        lower_third_text,
        date_text
    ])
    
    # 最終出力
    final_with_lower_third.write_videofile(
        "news_video_moviepy_broadcast_style.mp4",
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset='medium',
        threads=4
    )
    
    print(f"\n✅ 放送品質版も完成！")
    print(f"📺 出力ファイル: news_video_moviepy_broadcast_style.mp4")
    
    # ファイルサイズを表示
    for filename in [output_filename, "news_video_moviepy_broadcast_style.mp4"]:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024 / 1024
            print(f"📊 {filename}: {size:.2f} MB")
    
except Exception as e:
    print(f"\n❌ エラーが発生しました: {e}")
    print("\n💡 ヒント:")
    print("1. 日本語フォントがない場合は、font引数を削除してください")
    print("2. メモリ不足の場合は、resize()で動画サイズを小さくしてください")
    print("3. 処理が重い場合は、threads=1に変更してください")