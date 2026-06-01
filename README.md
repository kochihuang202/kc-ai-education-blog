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

## Cloudflare Pages

Cloudflare Pages 連 GitHub repository 後使用以下設定：

- Production branch: `main`
- Build command: `npm run build`
- Build directory: `dist`

`wrangler.jsonc` 也已設定 `pages_build_output_dir` 為 `./dist`。
