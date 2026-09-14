import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
today_str = "2026-09-14"

modified_folders = {}
for d in os.listdir(base):
    folder_path = os.path.join(base, d)
    if not os.path.isdir(folder_path):
        continue
    for f in os.listdir(folder_path):
        fpath = os.path.join(folder_path, f)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath))
        if mtime.strftime('%Y-%m-%d') == today_str and f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            if d not in modified_folders:
                modified_folders[d] = []
            modified_folders[d].append((f, mtime))

print(f"Total folders with images modified today ({today_str}): {len(modified_folders)}")
for d, files in modified_folders.items():
    print(f"\n📂 {d} ({len(files)} 張圖片修改):")
    for f, mtime in files[:5]:
        print(f"   - {f} ({mtime.strftime('%H:%M:%S')})")
    if len(files) > 5:
        print(f"   ...以及其他 {len(files)-5} 張")
