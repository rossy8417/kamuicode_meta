# Script Generation Prompt

タスクプランに基づいて、実行スクリプトを生成してください。

## 生成するファイル
1. `script/generate-[workflow-type].js` - メインスクリプト
2. `script/lib/task-executor.js` - タスク実行エンジン
3. `script/lib/prompt-loader.js` - プロンプトローダー
4. `script/lib/utils.js` - 共通ユーティリティ

## メインスクリプトの構造
```javascript
const TaskExecutor = require('./lib/task-executor');
const { loadTaskConfig } = require('./lib/utils');

const main = async () => {
  // タスク設定の読み込み
  const taskConfig = loadTaskConfig();
  
  // 実行するタスクの決定
  const taskId = process.argv[2] || 'all';
  
  // タスク実行
  const executor = new TaskExecutor(taskConfig);
  
  if (taskId === 'all') {
    await executor.executeAll();
  } else {
    await executor.executeTask(taskId);
  }
};

main().catch(console.error);
```

## プロンプトローダーの実装
```javascript
const fs = require('fs');
const path = require('path');

const loadPrompt = (promptFile, variables = {}) => {
  const content = fs.readFileSync(promptFile, 'utf8');
  
  // 変数置換
  let processed = content;
  Object.entries(variables).forEach(([key, value]) => {
    processed = processed.replace(new RegExp(`{{${key}}}`, 'g'), value);
  });
  
  return processed;
};

module.exports = { loadPrompt };
```

## エラーハンドリング
- 各タスクは独立したtry-catchブロック
- 失敗時は詳細なエラー情報を記録
- リトライロジックの実装
- フォールバック戦略の実装