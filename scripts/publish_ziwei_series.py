import os
import sys
import re
import shutil
import subprocess
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

src_root = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
project_root = r"C:\Users\ji3cp\Documents\antigravity\kc-ai-education-blog"

articles = [
    {
        "folder": "20260710紫微+AI育兒系列（一）：弔胃口-1",
        "slug": "ziwei-ai-parenting-p1",
        "title": "紫微+AI育兒系列（一）：弔胃口",
        "kicker": "紫微+AI育兒系列 · 第一篇"
    },
    {
        "folder": "20260710紫微+AI育兒系列（二）：運動七型-1",
        "slug": "ziwei-ai-parenting-p2",
        "title": "紫微+AI育兒系列（二）：運動七型",
        "kicker": "紫微+AI育兒系列 · 第二篇"
    },
    {
        "folder": "20260710紫微+AI育兒系列（三）：愛漂亮五型-1",
        "slug": "ziwei-ai-parenting-p3",
        "title": "紫微+AI育兒系列（三）：愛漂亮五型",
        "kicker": "紫微+AI育兒系列 · 第三篇"
    },
    {
        "folder": "20260710紫微+AI育兒系列（四上）：當命盤看見閱讀障礙-1",
        "slug": "ziwei-ai-parenting-p4a",
        "title": "紫微+AI育兒系列（四上）：當命盤看見閱讀障礙",
        "kicker": "紫微+AI育兒系列 · 第四篇（上）"
    },
    {
        "folder": "20260710紫微+AI育兒系列（四下）：閱讀障礙的破解路徑-1",
        "slug": "ziwei-ai-parenting-p4b",
        "title": "紫微+AI育兒系列（四下）：閱讀障礙的破解路徑",
        "kicker": "紫微+AI育兒系列 · 第四篇（下）"
    }
]

# 1. Parse and extract HTML for each article
def extract_html(folder_name, slug):
    folder_path = os.path.join(src_root, folder_name)
    html_file = None
    for f in os.listdir(folder_path):
        if f.endswith(".html"):
            html_file = os.path.join(folder_path, f)
            break
            
    if not html_file:
        print(f"[-] Error: No HTML file in {folder_path}")
        return
        
    with open(html_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Find the start line containing max-width:600px or fallback to line 9 (0-indexed 8)
    start_idx = 8
    for idx, line in enumerate(lines):
        if 'max-width:600px' in line:
            start_idx = idx
            break
            
    # Find the end line by scanning backwards for the last </section> before </body>
    end_idx = len(lines) - 2
    for idx in range(len(lines) - 1, -1, -1):
        if '</section>' in lines[idx]:
            end_idx = idx
            break
            
    inner_html = "".join(lines[start_idx : end_idx + 1])
    
    dest_path = os.path.join(project_root, "src", "article-html", "posts", f"{slug}.html")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(inner_html)
    print(f"[+] Extracted HTML for {slug} to {dest_path} (Lines {start_idx+1} to {end_idx+1})")

for art in articles:
    extract_html(art["folder"], art["slug"])

# 2. Group and route images correctly
# Image routing maps to handle the misplaced Part 4a image in the Part 4b folder
image_groups = {
    "ziwei-ai-parenting-p1": [],
    "ziwei-ai-parenting-p2": [],
    "ziwei-ai-parenting-p3": [],
    "ziwei-ai-parenting-p4a": [],
    "ziwei-ai-parenting-p4b": []
}

# Scan folders and populate image_groups
for art in articles:
    folder_path = os.path.join(src_root, art["folder"])
    for f in os.listdir(folder_path):
        if f.startswith("ChatGPT Image") and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            full_path = os.path.join(folder_path, f)
            
            # Special routing for Part 4a / 4b based on timestamp
            if "下午06_22_56" in f:
                image_groups["ziwei-ai-parenting-p4a"].append(full_path)
            elif "下午06_35_2" in f:
                image_groups["ziwei-ai-parenting-p4b"].append(full_path)
            else:
                image_groups[art["slug"]].append(full_path)

# Sort key helper
def sort_key(filepath):
    filename = os.path.basename(filepath)
    ampm = 1 if "下午" in filename else 0
    # Match standard ChatGPT timestamp pattern: "上午10_35_56 (1).png"
    match = re.search(r"(?:上午|下午)(\d+)_(\d+)_(\d+)\s*\((\d+)\)\.(?:png|jpg|jpeg|webp)$", filename)
    if match:
        h, m, s, num = map(int, match.groups())
        return (ampm, h, m, s, num)
    
    match_num = re.search(r"\((\d+)\)\.(?:png|jpg|jpeg|webp)$", filename)
    if match_num:
        return (0, 0, 0, 0, int(match_num.group(1)))
        
    return (0, 0, 0, 0, filename)

# Process and optimize images for each group
bucket = "kc-ai-education-blog-assets"
env = os.environ.copy()
env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"

for slug, paths in image_groups.items():
    sorted_paths = sorted(paths, key=sort_key)
    print(f"\n[+] Sorted images for {slug} (Count: {len(sorted_paths)}):")
    for idx, path in enumerate(sorted_paths, 1):
        print(f"  {idx:02d}: {os.path.basename(path)}")
        
    temp_dir = os.path.join(project_root, "tmp", slug)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Process
    for idx, path in enumerate(sorted_paths, 1):
        new_name = f"graphic-{idx:02d}.webp"
        dest_path = os.path.join(temp_dir, new_name)
        
        with Image.open(path) as img:
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
        print(f"  Optimized: {os.path.basename(path)} -> {new_name}")
        
        # Upload to R2
        r2_key = f"posts/{slug}/{new_name}"
        print(f"  Uploading {new_name} to R2 bucket...")
        cmd = [
            "npx.cmd" if os.name == "nt" else "npx",
            "wrangler",
            "r2",
            "object",
            "put",
            f"{bucket}/{r2_key}",
            "--file",
            dest_path,
            "--remote"
        ]
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            print(f"  [-] Failed to upload {new_name}!")
            print(result.stderr)
            sys.exit(1)

print("\n[+] All HTML extraction and R2 image uploads completed successfully!")
