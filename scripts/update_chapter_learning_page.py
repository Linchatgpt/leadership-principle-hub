import html
import json
import pathlib
import re
import sys

from chapter_callouts import load_chapter_callouts, render_chapter_callouts
from deep_reading_renderer import render_deep_reading_markdown, replace_deep_reading_article


ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = "LPI_Coach"


def render_case(data: dict) -> str:
    paragraphs = "".join(f"<p>{html.escape(p)}</p>" for p in data["paragraphs"])
    contrasts = "".join(
        '<div><span>{}</span><h3>{}</h3><p>{}</p></div>'.format(
            html.escape(item["label"]), html.escape(item["title"]), html.escape(item["text"])
        ) for item in data["contrasts"]
    )
    questions = "".join(f"<p>{i}. {html.escape(q)}</p>" for i, q in enumerate(data["questions"], 1))
    return (
        '<section id="s2"><div class="head"><small class="kicker">02 LOCAL CASE</small>'
        f'<h2>工作案例</h2><p>{html.escape(data["intro"])}</p></div>'
        f'<div class="story">{paragraphs}</div><div class="case-contrast">{contrasts}</div>'
        f'<div class="question"><b>三個提問</b>{questions}'
        '<p class="privacy-nudge"><b>書寫提醒：</b>請將人物與事件去識別化，不要輸入姓名、客戶名稱或其他可辨識資訊。</p>'
        '<label>你的整理<textarea data-key="caseAnswer"></textarea></label></div></section>'
    )


def render_questions(questions: list[list[str]]) -> str:
    blocks = []
    for index, (dimension, question) in enumerate(questions):
        ratings = "".join(
            f'<label><input type="radio" name="q{index}" value="{value}"><span>{value}</span></label>'
            for value in range(1, 6)
        )
        blocks.append(
            f'<fieldset class="q" tabindex="-1"><legend><b>{index + 1}.</b> {html.escape(question)}</legend>'
            f'<small>{html.escape(dimension)}｜最近 30 天</small><div class="rating" aria-label="1 代表幾乎沒有，5 代表經常如此">{ratings}</div></fieldset>'
        )
    return "".join(blocks)


def render_action_commitment() -> str:
    return (
        '<section id="s5"><div class="head"><small class="kicker">05 ACTION COMMITMENT</small>'
        '<h2>行動承諾</h2><p>只選一個小到能在工作現場完成的行動，寫下時間與場景。</p></div>'
        '<div class="simple-record action-commitment">'
        '<div id="experimentFocus" class="experiment-focus">尚未選擇發展焦點</div>'
        '<label>我的行動<textarea data-key="experiment"></textarea></label>'
        '<label class="action-date">預計實行日期 <input type="date" data-key="followupDate"></label>'
        '</div></section>'
    )


def render_start_prompt(data: dict) -> str:
    return (
        '<div class="dark"><small>{}</small><h3>{}</h3><p>{}</p>'
        '<textarea data-key="startPrompt" placeholder="{}"></textarea></div>'
    ).format(*(html.escape(data[key]) for key in ("label", "title", "text", "placeholder")))


def render_orientation(data: dict) -> str:
    items = "".join(f"<li>{html.escape(item)}</li>" for item in data["items"])
    return (
        '<aside class="reading-brief" aria-labelledby="reading-brief-title">'
        f'<span class="brief-label">{html.escape(data["label"])}</span>'
        f'<h3 id="reading-brief-title">{html.escape(data["title"])}</h3>'
        f'<p>{html.escape(data["text"])}</p><ul>{items}</ul></aside>'
    )


def render_quick_scan(items: list[dict]) -> str:
    questions = []
    for question_index, item in enumerate(items):
        buttons = "".join(
            f'<button type="button" data-option="{option_index}" aria-pressed="false">{html.escape(option["text"])}</button>'
            for option_index, option in enumerate(item["options"])
        )
        questions.append(
            f'<article class="quick-scan-question" data-question="{question_index}">'
            f'<h4>{question_index + 1}. {html.escape(item["question"])}</h4>'
            f'<div class="quick-scan-options">{buttons}</div>'
            '<p class="quick-scan-feedback" hidden aria-live="polite"></p></article>'
        )
    return (
        '<details class="quick-scan"><summary><span><small>BEFORE YOU READ</small>'
        '課前情境快問快答（3題）</span><span>點擊展開／收起</span></summary>'
        '<div class="quick-scan-body"><p class="quick-scan-intro">'
        '請依直覺選擇。這不是測驗，沒有標準答案；每題只用一段評論幫你看見當下的判斷起點。'
        f'</p>{"".join(questions)}</div></details>'
    )


def replace_between(source: str, start_pattern: str, end_pattern: str, replacement: str) -> str:
    updated, count = re.subn(start_pattern + r".*?" + end_pattern, replacement, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f"Could not replace section matching {start_pattern}")
    return updated


def current_shared_style() -> str:
    template = (ROOT / "templates" / "chapter_template.html").read_text(encoding="utf-8")
    brand_rule = template.split("{{CSS}}", 1)[1].split("</style>", 1)[0]
    return (
        "\n"
        + (ROOT / "assets" / "chapter.css").read_text(encoding="utf-8")
        + (ROOT / "assets" / "editor-runtime.css").read_text(encoding="utf-8")
        + brand_rule
    )


def update_chapter(chapter: int) -> pathlib.Path:
    page = ROOT / f"{PREFIX}_Chapter{chapter:02d}.html"
    source = page.read_text(encoding="utf-8")

    source, count = re.subn(
        r"<style>.*?</style>",
        lambda _: f"<style>{current_shared_style()}</style>",
        source,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError("Could not synchronize shared chapter styles")

    callouts = render_chapter_callouts(load_chapter_callouts(ROOT, chapter))
    source, count = re.subn(
        r'(</section>)(?:<aside class="reading-callout">.*?</aside>)*(<section id="s1">)',
        rf'\1{callouts}\2', source, count=1, flags=re.S,
    )
    if count != 1:
        raise ValueError("Could not insert pre-reading callouts")

    draft = ROOT / "reference_materials" / "chapters" / f"chapter_{chapter:02d}" / "02_deep_reading_draft.md"
    article = render_deep_reading_markdown(draft.read_text(encoding="utf-8"))
    source = replace_deep_reading_article(source, article)

    learning = json.loads((ROOT / "content" / f"chapter_{chapter:02d}_learning.json").read_text(encoding="utf-8"))

    hero_match = re.search(r'(<section class="hero" id="s0">)(.*?)(</section>)', source, flags=re.S)
    if not hero_match:
        raise ValueError("Could not locate chapter hero")
    hero_body = re.sub(r'<div class="dark">.*?</div>', '', hero_match.group(2), count=1, flags=re.S)
    source = source[:hero_match.start()] + hero_match.group(1) + hero_body + render_start_prompt(learning["start_prompt"]) + hero_match.group(3) + source[hero_match.end():]

    reading_entry = render_orientation(learning["orientation"]) + render_quick_scan(learning["quick_scan"])
    source, count = re.subn(
        r'(<section id="s1"><div class="head">.*?</div>)(?:<aside class="reading-brief"[^>]*>.*?</aside>)?(?:<details class="quick-scan"[^>]*>.*?</details>)?(<div class="reading-essay">)',
        lambda match: match.group(1) + reading_entry + match.group(2),
        source,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError("Could not insert reading orientation and quick scan")

    if "case" in learning:
        case_html = render_case(learning["case"])
        source = replace_between(source, r'<section id="s2">', r'<section id="s3">', case_html + '<section id="s3">')

    config_path = ROOT / "content" / f"chapter_{chapter:02d}.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["quick_scan"] = learning["quick_scan"]
    if "assessment" in learning:
        assessment = learning["assessment"]
        config.update({
            "assessment_version": assessment["version"],
            "dimensions": assessment["dimensions"],
            "questions": assessment["questions"],
            "focus_tips": assessment["focus_tips"],
            "chapter_reflection_prompt": assessment["reflection_prompt"],
        })

    questions_html = render_questions(config["questions"])
    assessment_shell = (
        '<div class="assessment-progress"><b>作答進度</b>'
        f'<span id="assessmentProgress" aria-live="polite">已完成 0／{len(config["questions"])}</span></div>'
        '<div id="assessmentMessageTop" class="assessment-message assessment-message-top" role="alert" tabindex="-1"></div>'
        f'<div class="assess">{questions_html}</div><div class="assessment-actions">'
    )
    source = replace_between(
        source,
        r'(?:<div class="assessment-progress">.*?</div>)?(?:<div id="assessmentMessageTop".*?</div>)?<div class="assess">',
        r'<div class="assessment-actions">',
        assessment_shell,
    )
    source = re.sub(
        r'<div id="assessmentMessage" class="assessment-message"(?: role="alert")?></div>',
        '<div id="assessmentMessage" class="assessment-message" role="alert"></div>',
        source,
        count=1,
    )

    if 'class="privacy-nudge"' not in source:
        source, count = re.subn(
            r'(<section id="s2">.*?<div class="question">)(.*?)(<textarea\b)',
            lambda match: match.group(1) + match.group(2)
            + '<p class="privacy-nudge"><b>書寫提醒：</b>請將人物與事件去識別化，不要輸入姓名、客戶名稱或其他可辨識資訊。</p>'
            + match.group(3),
            source,
            count=1,
            flags=re.S,
        )
        if count != 1:
            raise ValueError("Could not insert privacy reminder near case input")

    source, count = re.subn(
        r'<section id="s5">.*?</section>',
        render_action_commitment(),
        source,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError("Could not synchronize action commitment section")
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    config_json = json.dumps(config, ensure_ascii=False)
    source, count = re.subn(
        r'<script type="application/json" id="chapter-config">.*?</script>',
        f'<script type="application/json" id="chapter-config">{config_json}</script>',
        source, count=1, flags=re.S,
    )
    if count != 1:
        raise ValueError("Could not update chapter config")

    config_end = source.find("</script>", source.find('id="chapter-config"'))
    runtime_start = source.find("<script>", config_end)
    runtime_end = source.rfind("</script>")
    if config_end < 0 or runtime_start < 0 or runtime_end < runtime_start:
        raise ValueError("Could not synchronize chapter runtime")
    runtime = (ROOT / "assets" / "editor-runtime.js").read_text(encoding="utf-8") + "\n" + (ROOT / "assets" / "chapter-runtime.js").read_text(encoding="utf-8")
    source = source[:runtime_start] + f"<script>\n{runtime}\n</script>" + source[runtime_end + len("</script>"):]
    page.write_text(source, encoding="utf-8")
    return page


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 scripts/update_chapter_learning_page.py CHAPTER")
    print(update_chapter(int(sys.argv[1])))
