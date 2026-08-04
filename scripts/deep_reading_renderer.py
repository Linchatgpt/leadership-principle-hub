#!/usr/bin/env python3
"""Render the approved deep-reading Markdown subset into chapter article HTML."""

import html
import re


def _inline(value):
    escaped = html.escape(value.strip())
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)


def render_deep_reading_markdown(source):
    lines = source.splitlines()
    output = []
    paragraph = []
    list_kind = None
    open_panel = None

    def flush_paragraph():
        nonlocal paragraph
        if not paragraph:
            return
        text = "".join(part.strip() for part in paragraph)
        if text.startswith("導言｜"):
            text = "<b>導言｜</b>" + _inline(text[len("導言｜"):])
        else:
            text = _inline(text)
        output.append(f"<p>{text}</p>")
        paragraph = []

    def close_list():
        nonlocal list_kind
        if list_kind:
            output.append(f"</{list_kind}>")
            list_kind = None

    def close_panel():
        nonlocal open_panel
        if open_panel:
            output.append("</div>")
            open_panel = None

    index = 0
    while index < len(lines):
        raw = lines[index].rstrip()
        stripped = raw.strip()
        if not stripped:
            flush_paragraph()
            if open_panel == "tool":
                close_panel()
            close_list()
            index += 1
            continue

        if stripped.startswith("# "):
            flush_paragraph(); close_list(); close_panel()
            index += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph(); close_list(); close_panel()
            title = stripped[3:].strip()
            if title == "總結提要":
                output.extend([
                    '<div class="reading-summary">',
                    '<span class="tool-label">深入閱讀收束</span>',
                    "<h3>總結提要</h3>",
                ])
                open_panel = "summary"
            else:
                output.append(f"<h3>{_inline(title)}</h3>")
            index += 1
            continue

        if stripped.startswith("### "):
            flush_paragraph(); close_list(); close_panel()
            title = stripped[4:].strip()
            label, separator, heading = title.partition("｜")
            output.append('<div class="reading-tool">')
            output.append(f'<span class="tool-label">{_inline(label)}</span>')
            output.append(f"<h3>{_inline(heading if separator else title)}</h3>")
            open_panel = "tool"
            index += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph(); close_list()
            quote_lines = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip().rstrip())
                index += 1
            quote = " ".join(quote_lines).replace("  ", " ")
            match = re.match(r"\*\*(.+?)｜(.+?)\*\*\s*(.*)", quote)
            if match:
                output.extend([
                    '<div class="reading-pause">',
                    f'<span class="pause-label">{_inline(match.group(1))}</span>',
                    f"<h3>{_inline(match.group(2))}</h3>",
                    f"<p>{_inline(match.group(3))}</p>",
                    "</div>",
                ])
            else:
                output.append(f"<blockquote>{_inline(quote)}</blockquote>")
            continue

        ordered = re.match(r"\d+\.\s+(.*)", stripped)
        unordered = re.match(r"[-*]\s+(.*)", stripped)
        if ordered or unordered:
            flush_paragraph()
            desired = "ol" if ordered else "ul"
            if list_kind != desired:
                close_list()
                output.append(f"<{desired}>")
                list_kind = desired
            output.append(f"<li>{_inline((ordered or unordered).group(1))}</li>")
            index += 1
            continue

        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    close_list()
    close_panel()
    return "\n".join(output)


def replace_deep_reading_article(page_html, article_html):
    start_marker = '<div class="reading-essay">'
    end_marker = '</div></section><section id="s2">'
    start = page_html.find(start_marker)
    end = page_html.find(end_marker, start + len(start_marker))
    if start < 0 or end < 0:
        raise ValueError("chapter page is missing the deep-reading article boundary")
    content_start = start + len(start_marker)
    return page_html[:content_start] + article_html + page_html[end:]
