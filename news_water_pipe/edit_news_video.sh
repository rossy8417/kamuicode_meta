#!/bin/bash

echo "🎬 ニュース動画の編集を開始します..."

# まず素材をダウンロード
echo "📥 素材をダウンロード中..."

# 動画素材
curl -s -o "news_water_pipe/title_animation.mp4" "https://v3.fal.media/files/rabbit/nGmdta6D60ReiivHRg5pB_output.mp4"
curl -s -o "news_water_pipe/anchor_lipsync.mp4" "https://v3.fal.media/files/panda/oO10ZTDxbkZ4rXLhfkBjx_output.mp4"

# BGM
curl -s -L "https://storage.googleapis.com/geminicli/lyria_outputs/lyria_output_JdvOgOQNg.wav?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcs-signer%40kamui-445410.iam.gserviceaccount.com%2F20250728%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250728T004854Z&X-Goog-Expires=3599&X-Goog-Signature=58d162dd8e189d696df9ff13be866c3968a356b4c624c2f1aa3b62a3622ae90f5f26d9b1587f77b24d61e5df6a792d3f8020266b4c15e51856714d5d3f4d726489421211fd87f2fe0df78968857aee27c01d9631688df836190dbaf8245d1021e5ba44e7cc88d09099ead135cf7e60a3729e67c448f45a6dc3dd883713ad4684cf2c7b4bba3e1e28f43b2b19bc886962c88a541b252537fd57a14ae6b0e1eb97e209a60d5d9f08835bf7186f8c4fb05fec0a8b5c5b9e6966b3b0331d789c9c0b5bfe8bc397a45b65ed2fdde9d68830f9eca510671b780f7b4a22a9cb01ce9833f40fd03167e9c6f3bdd84efb575f83597c3ec8ee53a12352433430292fc957d9&X-Goog-SignedHeaders=host" -o "news_water_pipe/bgm.wav"

echo "✅ ダウンロード完了"

# ディレクトリに移動
cd news_water_pipe

# Step 1: タイトルアニメーションを5秒に調整
echo "📹 タイトルアニメーションを処理中..."
ffmpeg -i title_animation.mp4 -t 5 -c:v libx264 -c:a aac title_5sec.mp4 -y

# Step 2: リップシンク動画の長さを取得
duration=$(ffmpeg -i anchor_lipsync.mp4 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); print 3600*A[1] + 60*A[2] + A[3] }')

# Step 3: インフォグラフィック画像を5秒の動画に変換
echo "📊 インフォグラフィックを動画化中..."
if [ -f "infographic_ce251d91_1_1753663500.png" ]; then
    ffmpeg -loop 1 -i infographic_ce251d91_1_1753663500.png -c:v libx264 -t 5 -pix_fmt yuv420p infographic_video.mp4 -y
else
    # インフォグラフィックがない場合は黒画面を生成
    ffmpeg -f lavfi -i color=c=black:s=1920x1080:d=5 -c:v libx264 infographic_video.mp4 -y
fi

# Step 4: 動画リストファイルを作成
echo "📝 動画リストを作成中..."
cat > concat_list.txt << EOF
file 'title_5sec.mp4'
file 'anchor_lipsync.mp4'
file 'infographic_video.mp4'
EOF

# Step 5: 動画を結合
echo "🎞️ 動画を結合中..."
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy news_video_noaudio.mp4 -y

# Step 6: BGMの音量を調整（-20dB）
echo "🎵 BGMの音量を調整中..."
ffmpeg -i bgm.wav -filter:a "volume=-20dB" bgm_quiet.wav -y

# Step 7: 最終的な動画にBGMを追加
echo "🎬 最終動画を作成中..."
total_duration=$(ffmpeg -i news_video_noaudio.mp4 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); print 3600*A[1] + 60*A[2] + A[3] }')

# BGMをループさせて動画の長さに合わせる
ffmpeg -i news_video_noaudio.mp4 -stream_loop -1 -i bgm_quiet.wav -c:v copy -c:a aac -shortest -map 0:v -map 0:a? -map 1:a -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map "[a]" final_news_video.mp4 -y 2>/dev/null || \
ffmpeg -i news_video_noaudio.mp4 -stream_loop -1 -i bgm_quiet.wav -c:v copy -c:a aac -shortest final_news_video.mp4 -y

echo "✅ ニュース動画の作成が完了しました！"
echo "📺 出力ファイル: news_water_pipe/final_news_video.mp4"

# クリーンアップ（オプション）
# rm title_5sec.mp4 infographic_video.mp4 concat_list.txt news_video_noaudio.mp4 bgm_quiet.wav