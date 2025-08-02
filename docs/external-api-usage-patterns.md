# External API Usage Patterns and Minimal Unit Design

## API別の用途分類と推奨ミニマルユニット分割

### 1. YouTube API
**主な用途:**
- 動画アップロード ✅ `youtube-upload.yml`
- 動画情報取得 → `youtube-video-info.yml` (新規)
- チャンネル情報取得 → `youtube-channel-info.yml` (新規)
- プレイリスト管理 → `youtube-playlist-manage.yml` (新規)
- 分析データ取得 → `youtube-analytics.yml` (新規)

### 2. NewsAPI
**主な用途:**
- トップヘッドライン取得 ✅ `newsapi-fetch.yml` (現在は汎用)
- キーワード検索 → 既存で対応可能
- ソース別ニュース → `newsapi-sources.yml` (新規)

### 3. OpenAI GPT API
**主な用途:**
- テキスト生成 ✅ `openai-gpt.yml`
- 要約生成 → `openai-summarize.yml` (新規)
- 翻訳 → `openai-translate.yml` (新規)
- コード生成 → `openai-code-gen.yml` (新規)
- 画像分析 (Vision) → `openai-vision.yml` (新規)

### 4. GitHub API
**主な用途:**
- Issue作成 ✅ `github-issue-create.yml`
- リポジトリ検索 ✅ `github-repo-search.yml`
- PR作成 → `github-pr-create.yml` (既存を改修)
- Release作成 → `github-release-create.yml` (新規)
- Workflow実行 → `github-workflow-dispatch.yml` (新規)
- コード検索 → `github-code-search.yml` (新規)

### 5. Google Sheets API
**主な用途:**
- データ書き込み ✅ `google-sheets-write.yml`
- データ読み取り → `google-sheets-read.yml` (新規)
- シート作成 → `google-sheets-create.yml` (新規)
- チャート生成 → `google-sheets-chart.yml` (新規)

### 6. Slack API
**主な用途:**
- メッセージ送信 ✅ `slack-notify.yml`
- ファイルアップロード → `slack-file-upload.yml` (新規)
- チャンネル作成 → `slack-channel-create.yml` (新規)
- ユーザー情報取得 → `slack-user-info.yml` (新規)

### 7. Twitter/X API
**主な用途:**
- ツイート投稿 ✅ `twitter-post.yml`
- ツイート検索 → `twitter-search.yml` (新規)
- トレンド取得 → `twitter-trends.yml` (新規)
- ユーザー情報取得 → `twitter-user-info.yml` (新規)
- メディアアップロード → `twitter-media-upload.yml` (新規)

### 8. Discord API
**主な用途:**
- Webhook送信 ✅ `discord-webhook.yml`
- Bot メッセージ送信 → `discord-bot-send.yml` (新規)
- チャンネル管理 → `discord-channel-manage.yml` (新規)
- 音声チャンネル操作 → `discord-voice.yml` (新規)

### 9. Reddit API
**主な用途:**
- 投稿検索 ✅ `reddit-search.yml`
- 投稿作成 → `reddit-post-create.yml` (新規)
- コメント投稿 → `reddit-comment.yml` (新規)
- サブレディット情報 → `reddit-subreddit-info.yml` (新規)

### 10. ElevenLabs API
**主な用途:**
- 音声生成 ✅ `elevenlabs-tts.yml`
- 音声クローン → `elevenlabs-voice-clone.yml` (新規)
- 音声履歴取得 → `elevenlabs-history.yml` (新規)

## リクエストボディの違いによる分割基準

### 分割すべきケース
1. **必須パラメータが大きく異なる場合**
   - 例: YouTube動画アップロード vs チャンネル情報取得

2. **レスポンス形式が異なる場合**
   - 例: テキスト生成 vs 画像分析

3. **認証スコープが異なる場合**
   - 例: 読み取り専用 vs 書き込み権限

4. **処理時間が大きく異なる場合**
   - 例: 単純な情報取得 vs 重い処理（動画アップロード）

### 統合可能なケース
1. **オプションパラメータで対応可能な場合**
   - 例: NewsAPIの検索条件違い

2. **同じエンドポイントで複数の用途に対応できる場合**
   - 例: OpenAI GPTのプロンプト違い

## 実装優先順位

### 高優先度（よく使われる）
1. `youtube-video-info.yml` - 動画情報取得
2. `openai-summarize.yml` - 要約生成
3. `twitter-search.yml` - ツイート検索
4. `google-sheets-read.yml` - データ読み取り
5. `github-workflow-dispatch.yml` - Workflow実行

### 中優先度（特定用途向け）
1. `openai-vision.yml` - 画像分析
2. `slack-file-upload.yml` - ファイル共有
3. `reddit-post-create.yml` - Reddit投稿
4. `youtube-analytics.yml` - 分析データ

### 低優先度（ニッチな用途）
1. `discord-voice.yml` - 音声チャンネル
2. `elevenlabs-voice-clone.yml` - 音声クローン
3. `twitter-trends.yml` - トレンド取得

## カスタムノードでの組み合わせ例

### ニュース配信ワークフロー
```yaml
jobs:
  fetch-news:
    uses: newsapi-fetch.yml
  
  summarize:
    uses: openai-summarize.yml
    needs: fetch-news
    
  post-twitter:
    uses: twitter-post.yml
    needs: summarize
    
  notify-slack:
    uses: slack-notify.yml
    needs: post-twitter
```

### データ分析レポート
```yaml
jobs:
  read-data:
    uses: google-sheets-read.yml
    
  analyze:
    uses: openai-gpt.yml
    needs: read-data
    
  create-chart:
    uses: google-sheets-chart.yml
    needs: analyze
    
  upload-github:
    uses: github-issue-create.yml
    needs: create-chart
```