import argparse
import hashlib
import pathlib
import re
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from update_site_shell import FOOTER


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "LPI_Coach_Chapter03.html"
OUTPUT_PATH = ROOT / "experiments" / "chapter03-royal" / "LPI_Coach_Chapter03_Royal.html"
ROYAL_STYLESHEET = '<link rel="stylesheet" href="chapter03-royal.css">'
ROYAL_SITE_STYLESHEET = '<link rel="stylesheet" href="../../assets/site-shell.css">'


def replace_once(source: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1)
    if count != 1:
        raise ValueError(f"Could not find the expected {label}")
    return updated


def build_royal_html(source: str) -> str:
    royal_markers = (
        "royal-chapter" in source,
        ROYAL_STYLESHEET in source,
        "LPI_CoachChapter3RoyalV2" in source,
    )
    if all(royal_markers):
        shared_markers = (
            ROYAL_SITE_STYLESHEET in source,
            'class="site-footer"' in source,
        )
        if not all(shared_markers):
            raise ValueError("Royal chapter shared shell is incomplete")
        return source
    if any(royal_markers):
        raise ValueError("Royal chapter markers are only partially present")

    result = replace_once(
        source,
        r"<title>啟發共同願景｜(?:Leadership Hub|卓越領導力©核心課程)</title>",
        "<title>啟發共同願景｜皇家知識沙龍</title>",
        "Chapter 03 title",
    )
    result = replace_once(
        result,
        r"</head>",
        f"{ROYAL_STYLESHEET}{ROYAL_SITE_STYLESHEET}</head>",
        "closing head tag",
    )
    result = replace_once(
        result,
        r'<body(?:\s+class="chapter-page")?>',
        '<body class="chapter-page royal-chapter">',
        "body tag",
    )
    result = replace_once(
        result,
        r'"storage_key"\s*:\s*"LPI_CoachChapter3"',
        '"storage_key":"LPI_CoachChapter3RoyalV2"',
        "Chapter 03 storage key",
    )
    result = replace_once(
        result,
        r'href="index\.html"',
        'href="../../index.html"',
        "homepage return link",
    )
    result = result.replace('<link rel="stylesheet" href="assets/site-shell.css">', "", 1)
    if 'class="site-footer"' not in result:
        result = replace_once(result, r"</body>", f"{FOOTER}</body>", "closing body tag")
    return result


def build(source_path: pathlib.Path = SOURCE_PATH, output_path: pathlib.Path = OUTPUT_PATH) -> pathlib.Path:
    before = source_path.read_bytes()
    source_hash = hashlib.sha256(before).hexdigest()
    output = build_royal_html(before.decode("utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    after_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if after_hash != source_hash:
        raise RuntimeError("The original Chapter 03 file changed during the Royal build")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the standalone Royal Chapter 03 variant")
    parser.add_argument("--source", type=pathlib.Path, default=SOURCE_PATH)
    parser.add_argument("--output", type=pathlib.Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    built = build(args.source, args.output)
    print(built)


if __name__ == "__main__":
    main()
