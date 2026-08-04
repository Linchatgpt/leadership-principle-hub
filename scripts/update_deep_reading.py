#!/usr/bin/env python3
import argparse
from pathlib import Path

from deep_reading_renderer import render_deep_reading_markdown, replace_deep_reading_article


ROOT = Path(__file__).resolve().parents[1]


def update_chapter(chapter):
    draft = ROOT / "reference_materials" / "chapters" / f"chapter_{chapter:02d}" / "02_deep_reading_draft.md"
    page = ROOT / f"LPI_Coach_Chapter{chapter:02d}.html"
    if not draft.exists():
        raise FileNotFoundError(f"missing approved draft: {draft}")
    if not page.exists():
        raise FileNotFoundError(f"missing chapter page: {page}")
    article = render_deep_reading_markdown(draft.read_text(encoding="utf-8"))
    updated = replace_deep_reading_article(page.read_text(encoding="utf-8"), article)
    temporary = page.with_suffix(".html.tmp")
    temporary.write_text(updated, encoding="utf-8")
    temporary.replace(page)
    print(f"updated {page.name} from {draft.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chapters", nargs="+", type=int)
    args = parser.parse_args()
    for chapter in args.chapters:
        update_chapter(chapter)


if __name__ == "__main__":
    main()
