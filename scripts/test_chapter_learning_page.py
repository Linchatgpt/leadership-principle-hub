import json
import pathlib
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from update_chapter_learning_page import render_case, render_questions


class ChapterLearningPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "content" / "chapter_03_learning.json").read_text(encoding="utf-8"))

    def test_case_has_three_prompts_and_one_workspace(self):
        rendered = render_case(self.data["case"])
        self.assertEqual(rendered.count('<div><span>'), 2)
        self.assertEqual(rendered.count('<textarea data-key="caseAnswer">'), 1)
        for prompt in self.data["case"]["questions"]:
            self.assertIn(prompt, rendered)

    def test_assessment_has_twelve_unique_questions_and_four_dimensions(self):
        questions = self.data["assessment"]["questions"]
        self.assertEqual(len(questions), 12)
        self.assertEqual(len({text for _, text in questions}), 12)
        self.assertEqual(set(self.data["assessment"]["dimensions"]), {dimension for dimension, _ in questions})
        rendered = render_questions(questions)
        self.assertEqual(rendered.count('<fieldset class="q"'), 12)
        self.assertEqual(rendered.count('<legend>'), 12)
        self.assertEqual(rendered.count('type="radio"'), 60)

    def test_assessment_accessibility_contract_is_shared_by_first_three_chapters(self):
        for chapter in (1, 2, 3):
            page = BeautifulSoup(
                (ROOT / f"LPI_Coach_Chapter{chapter:02d}.html").read_text(encoding="utf-8"),
                "html.parser",
            )
            self.assertEqual(len(page.select("#s3 fieldset.q")), 12)
            self.assertEqual(len(page.select("#s3 fieldset.q > legend")), 12)
            self.assertIsNotNone(page.select_one("#assessmentProgress[aria-live='polite']"))
            self.assertIsNotNone(page.select_one("#assessmentMessageTop[role='alert']"))
            self.assertIsNotNone(page.select_one("#assessmentMessage[role='alert']"))

    def test_privacy_nudge_appears_before_the_first_case_textarea(self):
        for chapter in (1, 2, 3):
            page = BeautifulSoup(
                (ROOT / f"LPI_Coach_Chapter{chapter:02d}.html").read_text(encoding="utf-8"),
                "html.parser",
            )
            question = page.select_one("#s2 .question")
            nudge = question.select_one(".privacy-nudge")
            textarea = question.select_one("textarea")
            self.assertIsNotNone(nudge)
            self.assertIn("去識別化", nudge.get_text())
            self.assertLess(str(question).find(str(nudge)), str(question).find(str(textarea)))

    def test_runtime_and_css_include_requested_assessment_behaviors(self):
        runtime = (ROOT / "assets" / "chapter-runtime.js").read_text(encoding="utf-8")
        css = (ROOT / "assets" / "chapter.css").read_text(encoding="utf-8")
        self.assertIn("已完成 ", runtime)
        self.assertIn("assessmentMessageTop", runtime)
        self.assertIn("firstMissing.focus", runtime)
        self.assertIn("四項目前相近，請依工作情境選擇", runtime)
        self.assertIn("min-width:44px", css)
        self.assertIn("min-height:44px", css)
        self.assertIn(".rating input:focus-visible+span", css)

    def test_action_commitment_matches_work_record_structure(self):
        for chapter in (1, 2, 3):
            page = BeautifulSoup(
                (ROOT / f"LPI_Coach_Chapter{chapter:02d}.html").read_text(encoding="utf-8"),
                "html.parser",
            )
            self.assertIsNotNone(page.select_one("#s4 > .head"))
            self.assertIsNotNone(page.select_one("#s4 > .simple-record"))
            self.assertIsNotNone(page.select_one("#s5 > .head"))
            self.assertIsNotNone(page.select_one("#s5 > .simple-record.action-commitment"))
            self.assertIsNotNone(page.select_one("#s5 .action-commitment > label > textarea[data-key='experiment']"))
            self.assertIsNotNone(page.select_one("#s5 .action-date > input[data-key='followupDate']"))

        css = (ROOT / "assets" / "chapter.css").read_text(encoding="utf-8")
        self.assertIn(".action-commitment{background:#f7efe2;border-left-color:var(--gold)}", css)
        self.assertNotIn("#s5 > .experiment", css)

    def test_chapter_three_embeds_the_current_shared_styles(self):
        page = BeautifulSoup((ROOT / "LPI_Coach_Chapter03.html").read_text(encoding="utf-8"), "html.parser")
        template = (ROOT / "templates" / "chapter_template.html").read_text(encoding="utf-8")
        brand_rule = template.split("{{CSS}}", 1)[1].split("</style>", 1)[0]
        expected = (
            "\n"
            + (ROOT / "assets" / "chapter.css").read_text(encoding="utf-8")
            + (ROOT / "assets" / "editor-runtime.css").read_text(encoding="utf-8")
            + brand_rule
        )
        self.assertEqual(page.style.get_text(), expected)

    def test_chapter_three_has_the_three_pre_reading_entry_blocks(self):
        self.assertIn("start_prompt", self.data)
        self.assertIn("orientation", self.data)
        self.assertEqual(len(self.data.get("quick_scan", [])), 3)
        page = BeautifulSoup((ROOT / "LPI_Coach_Chapter03.html").read_text(encoding="utf-8"), "html.parser")
        hero = page.select_one("#s0")
        self.assertEqual(len(hero.select(":scope > .dark")), 1)
        reading_children = [
            " ".join(node.get("class", [])) if node.get("class") else node.name
            for node in page.select_one("#s1").find_all(recursive=False)
        ]
        self.assertEqual(reading_children[:4], ["head", "reading-brief", "quick-scan", "reading-essay"])
        self.assertEqual(len(page.select(".quick-scan-question")), 3)
        runtime = (ROOT / "assets" / "chapter-runtime.js").read_text(encoding="utf-8")
        self.assertIn("const quickScan", runtime)
        self.assertIn('delete data["quick_"+i]', runtime)

    def test_chapters_one_and_two_have_distinct_complete_reading_entries(self):
        entries = []
        for chapter in (1, 2):
            data = json.loads(
                (ROOT / "content" / f"chapter_{chapter:02d}_learning.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(data["orientation"]["items"]), 4)
            self.assertEqual(len(data["quick_scan"]), 3)
            self.assertTrue(all(len(question["options"]) == 2 for question in data["quick_scan"]))
            page = BeautifulSoup(
                (ROOT / f"LPI_Coach_Chapter{chapter:02d}.html").read_text(encoding="utf-8"),
                "html.parser",
            )
            self.assertEqual(len(page.select("#s0 > .dark")), 1)
            children = [
                " ".join(node.get("class", [])) if node.get("class") else node.name
                for node in page.select_one("#s1").find_all(recursive=False)
            ]
            self.assertEqual(children[:4], ["head", "reading-brief", "quick-scan", "reading-essay"])
            self.assertEqual(len(page.select(".quick-scan-question")), 3)
            entries.append(json.dumps(data, ensure_ascii=False, sort_keys=True))
        self.assertNotEqual(entries[0], entries[1])

    def test_chapter_two_has_model_the_way_specific_assessment(self):
        data = json.loads((ROOT / "content" / "chapter_02_learning.json").read_text(encoding="utf-8"))
        assessment = data["assessment"]
        expected_dimensions = {"價值澄清", "行動一致", "壓力回應", "回饋修復"}
        self.assertEqual(set(assessment["dimensions"]), expected_dimensions)
        self.assertEqual(len(assessment["questions"]), 12)
        self.assertEqual(len({text for _, text in assessment["questions"]}), 12)
        self.assertEqual({dimension for dimension, _ in assessment["questions"]}, expected_dimensions)
        self.assertEqual(set(assessment["focus_tips"]), expected_dimensions)


if __name__ == "__main__":
    unittest.main()
