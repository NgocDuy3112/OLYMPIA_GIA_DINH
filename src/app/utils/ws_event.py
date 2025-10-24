import json
from app.logger import global_logger
from valkey.asyncio import Valkey



async def publish_ws_event(cache: Valkey, match_code: str, event: dict):
    """
    Gửi event realtime tới tất cả WebSocket client của match_code qua Redis pub/sub.
    """
    channel = f"match:{match_code}:updates"
    try:
        await cache.publish(channel, json.dumps(event))
        global_logger.info(f"[WS] Published event to {channel}: {event}")
    except Exception as e:
        global_logger.warning(f"[WS] Failed to publish event to {channel}: {e}")