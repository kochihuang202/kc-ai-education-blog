import os
import sys
import json
import re
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publish_helper

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARTICLE = {
    "src": r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file\20260915先不要急著把「我害怕」，翻譯成「我做不到」",
    "slug": "dont-translate-fear-into-inability",
    "title": "先不要急著把「我害怕」，翻譯成「我做不到」",
    "date": "2026-09-15",
    "kicker": "KC 育兒手記",
    "excerpt": "我想趁孩子還小，讓她累積一種面對未知的先驗：害怕不是能力的判決，而是開始思考的提醒。",
    "categories": ["parents", "core"],
    "start_line": 9,
    "end_line": 381,
    "camel": "DontTranslateFearIntoInability"
}

def main():
    print("==========================================")
    print(f" Publishing: {ARTICLE['title']}")
    print(f" Slug: {ARTICLE['slug']}")
    print("==========================================")

    # 1. HTML extraction
    publish_helper.extract_html(
        src_dir=ARTICLE['src'],
        slug=ARTICLE['slug'],
        start_line=ARTICLE['start_line'],
        end_line=ARTICLE['end_line'],
        project_root=PROJECT_ROOT
    )

    # 2. Image processing
    img_count, temp_dir = publish_helper.process_images(
        src_dir=ARTICLE['src'],
        slug=ARTICLE['slug'],
        project_root=PROJECT_ROOT
    )
    print(f"[+] Total images processed: {img_count}")

    # 3. Upload to R2
    if img_count > 0:
        publish_helper.upload_to_r2(
            temp_img_dir=temp_dir,
            slug=ARTICLE['slug'],
            images_count=img_count
        )

    # 4. Update src/data/posts.ts
    posts_ts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    import_var = ARTICLE['camel'][0].lower() + ARTICLE['camel'][1:] + "Html"
    import_stmt = f'import {import_var} from "../article-html/posts/{ARTICLE["slug"]}.html?raw";\n'
    content = import_stmt + content

    var_base = ARTICLE['camel'][0].lower() + ARTICLE['camel'][1:] + "GraphicBase"
    var_gfx = ARTICLE['camel'][0].lower() + ARTICLE['camel'][1:] + "Graphics"
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
        f'    relatedPosts: [],\n'
        f'    body: {import_var}\n'
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
