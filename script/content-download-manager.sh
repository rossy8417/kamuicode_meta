#!/bin/bash
"""
AI生成コンテンツダウンロード・処理管理システム
統一されたダウンロード・品質向上・検証プロセス

Usage:
    ./content-download-manager.sh --url "https://..." --type image --iteration 1
"""

set -e

# デフォルト設定
CONTENT_TYPE="image"
ITERATION=1
WORKING_DIR="$(pwd)"
QUALITY_THRESHOLD=70

# ヘルプ表示
show_help() {
    cat << EOF
Content Download Manager - AI生成コンテンツ統合処理システム

Usage: $0 [OPTIONS]

Options:
    --url URL           認証済みフルURL (必須)
    --type TYPE         コンテンツタイプ (image|video|audio|3d) [default: image]
    --iteration NUM     イテレーション番号 (1-3) [default: 1]
    --category CAT      コンテンツカテゴリ (general|product|lifestyle等) [default: general]
    --working-dir DIR   作業ディレクトリ [default: current directory]
    --help             このヘルプを表示

Examples:
    $0 --url "https://storage.googleapis.com/very-long-google-url..." --type image --iteration 1
    $0 --url "https://fal.ai/files/short-fal-url.jpg" --type image --iteration 2 --category product
EOF
}

# パラメータ解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            CONTENT_URL="$2"
            shift 2
            ;;
        --type)
            CONTENT_TYPE="$2"
            shift 2
            ;;
        --iteration)
            ITERATION="$2"
            shift 2
            ;;
        --category)
            CONTENT_CATEGORY="$2"
            shift 2
            ;;
        --working-dir)
            WORKING_DIR="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# 必須パラメータチェック
if [ -z "$CONTENT_URL" ]; then
    echo "❌ Error: --url is required"
    show_help
    exit 1
fi

# 初期化
echo "🚀 Content Download Manager - Iteration $ITERATION"
echo "   URL: ${CONTENT_URL:0:80}..."
echo "   Type: $CONTENT_TYPE"
echo "   Category: ${CONTENT_CATEGORY:-general}"
echo "   Working Directory: $WORKING_DIR"
echo ""

cd "$WORKING_DIR"

# ログディレクトリ作成
mkdir -p .logs/content-processing

# ファイル名生成（URLから拡張子推定）
if [[ "$CONTENT_URL" == *".jpg"* ]] || [[ "$CONTENT_URL" == *"jpeg"* ]]; then
    EXT="jpg"
elif [[ "$CONTENT_URL" == *".png"* ]]; then
    EXT="png"
elif [[ "$CONTENT_URL" == *".webp"* ]]; then
    EXT="webp"
elif [[ "$CONTENT_URL" == *".mp4"* ]]; then
    EXT="mp4"
elif [[ "$CONTENT_URL" == *".wav"* ]] || [[ "$CONTENT_URL" == *".mp3"* ]]; then
    EXT="wav"
else
    # デフォルト拡張子
    case "$CONTENT_TYPE" in
        "image") EXT="jpg" ;;
        "video") EXT="mp4" ;;
        "audio") EXT="wav" ;;
        "3d") EXT="obj" ;;
        *) EXT="dat" ;;
    esac
fi

# ダウンロードファイル名生成
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DOWNLOADED_FILE="${CONTENT_TYPE}_${TIMESTAMP}_iter${ITERATION}.${EXT}"
FULL_PATH="$WORKING_DIR/$DOWNLOADED_FILE"

echo "📥 Step 1: Downloading content..."
echo "   Target file: $DOWNLOADED_FILE"

# ダウンロード実行（フルURL使用）
if curl -L -o "$DOWNLOADED_FILE" "$CONTENT_URL"; then
    echo "✅ Download successful: $DOWNLOADED_FILE"
    
    # フルパス出力（ホームディレクトリ基準）
    HOME_RELATIVE_PATH="${FULL_PATH/#$HOME/~}"
    echo "📁 Full path: $HOME_RELATIVE_PATH"
    
    # ファイルサイズ確認
    FILE_SIZE=$(stat -f%z "$DOWNLOADED_FILE" 2>/dev/null || stat -c%s "$DOWNLOADED_FILE" 2>/dev/null || echo "unknown")
    echo "📊 File size: $FILE_SIZE bytes"
else
    echo "❌ Download failed"
    exit 1
fi

echo ""
echo "🔍 Step 2: Opening and inspecting content..."

# ファイルオープン（OS別対応）
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$DOWNLOADED_FILE"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open "$DOWNLOADED_FILE"
    elif command -v display &> /dev/null; then
        display "$DOWNLOADED_FILE" &
    fi
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash/Cygwin)
    start "$DOWNLOADED_FILE"
fi

echo "👀 Content opened for inspection"
echo ""

# 品質向上処理（画像の場合）
if [ "$CONTENT_TYPE" = "image" ]; then
    echo "🎨 Step 3: Quality Enhancement Process..."
    
    # Python品質向上スクリプト実行
    if [ -f "script/enhance-content-quality.py" ]; then
        python3 script/enhance-content-quality.py \
            --input "$DOWNLOADED_FILE" \
            --type image \
            --iteration "$ITERATION" \
            --content-type "${CONTENT_CATEGORY:-general}"
        
        ENHANCEMENT_EXIT_CODE=$?
        
        if [ $ENHANCEMENT_EXIT_CODE -eq 0 ]; then
            echo "✅ Quality enhancement completed"
            
            # 強化されたファイルパス
            ENHANCED_FILE="${DOWNLOADED_FILE%.*}_enhanced_iter${ITERATION}.${EXT}"
            
            if [ -f "$ENHANCED_FILE" ]; then
                ENHANCED_FULL_PATH="$WORKING_DIR/$ENHANCED_FILE"
                ENHANCED_HOME_PATH="${ENHANCED_FULL_PATH/#$HOME/~}"
                echo "🎯 Enhanced file: $ENHANCED_HOME_PATH"
                
                # 強化されたファイルもオープン
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    open "$ENHANCED_FILE"
                elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                    if command -v xdg-open &> /dev/null; then
                        xdg-open "$ENHANCED_FILE"
                    fi
                elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
                    start "$ENHANCED_FILE"
                fi
                
                # 品質チェック結果確認
                if [ -f "quality_enhancement_iter${ITERATION}.json" ]; then
                    QUALITY_SCORE=$(python3 -c "
import json
try:
    with open('quality_enhancement_iter${ITERATION}.json', 'r') as f:
        data = json.load(f)
    print(f\"{data['quality_check']['score']:.1f}\")
except:
    print('0')
")
                    
                    echo "📊 Quality Score: $QUALITY_SCORE/100"
                    
                    # 次のイテレーション判定
                    if (( $(echo "$QUALITY_SCORE < $QUALITY_THRESHOLD" | bc -l) )) && [ "$ITERATION" -lt 3 ]; then
                        echo ""
                        echo "⚠️ Quality threshold not met. Next iteration recommended."
                        echo "🔄 Suggested next command:"
                        echo "   $0 --url \"$CONTENT_URL\" --type $CONTENT_TYPE --iteration $((ITERATION + 1)) --category ${CONTENT_CATEGORY:-general}"
                        
                        # ログに記録
                        cat >> .logs/content-processing/iteration_log.txt << EOF
$(date): Iteration $ITERATION completed
- Original: $HOME_RELATIVE_PATH
- Enhanced: $ENHANCED_HOME_PATH
- Quality Score: $QUALITY_SCORE/100
- Status: Needs next iteration
- URL: $CONTENT_URL

EOF
                    else
                        echo ""
                        echo "🎉 Quality threshold met! Processing complete."
                        echo "✅ Final result: $ENHANCED_HOME_PATH"
                        
                        # 成功ログ記録
                        cat >> .logs/content-processing/iteration_log.txt << EOF
$(date): Iteration $ITERATION completed successfully
- Original: $HOME_RELATIVE_PATH
- Enhanced: $ENHANCED_HOME_PATH
- Quality Score: $QUALITY_SCORE/100
- Status: COMPLETED
- URL: $CONTENT_URL

EOF
                    fi
                fi
            fi
        else
            echo "❌ Quality enhancement failed"
        fi
    else
        echo "⚠️ Quality enhancement script not found, skipping..."
    fi
else
    echo "ℹ️ Quality enhancement currently supports images only"
    
    # 非画像コンテンツのログ記録
    cat >> .logs/content-processing/iteration_log.txt << EOF
$(date): Content downloaded - Iteration $ITERATION
- File: $HOME_RELATIVE_PATH
- Type: $CONTENT_TYPE
- Status: Downloaded and opened
- URL: $CONTENT_URL

EOF
fi

echo ""
echo "📋 Step 4: Process Summary"
echo "   - Download: ✅"
echo "   - Open: ✅"
if [ "$CONTENT_TYPE" = "image" ]; then
    echo "   - Quality Enhancement: ✅"
    echo "   - Quality Check: ✅"
fi
echo "   - Full Path Output: ✅"
echo ""
echo "✅ Content processing iteration $ITERATION completed"

# 次ステップの指示
if [ "$ITERATION" -lt 3 ] && [ "$CONTENT_TYPE" = "image" ]; then
    echo ""
    echo "🔄 Iterative Improvement Process:"
    echo "   Current: Iteration $ITERATION/3"
    echo "   Next: Review the opened files and run iteration $((ITERATION + 1)) if needed"
    echo "   Goal: Achieve 3 iterations for optimal quality"
fi