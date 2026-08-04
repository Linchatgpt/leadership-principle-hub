import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]


def configure() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    start, end = config["module_range"]
    index_path = ROOT / "index.html"
    index = index_path.read_text(encoding="utf-8")
    cards = re.findall(r'<a class="map-card".*?</a>', index, flags=re.S)
    selected = [card for card in cards if any(f"MODULE {n:02d}" in card for n in range(start, end + 1))]
    index = re.sub(
        r'(<div class="map">).*?(</div></section>)',
        lambda match: match.group(1) + "".join(selected) + match.group(2),
        index,
        count=1,
        flags=re.S,
    )
    index = re.sub(r'<b>\d+ (?:章|個模組)</b>', f'<b>{len(selected)} 個模組</b>', index, count=1)
    index = re.sub(r'<h2>選一章，帶一個真實議題進來。</h2>', f'<h2>{config["home_map_heading"]}</h2>', index, count=1)
    index = re.sub(r'<section class="home-hero">(.*?)<p>.*?</p>', lambda m: '<section class="home-hero">' + m.group(1) + f'<p>{config["home_intro"]}</p>', index, count=1, flags=re.S)
    index = index.replace("開始本章 →", "開始本模組 →")
    index_path.write_text(index, encoding="utf-8")

    admin_path = ROOT / "admin.html"
    admin = admin_path.read_text(encoding="utf-8")
    admin = re.sub(
        r'<option value="LPI_Coach_Chapter(\d{2})\.html">.*?</option>',
        lambda m: m.group(0) if start <= int(m.group(1)) <= end else "",
        admin,
    )
    admin_path.write_text(admin, encoding="utf-8")


if __name__ == "__main__":
    configure()
