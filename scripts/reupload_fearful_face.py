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

ARTICLE = {
    "folder": os.path.join(BASE_FOLDER, "20260911最傷孩子的，可能不是你沒教他保護自己，而是你教保護時那張恐懼的臉"),
    "slug": "fearful-face-in-protection-education",
    "title": "最傷孩子的，可能不是你沒教他保護自己，而是你教保護時那張恐懼的臉",
}

def main():
    print(f"\n==========================================")
    print(f" Re-processing Images: {ARTICLE['slug']}")
    print(f"==========================================")
    
    img_count, temp_dir = publish_helper.process_images(
        src_dir=ARTICLE['folder'],
        slug=ARTICLE['slug'],
        project_root=PROJECT_ROOT
    )
    
    print(f"[+] Total images processed: {img_count}")
    if img_count > 0:
        publish_helper.upload_to_r2(
            temp_img_dir=temp_dir,
            slug=ARTICLE['slug'],
            images_count=img_count
        )

    # Update DEPLOY_VERSION in cloudflare/worker-proxy.js
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
