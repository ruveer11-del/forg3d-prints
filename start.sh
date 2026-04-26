#!/bin/bash
# Start both RVGPT servers
cd "$(dirname "$0")"

echo "🚀 Starting RVGPT servers..."
echo ""

# Start server.py (port 8000 - website chat)
python3 server.py &
SERVER_PID=$!

# Small delay
sleep 1

# Start rvgpt3.py (port 8080 - standalone app)
python3 rvgpt3.py &
RVGPT_PID=$!

echo ""
echo "✅ Both servers running!"
echo "   Website chat: http://localhost:8000"
echo "   RVGPT App:    http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for any process to exit
wait