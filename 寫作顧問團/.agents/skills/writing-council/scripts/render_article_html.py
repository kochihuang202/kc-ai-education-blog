#!/usr/bin/env python3
"""Render a writing-council Markdown draft as a readable standalone HTML file."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime
from pathlib import Path


LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
PARAGRAPH_ID_RE = re.compile(r"^\[(P\d+[A-Za-z]?)\]\s*(.*)$")


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = LINK_RE.sub(
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}" '
            f'target="_blank" rel="noreferrer">{match.group(1)}</a>'
        ),
        escaped,
    )
    escaped = re.sub(
        r"\*\*(.+?)\*\*",
        lambda match: "<strong>"
        + re.sub(r"\*([^*]+)\*", r"<em>\1</em>", match.group(1))
        + "</strong>",
        escaped,
    )
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def markdown_body(markdown: str, changed_ids: set[str]) -> tuple[str, str]:
    lines = markdown.splitlines()
    output: list[str] = []
    title = "文章預覽"
    index = 0

    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()

        if not stripped or stripped.startswith("<!--"):
            index += 1
            continue

        if stripped == "---":
            output.append("<hr>")
            index += 1
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            heading_text = heading.group(2)
            if level == 1:
                title = re.sub(r"[*_`]", "", heading_text)
            output.append(f"<h{level}>{inline_markup(heading_text)}</h{level}>")
            index += 1
            continue

        if stripped.startswith("> "):
            output.append(f"<blockquote>{inline_markup(stripped[2:])}</blockquote>")
            index += 1
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(f"<li>{inline_markup(lines[index].strip()[2:])}</li>")
                index += 1
            output.append("<ul>" + "".join(items) + "</ul>")
            continue

        paragraph = PARAGRAPH_ID_RE.match(stripped)
        if paragraph:
            paragraph_id, content = paragraph.groups()
            change_attributes = (
                ' class="latest-change" data-latest-change="true"'
                if paragraph_id in changed_ids
                else ""
            )
            output.append(
                f'<p id="{paragraph_id}" data-paragraph-id="{paragraph_id}"{change_attributes}>'
                f'{inline_markup(content)}</p>'
            )
        else:
            output.append(f"<p>{inline_markup(stripped)}</p>")
        index += 1

    return title, "\n".join(output)


def load_latest_changes(markdown_path: Path) -> tuple[list[str], set[str]]:
    change_file = markdown_path.parent / "09-本次修改.json"
    if not change_file.is_file():
        return [], set()
    try:
        change_data = json.loads(change_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return [], set()
    if change_data.get("source") != markdown_path.name:
        return [], set()
    summary = [str(item) for item in change_data.get("summary", []) if str(item).strip()]
    changed_ids = {str(item) for item in change_data.get("changed_ids", [])}
    return summary, changed_ids


def render(markdown_path: Path) -> str:
    markdown = markdown_path.read_text(encoding="utf-8")
    change_summary, changed_ids = load_latest_changes(markdown_path)
    title, body = markdown_body(markdown, changed_ids)
    modified = datetime.fromtimestamp(markdown_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    source = html.escape(markdown_path.name)
    page_title = html.escape(title)
    storage_key = json.dumps(f"writing-council:{markdown_path.stem}", ensure_ascii=False)
    suggested_name = json.dumps(f"{markdown_path.stem}-使用者修改.md", ensure_ascii=False)
    if change_summary:
        change_items = "".join(f"<li>{html.escape(item)}</li>" for item in change_summary)
        change_panel = (
            '<section class="latest-changes" aria-label="本次修改">'
            '<span class="change-kicker">LATEST CHANGES</span>'
            '<h2>本次修改</h2>'
            f'<ul>{change_items}</ul>'
            '<p>正文中的淡色區塊是這次有變動的部分；下一次修改時會自動換成新的標示。</p>'
            '</section>'
        )
    else:
        change_panel = ""

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <style>
    :root {{ --ink:#2d2926; --muted:#7d746d; --accent:#c0512f; --paper:#fffdf9; --page:#f4efe8; --line:#eadfd5; --reading-size:1.08rem; }}
    * {{ box-sizing:border-box; }}
    body[data-theme="dark"] {{ --ink:#e8dfd7; --muted:#ac9e94; --accent:#e58a65; --paper:#24201d; --page:#171513; --line:#423a35; }}
    body {{ margin:0; background:var(--page); color:var(--ink); font-family:"Noto Serif TC","Microsoft JhengHei",serif; line-height:1.95; transition:background .2s,color .2s; }}
    main {{ width:min(760px, calc(100% - 32px)); margin:32px auto; padding:52px 64px; background:var(--paper); border:1px solid var(--line); border-radius:18px; box-shadow:0 14px 44px rgba(74,55,42,.08); }}
    .workspace-label {{ display:block; margin-bottom:4px; color:var(--accent); font-family:"Microsoft JhengHei",sans-serif; font-size:.78rem; font-weight:700; letter-spacing:.16em; }}
    .workspace-help {{ margin:0 0 26px; color:var(--muted); font-family:"Microsoft JhengHei",sans-serif; font-size:.9rem; line-height:1.7; }}
    .latest-changes {{ margin:0 0 42px; padding:22px 24px; border:1px solid color-mix(in srgb, var(--accent) 30%, var(--line)); border-radius:14px; background:color-mix(in srgb, var(--accent) 7%, var(--paper)); font-family:"Microsoft JhengHei",sans-serif; }}
    .latest-changes .change-kicker {{ color:var(--accent); font-size:.7rem; font-weight:800; letter-spacing:.15em; }}
    .latest-changes h2 {{ margin:4px 0 10px; color:var(--ink); font-size:1.25rem; }}
    .latest-changes ul {{ margin:0; padding-left:1.3em; }}
    .latest-changes li {{ margin:.35em 0; }}
    .latest-changes p {{ margin:10px 0 0; color:var(--muted); font-size:.82rem; }}
    .toolbar {{ position:sticky; top:12px; z-index:10; display:flex; flex-wrap:wrap; gap:8px; margin:-18px 0 36px; padding:10px; border:1px solid var(--line); border-radius:12px; background:color-mix(in srgb, var(--paper) 94%, transparent); box-shadow:0 8px 24px rgba(74,55,42,.08); font-family:"Microsoft JhengHei",sans-serif; backdrop-filter:blur(10px); }}
    button {{ min-height:38px; padding:8px 13px; border:1px solid var(--line); border-radius:8px; background:var(--paper); color:var(--ink); cursor:pointer; font:inherit; }}
    button.primary {{ border-color:var(--accent); background:var(--accent); color:#fff; }}
    button:hover {{ transform:translateY(-1px); }}
    .toolbar-divider {{ width:1px; margin:3px 2px; background:var(--line); }}
    #edit-status {{ align-self:center; margin-left:auto; color:var(--muted); font-size:.8rem; }}
    .meta {{ margin-bottom:36px; padding-bottom:18px; border-bottom:1px solid var(--line); color:var(--muted); font-family:"Microsoft JhengHei",sans-serif; font-size:.86rem; }}
    h1 {{ margin:0 0 12px; color:#302722; font-size:clamp(2rem,5vw,3.15rem); line-height:1.25; letter-spacing:.02em; }}
    h2 {{ margin:56px 0 20px; color:var(--accent); font-size:1.45rem; line-height:1.45; }}
    h3 {{ margin:36px 0 16px; font-size:1.15rem; }}
    p {{ margin:0 0 1.35em; font-size:var(--reading-size); }}
    article[contenteditable="true"] {{ outline:none; }}
    article p.latest-change {{ margin-left:-16px; margin-right:-16px; padding:12px 16px; border-left:4px solid #e7a263; border-radius:0 10px 10px 0; background:color-mix(in srgb, #f1b77e 17%, var(--paper)); }}
    article[contenteditable="true"] p:hover, article[contenteditable="true"] h1:hover, article[contenteditable="true"] h2:hover, article[contenteditable="true"] blockquote:hover, article[contenteditable="true"] li:hover {{ background:#fff6e9; }}
    article[contenteditable="true"] p:focus, article[contenteditable="true"] h1:focus, article[contenteditable="true"] h2:focus, article[contenteditable="true"] blockquote:focus, article[contenteditable="true"] li:focus {{ outline:2px solid #e6aa74; outline-offset:5px; background:#fffaf2; }}
    blockquote {{ margin:20px 0 36px; padding:16px 22px; border-left:4px solid var(--accent); background:#fbf3ed; color:#5b4438; font-size:1.12rem; }}
    strong {{ color:#5f2d1c; }}
    a {{ color:var(--accent); text-underline-offset:3px; }}
    ul {{ padding-left:1.4em; }}
    li {{ margin:.55em 0; }}
    hr {{ margin:52px 0; border:0; border-top:1px solid var(--line); }}
    code {{ padding:.12em .35em; border-radius:4px; background:#f3ece6; font-family:ui-monospace,Consolas,monospace; }}
    article[contenteditable="true"]::before {{ content:"編輯模式"; position:fixed; right:18px; bottom:18px; z-index:20; padding:7px 11px; border-radius:999px; background:var(--accent); color:#fff; font:700 .75rem "Microsoft JhengHei",sans-serif; box-shadow:0 5px 18px rgba(0,0,0,.15); }}
    @media (max-width:640px) {{
      main {{ width:100%; margin:0; padding:32px 22px 56px; border:0; border-radius:0; }}
      h2 {{ margin-top:44px; }}
      .toolbar {{ top:0; margin:-16px -8px 24px; }}
      #edit-status {{ width:100%; margin-left:2px; }}
      .toolbar-divider {{ display:none; }}
    }}
    @media print {{ body {{ background:#fff; }} main {{ width:100%; margin:0; border:0; box-shadow:none; }} }}
  </style>
</head>
<body>
  <main>
    <span class="workspace-label">文章工作台</span>
    <div class="meta">最新版來源：{source}｜同步時間：{modified}</div>
    <p class="workspace-help">閱讀時保持乾淨版面；要自己修改時按「開始編輯」，完成後按「儲存修改稿」。你也可以不自行修改，直接回到 Codex 告訴我想改哪裡。</p>
    <div class="toolbar">
      <button class="primary" id="edit-button" type="button">開始編輯</button>
      <button id="save-button" type="button">儲存修改稿</button>
      <span class="toolbar-divider"></span>
      <button id="undo-button" type="button" title="復原上一步">復原</button>
      <button id="redo-button" type="button" title="重做上一步">重做</button>
      <button id="smaller-button" type="button" title="縮小文字">A−</button>
      <button id="larger-button" type="button" title="放大文字">A＋</button>
      <button id="theme-button" type="button">深色</button>
      <button id="reset-button" type="button">放棄本頁修改</button>
      <span id="edit-status">閱讀模式</span>
    </div>
    {change_panel}
    <article id="article" spellcheck="true">{body}</article>
  </main>
  <script>
    const article = document.getElementById('article');
    const editButton = document.getElementById('edit-button');
    const saveButton = document.getElementById('save-button');
    const resetButton = document.getElementById('reset-button');
    const undoButton = document.getElementById('undo-button');
    const redoButton = document.getElementById('redo-button');
    const smallerButton = document.getElementById('smaller-button');
    const largerButton = document.getElementById('larger-button');
    const themeButton = document.getElementById('theme-button');
    const status = document.getElementById('edit-status');
    const storageKey = {storage_key};
    const suggestedName = {suggested_name};
    const generatedHtml = article.innerHTML;
    const latestChangeIds = new Set(
      Array.from(article.querySelectorAll('[data-latest-change="true"]'))
        .map(element => element.dataset.paragraphId)
        .filter(Boolean)
    );
    let editing = false;

    function applyLatestChangeMarkers() {{
      article.querySelectorAll('[data-paragraph-id]').forEach(element => {{
        const isLatestChange = latestChangeIds.has(element.dataset.paragraphId);
        element.classList.toggle('latest-change', isLatestChange);
        if (isLatestChange) {{
          element.dataset.latestChange = 'true';
        }} else {{
          delete element.dataset.latestChange;
        }}
      }});
    }}

    const savedHtml = localStorage.getItem(storageKey);
    if (savedHtml) {{
      article.innerHTML = savedHtml;
      applyLatestChangeMarkers();
      status.textContent = '已載入本機修改';
    }}

    function setEditing(next) {{
      editing = next;
      article.contentEditable = next ? 'true' : 'false';
      editButton.textContent = next ? '完成編輯' : '開始編輯';
      status.textContent = next ? '編輯中（自動暫存於此瀏覽器）' : '閱讀模式';
      if (next) article.focus();
    }}

    editButton.addEventListener('click', () => setEditing(!editing));
    undoButton.addEventListener('click', () => document.execCommand('undo'));
    redoButton.addEventListener('click', () => document.execCommand('redo'));

    let readingSize = Number(localStorage.getItem(`${{storageKey}}:font-size`) || 1.08);
    function applyReadingSize() {{
      document.documentElement.style.setProperty('--reading-size', `${{readingSize}}rem`);
      localStorage.setItem(`${{storageKey}}:font-size`, String(readingSize));
    }}
    smallerButton.addEventListener('click', () => {{ readingSize = Math.max(.9, readingSize - .06); applyReadingSize(); }});
    largerButton.addEventListener('click', () => {{ readingSize = Math.min(1.42, readingSize + .06); applyReadingSize(); }});
    applyReadingSize();

    let theme = localStorage.getItem('writing-council:theme') || 'light';
    function applyTheme() {{
      document.body.dataset.theme = theme;
      themeButton.textContent = theme === 'light' ? '深色' : '淺色';
      localStorage.setItem('writing-council:theme', theme);
    }}
    themeButton.addEventListener('click', () => {{ theme = theme === 'light' ? 'dark' : 'light'; applyTheme(); }});
    applyTheme();
    article.addEventListener('input', () => {{
      localStorage.setItem(storageKey, article.innerHTML);
      status.textContent = '編輯中（已自動暫存）';
    }});

    function inlineMarkdown(node) {{
      if (node.nodeType === Node.TEXT_NODE) return node.textContent;
      if (node.nodeType !== Node.ELEMENT_NODE) return '';
      const content = Array.from(node.childNodes).map(inlineMarkdown).join('');
      if (node.tagName === 'STRONG' || node.tagName === 'B') return `**${{content}}**`;
      if (node.tagName === 'EM' || node.tagName === 'I') return `*${{content}}*`;
      if (node.tagName === 'CODE') return `\\`${{content}}\\``;
      if (node.tagName === 'A') return `[${{content}}](${{node.href}})`;
      if (node.tagName === 'BR') return '\\n';
      return content;
    }}

    function elementMarkdown(element) {{
      const content = Array.from(element.childNodes).map(inlineMarkdown).join('').trim();
      if (/^H[1-3]$/.test(element.tagName)) return `${{'#'.repeat(Number(element.tagName[1]))}} ${{content}}`;
      if (element.tagName === 'BLOCKQUOTE') return `> ${{content}}`;
      if (element.tagName === 'HR') return '---';
      if (element.tagName === 'UL') return Array.from(element.children).map(li => `- ${{Array.from(li.childNodes).map(inlineMarkdown).join('').trim()}}`).join('\\n');
      if (element.tagName === 'P') {{
        const paragraphId = element.dataset.paragraphId;
        return paragraphId ? `[${{paragraphId}}] ${{content}}` : content;
      }}
      return content;
    }}

    function exportMarkdown() {{
      return Array.from(article.children).map(elementMarkdown).filter(Boolean).join('\\n\\n') + '\\n';
    }}

    saveButton.addEventListener('click', async () => {{
      const markdown = exportMarkdown();
      try {{
        if ('showSaveFilePicker' in window) {{
          const handle = await window.showSaveFilePicker({{
            suggestedName,
            types: [{{ description: 'Markdown 文件', accept: {{ 'text/markdown': ['.md'] }} }}]
          }});
          const writable = await handle.createWritable();
          await writable.write(markdown);
          await writable.close();
          status.textContent = '修改稿已儲存';
          return;
        }}
      }} catch (error) {{
        if (error.name === 'AbortError') return;
      }}
      const blob = new Blob([markdown], {{ type: 'text/markdown;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = suggestedName;
      link.click();
      URL.revokeObjectURL(url);
      status.textContent = '修改稿已下載';
    }});

    resetButton.addEventListener('click', () => {{
      if (!confirm('確定放棄這個瀏覽器裡尚未交回的修改嗎？')) return;
      localStorage.removeItem(storageKey);
      article.innerHTML = generatedHtml;
      applyLatestChangeMarkers();
      setEditing(false);
      status.textContent = '已恢復產生時的內容';
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--current-output", type=Path)
    parser.add_argument("--workspace-output", type=Path)
    args = parser.parse_args()

    source = args.markdown.resolve()
    if not source.is_file():
        raise SystemExit(f"Markdown file not found: {source}")

    rendered = render(source)
    output = (args.output or source.with_suffix(".html")).resolve()
    output.write_text(rendered, encoding="utf-8")

    if args.current_output:
        current_output = args.current_output.resolve()
        current_output.write_text(rendered, encoding="utf-8")

    if args.workspace_output:
        workspace_output = args.workspace_output.resolve()
        workspace_output.write_text(rendered, encoding="utf-8")

    print(output)
    if args.current_output:
        print(args.current_output.resolve())
    if args.workspace_output:
        print(args.workspace_output.resolve())


if __name__ == "__main__":
    main()
