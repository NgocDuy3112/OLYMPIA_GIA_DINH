from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound

from fastapi import HTTPException

from app.model.player import Player
from app.model.match import Match
from app.model.record import Record
from app.schema.record import *
from app.logger import global_logger # Added logging import


# Helper function to find ID by code and raise 404 (Copied from answer.py for self-sufficiency)
async def _get_id_by_code(session: AsyncSession, model, code_field: str, code: str, entity_name: str) -> int:
    query = select(model.id).where(getattr(model, code_field) == code)
    try:
        execution = await session.execute(query)
        entity_id = execution.scalar_one()
        return entity_id
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f'{entity_name} with {code_field}={code} not found!'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed for {entity_name} validation.")


async def post_record_to_db(request: PostRecordRequest, session: AsyncSession) -> PostRecordResponse:
    global_logger.info(f"POST request received to create record for player: {request.player_code} in match: {request.match_code}.")
    
    try:
        # 1. Validate Player and Match existence
        player_id = await _get_id_by_code(session, Player, 'player_code', request.player_code, 'Player')
        match_id = await _get_id_by_code(session, Match, 'match_code', request.match_code, 'Match')
        global_logger.debug(f"Player ID: {player_id}, Match ID: {match_id}")
        
        # 2. Create the new Record object
        new_record = Record(
            d_score_earned = request.d_score_earned,
            player_id = player_id,
            match_id = match_id
        )
        session.add(new_record)
        global_logger.debug(f"Record object created and added to session.")
        
        # 3. Commit
        await session.commit()
        await session.refresh(new_record)
        global_logger.info(f"Record created successfully. record_id={new_record.id}")
        
        return PostRecordResponse(
            response={'message': f'Add a record with player_code={request.player_code} and match_code={request.match_code} successfully!'}
        )
    except HTTPException:
        raise
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during record creation/commit for player_code={request.player_code}, match_code={request.match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during record creation.'
        )


async def get_all_records_from_player_code_from_db(player_code: str, session: AsyncSession) -> GetRecordsResponse:
    global_logger.info(f"GET request received for all records of player: {player_code}.")
    try:
        # 1. Find Player ID and Info
        player_query = select(Player).where(Player.player_code == player_code)
        execution = await session.execute(player_query)
        player_found = execution.unique().scalar_one_or_none()
        if player_found is None:
            global_logger.warning(f"Player not found: player_code={player_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'Player with player_code={player_code} not found!'
            )

        # 2. Query Records
        records_query = (
            select(Record)
            .where(Record.player_id == player_found.id) # Use player_found.id
            .options(joinedload(Record.match)) # Assuming relation is to 'match'
            .order_by(Record.created_at.desc())
        )
        execution = await session.execute(records_query)
        records_list = execution.scalars().all() # Changed result to records_list
        
        global_logger.info(f"Successfully retrieved {len(records_list)} records for player: {player_code}.")
        
        return GetRecordsResponse(
            response={
                'data': {
                    'player_code': player_found.player_code,
                    'player_name': player_found.player_name,
                    'records': [
                        {
                            'match_code': record.match.match_code if record.match else 'N/A', # Access match_code via relationship
                            'd_score_earned': record.d_score_earned,
                            'updated_at': record.updated_at.isoformat()
                        } 
                        for record in records_list
                    ]
                }
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred while fetching records for player_code={player_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching records.'
        )


async def get_all_records_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetRecordsResponse:
    global_logger.info(f"GET request received for all records of match: {match_code}.")
    try:
        # 1. Find Match ID and Info
        match_query = select(Match).where(Match.match_code == match_code)
        execution = await session.execute(match_query)
        match_found = execution.unique().scalar_one_or_none()
        if match_found is None:
            global_logger.warning(f"Match not found: match_code={match_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'Match with match_code={match_code} not found!' # Fixed detail message
            )

        # 2. Query Records
        records_query = (
            select(Record)
            .where(Record.match_id == match_found.id) # Use match_found.id
            .options(joinedload(Record.player)) # Assuming relation is to 'player'
            .order_by(Record.created_at.desc())
        )
        execution = await session.execute(records_query)
        records_list = execution.scalars().all() # Changed result to records_list
        
        global_logger.info(f"Successfully retrieved {len(records_list)} records for match: {match_code}.")
        
        return GetRecordsResponse(
            response={
                'data': {
                    'match_code': match_found.match_code,
                    'match_name': match_found.match_name,
                    'records': [
                        {
                            'player_code': record.player.player_code if record.player else 'N/A', # Access player_code via relationship
                            'd_score_earned': record.d_score_earned,
                            'updated_at': record.updated_at.isoformat()
                        }
                    for record in records_list]
                }
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred while fetching records for match_code={match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching records.'
        )