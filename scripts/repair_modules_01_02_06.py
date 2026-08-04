from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

cases = {
    1: (
        "<p><b>情境：</b>新竹一家 180 人的電子製造公司裡，接受領導挑戰是專案經理怡君最近被期待補強的能力。她的團隊要在六週內完成客戶試產，但研發、品保與業務對優先順序各有不同說法。</p>",
        "<p><b>一封沒有答案的郵件：</b>台中一家 90 人的醫療服務公司裡，專案主管思妤收到三個部門寄來的不同版本：客服說客戶等待太久，資訊部門說需求一直變，財務則提醒預算不能再增加。她被要求在下週提出改善方向，卻發現每個人都把問題描述成別人的責任。</p>"
    ),
    2: (
        "<p><b>情境：</b>新竹一家 180 人的電子製造公司裡，以身作則是專案經理怡君最近被期待補強的能力。她的團隊要在六週內完成客戶試產，但研發、品保與業務對優先順序各有不同說法。</p>",
        "<p><b>週一早會之後：</b>高雄一家連鎖餐飲企業正準備更換訂貨系統。營運主管柏翰公開說「先確保前線能穩定服務」，但新系統上線前，他又要求團隊把所有時間投入測試，導致門市培訓被延後。成員開始猜測，品質究竟是不是只在口號裡重要。</p>"
    ),
    6: (
        "<p><b>情境：</b>新竹一家 180 人的電子製造公司裡，鼓舞人心是專案經理怡君最近被期待補強的能力。她的團隊要在六週內完成客戶試產，但研發、品保與業務對優先順序各有不同說法。</p>",
        "<p><b>凌晨兩點的訊息：</b>台南一家物流公司剛完成倉儲系統切換，第一晚雖然沒有重大事故，現場人員卻因連續加班而士氣低落。營運經理雅雯在群組裡看到大家只留下「收到」，開始思考要如何讓努力被看見，而不是再喊一次加油。</p>"
    )
}

for number, (old, new) in cases.items():
    path = ROOT / f"LPI_Coach_Chapter{number:02d}.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace("PART I · MODULE "+f"{number:02d}", "MODULE "+f"{number:02d}")
    if old in text:
        text = text.replace(old, new, 1)
    if number == 1:
        text = text.replace("<p>怡君的主管希望她「更有領導感」，卻只給了模糊的評語。她的同事阿哲則說：「你每次都很快給答案，我們反而不敢提出不同看法。」怡君想改善速度，又不想讓團隊覺得她失去掌控。你是她的內部教練，第一次對話要怎麼開始？</p>", "<p>思妤沒有立刻宣布新流程，而是邀請三方各帶一個最近發生的事件，先分辨事實、感受與推論。她想知道的不是誰最有道理，而是下一次會議要做哪一個不同選擇，才能讓問題更早被看見。你會如何陪她把模糊壓力轉成可練習的領導行動？</p>")
    elif number == 2:
        text = text.replace("<p>怡君的主管希望她「更有領導感」，卻只給了模糊的評語。她的同事阿哲則說：「你每次都很快給答案，我們反而不敢提出不同看法。」怡君想改善速度，又不想讓團隊覺得她失去掌控。你是她的內部教練，第一次對話要怎麼開始？</p>", "<p>柏翰發現自己不是不重視服務，而是壓力一來就把短期進度放到最前面。他決定在下一次排程會議中，先說明這次取捨、承認培訓延後造成的影響，再請前線代表指出不能被犧牲的底線。若你是他的教練，會如何把價值觀拉回一個可被看見的決定？</p>")
    else:
        text = text.replace("<p>怡君的主管希望她「更有領導感」，卻只給了模糊的評語。她的同事阿哲則說：「你每次都很快給答案，我們反而不敢提出不同看法。」怡君想改善速度，又不想讓團隊覺得她失去掌控。你是她的內部教練，第一次對話要怎麼開始？</p>", "<p>雅雯沒有立刻發一段口號式公告，而是隔天分別訪談夜班、客服與工程人員，請他們指出哪個努力最容易被忽略。她想把肯定連到具體進展，也想確認團隊真正需要的是更多掌聲、合理休息，還是下一個可相信的里程碑。你會如何陪她設計回應？</p>")
    if number == 6:
        text = re.sub(r'<section id="s5">.*?</section></main>', '<section id="s5"><div class="head"><small class="kicker">05 ACTION COMMITMENT</small><h2>行動承諾</h2><p>只選一個小到能在工作現場完成的行動，寫下時間與場景。</p></div><div class="simple-record action-commitment"><div id="experimentFocus" class="experiment-focus">尚未選擇發展焦點</div><label>我的行動<textarea data-key="experiment"></textarea></label><label class="action-date">預計實行日期 <input type="date" data-key="followupDate"></label></div></section></main>', text, count=1, flags=re.S)
    text = re.sub(r'<small class="kicker">PART I · MODULE \d{2}</small>', lambda m: m.group(0).replace('PART I · ', ''), text, count=1)
    path.write_text(text, encoding="utf-8")

for path in ROOT.glob("LPI_Coach_Chapter*.html"):
    text = path.read_text(encoding="utf-8")
    text = text.replace("PART I · ", "").replace("PART II · ", "")
    path.write_text(text, encoding="utf-8")

for path in (ROOT / "experiments").rglob("LPI_Coach_Chapter*.html") if (ROOT / "experiments").exists() else []:
    text = path.read_text(encoding="utf-8")
    text = text.replace("PART I · ", "").replace("PART II · ", "")
    path.write_text(text, encoding="utf-8")

index = ROOT / "index.html"
if index.exists():
    text = index.read_text(encoding="utf-8")
    text = text.replace(" · PART I", "").replace(" · PART II", "")
    index.write_text(text, encoding="utf-8")

# Keep future generated pages free of the old part label.
builder = ROOT / "scripts/build_chapters.py"
source = builder.read_text(encoding="utf-8")
source = source.replace("PART {'I' if i<=6 else 'II'} · MODULE {i:02d}", "MODULE {i:02d}")
source = source.replace('"PART I" if i<=6 else "PART II"', '""')
builder.write_text(source, encoding="utf-8")
