from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

p5 = ROOT / "LPI_Coach_Chapter05.html"
t5 = p5.read_text(encoding="utf-8")
old = "<p>一家約 180 人的軟體公司準備推出一項企業客戶功能。產品主管志豪希望資深專員怡君負責跨部門交付，因為她最熟悉客戶使用情境。過去團隊習慣所有需求都由志豪最後確認，導致小決定排隊，怡君也逐漸養成先問再做的習慣。</p>"
new = "<p><b>交接前的白板：</b>台中一家 120 人的居家照護服務商準備擴大夜間派案。營運主管芷晴希望資深督導柏宇接手排班與異常處理，因為他最熟悉照護員和家屬的實際需求；但過去所有臨時調度都由芷晴最後拍板，柏宇習慣先把每個小決定送回她的信箱。</p>"
if old in t5:
    t5 = t5.replace(old, new, 1)
old2 = "<p>這次志豪說希望怡君主導，但沒有說明哪些承諾可以自行調整、哪些資安議題要升級，也沒有交代工程與客服的可用時間。怡君收到客戶的新需求後，選擇先調整流程，卻在兩天後發現客服話術尚未更新，工程也需要額外測試。志豪得知後很焦慮，差點決定把所有對外決定收回。</p>"
new2 = "<p>芷晴沒有只說「你全權負責」，而是和柏宇列出共同結果：照護不中斷、重大安全事件必須升級、一般排班可自行調整，並約定每週檢查一次決策紀錄。第一週遇到一名照護員臨時請假，柏宇改了班表，卻發現客服通知與交通安排沒有同步；這個結果讓兩人看見，授權需要的不只是權限，還包括資訊與協作資源。你會如何陪他們設計下一輪支持？</p>"
if old2 in t5:
    t5 = t5.replace(old2, new2, 1)
p5.write_text(t5, encoding="utf-8")

style5 = re.search(r"<style>.*?</style>", t5, flags=re.S).group(0)
p6 = ROOT / "LPI_Coach_Chapter06.html"
t6 = p6.read_text(encoding="utf-8")
t6, count = re.subn(r"<style>.*?</style>", style5, t6, count=1, flags=re.S)
if count != 1:
    raise SystemExit("Module 06 style block missing")
p6.write_text(t6, encoding="utf-8")
