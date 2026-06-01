# KC AI 教育手記

AI 與教育主題部落格。第一版使用 Astro 產生靜態網站，部署目標是 Cloudflare Pages，文章正文以既有 `.html` 片段匯入。

## 本機指令

```bash
npm install
npm run dev
npm run build
```

本專案的 npm scripts 會在執行 Astro 時自動關閉 telemetry，避免本機建置嘗試寫入使用者設定資料夾。

## 新增文章

1. 把文章 HTML 片段放到 `src/article-html/posts/`。
2. 在 `src/data/posts.ts` 匯入該 HTML，新增一筆文章資料。
3. `categories` 可同時放多個分類：`parents`、`educators`、`society`、`core`。
4. 若有封面圖，放在 `public/images/`，並填入 `coverImage`。

## Cloudflare Workers / Pages

目前 Cloudflare dashboard 顯示此專案是 Workers application。正常目標是使用 Workers Static Assets 部署：

- Build command: `npm run build`
- Deploy command: `npm run deploy:cloudflare`
- Assets directory: `dist`

`wrangler.jsonc` 已設定 `assets.directory` 為 `./dist`，並啟用 `workers_dev` 讓專案可用 `*.workers.dev` 網址預覽。

Because Wrangler browser login did not complete on this Windows machine, the current live Worker was deployed through the Cloudflare API using `cloudflare/worker-proxy.js`. It serves the committed `dist/` files from GitHub raw URLs as a temporary bridge until Wrangler or native Workers Static Assets deployment is available.

## R2 圖片資產

- Bucket: `kc-ai-education-blog-assets`
- Public domain: `https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev`
- Current article graphics: `posts/letting-go-responsible-attitude/graphic-01.webp` through `graphic-10.webp`
