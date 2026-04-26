#!/usr/bin/env python3
"""
RVGPT 2.0 - Premium AI Assistant
A sleek, modern chatbot with text, voice, and image support.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
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
# CONFIG - EDIT LINE 34
# ========================
GEMINI_API_KEY = "AIzaSyCeoSNnyWAxA2p2zH58xUxGAnW1lQBZPco"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

# ========================
# PREMIUM CSS
# ========================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0a0a0f;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    color: #fff;
}

.app {
    width: 100%;
    max-width: 480px;
    height: 90vh;
    max-height: 800px;
    background: linear-gradient(180deg, #12121a 0%, #1a1a24 100%);
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 25px 80px rgba(0,0,0,0.5);
}

/* Header */
.header {
    padding: 24px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    position: relative;
}

.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-text {
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    opacity: 0.9;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.header-subtitle {
    font-size: 0.85rem;
    opacity: 0.9;
}

/* Chat Area */
.chat {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.chat::-webkit-scrollbar { width: 6px; }
.chat::-webkit-scrollbar-track { background: transparent; }
.chat::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

/* Messages */
.msg {
    display: flex;
    gap: 10px;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.msg.user { flex-direction: row-reverse; }

.msg-avatar {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}

.msg.bot .msg-avatar { background: linear-gradient(135deg, #6366f1, #a855f7); }
.msg.user .msg-avatar { background: #1e1e28; }

.msg-content {
    max-width: 80%;
    padding: 14px 18px;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.6;
}

.msg.bot .msg-content {
    background: #1e1e28;
    border-top-left-radius: 4px;
}

.msg.user .msg-content {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-top-right-radius: 4px;
}

.msg-content img {
    max-width: 100%;
    border-radius: 12px;
    margin-top: 10px;
}

.typing {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #666;
    font-size: 0.85rem;
    padding: 10px 0;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 6px;
    height: 6px;
    background: #666;
    border-radius: 50%;
    animation: bounce 1.4s infinite;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-6px); }
}

/* Input Area */
.input-area {
    padding: 16px 20px 24px;
    background: #12121a;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.input-row {
    display: flex;
    gap: 10px;
    align-items: center;
}

.input-row input {
    flex: 1;
    padding: 14px 18px;
    background: #1e1e28;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    color: #fff;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.2s;
}

.input-row input:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.input-row input::placeholder { color: #555; }

.icon-btn {
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-btn.voice {
    background: #1e1e28;
    color: #6366f1;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.icon-btn.voice:hover {
    background: #6366f1;
    color: #fff;
}

.icon-btn.voice.listening {
    background: #6366f1;
    color: #fff;
    animation: glow 1s infinite;
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.5); }
    50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.8); }
}

.icon-btn.send {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: #fff;
}

.icon-btn.send:hover {
    transform: scale(1.05);
}

.hidden-input { display: none; }

/* Image Preview */
.img-preview {
    display: none;
    margin-bottom: 12px;
    position: relative;
}

.img-preview.show { display: block; }

.img-preview img {
    width: 100%;
    max-height: 150px;
    object-fit: contain;
    border-radius: 12px;
    background: #1e1e28;
}

.img-preview .remove {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 24px;
    height: 24px;
    background: #ef4444;
    border: none;
    border-radius: 50%;
    color: #fff;
    cursor: pointer;
    font-size: 0.8rem;
}

/* Tracker Bar */
.tracker-bar {
    padding: 12px 20px;
    background: #0f0f14;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex;
    gap: 8px;
    overflow-x: auto;
}

.tracker-bar::-webkit-scrollbar { height: 4px; }
.tracker-bar::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

.tracker-item {
    flex-shrink: 0;
    background: #1e1e28;
    padding: 6px 12px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    white-space: nowrap;
}

.tracker-item span:first-child { font-size: 1rem; }
.tracker-item .sold { color: #22c55e; }
</style>
"""

# ========================
# HTML
# ========================
HTML = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RVGPT 2.0</title>
    {CSS}
</head>
<body>
    <div class="app">
        <div class="header">
            <div class="header-top">
                <div class="logo">
                    <img src="RV.png" style="width:40px;height:40px;border-radius:12px;" onerror="this.style.display='none'">
                    <span class="logo-text">RVGPT</span>
                </div>
                <div class="status-indicator">
                    <div class="status-dot" id="statusDot"></div>
                    <span id="statusText">Online</span>
                </div>
            </div>
            <p class="header-subtitle">Your intelligent assistant</p>
        </div>
        
        <div class="chat" id="chat">
            <div class="msg bot">
                <div class="msg-avatar">✨</div>
                <div class="msg-content">
                    Hey! I'm <strong>RVGPT</strong> ✨<br><br>
                    I'm here to help with anything you need:<br><br>
                    💬 <strong>Chat</strong> - Ask me anything<br>
                    🖼️ <strong>Images</strong> - Send me pictures<br>
                    📊 <strong>Products</strong> - Track orders<br><br>
                    What would you like to do today?
                </div>
            </div>
        </div>
        
        <div class="input-area">
            <div class="img-preview" id="imgPreview">
                <img id="previewImg" src="">
                <button class="remove" onclick="removeImg()">✕</button>
            </div>
            
            <div class="input-row">
                <input type="text" id="userInput" placeholder="Message RVGPT..." onkeypress="if(event.key==='Enter')send()">
                <button class="icon-btn send" onclick="send()">➤</button>
            </div>
            <input type="file" class="hidden-input" id="imgInput" accept="image/*" onchange="handleImg(this)">
        </div>
        
        <div class="tracker-bar" id="trackerBar">
            <div class="tracker-item">📦 No orders yet</div>
        </div>
    </div>
    
    <script>
    let attachedImg = null;
    let isListening = false;
    let rec = null;
    
    // Speech Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        rec = new SR();
        rec.continuous = false;
        rec.interimResults = true;
        
        rec.onresult = (e) => {{
            const text = Array.from(e.results).map(r => r[0].transcript).join('');
            document.getElementById('userInput').value = text;
            if (e.results[0].isFinal) send();
        }};
        
        rec.onend = () => {{
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
        }};
    }}
    
    function toggleVoice() {{
        if (!rec) {{ addBot('🎤 Voice not supported. Try Chrome!'); return; }}
        
        if (isListening) {{
            rec.stop();
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
        }} else {{
            rec.start();
            isListening = true;
            document.getElementById('voiceBtn').classList.add('listening');
        }}
    }}
    
    function handleImg(input) {{
        if (input.files && input.files[0]) {{
            const reader = new FileReader();
            reader.onload = (e) => {{
                attachedImg = e.target.result;
                document.getElementById('previewImg').src = attachedImg;
                document.getElementById('imgPreview').classList.add('show');
            }};
            reader.readAsDataURL(input.files[0]);
        }}
    }}
    
    function removeImg() {{
        attachedImg = null;
        document.getElementById('imgInput').value = '';
        document.getElementById('imgPreview').classList.remove('show');
    }}
    
    async function send() {{
        const input = document.getElementById('userInput');
        const text = input.value.trim();
        if (!text && !attachedImg) return;
        
        addUser(text, attachedImg);
        input.value = '';
        showTyping();
        
        try {{
            const formData = new FormData();
            formData.append('message', text);
            if (attachedImg) formData.append('image', attachedImg.split(',')[1]);
            
            const res = await fetch('/chat', {{ method: 'POST', body: formData }});
            const data = await res.json();
            hideTyping();
            
            if (data.success) {{
                addBot(data.response);
                speak(data.response);
            }} else {{
                addBot('Error: ' + (data.error || 'Check API key'));
            }}
        }} catch (e) {{
            hideTyping();
            addBot('Connection error. Is RVGPT running?');
        }}
    }}
    
    function addUser(text, img) {{
        const chat = document.getElementById('chat');
        chat.innerHTML += `
            <div class="msg user">
                <div class="msg-avatar">👤</div>
                <div class="msg-content">${{text}}${{img ? '<img src="' + img + '">' : ''}}</div>
            </div>
        `;
        chat.scrollTop = chat.scrollHeight;
    }}
    
    function addBot(text) {{
        const chat = document.getElementById('chat');
        chat.innerHTML += `
            <div class="msg bot">
                <div class="msg-avatar">✨</div>
                <div class="msg-content">${{text.replace(/\\n/g, '<br>')}}</div>
            </div>
        `;
        chat.scrollTop = chat.scrollHeight;
    }}
    
    function showTyping() {{
        const chat = document.getElementById('chat');
        chat.innerHTML += `
            <div class="msg bot" id="typingMsg">
                <div class="msg-avatar">✨</div>
                <div class="msg-content">
                    <div class="typing">
                        <span>typing</span>
                        <div class="typing-dots"><span></span><span></span><span></span></div>
                    </div>
                </div>
            </div>
        `;
        chat.scrollTop = chat.scrollHeight;
    }}
    
    function hideTyping() {{
        const typing = document.getElementById('typingMsg');
        if (typing) typing.remove();
    }}
    
    function speak(text) {{
        if (!('speechSynthesis' in window)) return;
        const u = new SpeechSynthesisUtterance(text);
        u.rate = 1;
        speechSynthesis.speak(u);
    }}
    
    function loadTracker() {{
        fetch('/tracker').then(r => r.json()).then(data => {{
            const bar = document.getElementById('trackerBar');
            if (data.top && data.top.length > 0) {{
                bar.innerHTML = data.top.slice(0, 5).map(p => `
                    <div class="tracker-item">
                        <span>${{p.emoji || '📦'}}</span>
                        <span>${{p.name}}</span>
                        <span class="sold">${{p.qty}} sold</span>
                    </div>
                `).join('');
            }}
        }});
    }}
    
    function checkStatus() {{
        fetch('/status').then(r => r.json()).then(data => {{
            const dot = document.getElementById('statusDot');
            if (data.ai_configured) {{
                dot.style.background = '#22c55e';
                document.getElementById('statusText').textContent = 'Online';
            }} else {{
                dot.style.background = '#f59e0b';
                document.getElementById('statusText').textContent = 'Add API Key';
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
            
            if not GEMINI_API_KEY:
                response = "Add your Gemini API key to rvgpt2.py line 34"
            else:
                response = ask_gemini(message, image_b64)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "response": response}).encode())


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
    parts = [{"text": f"You are RVGPT, a helpful AI assistant. Keep responses conversational and helpful.\n\nUser: {prompt}"}]
    
    if image_b64:
        parts.append({"inlineData": {"mimeType": "image/png", "data": image_b64}})
    
    data = {
        "contents": [{"parts": parts}],
        "generationConfig": {"maxOutputTokens": 300, "temperature": 0.7}
    }
    
    res = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=data, timeout=60)
    result = res.json()
    
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    elif "error" in result:
        return f"API Error: {result['error']['message']}"
    return "No response"


def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:8080")


if __name__ == "__main__":
    print("=" * 50)
    print("  ✨ RVGPT 2.0 - Premium AI Assistant")
    print("=" * 50)
    print()
    
    if not GEMINI_API_KEY:
        print("⚠️  Add your Gemini API key:")
        print("   Edit rvgpt2.py line 34")
        print("   Get free key: https://aistudio.google.com/apikey")
        print()
    
    print("🌐 Opening http://localhost:8080")
    print()
    
    threading.Thread(target=open_browser, daemon=True).start()
    HTTPServer(("localhost", 8080), Handler).serve_forever()