from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.player import Player
from app.model.match import Match
from app.model.answer import Answer
from app.schema.answer import *



async def post_answer_to_db(request: PostAnswerRequest, session: AsyncSession) -> PostAnswerResponse:
    try:
        player_id_query = select(Player.id).where(Player.player_code == request.player_code)
        execution = await session.execute(player_id_query)
        player_id = execution.scalar_one_or_none()
        if player_id is None:
            raise HTTPException(
                status_code=404,
                detail=f'Player with player_code={request.player_code} not found!'
            )
        match_id_query = select(Match.id).where(Match.match_code == request.match_code)
        execution = await session.execute(match_id_query)
        match_id = execution.scalar_one_or_none()
        if match_id is None:
            raise HTTPException(
                status_code=404,
                detail=f'Match with match_code={request.match_code} not found!'
            )
        new_answer = Answer(
            content=request.content,
            timestamp=request.timestamp,
            player_id=player_id,
            match_id=match_id
        )
        session.add(new_answer)
        await session.commit()
        await session.refresh(new_answer)
        return PostAnswerResponse(
            response={
                'messsage': f'Add an answer of the player with player_code={request.player_code} and match_code={request.match_code} successfully!'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )



async def get_all_answers_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetAnswerResponse:
    try:
        match_id_query = select(Match.id).where(Match.match_code == match_code)
        execution = await session.execute(match_id_query)
        match_id = execution.scalar_one_or_none()
        if match_id is None:
            raise HTTPException(
                status_code=404,
                detail=f'Match with match_code={match_code} not found!'
            )
        answers_query = (
            select(Answer)
            .options(joinedload(Answer.player))
            .where(Answer.match_id == match_id)
            .order_by(Answer.timestamp.desc())
        )
        execution = await session.execute(answers_query)
        result = execution.scalars()
        answers = [
            {
                'content': res.content,
                'timestamp': res.timestamp.isoformat(),
                'player_code': res.player.player_code,
            }
            for res in result
        ]
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
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )