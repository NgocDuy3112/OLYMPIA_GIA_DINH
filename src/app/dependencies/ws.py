import asyncio
from typing import Any
from fastapi.websockets import WebSocket

from app.logger import global_logger


class ConnectionManager:
    def __init__(self):
        # Lưu danh sách các WebSocket theo match_code
        self.active_connections: dict[str, list[WebSocket]] = {}

        # Lưu subscriber Valkey (mỗi match_code chỉ có 1)
        self.subscribers: dict[str, Any] = {}

        # Lưu task listen_to_valkey_pubsub để tránh tạo trùng
        self.subscriber_tasks: dict[str, asyncio.Task] = {}

    async def connect(self, match_code: str, websocket: WebSocket):
        """
        Kết nối 1 WebSocket client mới và đảm bảo không bị nhân đôi.
        """
        if websocket.application_state.name != "CONNECTED":
            await websocket.accept()

        if match_code not in self.active_connections:
            self.active_connections[match_code] = []

        # 🔹 Đảm bảo không thêm trùng kết nối
        if websocket not in self.active_connections[match_code]:
            self.active_connections[match_code].append(websocket)
            global_logger.info(
                f"[WS_CONNECT] match={match_code}, total={len(self.active_connections[match_code])}"
            )
        else:
            global_logger.debug(f"[WS_DUPLICATE] WebSocket for match={match_code} already registered.")

    def disconnect(self, match_code: str, websocket: WebSocket):
        """
        Ngắt kết nối WebSocket và xóa nếu match không còn client.
        """
        if match_code in self.active_connections:
            before = len(self.active_connections[match_code])
            self.active_connections[match_code] = [
                conn for conn in self.active_connections[match_code] if conn is not websocket
            ]
            after = len(self.active_connections[match_code])
            global_logger.info(
                f"[WS_DISCONNECT] match={match_code}, before={before}, after={after}"
            )

            if not self.active_connections[match_code]:
                self.active_connections.pop(match_code, None)
                # Tùy chọn: auto clean subscriber khi không còn ai nghe
                self.cleanup_subscriber(match_code)

    async def broadcast(self, match_code: str, message: dict[str, Any]):
        """
        Gửi 1 message JSON đến tất cả client đang kết nối cùng match_code.
        """
        if match_code not in self.active_connections:
            return

        connections = list(self.active_connections[match_code])
        results = await asyncio.gather(
            *[conn.send_json(message) for conn in connections],
            return_exceptions=True
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                global_logger.error(
                    f"[WS_BROADCAST_ERR] match={match_code}: {result}"
                )
                self.disconnect(match_code, connections[i])

        global_logger.debug(
            f"[WS_BROADCAST] match={match_code}, sent_to={len(connections)}"
        )

    # ------------------------------
    # 🔹 Subscriber helpers
    # ------------------------------

    def has_subscriber(self, match_code: str) -> bool:
        return match_code in self.subscribers

    def set_subscriber(self, match_code: str, subscriber: Any):
        self.subscribers[match_code] = subscriber
        global_logger.info(f"[WS_SUBSCRIBER] Added subscriber for match={match_code}")

    def get_subscriber(self, match_code: str):
        return self.subscribers.get(match_code)

    def set_subscriber_task(self, match_code: str, task: asyncio.Task):
        self.subscriber_tasks[match_code] = task

    def cleanup_subscriber(self, match_code: str):
        """
        Gỡ bỏ subscriber và task nếu match không còn client.
        """
        if match_code in self.subscribers:
            try:
                sub = self.subscribers.pop(match_code)
                global_logger.info(f"[WS_SUBSCRIBER] Removed subscriber for match={match_code}")
                asyncio.create_task(sub.unsubscribe(f"match:{match_code}:updates"))
            except Exception as e:
                global_logger.warning(f"[WS_SUBSCRIBER_CLEANUP] Failed: {e}")

        if match_code in self.subscriber_tasks:
            task = self.subscriber_tasks.pop(match_code)
            if not task.done():
                task.cancel()
                global_logger.info(f"[WS_TASK] Canceled subscriber task for match={match_code}")


# Singleton instance
manager = ConnectionManager()