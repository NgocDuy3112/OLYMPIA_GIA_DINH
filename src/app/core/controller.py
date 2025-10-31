import json
import asyncio
from valkey.asyncio import Valkey
from fastapi import HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.dependencies.ws import *
from app.schema.controller import *
from app.utils.match_event import *
from app.logger import global_logger



async def listen_to_valkey_pubsub(manager: ConnectionManager, match_code: str, subscriber: Valkey):
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
            client_msg = await websocket.receive_json() 
            global_logger.debug(f"[WS] From client: {client_msg}")
            event_type = client_msg.get("type")
            if event_type in ["buzz", "answer"]:
                locked = await valkey.get(f"match:{match_code}:locked")
                if locked == b"1" or locked == "1":
                    await websocket.send_json({"type": "answer_rejected", "reason": "time_up"})
                    continue
            await process_client_event(valkey, match_code, client_msg)
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
            listen_to_valkey_pubsub(manager, match_code, subscriber),
            listen_to_websocket_client(websocket, match_code, valkey)
        )
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(match_code, websocket)
        await subscriber.unsubscribe(f"match:{match_code}:updates")
        global_logger.info(f"[WS] Disconnected from match={match_code}")



async def trigger_start_timer(request: StartQuestionRequest, pubsub: Valkey) -> StartQuestionResponse:
    try:
        result = await trigger_start_time(
            pubsub=pubsub,
            match_code=request.match_code,
            question_code=request.question_code,
            time_limit=request.time_limit
        )
        return StartQuestionResponse(response={'message': result['message']})
    except Exception as e:
        global_logger.error(f"[API_START] There's an error when triggering the question {request.question_code} for match {request.match_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



async def trigger_pick_question(request: PickQuestionRequest, pubsub: Valkey) -> PickQuestionResponse:
    try:
        result = await pick_question(
            pubsub=pubsub,
            match_code=request.match_code,
            player_code=request.player_code,
            question_code=request.question_code
        )
        return PickQuestionResponse(response={'message': result['message']})
    except Exception as e:
        global_logger.error(f"[API_START] There's an error when picking the question {request.question_code} by player {request.player_code} for match {request.match_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")