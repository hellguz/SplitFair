# ./backend/app/api/v1/websockets.py
"""
WebSocket connection management for real-time updates.
"""
import json
from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

class ConnectionManager:
    """Manages active WebSocket connections."""
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, group_id: str, websocket: WebSocket):
        """Accepts a new WebSocket connection and adds it to the group's list."""
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = []
        self.active_connections[group_id].append(websocket)
        print(f"Client connected to group {group_id}. Total clients: {len(self.active_connections[group_id])}")

    def disconnect(self, group_id: str, websocket: WebSocket):
        """Removes a WebSocket connection from the group's list."""
        if group_id in self.active_connections:
            self.active_connections[group_id].remove(websocket)
            print(f"Client disconnected from group {group_id}. Total clients: {len(self.active_connections[group_id])}")

    async def broadcast(self, group_id: str, message: dict):
        """Sends a JSON message to all connected clients in a specific group."""
        if group_id in self.active_connections:
            message_json = json.dumps(message)
            for connection in self.active_connections[group_id]:
                await connection.send_text(message_json)

manager = ConnectionManager()

@router.websocket("/ws/{group_id}")
async def websocket_endpoint(websocket: WebSocket, group_id: str):
    """
    The WebSocket endpoint that clients connect to for real-time updates for a specific group.
    """
    await manager.connect(group_id, websocket)
    try:
        while True:
            # Keep the connection alive, listening for messages (though we don't act on them here)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(group_id, websocket)

