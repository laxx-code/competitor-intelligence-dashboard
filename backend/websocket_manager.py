import json
from datetime import datetime
from typing import List, Dict, Any
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

class WebSocketManager:
    """Handles real-time WebSocket connections and updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_update = None
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New WebSocket connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)
    
    async def broadcast_competitor_update(self, competitor_data: Dict):
        """Broadcast competitor update to all clients"""
        message = {
            "type": "competitor_update",
            "data": competitor_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_alert(self, alert: Dict):
        """Broadcast alert to all clients"""
        message = {
            "type": "alert",
            "data": alert,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_sentiment_update(self, sentiment: Dict):
        """Broadcast sentiment update"""
        message = {
            "type": "sentiment_update",
            "data": sentiment,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)

# Global WebSocket manager instance
ws_manager = WebSocketManager()
