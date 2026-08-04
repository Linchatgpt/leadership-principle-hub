import importlib.util
import json
import pathlib
import unittest

from bs4 import BeautifulSoup


ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts" / "build_chapter03_royal.py"
SOURCE_PATH = ROOT / "LPI_Coach_Chapter03.html"
ROYAL_PATH = ROOT / "experiments" / "chapter03-royal" / "LPI_Coach_Chapter03_Royal.html"


def load_builder():
    if not BUILDER_PATH.exists():
        raise AssertionError("Royal builder has not been implemented")
    spec = importlib.util.spec_from_file_location("build_chapter03_royal", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Chapter03RoyalTests(unittest.TestCase):
    def test_builder_preserves_learning_content_and_isolates_storage(self):
        builder = load_builder()
        source = (
            '<!doctype html><html lang="zh-Hant"><head>'
            '<title>啟發共同願景｜Leadership Hub</title></head><body>'
            '<a class="brand" href="index.html">學習中心</a>'
            '<main><section id="s1"><p>共同願景測試內容</p></section></main>'
            '<script id="chapter-config" type="application/json">'
            '{"storage_key":"LPI_CoachChapter3","questions":[["願景表達","測試題目"]]}'
            '</script></body></html>'
        )

        result = builder.build_royal_html(source)

        self.assertIn("共同願景測試內容", result)
        self.assertIn('body class="chapter-page royal-chapter"', result)
        self.assertIn('href="chapter03-royal.css"', result)
        self.assertIn('href="../../assets/site-shell.css"', result)
        self.assertIn('href="../../index.html"', result)
        self.assertIn('class="site-footer"', result)
        self.assertIn('href="https://leading4elite.com/about_wesley/"', result)
        self.assertIn('href="https://mail.google.com/mail/?view=cm&fs=1&to=wesley.lin@leading4elite.com"', result)
        self.assertIn('"storage_key":"LPI_CoachChapter3RoyalV2"', result)
        self.assertNotIn('"storage_key":"LPI_CoachChapter3"', result)
        self.assertEqual(builder.build_royal_html(result), result)

    def test_generated_page_keeps_the_complete_chapter_contract(self):
        if not ROYAL_PATH.exists():
            self.fail("Royal chapter page has not been generated")

        source = BeautifulSoup(SOURCE_PATH.read_text(encoding="utf-8"), "html.parser")
        royal = BeautifulSoup(ROYAL_PATH.read_text(encoding="utf-8"), "html.parser")
        source_config = json.loads(source.select_one("#chapter-config").get_text())
        royal_config = json.loads(royal.select_one("#chapter-config").get_text())

        self.assertEqual([node.get("id") for node in source.select("main section[id]")],
                         [node.get("id") for node in royal.select("main section[id]")])
        self.assertEqual(source.select_one("main").get_text(" ", strip=True),
                         royal.select_one("main").get_text(" ", strip=True))
        self.assertEqual(source_config["questions"], royal_config["questions"])
        self.assertEqual(source_config["quick_scan"], royal_config["quick_scan"])
        self.assertEqual(royal_config["storage_key"], "LPI_CoachChapter3RoyalV2")
        self.assertEqual(len(royal.select("#s3 fieldset.q")), 12)
        self.assertEqual(len(royal.select(".quick-scan-question")), 3)
        self.assertIsNotNone(royal.select_one('link[href="../../assets/site-shell.css"]'))
        self.assertIsNotNone(royal.select_one("footer.site-footer"))


if __name__ == "__main__":
    unittest.main()
