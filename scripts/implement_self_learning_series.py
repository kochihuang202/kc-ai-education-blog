import os
import sys
import re
import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Update src/data/categories.ts
categories_path = os.path.join(PROJECT_ROOT, "src", "data", "categories.ts")
with open(categories_path, "r", encoding="utf-8") as f:
    cat_code = f.read()

new_category = """  {
    id: "self-learning-reflection",
    label: "自學省思",
    summary: "女兒自學路上的微小教養省思：從自由與界線、自律與心流，到把 AI 當成思維對手。",
    accent: "#C0512F"
  },
] as const;"""

if "self-learning-reflection" not in cat_code:
    cat_code = cat_code.replace("] as const;", new_category)
    with open(categories_path, "w", encoding="utf-8") as f:
        f.write(cat_code)
    print("[+] Updated src/data/categories.ts with self-learning-reflection category.")
else:
    print("[*] Category self-learning-reflection already exists.")

# 2. Update src/data/series.ts
series_path = os.path.join(PROJECT_ROOT, "src", "data", "series.ts")
with open(series_path, "r", encoding="utf-8") as f:
    series_code = f.read()

new_series = """  {
    id: "self-learning-reflection",
    name: "自學省思（共 7 篇）",
    accent: "#C0512F",
    steps: [
      { slug: "giving-freedom-with-clear-non-negotiable-boundaries", title: "第1篇 ｜ 我給孩子很大的自由，直到有一天，「我不要」變成了她的萬用答案", label: "1" },
      { slug: "stop-reminding-kids-building-real-self-discipline", title: "第2篇 ｜ 我不再提醒孩子了，因為我終於發現：我一直在替她「自律」", label: "2" },
      { slug: "when-kids-say-boring-cut-easy-content", title: "第3篇 ｜ 孩子一直喊「好無聊」，我反而把有趣的教材砍掉了", label: "3" },
      { slug: "reading-flow-state-versus-proof-of-learning", title: "第4篇 ｜ 孩子明明讀到停不下來，我卻差點因為一張「閱讀紀錄」打斷她", label: "4" },
      { slug: "sighing-shaking-head-emotional-separation-for-kids", title: "第5篇 ｜ 孩子一被提醒就嘆氣、甩頭、走人，我以前只看見「沒禮貌」", label: "5" },
      { slug: "letting-kids-experience-consequences-without-cruelty", title: "第6篇 ｜ 我差點讓孩子熬夜到崩潰，只為了讓她「記住教訓」", label: "6" },
      { slug: "using-ai-thinking-partner-not-alone", title: "第7篇 ｜ 我開始用 AI 之後，最大的改變不是少想，而是不再只跟自己想", label: "7" }
    ]
  },
];"""

if "self-learning-reflection" not in series_code:
    series_code = series_code.replace("];", new_series)
    with open(series_path, "w", encoding="utf-8") as f:
        f.write(series_code)
    print("[+] Updated src/data/series.ts with self-learning-reflection series.")
else:
    print("[*] Series self-learning-reflection already exists.")

# 3. Update src/data/posts.ts
posts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
with open(posts_path, "r", encoding="utf-8") as f:
    posts_code = f.read()

SERIES_SLUGS = {
    "giving-freedom-with-clear-non-negotiable-boundaries": {
        "kicker": "自學省思 · 第1篇",
        "related": ["stop-reminding-kids-building-real-self-discipline", "letting-kids-experience-consequences-without-cruelty", "using-ai-thinking-partner-not-alone"]
    },
    "stop-reminding-kids-building-real-self-discipline": {
        "kicker": "自學省思 · 第2篇",
        "related": ["giving-freedom-with-clear-non-negotiable-boundaries", "when-kids-say-boring-cut-easy-content", "letting-kids-experience-consequences-without-cruelty"]
    },
    "when-kids-say-boring-cut-easy-content": {
        "kicker": "自學省思 · 第3篇",
        "related": ["stop-reminding-kids-building-real-self-discipline", "reading-flow-state-versus-proof-of-learning", "using-ai-thinking-partner-not-alone"]
    },
    "reading-flow-state-versus-proof-of-learning": {
        "kicker": "自學省思 · 第4篇",
        "related": ["when-kids-say-boring-cut-easy-content", "sighing-shaking-head-emotional-separation-for-kids", "stop-reminding-kids-building-real-self-discipline"]
    },
    "sighing-shaking-head-emotional-separation-for-kids": {
        "kicker": "自學省思 · 第5篇",
        "related": ["reading-flow-state-versus-proof-of-learning", "letting-kids-experience-consequences-without-cruelty", "giving-freedom-with-clear-non-negotiable-boundaries"]
    },
    "letting-kids-experience-consequences-without-cruelty": {
        "kicker": "自學省思 · 第6篇",
        "related": ["sighing-shaking-head-emotional-separation-for-kids", "using-ai-thinking-partner-not-alone", "giving-freedom-with-clear-non-negotiable-boundaries"]
    },
    "using-ai-thinking-partner-not-alone": {
        "kicker": "自學省思 · 第7篇",
        "related": ["letting-kids-experience-consequences-without-cruelty", "giving-freedom-with-clear-non-negotiable-boundaries", "when-kids-say-boring-cut-easy-content"]
    }
}

for slug, conf in SERIES_SLUGS.items():
    # Update categories to include "self-learning-reflection"
    pattern = re.compile(rf'(slug:\s*"{slug}",[\s\S]*?kicker:\s*)"[^"]+"(,[\s\S]*?categories:\s*)\[(.*?)\](,[\s\S]*?relatedPosts:\s*)\[(.*?)\]')
    
    match = pattern.search(posts_code)
    if match:
        kicker_prefix = match.group(1)
        cats_prefix = match.group(2)
        old_cats = match.group(3)
        rel_prefix = match.group(4)
        
        # Prepare categories
        cats_list = [c.strip().strip('"') for c in old_cats.split(",") if c.strip()]
        if "self-learning-reflection" not in cats_list:
            cats_list = ["self-learning-reflection"] + [c for c in cats_list if c != "self-learning-reflection"]
        new_cats_str = ", ".join(f'"{c}"' for c in cats_list)
        
        # Prepare related posts
        new_rel_str = ", ".join(f'"{r}"' for r in conf["related"])
        
        replacement = f'{kicker_prefix}"{conf["kicker"]}"{cats_prefix}[{new_cats_str}]{rel_prefix}[{new_rel_str}]'
        posts_code = posts_code[:match.start()] + replacement + posts_code[match.end():]
        print(f"[+] Updated post object: {slug}")
    else:
        print(f"[-] Could not find post object pattern for {slug}")

with open(posts_path, "w", encoding="utf-8") as f:
    f.write(posts_code)
print("[+] Updated src/data/posts.ts with series metadata.")

# 4. Update DEPLOY_VERSION in cloudflare/worker-proxy.js
worker_js_path = os.path.join(PROJECT_ROOT, "cloudflare", "worker-proxy.js")
with open(worker_js_path, "r", encoding="utf-8") as f:
    worker_code = f.read()

now_str = datetime.datetime.now().strftime("v_%Y_%m_%d_%H_%M_%S")
worker_code = re.sub(r'const DEPLOY_VERSION = "[^"]+";', f'const DEPLOY_VERSION = "{now_str}";', worker_code)
with open(worker_js_path, "w", encoding="utf-8") as f:
    f.write(worker_code)
print(f"[+] Updated DEPLOY_VERSION in cloudflare/worker-proxy.js to {now_str}")
