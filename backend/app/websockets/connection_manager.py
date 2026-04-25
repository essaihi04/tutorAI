"""
WebSocket Connection Manager
Manages active WebSocket connections for real-time voice streaming.
"""
from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, student_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[student_id] = websocket

    def disconnect(self, student_id: str):
        self.active_connections.pop(student_id, None)

    async def send_json(self, student_id: str, data: dict):
        ws = self.active_connections.get(student_id)
        if ws:
            await ws.send_json(data)

    async def send_bytes(self, student_id: str, data: bytes):
        ws = self.active_connections.get(student_id)
        if ws:
            await ws.send_bytes(data)

    def is_connected(self, student_id: str) -> bool:
        return student_id in self.active_connections


manager = ConnectionManager()
