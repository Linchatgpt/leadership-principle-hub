#!/usr/bin/env python3
import unittest

from deep_reading_renderer import render_deep_reading_markdown, replace_deep_reading_article


class DeepReadingRendererTests(unittest.TestCase):
    def test_renders_article_structure_and_tools(self):
        source = """# 文章標題

導言｜這是一段導言。

## 一、第一節

這是含有**重點**的正文。

### 工具一｜行動卡

1. **場景：**在哪裡？
2. **動作：**做什麼？

> **停下來想一想｜第一個反應**  
> 先辨識自己的反應。

## 總結提要

1. 第一項總結。
"""
        rendered = render_deep_reading_markdown(source)
        self.assertNotIn("<h1", rendered)
        self.assertIn("<p><b>導言｜</b>這是一段導言。</p>", rendered)
        self.assertIn("<h3>一、第一節</h3>", rendered)
        self.assertIn('<div class="reading-tool">', rendered)
        self.assertIn('<span class="tool-label">工具一</span>', rendered)
        self.assertIn("<h3>行動卡</h3>", rendered)
        self.assertIn("<ol>", rendered)
        self.assertIn('<div class="reading-pause">', rendered)
        self.assertIn('<div class="reading-summary">', rendered)
        self.assertTrue(rendered.count("<div") == rendered.count("</div>"))

    def test_escapes_raw_html(self):
        rendered = render_deep_reading_markdown("# 標題\n\n<script>alert(1)</script>")
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_replaces_only_reading_article(self):
        page = (
            '<aside class="reading-callout">保留</aside><section id="s1">'
            '<div class="reading-essay"><p>舊文</p></div></section>'
            '<section id="s2"><p>案例保留</p></section>'
        )
        updated = replace_deep_reading_article(page, "<p>新文</p>")
        self.assertIn("reading-callout\">保留", updated)
        self.assertIn('<div class="reading-essay"><p>新文</p></div>', updated)
        self.assertIn("案例保留", updated)
        self.assertNotIn("舊文", updated)


if __name__ == "__main__":
    unittest.main()
