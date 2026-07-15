import os
import sys
import re
import shutil
import subprocess
import json
from datetime import datetime
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUCKET_NAME = "kc-ai-education-blog-assets"

# Define the articles to publish
articles_config = [
    {
        "src_name": "20260713兩個物體怎麼連？——從硬想到AI幫你想",
        "slug": "how-to-link-two-objects",
        "kicker": "記憶學_應用 · 第四篇",
        "categories": ["memory-science-app", "parents", "core"],
        "date": "2026-07-13",
        "has_inline_images": False
    },
    {
        "src_name": "20260713腦中的圖，要看得見——AI製圖讓記憶從模糊變確定",
        "slug": "making-brain-images-visible",
        "kicker": "記憶學_應用 · 第五篇",
        "categories": ["memory-science-app", "parents", "core"],
        "date": "2026-07-13",
        "has_inline_images": True,
        "inline_images_info": [
            {"src_name": "1.png", "target_name": "image-1.webp", "placeholder": "【第一張：】", "caption": "第一張：板橋到瑞芳（巧虎到外套）"},
            {"src_name": "2.png", "target_name": "image-2.webp", "placeholder": "【第二張：】", "caption": "第二張：侯硐到頂雙溪（烏龜到瀑布）"},
            {"src_name": "3.png", "target_name": "image-3.webp", "placeholder": "【第三張：】", "caption": "第三張：貢寮到石城（大象到鬧鐘）"},
            {"src_name": "4.png", "target_name": "image-4.webp", "placeholder": "【第四張：】", "caption": "第四張：大里到花蓮（長頸鹿到大便）"}
        ]
    },
    {
        "src_name": "20260713位置記憶法的規模化——從A4排版到5∞結構圖",
        "slug": "scaling-up-method-of-loci",
        "kicker": "記憶學_應用 · 第六篇",
        "categories": ["memory-science-app", "parents", "core"],
        "date": "2026-07-13",
        "has_inline_images": True,
        "inline_images_info": [
            {"src_name": "1.png", "target_name": "image-1.webp", "placeholder": "【第一張：1-25站結構圖】", "caption": "1-25站結構圖"},
            {"src_name": "2.png", "target_name": "image-2.webp", "placeholder": "【第二張：25-48站結構圖】", "caption": "25-48站結構圖"},
            {"src_name": "3.png", "target_name": "image-3.webp", "placeholder": "【第三張：1-48站合併全景圖】", "caption": "1-48站合併全景圖"}
        ]
    },
    {
        "src_name": "20260714數字編碼00-99——當孩子編不出來，AI幫他找到能懂的配對-1",
        "slug": "number-coding-00-99",
        "kicker": "記憶學_應用 · 第七篇",
        "categories": ["memory-science-app", "parents", "core"],
        "date": "2026-07-14",
        "has_inline_images": False
    }
]

SOURCE_BASE_DIR = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"

def sort_key(filename):
    ampm = 1 if "下午" in filename else 0
    match = re.search(r"(?:上午|下午)(\d+)_(\d+)_(\d+)\s*\((\d+)\)\.(?:png|jpg|jpeg|webp)$", filename)
    if match:
        h, m, s, num = map(int, match.groups())
        return (ampm, h, m, s, num)
    
    match_num = re.search(r"\((\d+)\)\.(?:png|jpg|jpeg|webp)$", filename)
    if match_num:
        return (0, 0, 0, 0, int(match_num.group(1)))
    return (0, 0, 0, 0, filename)

def optimize_image(src_path, dest_path):
    with Image.open(src_path) as img:
        w, h = img.size
        max_size = 1600
        if w > max_size or h > max_size:
            if w > h:
                new_w = max_size
                new_h = int(h * max_size / w)
            else:
                new_h = max_size
                new_w = int(w * max_size / h)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img.save(dest_path, "WEBP", quality=75)

def upload_r2_object(local_path, r2_key):
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"
    
    cmd = [
        "npx.cmd" if os.name == "nt" else "npx",
        "wrangler",
        "r2",
        "object",
        "put",
        f"{BUCKET_NAME}/{r2_key}",
        "--file",
        local_path,
        "--remote"
    ]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"[-] Failed to upload {local_path} to {r2_key}!")
        print(result.stderr)
        sys.exit(1)

def extract_html_and_metadata(src_dir, config):
    slug = config["slug"]
    html_file = None
    for f in os.listdir(src_dir):
        if f.endswith(".html"):
            html_file = os.path.join(src_dir, f)
            break
            
    if not html_file:
        print(f"[-] Error: No HTML file found in {src_dir}")
        sys.exit(1)
        
    print(f"[+] Found HTML file: {html_file}")
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Locate body range
    lines = html_content.splitlines()
    start_line = None
    end_line = None
    
    for idx, line in enumerate(lines, 1):
        if "<section" in line and "max-width:600px" in line:
            start_line = idx
            break
            
    for idx in range(len(lines), 0, -1):
        line = lines[idx - 1]
        if "</section>" in line:
            end_line = idx
            break
            
    if start_line is None or end_line is None:
        start_line = 9
        end_line = len(lines) - 2
        
    print(f"[+] Body range: lines {start_line} to {end_line}")
    inner_lines = lines[start_line - 1 : end_line]
    inner_html = "\n".join(inner_lines)

    # Title extraction
    title = ""
    for line in lines:
        match = re.search(r"<title>(.*?)</title>", line)
        if match:
            title = match.group(1).replace("-1", "").strip()
            break
    if not title:
        title = slug.replace("-", " ").capitalize()

    # Handle inline images replacement
    if config["has_inline_images"]:
        for img_info in config["inline_images_info"]:
            placeholder = img_info["placeholder"]
            target_name = img_info["target_name"]
            caption = img_info["caption"]
            
            # Pattern matching: <section style="...">\s*<p[^>]*>【...】</p>\s*</section>
            # Let's write a flexible regex to replace the entire placeholder card block
            pattern = re.compile(
                r'<section style="background-color:#F0EBE4;padding:40px 20px;margin:0 0 (?:12|22|0)px? 0;text-align:center;border-radius:2px;">\s*<p[^>]*>' + re.escape(placeholder) + r'</p>\s*</section>',
                re.DOTALL
            )
            
            replacement = (
                f'<figure style="margin: 0 0 24px 0; text-align: center;">\n'
                f'  <img src="https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}/{target_name}" alt="{caption}" style="width: 100%; max-width: 600px; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />\n'
                f'  <figcaption style="margin-top: 8px; font-size: 14px; color: #8A817A; font-style: italic;">{caption}</figcaption>\n'
                f'</figure>'
            )
            
            inner_html, count = pattern.subn(replacement, inner_html)
            if count > 0:
                print(f"[+] Replaced inline image placeholder '{placeholder}' with webp tag.")
            else:
                # Fallback if styling is slightly different
                fallback_pattern = re.compile(re.escape(placeholder))
                inner_html, fallback_count = fallback_pattern.subn(replacement, inner_html)
                if fallback_count > 0:
                    print(f"[!] Replaced inline image placeholder using fallback: '{placeholder}'")
                else:
                    print(f"[-] Warning: Placeholder '{placeholder}' not found in HTML!")

    dest_path = os.path.join(PROJECT_ROOT, "src", "article-html", "posts", f"{slug}.html")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(inner_html)
    print(f"[+] Extracted HTML to {dest_path}")

    # Excerpt extraction
    sections = inner_html.split("<section")
    actual_text_parts = []
    greeting_found = False
    
    for sec in sections:
        if "嗨，大家好，我是" in sec or "我是 KC" in sec:
            greeting_found = True
            continue
            
        if greeting_found:
            paras = re.findall(r"<p[^>]*>(.*?)</p>", sec, re.DOTALL)
            for p in paras:
                clean_p = re.sub(r"<[^>]+>", "", p)
                clean_p = clean_p.strip().replace("\n", "").replace("\r", "")
                if clean_p and not clean_p.startswith("——") and "系列導讀" not in clean_p and "第" not in clean_p and "篇" not in clean_p:
                    actual_text_parts.append(clean_p)
            if len("".join(actual_text_parts)) > 100:
                break
                
    if not actual_text_parts:
        paras = re.findall(r"<p[^>]*>(.*?)</p>", inner_html, re.DOTALL)
        for p in paras:
            clean_p = re.sub(r"<[^>]+>", "", p)
            clean_p = clean_p.strip().replace("\n", "").replace("\r", "")
            if clean_p and not clean_p.startswith("嗨，大家好") and not clean_p.startswith("每天陪你多想") and not clean_p.startswith("——") and "第" not in clean_p and "篇" not in clean_p:
                actual_text_parts.append(clean_p)
                if len("".join(actual_text_parts)) > 100:
                    break
                    
    excerpt = " ".join(actual_text_parts).strip()[:125]
    if len(" ".join(actual_text_parts).strip()) > 125:
        excerpt += "..."
        
    return title, excerpt

def process_and_upload_assets(src_dir, config):
    slug = config["slug"]
    img_extensions = (".png", ".jpg", ".jpeg", ".webp")
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(img_extensions)]
    
    # Separate inline images and carousel images
    inline_names = []
    if config["has_inline_images"]:
        inline_names = [img["src_name"] for img in config["inline_images_info"]]
        
    carousel_files = [f for f in files if f not in inline_names]
    sorted_carousel = sorted(carousel_files, key=sort_key)
    
    temp_dir = os.path.join(PROJECT_ROOT, "tmp", slug)
    os.makedirs(temp_dir, exist_ok=True)
    
    uploaded_files = []
    
    # 1. Process Carousel Graphics
    print(f"[*] Processing {len(sorted_carousel)} carousel images...")
    for idx, f in enumerate(sorted_carousel, 1):
        target_name = f"graphic-{idx:02d}.webp"
        src_path = os.path.join(src_dir, f)
        local_dest = os.path.join(temp_dir, target_name)
        optimize_image(src_path, local_dest)
        
        r2_key = f"posts/{slug}/{target_name}"
        upload_r2_object(local_dest, r2_key)
        uploaded_files.append(target_name)
        
    # 2. Process Inline Images
    if config["has_inline_images"]:
        print(f"[*] Processing {len(inline_names)} inline images...")
        for img_info in config["inline_images_info"]:
            src_name = img_info["src_name"]
            target_name = img_info["target_name"]
            src_path = os.path.join(src_dir, src_name)
            local_dest = os.path.join(temp_dir, target_name)
            
            if os.path.exists(src_path):
                optimize_image(src_path, local_dest)
                r2_key = f"posts/{slug}/{target_name}"
                upload_r2_object(local_dest, r2_key)
                uploaded_files.append(target_name)
                print(f"[+] Uploaded inline image {src_name} -> {target_name}")
            else:
                print(f"[-] Error: Inline image file {src_path} not found!")
                sys.exit(1)
                
    shutil.rmtree(temp_dir)
    print(f"[+] Successfully processed and uploaded all assets for '{slug}'.")
    return len(sorted_carousel)

def register_post(slug, title, kicker, categories, date, carousel_count):
    # 1. Update fb-status.json
    fb_status_path = os.path.join(PROJECT_ROOT, "src", "data", "fb-status.json")
    with open(fb_status_path, "r", encoding="utf-8") as f:
        fb_status = json.load(f)
        
    if slug not in fb_status:
        new_fb = {slug: False}
        for k, v in fb_status.items():
            new_fb[k] = v
        with open(fb_status_path, "w", encoding="utf-8") as f:
            json.dump(new_fb, f, indent=2, ensure_ascii=False)
        print(f"[+] Registered '{slug}' in fb-status.json")
        
    # 2. Update posts.ts
    posts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_path, "r", encoding="utf-8") as f:
        posts_content = f.read()
        
    if slug not in posts_content:
        import_camel = "".join(x.capitalize() for x in slug.split("-"))
        import_camel_lc = import_camel[0].lower() + import_camel[1:]
        
        import_line = f'import {import_camel_lc}Html from "../article-html/posts/{slug}.html?raw";'
        
        graphics_block = (
            f'const {import_camel_lc}GraphicBase =\n'
            f'  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}";\n\n'
            f'const {import_camel_lc}Graphics = Array.from({{ length: {carousel_count} }}, (_, index) => {{\n'
            f'  const page = index + 1;\n'
            f'  return {{\n'
            f'    src: `${{{import_camel_lc}GraphicBase}}/graphic-${{String(page).padStart(2, "0")}}.webp`,\n'
            f'    alt: `{title}圖文解析 ${{page}}/{carousel_count}`\n'
            f'  }};\n'
            f'}});\n\n'
        )
        
        # Link related posts bidirectionally
        related_slugs = ["remembering-48-stations-in-43-minutes", "how-to-actually-use-memory-science", "how-would-you-remember-fruits-of-four-seasons"]
        related_str = "[" + ", ".join(f'"{s}"' for s in related_slugs) + "]"
        
        cat_list_str = "[" + ", ".join(f'"{c}"' for c in categories) + "]"
        post_object = (
            f'  {{\n'
            f'    title: "{title}",\n'
            f'    slug: "{slug}",\n'
            f'    date: "{date}",\n'
            f'    kicker: "{kicker}",\n'
            f'    excerpt:\n'
            f'      "{excerpt_global}",\n'
            f'    categories: {cat_list_str},\n'
            f'    coverImage: {import_camel_lc}Graphics[0].src,\n'
            f'    coverAlt: {import_camel_lc}Graphics[0].alt,\n'
            f'    gallery: {{\n'
            f'      label: "<圖文解析>",\n'
            f'      images: {import_camel_lc}Graphics\n'
            f'    }},\n'
            f'    relatedPosts: {related_str},\n'
            f'    body: {import_camel_lc}Html\n'
            f'  }},\n'
        )
        
        lines = posts_content.splitlines()
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") and "?raw" in line:
                last_import_idx = i
        lines.insert(last_import_idx + 1, import_line)
        
        posts_content_temp = "\n".join(lines)
        posts_content_temp = posts_content_temp.replace(
            "export const posts = [",
            graphics_block + "export const posts = [\n" + post_object
        )
        
        # Inject bidirectional links
        for r_slug in related_slugs:
            pattern = re.compile(
                rf'(slug:\s*"{r_slug}".*?relatedPosts:\s*\[)([^]]*?)(\])',
                re.DOTALL
            )
            def repl(m):
                content_inside = m.group(2).strip()
                if not content_inside:
                    return f'{m.group(1)}"{slug}"{m.group(3)}'
                if f'"{slug}"' in content_inside:
                    return m.group(0)
                return f'{m.group(1)}{content_inside}, "{slug}"{m.group(3)}'
            posts_content_temp = pattern.sub(repl, posts_content_temp)
            
        with open(posts_path, "w", encoding="utf-8") as f:
            f.write(posts_content_temp)
        print(f"[+] Registered '{slug}' in posts.ts with bidirectional links.")
    else:
        print(f"[*] Already registered '{slug}' in posts.ts")

# ----------------- Main Flow -----------------
def main():
    global excerpt_global
    
    published_slugs = []
    
    for config in articles_config:
        src_dir = os.path.join(SOURCE_BASE_DIR, config["src_name"])
        print(f"\n[*] Processing article from: {src_dir}")
        
        if not os.path.exists(src_dir):
            print(f"[-] Error: Source directory '{src_dir}' does not exist!")
            sys.exit(1)
            
        title, excerpt = extract_html_and_metadata(src_dir, config)
        excerpt_global = excerpt
        
        carousel_count = process_and_upload_assets(src_dir, config)
        
        register_post(
            slug=config["slug"],
            title=title,
            kicker=config["kicker"],
            categories=config["categories"],
            date=config["date"],
            carousel_count=carousel_count
        )
        published_slugs.append(config["slug"])

    # 1. Update DEPLOY_VERSION in worker-proxy.js
    proxy_path = os.path.join(PROJECT_ROOT, "cloudflare", "worker-proxy.js")
    with open(proxy_path, "r", encoding="utf-8") as f:
        proxy_content = f.read()
        
    deploy_version = f"v_{datetime.now().strftime('%Y_%m_%d_%H_%M')}"
    proxy_content = re.sub(
        r'const DEPLOY_VERSION = "v_\d+_\d+_\d+_\d+_\d+";',
        f'const DEPLOY_VERSION = "{deploy_version}";',
        proxy_content
    )
    with open(proxy_path, "w", encoding="utf-8") as f:
        f.write(proxy_content)
    print(f"\n[+] Bumped proxy DEPLOY_VERSION to: {deploy_version}")

    # 2. Rebuild project
    print("[*] Rebuilding project...")
    build_result = subprocess.run(["npm.cmd" if os.name == "nt" else "npm", "run", "build"], capture_output=True, text=True, encoding="utf-8")
    if build_result.returncode != 0:
        print("[-] Build failed!")
        print(build_result.stderr)
        sys.exit(1)
    print("[+] Project built and sitemap regenerated.")

    # 3. Deploy to Cloudflare Workers
    print("[*] Deploying to Cloudflare Workers...")
    deploy_result = subprocess.run(["npx.cmd" if os.name == "nt" else "npx", "wrangler", "deploy"], capture_output=True, text=True, encoding="utf-8")
    if deploy_result.returncode != 0:
        print("[-] Wrangler deployment failed!")
        print(deploy_result.stderr)
        sys.exit(1)
    print("[+] Deployed to Cloudflare successfully.")

    # 4. Sync with Git
    print("[*] Syncing with GitHub...")
    subprocess.run(["git", "add", "."])
    commit_msg = f"feat: publish four memory-science articles and deploy {deploy_version}"
    subprocess.run(["git", "commit", "-m", commit_msg])
    subprocess.run(["git", "push", "origin", "main"])
    print("[+] Changes pushed to GitHub.")

    print("\n[+] SUCCESS! All four articles are live and deployed.")
    for slug in published_slugs:
        print(f"    - https://kc-ai-education-blog.ji3cp31p4.workers.dev/posts/{slug}/")

if __name__ == "__main__":
    main()
