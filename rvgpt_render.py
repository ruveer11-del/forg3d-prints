#!/usr/bin/env python3
"""
RVGPT 3.0 - For Render deployment (WSGI + Gunicorn)
"""

from wsgiref.simple_server import make_server
import json
import os
import base64
from pathlib import Path

try:
    import requests
except ImportError:
    import pip
    pip.main(['install', 'requests'])
    import requests

# ========================
# CONFIG
# ========================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCeoSNnyWAxA2p2zH58xUxGAnW1lQBZPco")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

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

.header {
    padding: 24px 28px;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    display: flex;
    align-items: center;
    gap: 14px;
}

.logo { width: 48px; height: 48px; border-radius: 14px; object-fit: cover; background: rgba(255,255,255,0.2); }
.logo-text { flex: 1; }
.logo-text h1 { font-size: 1.4rem; font-weight: 700; }
.logo-text span { font-size: 0.8rem; opacity: 0.9; }

.status { display: flex; align-items: center; gap: 6px; font-size: 0.75rem; background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 20px; }
.dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

.chat { flex: 1; overflow-y: auto; padding: 20px 24px; display: flex; flex-direction: column; gap: 14px; }
.chat::-webkit-scrollbar { width: 4px; }
.chat::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

.msg { display: flex; gap: 10px; animation: slide 0.3s ease; }
@keyframes slide { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.msg.user { flex-direction: row-reverse; }

.avatar { width: 36px; height: 36px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.msg.bot .avatar { background: linear-gradient(135deg, #1e3c72, #2a5298); }
.msg.user .avatar { background: #2d2d44; }

.content { max-width: 78%; padding: 14px 18px; border-radius: 18px; font-size: 0.95rem; line-height: 1.6; }
.msg.bot .content { background: #252538; border-top-left-radius: 6px; }
.msg.user .content { background: linear-gradient(135deg, #1e3c72, #2a5298); border-top-right-radius: 6px; }

.typing { display: flex; align-items: center; gap: 8px; padding: 10px 0; color: #666; font-size: 0.85rem; }
.dots { display: flex; gap: 4px; }
.dots span { width: 6px; height: 6px; background: #666; border-radius: 50%; animation: bounce 1.4s infinite; }
.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-8px); } }

.input-area { padding: 16px 20px 24px; background: #12121c; border-top: 1px solid rgba(255,255,255,0.05); }
.input-row { display: flex; gap: 10px; align-items: center; }
.input-row input { flex: 1; padding: 14px 18px; background: #1e1e32; border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; color: #fff; font-size: 0.95rem; outline: none; }
.input-row input:focus { border-color: #1e3c72; box-shadow: 0 0 0 3px rgba(30,60,114,0.2); }
.input-row input::placeholder { color: #555; }

.btn { width: 50px; height: 50px; border: none; border-radius: 14px; cursor: pointer; font-size: 1.2rem; transition: all 0.2s; display: flex; align-items: center; justify-content: center; }
.btn.img { background: #1e1e32; color: #1e3c72; }
.btn.img:hover { background: #1e3c72; color: #fff; }
.btn.send { background: linear-gradient(135deg, #1e3c72, #2a5298); color: #fff; }
.btn.send:hover { transform: scale(1.05); }

.hidden { display: none; }

.tracker { padding: 12px 20px; background: #0f0f16; border-top: 1px solid rgba(255,255,255,0.05); display: flex; gap: 8px; overflow-x: auto; }
.tracker::-webkit-scrollbar { height: 3px; }
.tracker::-webkit-scrollbar-thumb { background: #333; }
.item { flex-shrink: 0; background: #1e1e32; padding: 6px 12px; border-radius: 20px; display: flex; align-items: center; gap: 6px; font-size: 0.75rem; }
.item span:first-child { font-size: 1rem; }
.item .sold { color: #22c55e; }
</style>
"""

HTML = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RVGPT</title>
    {CSS}
</head>
<body>
    <div class="app">
        <div class="header">
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
                    I can help you with questions, analyze images, and more.<br><br>
                    What can I help you with today?
                </div>
            </div>
        </div>
        
        <div class="input-area">
            <div class="input-row">
                <input type="text" id="input" placeholder="Ask RVGPT anything..." onkeypress="if(event.key==='Enter')send()">
                <button class="btn send" onclick="send()">➤</button>
            </div>
        </div>
        
        <div class="tracker" id="tracker">
            <div class="item">📦 No orders yet</div>
        </div>
    </div>
    
    <script>
    async function send() {{
        const text = document.getElementById('input').value.trim();
        if (!text) return;
        
        addMsg(text, 'user');
        document.getElementById('input').value = '';
        showTyping();
        
        try {{
            const res = await fetch('/chat', {{ method: 'POST', body: JSON.stringify({{message: text}}), headers: {{'Content-Type': 'application/json'}} }});
            const data = await res.json();
            hideTyping();
            addMsg(data.response || 'Error', 'bot');
        }} catch (e) {{
            hideTyping();
            addMsg('Connection error. Please try again.', 'bot');
        }}
    }}
    
    function addMsg(text, type) {{
        const chat = document.getElementById('chat');
        chat.innerHTML += `<div class="msg ${{type}}"><div class="avatar">${{type === 'bot' ? '✨' : '👤'}}</div><div class="content">${{text}}</div></div>`;
        chat.scrollTop = chat.scrollHeight;
    }}
    
    function showTyping() {{
        document.getElementById('chat').innerHTML += `<div class="msg bot" id="typing"><div class="avatar">✨</div><div class="content"><div class="typing">typing <div class="dots"><span></span><span></span><span></span></div></div></div></div>`;
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
        }}).catch(() => {{}});
    }}
    
    checkStatus();
    </script>
</body>
</html>
"""

def ask_gemini(prompt, image_b64=None):
    parts = [{"text": f"You are RVGPT, a helpful AI assistant. Keep responses friendly and concise.\n\n{prompt}"}]
    if image_b64:
        parts.append({"inlineData": {"mimeType": "image/png", "data": image_b64}})
    
    data = {"contents": [{"parts": parts}], "generationConfig": {"maxOutputTokens": 500, "temperature": 0.7}}
    
    try:
        res = requests.post(GEMINI_URL + "?key=" + GEMINI_API_KEY, json=data, timeout=60)
        result = res.json()
        
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        return result.get("error", {}).get("message", "No response")
    except Exception as e:
        return f"Error: {str(e)}"

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    
    if path == "/" or path == "/index.html":
        start_response("200 OK", [("Content-Type", "text/html")])
        return [HTML.encode()]
    
    elif path == "/status":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps({"ai_configured": bool(GEMINI_API_KEY)}).encode()]
    
    elif path == "/chat":
        import cgi
        length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(length).decode()
        try:
            data = json.loads(body)
            message = data.get("message", "")
        except:
            message = body
        
        response = ask_gemini(message)
        
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps({"response": response}).encode()]
    
    else:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Not Found"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Starting RVGPT on port {port}...")
    with make_server("", port, app) as httpd:
        print(f"   Visit: http://localhost:{port}")
        httpd.serve_forever()