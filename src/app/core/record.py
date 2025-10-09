from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.player import Player
from app.model.match import Match
from app.model.record import Record
from app.schema.record import *



async def post_record_to_db(request: PostRecordRequest, session: AsyncSession) -> PostRecordResponse:
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
        new_record = Record(
            d_score_earned = request.d_score_earned,
            player_id = player_id,
            match_id = match_id
        )
        await session.commit()
        await session.refresh(new_record)
        return PostRecordResponse(
            response={'message': f'Add a record with player_code={request.player_code} and match_code={request.match_code} successfully!'}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )



async def get_all_records_from_player_code_from_db(player_code: str, session: AsyncSession) -> GetRecordsResponse:
    try:
        player_query = select(Player.id).where(Player.player_code == player_code)
        execution = await session.execute(player_query)
        player_found = execution.scalar_one_or_none()
        if player_found is None:
            raise HTTPException(
                status_code=404,
                detail=f'Player with player_code={player_code} not found!'
            )
        records_query = (
            select(Record)
            .where(Record.player_id == player_found.player_id)
            .options(joinedload(Record.player))
            .order_by(Record.created_at.desc())
        )
        execution = await session.execute(records_query)
        result = execution.scalars().all()
        return GetRecordsResponse(
            response={
                'data': {
                    'player_code': player_found.player_code,
                    'player_name': player_found.player_name,
                    'records': [
                        {
                            'match_code': record.match_code,
                            'd_score_earned': record.d_score_earned,
                            'updated_at': record.updated_at
                        } 
                        for record in result.records
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



async def get_all_records_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetRecordsResponse:
    try:
        match_query = select(Match).where(Match.match_code == match_code)
        execution = await session.execute(match_query)
        match_found = execution.scalar_one_or_none()
        if match_found is None:
            raise HTTPException(
                status_code=404,
                detail=f'Player with player_code={match_code} not found!'
            )
        records_query = (
            select(Record)
            .where(Record.match_id == match_found.match_id)
            .options(joinedload(Record.matches))
            .order_by(Record.created_at.desc())
        )
        execution = await session.execute(records_query)
        result = execution.scalars().all()
        return GetRecordsResponse(
            response={
                'data': {
                    'match_code': match_found.match_code,
                    'match_name': match_found.match_name,
                    'records': [
                        {
                            'player_code': record.player_code,
                            'd_score_earned': record.d_score_earned,
                            'updated_at': record.updated_at
                        }
                    for record in result.records]
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