import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_FOLDER = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"

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
    folder_path = os.path.join(BASE_FOLDER, matched[0])
    html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    filepath = os.path.join(folder_path, html_files[0])
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    start_line = None
    for idx, line in enumerate(lines, 1):
        if "<div style=\"max-width:600px" in line or "<section style=\"max-width:600px" in line:
            start_line = idx
            break
            
    end_line = None
    for idx in range(len(lines), 0, -1):
        line = lines[idx-1].strip().lower()
        if line.endswith("</section>") or line.endswith("</div>"):
            end_line = idx
            break
            
    print(f"{item['slug']}: start={start_line}, end={end_line}, last_line='{lines[end_line-1].strip()}'")
