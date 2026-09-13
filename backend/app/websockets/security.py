"""Authenticate raw WebSocket frames, including binary audio and token refresh."""
import json
import time
from fastapi import HTTPException
from starlette.websockets import WebSocketDisconnect

from app.dependencies import student_from_token


def protect_tutor_socket(websocket, student_id: str, token: str):
    original_receive = websocket.receive
    session_token = token
    last_audio_check = float('-inf')
    window_start = time.monotonic()
    frame_count = 0
    byte_count = 0

    async def reject(code=4001):
        await websocket.close(code=code, reason='Account or request unavailable')
        raise WebSocketDisconnect(code=code)

    async def check(candidate):
        try:
            account = await student_from_token(candidate)
        except HTTPException:
            await reject()
        if str(account['id']) != str(student_id):
            await reject()

    async def checked_receive():
        nonlocal session_token, last_audio_check, window_start, frame_count, byte_count
        while True:
            frame = await original_receive()
            if frame['type'] != 'websocket.receive':
                return frame
            now = time.monotonic()
            if now - window_start >= 60:
                window_start, frame_count, byte_count = now, 0, 0
            text = frame.get('text')
            size = len(text.encode('utf-8')) if text is not None else len(frame.get('bytes') or b'')
            frame_count += 1
            byte_count += size
            if size > 4 * 1024 * 1024 or byte_count > 32 * 1024 * 1024 or frame_count > 1000:
                await reject(1009)
            if text is not None:
                try:
                    message = json.loads(text)
                except (ValueError, TypeError):
                    message = None
                if isinstance(message, dict) and message.get('type') == 'auth_refresh':
                    candidate = message.get('token')
                    if not isinstance(candidate, str) or len(candidate) > 8192:
                        await reject()
                    await check(candidate)
                    session_token = candidate
                    last_audio_check = now
                    continue  # Authentication messages never reach the tutor/LLM.
                await check(session_token)
                last_audio_check = now
            elif now - last_audio_check >= 2:
                # Audio arrives in frequent chunks; bound the revocation delay
                # without issuing two network calls for every audio fragment.
                await check(session_token)
                last_audio_check = now
            return frame

    websocket.receive = checked_receive
