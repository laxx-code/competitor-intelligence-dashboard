#!/bin/bash

echo "🔄 Restarting Competitor Intelligence Dashboard"

# Kill everything
echo "Cleaning ports..."
sudo lsof -ti:8000 | xargs kill -9 2>/dev/null
sudo lsof -ti:3001 | xargs kill -9 2>/dev/null
pkill -f uvicorn 2>/dev/null
pkill -f react-scripts 2>/dev/null
sleep 2

# Start backend
echo "Starting backend on port 8000..."
cd ~/competitor-intelligence-dashboard/backend
source venv/bin/activate
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
cd ..

# Wait for backend
sleep 5

# Start frontend
echo "Starting frontend on port 3001..."
cd ~/competitor-intelligence-dashboard/frontend
PORT=3001 npm start &
cd ..

echo ""
echo "✅ System Ready!"
echo "📊 Frontend: http://localhost:3001"
echo "🔗 Backend: http://localhost:8000"
