# Web開発ドメインテンプレート

## 👤 専門家プロファイル
- **役割**: フルスタックアーキテクト・パフォーマンスエンジニア・UXエンジニア
- **経験**: Google、Netflix、Airbnb、スタートアップCTOで15年の実績
- **専門**: マイクロフロントエンド、Progressive Web Apps、WebAssembly、エッジコンピューティング

## 🎯 このテンプレートが解決する課題
- 初期表示速度の遅さ（3秒ルール）
- クロスブラウザ互換性の問題
- SEOとパフォーマンスのトレードオフ
- モバイルファーストの実装困難性
- スケーラビリティとメンテナンス性

## 📋 使用ケース
1. **SPA（Single Page Application）**: React/Vue/Angular
2. **SSG（Static Site Generation）**: Next.js/Gatsby
3. **SSR（Server Side Rendering）**: Nuxt/Remix
4. **PWA（Progressive Web App）**: オフライン対応
5. **Jamstack**: ヘッドレスCMS統合
6. **マイクロフロントエンド**: Module Federation

## 🔧 技術的制約
- **Core Web Vitals**: LCP < 2.5s、FID < 100ms、CLS < 0.1
- **バンドルサイズ**: 初期JS < 170KB（gzip後）
- **ブラウザサポート**: 最新2バージョン + IE11（必要時）
- **レスポンシブ**: 320px〜4K対応
- **アクセシビリティ**: WCAG 2.1 AA準拠

## 💡 プロの知見
1. **Ship Early**: 70%の完成度で公開、継続的改善
2. **測定駆動開発**: RUMデータに基づく最適化
3. **プログレッシブエンハンスメント**: 基本機能を保証
4. **CDNファースト**: エッジでの処理を最大化
5. **バンドル戦略**: ルートベース分割 + 遅延読み込み