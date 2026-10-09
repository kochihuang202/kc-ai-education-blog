import os
import sys
import re
import json
import shutil
import subprocess
import datetime
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"C:\Users\ji3cp\Documents\antigravity\kc-ai-education-blog"
BASE_DIR = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file\20261010內在動機"

ARTICLES = [
    {
        "index": 1,
        "folder": "01_我一直以為自己懂「內在動機」",
        "title": "我一直以為自己懂「內在動機」",
        "slug": "i-thought-i-understood-intrinsic-motivation",
        "camel": "iThoughtIUnderstoodIntrinsicMotivation",
        "excerpt": "我一直以為自己懂「內在動機」，直到我開始追問：你說的「內在」，到底是哪一種？孩子不用催會自己去做，但如果推著他的是恐懼、羞恥、責任或好奇呢？",
        "related": ["if-all-desire-is-intrinsic-motivation-always-better", "what-we-truly-want-is-not-just-intrinsic-motivation", "is-extrinsic-motivation-really-inferior"]
    },
    {
        "index": 2,
        "folder": "02_如果都是慾望，內在動機就一定比較好嗎？",
        "title": "如果都是慾望，內在動機就一定比較好嗎？",
        "slug": "if-all-desire-is-intrinsic-motivation-always-better",
        "camel": "ifAllDesireIsIntrinsicMotivationAlwaysBetter",
        "excerpt": "想吃糖是慾望，想知道答案也是慾望。當我真的一路追下去，我開始懷疑：我們一直想替孩子培養的「內在動機」，真的天然就比較值得追求嗎？",
        "related": ["i-thought-i-understood-intrinsic-motivation", "what-we-truly-want-is-not-just-intrinsic-motivation", "learning-only-interests-leads-to-fewer-choices"]
    },
    {
        "index": 3,
        "folder": "03_我們真正想要的，也許不只是「內在動機」",
        "title": "我們真正想要的，也許不只是「內在動機」",
        "slug": "what-we-truly-want-is-not-just-intrinsic-motivation",
        "camel": "whatWeTrulyWantIsNotJustIntrinsicMotivation",
        "excerpt": "父母研究動機，說到底不是想學心理學。我們只是希望有一天孩子不需要一直被催、被盯、被推，也願意自己往前走。但平常說的內在動機混了太多東西。",
        "related": ["if-all-desire-is-intrinsic-motivation-always-better", "learning-only-interests-leads-to-fewer-choices", "when-kids-lack-interest-can-we-only-wait"]
    },
    {
        "index": 4,
        "folder": "04_只學有興趣的，最後不是更自由，而是更沒得選",
        "title": "只學有興趣的，最後不是更自由，而是更沒得選",
        "slug": "learning-only-interests-leads-to-fewer-choices",
        "camel": "learningOnlyInterestsLeadsToFewerChoices",
        "excerpt": "研究了 SDT 之後，我反而開始重新檢查我們天天掛在嘴上的「興趣」。如果「有沒有興趣」變成學不學的最高標準，我們保護的究竟是孩子，還是他當下的感受？",
        "related": ["what-we-truly-want-is-not-just-intrinsic-motivation", "when-kids-lack-interest-can-we-only-wait", "do-kids-need-constant-success-for-competence"]
    },
    {
        "index": 5,
        "folder": "05_孩子沒興趣，我們真的只能等嗎？",
        "title": "孩子沒興趣，我們真的只能等嗎？",
        "slug": "when-kids-lack-interest-can-we-only-wait",
        "camel": "whenKidsLackInterestCanWeOnlyWait",
        "excerpt": "我們不能命令孩子愛上數學、閱讀或英文。但這不代表大人只能站在旁邊等。研究 SDT 之後，我開始轉向思考：什麼環境支持內在動機，又是什麼環境會磨掉它？",
        "related": ["learning-only-interests-leads-to-fewer-choices", "do-kids-need-constant-success-for-competence", "is-autonomy-just-letting-kids-choose"]
    },
    {
        "index": 6,
        "folder": "06_孩子需要能力感，所以要讓他一直成功嗎？",
        "title": "孩子需要能力感，所以要讓他一直成功嗎？",
        "slug": "do-kids-need-constant-success-for-competence",
        "camel": "doKidsNeedConstantSuccessForCompetence",
        "excerpt": "我原本以為能力感就是多讓孩子成功、少讓他挫折。直到我開始追問：如果永遠只做已經會的事，真的會更有能力感嗎？",
        "related": ["when-kids-lack-interest-can-we-only-wait", "is-autonomy-just-letting-kids-choose", "learning-never-happens-only-in-the-brain"]
    },
    {
        "index": 7,
        "folder": "07_自主，就是讓孩子自己選嗎？",
        "title": "自主，就是讓孩子自己選嗎？",
        "slug": "is-autonomy-just-letting-kids-choose",
        "camel": "isAutonomyJustLettingKidsChoose",
        "excerpt": "做得到和願意做，是兩件不同的事。一個人明明知道「我做得到」，卻還是可能說「可是我不想做」。我從這裡開始理解 SDT 另一個核心——自主。",
        "related": ["do-kids-need-constant-success-for-competence", "learning-never-happens-only-in-the-brain", "from-you-want-me-to-do-to-i-find-it-worthwhile"]
    },
    {
        "index": 8,
        "folder": "08_學習，從來不只發生在孩子腦袋裡",
        "title": "學習，從來不只發生在孩子腦袋裡",
        "slug": "learning-never-happens-only-in-the-brain",
        "camel": "learningNeverHappensOnlyInTheBrain",
        "excerpt": "同一個孩子遇到不同老師，狀態可以差很多。你愈想影響孩子，愈不能忽略你們之間發生了什麼；關係讓話能進得去，學習從來不只發生在孩子腦袋裡。",
        "related": ["is-autonomy-just-letting-kids-choose", "from-you-want-me-to-do-to-i-find-it-worthwhile", "is-extrinsic-motivation-really-inferior"]
    },
    {
        "index": 9,
        "folder": "09_從「你要我做」到「我自己也認為值得」，中間到底發生了什麼？",
        "title": "從「你要我做」到「我自己也認為值得」，中間到底發生了什麼？",
        "slug": "from-you-want-me-to-do-to-i-find-it-worthwhile",
        "camel": "fromYouWantMeToDoToIFindItWorthwhile",
        "excerpt": "我們真正想要的，也許不是孩子最後被歸類成「內在動機」，而是他有一天能自己願意學。這正是自我決定理論中最關鍵的概念：內化（internalization）。",
        "related": ["learning-never-happens-only-in-the-brain", "is-extrinsic-motivation-really-inferior", "i-thought-i-understood-intrinsic-motivation"]
    },
    {
        "index": 10,
        "folder": "10_外在動機，真的比較差嗎？",
        "title": "外在動機，真的比較差嗎？",
        "slug": "is-extrinsic-motivation-really-inferior",
        "camel": "isExtrinsicMotivationReallyInferior",
        "excerpt": "當學習需要經歷枯燥與長期累積，父母該怎麼要求，才能讓孩子逐漸形成自己的學習理由？要求不等於每次都要吵到贏，也不要把關係搞壞。",
        "related": ["from-you-want-me-to-do-to-i-find-it-worthwhile", "i-thought-i-understood-intrinsic-motivation", "if-all-desire-is-intrinsic-motivation-always-better"]
    }
]

def extract_page_num(filename):
    m = re.search(r'-(\d+)\.(png|jpg|webp)$', filename)
    if m: return int(m.group(1))
    m = re.match(r'^(\d+)_', filename)
    if m: return int(m.group(1))
    return None

def main():
    print("=================================================================")
    print(" BATCH PUBLISHING: 【內在動機】系列（共 10 篇）")
    print("=================================================================")

    # Step 1: Update categories.ts
    print("\n[1/7] Updating src/data/categories.ts...")
    cat_file = os.path.join(PROJECT_ROOT, "src", "data", "categories.ts")
    with open(cat_file, "r", encoding="utf-8") as f:
        cat_content = f.read()

    new_cat = """  {
    id: "intrinsic-motivation",
    label: "內在動機",
    summary: "十篇文章拆解自我決定理論（SDT）：從慾望、興趣、能力感、自主到內化，釐清孩子真正願意學的底層動力。",
    accent: "#D96B27"
  },
] as const;"""

    if "intrinsic-motivation" not in cat_content:
        cat_content = cat_content.replace("] as const;", new_cat)
        with open(cat_file, "w", encoding="utf-8") as f:
            f.write(cat_content)
        print("  [+] Added intrinsic-motivation category.")
    else:
        print("  [*] Category intrinsic-motivation already exists.")

    # Step 2: Update series.ts
    print("\n[2/7] Updating src/data/series.ts...")
    series_file = os.path.join(PROJECT_ROOT, "src", "data", "series.ts")
    with open(series_file, "r", encoding="utf-8") as f:
        series_content = f.read()

    series_steps = []
    for art in ARTICLES:
        series_steps.append(f'      {{ slug: "{art["slug"]}", title: "第{art["index"]}篇 ｜ {art["title"]}", label: "{art["index"]}" }}')
    steps_joined = ",\n".join(series_steps)

    new_series_block = f"""  {{
    id: "intrinsic-motivation",
    name: "內在動機（共 10 篇）",
    accent: "#D96B27",
    steps: [
{steps_joined}
    ]
  }},
];"""

    if "intrinsic-motivation" not in series_content:
        series_content = series_content.replace("];", new_series_block)
        with open(series_file, "w", encoding="utf-8") as f:
            f.write(series_content)
        print("  [+] Added intrinsic-motivation series config.")
    else:
        print("  [*] Series intrinsic-motivation already exists.")

    # Step 3: Extract HTML fragments
    print("\n[3/7] Extracting HTML fragments...")
    for art in ARTICLES:
        folder_path = os.path.join(BASE_DIR, art["folder"])
        html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
        if not html_files:
            print(f"  [-] Error: No HTML found in {art['folder']}")
            sys.exit(1)
        src_html = os.path.join(folder_path, html_files[0])
        with open(src_html, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Find line 9 (index 8) to final </section>
        last_sec = -1
        for idx in range(len(lines) - 1, -1, -1):
            if "</section>" in lines[idx]:
                last_sec = idx + 1
                break
        
        extracted = "".join(lines[8:last_sec])
        dest_html = os.path.join(PROJECT_ROOT, "src", "article-html", "posts", f"{art['slug']}.html")
        os.makedirs(os.path.dirname(dest_html), exist_ok=True)
        with open(dest_html, "w", encoding="utf-8") as f:
            f.write(extracted)
        print(f"  [+] #{art['index']} Extracted {last_sec-8} lines to {art['slug']}.html")

    # Step 4: Process images and upload to Cloudflare R2
    print("\n[4/7] Processing images and uploading to Cloudflare R2...")
    bucket = "kc-ai-education-blog-assets"
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"

    temp_root = os.path.join(PROJECT_ROOT, "temp_intrinsic_images")
    if os.path.exists(temp_root):
        shutil.rmtree(temp_root)
    os.makedirs(temp_root, exist_ok=True)

    for art in ARTICLES:
        print(f"\n  Processing #{art['index']}: {art['title']}...")
        folder_path = os.path.join(BASE_DIR, art["folder"])
        img_files = [f for f in os.listdir(folder_path) if f.endswith(".png") or f.endswith(".jpg")]
        
        # Sort images 1 to 10
        sorted_imgs = sorted(img_files, key=lambda f: extract_page_num(f))
        if len(sorted_imgs) != 10:
            print(f"  [-] Error: Expected 10 images for {art['folder']}, found {len(sorted_imgs)}")
            sys.exit(1)

        art_temp = os.path.join(temp_root, art["slug"])
        os.makedirs(art_temp, exist_ok=True)

        # Convert to WebP
        for idx, img_name in enumerate(sorted_imgs, start=1):
            src_img = os.path.join(folder_path, img_name)
            out_name = f"graphic-{idx:02d}.webp"
            out_path = os.path.join(art_temp, out_name)

            with Image.open(src_img) as im:
                im = im.convert("RGB")
                if im.width > 1600:
                    ratio = 1600.0 / im.width
                    new_size = (1600, int(im.height * ratio))
                    im = im.resize(new_size, Image.Resampling.LANCZOS)
                
                # Strip EXIF and save WebP quality 75
                im.save(out_path, format="WEBP", quality=75, method=6)

            # Upload to Cloudflare R2
            r2_key = f"posts/{art['slug']}/{out_name}"
            cmd = [
                "npx.cmd" if os.name == "nt" else "npx",
                "wrangler",
                "r2",
                "object",
                "put",
                f"{bucket}/{r2_key}",
                "--file",
                out_path,
                "--remote"
            ]
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")
            if result.returncode != 0:
                print(f"    [-] Failed to upload {out_name} to R2: {result.stderr}")
                sys.exit(1)
            print(f"    [+] Uploaded {out_name} to posts/{art['slug']}/")

    # Cleanup temp images
    shutil.rmtree(temp_root)
    print("\n  [+] All 100 images processed and uploaded to Cloudflare R2 successfully!")

    # Step 5: Update posts.ts
    print("\n[5/7] Updating src/data/posts.ts...")
    posts_file = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_file, "r", encoding="utf-8") as f:
        posts_content = f.read()

    # 5.1 Imports at top
    import_lines = []
    for art in ARTICLES:
        import_lines.append(f'import {art["camel"]}Html from "../article-html/posts/{art["slug"]}.html?raw";')
    imports_joined = "\n".join(import_lines) + "\n"

    # Insert imports right at the beginning
    posts_content = imports_joined + posts_content

    # 5.2 Graphic bases & definitions
    graphic_defs = []
    for art in ARTICLES:
        graphic_defs.append(f"""const {art["camel"]}GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{art["slug"]}";

const {art["camel"]}Graphics = Array.from({{ length: 10 }}, (_, index) => {{
  const page = index + 1;
  return {{
    src: `${{{art["camel"]}GraphicBase}}/graphic-${{String(page).padStart(2, "0")}}.webp`,
    alt: `{art["title"]}圖文解析 ${{page}}/10`
  }};
}});
""")
    graphics_joined = "\n".join(graphic_defs)

    posts_array_marker = "export const posts = ["
    posts_content = posts_content.replace(posts_array_marker, graphics_joined + "\n" + posts_array_marker)

    # 5.3 Post objects inserted in order 1 to 10
    post_objs = []
    for art in ARTICLES:
        rel_str = ", ".join(f'"{r}"' for r in art["related"])
        obj = f"""  {{
    title: "{art["title"]}",
    slug: "{art["slug"]}",
    date: "2026-10-10",
    kicker: "內在動機 · 第{art["index"]}篇",
    excerpt:
      "{art["excerpt"]}",
    categories: ["intrinsic-motivation", "parents", "core"],
    coverImage: {art["camel"]}Graphics[0].src,
    coverAlt: {art["camel"]}Graphics[0].alt,
    gallery: {{
      label: "<圖文解析>",
      images: {art["camel"]}Graphics
    }},
    relatedPosts: [{rel_str}],
    body: {art["camel"]}Html
  }},"""
        post_objs.append(obj)
    
    posts_objs_joined = "\n".join(post_objs) + "\n"
    posts_content = posts_content.replace(posts_array_marker, posts_array_marker + "\n" + posts_objs_joined)

    with open(posts_file, "w", encoding="utf-8") as f:
        f.write(posts_content)
    print("  [+] Successfully updated src/data/posts.ts with 10 articles.")

    # Step 6: Update fb-status.json
    print("\n[6/7] Updating src/data/fb-status.json...")
    fb_file = os.path.join(PROJECT_ROOT, "src", "data", "fb-status.json")
    with open(fb_file, "r", encoding="utf-8") as f:
        fb_data = json.load(f)

    # Prepend the 10 slugs
    new_fb = {}
    for art in ARTICLES:
        new_fb[art["slug"]] = False
    for k, v in fb_data.items():
        if k not in new_fb:
            new_fb[k] = v

    with open(fb_file, "w", encoding="utf-8") as f:
        json.dump(new_fb, f, ensure_ascii=False, indent=2)
    print("  [+] Successfully updated fb-status.json.")

    # Step 7: Update DEPLOY_VERSION in worker-proxy.js
    print("\n[7/7] Updating DEPLOY_VERSION in cloudflare/worker-proxy.js...")
    proxy_file = os.path.join(PROJECT_ROOT, "cloudflare", "worker-proxy.js")
    with open(proxy_file, "r", encoding="utf-8") as f:
        proxy_content = f.read()

    new_version = datetime.datetime.now().strftime("v_%Y_%m_%d_%H_%M_%S")
    proxy_content = re.sub(r'const DEPLOY_VERSION = "[^"]+";', f'const DEPLOY_VERSION = "{new_version}";', proxy_content)
    with open(proxy_file, "w", encoding="utf-8") as f:
        f.write(proxy_content)
    print(f"  [+] Bumping DEPLOY_VERSION to {new_version}.")

    print("\n=================================================================")
    print(" ALL 7 STEPS COMPLETE! READY FOR BUILD AND DEPLOY.")
    print("=================================================================")

if __name__ == "__main__":
    main()
