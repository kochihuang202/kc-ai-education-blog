import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_FOLDER = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARTICLES_11 = [
    {"slug": "same-ai-command-vs-looping", "folder_pattern": "20260905同一個AI"},
    {"slug": "city-walk-kids-building-capabilities", "folder_pattern": "20260905城市健走"},
    {"slug": "interest-and-habits-are-results-not-starts", "folder_pattern": "20260905興趣和習慣"},
    {"slug": "fearful-face-in-protection-education", "folder_pattern": "20260911最傷孩子的"},
    {"slug": "using-ai-thinking-partner-not-alone", "folder_pattern": "20260913我開始用"},
    {"slug": "reading-flow-state-versus-proof-of-learning", "folder_pattern": "20260913孩子明明讀到"},
    {"slug": "letting-kids-experience-consequences-without-cruelty", "folder_pattern": "20260913我差點讓"},
    {"slug": "when-kids-say-boring-cut-easy-content", "folder_pattern": "20260913孩子一直喊"},
    {"slug": "stop-reminding-kids-building-real-self-discipline", "folder_pattern": "20260913我不再提醒"},
    {"slug": "sighing-shaking-head-emotional-separation-for-kids", "folder_pattern": "20260913孩子一被提醒"},
    {"slug": "giving-freedom-with-clear-non-negotiable-boundaries", "folder_pattern": "20260913我給孩子很大的自由"},
]

for item in ARTICLES_11:
    matched = [d for d in os.listdir(BASE_FOLDER) if item['folder_pattern'] in d]
    if not matched:
        print(f"[-] No folder for pattern: {item['folder_pattern']}")
        continue
    folder_path = os.path.join(BASE_FOLDER, matched[0])
    html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    if not html_files:
        print(f"[-] No HTML in: {folder_path}")
        continue
    filepath = os.path.join(folder_path, html_files[0])
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    
    # Find line with max-width:600px
    start_line = 1
    for idx, line in enumerate(lines, 1):
        if "max-width" in line:
            start_line = idx
            break
            
    # Find last line before </body> or </html>
    end_line = len(lines)
    for idx in range(len(lines), 0, -1):
        line = lines[idx-1].strip()
        if "</div>" in line:
            end_line = idx
            break
            
    print(f"[+] {item['slug']}: lines {start_line} to {end_line} (Total {len(lines)}) | file: {html_files[0]}")
    print(f"    Line {start_line}: {lines[start_line-1].strip()[:60]}")
    print(f"    Line {end_line}: {lines[end_line-1].strip()[:60]}")
