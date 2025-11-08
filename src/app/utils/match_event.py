import time
from valkey.asyncio import Valkey
import asyncio
import json

from app.logger import global_logger


MATCH_STATUS_BUZZING = "buzzing"
MATCH_STATUS_BUZZED = "buzzed"




async def publish_ws_event(pubsub: Valkey, match_code: str, event: dict):
    """
    Sent real-time event to WebSocket clients via Valkey PubSub.
    """
    channel = f"match:{match_code}:updates"
    try:
        await pubsub.publish(channel, json.dumps(event))
        global_logger.info(f"[WS] Published event to {channel}: {event}")
    except Exception as e:
        global_logger.warning(f"[WS] Failed to publish event to {channel}: {e}")



async def auto_time_up(pubsub: Valkey, match_code: str, question_code: str, end_time: float):
    """Automatically fire time_up event when time_limit ends."""
    delay = max(0, end_time - time.time())
    await asyncio.sleep(delay)
    await pubsub.set(f"match:{match_code}:locked", 1)
    event = {
        "type": "time_up",
        "match_code": match_code,
        "question_code": question_code,
    }
    await pubsub.publish(f"match:{match_code}:updates", json.dumps(event))
    global_logger.info(f"[TIME_UP] match={match_code} question={question_code}")



async def trigger_start_time(
    pubsub: Valkey,
    match_code: str,
    question_code: str,
    time_limit: int,
) -> dict:
    """
    Set start_time & end_time for a question and broadcast event.
    time_limit: int (seconds)
    """
    start_time = time.time()
    end_time = start_time + time_limit

    try:
        await pubsub.set(f"match:{match_code}:start_time", start_time)
        await pubsub.set(f"match:{match_code}:end_time", end_time)
        await pubsub.set(f"match:{match_code}:current_question_code", question_code)
        await pubsub.set(f"match:{match_code}:buzz_status", MATCH_STATUS_BUZZING)
        await pubsub.set(f"match:{match_code}:buzzer_winner", "None")
        await pubsub.set(f"match:{match_code}:locked", 0)
        global_logger.info(f"[START] {match_code} {question_code} start={start_time} end={end_time}")
        event = {
            "type": "start_the_timer",
            "match_code": match_code,
            "question_code": question_code,
            "start_time": start_time,
            "time_limit": time_limit,
        }
        await pubsub.publish(f"match:{match_code}:updates", json.dumps(event))
        global_logger.info(f"[WS] Broadcast 'start_the_timer' event for question {question_code} in {match_code}")
        asyncio.create_task(auto_time_up(pubsub, match_code, question_code, end_time))
        return {
            "message": "'start_the_timer' triggered", 
            "start_time": start_time, 
            "end_time": end_time
        }
    except Exception as e:
        global_logger.error(f"[FAILED] Event 'start_the_timer' failed for match={match_code}: {e}")
        raise



async def pick_question(pubsub: Valkey, match_code: str, player_code: str, question_code: str) -> dict:
    try:
        await pubsub.set(f"match:{match_code}:picked_question_code", question_code)
        await pubsub.set(f"match:{match_code}:picked_player_code", player_code)
        global_logger.info(f"[PICKED] {match_code} {question_code} being picked by {player_code}")
        event = {
            "type": "pick_question",
            "match_code": match_code,
            "player_code": player_code,
            "question_code": question_code
        }
        await pubsub.publish(f"match:{match_code}:updates", json.dumps(event))
        global_logger.info(f"[WS] Broadcast 'pick_question' event for question {question_code}, picked by player {player_code} in {match_code}")
        return {
            'message': "'pick_question' triggered",
            "match_code": match_code,
            "player_code": player_code,
            "question_code": question_code
        }
    except Exception as e:
        global_logger.error(f"[FAILED] Event 'pick_question' failed for match={match_code}: {e}")
        raise



async def process_client_event(
    valkey: Valkey,
    match_code: str,
    client_msg: dict
):
    """
    Process all events and publish to Valkey.
    Assuming the locked check is already done.
    """
    event_type = client_msg.get("type")
    player_code = client_msg.get("player_code")
    question_code = client_msg.get("question_code")
    if not player_code:
        global_logger.warning(f"[WS_PROCESS] Client message missing player_code: {client_msg}")
        return

    event = None
    current_status = await valkey.get(f"match:{match_code}:status").decode('utf-8')
    buzzer_winner = await valkey.get(f"match:{match_code}:buzzer_winner").decode('utf-8')

    if event_type == "buzz":
        if current_status != MATCH_STATUS_BUZZING:
            global_logger.debug(f"[BUZZ_REJECTED] {player_code} buzz rejected. Status is {current_status}")
            await publish_ws_event(valkey, match_code, {
                "type": "buzz_rejected", 
                "player_code": player_code, 
                "reason": f"Not in BUZZING state ({current_status})"
            })
            return

        if buzzer_winner != "None":
            global_logger.debug(f"[BUZZ_REJECTED] {player_code} buzz rejected. Winner already set: {buzzer_winner}")
            await publish_ws_event(valkey, match_code, {
                "type": "buzz_rejected", 
                "player_code": player_code, 
                "reason": f"Winner already set: {buzzer_winner}"
            })
            return

        buzz_time = time.time()
        await valkey.set(f"match:{match_code}:buzzer_winner", player_code)

        event = {
            "type": "buzzer_winner",
            "match_code": match_code,
            "question_code": question_code,
            "player_code": player_code,
            "buzzed_at": buzz_time,
        }
    elif event_type == "pick_question":
        event = {
            "type": "player_picked_question",
            "player_code": player_code,
            "question_code": question_code
        }
    elif event_type == "answer":
        answer = client_msg.get("answer")
        event = {
            "type": "player_answered",
            "player_code": player_code,
            "question_code": question_code,
            "answer": answer,
        }
    elif event_type == "buzz_cnv":
        event = {
            "type": "player_buzzed_cnv",
            "player_code": player_code,
        }
    if event:
        await valkey.publish(f"match:{match_code}:updates", json.dumps(event))
        global_logger.debug(f"[WS_PUBLISH] Published {event_type} for {player_code} in {match_code}")
    else:
        global_logger.debug(f"[WS_PROCESS] Unhandled event type: {event_type}")