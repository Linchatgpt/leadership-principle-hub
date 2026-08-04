import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from chapter_callouts import load_chapter_callouts, render_chapter_callouts


class ChapterCalloutsTest(unittest.TestCase):
    def test_first_two_chapters_have_distinct_callout_content(self):
        chapter_1 = load_chapter_callouts(ROOT, 1)
        chapter_2 = load_chapter_callouts(ROOT, 2)

        self.assertEqual([item["label"] for item in chapter_1], ["概念說明", "專有名詞解釋", "工具箱專欄"])
        self.assertEqual([item["label"] for item in chapter_2], ["概念說明", "專有名詞解釋", "工具箱專欄"])
        self.assertNotEqual([item["title"] for item in chapter_1], [item["title"] for item in chapter_2])
        self.assertNotEqual(render_chapter_callouts(chapter_1), render_chapter_callouts(chapter_2))

    def test_renderer_escapes_text_and_supports_lists(self):
        html = render_chapter_callouts([
            {"label": "工具箱專欄", "title": "A < B", "paragraphs": ["安全 & 清楚"], "items": ["一 < 二"]}
        ])

        self.assertIn("A &lt; B", html)
        self.assertIn("安全 &amp; 清楚", html)
        self.assertIn("<ol><li>一 &lt; 二</li></ol>", html)


if __name__ == "__main__":
    unittest.main()
