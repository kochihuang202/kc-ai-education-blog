import os
import re
import sys
import json
import subprocess
from datetime import datetime
from PIL import Image

src_dir = r"C:\Users\ji3cp\OneDrive\Documents\40_AI_folder\PO文網站\file\20260625來了解記憶學如何快速記憶四季水果"
project_root = r"C:\Users\ji3cp\OneDrive\Documents\40_AI_folder\PO文網站"
slug = "how-to-actually-use-memory-science"
title = "記憶學到底怎麼用——一個同事的四次試錯"
kicker = "記憶學_應用 · 第二篇"
categories_str = "memory-science-app,parents,core"
date_str = datetime.now().strftime("%Y-%m-%d")

tmp_dir = os.path.join(project_root, "tmp", slug)
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# 1. Parse and extract HTML, replacing placeholders with images
html_path = os.path.join(src_dir, "來了解記憶學如何快速記憶四季水果.html")
with open(html_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract inner HTML (lines 9 to 247, 1-based index)
inner_html = "".join(lines[8:247])

# Inline images captions
captions = {
    1: "第一次試錯：擺在一起不等於連結",
    2: "第二次試錯：缺了與春天的連結，且夏天的物品缺乏互動",
    3: "第三次試錯：背景過於花俏，視覺元素過多造成記憶干擾",
    4: "第四次成功方案：無背景白底，僅保留核心物品與流暢的因果動作連結"
}

for i in range(1, 5):
    placeholder = f'<p style="font-family:Georgia,\'Noto Serif SC\',\'Songti SC\',serif;font-size:13px;color:#8A817A;line-height:1.6;margin:0 0 6px 0;text-align:center;">〔插入圖片 {i}.png〕</p>'
    img_tag = f"""<!-- 內文插圖 {i} -->
<div style="margin:24px auto;max-width:500px;text-align:center;">
  <img src="https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}/image-{i}.webp" alt="{captions[i]}" style="width:100%;height:auto;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.08);border:1px solid rgba(192,81,47,0.15);" />
  <p style="font-family:Georgia,'Noto Serif SC','Songti SC',serif;font-size:13px;color:#8A817A;line-height:1.6;margin:8px 0 0 0;text-align:center;">{captions[i]}</p>
</div>"""
    inner_html, count = re.subn(re.escape(placeholder), img_tag, inner_html)
    print(f"Replaced placeholder {i} -> {count} match")

# Extract excerpt
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

dest_html_path = os.path.join(project_root, "src", "article-html", "posts", f"{slug}.html")
os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)
with open(dest_html_path, "w", encoding="utf-8") as f:
    f.write(inner_html)
print(f"[+] Saved HTML to {dest_html_path}")
print(f"[+] Excerpt: {excerpt}")

# 2. Process and optimize images
# 2a. Carousel images (graphic-XX.webp)
carousel_files = []
for f in os.listdir(src_dir):
    if f.startswith("ChatGPT Image") and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        match = re.search(r"\((\d+)\)\.(?:png|jpg|jpeg|webp)$", f)
        if match:
            num = int(match.group(1))
            carousel_files.append((num, f))
carousel_files.sort()

processed_carousel = []
for idx, (num, f) in enumerate(carousel_files, 1):
    new_name = f"graphic-{idx:02d}.webp"
    src_path = os.path.join(src_dir, f)
    dest_path = os.path.join(tmp_dir, new_name)
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
    print(f"Processed Carousel: {f} -> {new_name}")
    processed_carousel.append(new_name)

# 2b. Inline images (image-1.webp to image-4.webp)
processed_inline = []
for i in range(1, 5):
    f = f"{i}.png"
    new_name = f"image-{i}.webp"
    src_path = os.path.join(src_dir, f)
    dest_path = os.path.join(tmp_dir, new_name)
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
    print(f"Processed Inline: {f} -> {new_name}")
    processed_inline.append(new_name)

# 3. Upload all to Cloudflare R2
bucket = "kc-ai-education-blog-assets"
env = os.environ.copy()
env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"

def upload_file(filename):
    local_path = os.path.join(tmp_dir, filename)
    r2_key = f"posts/{slug}/{filename}"
    print(f"Uploading {filename} to {bucket}/{r2_key}...")
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
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"[-] Failed to upload {filename}!")
        print(result.stderr)
        sys.exit(1)

for f in processed_carousel + processed_inline:
    upload_file(f)

# Clean up local temp directory
import shutil
shutil.rmtree(tmp_dir)
print("[+] All uploads completed and local temp files cleaned.")

# 4. Codebase registration
# 4a. Update fb-status.json
fb_status_path = os.path.join(project_root, "src", "data", "fb-status.json")
with open(fb_status_path, "r", encoding="utf-8") as f:
    fb_status = json.load(f)

if slug not in fb_status:
    new_fb = {slug: False}
    for k, v in fb_status.items():
        new_fb[k] = v
    with open(fb_status_path, "w", encoding="utf-8") as f:
        json.dump(new_fb, f, indent=2, ensure_ascii=False)
    print("[+] Registered in fb-status.json")

# 4b. Update series.ts
series_path = os.path.join(project_root, "src", "data", "series.ts")
with open(series_path, "r", encoding="utf-8") as f:
    series_content = f.read()

target_step_str = '{ slug: "how-would-you-remember-fruits-of-four-seasons", title: "第一篇 ｜ 四季的水果，你會怎麼記", label: "1" }'
new_step_str = target_step_str + ',\n      { slug: "how-to-actually-use-memory-science", title: "第二篇 ｜ 記憶學到底怎麼用——一個同事的四次試錯", label: "2" }'

if slug not in series_content:
    series_content = series_content.replace(target_step_str, new_step_str)
    with open(series_path, "w", encoding="utf-8") as f:
        f.write(series_content)
    print("[+] Registered in series.ts")

# 4c. Update posts.ts
posts_path = os.path.join(project_root, "src", "data", "posts.ts")
with open(posts_path, "r", encoding="utf-8") as f:
    posts_content = f.read()

if slug not in posts_content:
    camel_var = "howToActuallyUseMemoryScience"
    import_line = f'import {camel_var}Html from "../article-html/posts/{slug}.html?raw";'
    graphics_block = f"""const {camel_var}GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}";

const {camel_var}Graphics = Array.from({{ length: {len(processed_carousel)} }}, (_, index) => {{
  const page = index + 1;
  return {{
    src: `${{{camel_var}GraphicBase}}/graphic-${{String(page).padStart(2, "0")}}.webp`,
    alt: `四季的水果，你會怎麼記圖文解析 ${{page}}/{len(processed_carousel)}`
  }};
}});

"""
    post_object = f"""  {{
    title: "{title}",
    slug: "{slug}",
    date: "{date_str}",
    kicker: "{kicker}",
    excerpt:
      "{excerpt}",
    categories: ["memory-science-app", "parents", "core"],
    coverImage: {camel_var}Graphics[0].src,
    coverAlt: {camel_var}Graphics[0].alt,
    gallery: {{
      label: "<圖文解析>",
      images: {camel_var}Graphics
    }},
    relatedPosts: ["how-would-you-remember-fruits-of-four-seasons", "memory-science-is-misunderstood-p9", "memory-science-is-misunderstood-p8"],
    body: {camel_var}Html
  }},

"""
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
    
    # Add bidirectional links in relatedPosts
    related_slugs = ["how-would-you-remember-fruits-of-four-seasons", "memory-science-is-misunderstood-p9", "memory-science-is-misunderstood-p8"]
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
    print("[+] Registered in posts.ts with bidirectional links")

# 5. Rebuild and Deploy
print("[*] Rebuilding project...")
build_cmd = ["npm.cmd", "run", "build"] if os.name == "nt" else ["npm", "run", "build"]
result = subprocess.run(build_cmd, capture_output=True, text=True, encoding="utf-8")
if result.returncode != 0:
    print("[-] Build failed!")
    print(result.stderr)
    sys.exit(1)
print("[+] Project built and sitemap regenerated.")

# Bump DEPLOY_VERSION
proxy_path = os.path.join(project_root, "cloudflare", "worker-proxy.js")
with open(proxy_path, "r", encoding="utf-8") as f:
    proxy_content = f.read()
    
now_str = datetime.now().strftime("v_%Y_%m_%d_%H_%M")
pattern = re.compile(r'const DEPLOY_VERSION = "v_.*?";')
proxy_content = pattern.sub(f'const DEPLOY_VERSION = "{now_str}";', proxy_content)

with open(proxy_path, "w", encoding="utf-8") as f:
    f.write(proxy_content)
print(f"[+] Cleaned cache via DEPLOY_VERSION = {now_str}")

# Deploy wrangler
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
subprocess.run(["git", "commit", "-m", f"feat: publish how-to-actually-use-memory-science and deploy {now_str}"])
subprocess.run(["git", "push", "origin", "main"])
print("[+] Code pushed to GitHub repository.")
print(f"[+] SUCCESS! Article is live at: https://kc-ai-education-blog.ji3cp31p4.workers.dev/posts/{slug}/")
