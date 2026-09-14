import os
import sys
import datetime
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_FOLDER = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read posts.ts to see previous length for each slug
posts_ts = open(os.path.join(PROJECT_ROOT, "src", "data", "posts.ts"), encoding="utf-8").read()

folders = [d for d in sorted(os.listdir(BASE_FOLDER)) if os.path.isdir(os.path.join(BASE_FOLDER, d)) and "20260913" in d]

print(f"{'資料夾名稱':<45} | {'目前圖數':<8} | {'先前上傳數':<10} | {'變動狀態'}")
print("-" * 95)

for d in folders:
    fpath = os.path.join(BASE_FOLDER, d)
    imgs = [f for f in os.listdir(fpath) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    # Check modification times
    has_today = any(datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(fpath, f))).strftime('%Y-%m-%d') == '2026-09-14' for f in imgs)
    
    # Guess previous count from posts.ts
    # Let's find slug or Graphics length in posts.ts
    prev_count = "無"
    if "孩子一直喊" in d:
        slug = "when-kids-say-boring-cut-easy-content"
    elif "自律" in d:
        slug = "stop-reminding-kids-building-real-self-discipline"
    elif "熬夜" in d:
        slug = "letting-kids-experience-consequences-without-cruelty"
    elif "嘆氣" in d:
        slug = "sighing-shaking-head-emotional-separation-for-kids"
    elif "閱讀紀錄" in d:
        slug = "reading-flow-state-versus-proof-of-learning"
    elif "不再只跟自己想" in d:
        slug = "using-ai-thinking-partner-not-alone"
    elif "很大的自由" in d:
        slug = "giving-freedom-with-clear-non-negotiable-boundaries"
    else:
        slug = ""

    match = re.search(r'length:\s*(\d+)\s*\}\s*,\s*\(_, index\)', posts_ts[posts_ts.find(slug):posts_ts.find(slug)+400] if slug and posts_ts.find(slug) != -1 else "")
    # Actually let's search `slugGraphics = Array.from({ length: X }`
    var_name = "".join(x.capitalize() for x in slug.split("-"))
    var_name = var_name[0].lower() + var_name[1:] + "Graphics"
    m_len = re.search(rf'{var_name}\s*=\s*Array\.from\(\{{\s*length:\s*(\d+)', posts_ts)
    if m_len:
        prev_count = f"{m_len.group(1)} 張"
    elif slug == "when-kids-say-boring-cut-easy-content":
        prev_count = "0 張 (無圖)"
        
    status = []
    if prev_count == "0 張 (無圖)" and len(imgs) > 0:
        status.append("🔥 原為 0 張，現補上 8 張圖片！")
    elif has_today:
        status.append(f"🔥 今日重新放入全新圖片 (現有 {len(imgs)} 張)！")
    else:
        status.append("✅ 未變動 (維持 9/13 原圖)")
        
    print(f"{d[:42]:<45} | {len(imgs):<8} | {prev_count:<10} | {', '.join(status)}")
