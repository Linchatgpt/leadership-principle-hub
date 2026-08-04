from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
replacements = {
    3: [
        ("<p>情境：新北一家約 220 人的企業軟體公司，產品負責人子晴被交付一項任務：十八個月內，讓公司從一次性專案交付，逐步轉向能持續創造客戶成果的訂閱服務。執行長希望她提出一個能凝聚產品、業務、客服與工程團隊的方向。</p>", "<p><b>客戶的沉默：</b>台北一家 140 人的教育科技公司準備把服務從單次課程改成長期學習方案。產品經理若芸發現，業務談的是續約收入，教學團隊在意學習成效，客服則每天接住家長對使用困難的抱怨。主管要她提出一個能讓各方願意投入的共同方向。</p>"),
        ("<p>策略會議上，子晴提出「成為客戶最信任的數位夥伴」。大家點頭，卻沒有追問這句話會如何改變工作。一週後，業務為了季底營收答應大客戶新增客製報表；產品團隊認為這會拖延共用功能；客服擔心續約風險；工程團隊則不願再背負難以維護的例外。每個人都支持願景，但仍依照各自的績效壓力做選擇。</p>", "<p>她沒有先寫一份漂亮標語，而是邀請一位續約失敗的客戶匿名分享使用歷程，再請各部門回答：「如果這個家庭三個月後願意繼續使用，我們今天必須共同做到什麼？」答案出現差異，也讓團隊看見彼此其實在保護不同的價值。你會如何陪若芸把分歧整理成可共同投入的未來圖像？</p>"),
    ],
    4: [
        ("<p>桃園一家約 260 人的電子零組件公司，近半年接到的客製需求增加。業務把客戶需求寄到共用信箱，客服再轉給產品與品保；只要需求資訊不完整，就會在三個部門之間來回補問。專案經理怡安發現，團隊每週花很多時間追資料，卻仍有幾次在報價後才發現規格理解不同。</p>", "<p><b>星期三下午三點：</b>高雄一家 70 人的餐飲供應商收到連鎖客戶的臨時改單。採購說庫存不足，倉儲說標籤已印好，業務則承諾隔天一定送到。營運專員冠廷打開群組訊息，發現每個人都在補救同一個資訊缺口，卻沒有人能說清楚訂單在哪一個節點卡住。</p>"),
        ("<p>營運主管希望她在一個月內縮短回覆時間，業務主管則擔心增加表單會讓客戶覺得公司反應變慢。品保主管要求保留必要的風險檢查，產品經理認為真正問題不是少一張表，而是沒有人負責判斷哪些資訊已經足夠開始。怡安原本想新增一個簽核關卡，但同事提醒，這可能只是把等待往後移。</p>", "<p>冠廷沒有先新增簽核，而是把最近十筆改單依序畫出：需求何時進來、誰第一次看見、哪項資訊被重問、何時才有人能承諾。他發現緊急訂單不是每次都慢，而是不同角色對「已確認」的意思不同。下一步，他要在不碰觸食品安全護欄的前提下，試做一個一週的交接標記。你會如何協助他選擇證據與回看時間？</p>"),
    ],
}

for number, pairs in replacements.items():
    path = ROOT / f"LPI_Coach_Chapter{number:02d}.html"
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")

canonical = (ROOT / "LPI_Coach_Chapter03.html").read_text(encoding="utf-8")
royal_path = ROOT / "experiments/chapter03-royal/LPI_Coach_Chapter03_Royal.html"
if royal_path.exists():
    royal = royal_path.read_text(encoding="utf-8")
    start = canonical.index('<section id="s2">')
    end = canonical.index('<section id="s3">', start)
    rstart = royal.index('<section id="s2">')
    rend = royal.index('<section id="s3">', rstart)
    royal_path.write_text(royal[:rstart] + canonical[start:end] + royal[rend:], encoding="utf-8")
