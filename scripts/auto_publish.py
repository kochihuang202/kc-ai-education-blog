import os
import sys
import re
import argparse
import subprocess
import shutil
import json
from datetime import datetime
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUCKET_NAME = "kc-ai-education-blog-assets"

def get_args():
    parser = argparse.ArgumentParser(description="KC AI Education Blog - Fully Automated Article Publisher")
    parser.add_argument("--src", required=True, help="Path to source folder containing HTML and images")
    parser.add_argument("--slug", required=True, help="Slug for the article (e.g., no-punishment-is-hard)")
    parser.add_argument("--kicker", default="KC 育兒手記", help="Article kicker category (default: KC 育兒手記)")
    parser.add_argument("--categories", default="parents,core", help="Comma-separated category IDs (default: parents,core)")
    parser.add_argument("--date", help="Publish date YYYY-MM-DD (defaults to today)")
    return parser.parse_args()

def extract_html_and_metadata(src_dir, slug):
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
        lines = f.readlines()
        
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
        print(f"[-] Warning: Could not auto-detect section boundaries. Defaulting to 9 and {len(lines) - 2}")
        start_line = 9
        end_line = len(lines) - 2
        
    print(f"[+] Auto-detected body range: lines {start_line} to {end_line}")
    inner_html = "".join(lines[start_line - 1 : end_line])
    
    dest_path = os.path.join(PROJECT_ROOT, "src", "article-html", "posts", f"{slug}.html")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(inner_html)
    print(f"[+] Extracted HTML section to {dest_path}")
    
    # Title extraction
    title = ""
    for line in lines:
        match = re.search(r"<title>(.*?)</title>", line)
        if match:
            title = match.group(1).replace("-1", "").strip()
            break
    if not title:
        title = slug.replace("-", " ").capitalize()
        
    # Excerpt extraction (skip cover and greeting blocks)
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
        # Fallback
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

def process_images(src_dir, slug):
    img_extensions = (".png", ".jpg", ".jpeg", ".webp")
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(img_extensions)]
    
    if not files:
        print("[-] Warning: No images found in source folder.")
        return 0, None
        
    sorted_files = sorted(files, key=sort_key)
    temp_img_dir = os.path.join(PROJECT_ROOT, "tmp", slug)
    os.makedirs(temp_img_dir, exist_ok=True)
    
    optimized_files = []
    for idx, file in enumerate(sorted_files, 1):
        new_name = f"graphic-{idx:02d}.webp"
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(temp_img_dir, new_name)
        
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
        optimized_files.append(new_name)
        
    print(f"[+] Optimized {len(optimized_files)} images.")
    return len(optimized_files), temp_img_dir

def upload_to_r2(temp_img_dir, slug, images_count):
    if not temp_img_dir or images_count == 0:
        return
        
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"
    
    print(f"[*] Uploading {images_count} images to Cloudflare R2 bucket '{BUCKET_NAME}'...")
    for i in range(1, images_count + 1):
        filename = f"graphic-{i:02d}.webp"
        local_path = os.path.join(temp_img_dir, filename)
        r2_key = f"posts/{slug}/{filename}"
        
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
            print(f"[-] Failed to upload {filename}!")
            print(result.stderr)
            sys.exit(1)
            
    print("[+] All images successfully uploaded to Cloudflare R2.")
    shutil.rmtree(temp_img_dir)

def register_codebase(slug, title, kicker, categories_str, date_str, images_count):
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
        print("[+] Registered in fb-status.json")
        
    # 2. Update posts.ts
    posts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_path, "r", encoding="utf-8") as f:
        posts_content = f.read()
        
    if slug not in posts_content:
        import_camel = "".join(x.capitalize() for x in slug.split("-"))
        import_camel_lc = import_camel[0].lower() + import_camel[1:]
        
        # Prepare imports & graphics block
        import_line = f'import {import_camel_lc}Html from "../article-html/posts/{slug}.html?raw";'
        
        graphics_block = (
            f'const {import_camel_lc}GraphicBase =\n'
            f'  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}";\n\n'
            f'const {import_camel_lc}Graphics = Array.from({{ length: {images_count} }}, (_, index) => {{\n'
            f'  const page = index + 1;\n'
            f'  return {{\n'
            f'    src: `${{{import_camel_lc}GraphicBase}}/graphic-${{String(page).padStart(2, "0")}}.webp`,\n'
            f'    alt: `{title}圖文解析 ${{page}}/{images_count}`\n'
            f'  }};\n'
            f'}});\n\n'
        )
        
        # Find related post slugs in the same categories to link bidirectionally
        cat_ids = [c.strip() for c in categories_str.split(",")]
        # Simple extraction of other slugs in the file to build relations
        existing_slugs = re.findall(r'slug:\s*"([^"]+)"', posts_content)
        related_slugs = [s for s in existing_slugs if s != slug][:3] # Pick top 3
        
        related_str = "[" + ", ".join(f'"{s}"' for s in related_slugs) + "]"
        
        # Post Object
        cat_list_str = "[" + ", ".join(f'"{c}"' for c in cat_ids) + "]"
        post_object = (
            f'  {{\n'
            f'    title: "{title}",\n'
            f'    slug: "{slug}",\n'
            f'    date: "{date_str}",\n'
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
        
        # Injects imports
        lines = posts_content.splitlines()
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") and "?raw" in line:
                last_import_idx = i
        lines.insert(last_import_idx + 1, import_line)
        
        posts_content_temp = "\n".join(lines)
        
        # Inject graphics & post object
        posts_content_temp = posts_content_temp.replace(
            "export const posts = [",
            graphics_block + "export const posts = [\n" + post_object
        )
        
        # Inject bidirectional links into those related posts
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
            
        print("[+] Registered in posts.ts with bidirectional related links.")
    else:
        print("[*] Already registered in posts.ts")

def rebuild_and_deploy():
    print("[*] Rebuilding project...")
    build_cmd = ["npm.cmd", "run", "build"] if os.name == "nt" else ["npm", "run", "build"]
    result = subprocess.run(build_cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print("[-] Build failed!")
        print(result.stderr)
        sys.exit(1)
    print("[+] Project built and sitemap regenerated.")
    
    # Bump DEPLOY_VERSION
    proxy_path = os.path.join(PROJECT_ROOT, "cloudflare", "worker-proxy.js")
    with open(proxy_path, "r", encoding="utf-8") as f:
        proxy_content = f.read()
        
    now_str = datetime.now().strftime("v_%Y_%m_%d_%H_%M")
    pattern = re.compile(r'const DEPLOY_VERSION = "v_.*?";')
    proxy_content = pattern.sub(f'const DEPLOY_VERSION = "{now_str}";', proxy_content)
    
    with open(proxy_path, "w", encoding="utf-8") as f:
        f.write(proxy_content)
    print(f"[+] Cleaned cache via DEPLOY_VERSION = {now_str}")
    
    # Deploy wrangler
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"
    
    print("[*] Deploying to Cloudflare Workers...")
    deploy_cmd = ["npx.cmd", "wrangler", "deploy"] if os.name == "nt" else ["npx", "wrangler", "deploy"]
    result = subprocess.run(deploy_cmd, env=env, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print("[-] Cloudflare deployment failed!")
        print(result.stderr)
        sys.exit(1)
    print("[+] Deployed to Cloudflare successfully.")
    
    # Git sync
    print("[*] Syncing with GitHub...")
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", f"feat: publish article and deploy {now_str}"])
    subprocess.run(["git", "push", "origin", "main"])
    print("[+] Code pushed to GitHub repository.")

if __name__ == "__main__":
    args = get_args()
    date_val = args.date if args.date else datetime.now().strftime("%Y-%m-%d")
    
    print(f"[*] Starting publication workflow for: {args.slug}")
    
    # 1. Parse and extract HTML/Excerpt
    global excerpt_global
    title_val, excerpt_global = extract_html_and_metadata(args.src, args.slug)
    print(f"[+] Title: {title_val}")
    print(f"[+] Excerpt: {excerpt_global}")
    
    # 2. Image conversion & optimization
    img_count, temp_dir = process_images(args.src, args.slug)
    
    # 3. R2 upload
    upload_to_r2(temp_dir, args.slug, img_count)
    
    # 4. Codebase registration
    register_codebase(args.slug, title_val, args.kicker, args.categories, date_val, img_count)
    
    # 5. Build, Cache bust, Deploy & Git push
    rebuild_and_deploy()
    
    print(f"\n[+] SUCCESS! Article is live at: https://kc-ai-education-blog.ji3cp31p4.workers.dev/posts/{args.slug}/")
