# 📖 KC AI 教育手記 - 新文章發布標準作業流程 (SOP)

本文件供開發人員及 AI 助理（如 Antigravity）使用，以確保在任何電腦上都能以完全相同、安全且優化（網頁載入效能最佳化、SEO 精準）的流程，將新文章與圖文解析圖片發布至部落格。

---

## 🛠️ 事前準備與依賴環境

在執行發布流程前，請確認該電腦已安裝並設定以下環境：
1. **Python 3**：需安裝圖片處理庫 Pillow。
   ```bash
   pip install Pillow
   ```
2. **Node.js & npm**：用於本地端 Astro 建置與 Wrangler 工具執行。
3. **Cloudflare Wrangler**：需登入以具備 Cloudflare R2 上傳權限。
   ```bash
   npx wrangler login
   ```
   *注意：若本機網路有安全憑證檢查限制，導致登入或部署失敗（例如顯示 `Wrangler authorization failed`），請在執行指令前先於終端機設定忽略憑證變數：*
   * *CMD: `set NODE_TLS_REJECT_UNAUTHORIZED=0`*
   * *PowerShell: `$env:NODE_TLS_REJECT_UNAUTHORIZED=0`*
4. **Git**：具備推送到專案 GitHub 倉庫的存取權限。
5. **Cloudflare 專案設定 (`wrangler.jsonc`)**：
   * 必須確保 `wrangler.jsonc` 包含 `"main": "cloudflare/worker-proxy.js"` 設定，否則 Cloudflare Git 自動建置只會更新靜態資源，而不會更新並部署 Worker 代理程式。


---

## 🚀 完整發布步驟

### 步驟 1：整理來源檔案
當您收到使用者提供的新文章時，確認資料夾內包含：
- **1 個 HTML 檔案**：內含文章網頁內容。
- **多張圖文解析圖片**：通常為 `.png` 或 `.jpg` 檔，檔名尾端應包含時序與編號括號，例如 `*(1).png` 至 `*(18).png`。
- **定義網址代稱 (Slug)**：根據主題轉換成適合的英文小寫代称，例如「不想處罰孩子，但真的很難」➔ `no-punishment-is-hard`。

---

### 步驟 2：執行自動化處理與上傳腳本 (`publish_helper.py`)
使用我們專門撰寫的自動化腳本，一次完成 **HTML 段落提取**、**圖片時序與編號排序**、**網頁級最優化處理（縮放/壓縮/剝離元資料）**，以及 **R2 自動上傳**。

執行以下指令：
```powershell
python scripts/publish_helper.py --src "[來源資料夾絕對路徑]" --slug "[文章代稱]" --excerpt "[1-2句吸引人的文章摘要]" --start-line 9 --end-line 331
```
*參數說明：*
- `--src`：包含原始 HTML 及圖片的資料夾路徑。
- `--slug`：文章網址代稱（如 `no-punishment-is-hard`）。
- `--excerpt`：文章的大意摘要（用於首頁及 SEO 搜尋結果）。
- `--start-line` 與 `--end-line`：原始 HTML 中，包含文章本文 `<section>...</section>` 區塊的起始與結束行數（預設為 9 到 331）。

**腳本將自動執行：**
1. 提取指定行數的 HTML 並儲存至 `src/article-html/posts/[slug].html`。
2. 排序圖片：依據檔名時間（上午/下午時序）與編號，精準排序為 `graphic-01.webp` 等。
3. 圖片優化：若圖片寬高大於 `1600px` 則等比例縮放至最高 `1600px`，轉換成 WebP（75% 品質），剝離 EXIF 元資料以最小化檔案大小。
4. 上傳 R2：繞過本機憑證限制（TLS bypass），自動將圖片上傳至 R2 儲存庫：`posts/[slug]/graphic-[01-XX].webp`。
5. 清除本機臨時產生的圖檔。
6. **自動於終端機輸出後續步驟 3 所需的程式碼範本**。

---

### 步驟 3：更新部落格註冊數據與 FB 狀態
根據步驟 2 腳本執行完畢後輸出在終端機的代碼範本，進行以下編輯：

1. **更新 `src/data/posts.ts`**：
   - **匯入內文**：在檔案頂部匯入剛剛生成的 HTML：
     ```typescript
     import [slug]Html from "../article-html/posts/[slug].html?raw";
     ```
   - **設定圖片 Gallery**：在 `export const posts = [` 陣列上方宣告圖片路徑與 alt：
     ```typescript
     const [slug]GraphicBase = "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/[slug]";
     const [slug]Graphics = Array.from({ length: [圖片數量] }, (_, index) => {
       const page = index + 1;
       return {
         src: `${[slug]GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
         alt: `[文章標題]圖文解析 ${page}/[圖片數量]`
       };
     });
     ```
   - **註冊文章**：在 `posts` 陣列的最上方插入新的文章物件（確保其顯示在首頁最前列）。
   - **建立雙向「延伸閱讀」連結**：
     - 在新文章物件的 `relatedPosts` 欄位填入相關文章的 Slug。
     - **重要**：回頭尋找這幾篇相關文章，在它們的 `relatedPosts` 欄位中也補上新文章的 Slug，確保讀者能雙向導流。

2. **更新 `src/data/fb-status.json`**：
   - 在 JSON 最上方插入新文章狀態，初始化為 `false`：
     ```json
     {
       "[slug]": false,
       ...
     }
     ```

---

### 步驟 4：本機編譯打包
在專案根目錄下執行 Astro 建置指令，確認沒有 TypeScript 語法錯誤且順利編譯：
```bash
npm run build
```
確認輸出目錄中成功生成了 `dist/posts/[slug]/index.html`。

---

### 步驟 5：提交與推送到 GitHub
將所有變更（含靜態建置產物 `dist/` 的內容）暫存、提交並推送至 GitHub：
```powershell
git add -A
git commit -m "feat: add [slug] article with gallery and bidirectional related posts links"
git push origin main
```
*說明：線上 Cloudflare Worker 代理會自動讀取 GitHub 上的最新 `dist/` 靜態檔案，因此推送成功後新文章即會在 1 分鐘內生效。*

---

### 步驟 6：線上驗證與交付
1. **驗證專屬連結**：在瀏覽器中開啟 `https://kc-ai-education-blog.ji3cp31p4.workers.dev/posts/[slug]/`，確認網頁能成功載入且圖片輪播正常。
2. **驗證首頁**：開啟 `https://kc-ai-education-blog.ji3cp31p4.workers.dev/`。
   - *注意：若首頁未即時看到新文章，通常是因為 Cloudflare CDN 快取（快取時間為 5 分鐘 / 300 秒）。請使用 `Ctrl + F5` 強制重新整理或稍候幾分鐘即可。*
3. **交付報告**：在對話中直接附上線上首頁、新文章頁面以及管理後台的點擊網址連結，方便使用者直接查閱。

---

## ⚠️ 疑難排解與備用方案（當 R2 / Wrangler 直連受限時）

若因帳號權限或 TLS 憑證攔截問題，導致無法使用 `publish_helper.py` 上傳圖片至 R2，請改用以下**本機圖片封裝備用流程**：

### 1. 本機圖片 WebP 轉檔與封裝
1. 在專案中執行 `convert.cjs` 或手動使用圖片工具（如 `sharp`、`Pillow`），將圖片等比例縮放至最高 `1600px`，並轉換為 `.webp` 格式（品質建議 80%）。
2. 將圖片依序命名為 `graphic-01.webp` 至 `graphic-XX.webp`。
3. 於專案目錄 `public/images/posts/[slug]/` 下建立以文章代稱命名的資料夾，並放入所有轉檔後的 WebP 圖片。

### 2. 註冊資料與程式碼設定
1. **編輯 `src/data/posts.ts`**：
   * 將文章的圖片 Base 路徑直接指向本機相對路徑：
     ```typescript
     const [slug]GraphicBase = "/images/posts/[slug]";
     ```
   * 其餘 Gallery 宣告與文章註冊流程與正常步驟相同。
2. **手動部署與推送**：
   * 本機執行 `npm run build` 確認編譯成功。
   * 使用 Git 將更新（包含 `public/images/posts/[slug]/` 的圖片與 `dist/` 建置產物）推送到 GitHub。
   * 若 Cloudflare 自動建置未即時反映，請在本機設定 `set NODE_TLS_REJECT_UNAUTHORIZED=0` 後，手動執行 `npm run deploy:cloudflare` 以強制上傳最新靜態資源與更新 Worker 腳本。

