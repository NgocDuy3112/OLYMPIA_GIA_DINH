from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.match import Match
from app.schema.match import *



async def post_match_to_db(request: PostMatchRequest, session: AsyncSession) -> PostMatchResponse:
    try:
        new_match = Match(
            match_code = request.match_code,
            match_name = request.match_name
        )
        session.add(new_match)
        await session.commit()
        await session.refresh(new_match)
        return PostMatchResponse(
            response={'messsage': f'Add a match with match_code = {request.match_code} successfully!'}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )



async def get_all_matches_from_db(session: AsyncSession) -> GetMatchResponse:
    try:
        matches_query = (
            select(Match)
            .options(joinedload(Match.players))
            .join(Match.players)
        )
        execution = await session.execute(matches_query)
        result = execution.scalars()
        return GetMatchResponse(
            response={
                'data': [
                    {
                        'match_name': res.match_name,
                        'match_code': res.match_code,
                        'players': [
                            {
                                'player_name': p.player_name,
                                'player_code': p.player_code
                            }
                        for p in result.players
                        ]
                    }
                for res in result
                ]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )



async def get_match_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetMatchResponse:
    try:
        match_query = (
            select(Match)
            .options(joinedload(Match.players))
            .join(Match.players)
            .where(Match.match_code == match_code)
        )
        execution = await session.execute(match_query)
        result = execution.scalar_one_or_none()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'Match with match_code={match_code} not found'
            )
        return GetMatchResponse(
            response={
                'data': {
                    'match_code': match_code,
                    'match_name': result.match_name,
                    'players': [
                        {
                            'player_name': p.player_name,
                            'player_code': p.player_code
                        }
                    for p in result.players
                    ]
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