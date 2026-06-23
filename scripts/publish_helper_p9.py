import os
import re
import sys
import json
import subprocess
from PIL import Image

src_dir = r"C:\Users\ji3cp\OneDrive\Documents\40_AI_folder\PO文網站\file\20260623記憶學被冤枉·第九篇——拆字進階：核心觀點與更多範例-1"
project_root = r"C:\Users\ji3cp\OneDrive\Documents\40_AI_folder\PO文網站"
slug = "memory-science-is-misunderstood-p9"

tmp_dir = os.path.join(project_root, "tmp", slug)
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# 1. Parse and extract HTML, replacing placeholders
html_path = os.path.join(src_dir, "記憶學被冤枉·第九篇——拆字進階：核心觀點與更多範例-1.html")
with open(html_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract inner HTML (lines 9 to 319, 1-based index)
# lines[8:319]
inner_html = "".join(lines[8:319])

card_mapping = [
    (96, "意"), (97, "拉"), (98, "粒"), (99, "里"), (100, "童"),
    (101, "占"), (102, "站"), (103, "位"), (104, "民"), (105, "眠"),
    (106, "分"), (107, "盼"), (108, "公"), (109, "少"), (110, "其"),
    (111, "省"), (112, "期"), (113, "也"), (114, "地"), (115, "他"),
    (116, "它"), (117, "蛇"), (118, "享"), (119, "受"), (120, "亡")
]

for num, char in card_mapping:
    char_esc = re.escape(char)
    pattern = rf'<section style="background-color:rgba\(192,81,47,0\.06\);padding:36px 20px;margin:0 0 (?:14|20)px 0;text-align:center;">\s*<p[^>]*>\[\s*圖卡：{num}\s+{char_esc}\s*\]</p>\s*</section>'
    
    img_tag = f"""<!-- 象形字圖卡：{char} -->
<div style="margin:24px auto;max-width:360px;text-align:center;">
  <img src="https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}/card-{num:02d}.webp" alt="象形字圖卡：{char}" style="width:100%;height:auto;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.08);border:1px solid rgba(192,81,47,0.15);" />
</div>"""
    
    inner_html, count = re.subn(pattern, img_tag, inner_html)
    print(f"Replaced placeholder [ 圖卡：{num} {char} ] -> card-{num:02d}.webp ({count} match)")

# Save the updated inner HTML
dest_html_path = os.path.join(project_root, "src", "article-html", "posts", f"{slug}.html")
os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)
with open(dest_html_path, "w", encoding="utf-8") as f:
    f.write(inner_html)
print(f"[+] Saved extracted HTML to {dest_html_path}")

# 2. Process and optimize images
# 2a. Carousel images (graphic-XX.webp)
carousel_files = []
for f in os.listdir(src_dir):
    if f.startswith("ChatGPT Image") and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        # Extract number: (1) to (10)
        match = re.search(r"\((\d+)\)\.(?:png|jpg|jpeg|webp)$", f)
        if match:
            num = int(match.group(1))
            carousel_files.append((num, f))
carousel_files.sort()

print("[+] Sorted Carousel images:")
for num, f in carousel_files:
    print(f"  {num}: {f}")

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
    print(f"Processed: {f} -> {new_name}")
    processed_carousel.append(new_name)

# 2b. Card images (card-XX.webp)
card_files = []
for f in os.listdir(src_dir):
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) and not f.startswith("ChatGPT Image"):
        # Match number prefix: "96_意.png"
        match = re.match(r"^(\d+)_", f)
        if match:
            num = int(match.group(1))
            card_files.append((num, f))
card_files.sort()

print("[+] Sorted Card images:")
for num, f in card_files:
    print(f"  {num}: {f}")

processed_cards = []
for num, f in card_files:
    new_name = f"card-{num:02d}.webp"
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
    print(f"Processed: {f} -> {new_name}")
    processed_cards.append(new_name)

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

for f in processed_carousel + processed_cards:
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

target_p8_str = '{ slug: "memory-science-is-misunderstood-p8", title: "第八篇 ｜ 拆字實戰：二十幾個字，帶你走一遍", label: "8" }'
new_p9_str = target_p8_str + ',\n      { slug: "memory-science-is-misunderstood-p9", title: "第九篇 ｜ 拆字進階：核心觀點與更多範例", label: "9" }'

if slug not in series_content:
    series_content = series_content.replace(target_p8_str, new_p9_str)
    with open(series_path, "w", encoding="utf-8") as f:
        f.write(series_content)
    print("[+] Registered in series.ts")

# 4c. Update posts.ts
posts_path = os.path.join(project_root, "src", "data", "posts.ts")
with open(posts_path, "r", encoding="utf-8") as f:
    posts_content = f.read()

if slug not in posts_content:
    # 1. Add import line
    import_line = f'import memoryScienceIsMisunderstoodP9Html from "../article-html/posts/{slug}.html?raw";'
    lines = posts_content.splitlines()
    last_import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("import ") and "?raw" in line:
            last_import_idx = i
    lines.insert(last_import_idx + 1, import_line)
    posts_content_temp = "\n".join(lines)

    # 2. Add graphics block & post object
    graphics_block = f"""const memoryScienceIsMisunderstoodP9GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}";

const memoryScienceIsMisunderstoodP9Graphics = Array.from({{ length: 10 }}, (_, index) => {{
  const page = index + 1;
  return {{
    src: `${{memoryScienceIsMisunderstoodP9GraphicBase}}/graphic-${{String(page).padStart(2, "0")}}.webp`,
    alt: `記憶學被冤枉·第九篇——拆字進階：核心觀點與更多範例圖文解析 ${{page}}/10`
  }};
}});\n\n"""

    related_slugs = ["memory-science-is-misunderstood-p8", "memory-science-is-misunderstood-p7", "memory-science-is-misunderstood-p6", "how-to-train-memory-since-childhood"]
    related_str = "[" + ", ".join(f'"{s}"' for s in related_slugs) + "]"

    post_object = f"""  {{
    title: "記憶學被冤枉·第九篇——拆字進階：核心觀點與更多範例",
    slug: "{slug}",
    date: "2026-06-23",
    kicker: "記憶學 · 第九篇",
    excerpt:
      "上一篇，我們開始拆字了。二十幾字走一遍，你大概有了手感。但你可能遇到了幾個問題：孩子記不住、拆出來的部件孩子聽不懂、孩子自己想了一個你覺得不合理的拆法——到底該聽誰的？這篇，我要把底層邏輯講清楚。",
    categories: ["memory-science", "parents", "core"],
    coverImage: memoryScienceIsMisunderstoodP9Graphics[0].src,
    coverAlt: memoryScienceIsMisunderstoodP9Graphics[0].alt,
    gallery: {{
      label: "<圖文解析>",
      images: memoryScienceIsMisunderstoodP9Graphics
    }},
    relatedPosts: {related_str},
    body: memoryScienceIsMisunderstoodP9Html
  }},

"""

    posts_content_temp = posts_content_temp.replace(
        "export const posts = [",
        graphics_block + "export const posts = [\n" + post_object
    )

    # 3. Establish bidirectional related links
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
    print("[+] Registered in posts.ts with bidirectional links.")
else:
    print("[*] Already registered in posts.ts")

print("\n[+] SUCCESS! Automated script completed.")
