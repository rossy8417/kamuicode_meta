#!/bin/bash

echo "📺 ニュース動画素材をダウンロード中..."

# ディレクトリ作成
mkdir -p news_water_pipe

# 動画素材
echo "🎬 動画をダウンロード..."
curl -o "news_water_pipe/title_animation.mp4" "https://v3.fal.media/files/rabbit/nGmdta6D60ReiivHRg5pB_output.mp4"
curl -o "news_water_pipe/anchor_lipsync.mp4" "https://v3.fal.media/files/panda/oO10ZTDxbkZ4rXLhfkBjx_output.mp4"

# 音声素材
echo "🎵 音声をダウンロード..."
curl -L "https://storage.googleapis.com/geminicli/lyria_outputs/lyria_output_JdvOgOQNg.wav?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcs-signer%40kamui-445410.iam.gserviceaccount.com%2F20250728%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250728T004854Z&X-Goog-Expires=3599&X-Goog-Signature=58d162dd8e189d696df9ff13be866c3968a356b4c624c2f1aa3b62a3622ae90f5f26d9b1587f77b24d61e5df6a792d3f8020266b4c15e51856714d5d3f4d726489421211fd87f2fe0df78968857aee27c01d9631688df836190dbaf8245d1021e5ba44e7cc88d09099ead135cf7e60a3729e67c448f45a6dc3dd883713ad4684cf2c7b4bba3e1e28f43b2b19bc886962c88a541b252537fd57a14ae6b0e1eb97e209a60d5d9f08835bf7186f8c4fb05fec0a8b5c5b9e6966b3b0331d789c9c0b5bfe8bc397a45b65ed2fdde9d68830f9eca510671b780f7b4a22a9cb01ce9833f40fd03167e9c6f3bdd84efb575f83597c3ec8ee53a12352433430292fc957d9&X-Goog-SignedHeaders=host" -o "news_water_pipe/bgm.wav"

echo "✅ すべての素材のダウンロードが完了しました！"
echo ""
echo "📁 ダウンロードされたファイル:"
echo "  - title_animation.mp4 (タイトルアニメーション)"
echo "  - anchor_lipsync.mp4 (リップシンク済みキャスター映像)"
echo "  - bgm.wav (BGM)"
echo ""
echo "💡 次のステップ: 動画編集ソフトでこれらの素材を組み合わせてください"