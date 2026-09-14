import os
import sys
import json
import re
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publish_helper

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_FOLDER = r"C:\Users\ji3cp\OneDrive - Foxconn\01_Home\32_上傳文章\file"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARTICLES = [
    {
        "folder": os.path.join(BASE_FOLDER, "20260911保護教育之後的二次傷害"),
        "slug": "fearful-face-in-protection-education",
        "title": "最傷孩子的，可能不是你沒教他保護自己，而是你教保護時那張恐懼的臉",
        "date": "2026-09-11",
        "excerpt": "你教孩子保護身體、認識界線、說不、跑、求救，這些都是對的。但你有沒有想過，你教這些的時候，臉上的表情與緊張，本身就在傳遞「這件事會毀了你」。真正的傷害是身體上的，但文化疊加的羞恥感，才是我們最該替孩子拆掉的二次傷害。",
        "start_line": 20,
        "end_line": 160,
        "camel": "FearfulFaceInProtectionEducation"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913好好使用 AI，不是少想一點，而是不再只跟自己想"),
        "slug": "using-ai-thinking-partner-not-alone",
        "title": "我開始用 AI 之後，最大的改變不是少想，而是不再只跟自己想",
        "date": "2026-09-13",
        "excerpt": "開始自學之後，最困擾我的往往不是選擇教材，而是沒有標準答案的微小育兒問題：孩子拖延、喊無聊、自律靠提醒、情緒反應強。好好使用 AI，不是為了偷懶少想，而是找一個強大的對手，不再讓自己一個人閉門造車。",
        "start_line": 20,
        "end_line": 539,
        "camel": "UsingAiThinkingPartnerNotAlone"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913孩子一看書就陷進去，我為什麼還一直想要她證明「有學到」？"),
        "slug": "reading-flow-state-versus-proof-of-learning",
        "title": "孩子明明讀到停不下來，我卻差點因為一張「閱讀紀錄」打斷她",
        "date": "2026-09-13",
        "excerpt": "女兒跟我說：「我一看書就會陷進去，所以我不想做紀錄。」大人常因為自己的不安與焦慮，急著要求孩子給出證明與成果，卻差點用功利主義打斷了孩子最珍貴、最難得的「心流狀態」。",
        "start_line": 20,
        "end_line": 490,
        "camel": "ReadingFlowStateVersusProofOfLearning"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913孩子因自己的選擇而痛苦，父母一定要救嗎？"),
        "slug": "letting-kids-experience-consequences-without-cruelty",
        "title": "我差點讓孩子熬夜到崩潰，只為了讓她「記住教訓」",
        "date": "2026-09-13",
        "excerpt": "孩子拖延到半夜才要做任務，我曾想狠下心「陪她做到凌晨兩點，用痛苦讓她記住教訓」。但我突然發覺：強迫折磨只是大人內心憤怒的宣洩，並不能培養真正的責任感。界線與後果，不等於殘忍地看著孩子崩潰。",
        "start_line": 20,
        "end_line": 372,
        "camel": "LettingKidsExperienceConsequencesWithoutCruelty"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913孩子說「很無聊」，父母到底該堅持，還是換方法？"),
        "slug": "when-kids-say-boring-cut-easy-content",
        "title": "孩子一直喊「好無聊」，我反而把有趣的教材砍掉了",
        "date": "2026-09-13",
        "excerpt": "孩子學英文一直喊好無聊，我做了一個奇怪的決定：把她最喜歡的趣味卡通佩佩豬砍掉，留下了最難最不喜歡但最有思考階梯的內容。結果她適應後展現了驚人理解力。無聊有時不是內容壞了，而是缺乏真正的挑戰。",
        "start_line": 20,
        "end_line": 375,
        "camel": "WhenKidsSayBoringCutEasyContent"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913我不再一直提醒孩子了：因為我發現，連「自律」都是我在替她做"),
        "slug": "stop-reminding-kids-building-real-self-discipline",
        "title": "我不再提醒孩子了，因為我終於發現：我一直在替她「自律」",
        "date": "2026-09-13",
        "excerpt": "我給孩子排了每日任務清單，以為這就是自主。直到我發覺每天真正出現的畫面，是我在後面狂盯時間、倒數提醒。你以為在教自律，其實只是你在幫她自律。當我停止提醒，孩子才真正開始掌握時間。",
        "start_line": 20,
        "end_line": 400,
        "camel": "StopRemindingKidsBuildingRealSelfDiscipline"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913我不是要孩子不生氣，而是不把自己交給情緒小怪獸"),
        "slug": "sighing-shaking-head-emotional-separation-for-kids",
        "title": "孩子一被提醒就嘆氣、甩頭、走人，我以前只看見「沒禮貌」",
        "date": "2026-09-13",
        "excerpt": "孩子被提醒就嘆氣、甩頭甚至轉身走開，大人第一時間只看見「沒禮貌」想立刻糾正。但比講禮貌更重要的是引導孩子了解：她不是故意忤逆，而是不知道怎麼處理情緒。允許生氣，但教孩子不把主導權交給情緒小怪獸。",
        "start_line": 20,
        "end_line": 540,
        "camel": "SighingShakingHeadEmotionalSeparationForKids"
    },
    {
        "folder": os.path.join(BASE_FOLDER, "20260913我給了孩子很大的自由，後來又收回了一點"),
        "slug": "giving-freedom-with-clear-non-negotiable-boundaries",
        "title": "我給孩子很大的自由，直到有一天，「我不要」變成了她的萬用答案",
        "date": "2026-09-13",
        "excerpt": "給了孩子很大的自由後，她開始發現原來討厭的事可以直接說「不要」，甚至進入僵局。大人意識到：給自由不等於無限退讓。沒有界線的自由會變成無序，適度收回部分決定權、守住底線，才是安全的自由。",
        "start_line": 20,
        "end_line": 276,
        "camel": "GivingFreedomWithClearNonNegotiableBoundaries"
    }
]

def run_all():
    # 1. Process each article with publish_helper
    for idx, art in enumerate(ARTICLES, 1):
        print(f"\n==========================================")
        print(f" Processing Article {idx}/8: {art['slug']}")
        print(f"==========================================")

        publish_helper.extract_html(
            src_dir=art['folder'],
            slug=art['slug'],
            start_line=art['start_line'],
            end_line=art['end_line'],
            project_root=PROJECT_ROOT
        )

        img_count, temp_dir = publish_helper.process_images(
            src_dir=art['folder'],
            slug=art['slug'],
            project_root=PROJECT_ROOT
        )

        if img_count > 0:
            publish_helper.upload_to_r2(
                temp_img_dir=temp_dir,
                slug=art['slug'],
                images_count=img_count
            )

        art['img_count'] = img_count

    # 2. Modify src/data/posts.ts
    posts_ts_path = os.path.join(PROJECT_ROOT, "src", "data", "posts.ts")
    with open(posts_ts_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build imports
    imports_str = ""
    for art in ARTICLES:
        import_var = art['camel'][0].lower() + art['camel'][1:] + "Html"
        imports_str += f'import {import_var} from "../article-html/posts/{art["slug"]}.html?raw";\n'

    # Insert imports at top after line 79 (before type CategoryId import)
    content = imports_str + content

    # Build graphics definitions
    graphics_str = ""
    for art in ARTICLES:
        if art['img_count'] > 0:
            var_base = art['camel'][0].lower() + art['camel'][1:] + "GraphicBase"
            var_gfx = art['camel'][0].lower() + art['camel'][1:] + "Graphics"
            graphics_str += f'const {var_base} =\n'
            graphics_str += f'  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/{art["slug"]}";\n\n'
            graphics_str += f'const {var_gfx} = Array.from({{ length: {art["img_count"]} }}, (_, index) => {{\n'
            graphics_str += f'  const page = index + 1;\n'
            graphics_str += f'  return {{\n'
            graphics_str += f'    src: `${{{var_base}}}/graphic-${{String(page).padStart(2, "0")}}.webp`,\n'
            graphics_str += f'    alt: `{art["title"]}圖文解析 ${{page}}/{art["img_count"]}`\n'
            graphics_str += f'  }};\n'
            graphics_str += f'}});\n\n'

    # Insert graphics declarations right before 'export const posts = ['
    posts_array_marker = "export const posts = ["
    content = content.replace(posts_array_marker, graphics_str + posts_array_marker)

    # Build post objects
    post_objects_str = ""
    for art in ARTICLES:
        html_var = art['camel'][0].lower() + art['camel'][1:] + "Html"
        gfx_var = art['camel'][0].lower() + art['camel'][1:] + "Graphics"
        
        post_objects_str += "  {\n"
        post_objects_str += f'    title: "{art["title"]}",\n'
        post_objects_str += f'    slug: "{art["slug"]}",\n'
        post_objects_str += f'    date: "{art["date"]}",\n'
        post_objects_str += f'    kicker: "KC 育兒手記",\n'
        post_objects_str += f'    excerpt:\n      "{art["excerpt"]}",\n'
        post_objects_str += f'    categories: ["parents", "core"],\n'
        
        if art['img_count'] > 0:
            post_objects_str += f'    coverImage: {gfx_var}[0].src,\n'
            post_objects_str += f'    coverAlt: {gfx_var}[0].alt,\n'
            post_objects_str += f'    gallery: {{\n'
            post_objects_str += f'      label: "<圖文解析>",\n'
            post_objects_str += f'      images: {gfx_var}\n'
            post_objects_str += f'    }},\n'
            
        post_objects_str += f'    relatedPosts: [],\n'
        post_objects_str += f'    body: {html_var}\n'
        post_objects_str += "  },\n"

    content = content.replace(posts_array_marker, posts_array_marker + "\n" + post_objects_str)

    with open(posts_ts_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[+] Updated src/data/posts.ts")

    # 3. Modify src/data/fb-status.json
    fb_json_path = os.path.join(PROJECT_ROOT, "src", "data", "fb-status.json")
    with open(fb_json_path, "r", encoding="utf-8") as f:
        fb_data = json.load(f)

    new_fb_data = {}
    for art in ARTICLES:
        new_fb_data[art["slug"]] = False
    new_fb_data.update(fb_data)

    with open(fb_json_path, "w", encoding="utf-8") as f:
        json.dump(new_fb_data, f, ensure_ascii=False, indent=2)
    print("[+] Updated src/data/fb-status.json")

    # 4. Modify cloudflare/worker-proxy.js DEPLOY_VERSION
    worker_js_path = os.path.join(PROJECT_ROOT, "cloudflare", "worker-proxy.js")
    with open(worker_js_path, "r", encoding="utf-8") as f:
        worker_code = f.read()

    import datetime
    now_str = datetime.datetime.now().strftime("v_%Y_%m_%d_%H_%M")
    worker_code = re.sub(r'const DEPLOY_VERSION = "[^"]+";', f'const DEPLOY_VERSION = "{now_str}";', worker_code)

    with open(worker_js_path, "w", encoding="utf-8") as f:
        f.write(worker_code)
    print(f"[+] Updated DEPLOY_VERSION in cloudflare/worker-proxy.js to {now_str}")

if __name__ == "__main__":
    run_all()
