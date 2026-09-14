import os
import sys
import re
import datetime
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publish_helper

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_FOLDER = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODIFIED_ARTICLES = [
    {
        "folder": os.path.join(BASE_FOLDER, "20260913孩子一直喊「好無聊」，我反而把有趣的教材砍掉了"),
        "slug": "when-kids-say-boring-cut-easy-content",
        "title": "孩子一直喊「好無聊」，我反而把有趣的教材砍掉了",
        "camel": "WhenKidsSayBoringCutEasyContent"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913我不再提醒孩子了，因為我終於發現：我一直在替她「自律」"),
        "slug": "stop-reminding-kids-building-real-self-discipline",
        "title": "我不再提醒孩子了，因為我終於發現：我一直在替她「自律」",
        "camel": "StopRemindingKidsBuildingRealSelfDiscipline"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913我差點讓孩子熬夜到崩潰，只為了讓她「記住教訓」"),
        "slug": "letting-kids-experience-consequences-without-cruelty",
        "title": "我差點讓孩子熬夜到崩潰，只為了讓她「記住教訓」",
        "camel": "LettingKidsExperienceConsequencesWithoutCruelty"
    }
]

def main():
    # 1. Process and upload images for each modified article
    for idx, art in enumerate(MODIFIED_ARTICLES, 1):
        print(f"\n==========================================")
        print(f" Processing Article {idx}/3: {art['slug']}")
        print(f"==========================================")
        
        img_count, temp_dir = publish_helper.process_images(
            src_dir=art['folder'],
            slug=art['slug'],
            project_root=PROJECT_ROOT
        )
        
        print(f"[+] Total images processed: {img_count}")
        if img_count > 0:
            publish_helper.upload_to_r2(
                temp_img_dir=temp_dir,
                slug=art['slug'],
                images_count=img_count
            )
            
        art['img_count'] = img_count

    # 2. Update src/data/posts.ts
    posts_ts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update stopRemindingKidsBuildingRealSelfDisciplineGraphics length to 10
    content = re.sub(
        r'const stopRemindingKidsBuildingRealSelfDisciplineGraphics = Array\.from\(\{\s*length:\s*\d+\s*\}',
        f'const stopRemindingKidsBuildingRealSelfDisciplineGraphics = Array.from({{ length: {MODIFIED_ARTICLES[1]["img_count"]} }}',
        content
    )
    # Update alt text count
    content = re.sub(
        r'alt: `我不再提醒孩子了，因為我終於發現：我一直在替她「自律」圖文解析 \$\{page\}/\d+`',
        f'alt: `我不再提醒孩子了，因為我終於發現：我一直在替她「自律」圖文解析 ${{page}}/{MODIFIED_ARTICLES[1]["img_count"]}`',
        content
    )

    # Update lettingKidsExperienceConsequencesWithoutCrueltyGraphics length to 10
    content = re.sub(
        r'const lettingKidsExperienceConsequencesWithoutCrueltyGraphics = Array\.from\(\{\s*length:\s*\d+\s*\}',
        f'const lettingKidsExperienceConsequencesWithoutCrueltyGraphics = Array.from({{ length: {MODIFIED_ARTICLES[2]["img_count"]} }}',
        content
    )
    # Update alt text count
    content = re.sub(
        r'alt: `我差點讓孩子熬夜到崩潰，只為了讓她「記住教訓」圖文解析 \$\{page\}/\d+`',
        f'alt: `我差點讓孩子熬夜到崩潰，只為了讓她「記住教訓」圖文解析 ${{page}}/{MODIFIED_ARTICLES[2]["img_count"]}`',
        content
    )

    # For whenKidsSayBoringCutEasyContent: check if graphic base already defined
    if "whenKidsSayBoringCutEasyContentGraphicBase" not in content:
        boring_graphics_decl = (
            f'const whenKidsSayBoringCutEasyContentGraphicBase =\n'
            f'  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/when-kids-say-boring-cut-easy-content";\n\n'
            f'const whenKidsSayBoringCutEasyContentGraphics = Array.from({{ length: {MODIFIED_ARTICLES[0]["img_count"]} }}, (_, index) => {{\n'
            f'  const page = index + 1;\n'
            f'  return {{\n'
            f'    src: `${{whenKidsSayBoringCutEasyContentGraphicBase}}/graphic-${{String(page).padStart(2, "0")}}.webp`,\n'
            f'    alt: `孩子一直喊「好無聊」，我反而把有趣的教材砍掉了圖文解析 ${{page}}/{MODIFIED_ARTICLES[0]["img_count"]}`\n'
            f'  }};\n'
            f'}});\n\n'
        )
        content = content.replace("export const posts = [", boring_graphics_decl + "export const posts = [")

    # In whenKidsSayBoringCutEasyContent post object: add coverImage, coverAlt, gallery
    target_post_pattern = re.compile(
        r'(slug:\s*"when-kids-say-boring-cut-easy-content",[\s\S]*?categories:\s*\["parents",\s*"core"\],)'
    )
    replacement_fields = (
        r'\1\n'
        r'    coverImage: whenKidsSayBoringCutEasyContentGraphics[0].src,\n'
        r'    coverAlt: whenKidsSayBoringCutEasyContentGraphics[0].alt,\n'
        r'    gallery: {\n'
        r'      label: "<圖文解析>",\n'
        r'      images: whenKidsSayBoringCutEasyContentGraphics\n'
        r'    },'
    )
    if "coverImage: whenKidsSayBoringCutEasyContentGraphics[0].src" not in content:
        content = target_post_pattern.sub(replacement_fields, content, count=1)

    with open(posts_ts_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[+] Successfully updated src/data/posts.ts")

    # 3. Update DEPLOY_VERSION in cloudflare/worker-proxy.js
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
