import pathlib
import re
import unittest
from html.parser import HTMLParser


ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN = ("本書", "培養卓越領導者的教練指南", "James", "Kouzes", "Posner", "Biech")


class ReadingTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "div" and "reading-essay" in attributes.get("class", "").split():
            self.depth = 1
        elif self.depth:
            self.depth += 1

    def handle_endtag(self, _tag):
        if self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)


def page_text(path: pathlib.Path) -> str:
    return re.sub(r"<[^>]+>", "", path.read_text(encoding="utf-8"))


def rendered_reading_length(path: pathlib.Path) -> int:
    parser = ReadingTextParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return len(re.sub(r"\s", "", "".join(parser.text)))


def style_block(path: pathlib.Path) -> str:
    source = path.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*?)</style>", source, flags=re.S)
    if not match:
        raise AssertionError(f"Missing style block in {path.name}")
    return match.group(1)


class HomeAndChaptersNormalizationTests(unittest.TestCase):
    def test_home_is_source_neutral_and_links_each_canonical_page_once(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        visible = page_text(ROOT / "index.html")
        for term in FORBIDDEN:
            self.assertNotIn(term, visible)
        self.assertIn('lang="zh-Hant"', home)
        self.assertIn('font-family:"Noto Sans TC"', home)
        for chapter in range(1, 4):
            self.assertEqual(home.count(f'href="LPI_Coach_Chapter{chapter:02d}.html"'), 1)

    def test_home_generator_cannot_restore_source_book_copy(self):
        builder = (ROOT / "scripts" / "build_chapters.py").read_text(encoding="utf-8")
        learner_copy = builder.split("custom='''", 1)[1]
        for term in FORBIDDEN:
            self.assertNotIn(term, learner_copy)

    def test_root_contains_only_canonical_chapter_html_names(self):
        noncanonical = [
            path.name for path in ROOT.glob("LPI_Coach_Chapter*.html")
            if not re.fullmatch(r"LPI_Coach_Chapter\d{2}\.html", path.name)
        ]
        self.assertEqual(noncanonical, [])

    def test_chapters_share_style_and_latest_structure(self):
        pages = [ROOT / f"LPI_Coach_Chapter{chapter:02d}.html" for chapter in range(1, 4)]
        styles = [style_block(page) for page in pages]
        self.assertTrue(all(style == styles[0] for style in styles[1:]))
        for page in pages:
            source = page.read_text(encoding="utf-8")
            self.assertEqual(source.count('class="brand" href="index.html"'), 1)
            self.assertIn('font-family: "Noto Sans TC"', source)
            self.assertRegex(source, r'<div class="journey-plan">.*?<div class="dark">')
            self.assertRegex(
                source,
                r'<section id="s1"><div class="head">.*?</div><aside class="reading-brief".*?</aside><details class="quick-scan".*?</details><div class="reading-essay">',
            )
            self.assertIn('<fieldset class="q" tabindex="-1">', source)
            self.assertIn('id="assessmentProgress"', source)
            self.assertIn('<section id="s4"><div class="head">', source)
            self.assertIn('<section id="s5"><div class="head">', source)
            self.assertIn('<div class="simple-record action-commitment">', source)

    def test_shared_body_font_prefers_noto_sans_tc(self):
        stylesheet = (ROOT / "assets" / "chapter.css").read_text(encoding="utf-8")
        self.assertRegex(
            stylesheet,
            r'body\{[^}]*font-family:"Noto Sans TC",Arial,sans-serif',
        )

    def test_each_deep_reading_has_at_least_5000_rendered_characters(self):
        counts = {
            chapter: rendered_reading_length(ROOT / f"LPI_Coach_Chapter{chapter:02d}.html")
            for chapter in range(1, 4)
        }
        self.assertTrue(all(count >= 5000 for count in counts.values()), counts)

    def test_chapters_are_source_neutral_and_storage_keys_stay_stable(self):
        expected_keys = {
            1: "LPI_CoachChapter1",
            2: "LPI_CoachChapter2",
            3: "LPI_CoachChapter3",
        }
        for chapter, key in expected_keys.items():
            page = ROOT / f"LPI_Coach_Chapter{chapter:02d}.html"
            source = page.read_text(encoding="utf-8")
            visible = page_text(page)
            for term in FORBIDDEN:
                self.assertNotIn(term, visible)
            self.assertIn(f'"storage_key": "{key}"', source)


if __name__ == "__main__":
    unittest.main()
