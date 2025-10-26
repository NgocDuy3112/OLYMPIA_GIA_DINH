import json
import time
import asyncio
from valkey.asyncio import Valkey
from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.dependencies.ws import manager
from app.logger import global_logger



async def listen_to_valkey_pubsub(subscriber, match_code, manager):
    try:
        while True:
            message = await subscriber.get_message(ignore_subscribe_messages=True) 
            if message and message.get("type") == "message":
                try:
                    data = json.loads(message["data"])
                    await manager.broadcast(match_code, data)
                except Exception as e:
                    global_logger.error(f"[WS] Invalid Valkey message in listener: {e}")
    except Exception as e:
        global_logger.error(f"[WS] PubSub listener failed: {e}")



async def listen_to_websocket_client(websocket: WebSocket, match_code: str, valkey: Valkey):
    try:
        while True:
            # Lắng nghe tin nhắn từ client. Nếu không có tin nhắn, tác vụ này sẽ ngủ.
            client_msg = await websocket.receive_json() 
            event_type = client_msg.get("type")
            player_code = client_msg.get("player_code")
            global_logger.debug(f"[WS] From client: {client_msg}")
            
            # Check if locked (no more buzz/answer allowed)
            locked = await valkey.get(f"match:{match_code}:locked")
            if locked == b"1" or locked == "1":
                await websocket.send_json({"type": "answer_rejected", "reason": "time_up"})
                continue
    except WebSocketDisconnect:
        raise 
    except Exception as e:
        global_logger.error(f"[WS] Client listener failed: {e}")



async def handle_match_websocket(websocket: WebSocket, match_code: str, valkey: Valkey):
    await manager.connect(match_code, websocket)
    subscriber = valkey.pubsub()
    await subscriber.subscribe(f"match:{match_code}:updates")
    global_logger.info(f"[WS] Client connected to match={match_code}")

    try:
        await asyncio.gather(
            listen_to_valkey_pubsub(subscriber, match_code, manager),
            listen_to_websocket_client(websocket, match_code, valkey)
        )
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(match_code, websocket)
        await subscriber.unsubscribe(f"match:{match_code}:updates")
        global_logger.info(f"[WS] Disconnected from match={match_code}")
