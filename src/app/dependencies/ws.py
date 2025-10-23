import asyncio
from typing import Any
from fastapi.websockets import WebSocket

from app.logger import global_logger



class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, match_code: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(match_code, []).append(websocket)
        global_logger.info(f"Connected websocket for match_code={match_code}. Total connections: {len(self.active_connections[match_code])}")

    def disconnect(self, match_code: str, websocket: WebSocket):
        if match_code in self.active_connections:
            self.active_connections[match_code] = [
                conn for conn in self.active_connections[match_code] if conn is not websocket
            ]
            global_logger.info(f"Disconnected websocket for match_code={match_code}. Remaining connections: {len(self.active_connections[match_code])}")
            if not self.active_connections[match_code]:
                del self.active_connections[match_code]

    async def broadcast(self, match_code: str, message: dict[str, Any]):
        if match_code in self.active_connections:
            connections_to_send = list(self.active_connections[match_code])
            results = await asyncio.gather(
                *[connection.send_json(message) for connection in connections_to_send], 
                return_exceptions=True
            )
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    global_logger.error(f"Error sending message to websocket for match_code={match_code}: {result}")
                    self.disconnect(match_code, connections_to_send[i])


manager = ConnectionManager()