import os
import sys
import json
import re
import shutil
import subprocess
import datetime
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"C:\Users\ji3cp\Documents\antigravity\kc-ai-education-blog"
SRC_DIR = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file\20261018減少自由選項，反而養出自驅力"

ARTICLE = {
    "src": SRC_DIR,
    "slug": "reducing-free-choices-builds-self-drive",
    "title": "減少自由選項，反而養出自驅力",
    "date": "2026-10-18",
    "kicker": "KC 育兒手記",
    "excerpt": "當孩子抗拒時，我曾以為給她自由、放慢腳步能等她自己好起來，結果她只學會放大「我不喜歡」。真正能幫孩子長出自驅力的，不是無底限的自由，而是收攏選項、守住底盤。",
    "categories": ["parents", "core"],
    "start_line": 9,
    "end_line": 168,
    "camel": "ReducingFreeChoicesBuildsSelfDrive",
    "related": ["separate-empathy-from-rules", "giving-freedom-with-clear-non-negotiable-boundaries", "stop-reminding-kids-building-real-self-discipline"]
}

def extract_page_num(filename):
    m = re.search(r'-(\d+)\.(png|jpg|webp)$', filename)
    if m: return int(m.group(1))
    m = re.search(r'\((\d+)\)\.(png|jpg|webp)$', filename)
    if m: return int(m.group(1))
    m = re.match(r'^(\d+)_', filename)
    if m: return int(m.group(1))
    return 0

def main():
    print("==========================================")
    print(f" Publishing: {ARTICLE['title']}")
    print(f" Slug: {ARTICLE['slug']}")
    print("==========================================")

    # 1. HTML extraction
    html_file = None
    for f in os.listdir(ARTICLE['src']):
        if f.endswith(".html"):
            html_file = os.path.join(ARTICLE['src'], f)
            break

    if not html_file:
        print(f"[-] Error: No HTML found in {ARTICLE['src']}")
        sys.exit(1)

    with open(html_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    last_sec = ARTICLE['end_line']
    inner_html = "".join(lines[ARTICLE['start_line'] - 1 : last_sec])
    dest_path = os.path.join(PROJECT_ROOT, "src", "article-html", "posts", f"{ARTICLE['slug']}.html")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(inner_html)
    print(f"[+] Extracted HTML fragment to {dest_path} ({last_sec - ARTICLE['start_line'] + 1} lines)")

    # 2. Image processing
    img_files = [f for f in os.listdir(ARTICLE['src']) if f.endswith(".png") or f.endswith(".jpg")]
    sorted_imgs = sorted(img_files, key=extract_page_num)
    img_count = len(sorted_imgs)
    print(f"[+] Found {img_count} images:")
    for idx, f in enumerate(sorted_imgs, 1):
        print(f"  {idx:02d}: {f}")

    temp_dir = os.path.join(PROJECT_ROOT, "tmp", ARTICLE['slug'])
    os.makedirs(temp_dir, exist_ok=True)

    for idx, f in enumerate(sorted_imgs, 1):
        src_path = os.path.join(ARTICLE['src'], f)
        dest_name = f"graphic-{idx:02d}.webp"
        dest_file = os.path.join(temp_dir, dest_name)

        with Image.open(src_path) as im:
            im = im.convert("RGB")
            if im.width > 1600:
                ratio = 1600.0 / im.width
                new_size = (1600, int(im.height * ratio))
                im = im.resize(new_size, Image.Resampling.LANCZOS)
            im.save(dest_file, format="WEBP", quality=75, method=6)
        print(f"[+] Converted {f} -> {dest_name}")

    # 3. Upload to Cloudflare R2
    bucket = "kc-ai-education-blog-assets"
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"

    print(f"[*] Uploading {img_count} images to Cloudflare R2 bucket '{bucket}'...")
    for idx in range(1, img_count + 1):
        filename = f"graphic-{idx:02d}.webp"
        local_path = os.path.join(temp_dir, filename)
        r2_key = f"posts/{ARTICLE['slug']}/{filename}"
        cmd = [
            "npx.cmd" if os.name == "nt" else "npx",
            "wrangler",
            "r2",
            "object",
            "put",
            f"{bucket}/{r2_key}",
            "--file",
            local_path,
            "--remote"
        ]
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            print(f"[-] Failed to upload {filename}: {res.stderr}")
            sys.exit(1)
        print(f"  [+] Uploaded {filename} to posts/{ARTICLE['slug']}/")

    shutil.rmtree(temp_dir)
    print("[+] All images uploaded and local temp cleaned.")

    # 4. Update src/data/posts.ts
    posts_ts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    camel_lc = ARTICLE['camel'][0].lower() + ARTICLE['camel'][1:]
    import_stmt = f'import {camel_lc}Html from "../article-html/posts/{ARTICLE["slug"]}.html?raw";\n'
    content = import_stmt + content

    var_base = f"{camel_lc}GraphicBase"
    var_gfx = f"{camel_lc}Graphics"
    graphics_decl = (
        f'const {var_base} =\n'
        f'  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{ARTICLE["slug"]}";\n\n'
        f'const {var_gfx} = Array.from({{ length: {img_count} }}, (_, index) => {{\n'
        f'  const page = index + 1;\n'
        f'  return {{\n'
        f'    src: `${{{var_base}}}/graphic-${{String(page).padStart(2, "0")}}.webp`,\n'
        f'    alt: `{ARTICLE["title"]}圖文解析 ${{page}}/{img_count}`\n'
        f'  }};\n'
        f'}});\n\n'
    )
    content = content.replace("export const posts = [", graphics_decl + "export const posts = [")

    rel_str = ", ".join(f'"{r}"' for r in ARTICLE["related"])
    post_obj = (
        f'  {{\n'
        f'    title: "{ARTICLE["title"]}",\n'
        f'    slug: "{ARTICLE["slug"]}",\n'
        f'    date: "{ARTICLE["date"]}",\n'
        f'    kicker: "{ARTICLE["kicker"]}",\n'
        f'    excerpt:\n'
        f'      "{ARTICLE["excerpt"]}",\n'
        f'    categories: ["parents", "core"],\n'
        f'    coverImage: {var_gfx}[0].src,\n'
        f'    coverAlt: {var_gfx}[0].alt,\n'
        f'    gallery: {{\n'
        f'      label: "<圖文解析>",\n'
        f'      images: {var_gfx}\n'
        f'    }},\n'
        f'    relatedPosts: [{rel_str}],\n'
        f'    body: {camel_lc}Html\n'
        f'  }},\n'
    )
    content = content.replace("export const posts = [\n", "export const posts = [\n" + post_obj)

    with open(posts_ts_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[+] Updated src/data/posts.ts")

    # 5. Update src/data/fb-status.json
    fb_json_path = os.path.join(PROJECT_ROOT, "src", "data", "fb-status.json")
    with open(fb_json_path, "r", encoding="utf-8") as f:
        fb_data = json.load(f)

    new_fb = {ARTICLE["slug"]: False}
    new_fb.update(fb_data)
    with open(fb_json_path, "w", encoding="utf-8") as f:
        json.dump(new_fb, f, ensure_ascii=False, indent=2)
    print("[+] Updated src/data/fb-status.json")

    # 6. Update DEPLOY_VERSION in cloudflare/worker-proxy.js
    worker_js_path = os.path.join(PROJECT_ROOT, "cloudflare", "worker-proxy.js")
    with open(worker_js_path, "r", encoding="utf-8") as f:
        worker_code = f.read()

    now_str = datetime.datetime.now().strftime("v_%Y_%m_%d_%H_%M_%S")
    worker_code = re.sub(r'const DEPLOY_VERSION = "[^"]+";', f'const DEPLOY_VERSION = "{now_str}";', worker_code)
    with open(worker_js_path, "w", encoding="utf-8") as f:
        f.write(worker_code)
    print(f"[+] Updated DEPLOY_VERSION in cloudflare/worker-proxy.js to {now_str}")

if __name__ == "__main__":
    main()
