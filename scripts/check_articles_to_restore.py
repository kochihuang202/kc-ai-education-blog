import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "data", "posts.ts")
with open(p, "r", encoding="utf-8") as f:
    content = f.read()

posts_data = re.findall(r'title:\s*"([^"]+)",\s*slug:\s*"([^"]+)",\s*date:\s*"([^"]+)"', content)
for title, slug, date in posts_data[:20]:
    print(f"{date} | {slug} | {title}")
