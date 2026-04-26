#!/usr/bin/env python3
"""
RVGPT - Your AI Assistant
A standalone AI chatbot that can be copied anywhere and run.
Supports text, voice, images, and integrates with product tracking.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import base64
import tempfile
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import threading
import time

try:
    import speech_recognition as sr
except ImportError:
    os.system("pip3 install SpeechRecognition")
    import speech_recognition as sr

try:
    import requests
except ImportError:
    os.system("pip3 install requests")
    import requests

# ========================
# CONFIG - EDIT THIS LINE
# ========================
GEMINI_API_KEY = "AIzaSyCeoSNnyWAxA2p2zH58xUxGAnW1lQBZPco"  # AIzaSyCeoSNnyWAxA2p2zH58xUxGAnW1lQBZPco
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# ========================
# STYLE
# ========================
DARK_STYLE = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}
.chat-container {
    width: 100%;
    max-width: 600px;
    background: #0f0f23;
    border-radius: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    overflow: hidden;
}
.chat-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    text-align: center;
    color: white;
}
.chat-header h1 { font-size: 1.5rem; margin-bottom: 4px; }
.corner-badge {
    position: absolute;
    top: 12px;
    right: 16px;
    background: rgba(255,255,255,0.2);
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}
.chat-header p { font-size: 0.85rem; opacity: 0.9; }
.status-bar {
    background: #1a1a2e;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    color: #888;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #e74c3c;
    display: inline-block;
    margin-right: 6px;
}
.status-dot.online { background: #27ae60; }
.messages {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.message {
    display: flex;
    gap: 12px;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.message.user { flex-direction: row-reverse; }
.message-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.message.user .message-avatar { background: #667eea; }
.message.bot .message-avatar { background: #764ba2; }
.message-content {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.5;
}
.message.user .message-content {
    background: #667eea;
    color: white;
    border-bottom-right-radius: 4px;
}
.message.bot .message-content {
    background: #1a1a2e;
    color: #eee;
    border-bottom-left-radius: 4px;
}
.message-content img {
    max-width: 100%;
    border-radius: 12px;
    margin-top: 8px;
}
.input-area {
    padding: 20px;
    background: #0f0f23;
    border-top: 1px solid #2a2a4a;
}
.input-row {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
}
.input-row input {
    flex: 1;
    padding: 14px 18px;
    border: none;
    border-radius: 25px;
    background: #1a1a2e;
    color: white;
    font-size: 1rem;
    outline: none;
}
.input-row input:focus {
    box-shadow: 0 0 0 2px #667eea;
}
.send-btn {
    width: 50px;
    height: 50px;
    border: none;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    transition: transform 0.2s;
}
.send-btn:hover { transform: scale(1.1); }
.voice-btn {
    width: 50px;
    height: 50px;
    border: 2px solid #667eea;
    border-radius: 50%;
    background: transparent;
    color: #667eea;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.2s;
}
.voice-btn:hover, .voice-btn.listening {
    background: #667eea;
    color: white;
}
.voice-btn.listening { animation: pulse 1s infinite; }
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.5); }
    50% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
}
.image-btn {
    width: 50px;
    height: 50px;
    border: 2px solid #764ba2;
    border-radius: 50%;
    background: transparent;
    color: #764ba2;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.2s;
}
.image-btn:hover {
    background: #764ba2;
    color: white;
}
.image-preview {
    display: none;
    position: relative;
    margin-bottom: 12px;
}
.image-preview.show { display: block; }
.image-preview img {
    width: 100%;
    max-height: 200px;
    object-fit: contain;
    border-radius: 12px;
    background: #1a1a2e;
}
.image-preview .remove-img {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 50%;
    background: #e74c3c;
    color: white;
    cursor: pointer;
}
.hidden-input { display: none; }
.tracker-section {
    padding: 16px 20px;
    background: #1a1a2e;
    border-top: 1px solid #2a2a4a;
}
.tracker-section h3 {
    color: #667eea;
    font-size: 0.9rem;
    margin-bottom: 10px;
}
.tracker-list {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 8px;
}
.tracker-item {
    flex-shrink: 0;
    background: #0f0f23;
    padding: 8px 14px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    color: #ccc;
}
.tracker-item span:first-child { font-size: 1.2rem; }
.typing-indicator {
    display: none;
    align-items: center;
    gap: 6px;
    color: #888;
    font-size: 0.85rem;
}
.typing-dots { display: flex; gap: 3px; }
.typing-dots span {
    width: 6px;
    height: 6px;
    background: #888;
    border-radius: 50%;
    animation: typing 1.4s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-4px); }
}
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
    <title>RVGPT - AI Assistant</title>
    {DARK_STYLE}
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <span class="corner-badge">🤖 RVGPT</span>
            <h1>Your AI Assistant</h1>
            <p>Text • Voice • Image • Products</p>
        </div>
        
        <div class="status-bar">
            <span><span class="status-dot" id="statusDot"></span><span id="statusText">Initializing...</span></span>
            <span id="productCount">0 products tracked</span>
        </div>
        
        <div class="messages" id="messages">
            <div class="message bot">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    Hey there! 👋 I'm <strong>RVGPT</strong>, your AI assistant<br><br>
                    I can help with:<br>
                    • 💬 Chat about anything<br>
                    • 🖼️ Analyze images<br>
                    • 📊 Track your products<br>
                    • 🎤 Listen to your voice<br><br>
                    <em>What can I help you with today?</em>
                </div>
            </div>
        </div>
        
        <div class="input-area">
            <div class="image-preview" id="imagePreview">
                <img id="previewImg" src="">
                <button class="remove-img" onclick="removeImage()">✕</button>
            </div>
            
            <div class="input-row">
                <input type="text" id="userInput" placeholder="What can I help you with?" onkeypress="if(event.key==='Enter')sendMessage()">
                <button class="image-btn" onclick="document.getElementById('imageInput').click()">🖼️</button>
                <button class="voice-btn" id="voiceBtn" onclick="toggleVoice()">🎤</button>
                <button class="send-btn" onclick="sendMessage()">➤</button>
            </div>
            <input type="file" class="hidden-input" id="imageInput" accept="image/*" onchange="handleImage(this)">
        </div>
        
        <div class="tracker-section">
            <h3>📊 Top Products (from orders)</h3>
            <div class="tracker-list" id="trackerList">
                <div class="tracker-item" style="color:#888;">No orders yet...</div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            <span>RVGPT is typing</span>
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    </div>
    
    <script>
    let messages = [];
    let attachedImage = null;
    let isListening = false;
    let recognition = null;
    
    // Check for Web Speech API
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        
        recognition.onresult = (event) => {{
            const transcript = Array.from(event.results).map(r => r[0].transcript).join('');
            document.getElementById('userInput').value = transcript;
            if (event.results[0].isFinal) {{
                sendMessage();
            }}
        }};
        
        recognition.onend = () => {{
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
        }};
        
        recognition.onerror = (e) => {{
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
        }};
    }}
    
    function toggleVoice() {{
        if (!recognition) {{
            addBotMessage("🎤 Voice not supported in this browser. Try Chrome!");
            return;
        }}
        
        if (isListening) {{
            recognition.stop();
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
        }} else {{
            recognition.start();
            isListening = true;
            document.getElementById('voiceBtn').classList.add('listening');
        }}
    }}
    
    function handleImage(input) {{
        if (input.files && input.files[0]) {{
            const reader = new FileReader();
            reader.onload = (e) => {{
                attachedImage = e.target.result;
                document.getElementById('previewImg').src = attachedImage;
                document.getElementById('imagePreview').classList.add('show');
            }};
            reader.readAsDataURL(input.files[0]);
        }}
    }}
    
    function removeImage() {{
        attachedImage = null;
        document.getElementById('imageInput').value = '';
        document.getElementById('imagePreview').classList.remove('show');
    }}
    
    async function sendMessage() {{
        const input = document.getElementById('userInput');
        const text = input.value.trim();
        if (!text && !attachedImage) return;
        
        // Add user message
        addUserMessage(text, attachedImage);
        input.value = '';
        
        // Show typing indicator
        document.getElementById('typingIndicator').style.display = 'flex';
        
        // Send to server
        try {{
            const formData = new FormData();
            formData.append('message', text);
            if (attachedImage) {{
                formData.append('image', attachedImage.split(',')[1]);
            }}
            
            const response = await fetch('/chat', {{
                method: 'POST',
                body: formData
            }});
            
            const data = await response.json();
            document.getElementById('typingIndicator').style.display = 'none';
            
            if (data.success) {{
                addBotMessage(data.response);
                speak(data.response);
            }} else {{
                addBotMessage("Sorry, I encountered an error. Make sure the API key is set in rvgpt.py");
            }}
        }} catch (e) {{
            document.getElementById('typingIndicator').style.display = 'none';
            addBotMessage("Can't connect to RVGPT server. Make sure it's running!");
        }}
    }}
    
    function addUserMessage(text, image) {{
        const container = document.getElementById('messages');
        let html = `
            <div class="message user">
                <div class="message-avatar">👤</div>
                <div class="message-content">${{text}}${{image ? '<img src="' + image + '">' : ''}}</div>
            </div>
        `;
        container.innerHTML += html;
        container.scrollTop = container.scrollHeight;
    }}
    
    function addBotMessage(text) {{
        const container = document.getElementById('messages');
        const html = `
            <div class="message bot">
                <div class="message-avatar">🤖</div>
                <div class="message-content">${{text.replace(/\\n/g, '<br>')}}</div>
            </div>
        `;
        container.innerHTML += html;
        container.scrollTop = container.scrollHeight;
    }}
    
    function speak(text) {{
        if (!('speechSynthesis' in window)) return;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;
        speechSynthesis.speak(utterance);
    }}
    
    function loadTracker() {{
        fetch('/tracker').then(r => r.json()).then(data => {{
            document.getElementById('productCount').textContent = data.total + ' products tracked';
            const list = document.getElementById('trackerList');
            if (data.top.length > 0) {{
                list.innerHTML = data.top.slice(0, 5).map(p => `
                    <div class="tracker-item">
                        <span>${{p.emoji || '📦'}}</span>
                        <span>${{p.name}}</span>
                        <span style="color:#27ae60;">${{p.qty}} sold</span>
                    </div>
                `).join('');
            }}
        }});
    }}
    
    // Check status
    function checkStatus() {{
        fetch('/status').then(r => r.json()).then(data => {{
            const dot = document.getElementById('statusDot');
            const text = document.getElementById('statusText');
            if (data.ai_configured) {{
                dot.classList.add('online');
                text.textContent = 'AI Online';
            }} else {{
                dot.style.background = '#f39c12';
                text.textContent = 'Add API Key';
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
    def log_message(self, format, *args):
        pass  # Silent logging
    
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
            self.wfile.write(json.dumps({"top": get_product_stats(), "total": sum(p["qty"] for p in get_product_stats())}).encode())
        
        elif self.path == "/sync":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            update_product_stats(data.get("items", []))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def do_POST(self):
        if self.path == "/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                from urllib.parse import parse_qs as pq
                params = pq(post_data.decode())
                message = params.get("message", [""])[0]
                image_b64 = params.get("image", [None])[0]
                
                if not GEMINI_API_KEY:
                    response = "Please add your Gemini API key to rvgpt.py line 12"
                else:
                    response = ask_gemini(message, image_b64)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "response": response}).encode())
            
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())


def get_product_stats():
    """Get product stats from localStorage file"""
    stats = {}
    storage_file = Path.home() / ".rvgpt_storage.json"
    
    if storage_file.exists():
        try:
            data = json.loads(storage_file.read_text())
            stats = data.get("product_stats", {})
        except:
            pass
    
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    return [{"name": k, "qty": v, "emoji": "📦"} for k, v in sorted_stats[:10]]


def update_product_stats(order_items):
    """Update product stats when order is placed"""
    storage_file = Path.home() / ".rvgpt_storage.json"
    data = {}
    
    if storage_file.exists():
        try:
            data = json.loads(storage_file.read_text())
        except:
            pass
    
    stats = data.get("product_stats", {})
    for item in order_items:
        name = item.get("name", "Unknown")
        qty = item.get("qty", 1)
        stats[name] = stats.get(name, 0) + qty
    
    data["product_stats"] = stats
    storage_file.write_text(json.dumps(data, indent=2))


def ask_gemini(prompt, image_b64=None):
    global GEMINI_API_KEY
    
    parts = [{"text": prompt}]
    
    if image_b64:
        parts.append({
            "inlineData": {
                "mimeType": "image/png",
                "data": image_b64
            }
        })
    
    data = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "maxOutputTokens": 500,
            "temperature": 0.7
        }
    }
    
    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        json=data,
        timeout=60
    )
    
    result = response.json()
    
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    elif "error" in result:
        return f"API Error: {result['error']['message']}"
    else:
        return "No response from AI"


def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:8080")


if __name__ == "__main__":
    print("=" * 60)
    print("  🤖 RVGPT - Your AI Assistant")
    print("=" * 60)
    print()
    
    if not GEMINI_API_KEY:
        print("⚠️  WARNING: Gemini API key not set!")
        print()
        print("   1. Get free key at: https://aistudio.google.com/apikey")
        print("   2. Edit rvgpt.py line 12:")
        print('      GEMINI_API_KEY = "YOUR_KEY_HERE"')
        print()
        print("   The chatbot will still work but AI responses will show this message.")
        print()
    else:
        print("✅ Gemini API configured")
    
    print("🌐 Opening browser at http://localhost:8080")
    print()
    print("   Press Ctrl+C to stop")
    print()
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    server = HTTPServer(("localhost", 8080), Handler)
    server.serve_forever()