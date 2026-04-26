#!/usr/bin/env python3
"""
RVGPT 3.0 - Ultimate AI Assistant
Premium design with logo, image support, and effects.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import base64
from pathlib import Path
import threading
import time
import webbrowser

try:
    import requests
except ImportError:
    os.system("pip3 install requests")
    import requests

# ========================
# CONFIG - EDIT LINE 26
# ========================
GEMINI_API_KEY = "AIzaSyCeoSNnyWAxA2p2zH58xUxGAnW1lQBZPco"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Load logo path
LOGO_URL = "/RV.png"
logo_path = Path("RV.png")
if not logo_path.exists():
    print("⚠️  RV.png not found!")

# ========================
# CSS
# ========================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Poppins', sans-serif;
    background: #0f0f1a;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    color: #fff;
}

.app {
    width: 100%;
    max-width: 500px;
    height: 92vh;
    max-height: 850px;
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 30px 100px rgba(0,0,0,0.6);
}

/* Header */
.header {
    padding: 24px 28px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    gap: 14px;
    position: relative;
}

.logo {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    object-fit: cover;
    background: rgba(255,255,255,0.2);
}

.logo-fallback {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: rgba(255,255,255,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.logo-text { flex: 1; }

.logo-text h1 {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.logo-text span {
    font-size: 0.8rem;
    opacity: 0.9;
}

.status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    background: rgba(255,255,255,0.15);
    padding: 6px 12px;
    border-radius: 20px;
}

.dot {
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Chat */
.chat {
    flex: 1;
    overflow-y: auto;
    padding: 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.chat::-webkit-scrollbar { width: 4px; }
.chat::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

.msg {
    display: flex;
    gap: 10px;
    animation: slide 0.3s ease;
}

@keyframes slide {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.msg.user { flex-direction: row-reverse; }

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}

.msg.bot .avatar { background: linear-gradient(135deg, #667eea, #764ba2); }
.msg.user .avatar { background: #2d2d44; }

.content {
    max-width: 78%;
    padding: 14px 18px;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.6;
}

.msg.bot .content {
    background: #252538;
    border-top-left-radius: 6px;
}

.msg.user .content {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-top-right-radius: 6px;
}

.content img {
    max-width: 100%;
    border-radius: 12px;
    margin-top: 10px;
}

.typing {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 0;
    color: #666;
    font-size: 0.85rem;
}

.dots { display: flex; gap: 4px; }
.dots span {
    width: 6px;
    height: 6px;
    background: #666;
    border-radius: 50%;
    animation: bounce 1.4s infinite;
}
.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-8px); }
}

/* Input */
.input-area {
    padding: 16px 20px 24px;
    background: #12121c;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.img-preview {
    display: none;
    margin-bottom: 12px;
    position: relative;
}

.img-preview.show { display: block; }

.img-preview img {
    width: 100%;
    max-height: 120px;
    object-fit: contain;
    border-radius: 12px;
    background: #1a1a2e;
}

.img-preview .remove {
    position: absolute;
    top: 6px;
    right: 6px;
    width: 22px;
    height: 22px;
    background: #ef4444;
    border: none;
    border-radius: 50%;
    color: #fff;
    cursor: pointer;
    font-size: 0.7rem;
}

.input-row {
    display: flex;
    gap: 10px;
    align-items: center;
}

.input-row input {
    flex: 1;
    padding: 14px 18px;
    background: #1e1e32;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    color: #fff;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.2s;
}

.input-row input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.input-row input::placeholder { color: #555; }

.btn {
    width: 50px;
    height: 50px;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn.img { background: #1e1e32; color: #667eea; border: 1px solid rgba(102,126,234,0.3); }
.btn.img:hover { background: #667eea; color: #fff; }
.btn.send { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; }
.btn.send:hover { transform: scale(1.05); }

.hidden { display: none; }

/* Tracker */
.tracker {
    padding: 12px 20px;
    background: #0f0f16;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex;
    gap: 8px;
    overflow-x: auto;
}

.tracker::-webkit-scrollbar { height: 3px; }
.tracker::-webkit-scrollbar-thumb { background: #333; }

.item {
    flex-shrink: 0;
    background: #1e1e32;
    padding: 6px 12px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
}

.item span:first-child { font-size: 1rem; }
.item .sold { color: #22c55e; }
</style>
"""

# ========================
# HTML
# ========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RVGPT</title>
    """ + CSS + """
</head>
<body>
    <div class="app">
        <div class="header">
            <img src="RV.png" class="logo" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
            <div class="logo-fallback" style="display:none">RV</div>
            <div class="logo-text">
                <h1>RVGPT</h1>
                <span>Your AI Assistant</span>
            </div>
            <div class="status">
                <div class="dot" id="dot"></div>
                <span id="status">Online</span>
            </div>
        </div>
        
        <div class="chat" id="chat">
            <div class="msg bot">
                <div class="avatar">✨</div>
                <div class="content">
                    Hey there! 👋 I'm <strong>RVGPT</strong><br><br>
                    I can help you with:<br>
                    💬 Answer questions<br>
                    🖼️ Analyze images<br>
                    📊 Track products<br><br>
                    What can I help you with today?
                </div>
            </div>
        </div>
        
        <div class="input-area">
            <div class="img-preview" id="preview">
                <img id="previewImg" src="">
                <button class="remove" onclick="removeImg()">✕</button>
            </div>
            <div class="input-row">
                <button class="btn img" onclick="document.getElementById('fileInput').click()">🖼️</button>
                <input type="text" id="input" placeholder="Ask RVGPT anything..." onkeypress="if(event.key==='Enter')send()">
                <button class="btn send" onclick="send()">➤</button>
            </div>
            <input type="file" class="hidden" id="fileInput" accept="image/*" onchange="handleImg(this)">
        </div>
        
        <div class="tracker" id="tracker">
            <div class="item">📦 No orders tracked</div>
        </div>
    </div>
    
    <script>
    let img = null;
    
    function handleImg(f) {{
        if (f.files && f.files[0]) {{
            const r = new FileReader();
            r.onload = (e) => {{
                img = e.target.result;
                document.getElementById('previewImg').src = img;
                document.getElementById('preview').classList.add('show');
            }};
            r.readAsDataURL(f.files[0]);
        }}
    }}
    
    function removeImg() {{
        img = null;
        document.getElementById('fileInput').value = '';
        document.getElementById('preview').classList.remove('show');
    }}
    
    async function send() {{
        const text = document.getElementById('input').value.trim();
        if (!text && !img) return;
        
        addMsg(text, img, 'user');
        document.getElementById('input').value = '';
        showTyping();
        
        try {{
            const fd = new FormData();
            fd.append('message', text);
            if (img) fd.append('image', img.split(',')[1]);
            
            const res = await fetch('/chat', {{ method: 'POST', body: fd }});
            const data = await res.json();
            hideTyping();
            addMsg(data.response || 'Error', null, 'bot');
        }} catch (e) {{
            hideTyping();
            addMsg('Connection error. Is server running?', null, 'bot');
        }}
    }}
    
    function addMsg(text, image, type) {{
        const chat = document.getElementById('chat');
        chat.innerHTML += `
            <div class="msg ${{type}}">
                <div class="avatar">${{type === 'bot' ? '✨' : '👤'}}</div>
                <div class="content">${{text}}${{image ? '<img src="' + image + '">' : ''}}</div>
            </div>
        `;
        chat.scrollTop = chat.scrollHeight;
    }}
    
    function showTyping() {{
        document.getElementById('chat').innerHTML += `
            <div class="msg bot" id="typing">
                <div class="avatar">✨</div>
                <div class="content">
                    <div class="typing">typing <div class="dots"><span></span><span></span><span></span></div></div>
                </div>
            </div>
        `;
    }}
    
    function hideTyping() {{
        const t = document.getElementById('typing');
        if (t) t.remove();
    }}
    
    function checkStatus() {{
        fetch('/status').then(r=>r.json()).then(d => {{
            if (d.ai_configured) {{
                document.getElementById('dot').style.background = '#22c55e';
                document.getElementById('status').textContent = 'Online';
            }} else {{
                document.getElementById('dot').style.background = '#f59e0b';
                document.getElementById('status').textContent = 'No Key';
            }}
        }});
    }}
    
    function loadTracker() {{
        fetch('/tracker').then(r=>r.json()).then(d => {{
            const t = document.getElementById('tracker');
            if (d.top && d.top.length > 0) {{
                t.innerHTML = d.top.slice(0,5).map(p => `
                    <div class="item">
                        <span>${{p.emoji || '📦'}}</span>
                        <span>${{p.name}}</span>
                        <span class="sold">${{p.qty}} sold</span>
                    </div>
                `).join('');
            }}
        }});
    }}
    
    checkStatus();
    loadTracker();
    setInterval(loadTracker, 30000);
    </script>
</body>
</html>
"""

# ========================
# SERVER
# ========================
class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()
    
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ai_configured": bool(GEMINI_API_KEY)}).encode())
        elif self.path == "/tracker":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"top": get_stats()}).encode())
        elif self.path == "/RV.png":
            try:
                with open("RV.png", "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "image/png")
                    self.end_headers()
                    self.wfile.write(f.read())
            except:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == "/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(content_length).decode()
            from urllib.parse import parse_qs
            params = parse_qs(data)
            message = params.get("message", [""])[0]
            image_b64 = params.get("image", [None])[0]
            
            response = ask_gemini(message, image_b64) if GEMINI_API_KEY else "Add API key to rvgpt3.py"
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"response": response}).encode())


def get_stats():
    stats = {}
    file = Path.home() / ".rvgpt_storage.json"
    if file.exists():
        try:
            data = json.loads(file.read_text())
            stats = data.get("product_stats", {})
        except: pass
    return [{"name": k, "qty": v, "emoji": "📦"} for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10]]


def ask_gemini(prompt, image_b64=None):
    parts = [{"text": f"You are RVGPT, a helpful AI assistant. Keep responses friendly and concise.\n\n{prompt}"}]
    if image_b64:
        parts.append({"inlineData": {"mimeType": "image/png", "data": image_b64}})
    
    data = {"contents": [{"parts": parts}], "generationConfig": {"maxOutputTokens": 300, "temperature": 0.7}}
    
    res = requests.post(GEMINI_URL + "?key=" + GEMINI_API_KEY, json=data, timeout=60)
    result = res.json()
    
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    return result.get("error", {}).get("message", "No response")


def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:8080")


if __name__ == "__main__":
    print("=" * 50)
    print("  RVGPT 3.0 - Ultimate AI Assistant")
    print("=" * 50)
    print()
    if not GEMINI_API_KEY:
        print("⚠️  Add API key on line 26:")
        print("    GEMINI_API_KEY = 'YOUR_KEY'")
        print("    Get free key: https://aistudio.google.com/apikey")
        print()
    print("🌐 Opening http://localhost:8080")
    print()
    threading.Thread(target=open_browser, daemon=True).start()
    HTTPServer(("localhost", 8080), Handler).serve_forever()