from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound

from fastapi import HTTPException

from app.model.player import Player
from app.model.match import Match
from app.model.answer import Answer
from app.schema.answer import *
from app.logger import global_logger


# Helper function to find ID by code and raise 404
async def _get_id_by_code(session: AsyncSession, model, code_field: str, code: str, entity_name: str) -> int:
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


async def post_answer_to_db(request: PostAnswerRequest, session: AsyncSession) -> PostAnswerResponse:
    global_logger.info(f"POST request received to record answer for player: {request.player_code} in match: {request.match_code}.")
    
    try:
        # 1. Validate Player and Match existence
        player_id = await _get_id_by_code(session, Player, 'player_code', request.player_code, 'Player')
        match_id = await _get_id_by_code(session, Match, 'match_code', request.match_code, 'Match')
        
        # 2. Create the new Answer object
        new_answer = Answer(
            content=request.content,
            timestamp=request.timestamp,
            player_id=player_id,
            match_id=match_id
        )
        session.add(new_answer)
        global_logger.debug(f"Answer object created and added to session.")

        # 3. Commit
        await session.commit()
        await session.refresh(new_answer)
        global_logger.info(f"Answer recorded successfully. player_id={player_id}, match_id={match_id}")
        
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
            detail=f'An unexpected error occurred during answer creation.'
        )


async def get_all_answers_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetAnswerResponse:
    global_logger.info(f"GET request received for all answers in match: {match_code}.")
    try:
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')
        
        answers_query = (
            select(Answer)
            .options(joinedload(Answer.player))
            .where(Answer.match_id == match_id)
            .order_by(Answer.timestamp.desc())
        )
        execution = await session.execute(answers_query)
        result = execution.unique().scalars().all()

        answers = [
            {
                'content': res.content,
                'timestamp': res.timestamp.isoformat(),
                'player_code': res.player.player_code,
            }
            for res in result
        ]
        
        global_logger.info(f"Successfully retrieved {len(answers)} answers for match: {match_code}.")
        
        return GetAnswerResponse(
            response={
                'data': {
                    'match_code': match_code,
                    'answers': answers
                }
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred while fetching answers for match_code={match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching answers.'
        )