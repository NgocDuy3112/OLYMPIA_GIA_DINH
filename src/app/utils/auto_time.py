import time
from valkey.asyncio import Valkey
import asyncio
import json

from app.logger import global_logger



async def auto_time_up(pubsub: Valkey, match_code: str, question_code: str, end_time: float):
    """Automatically fire time_up event when time_limit ends."""
    delay = max(0, end_time - time.time())
    await asyncio.sleep(delay)

    # Lock answering
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
    event_type: str = "new_question",
):
    """
    Set start_time & end_time for a question and broadcast event.
    time_limit: int (seconds)
    """
    start_time = time.time()
    end_time = start_time + time_limit

    try:
        # RESET previous state and store new
        await pubsub.set(f"match:{match_code}:start_time", start_time)
        await pubsub.set(f"match:{match_code}:end_time", end_time)
        await pubsub.set(f"match:{match_code}:current_question_code", question_code)
        await pubsub.set(f"match:{match_code}:locked", 0)

        global_logger.info(f"[START] {match_code} {question_code} start={start_time} end={end_time}")

        event = {
            "type": event_type,
            "match_code": match_code,
            "question_code": question_code,
            "start_time": start_time,
            "time_limit": time_limit,
        }
        await pubsub.publish(f"match:{match_code}:updates", json.dumps(event))
        global_logger.info(f"[WS] Broadcast {event_type} for {match_code}")
        asyncio.create_task(auto_time_up(pubsub, match_code, question_code, end_time))

        return {"message": f"{event_type} triggered", "start_time": start_time, "end_time": end_time}

    except Exception as e:
        global_logger.error(f"[START] Failed for match={match_code}: {e}")
        raise