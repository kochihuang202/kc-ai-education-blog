import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"

folders = [d for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, d)) and "20260913" in d]

for d in folders:
    folder_path = os.path.join(base, d)
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    print(f"\n📂 【{d}】 (圖片數量: {len(images)})")
    if not images:
        print("  (無圖片)")
        continue
    for f in sorted(images):
        fpath = os.path.join(folder_path, f)
        size = os.path.getsize(fpath)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d %H:%M:%S")
        ctime = datetime.datetime.fromtimestamp(os.path.getctime(fpath)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  - {f} | 大小: {size:,} bytes | 修改時間: {mtime} | 建立時間: {ctime}")
