import os
import sys
import re
import datetime
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_FOLDER = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARTICLES_11 = [
    {"slug": "same-ai-command-vs-looping", "folder_pattern": "20260905同一個AI", "start": 9, "end": 217},
    {"slug": "city-walk-kids-building-capabilities", "folder_pattern": "20260905城市健走", "start": 9, "end": 134},
    {"slug": "interest-and-habits-are-results-not-starts", "folder_pattern": "20260905興趣和習慣", "start": 9, "end": 197},
    {"slug": "fearful-face-in-protection-education", "folder_pattern": "20260911最傷孩子的", "start": 9, "end": 169},
    {"slug": "using-ai-thinking-partner-not-alone", "folder_pattern": "20260913我開始用", "start": 9, "end": 547},
    {"slug": "reading-flow-state-versus-proof-of-learning", "folder_pattern": "20260913孩子明明讀到", "start": 9, "end": 498},
    {"slug": "letting-kids-experience-consequences-without-cruelty", "folder_pattern": "20260913我差點讓", "start": 9, "end": 380},
    {"slug": "when-kids-say-boring-cut-easy-content", "folder_pattern": "20260913孩子一直喊", "start": 9, "end": 385},
    {"slug": "stop-reminding-kids-building-real-self-discipline", "folder_pattern": "20260913我不再提醒", "start": 9, "end": 408},
    {"slug": "sighing-shaking-head-emotional-separation-for-kids", "folder_pattern": "20260913孩子一被提醒", "start": 9, "end": 548},
    {"slug": "giving-freedom-with-clear-non-negotiable-boundaries", "folder_pattern": "20260913我給孩子很大的自由", "start": 9, "end": 284},
]

def restore_html():
    print("[*] Restoring all 11 articles HTML fragments (including signature blocks & max-width:600px)...")
    for item in ARTICLES_11:
        matched = [d for d in os.listdir(BASE_FOLDER) if item['folder_pattern'] in d]
        if not matched:
            print(f"[-] Missing folder for {item['slug']}")
            continue
        folder_path = os.path.join(BASE_FOLDER, matched[0])
        html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
        if not html_files:
            print(f"[-] Missing HTML file in {folder_path}")
            continue
        
        filepath = os.path.join(folder_path, html_files[0])
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        inner_html = "".join(lines[item['start'] - 1 : item['end']])
        
        dest_path = os.path.join(PROJECT_ROOT, "src", "article-html", "posts", f"{item['slug']}.html")
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(inner_html)
            
        print(f"[+] Restored {item['slug']} ({len(lines[item['start'] - 1 : item['end']])} lines)")

    # Update DEPLOY_VERSION
    worker_js_path = os.path.join(PROJECT_ROOT, "cloudflare", "worker-proxy.js")
    with open(worker_js_path, "r", encoding="utf-8") as f:
        worker_code = f.read()

    now_str = datetime.datetime.now().strftime("v_%Y_%m_%d_%H_%M_%S")
    worker_code = re.sub(r'const DEPLOY_VERSION = "[^"]+";', f'const DEPLOY_VERSION = "{now_str}";', worker_code)
    with open(worker_js_path, "w", encoding="utf-8") as f:
        f.write(worker_code)
    print(f"[+] Updated DEPLOY_VERSION to {now_str}")

if __name__ == "__main__":
    restore_html()
