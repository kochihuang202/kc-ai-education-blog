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

articles_config = [
    {
        "src_name": "20260828荒廢的價值",
        "slug": "value-of-wasting-time",
        "kicker": "KC 育兒手記",
        "categories": ["parents", "core"],
        "date": "2026-08-28",
        "has_inline_images": False
    },
    {
        "src_name": "20260828把書讀厚——親子共讀不是教讀書，是把自己傳過去",
        "slug": "parent-child-reading-passing-yourself-on",
        "kicker": "KC 育兒手記",
        "categories": ["parents", "core"],
        "date": "2026-08-28",
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
    
    match_num = re.search(r"^\D*(\d+).*\.(?:png|jpg|jpeg|webp)$", filename)
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

    lines = html_content.splitlines()
    start_line = None
    end_line = None
    
    for idx, line in enumerate(lines, 1):
        if ("<section" in line or "<div" in line) and "max-width:600px" in line:
            start_line = idx
            break
            
    for idx in range(len(lines), 0, -1):
        line = lines[idx - 1]
        if "</section>" in line or "</div>" in line:
            end_line = idx
            break
            
    if start_line is None or end_line is None:
        start_line = 9
        end_line = len(lines) - 1
        
    print(f"[+] Body range: lines {start_line} to {end_line}")
    inner_lines = lines[start_line - 1 : end_line]
    inner_html = "\n".join(inner_lines)

    title = ""
    for line in lines:
        match = re.search(r"<title>(.*?)</title>", line)
        if match:
            title = match.group(1).replace("-1", "").strip()
            break
    if not title:
        title = slug.replace("-", " ").capitalize()

    dest_path = os.path.join(PROJECT_ROOT, "src", "article-html", "posts", f"{slug}.html")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(inner_html)
    print(f"[+] Extracted HTML to {dest_path}")

    actual_text_parts = []
    greeting_found = False
    
    paras = re.findall(r"<p[^>]*>(.*?)</p>", inner_html, re.DOTALL)
    for p in paras:
        clean_p = re.sub(r"<[^>]+>", "", p)
        clean_p = clean_p.strip().replace("\n", "").replace("\r", "")
        if "嗨，大家好" in clean_p or "我是 KC" in clean_p or "每天陪你多想一點" in clean_p:
            continue
        if clean_p and not clean_p.startswith("——") and "第" not in clean_p and "篇" not in clean_p:
            actual_text_parts.append(clean_p)
            if len(" ".join(actual_text_parts)) > 100:
                break
                
    excerpt = " ".join(actual_text_parts).strip()[:125]
    if len(" ".join(actual_text_parts).strip()) > 125:
        excerpt += "..."
        
    return title, excerpt

def process_and_upload_assets(src_dir, config):
    slug = config["slug"]
    img_extensions = (".png", ".jpg", ".jpeg", ".webp")
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(img_extensions)]
    
    sorted_carousel = sorted(files, key=sort_key)
    temp_dir = os.path.join(PROJECT_ROOT, "tmp", slug)
    os.makedirs(temp_dir, exist_ok=True)
    
    uploaded_files = []
    
    print(f"[*] Processing {len(sorted_carousel)} carousel images...")
    for idx, f in enumerate(sorted_carousel, 1):
        target_name = f"graphic-{idx:02d}.webp"
        src_path = os.path.join(src_dir, f)
        local_dest = os.path.join(temp_dir, target_name)
        optimize_image(src_path, local_dest)
        
        r2_key = f"posts/{slug}/{target_name}"
        upload_r2_object(local_dest, r2_key)
        uploaded_files.append(target_name)
                
    shutil.rmtree(temp_dir)
    print(f"[+] Successfully processed and uploaded all assets for '{slug}'.")
    return len(sorted_carousel)

def register_post(slug, title, kicker, categories, date, carousel_count):
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
        
    posts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_path, "r", encoding="utf-8") as f:
        posts_content = f.read()
        
    if f'slug: "{slug}"' not in posts_content:
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
        
        related_slugs = ["value-of-wasting-time", "parent-child-reading-passing-yourself-on", "give-learning-time-back-to-kids", "why-learning-method-isnt-mainstream"]
        related_slugs = [s for s in related_slugs if s != slug]
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
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"
    deploy_result = subprocess.run(["npx.cmd" if os.name == "nt" else "npx", "wrangler", "deploy"], env=env, capture_output=True, text=True, encoding="utf-8")
    if deploy_result.returncode != 0:
        print("[-] Wrangler deployment failed!")
        print(deploy_result.stderr)
        sys.exit(1)
    print("[+] Deployed to Cloudflare successfully.")

    # 4. Sync with Git
    print("[*] Syncing with GitHub...")
    subprocess.run(["git", "add", "."])
    commit_msg = f"feat: publish two articles (2026-08-28) and deploy {deploy_version}"
    subprocess.run(["git", "commit", "-m", commit_msg])
    subprocess.run(["git", "push", "origin", "main"])
    print("[+] Changes pushed to GitHub.")

    print("\n[+] SUCCESS! All articles are live and deployed.")
    for slug in published_slugs:
        print(f"    - https://kc-ai-education-blog.ji3cp31p4.workers.dev/posts/{slug}/")

if __name__ == "__main__":
    main()
