import pathlib
import re
import sys

from chapter_callouts import load_chapter_callouts, render_chapter_callouts


ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = "LPI_Coach"


def update_chapter(chapter: int) -> pathlib.Path:
    page = ROOT / f"{PREFIX}_Chapter{chapter:02d}.html"
    source = page.read_text(encoding="utf-8")
    replacement = render_chapter_callouts(load_chapter_callouts(ROOT, chapter))
    pattern = r'(</section>)(?:<aside class="reading-callout">.*?</aside>){3}(<section id="s1">)'
    updated, count = re.subn(pattern, rf'\1{replacement}\2', source, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f"Could not locate the three pre-reading callouts in {page}")
    page.write_text(updated, encoding="utf-8")
    return page


if __name__ == "__main__":
    chapters = [int(value) for value in sys.argv[1:]]
    if not chapters:
        raise SystemExit("Usage: python3 scripts/update_chapter_callouts.py CHAPTER [CHAPTER ...]")
    for chapter_number in chapters:
        print(update_chapter(chapter_number))
