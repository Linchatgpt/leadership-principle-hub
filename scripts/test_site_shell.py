import pathlib
import re
import unittest
from bs4 import BeautifulSoup


ROOT = pathlib.Path(__file__).resolve().parents[1]
ABOUT_URL = "https://leading4elite.com/about_wesley/"
GMAIL_URL = "https://mail.google.com/mail/?view=cm&fs=1&to=wesley.lin@leading4elite.com"
CONFIG = __import__("json").loads((ROOT / "config.json").read_text(encoding="utf-8"))
MODULE_START, MODULE_END = CONFIG.get("module_range", [1, 11])


class SiteShellTests(unittest.TestCase):
    def test_home_brand_uses_the_same_left_alignment_formula_as_home_content(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        shell_css = (ROOT / "assets" / "site-shell.css").read_text(encoding="utf-8")
        self.assertIn('class="home-page"', home)
        self.assertIn('href="assets/site-shell.css"', home)
        self.assertIn("calc((100% - 1100px)/2 + 6%)", shell_css)
        self.assertRegex(shell_css, r"\.home-page \.top\s*\{[^}]*padding-left:\s*max\(6%, calc\(\(100% - 1100px\)/2 \+ 6%\)\)")

    def test_home_and_all_canonical_chapters_use_the_shared_contact_footer(self):
        pages = [ROOT / "index.html"] + [
            ROOT / f"LPI_Coach_Chapter{chapter:02d}.html" for chapter in range(MODULE_START, MODULE_END + 1)
        ]
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.name):
                self.assertEqual(source.count('class="site-footer"'), 1)
                self.assertIn("精萃領導™學習中心", source)
                self.assertIn(f'href="{ABOUT_URL}"', source)
                self.assertIn(">林祖威教練</a>", source)
                self.assertIn(f'href="{GMAIL_URL}"', source)
                self.assertIn(">wesley.lin@leading4elite.com</a>", source)
                self.assertIn('target="_blank"', source)
                self.assertIn('rel="noopener noreferrer"', source)
                self.assertNotIn('site-footer__separator', source)

    def test_chapter_brand_aligns_with_the_left_rail_and_footer_text_is_doubled(self):
        shell_css = (ROOT / "assets" / "site-shell.css").read_text(encoding="utf-8")
        updater = (ROOT / "scripts" / "update_site_shell.py").read_text(encoding="utf-8")
        chapter = (ROOT / f"LPI_Coach_Chapter{MODULE_START:02d}.html").read_text(encoding="utf-8")
        self.assertIn('class="chapter-page"', chapter)
        self.assertIn("calc((100% - 1220px)/2 + 25px)", shell_css)
        self.assertRegex(shell_css, r"\.chapter-page \.top\s*\{[^}]*padding-left:")
        self.assertRegex(shell_css, r"\.site-footer\s*\{[^}]*font:\s*22px/")
        self.assertNotIn("site-footer__separator", updater)

    def test_every_page_uses_the_updated_brand_name_and_logo(self):
        pages = [ROOT / "index.html"] + [
            ROOT / f"LPI_Coach_Chapter{chapter:02d}.html" for chapter in range(MODULE_START, MODULE_END + 1)
        ]
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.name):
                self.assertIn('<i>XL</i> 卓越領導力©核心課程', source)
                if page.name == "index.html":
                    self.assertIn('<title>卓越領導力©核心課程</title>', source)
                else:
                    self.assertIn('｜卓越領導力©核心課程</title>', source)
                self.assertNotIn('卓越領導力學習中心', source)
                self.assertNotIn('<i>LPI</i>', source)
                self.assertNotIn('卓越領導者教練學習中心', source)

    def test_home_no_longer_contains_the_old_notice_section(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("使用前請知道", home)
        self.assertNotIn('class="home-note"', home)

    def test_visible_chapter_labels_are_module_labels(self):
        pages = [ROOT / "index.html"] + [
            ROOT / f"LPI_Coach_Chapter{chapter:02d}.html" for chapter in range(MODULE_START, MODULE_END + 1)
        ]
        for page in pages:
            soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
            for hidden in soup.select("script, style"):
                hidden.decompose()
            visible = soup.get_text(" ", strip=True)
            with self.subTest(page=page.name):
                self.assertNotRegex(visible, r"\bCHAPTER\b|\bChapter\b")
                self.assertRegex(visible, r"\bMODULE\b|\bModule\b")

    def test_generators_preserve_header_alignment_and_shared_footer(self):
        builder = (ROOT / "scripts" / "build_chapters.py").read_text(encoding="utf-8")
        shell_css = (ROOT / "assets" / "site-shell.css").read_text(encoding="utf-8")
        shell_updater = (ROOT / "scripts" / "update_site_shell.py").read_text(encoding="utf-8")
        index_template = (ROOT / "templates" / "index_template.html").read_text(encoding="utf-8")
        chapter_template = (ROOT / "templates" / "chapter_template.html").read_text(encoding="utf-8")
        self.assertIn("calc((100% - 1100px)/2 + 6%)", shell_css)
        self.assertIn("from update_site_shell import FOOTER", builder)
        self.assertIn('class="site-footer"', shell_updater)
        self.assertIn(ABOUT_URL, shell_updater)
        self.assertIn(GMAIL_URL, shell_updater)
        self.assertIn('href="assets/site-shell.css"', index_template)
        self.assertIn('href="assets/site-shell.css"', chapter_template)


if __name__ == "__main__":
    unittest.main()
