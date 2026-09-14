import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
folders = [d for d in sorted(os.listdir(base)) if "20260913" in d]

for d in folders:
    fpath = os.path.join(base, d)
    htmls = [f for f in os.listdir(fpath) if f.endswith(".html")]
    if not htmls:
        continue
    filepath = os.path.join(fpath, htmls[0])
    lines = open(filepath, encoding="utf-8", errors="ignore").readlines()
    print(f"\n📂 {d}")
    print(f"   HTML: {htmls[0]}")
    for l in lines[8:25]:
        if l.strip():
            print(f"   {l.strip()[:80]}")
