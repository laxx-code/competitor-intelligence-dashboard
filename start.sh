#!/bin/bash

echo "🚀 Starting Competitor Intelligence Dashboard"
echo "============================================="

cd ~/competitor-intelligence-dashboard

# Kill existing processes
echo "Cleaning up..."
pkill -f uvicorn 2>/dev/null
pkill -f react-scripts 2>/dev/null
sudo lsof -ti:8000 | xargs kill -9 2>/dev/null
sudo lsof -ti:3000 | xargs kill -9 2>/dev/null
sleep 2

# Start backend
echo "Starting backend..."
cd backend
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &
BACKEND=$!
cd ..

# Wait for backend
echo "Waiting for backend..."
sleep 3

# Check backend
if curl -s http://localhost:8000/health >/dev/null; then
    echo "✅ Backend running on port 8000"
else
    echo "⚠️ Backend may have issues"
fi

# Start frontend
echo "Starting frontend..."
cd frontend
npm start &
FRONTEND=$!
cd ..

echo ""
echo "✅ System Ready!"
echo "📊 Frontend: http://localhost:3000"
echo "🔗 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

wait $BACKEND $FRONTEND
