import json
import time
from valkey.asyncio import Valkey
from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.dependencies.ws import manager
from app.logger import global_logger



async def trigger_start_time(
    cache: Valkey,
    match_code: str,
    round_name: str,
    question_code: str,
    event_type: str = "new_question",
):
    """
    Ghi lại mốc thời gian bắt đầu câu hỏi hoặc bật chuông,
    đồng thời broadcast event cho toàn hệ thống.
    """
    start_time = time.time()
    key = f"match:{match_code}:start_time"

    try:
        await cache.set(key, start_time)
        global_logger.info(f"[START] Set start_time={start_time} for match={match_code}")
        event = {
            "type": event_type,
            "match_code": match_code,
            "round": round_name,
            "question_code": question_code,
            "start_time": start_time,
        }
        await cache.publish(f"match:{match_code}:updates", json.dumps(event))
        global_logger.info(f"[WS] Published {event_type} event for match={match_code}")

        return {"message": f"{event_type} triggered", "start_time": start_time}
    except Exception as e:
        global_logger.error(f"[START] Failed to trigger start_time for match={match_code}: {e}")
        raise



async def handle_match_websocket(websocket: WebSocket, match_code: str, valkey: Valkey):
    await manager.connect(match_code, websocket)
    subscriber = valkey.pubsub()
    await subscriber.subscribe(f"match:{match_code}:updates")
    global_logger.info(f"[WS] Subscribed to Redis channel match:{match_code}:updates")

    try:
        while True:
            message = await subscriber.get_message(ignore_subscribe_messages=True, timeout=0.1)
            if message and message.get("type") == "message":
                try:
                    data = json.loads(message["data"])
                    await manager.broadcast(match_code, data)
                except Exception as e:
                    global_logger.error(f"[WS] Invalid message from Redis: {e}")

            try:
                client_msg = await websocket.receive_json()
                global_logger.debug(f"[WS] Received from client: {client_msg}")
                event_type = client_msg.get("type")
                if event_type == "buzz":
                    event = {
                        "type": "player_buzzed",
                        "player_code": client_msg["player_code"],
                    }
                    await valkey.publish(f"match:{match_code}:updates", json.dumps(event))
                elif event_type == "answer":
                    event = {
                        "type": "player_answered",
                        "player_code": client_msg["player_code"],
                        "answer": client_msg["answer"],
                    }
                    await valkey.publish(f"match:{match_code}:updates", json.dumps(event))
            except Exception:
                pass

    except WebSocketDisconnect:
        manager.disconnect(match_code, websocket)
        await subscriber.unsubscribe(f"match:{match_code}:updates")
        global_logger.info(f"[WS] Disconnected from match={match_code}")