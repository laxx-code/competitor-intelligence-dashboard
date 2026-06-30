#!/bin/bash

echo "🚀 Starting Competitor Intelligence Dashboard"
echo "============================================="

cd ~/competitor-intelligence-dashboard

# Kill everything
echo "Cleaning up ports..."
pkill -f uvicorn 2>/dev/null
pkill -f react-scripts 2>/dev/null
sudo lsof -ti:8000 | xargs kill -9 2>/dev/null
sudo lsof -ti:3000 | xargs kill -9 2>/dev/null
sudo lsof -ti:3001 | xargs kill -9 2>/dev/null
sleep 2

# Start backend
echo "Starting backend on port 8000..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend
echo "Waiting for backend..."
sleep 5

# Check backend
if curl -s http://localhost:8000/health >/dev/null; then
    echo "✅ Backend running on port 8000"
else
    echo "⚠️ Backend may have issues, check logs"
fi

# Check if port 3000 is free
if sudo lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null; then
    echo "⚠️ Port 3000 is busy, using port 3001"
    FRONTEND_PORT=3001
else
    FRONTEND_PORT=3000
fi

# Start frontend
echo "Starting frontend on port $FRONTEND_PORT..."
cd frontend
PORT=$FRONTEND_PORT npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ System Ready!"
echo "📊 Frontend: http://localhost:$FRONTEND_PORT"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

wait $BACKEND_PID $FRONTEND_PID
