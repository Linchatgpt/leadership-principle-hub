#!/usr/bin/env python3
"""Local-only editor server. Run from this project directory: python3 admin_server.py"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib, json, re
ROOT = Path(__file__).resolve().parent
PORT = 8765
PASSWORD_HASH = ""
HISTORY = ROOT / ".admin_history"
HISTORY.mkdir(exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/admin.html":
            source=(ROOT/"admin.html").read_text(encoding="utf-8")
            source=source.replace('</head>', '<link rel="stylesheet" href="assets/chapter.css"></head>', 1)
            source=source.replace('<link rel="stylesheet" href="https://cdn.ckeditor.com/ckeditor5/48.3.1/ckeditor5.css">','<link rel="stylesheet" href="assets/chapter.css">')
            source=source.replace('<script type="module">', '<script src="assets/ckeditor5.bundle.js"></script><script type="module">', 1)
            source=source.replace("import{ClassicEditor,Essentials,Paragraph,Bold,Italic,Font,Undo,Heading,BlockQuote,Link,List}from'ckeditor5';", "const {ClassicEditor,Essentials,Paragraph,Bold,Italic,Font,Heading,BlockQuote,Link,List}=window;")
            source=source.replace("import { ClassicEditor, Essentials, Paragraph, Bold, Italic, Font, Heading, BlockQuote, Link, List } from 'ckeditor5';", "const { ClassicEditor, Essentials, Paragraph, Bold, Italic, Font, Heading, BlockQuote, Link, List } = window;")
            source=source.replace("ClassicEditor.create($('editor'),{", "ClassicEditor.create($('editor'),{initialData:data,")
            source=source.replace("licenseKey:'GPL',", "")
            source=source.replace("fontFamily:{options:['default','Arial','Georgia','Noto Sans TC','Courier New']}})}", "fontFamily:{options:['default','Arial','Georgia','Noto Sans TC','Courier New']}});editor.disableReadOnlyMode('admin')}")
            source=source.replace('<option value="1">100% 一般</option><option value="0.5">50% 一半</option><option value="0.75">75% 較小</option><option value="1.25">125% 較大</option><option value="1.5">150% 大標題</option>', '<option value="12px">12px</option><option value="14px">14px</option><option value="16px">16px</option><option value="20px">20px</option><option value="24px">24px</option><option value="32px">32px</option>')
            sync="<script>let editHistory=[],editFuture=[],historyBusy=false;setTimeout(()=>{editHistory=[editor.innerHTML];new MutationObserver(()=>{if(historyBusy)return;const h=editor.innerHTML;if(h!==editHistory[editHistory.length-1]){editHistory.push(h);if(editHistory.length>30)editHistory.shift();editFuture=[]}}).observe(editor,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['style','color','size']})},250);let savedRange=null;document.addEventListener('selectionchange',()=>{const s=getSelection(),ed=$('editor');if(s.rangeCount&&ed.contains(s.anchorNode))savedRange=s.getRangeAt(0).cloneRange()});function editBlock(){const s=getSelection(),ed=$('editor');if(!s.rangeCount||!ed.contains(s.anchorNode)){$('status').textContent='請先把游標放在要修改的文字區塊';return null}let e=s.anchorNode.nodeType===3?s.anchorNode.parentElement:s.anchorNode;const inline=e.closest&&e.closest('font,em,i');if(inline&&ed.contains(inline))return inline;return e.closest('h1,h2,h3,p,li,blockquote')||e}$('font').onchange=()=>{const e=editBlock();if(e){const v=$('font').value;if(v)e.style.fontFamily=v;else e.style.removeProperty('font-family')}};$('size').onchange=()=>{const e=editBlock();if(e)e.style.fontSize=$('size').value};$('color').onchange=()=>{$('applyColor').click()};$('applyColor').onclick=()=>{if(savedRange){const s=getSelection();s.removeAllRanges();s.addRange(savedRange);editor.focus()}const e=editBlock();if(e)e.style.color=$('color').value};$('formatUndo').onclick=()=>{if(editHistory.length>1){editFuture.push(editHistory.pop());editor.innerHTML=editHistory[editHistory.length-1]}};$('formatRedo').onclick=()=>{if(editFuture.length){const v=editFuture.pop();editHistory.push(v);editor.innerHTML=v}};$('listType').onchange=()=>{if(savedRange){const s=getSelection();s.removeAllRanges();s.addRange(savedRange);editor.focus()}if($('listType').value)document.execCommand($('listType').value,false,null);$('listType').value=''};$('link').onclick=()=>{const u=prompt('請輸入連結網址','https://');if(!u)return;const s=getSelection();if(savedRange){s.removeAllRanges();s.addRange(savedRange);document.execCommand('createLink',false,u)}else{const e=editBlock();if(e)e.innerHTML='<a href=\"'+u+'\" target=\"_blank\" rel=\"noopener\">'+e.innerHTML+'</a>'}};</script>"
            source=source.replace('</body>', sync+'</body>', 1)
            source=source.replace("$('size').value+'em'", "$('size').value")
            source=source.replace('<option value="12px">12px</option><option value="14px">14px</option>', '<option value="">選擇字級</option><option value="12px">12px</option><option value="14px">14px</option>')
            body=source.encode('utf-8'); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body); return
        return super().do_GET()
    def do_POST(self):
        if self.path not in ("/api/save", "/api/undo"): self.send_error(404); return
        try: data=json.loads(self.rfile.read(int(self.headers.get("Content-Length","0"))))
        except Exception: self.send_error(400,"Invalid JSON"); return
        if PASSWORD_HASH and hashlib.sha256(data.get("password","").encode()).hexdigest()!=PASSWORD_HASH: self.send_error(403,"Password rejected"); return
        page=data.get("page","")
        if not re.fullmatch(r"LPI_Coach_Chapter\d{2}\.html",page): self.send_error(400,"Invalid page"); return
        path=ROOT/page
        if not path.exists(): self.send_error(404); return
        source=path.read_text(encoding="utf-8")
        history_path=HISTORY / f"{page}.json"
        history=json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
        if self.path == "/api/undo":
            if not history: self.send_error(409,"No previous state"); return
            path.write_text(history.pop(),encoding="utf-8")
            history_path.write_text(json.dumps(history,ensure_ascii=False),encoding="utf-8")
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(b'{"ok":true}'); return
        history.append(source); history_path.write_text(json.dumps(history[-20:],ensure_ascii=False),encoding="utf-8")
        source=re.sub(r"<main>.*?</main>","<main>"+data.get("main","")+"</main>",source,count=1,flags=re.S)
        css=f":root{{--reader-font-size:{float(data.get('fontSize',1))};--reader-text-color:{data.get('textColor','#17352e')};}}"
        if 'id="admin-overrides"' in source: source=re.sub(r'<style id="admin-overrides">.*?</style>',f'<style id="admin-overrides">{css}</style>',source,count=1,flags=re.S)
        else: source=source.replace("</head>",f'<style id="admin-overrides">{css}</style></head>',1)
        path.write_text(source,encoding="utf-8")
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(b'{"ok":true}')
if __name__ == "__main__":
    print(f"管理頁：http://127.0.0.1:{PORT}/admin.html")
    ThreadingHTTPServer(("127.0.0.1",PORT),Handler).serve_forever()
