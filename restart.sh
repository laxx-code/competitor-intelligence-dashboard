#!/bin/bash

echo "🔄 Restarting Competitor Intelligence Dashboard"
echo "=============================================="

# Kill everything
echo "Cleaning up ports..."
sudo lsof -ti:8000 | xargs kill -9 2>/dev/null
sudo lsof -ti:3001 | xargs kill -9 2>/dev/null
pkill -f uvicorn 2>/dev/null
pkill -f react-scripts 2>/dev/null
sleep 2

# Start backend
echo "Starting backend on port 8000..."
cd backend
source ../venv/bin/activate
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend
sleep 5

# Check backend
if curl -s http://localhost:8000/health >/dev/null; then
    echo "✅ Backend running on port 8000"
else
    echo "⚠️ Backend may have issues"
fi

# Start frontend
echo "Starting frontend on port 3001..."
cd frontend
PORT=3001 npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ System Ready!"
echo "📊 Frontend: http://localhost:3001"
echo "🔗 Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

wait $BACKEND_PID $FRONTEND_PID
