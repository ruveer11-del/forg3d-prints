const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const GEMINI_API_KEY = process.env.GEMINI_API_KEY || 'AIzaSyCeoSNnyWAxA2p2zH58xUxGAnW1lQBZPco';
const GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent';

async function askGemini(prompt) {
  try {
    const res = await fetch(GEMINI_URL + '?key=' + GEMINI_API_KEY, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: 'You are RVGPT, a helpful AI assistant. Keep responses short and friendly.\n\n' + prompt }] }],
        generationConfig: { maxOutputTokens: 300, temperature: 0.7 }
      })
    });
    const d = await res.json();
    if (d.candidates && d.candidates[0]) {
      return d.candidates[0].content.parts[0].text;
    }
    return d.error?.message || 'No response';
  } catch (e) {
    return 'Error: ' + e.message;
  }
}

app.get('/', (req, res) => {
  res.send(`<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>RVGPT</title><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, sans-serif; background: #0f0f1a; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; color: #fff; }
  .app { width: 100%; max-width: 450px; background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); border-radius: 24px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
  .header { padding: 20px; background: linear-gradient(135deg, #1e3c72, #2a5298); display: flex; align-items: center; gap: 12px; }
  .header h1 { font-size: 1.4rem; }
  .chat { height: 400px; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
  .msg { display: flex; gap: 10px; }
  .msg.user { flex-direction: row-reverse; }
  .avatar { width: 32px; height: 32px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; }
  .msg.bot .avatar { background: linear-gradient(135deg, #1e3c72, #2a5298); }
  .msg.user .avatar { background: #333; }
  .content { max-width: 75%; padding: 12px 14px; border-radius: 14px; font-size: 0.9rem; line-height: 1.5; }
  .msg.bot .content { background: #252538; border-bottom-left-radius: 4px; }
  .msg.user .content { background: linear-gradient(135deg, #1e3c72, #2a5298); border-bottom-right-radius: 4px; }
  .input { padding: 16px; display: flex; gap: 10px; border-top: 1px solid rgba(255,255,255,0.1); }
  .input input { flex: 1; padding: 12px 14px; background: #1e1e32; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; color: #fff; outline: none; }
  .input button { padding: 12px 20px; border: none; border-radius: 10px; background: linear-gradient(135deg, #1e3c72, #2a5298); color: #fff; cursor: pointer; }
  </style></head><body>
  <div class="app">
    <div class="header"><h1>RVGPT</h1></div>
    <div class="chat" id="chat">
      <div class="msg bot"><div class="avatar">AI</div><div class="content">Hi! I'm RVGPT. Ask me anything!</div></div>
    </div>
    <div class="input">
      <input id="input" placeholder="Type a message..." onkeypress="if(event.key==='Enter')send()">
      <button onclick="send()">Send</button>
    </div>
  </div>
  <script>
  async function send() {
    const text = document.getElementById('input').value.trim();
    if (!text) return;
    const chat = document.getElementById('chat');
    chat.innerHTML += '<div class="msg user"><div class="avatar">You</div><div class="content">' + text + '</div></div>';
    document.getElementById('input').value = '';
    chat.scrollTop = chat.scrollHeight;
    try {
      const res = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: text}) });
      const data = await res.json();
      chat.innerHTML += '<div class="msg bot"><div class="avatar">AI</div><div class="content">' + (data.response || 'Try again') + '</div></div>';
    } catch(e) { chat.innerHTML += '<div class="msg bot"><div class="avatar">AI</div><div class="content">Error</div></div>'; }
    chat.scrollTop = chat.scrollHeight;
  }
  </script></body></html>`);
});

app.get('/status', (req, res) => {
  res.json({ ai_configured: !!GEMINI_API_KEY });
});

app.post('/chat', async (req, res) => {
  const { message } = req.body;
  const response = await askGemini(message);
  res.json({ response });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('RVGPT running on port ' + PORT));