import json
import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SplitContractTests(unittest.TestCase):
    def test_root_and_index_match_configured_module_range(self):
        config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
        start, end = config["module_range"]
        expected = {f"LPI_Coach_Chapter{n:02d}.html" for n in range(start, end + 1)}
        actual = {path.name for path in ROOT.glob("LPI_Coach_Chapter*.html")}
        self.assertEqual(actual, expected)
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        linked = set(re.findall(r'href="(LPI_Coach_Chapter\d{2}\.html)"', index))
        self.assertEqual(linked, expected)
        self.assertIn(f'<b>{len(expected)} 個模組</b>', index)

    def test_admin_lists_only_configured_modules(self):
        config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
        start, end = config["module_range"]
        admin = (ROOT / "admin.html").read_text(encoding="utf-8")
        listed = {int(n) for n in re.findall(r'>Module (\d{2})｜', admin)}
        self.assertEqual(listed, set(range(start, end + 1)))


if __name__ == "__main__":
    unittest.main()
