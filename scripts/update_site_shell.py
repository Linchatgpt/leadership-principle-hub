import pathlib
import re
import json


ROOT = pathlib.Path(__file__).resolve().parents[1]
ABOUT_URL = "https://leading4elite.com/about_wesley/"
GMAIL_URL = "https://mail.google.com/mail/?view=cm&fs=1&to=wesley.lin@leading4elite.com"
LEGACY_BRAND_NAMES = ("卓越領導者教練學習中心", "卓越領導力學習中心")
BRAND_NAME = "卓越領導力©核心課程"
STYLESHEET = '<link rel="stylesheet" href="assets/site-shell.css">'
FOOTER = (
    '<footer class="site-footer"><div class="site-footer__inner">'
    '<span>精萃領導™學習中心</span>'
    f'<a href="{ABOUT_URL}" target="_blank" rel="noopener noreferrer">林祖威教練</a>'
    f'<a href="{GMAIL_URL}" target="_blank" rel="noopener noreferrer">wesley.lin@leading4elite.com</a>'
    '</div></footer>'
)


def update_page(source: str, *, home: bool = False) -> str:
    for old_name in LEGACY_BRAND_NAMES:
        source = source.replace(f'<i>LPI</i> {old_name}', f'<i>XL</i> {BRAND_NAME}')
        source = source.replace(f'<i>XL</i> {old_name}', f'<i>XL</i> {BRAND_NAME}')
        source = source.replace(old_name, BRAND_NAME)
    if home:
        source = re.sub(r"<title>.*?</title>", f"<title>{BRAND_NAME}</title>", source, count=1)
    else:
        source = source.replace("｜Leadership Hub</title>", f"｜{BRAND_NAME}</title>")

    if STYLESHEET not in source:
        source = source.replace("</head>", f"{STYLESHEET}</head>", 1)

    if home:
        source = re.sub(
            r'<section class="home-note">.*?</section>',
            "",
            source,
            count=1,
            flags=re.S,
        )
        source = source.replace("<body>", '<body class="home-page">', 1)
    else:
        source = re.sub(r'<body(?:\s+class="[^"]*")?>', '<body class="chapter-page">', source, count=1)

    source, count = re.subn(r"<footer(?:\s[^>]*)?>.*?</footer>", FOOTER, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError("Could not replace the page footer")
    return source


def update_all() -> list[pathlib.Path]:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    module_start, module_end = config.get("module_range", [1, 11])
    pages = [ROOT / "index.html"] + [
        ROOT / f"LPI_Coach_Chapter{chapter:02d}.html" for chapter in range(module_start, module_end + 1)
    ]
    for page in pages:
        updated = update_page(page.read_text(encoding="utf-8"), home=page.name == "index.html")
        page.write_text(updated, encoding="utf-8")
    return pages


if __name__ == "__main__":
    for updated_page in update_all():
        print(updated_page)
