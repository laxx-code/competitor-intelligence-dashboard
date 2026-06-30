#!/bin/bash

echo "🚀 Starting Competitor Intelligence Dashboard"
echo "============================================="

# Kill existing processes
pkill -f uvicorn 2>/dev/null
pkill -f react-scripts 2>/dev/null
sudo lsof -ti:8000 | xargs kill -9 2>/dev/null
sudo lsof -ti:3001 | xargs kill -9 2>/dev/null
sleep 2

# Start backend
echo "📡 Starting backend on port 8000..."
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
    echo "⚠️ Backend may have issues. Check the terminal."
fi

# Start frontend
echo "🎨 Starting frontend on port 3001..."
cd frontend
PORT=3001 npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ System Ready!"
echo "📊 Frontend: http://localhost:3001"
echo "🔗 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

wait $BACKEND_PID $FRONTEND_PID
