import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ChapterIntroductionTests(unittest.TestCase):
    def test_first_two_chapter_drafts_have_labeled_introduction(self):
        for chapter in (1, 2):
            draft = ROOT / "reference_materials" / "chapters" / f"chapter_{chapter:02d}" / "02_deep_reading_draft.md"
            paragraphs = [part.strip() for part in draft.read_text(encoding="utf-8").split("\n\n")]
            self.assertTrue(
                any(paragraph.startswith("導言｜") for paragraph in paragraphs[:3]),
                f"Chapter {chapter:02d} must start with a labeled introduction",
            )
            self.assertTrue(
                paragraphs[2].startswith("## "),
                f"Chapter {chapter:02d} must have only one introduction paragraph before the first section",
            )

    def test_chapter_two_introduction_uses_desktop_target_length(self):
        draft = ROOT / "reference_materials" / "chapters" / "chapter_02" / "02_deep_reading_draft.md"
        introduction = next(
            part.strip().removeprefix("導言｜")
            for part in draft.read_text(encoding="utf-8").split("\n\n")
            if part.strip().startswith("導言｜")
        )
        self.assertGreaterEqual(len(introduction), 180)
        self.assertLessEqual(len(introduction), 260)


if __name__ == "__main__":
    unittest.main()
