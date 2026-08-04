# 產品規格

「卓越領導力©核心課程」的 Leadership Principle hub 聚焦 Module 01–06：接受領導挑戰與五項卓越領導實踐。它把六個主題轉成可重複的學習循環：閱讀、案例、自我反思、工作紀錄與行動承諾。

目標學習者：台灣企業主管、內部教練、HR／OD與領導力培訓者。

資料策略：所有學習紀錄只儲存在目前瀏覽器／裝置的 localStorage；沒有帳號、雲端同步或管理者可見性。

第一階段 Article Hub：文章來源位於 `content/articles/article_XX/`，由 `scripts/build_article_hub.py` 產生主目錄與 `Article_Learning_ArticleXX.html`。每頁包含閱讀導讀、情境快問、自我整理、工作紀錄與行動承諾。

發展自評契約：顯示完成題數，缺答時在題目前與送出區同時提示並聚焦第一題缺答；題目使用 fieldset／legend，評分觸控目標至少 44px，並提供清楚的鍵盤焦點。構面相近時不標示系統建議，改以工作情境問題協助學習者自行選擇焦點。

隱私與可讀性：第一個案例輸入區旁即提醒人物與事件去識別化；小字使用足夠深的 sage／gold 文字色，不只在頁尾提醒。
## Canonical learner pages

- Root `index.html` is the only learner entry map and uses source-neutral copy.
- `LPI_Coach_Chapter01.html` through `LPI_Coach_Chapter06.html` are this project's canonical module outputs.
- Visual experiments are stored under `experiments/` and are not linked as canonical chapters or included in root chapter validation.
- Chapters 01–03 use the latest reading-entry, assessment accessibility, work-record, and action-commitment contracts. Later chapters remain scheduled for migration.

## Shared site shell

- The homepage brand aligns with the homepage content column at desktop widths and returns to the root learning map.
- Chapter brands align with the left edge of the chapter navigation rail content at desktop widths.
- The homepage and every canonical chapter use the same contact footer: `精萃領導™學習中心`、the coach profile link, and a Gmail compose link addressed to `wesley.lin@leading4elite.com`.
- Footer items are separated by spacing rather than punctuation and use a 22px display size.
- The visible brand uses the `XL` monogram and the name `卓越領導力©核心課程` on the homepage and every chapter.
- External footer links open in a new tab with `noopener noreferrer`; the footer stacks without horizontal overflow on narrow screens.
