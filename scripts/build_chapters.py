import json, html, pathlib, re
from deep_reading_renderer import render_deep_reading_markdown
from update_chapter_learning_page import render_questions, update_chapter as update_chapter_learning_page
from chapter_callouts import callout_path, load_chapter_callouts, render_chapter_callouts
from update_site_shell import FOOTER

ROOT=pathlib.Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'config.json').read_text())
prefix=cfg['output_prefix']
module_start,module_end=cfg.get('module_range',[1,11])
chapters=[
('接受領導挑戰','從「我知道答案」轉向陪伴他人找到可行的下一步','建立教練視角、學習契約與五項實踐的共同語言。','接受挑戰'),
('以身作則','把價值觀變成團隊看得見、跟得上的日常行為','教練協助領導者對齊價值、承諾與行動。','以身作則'),
('啟發共同願景','讓未來圖像成為今天做選擇的理由','從個人渴望出發，連結團隊意義與可說清楚的方向。','共同願景'),
('挑戰流程','把「這裡一直都是這樣」改寫成可測試的假設','以安全的小實驗取代大聲宣告，從學習中推進改進。','挑戰流程'),
('促能他人行動','授權不是把工作丟出去，而是讓人有能力完成它','從信任、能力、資源與決策邊界打造自主行動。','促能他人'),
('鼓舞人心','讓努力被看見，讓團隊知道自己正在變好','以真實、及時、具體的肯定維持集體動能。','鼓舞人心'),
('走向成功的教練','先定義成功，再一起設計抵達路徑','釐清角色、成果、責任與回饋節奏，避免教練變成代辦者。','教練成功'),
('教練能力','高品質教練對話，始於聽見未說出口的東西','練習聆聽、提問、回饋、挑戰與保持界線。','教練能力'),
('教練流程','從回饋資料走到一個能被追蹤的行動','建立回饋—聚焦—實驗—檢視—調整的循環。','教練流程'),
('事情失控時','當對話卡住，先修復安全感，再處理問題','面對防衛、失信、衝突與高風險情境，採取低傷害的下一步。','修復與風險'),
('教練自己到精熟','教練也需要被教練，才能持續看見自己的盲點','用反思、督導、同儕回饋與刻意練習累積精熟。','教練精熟')]
dims=['以身作則','啟發願景','挑戰流程','促能他人','鼓舞人心']
def qitems(title):
  stems={
    '以身作則':'我有把自己說重視的原則，轉成別人看得見的行動。',
    '啟發願景':'我有讓對方說出他願意投入的未來，而不是只宣布目標。',
    '挑戰流程':'我有把改善想法拆成低風險、可檢驗的小實驗。',
    '促能他人':'我有提供決策邊界、資源或練習，讓對方能自主完成。',
    '鼓舞人心':'我有具體指出進展與貢獻，而不是只在結果完美時稱讚。'}
  return [[dims[i%5],stems[dims[i%5]]] for i in range(12)]
def page(i,title,lead,desc,focus):
  fn=f'{prefix}_Chapter{i:02d}.html'; key=f'{prefix}Chapter{i}'
  chapter_dims=dims
  questions=qitems(focus)
  nav=['00 開始','01 深入閱讀','02 工作案例','03 發展自評','04 工作紀錄','05 行動承諾']
  navhtml=''.join(f'<a href="#s{j}">{n}</a>' for j,n in enumerate(nav))
  qhtml=render_questions(questions)
  article=(f'<p>在組織裡，領導力不只發生在正式職位上，也發生在你如何面對一個不確定的要求、如何讓別人願意一起工作，以及如何把回饋變成下一次選擇。本章把「{title}」視為一種可以被觀察、練習與修正的工作行為。</p>'
           f'<h3>先從一個真實張力開始</h3><p>當工作忙、權責不清或團隊對方向沒有共識時，人很容易把教練對話變成建議清單。更有用的做法，是先讓對方看見自己的價值、選擇與證據，再共同定義一個小而可行的行動。</p>'
           f'<h3>本章的工作鏡頭</h3><p>請將抽象詞語換成可看見的動作：誰在什麼時候說了什麼？對方如何回應？結果是什麼？如果沒有證據，就把它當成假設，而不是結論。教練的任務不是替領導者評分，而是協助他把回饋轉成學習。</p>'
           f'<div class="reading-tool"><span class="tool-label">原創工作工具</span><h3>三格教練鏡頭</h3><ol><li><b>價值：</b>我希望別人從我的行動看見什麼？</li><li><b>證據：</b>最近哪個具體事件支持或挑戰這個看法？</li><li><b>下一步：</b>一週內要做哪個最小實驗？</li></ol><p class="tool-limit">這是本學習中心的工作工具，不是書中量表，也不取代正式教練、督導或組織程序。</p></div>')
  if i==1:
    article='''<p>領導者並不是天生不同，而是許多人在自己最投入、最有影響力的經驗裡，會反覆做出一些相似的行為。這些行為可以被描述、被回饋，也可以在工作現場重新練習。教練的價值，正是在這裡：把一段模糊的「我好像不夠會帶人」，轉成一組可以觀察的選擇。</p>
    <h3>接受挑戰，不等於把自己變成完美領導者</h3><p>接受領導挑戰，首先是承認領導力是一種責任，而不是頭銜。你不需要先等到有正式授權、資源充足或所有人都支持，才開始影響事情；但你也不必把所有結果扛在自己身上。成熟的教練會同時守住兩條線：讓領導者對自己的行為與承諾負責，也讓他看見系統、權限與他人選擇對結果的影響。</p>
    <p>因此，教練對話不是「告訴你五項能力哪一項最低」，而是協助領導者回答三個問題：我想成為怎樣的人？最近的行動讓別人看見了什麼？下一週我願意用哪個小行動取得新證據？這三題把價值、行為與學習連在一起。</p>
    <h3>五項實踐是一張地圖，不是五個抽屜</h3><p>本學習中心採用五項實踐作為共同語言：以身作則、啟發共同願景、挑戰流程、促能他人行動、鼓舞人心。它們常常同時出現在一個事件裡。例如，推動新流程時，你要先說清楚重視的原則，讓團隊理解未來圖像，邀請大家設計實驗，提供資源與決策邊界，並在進展中肯定貢獻。若只強調其中一項，行動可能變成口號、命令或單次激勵。</p>
    <div class="reading-tool"><span class="tool-label">五項實踐的快速定位</span><h3>當你卡住時，問「少了哪一種行動？」</h3><ul><li><b>以身作則：</b>我是否清楚說出並實踐重要原則？</li><li><b>啟發共同願景：</b>對方是否看見自己為何值得投入？</li><li><b>挑戰流程：</b>我們是否把改善變成可學習的小實驗？</li><li><b>促能他人：</b>對方是否擁有能力、信任與必要資源？</li><li><b>鼓舞人心：</b>進展與貢獻是否被真實而及時地看見？</li></ul><p class="tool-limit">這是本學習中心的原創定位工具，用於選擇對話焦點，不是正式量表或診斷。</p></div>
    <h3>教練如何使用回饋資料</h3><p>回饋資料的用途，是幫助領導者看見自己與不同關係人的觀察差異，然後安排下一步。對話時，先請當事人說出他看見的模式，再一起檢視哪些分數或留言值得追問。不要把單一低分直接解釋成缺陷，也不要把高分當作已經精熟；最有價值的線索，往往是「我以為別人看見了什麼」與「別人實際描述了什麼」之間的距離。</p>
    <p>如果你使用正式 LPI，應遵守授權、匿名與施測流程，並由受訓的引導者協助解讀。本頁的自評只是一個原創的學習暖身，不能代表正式 LPI 結果，也不適合用於晉升、考核或選才。</p>
    <h3>領導挑戰通常不是單一人的問題</h3><p>工作現場的領導困難，很少只是「某個人不夠有自信」或「溝通技巧不好」。它往往同時受到幾個力量影響：組織的獎酬制度鼓勵什麼、主管真正支持什麼、團隊過去如何形成默契、跨部門之間誰有正式或非正式的權力，以及眼前的交付壓力有多大。教練如果只要求領導者「更勇敢」，可能會把系統性限制個人化；如果只把責任推給制度，又會讓領導者失去可以行動的空間。</p><p>較好的起點是把問題分成三層。第一層是我能直接控制的行為，例如我如何主持會議、如何回應不同意見、如何追蹤承諾。第二層是我能影響但不能單獨決定的關係，例如我如何與主管、同儕或關鍵利害關係人建立對話。第三層是我目前只能理解、調整策略或尋求正式支持的制度限制，例如權責設計、資源分配或不合理的安全風險。這樣的區分讓教練對話既不過度責怪個人，也不會停留在無力感。</p>
    <h3>教練不是替領導者解題的人</h3><p>在台灣職場，內部教練常常同時是主管、資深同事或 HR。這種雙重角色很容易讓對話混合成「我一邊聽你說，一邊評估你」。因此，第一次對話需要先說清楚：這次談話的目的、資料如何使用、哪些內容需要保密、哪些情境必須依組織程序處理。只要涉及霸凌、歧視、報復、違法或人身安全，就不能把它包裝成單純的行為實驗，應優先使用正式申訴、HR、法遵或專業支持管道。</p><p>教練與顧問的差異，也不在於誰比較有經驗，而在於工作方式不同。顧問可能受邀提供專業判斷與方案；教練則更常協助對方澄清問題、辨識假設、比較選項並承擔選擇。教練仍然可以分享觀察或提出建議，但應先取得允許，並把建議放回對方的情境中檢驗：「這是我的一個可能看法，你想聽嗎？」說完後再問：「哪一部分適用？哪一部分不適用？」這樣才能避免建議變成新的命令。</p>
    <h3>五項實踐如何在一個事件裡連動</h3><p>假設一位部門主管要導入新的客戶回覆流程。若他只做「挑戰流程」，直接宣布新規定，團隊可能因為不理解目的而表面配合；若他只做「啟發願景」，談很多服務理想卻沒有試行步驟，也可能被視為空話。完整的領導行動會先說明自己重視的原則，例如「回覆速度不能以犧牲承諾為代價」；接著邀請團隊描述客戶真正需要的體驗；再共同選一種低風險的試行方式，設定誰有權調整；過程中持續詢問阻礙並補足資源；最後用具體事例肯定那些讓流程變好的貢獻。</p><p>這個例子顯示，五項實踐不是五個獨立技能的清單，而是一個互相支撐的循環。價值讓願景可信，願景讓改變有方向，實驗讓願景進入現實，信任與能力讓更多人能參與，肯定則讓團隊願意繼續投入。少了其中一環，領導者常會落入熟悉的補償模式：用更強的控制補足信任不足，用更多簡報補足願景不清，用加班補足流程設計的問題。</p>
    <h3>如何讀一份回饋，而不被分數綁架</h3><p>回饋資料最容易引發兩種反應：防衛或過度討好。看到低分時，領導者可能急著解釋「他們不了解我的工作」；看到高分時，則可能把它當成已經不需要練習的證明。教練可以把分數改寫成探索問題。先問：「哪一個結果最讓你意外？」再問：「你想到哪個具體事件？」接著比較不同角色的觀察：「主管、同儕與部屬看到的是同一個情境嗎？」最後才討論：「如果要取得新的證據，你願意做哪一個小行動？」</p><p>還要留意平均分數遮蔽的訊息。例如同樣是 3.8 分，有可能代表所有人都給中間評價，也可能代表有人給 5 分、有人給 2 分。後者通常不是單純的能力高低，而是行為在不同情境、不同關係或不同壓力下呈現不一致。教練應協助領導者找出「何時有效、何時失效」，而不是只追求下一次平均分數上升。</p><p>同樣重要的是回饋的情緒承接。當事人第一次看到與自我形象不一致的資料時，可能需要先停下來，而不是立刻訂出三個改進目標。教練可以說：「這份結果看起來有些刺耳，我們先不用急著同意或反駁。你想先理解哪一個部分？」這句話把速度放慢，也保留了當事人的尊嚴。對話若沒有安全感，再精確的資料也很難轉成學習。</p>
    <h3>一段有品質的第一場教練對話</h3><p>第一場對話不必急著完成完整發展計畫，可以使用四個階段。第一，讓領導者用自己的話說明他想改善什麼，以及為什麼現在重要。第二，請他選一個最近的真實事件，描述當時的目的、行動、他人反應與結果。第三，教練分享一到兩個觀察，清楚標示它們是觀察還是推論，並邀請對方修正。第四，雙方把焦點縮小成一個可在一週內觀察的行為，約定如何知道它有產生不同。</p><p>可以使用這樣的句型：「當你說希望團隊更主動時，你期待看到什麼具體行為？」、「在剛才的事件中，你做了什麼，讓對方更容易或更難表達不同意見？」、「如果不要求自己一次改完，你願意先測試哪個小改變？」這些問題的功能不是讓對方答出標準答案，而是把抽象評語轉為可學習的證據。</p><p>對話結束前，請把承諾說得足夠小、足夠清楚。不要只寫「提升授權」或「改善溝通」，而要寫成「在下週二的跨部門會議，我先邀請兩位成員各提出一個風險，再由他們選擇一項可處理的問題；會後詢問他們是否更清楚自己的決策範圍」。這種描述包含場景、行動與回饋，才有可能在事後回看。若行動沒有成功，也不等於教練失敗；重要的是知道哪個假設不成立，下一輪要調整什麼。</p>
    <h3>教練如何示範這套模型</h3><p>教練也需要示範這五項實踐：以身作則，是準時、守約、說到做到；啟發願景，是與領導者共同定義他想成為的樣子；挑戰流程，是勇於提出不舒服但有用的問題；促能他人，是讓對方保有選擇與責任；鼓舞人心，是在挫折中指出已經發生的進展。若教練只要求領導者改變，自己卻急著給答案、忘記追蹤或只在成功時出現，對話本身就失去可信度。</p><p>最後，請把「接受挑戰」理解成持續選擇，而不是一次性的宣言。每一次會議、回饋、授權與修復，都提供新的練習場。你可以從一個不大的承諾開始：下一次遇到熟悉的壓力反應時，先多問一個問題，先說清楚一項原則，或先邀請一個不同聲音。小行動不會立刻消除複雜性，卻能讓你與團隊取得比昨天更好的證據。</p>
    <blockquote>把回饋當作鏡子，不是判決；把行動當作實驗，不是表演。</blockquote>'''
  if i==2:
    article='''<p>「以身作則」不是把自己塑造成永遠正確、永遠穩定的模範人物，而是讓你所說重視的原則，在別人每天看得見的選擇裡有一致的證據。當領導者說重視透明，卻在壞消息出現時只問「誰要負責」；說重視授權，卻在每個細節都收回決定權，團隊收到的訊息就會以行動為準，而不是以宣言為準。</p>
    <h3>價值觀必須從口號變成選擇</h3><p>組織裡很少有人會直接反對「誠信、合作、客戶第一」這類價值。然而真正困難的地方，是當兩個好原則同時出現時，你如何做取捨。例如，客戶希望立即回覆，但工程團隊還沒有足夠資料；你可以追求速度，也可以保護承諾的可信度。以身作則不是找到一句更漂亮的標語，而是說清楚在衝突情境中你依據什麼排序，並願意承擔這個排序帶來的成本。</p><p>教練可以協助領導者把抽象價值拆成三個問題：第一，這個價值在具體工作中應該看起來像什麼？第二，壓力升高時，我最容易做出哪個相反的行為？第三，如果我要讓團隊相信我，下一個可被觀察的選擇是什麼？這三題會把「我很重視」轉成「我會在某個場景做某件事」。</p>
    <h3>一致性不是沒有變化，而是有可理解的原則</h3><p>成熟的領導者不會把一致性誤解成每次都用同一種處理方式。面對新進同仁與資深專家，支持方式可能不同；面對一般失誤與安全風險，處理速度也可能不同。真正需要一致的是判斷原則、溝通方式與承擔責任的態度。當例外出現時，領導者要能說明：「這次的情況和上次不同在哪裡？因此我如何調整？」如果只改變結論、不說明理由，團隊很容易把彈性解讀成偏心或政治判斷。</p><p>這也是教練對話中很重要的區分：我們要檢視的不是領導者是否每次都做出完美選擇，而是他是否能讓自己的選擇被理解、被追問、被修正。當領導者承認「我昨天要求大家提早通報風險，但今天自己卻延後說明」，這種承認不是削弱權威，反而示範了責任與修復的可能。</p>
    <div class="reading-tool"><span class="tool-label">原創工作工具</span><h3>價值—行動對照表</h3><ol><li><b>我說重視：</b>最近常掛在嘴上的一項原則是什麼？</li><li><b>別人看見：</b>在最近一次壓力情境中，我做了什麼，讓別人判斷我真的重視它？</li><li><b>落差位置：</b>哪個行為讓我的說法失去可信度？不要先解釋，先描述。</li><li><b>下一次選擇：</b>我會在什麼時間、對誰、做哪個可觀察的不同動作？</li></ol><p class="tool-limit">這是本學習中心的原創反思工具，用來準備教練對話，不是原書量表或正式診斷。</p></div>
    <h3>教練要追問行為，也要保護人的尊嚴</h3><p>當回饋指出「你說一套、做一套」時，領導者很容易立刻防衛。教練若只重複評語，對話可能變成審判；若急著安慰，又會錯過重要資料。較好的做法，是把評語轉成事件：「你想到的是哪一次會議？」、「當時你說了什麼、做了什麼？」、「團隊可能如何理解那個決定？」這樣既不否定回饋，也不把一個行為等同於一個人的人格。</p><p>接著可以邀請領導者補充情境因素，但順序很重要：先承認行為造成的影響，再討論當時的限制。若一開始就用資源不足、時程壓力或上級要求來解釋，對方可能聽見的是推卸責任。教練可以說：「這些限制確實存在；在限制存在的前提下，你仍然想讓團隊看見什麼原則？」問題因此從「你為什麼做錯」轉向「下一次你想如何在現實裡做得更一致」。</p>
    <h3>以身作則也包含如何面對錯誤</h3><p>團隊不只觀察領導者在成功時怎麼做，也觀察他犯錯後怎麼做。當決策造成延誤，領導者是否願意先說明自己的部分？當成員提出不同意見，領導者是否會處罰提出問題的人？當承諾無法完成，領導者是否及早更新資訊、重新協商範圍？這些瞬間會形成比年度價值宣告更強的文化訊號。</p><p>一個有用的修復句型是：「我原本說要＿＿，但我實際做了＿＿；這讓你們可能承受＿＿。我現在能先補上的一件事是＿＿，也請你們告訴我下一步需要看見什麼。」這不是表演脆弱，而是把責任、影響與補救連在一起。教練可以協助領導者練習短而具體的說法，避免把道歉變成長篇自我辯護。</p>
    <h3>把原則帶進授權與回饋</h3><p>以身作則常被誤解成「領導者自己做給大家看」，但如果所有事情都由領導者親自完成，團隊反而沒有練習的空間。更完整的示範包括：清楚說明決策邊界、讓成員知道什麼情況需要升級、在結果不完美時檢視學習，而不是只收回權限。領導者可以說：「這個範圍由你決定；如果涉及客戶安全或成本超過某個界線，再一起討論。」這種邊界本身就是對責任與信任的示範。</p><p>回饋也要同樣具體。不要只說「你很符合我們的價值」，而要指出：「你在會議中先讓品保說明風險，再邀請業務提出客戶影響；這讓團隊在速度與品質之間有共同依據。」具體回饋讓被肯定的人知道要繼續什麼，也讓旁觀者知道組織真正重視什麼。</p>
    <h3>案例拆解：當主管要求大家坦誠，卻不接壞消息</h3><p>怡君在週會上宣布：「我們要建立坦誠文化，任何風險都要早點說。」接著一位工程師提到測試可能延後兩天。怡君第一反應是皺眉，追問：「為什麼現在才講？你有沒有先想辦法？」會議後大家仍然說「沒問題」，但私下開始把風險留到最後一刻。</p><p>這個事件不必簡化成怡君「不會溝通」。她可能同時承受客戶節點、主管期待與團隊交付壓力。教練可以請她比較宣言與行動的落差：她說希望早點知道風險，卻在第一個壞消息出現時讓提出者承受羞愧。下一次，她可以先問：「這個延後目前最需要我們理解的是哪個假設？」再說明：「我們先把資訊攤開，責任與處理方案稍後分開談。」這是一個小小的順序改變，卻能讓團隊看見她真的把學習與透明放在一起。</p>
    <h3>一週行動的設計原則</h3><p>以身作則的實驗不應只是「我要更有榜樣」，而要包含場景、行為與證據。例如：「在下週一的專案例會，當有人提出延誤或風險時，我先用一個澄清問題理解情況，再說明我如何判斷優先順序；會後請兩位成員回饋，他們是否更敢在早期提出問題。」這個實驗不保證結果立刻變好，但能產生新的資料：誰更願意發言？哪些風險被提早看見？我是否仍在壓力下回到原來的反應？</p><p>若實驗失敗，請不要把它解釋成「我不適合當領導者」。可以回到三個檢視點：我的原則是否太抽象？我的行動是否與場景不匹配？我是否提供了足夠的決策邊界與後續回饋？以身作則的學習不是一次證明自己，而是在一連串選擇中逐步提高可信度。</p>
    <blockquote>領導者最有影響力的價值宣告，往往發生在壓力升高、壞消息出現的那一刻。</blockquote>'''
  if i in (1,2):
    article += '''<h3>從概念走到現場：先辨識行為單位</h3><p>抽象的領導語言之所以難以練習，常常是因為它把太多動作包在一個詞裡。「更有擔當」可能包含提早通報、承認錯誤、重新分配資源與向上溝通；「更能授權」則可能包含說明邊界、提供資訊、允許不同做法與在事後檢視。當你只寫下概念，就無法知道下一次要改變哪個動作。請把每個概念拆成一個可在三十分鐘內被觀察的行為單位。</p><p>一個好的行為單位通常包含四個元素：發生的場景、你做出的動作、對方可觀察的反應，以及你會如何判斷下一步。比如「在週會中先請一位平常少發言的人提出風險，等待至少五秒再回應，並記錄他是否補充資訊」就比「改善傾聽」更容易實驗。它也讓教練有機會問：「你做了什麼？對方做了什麼？哪裡和預期不同？」</p>
    <h3>區分意圖、行為與影響</h3><p>領導者常以意圖理解自己：「我只是希望事情順利」、「我只是想保護團隊」、「我只是要求負責」。團隊卻以行為與影響理解他：打斷、追問、收回決定、延後說明，或讓人不敢再提供壞消息。意圖不必被否定，但它不能代替影響的檢視。教練可以同時保留兩個句子：「你想保護品質」與「你的回應讓人暫停提供資訊」都可能是真的。成熟的發展對話不是在兩者之間選一個，而是尋找能讓意圖與影響更接近的下一個行動。</p><p>也要小心把影響直接推論成動機。有人沉默，不一定代表他不在乎；有人反覆確認，不一定代表他能力不足。先描述可見事實，再提出多個可能解釋，最後向當事人或關係人求證。這種做法能降低貼標籤，也能讓回饋變成更可靠的學習資料。</p>
    <h3>設計一個安全而有挑戰的練習</h3><p>小實驗不是把重要工作拿來冒險，而是在可承受的範圍內取得新證據。設計時可先問四件事：如果這個做法不如預期，最壞的可逆損失是什麼？誰需要事先知道？哪個決策仍然必須升級？我們要在什麼時間點停下來檢查？對高風險議題，安全、法規、客戶承諾與人身福祉要優先於學習速度，不能用「實驗」掩蓋應有的治理程序。</p><p>安全也不是讓所有人永遠舒服。若團隊只說熟悉的答案，教練可以邀請不同觀點；若領導者一直把責任推給制度，教練可以請他辨識仍能控制的一小段行動。挑戰與支持要同時存在：有足夠支持，人才能承受挑戰；有適度挑戰，支持才不會變成縱容或停滯。</p>
    <h3>用對話建立承諾，而不是用漂亮句子結案</h3><p>一段教練對話的品質，不在於最後寫出多完整的計畫，而在於當事人是否用自己的語言說出承諾、理解代價，並知道如何取得回饋。結尾可以請對方完成四句話：「我真正想改變的是……」、「我願意先測試……」、「我預期最難的是……」、「我會從誰那裡取得什麼證據……」。若對方只說「我會更注意」，教練可以溫和地追問場景與時間，而不是替他把承諾寫好。</p><p>承諾需要有回來檢視的節點。檢視不是檢查誰有做到，而是比較假設與現實：哪一部分有效？哪一部分讓事情更難？誰受到意外影響？下一輪要保留、停止或調整什麼？當團隊習慣用這種方式回顧，失敗就不必被隱藏，成功也不會被過度神化。</p>
    <h3>給自己的收束問題</h3><p>完成本章後，請不要急著挑一個最漂亮的答案。選一個最近仍然讓你在意的事件，寫下當時的情境、你的意圖、實際行為、他人可能承受的影響，以及下一次想取得的證據。再請一位熟悉你工作的人只回應一個問題：「在這個情境裡，我哪個行動最值得保留？哪個行動若調整，最可能讓合作變容易？」把答案帶回工作現場，讓學習成為下一次選擇的準備，而不是停在頁面上的自我描述。</p>
    <h3>當原則彼此衝突時，如何做出可說明的選擇</h3><p>工作裡的價值很少單獨出現。透明可能與保密衝突，速度可能與品質衝突，照顧個人可能與團隊公平衝突。領導者不必假裝所有原則都能同時最大化，但需要讓大家知道自己如何排序，以及這個排序何時會重新檢查。教練可以請當事人畫出兩個原則的拉力，分別寫下「如果偏向 A，誰會受益？誰可能承受代價？」再問：「哪個代價是我們願意承擔的？哪個代價不能被接受？」這樣的討論比尋找唯一正確答案更接近真實決策。</p><p>說明選擇時，請避免只引用職位權力。可以說明資料、限制、判斷原則與暫時性：「目前我們知道的是……，還不知道的是……；基於安全與客戶承諾，我們先選擇……；如果在週三前取得新的證據，就重新檢查。」這種說法讓團隊知道決定不是神諭，也不代表領導者沒有立場。它同時示範了判斷、謙遜與責任。</p>
    <h3>讓團隊也能看見並複製好行為</h3><p>以身作則的終點，不是大家依賴一個模範，而是團隊逐漸能自行做出符合原則的選擇。領導者可以把自己的判斷過程說出來，邀請成員用同一套問題練習，而不是只公布結論。例如在回顧會議中，先問：「我們當時想保護什麼？哪個訊號被忽略？下次誰可以更早提出？」久而久之，原則就從個人風格轉成團隊的共同工作方式。</p><p>也要留意示範不等於控制。當成員採取與你不同、但同樣符合原則的做法時，請辨識「原則是否一致」與「方法是否必須相同」的差別。若領導者要求所有人用自己的語氣、流程與節奏，團隊可能學到的是服從；若領導者說清楚底線並容許多種合宜做法，團隊才會累積真正的判斷能力。</p>
    <h3>把觀察變成下一輪發展</h3><p>每次行動後，請保留三種資料：你當下注意到什麼、別人實際回應什麼、結果和預期有何差異。不要只保留成功故事，因為那些卡住、重複或被誤解的片段，往往更能指出下一個學習焦點。教練可以協助你把資料分成「我能直接改變的行為」、「我需要與他人協商的關係」以及「我需要升級或調整的制度條件」。分層之後，行動會更小、更精準，也比較不會把整個系統的問題都變成個人責任。</p><p>當你再次回到同一類情境，先不要問自己有沒有變成理想中的領導者；改問：「這次我是否更早看見訊號？是否更清楚說明選擇？是否讓更多人有機會承擔適當責任？」這些問題把成長從自我評價移到可觀察證據，也讓每一次工作事件都成為下一輪練習的素材。</p>
    <p>最後，把一次練習的結果交還給團隊，而不是只留在自己的筆記裡。分享你看見的改變、仍然不確定的地方，以及下一次想邀請大家一起觀察的訊號。當領導者願意讓學習過程被看見，團隊就不必猜測標準，也更容易提供真實回饋。這種公開但不羞辱人的檢視，會讓原則逐漸成為日常協作的語言。你也可以請團隊指出一個「繼續做」與一個「停止做」的具體行為，讓下一輪練習有清楚的起點。把這些回饋放在下一次會議開始前重新閱讀，提醒自己先實踐再要求他人跟上。</p>'''
    article=article.replace('教練可以說：「這份結果看起來有些刺耳，我們先不用急著同意或反駁。你想先理解哪一個部分？」這句話把速度放慢，也保留了當事人的尊嚴。', '教練可以說：「這份結果看起來有些刺耳，我們先不用急著同意或反駁。你想先理解哪一個部分？」這句話把速度放慢，也保留了當事人的尊嚴。<div class="reading-pause"><span class="pause-label">停下來想一想</span><h3>你的第一個反應是什麼？</h3><p>當你收到與自我形象不一致的回饋時，通常會先解釋、反駁、沉默，還是追問？先寫下這個反應，不必急著判斷它好不好。</p><p class="pause-prompt">我最常出現的第一個反應是：</p><div class="pause-line"></div></div>')
    article=article.replace('這種描述包含場景、行動與回饋，才有可能在事後回看。若行動沒有成功，也不等於教練失敗；重要的是知道哪個假設不成立，下一輪要調整什麼。', '這種描述包含場景、行動與回饋，才有可能在事後回看。若行動沒有成功，也不等於教練失敗；重要的是知道哪個假設不成立，下一輪要調整什麼。<div class="reading-pause reading-pause--compare"><span class="pause-label">現場對照</span><h3>把「更有領導感」翻成看得見的行動</h3><p>想像你在下週的跨部門會議中，團隊成員提出一個你不同意的做法。你會怎麼做，才能同時保留決策責任，也讓對方願意繼續提供資訊？請寫下一個具體說法或動作。</p><p class="pause-prompt">我會說／做：</p><div class="pause-line"></div></div>')
    article=article.replace('小行動不會立刻消除複雜性，卻能讓你與團隊取得比昨天更好的證據。', '小行動不會立刻消除複雜性，卻能讓你與團隊取得比昨天更好的證據。<div class="reading-pause reading-pause--action"><span class="pause-label">帶走一個行動</span><h3>把本章變成下一次選擇</h3><p>請選一個真實場景，寫下你願意開始、停止或繼續的行為。行動要小到能在一週內完成，並且要能觀察到他人的反應。</p><p class="pause-prompt">下一個場景／我的行動／我要觀察的證據：</p><div class="pause-line"></div></div>')
    article=article.replace('不是原書量表','不是正式量表').replace('不是書中量表','不是正式量表')
    article += '<div class="reading-tool"><span class="tool-label">現場辨識卡</span><h3>當你卡住時，先找出哪一層需要調整</h3><ol><li><b>行為：</b>我現在能直接改變哪一個說法或動作？</li><li><b>關係：</b>我需要和誰重新對齊期待、資訊或決策邊界？</li><li><b>系統：</b>哪一項制度限制需要升級、協商或取得支持？</li></ol><p class="tool-limit">先分層，再選擇；不要把所有複雜問題都變成個人缺點。</p></div><p>請把今天的閱讀轉成一個明確承諾：在下一個真實場景中，讓一位合作對象看見一項不同的行動，並在事後記下對方的反應與自己的學習。這份紀錄會成為下一次對話的起點，也能幫助你分辨真正的改變與一時的順利。</p>'
    article += '''<aside class="reading-callout"><span class="tool-label">概念說明</span><h3>意圖、行為與影響</h3><p>意圖是你想完成的事，行為是別人實際看見的事，影響則是對方因此如何理解、感受與行動。三者可能一致，也可能產生落差。閱讀一個事件時，先分開記錄這三層，再討論下一步，能避免把人格評價誤當成發展回饋。</p></aside>
    <aside class="reading-callout"><span class="tool-label">專有名詞解釋</span><h3>行為單位</h3><p>「行為單位」是可以在特定場景中被觀察、描述與回饋的一個小動作，例如先邀請一位少發言的同事說明風險，等待五秒後再回應。它比「改善溝通」或「更有領導力」具體，適合用來設計練習與檢視變化。</p></aside>
    <aside class="reading-callout"><span class="tool-label">工具箱專欄</span><h3>一週行動卡</h3><ol><li><b>場景：</b>我會在哪一個會議或對話中練習？</li><li><b>動作：</b>我會開始、停止或繼續哪一個可觀察行為？</li><li><b>證據：</b>我會向誰取得什麼回應，判斷是否需要調整？</li></ol></aside>
    <div class="reading-summary"><span class="tool-label">深入閱讀收束</span><h3>總結提要</h3><ol><li>領導力要從抽象價值轉成別人看得見的行為。</li><li>教練對話同時看見意圖、行為、影響與情境限制，不急著替人下結論。</li><li>最有效的發展不是一次改好，而是用安全、可逆的小實驗取得新證據。</li><li>把承諾、回饋與檢視節點寫清楚，才能讓閱讀回到工作現場。</li></ol></div>'''
  approved_draft=ROOT/'reference_materials'/'chapters'/f'chapter_{i:02d}'/'02_deep_reading_draft.md'
  if approved_draft.exists():
    preserved_callouts=''.join(re.findall(r'<aside class="reading-callout">.*?</aside>', article, flags=re.S))
    if callout_path(ROOT, i).exists():
      preserved_callouts=render_chapter_callouts(load_chapter_callouts(ROOT, i))
    article=render_deep_reading_markdown(approved_draft.read_text(encoding='utf-8'))+preserved_callouts
  body=f'''<div class="top"><a class="brand" href="index.html" aria-label="返回卓越領導力©核心課程"><i>XL</i> 卓越領導力©核心課程</a><span id="saved" class="save">已儲存於本機</span></div><div class="layout"><aside class="side"><small>MODULE {i:02d}</small><h2>{html.escape(title)}</h2>{navhtml}</aside><main><section class="hero" id="s0"><small class="kicker">MODULE {i:02d}</small><h1>{html.escape(title)}<br><em>讓領導力成為可練習的行動</em></h1><p class="lead">{html.escape(lead)}</p><div class="journey-plan"><div><b>今天完成</b><span>閱讀、案例、自評與實驗規劃</span><small>約 50–70 分鐘</small></div><div><b>一週內完成</b><span>工作觀察與一次領導行為實驗</span><small>回到工作現場</small></div><div><b>行動後回來</b><span>引導式反思與行動整理</span><small>約 15–20 分鐘</small></div></div></section><section id="s1"><div class="head"><small class="kicker">01 DEEP READING</small><h2>深入閱讀</h2><p>{html.escape(desc)}</p></div><div class="reading-essay">{article}</div></section><section id="s2"><div class="head"><small class="kicker">02 LOCAL CASE</small><h2>工作案例</h2><p>台灣組織情境：跨部門協作、資源有限與關係維護同時存在。</p></div><div class="story"><p><b>情境：</b>新竹一家 180 人的電子製造公司裡，{html.escape(title)}是專案經理怡君最近被期待補強的能力。她的團隊要在六週內完成客戶試產，但研發、品保與業務對優先順序各有不同說法。</p><p>怡君的主管希望她「更有領導感」，卻只給了模糊的評語。她的同事阿哲則說：「你每次都很快給答案，我們反而不敢提出不同看法。」怡君想改善速度，又不想讓團隊覺得她失去掌控。你是她的內部教練，第一次對話要怎麼開始？</p></div><div class="case-contrast"><div><span>管理需求 A</span><h3>交付與速度</h3><p>客戶節點不能延後，決策需要有人承擔。</p></div><div><span>管理需求 B</span><h3>學習與關係</h3><p>跨部門信任不足，直接下令可能讓資訊更少。</p></div></div><div class="question"><b>三個提問</b><p>1. 你會先問什麼，以避免把「領導感」當成個性問題？</p><textarea data-key="caseAnswer"></textarea><p>2. 哪個行為證據最值得追問？3. 一週內可測試的最小改變是什麼？</p></div></section><section id="s3"><div class="head"><small class="kicker">03 DEVELOPMENTAL SELF-REFLECTION</small><h2>發展自評</h2><p>請以最近 30 天的真實行為作答：1 代表幾乎沒有，5 代表經常如此。這是學習工具，不是標準化測驗或人資決策工具。</p></div><div class="assess">{qhtml}</div><div class="assessment-actions"><button class="clear-button" id="clearAssessment">清除本章答案</button><button class="button" id="confirmAssessment">查看我的學習輪廓</button></div><div id="assessmentMessage" class="assessment-message"></div><div id="result" class="result"><div class="result-top"><div><h3>你的學習輪廓</h3><p>分數只提供對話起點；請用真實事件與他人回饋檢驗。</p></div><canvas id="radar" width="700" height="580"></canvas></div><div id="interpret" class="interpret"></div><div id="focusPicker" class="focus-picker"></div></div></section><section id="s4"><div class="head"><small class="kicker">04 OBSERVATION</small><h2>工作觀察</h2><p>這一段只記錄可驗證的事實，先不要急著解釋或評價。</p></div><div class="action-loop"><span>看見現況</span><b>→</b><span>試做改變</span><b>→</b><span>回看學習</span></div><div class="work"><label>情境、角色與任務<textarea data-key="observationSituation"></textarea></label><label>我看見的具體行為與對方反應<textarea data-key="observationBehavior"></textarea></label><label>結果與尚未解決之處<textarea data-key="observationResult"></textarea></label></div></section><section id="s5"><div class="experiment"><small class="kicker">05 BEHAVIOR EXPERIMENT</small><h2>一至兩週行為實驗</h2><p>承接 04 的觀察，只選一個能在工作現場測試的微小行動。</p><ol><li><b>01 行為</b><span>我會開始／停止／繼續……</span></li><li><b>02 場景</b><span>在誰、何時、哪個會議中做？</span></li><li><b>03 證據</b><span>我會觀察什麼反應或結果？</span></li></ol><textarea data-key="experiment"></textarea><label>回來檢視日期 <input type="date" data-key="followupDate"></label><div id="experimentFocus" class="experiment-focus">尚未選擇發展焦點</div></div></section><section id="s6"><div class="head"><small class="kicker">06 ACTION REVIEW</small><h2>行動回顧</h2><p>回到 04 的事實與 05 的實驗，整理影響、學習與下一步。</p></div><div id="reflection" class="reflect"></div><div class="final"><h3>帶走一句話</h3><p>我想在下一次教練對話中，刻意練習：</p><textarea data-key="commitment"></textarea></div></section></main></div><footer>資料只保存在目前瀏覽器／裝置的 localStorage；清除網站資料會刪除紀錄，沒有登入、雲端備份或跨裝置同步。請將人物與事件去識別化。</footer>'''
  body=body.replace(
    '<div class="assess">',
    '<div class="assessment-progress"><b>作答進度</b><span id="assessmentProgress" aria-live="polite">已完成 0／12</span></div>'
    '<div id="assessmentMessageTop" class="assessment-message assessment-message-top" role="alert" tabindex="-1"></div>'
    '<div class="assess">',
    1,
  )
  body=body.replace(
    '<div id="assessmentMessage" class="assessment-message"></div>',
    '<div id="assessmentMessage" class="assessment-message" role="alert"></div>',
    1,
  )
  body=re.sub(
    r'(<section id="s2">.*?<div class="question">.*?)(<textarea\b)',
    r'\1<p class="privacy-nudge"><b>書寫提醒：</b>請將人物與事件去識別化，不要輸入姓名、客戶名稱或其他可辨識資訊。</p>\2',
    body,
    count=1,
    flags=re.S,
  )
  callout_matches=re.findall(r'<aside class="reading-callout">.*?</aside>', article, flags=re.S)
  reading_cards=''.join(callout_matches)
  for card in callout_matches: body=body.replace(card,'',1)
  body=body.replace('<section id="s1">',reading_cards+'<section id="s1">',1)
  body=re.sub(r'<section id="s4">.*?</section><section id="s5">', '<section id="s4"><div class="head"><small class="kicker">04 WORK RECORD</small><h2>工作紀錄</h2><p>讀完文章與自評後，留下一段最值得帶回工作的觀察。</p></div><div class="simple-record"><label>我現在最想記住的情境、行為或提醒<textarea data-key="observationRecord"></textarea></label><label>給自己的話<textarea data-key="commitment"></textarea></label></div></section><section id="s5">', body, count=1, flags=re.S)
  body=re.sub(r'<section id="s5">.*?</section><section id="s6">', '<section id="s5"><div class="head"><small class="kicker">05 ACTION COMMITMENT</small><h2>行動承諾</h2><p>只選一個小到能在工作現場完成的行動，寫下時間與場景。</p></div><div class="simple-record action-commitment"><div id="experimentFocus" class="experiment-focus">尚未選擇發展焦點</div><label>我的行動<textarea data-key="experiment"></textarea></label><label class="action-date">預計實行日期 <input type="date" data-key="followupDate"></label></div></section><section id="s6">', body, count=1, flags=re.S)
  body=re.sub(r'<section id="s6">.*?</section></main>', '</main>', body, count=1, flags=re.S)
  body=re.sub(r'<footer(?:\s[^>]*)?>.*?</footer>', FOOTER, body, count=1, flags=re.S)
  runtime=(ROOT/'assets/chapter-runtime.js').read_text()
  conf={'chapter':i,'page_title':title,'content_version':'1.0.0','assessment_version':'1.0.0','storage_key':key,'dimensions':chapter_dims,'dimension_suffix':'','questions':questions,'focus_tips':{d:f'本週在「{d}」上做一個可被看見的小實驗。' for d in chapter_dims},'empty_focus_text':'尚未選擇發展焦點','reset_assessment_on_version_change':True,'assessment_mode':'behavior','chapter_reflection_prompt':f'在「{title}」上，你最想讓哪個人看見什麼改變？'}
  conf['editor_password_hash']=cfg.get('editor_password_hash','')
  shell=(ROOT/'templates/chapter_template.html').read_text().replace('{{PAGE_TITLE}}',title).replace('{{CSS}}',(ROOT/'assets/chapter.css').read_text()+(ROOT/'assets/editor-runtime.css').read_text()).replace('{{BODY}}',body).replace('{{CONFIG}}',json.dumps(conf,ensure_ascii=False)).replace('{{RUNTIME}}',(ROOT/'assets/editor-runtime.js').read_text()+'\n'+runtime)
  (ROOT/fn).write_text(shell)
  (ROOT/'content'/f'chapter_{i:02d}.json').write_text(json.dumps(conf,ensure_ascii=False,indent=2))
selected_modules=[(i,chapters[i-1]) for i in range(module_start,module_end+1)]
for i,c in selected_modules: page(i,*c)
for i,_ in selected_modules:
  if (ROOT/'content'/f'chapter_{i:02d}_learning.json').exists():
    update_chapter_learning_page(i)
index=(ROOT/'templates/index_template.html').read_text()
cards=''.join(f'<a class="map-card" href="{prefix}_Chapter{i:02d}.html"><small>MODULE {i:02d} · {""}</small><h3>{c[0]}</h3><p>{c[2]}</p><span>開始本模組 →</span></a>' for i,c in selected_modules)
custom='''<div class="top"><a class="brand" href="index.html" aria-label="學習中心首頁"><i>XL</i> 卓越領導力©核心課程</a></div><main class="home"><section class="home-hero"><small>FROM FEEDBACK TO PRACTICE</small><h1>把領導力，<em>練成日常。</em></h1><p>一個以領導力教練與組織學習為核心的繁體中文個人學習中心。從五項領導實踐出發，走過教練能力與流程，最後回到你自己的工作現場。</p><div class="journey"><b>11 章</b><span>從領導挑戰到教練精熟</span><b>1 個循環</b><span>閱讀 → 觀察 → 實驗 → 反思</span></div></section><section><small>LEARNING MAP</small><h2>選一章，帶一個真實議題進來。</h2><div class="map">'''+cards+'''</div></section><section class="home-note"><h2>使用前請知道</h2><p>頁面中的自評題目、案例與工作工具都是發展用途，不是標準化量表或人資決策工具。你的紀錄只保存在目前瀏覽器／裝置中；請將人物與事件去識別化。</p></section></main><footer>卓越領導力©核心課程 · 個人學習原型</footer>'''
custom=re.sub(r'<section class="home-note">.*?</section>','',custom,count=1,flags=re.S)
custom=custom.replace('11 章',f'{len(selected_modules)} 個模組')
custom=custom.replace('一個以領導力教練與組織學習為核心的繁體中文個人學習中心。從五項領導實踐出發，走過教練能力與流程，最後回到你自己的工作現場。',cfg.get('home_intro','一個把閱讀、觀察、實驗與反思帶回工作現場的繁體中文學習中心。'))
custom=custom.replace('選一章，帶一個真實議題進來。',cfg.get('home_map_heading','選一個模組，帶一個真實議題進來。'))
custom=re.sub(r'<footer(?:\s[^>]*)?>.*?</footer>',FOOTER,custom,count=1,flags=re.S)
css=''' :root{--ink:#17352e;--sage:#6f8f7b;--cream:#f5f1e8;--paper:#fcfbf7;--gold:#d49b52;--line:#d8ddd6;--muted:#64736d}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans TC",Arial,sans-serif;line-height:1.8}.top{height:64px;padding:0 6%;border-bottom:1px solid var(--line);display:flex;align-items:center}.brand{color:var(--ink);text-decoration:none;font-weight:700}.brand i{display:inline-grid;place-items:center;width:34px;height:34px;margin-right:10px;border-radius:50%;background:var(--ink);color:white;font:12px Georgia;font-style:normal}.home{max-width:1100px;margin:auto;padding:40px 6% 100px}.home-hero{padding:70px 0 100px;max-width:780px}.home-hero small,section>small{letter-spacing:.18em;color:#76552f;font-size:11px}.home-hero h1{font:58px/1.12 Georgia;margin:18px 0}.home-hero em{color:var(--sage);font-weight:400;font-style:normal}.home-hero p{font:20px/1.9 Georgia;color:#456057}.journey{display:grid;grid-template-columns:auto 1fr auto 1fr;gap:12px 25px;margin-top:40px;padding:20px;background:var(--cream);align-items:center}.journey b{font:28px Georgia}.journey span{font-size:13px;color:var(--muted)}h2{font:36px Georgia;margin:8px 0 28px}.map{display:grid;grid-template-columns:repeat(2,1fr);gap:15px}.map-card{display:block;text-decoration:none;color:var(--ink);padding:25px;background:#fff;border:1px solid var(--line);transition:.2s}.map-card:hover,.map-card:focus-visible{transform:translateY(-3px);border-color:var(--gold);outline:2px solid var(--gold);outline-offset:2px}.map-card small{color:#76552f;font-size:10px;letter-spacing:.14em}.map-card h3{font:25px Georgia;margin:10px 0}.map-card p{color:var(--muted);font-size:13px}.map-card span{font-size:12px;color:#76552f}.home-note{margin-top:70px;border-top:1px solid var(--line);padding-top:35px;max-width:700px}.home-note p{color:var(--muted);font-size:14px}footer{padding:30px 6%;background:#102a25;color:white;font-size:12px}@media(max-width:700px){.home-hero h1{font-size:44px}.journey{grid-template-columns:1fr 2fr}.map{grid-template-columns:1fr}}'''
index=index.replace('<html lang="en">','<html lang="zh-Hant">').replace('{{PROJECT_TITLE}}',cfg['project_title']).replace('{{CSS}}',css)
if '<style>' in index and '</style>' in index:
  a=index.find('<style>')+len('<style>'); b=index.find('</style>',a)
  index=index[:a]+css+index[b:]
index=index.replace(index[index.find('<body'):index.find('</body>')+7], '<body class="home-page">'+custom+'</body>')
(ROOT/'index.html').write_text(index)
