import os
import sys
import re
import argparse
import subprocess
import shutil
from PIL import Image

def get_args():
    parser = argparse.ArgumentParser(description="KC AI Education Blog - Article Publishing Helper")
    parser.add_argument("--src", required=True, help="Path to source folder containing HTML and images")
    parser.add_argument("--slug", required=True, help="Slug for the article (e.g., no-punishment-is-hard)")
    parser.add_argument("--excerpt", required=True, help="1-2 sentences of article summary for SEO & feed")
    parser.add_argument("--title", help="Article title (optional, falls back to HTML parsing)")
    parser.add_argument("--kicker", default="KC 育兒手記", help="Article kicker category (default: KC 育兒手記)")
    parser.add_argument("--categories", default="parents,core", help="Comma-separated category IDs (default: parents,core)")
    parser.add_argument("--start-line", type=int, default=9, help="1-based start line of the article inner HTML (default: 9)")
    parser.add_argument("--end-line", type=int, default=331, help="1-based end line of the article inner HTML (default: 331)")
    return parser.parse_args()

def extract_html(src_dir, slug, start_line, end_line, project_root):
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
        
    # Extract line range (1-based to 0-based index)
    # lines[start-1:end] will contain lines from start to end inclusive.
    inner_html = "".join(lines[start_line - 1 : end_line])
    
    dest_path = os.path.join(project_root, "src", "article-html", "posts", f"{slug}.html")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(inner_html)
    
    print(f"[+] Extracted HTML fragment to {dest_path}")
    
    # Extract title from HTML if not provided
    extracted_title = ""
    for line in lines:
        match = re.search(r"<title>(.*?)</title>", line)
        if match:
            extracted_title = match.group(1).strip()
            break
    return extracted_title

def sort_key(filename):
    # Sort by AM/PM, Hour, Minute, Second, and parenthesized number
    ampm = 1 if "下午" in filename else 0
    # Match standard ChatGPT timestamp pattern: "上午10_00_29 (1).png"
    match = re.search(r"(?:上午|下午)(\d+)_(\d+)_(\d+)\s*\((\d+)\)\.(?:png|jpg|jpeg|webp)$", filename)
    if match:
        h, m, s, num = map(int, match.groups())
        return (ampm, h, m, s, num)
    
    # Fallback to parenthesized number at the end
    match_num = re.search(r"\((\d+)\)\.(?:png|jpg|jpeg|webp)$", filename)
    if match_num:
        return (0, 0, 0, 0, int(match_num.group(1)))
        
    # Full fallback to string sorting
    return (0, 0, 0, 0, filename)

def process_images(src_dir, slug, project_root):
    img_extensions = (".png", ".jpg", ".jpeg", ".webp")
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(img_extensions)]
    
    if not files:
        print("[-] Warning: No images found in source folder.")
        return 0, []
        
    sorted_files = sorted(files, key=sort_key)
    print("[+] Chronologically and numerically sorted images:")
    for idx, file in enumerate(sorted_files, 1):
        print(f"  {idx:02d}: {file}")
        
    temp_img_dir = os.path.join(project_root, "tmp", slug)
    os.makedirs(temp_img_dir, exist_ok=True)
    
    optimized_files = []
    for idx, file in enumerate(sorted_files, 1):
        new_name = f"graphic-{idx:02d}.webp"
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(temp_img_dir, new_name)
        
        with Image.open(src_path) as img:
            w, h = img.size
            max_size = 1600
            # Resize if necessary
            if w > max_size or h > max_size:
                if w > h:
                    new_w = max_size
                    new_h = int(h * max_size / w)
                else:
                    new_h = max_size
                    new_w = int(w * max_size / h)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Save WebP with 75% quality. Metadata is stripped by Pillow by default unless keep_metadata is set.
            img.save(dest_path, "WEBP", quality=75)
            
        print(f"[+] Processed & Optimized: {file} -> {new_name}")
        optimized_files.append(new_name)
        
    return len(optimized_files), temp_img_dir

def upload_to_r2(temp_img_dir, slug, images_count):
    if images_count == 0:
        return
        
    bucket = "kc-ai-education-blog-assets"
    env = os.environ.copy()
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"
    
    print(f"[*] Uploading {images_count} images to Cloudflare R2 bucket '{bucket}'...")
    
    for i in range(1, images_count + 1):
        filename = f"graphic-{i:02d}.webp"
        local_path = os.path.join(temp_img_dir, filename)
        r2_key = f"posts/{slug}/{filename}"
        
        print(f"  Uploading {filename} to posts/{slug}/...")
        
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
            print(f"  [-] Failed to upload {filename}!")
            print(result.stderr)
            sys.exit(1)
            
    print("[+] All images successfully uploaded to Cloudflare R2!")
    
    # Cleanup temp directory
    shutil.rmtree(temp_img_dir)
    print("[+] Cleaned up local temporary optimized images.")

def generate_code_templates(slug, title, kicker, excerpt, categories, images_count):
    # Format categories
    cat_list = [f'"{c.strip()}"' for c in categories.split(",")]
    cat_str = f"[{', '.join(cat_list)}]"
    
    import_camel = "".join(x.capitalize() for x in slug.split("-"))
    import_camel_lc = import_camel[0].lower() + import_camel[1:]
    
    print("\n" + "="*80)
    print("📋 CODE GENERATION TEMPLATES FOR posts.ts AND fb-status.json")
    print("="*80)
    
    print(f"\n1️⃣ STEP 1: Add this import at the top of 'src/data/posts.ts':")
    print(f'import {import_camel_lc}Html from "../article-html/posts/{slug}.html?raw";')
    
    print(f"\n2️⃣ STEP 2: Add this definition above the 'export const posts = [' array:")
    print(f'const {import_camel_lc}GraphicBase =')
    print(f'  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{slug}";')
    print()
    print(f'const {import_camel_lc}Graphics = Array.from({{ length: {images_count} }}, (_, index) => {{')
    print(f'  const page = index + 1;')
    print(f'  return {{')
    print(f'    src: `${{{import_camel_lc}GraphicBase}}/graphic-${{String(page).padStart(2, "0")}}.webp`,')
    print(f'    alt: `{title}圖文解析 ${{page}}/{images_count}`')
    print(f'  }};')
    print(f'}});')
    
    print(f"\n3️⃣ STEP 3: Insert this post object at the top of the 'posts' array:")
    print(f'  {{')
    print(f'    title: "{title}",')
    print(f'    slug: "{slug}",')
    print(f'    date: "{os.popen("date /t" if os.name == "nt" else "date +%Y-%m-%d").read().strip().replace("/", "-")}",')
    print(f'    kicker: "{kicker}",')
    print(f'    excerpt:')
    print(f'      "{excerpt}",')
    print(f'    categories: {cat_str},')
    print(f'    coverImage: {import_camel_lc}Graphics[0].src,')
    print(f'    coverAlt: {import_camel_lc}Graphics[0].alt,')
    print(f'    gallery: {{')
    print(f'      label: "<圖文解析>",')
    print(f'      images: {import_camel_lc}Graphics')
    print(f'    }},')
    print(f'    relatedPosts: [], // Add related slugs here (bidirectionally!)')
    print(f'    body: {import_camel_lc}Html')
    print(f'  }},')
    
    print(f"\n4️⃣ STEP 4: Insert this key-value into 'src/data/fb-status.json':")
    print(f'  "{slug}": false,')
    
    print("\n" + "="*80)

def main():
    args = get_args()
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print(f"[*] Project root identified as: {project_root}")
    
    # 1. HTML fragment extraction
    html_title = extract_html(args.src, args.slug, args.start_line, args.end_line, project_root)
    title = args.title if args.title else html_title
    
    # 2. Image resizing, optimization and webp conversion
    images_count, temp_img_dir = process_images(args.src, args.slug, project_root)
    
    # 3. Upload to Cloudflare R2
    upload_to_r2(temp_img_dir, args.slug, images_count)
    
    # 4. Generate configurations
    generate_code_templates(args.slug, title, args.kicker, args.excerpt, args.categories, images_count)
    
    print("\n[+] SUCCESS! Follow the templates above to register the post, then run:")
    print("    npm run build")
    print("    git add -A; git commit -m 'feat: publish post ...'; git push origin main")

if __name__ == "__main__":
    main()
