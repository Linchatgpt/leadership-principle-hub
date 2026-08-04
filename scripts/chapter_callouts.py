import html
import json
import pathlib


def callout_path(root: pathlib.Path, chapter: int) -> pathlib.Path:
    return root / "content" / f"chapter_{chapter:02d}_callouts.json"


def load_chapter_callouts(root: pathlib.Path, chapter: int) -> list[dict]:
    path = callout_path(root, chapter)
    data = json.loads(path.read_text(encoding="utf-8"))
    if len(data) != 3:
        raise ValueError(f"{path} must contain exactly three callouts")
    required = {"label", "title", "paragraphs"}
    for item in data:
        missing = required - item.keys()
        if missing:
            raise ValueError(f"{path} callout missing: {', '.join(sorted(missing))}")
    return data


def render_chapter_callouts(callouts: list[dict]) -> str:
    rendered = []
    for item in callouts:
        parts = [
            '<aside class="reading-callout">',
            f'<span class="tool-label">{html.escape(item["label"])}</span>',
            f'<h3>{html.escape(item["title"])}</h3>',
        ]
        parts.extend(f'<p>{html.escape(paragraph)}</p>' for paragraph in item["paragraphs"])
        if item.get("items"):
            parts.append("<ol>" + "".join(f'<li>{html.escape(value)}</li>' for value in item["items"]) + "</ol>")
        parts.append("</aside>")
        rendered.append("".join(parts))
    return "".join(rendered)
