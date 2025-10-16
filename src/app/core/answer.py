import uuid
import json

from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from valkey.asyncio import Valkey

from fastapi import HTTPException

from app.model.player import Player
from app.model.match import Match
from app.model.answer import Answer
from app.model.question import Question
from app.schema.answer import *
from app.logger import global_logger



# Helper function to find ID by code and raise 404
async def _get_id_by_code(session: AsyncSession, model, code_field: str, code: str, entity_name: str) -> uuid.UUID:
    query = select(model.id).where(getattr(model, code_field) == code)
    try:
        execution = await session.execute(query)
        entity_id = execution.scalar_one()
        global_logger.debug(f"{entity_name} found. {code_field}: {code}, id: {entity_id}")
        return entity_id
    except NoResultFound:
        global_logger.warning(f"{entity_name} not found: {code_field}={code}. Returning 404.")
        raise HTTPException(
            status_code=404,
            detail=f'{entity_name} with {code_field}={code} not found!'
        )
    except Exception as e:
        global_logger.error(f"Failed to query {entity_name} ID for {code_field}={code}. Error: {e.__class__.__name__}")
        raise HTTPException(status_code=500, detail=f"Database query failed for {entity_name} validation.")



async def post_answer_to_db(request: PostAnswerRequest, session: AsyncSession, cache: Valkey) -> PostAnswerResponse:
    global_logger.info(f"POST request received to record answer for player: {request.player_code} in match: {request.match_code}.")
    try:
        # 1. Validate Player and Match existence
        player_id = await _get_id_by_code(session, Player, 'player_code', request.player_code, 'Player')
        match_id = await _get_id_by_code(session, Match, 'match_code', request.match_code, 'Match')
        question_id = await _get_id_by_code(session, Question, 'question_code', request.question_code, 'Question')
        # 2. Create the new Answer object
        new_answer = Answer(
            content=request.content,
            timestamp=round(request.timestamp, 3),
            player_id=player_id,
            match_id=match_id,
            question_id=question_id
        )
        session.add(new_answer)
        global_logger.debug(f"Answer object created and added to session.")

        # 3. Commit
        await session.commit()
        await session.refresh(new_answer)
        global_logger.info(f"Answer recorded successfully. player_id={player_id}, match_id={match_id}")
        cache_key = f"answers:{request.match_code}:{request.player_code}"
        new_entry = {
            "content": new_answer.content,
            "timestamp": float(new_answer.timestamp) if isinstance(new_answer.timestamp, Decimal) else new_answer.timestamp,
            "player_code": request.player_code,
            "match_code": request.match_code,
            "question_code": request.question_code
        }
        await cache.set(cache_key, json.dumps(new_entry), ex=60)
        global_logger.info(f"Cached answer for {cache_key}")
        return PostAnswerResponse(
            response={
                'messsage': f'Add an answer of the player with player_code={request.player_code} and match_code={request.match_code} successfully!'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        global_logger.exception(f'Unexpected error during answer creation/commit for player_code={request.player_code}, match_code={request.match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred: {e}'
        )



async def get_recent_answers_from_match_code_from_cache(match_code: str, cache: Valkey) -> GetAnswerResponse:
    global_logger.info(f"GET request received for recent answers of match={match_code}.")
    try:
        # 1. Find all keys that belong to this match
        pattern = f"answers:{match_code}:*"
        keys = await cache.keys(pattern)
        global_logger.debug(f"Found {len(keys)} cached answers for match={match_code}.")
        answers = []
        if keys:
            # 2. Fetch all answers concurrently
            cached_values = await cache.mget(*keys)
            # 3. Deserialize JSON
            for raw in cached_values:
                if raw:
                    try:
                        entry = json.loads(raw)
                        answer_obj = {
                            "player_code": entry.get("player_code", ""),
                            "question_code": entry.get("question_code", ""),
                            "content": entry.get("content", ""),
                            "timestamp": entry.get("timestamp", 0.000)
                        }
                        answers.append(answer_obj)
                    except json.JSONDecodeError:
                        global_logger.warning("Failed to parse cached JSON for one answer entry.")
        else:
            global_logger.info(f"No cached answers found for match={match_code}.")

        global_logger.info(f"Returning {len(answers)} cached answers for match={match_code}.")
        return GetAnswerResponse(
            response={
                "data": {
                    "match_code": match_code,
                    "answers": answers
                }
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f"Error while retrieving answers from Valkey for match={match_code}.")
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during answer creation.'
        )



async def get_all_answers_from_match_code_from_db(
    match_code: str,
    session: AsyncSession
) -> GetAnswerResponse:
    global_logger.info(f"GET request received for latest answers of match_code={match_code}.")
    try:
        # 1️⃣ Validate match existence
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')

        # 2️⃣ Subquery — latest updated_at per (player_id, question_id)
        subq = (
            select(
                Answer.player_id,
                Answer.question_id,
                func.max(Answer.updated_at).label("latest_updated_at")
            )
            .where(Answer.match_id == match_id)
            .group_by(Answer.player_id, Answer.question_id)
            .subquery()
        )

        # 3️⃣ Join main Answer table with subquery to get latest full records
        latest_answers_query = (
            select(Answer)
            .join(
                subq,
                (Answer.player_id == subq.c.player_id)
                & (Answer.question_id == subq.c.question_id)
                & (Answer.updated_at == subq.c.latest_updated_at)
            )
            .options(joinedload(Answer.player), joinedload(Answer.question))
            .order_by(Answer.player_id.asc(), Answer.question_id.asc())
        )

        execution = await session.execute(latest_answers_query)
        results = execution.scalars().all()

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f'No answers found for match_code={match_code}'
            )

        global_logger.info(f"Retrieved {len(results)} latest answers for match_code={match_code}.")

        # 4️⃣ Build clean JSON-safe response
        answers = [
            {
                "player_code": res.player.player_code if res.player else None,
                "question_code": res.question.question_code if res.question else None,
                "content": res.content,
                "timestamp": float(res.timestamp) if res.timestamp is not None else None,
            }
            for res in results
        ]

        # 5️⃣ Return structured response
        return GetAnswerResponse(
            response={
                "match_code": match_code,
                "answers": answers
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        global_logger.exception(f"Error while retrieving latest answers for match_code={match_code}.")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {e}"
        )