from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs, unquote

try:
    import requests
except ImportError:
    import os
    os.system("pip3 install requests")
    import requests

GEMINI_API_KEY = "AIzaSyCeoSNnyWAxA2p2zH58xUxGAnW1lQBZPco"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def ask_ai(prompt):
    if not GEMINI_API_KEY:
        return "AI not configured"
    
    try:
        url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": 150,
                "temperature": 0.7
            }
        }
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            return f"Error: {result['error']['message']}"
        else:
            return "No response"
    except Exception as e:
        return f"Error: {str(e)}"


class Handler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        try:
            if self.path.startswith("/ask"):
                parsed = urlparse(self.path)
                query = parse_qs(parsed.query).get("q", [""])[0]
                query = unquote(query)
                
                prompt = f"""You are a helpful assistant for a 3D printing store called Simple Prints. 
Keep responses short (2-3 sentences max). Be friendly and helpful.
Question: {query}"""
                
                result = ask_ai(prompt)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps({
                    "query": query,
                    "result": result
                }).encode())

            elif self.path == "/health":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                configured = bool(GEMINI_API_KEY)
                self.wfile.write(json.dumps({"status": "ok", "ai_configured": configured}).encode())

            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"AI Server Running. Use /ask?q=your question")

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())


if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("=" * 50)
        print("WARNING: Gemini API key not set!")
        print("Edit server.py and add your key on line 9:")
        print('GEMINI_API_KEY = "YOUR_KEY_HERE"')
        print("=" * 50)
        print()
        print("Get your free API key at:")
        print("https://aistudio.google.com/apikey")
        print()
    else:
        print("Gemini AI configured ✓")
    
    print("Server running at http://localhost:8000")
    print("Press Ctrl+C to stop")
    print()
    
    server = HTTPServer(("localhost", 8000), Handler)
    server.serve_forever()