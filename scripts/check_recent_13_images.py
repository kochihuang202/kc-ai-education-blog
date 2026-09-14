import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
folders = [d for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, d)) and "20260913" in d]

print(f"Total 20260913 folders: {len(folders)}")
for d in folders:
    folder_path = os.path.join(base, d)
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    print(f"\n=======================================================")
    print(f"📂 {d}")
    print(f"   圖片數量: {len(images)}")
    
    # Check modification times
    recent = []
    for f in sorted(images):
        fpath = os.path.join(folder_path, f)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath))
        recent.append((f, os.path.getsize(fpath), mtime))
        
    for f, size, mtime in recent:
        is_today = mtime.strftime('%Y-%m-%d') == '2026-09-14'
        tag = "🔴 [今天更動]" if is_today else "⚪ [舊檔案]"
        print(f"   {tag} {f} ({size:,} B) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
