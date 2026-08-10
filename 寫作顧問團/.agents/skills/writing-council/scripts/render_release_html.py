#!/usr/bin/env python3
"""Render a clean, upload-ready KC article from a writing-council release Markdown file."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
PARAGRAPH_ID_RE = re.compile(r"^\[(P\d+[A-Za-z]?)\]\s*(.*)$")
ACCENT = "#C0512F"
INK = "#1C1A17"
MUTED = "#8A817A"
PAPER = "#FAF7F2"
LINE = "#E0D8CF"


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = LINK_RE.sub(
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}" '
            f'target="_blank" rel="noreferrer" '
            f'style="color:{ACCENT};text-decoration:underline;text-underline-offset:3px;">'
            f'{match.group(1)}</a>'
        ),
        escaped,
    )
    escaped = re.sub(
        r"\*\*(.+?)\*\*",
        lambda match: f'<strong style="color:{ACCENT};font-weight:700;">{match.group(1)}</strong>',
        escaped,
    )
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def extract_brand(markdown: str, name: str) -> tuple[list[str], str]:
    pattern = re.compile(
        rf"<!-- {name} -->\s*(.*?)\s*<!-- /{name} -->",
        re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        return [], markdown
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", match.group(1)) if item.strip()]
    return paragraphs, pattern.sub("", markdown, count=1)


def paragraph_html(paragraph_id: str | None, content: str) -> str:
    rendered = inline_markup(content)
    attrs = f' id="{paragraph_id}" data-paragraph-id="{paragraph_id}"' if paragraph_id else ""

    if paragraph_id in {"P08", "P47"}:
        font_size = "22px" if paragraph_id == "P08" else "18px"
        return (
            '<section style="padding:8px 24px 18px 24px;">'
            f'<section style="background-color:{ACCENT};padding:22px 18px;margin:0;">'
            f'<p{attrs} style="font-size:{font_size};font-weight:bold;color:#FFFFFF;'
            f'margin:0;line-height:1.6;text-align:center;">{rendered}</p>'
            '</section></section>'
        )

    if paragraph_id in {"P16", "P20", "P41"}:
        return (
            '<section style="padding:8px 24px 18px 24px;">'
            f'<section style="background-color:rgba(192,81,47,0.06);padding:20px 18px;'
            f'border-left:5px solid {ACCENT};margin:0;">'
            f'<p{attrs} style="font-size:18px;font-weight:bold;color:{ACCENT};'
            f'margin:0;line-height:1.65;">{rendered}</p>'
            '</section></section>'
        )

    if paragraph_id in {"P29", "P30", "P31", "P32", "P33"}:
        return (
            '<section style="padding:0 24px 12px 24px;">'
            f'<section style="border-left:4px solid {ACCENT};padding:14px 16px;'
            f'background-color:rgba(192,81,47,0.035);">'
            f'<p{attrs} style="font-size:16px;color:{INK};margin:0;line-height:1.85;">{rendered}</p>'
            '</section></section>'
        )

    if paragraph_id == "P35":
        return (
            '<section style="padding:4px 24px 18px 24px;">'
            f'<section style="background-color:rgba(192,81,47,0.06);padding:18px 16px;margin:0;">'
            f'<p{attrs} style="font-size:16px;color:{INK};margin:0;line-height:1.85;">{rendered}</p>'
            '</section></section>'
        )

    if paragraph_id in {"P49", "P50"}:
        return (
            '<section style="padding:0 24px 14px 24px;">'
            f'<section style="border:1px solid {LINE};padding:18px 16px;background-color:#FFFDFC;">'
            f'<p{attrs} style="font-size:16px;color:{INK};margin:0;line-height:1.85;">{rendered}</p>'
            '</section></section>'
        )

    return (
        '<section style="padding:0 24px;">'
        f'<p{attrs} style="font-size:16px;color:{INK};margin:0 0 18px 0;line-height:1.85;">'
        f'{rendered}</p></section>'
    )


def render(markdown_path: Path) -> str:
    markdown = markdown_path.read_text(encoding="utf-8")
    brand_open, markdown = extract_brand(markdown, "BRAND_OPEN")
    brand_close, markdown = extract_brand(markdown, "BRAND_CLOSE")

    title = "文章"
    subtitle = ""
    body: list[str] = []
    lines = markdown.splitlines()
    index = 0

    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or stripped.startswith("<!--"):
            index += 1
            continue

        if stripped == "---":
            body.append(
                '<section style="padding:34px 24px 0 24px;">'
                f'<section style="height:1px;background-color:{ACCENT};opacity:0.25;margin:0;"></section>'
                '</section>'
            )
            index += 1
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            heading_text = heading.group(2)
            if level == 1:
                title = re.sub(r"[*_`]", "", heading_text)
            else:
                body.append(
                    '<section style="padding:40px 24px 16px 24px;">'
                    f'<section style="border-left:5px solid {ACCENT};padding-left:14px;">'
                    f'<h2 style="font-size:22px;font-weight:bold;color:{ACCENT};margin:0;'
                    f'line-height:1.45;">{inline_markup(heading_text)}</h2>'
                    '</section></section>'
                )
            index += 1
            continue

        if stripped.startswith("> "):
            subtitle = stripped[2:]
            index += 1
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                item = inline_markup(lines[index].strip()[2:])
                items.append(
                    f'<li style="font-size:14px;color:{MUTED};margin:0 0 10px 0;'
                    f'line-height:1.7;">{item}</li>'
                )
                index += 1
            body.append(
                '<section style="padding:0 24px 8px 24px;">'
                f'<ul style="margin:0;padding-left:20px;color:{MUTED};">{"".join(items)}</ul>'
                '</section>'
            )
            continue

        paragraph = PARAGRAPH_ID_RE.match(stripped)
        if paragraph:
            paragraph_id, content = paragraph.groups()
            body.append(paragraph_html(paragraph_id, content))
        else:
            body.append(paragraph_html(None, stripped))
        index += 1

    open_html = "".join(
        f'<p style="font-size:16px;color:{ACCENT};margin:0 0 '
        f'{"10px" if i < len(brand_open) - 1 else "0"} 0;line-height:1.8;">'
        f'{inline_markup(text)}</p>'
        for i, text in enumerate(brand_open)
    )
    close_html = "".join(
        f'<p style="font-size:16px;color:{ACCENT};margin:0 0 '
        f'{"14px" if i < len(brand_close) - 1 else "0"} 0;line-height:1.8;">'
        f'{inline_markup(text)}</p>'
        for i, text in enumerate(brand_close)
    )

    subtitle_html = (
        f'<p style="font-size:16px;color:{MUTED};margin:14px 0 0 0;line-height:1.75;">'
        f'{inline_markup(subtitle)}</p>'
        if subtitle
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
</head>
<body style="margin:0;background-color:#EFE9E2;">
<section style="max-width:600px;margin:0 auto;padding:0;background-color:{PAPER};font-family:Georgia,'Noto Serif SC','Noto Serif TC','Songti SC','PMingLiU','新細明體',serif;color:{INK};line-height:1.85;">
  <section style="height:6px;background-color:{ACCENT};margin:0;padding:0;"></section>
  <section style="padding:32px 24px 0 24px;">{open_html}</section>
  <section style="padding:20px 24px 0 24px;"><section style="height:1px;background-color:{ACCENT};opacity:0.25;margin:0;"></section></section>
  <section style="padding:28px 24px 26px 24px;">
    <h1 style="font-size:28px;font-weight:bold;color:{INK};line-height:1.45;margin:0;letter-spacing:0.3px;">{inline_markup(title)}</h1>
    {subtitle_html}
  </section>
  {''.join(body)}
  <section style="padding:36px 24px 0 24px;"><section style="height:1px;background-color:{ACCENT};opacity:0.25;margin:0;"></section></section>
  <section style="padding:20px 24px 40px 24px;">{close_html}</section>
</section>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview-output", type=Path)
    args = parser.parse_args()

    output = args.output or args.markdown.with_suffix(".html")
    rendered = render(args.markdown)
    output.write_text(rendered, encoding="utf-8")
    print(output.resolve())
    if args.preview_output:
        args.preview_output.write_text(rendered, encoding="utf-8")
        print(args.preview_output.resolve())


if __name__ == "__main__":
    main()
