"""
WebSocket Connection Manager
Manages active WebSocket connections for real-time voice streaming.
"""
from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_info: Dict[str, dict] = {}

    def _extract_ip(self, websocket: WebSocket) -> str:
        """Extract client IP from X-Forwarded-For (nginx) or direct connection."""
        headers = dict(websocket.headers) if hasattr(websocket, 'headers') else {}
        forwarded = headers.get('x-forwarded-for', '')
        if forwarded:
            return forwarded.split(',')[0].strip()
        real_ip = headers.get('x-real-ip', '')
        if real_ip:
            return real_ip.strip()
        if websocket.client:
            return websocket.client.host
        return 'unknown'

    async def connect(self, student_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[student_id] = websocket
        from datetime import datetime
        self.connection_info[student_id] = {
            'ip': self._extract_ip(websocket),
            'connected_at': datetime.utcnow().isoformat(),
        }

    def disconnect(self, student_id: str):
        self.active_connections.pop(student_id, None)
        self.connection_info.pop(student_id, None)

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
