import os
import re
import sys
import subprocess
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

src_dir = r"C:\Users\ji3cp\Downloads\20260620記憶學被冤枉·第六篇——象形字圖卡（二）：人物姿態與動物飛禽-1"
project_root = r"C:\Users\ji3cp\Documents\antigravity\kc-ai-education-blog"
slug = "memory-science-is-misunderstood-p6"

tmp_dir = os.path.join(project_root, "tmp", slug)
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# 1. Parse and extract HTML, replacing placeholders
html_path = os.path.join(src_dir, "記憶學被冤枉·第六篇——象形字圖卡（二）：人物姿態與動物飛禽-1.html")
with open(html_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract inner HTML (lines 9 to 223, 1-based index)
# lines[8:223]
inner_html = "".join(lines[8:223])

# Placeholder replacement map (starts at index 24)
card_mapping = [
    "人", "女", "大", "子", "交", "長",
    "馬", "牛", "羊", "鳥", "魚", "虫", "犬", "豕", "虎", "象", "鹿", "龜", "燕", "兔", "羽"
]

for idx, char in enumerate(card_mapping, 24):
    # Regex to match the placeholder section
    pattern = rf'<section style="background-color:rgba\(192,81,47,0\.06\);padding:40px 20px;margin:0 0 (?:16|24)px 0;text-align:center;">\s*<p[^>]*>\[\s*圖卡：{char}\s*\]</p>\s*</section>'
    
    img_tag = f"""<!-- 象形字圖卡：{char} -->
<div style="margin:24px auto;max-width:360px;text-align:center;">
  <img src="https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}/card-{idx:02d}.webp" alt="象形字圖卡：{char}" style="width:100%;height:auto;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.08);border:1px solid rgba(192,81,47,0.15);" />
</div>"""
    
    inner_html, count = re.subn(pattern, img_tag, inner_html)
    print(f"Replaced placeholder [ 圖卡：{char} ] -> card-{idx:02d}.webp ({count} match)")

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
        # Extract number: (1) to (8)
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
        # Match number prefix: "24_人_圖卡.png"
        match = re.match(r"^(\d+)_", f)
        if match:
            num = int(match.group(1))
            card_files.append((num, f))
card_files.sort()

print("[+] Sorted Card images:")
for num, f in card_files:
    print(f"  {num}: {f}")

processed_cards = []
for idx, (num, f) in enumerate(card_files, 24):
    new_name = f"card-{idx:02d}.webp"
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

print("[+] All uploads completed successfully!")
