from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from valkey.asyncio import Valkey

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import io
import json
import pandas as pd

from app.model.player import Player
from app.model.match import Match
from app.model.record import Record
from app.model.question import Question
from app.schema.record import *
from app.logger import global_logger
from app.utils.get_id_by_code import _get_id_by_code
from app.utils.ws_event import publish_ws_event


MEDIA_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'



async def post_record_to_db(request: PostRecordRequest, cache: Valkey, session: AsyncSession) -> PostRecordResponse:
    global_logger.info(f"POST request received to create record for player: {request.player_code} in match: {request.match_code}.")
    try:
        # 1. Validate Player and Match existence
        player_id = await _get_id_by_code(session, Player, 'player_code', request.player_code, 'Player')
        match_id = await _get_id_by_code(session, Match, 'match_code', request.match_code, 'Match')
        question_id = await _get_id_by_code(session, Question, 'question_code', request.question_code, 'Question')
        global_logger.debug(f"Player ID: {player_id}, Match ID: {match_id}, Question ID: {question_id}")

        # 2. Create the new Record object
        new_record = Record(
            d_score_earned = request.d_score_earned,
            player_id = player_id,
            match_id = match_id,
            question_id = question_id
        )
        session.add(new_record)
        global_logger.debug(f"Record object created and added to session.")

        # 3. Commit
        await session.commit()
        await session.refresh(new_record)
        global_logger.info(f"Record created successfully. record_id={new_record.id}")
    
        # 4. Update cummulative D score in cache
        valkey_key = f"scoreboard:{request.match_code}"
        try:
            await cache.hincrby(valkey_key, request.player_code, request.d_score_earned)
            new_total_raw = await cache.hget(valkey_key, request.player_code)
            new_total_score = int(new_total_raw or 0)
            event = {
                "type": "player_score_updated",
                "match_code": request.match_code,
                "player_code": request.player_code,
                "d_score_earned": request.d_score_earned,
                "new_total_score": new_total_score
            }
            await publish_ws_event(cache, request.match_code, event)
            global_logger.info(f"Cache updated {request.player_code} {request.d_score_earned:+d} = {new_total_score} (match={request.match_code})")
        except Exception as valkey_err:
            global_logger.warning(f"Failed to update scoreboard for match={request.match_code}, player={request.player_code}: {valkey_err}")
        return PostRecordResponse(
            response={
                "message": f"Record created successfully for player={request.player_code}, match={request.match_code}, question={request.question_code}."
            }
        )
    except HTTPException:
        raise
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during record creation/commit for player_code={request.player_code}, match_code={request.match_code}, question_code={request.question_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during record creation.'
        )



async def put_record_to_db(request: PutRecordRequest, cache: Valkey, session: AsyncSession) -> PutRecordResponse:
    global_logger.info(f"PUT request received to update record for player: {request.player_code} in match: {request.match_code}.")
    try:
        player_id = await _get_id_by_code(session, Player, 'player_code', request.player_code, 'Player')
        match_id = await _get_id_by_code(session, Match, 'match_code', request.match_code, 'Match')
        question_id = await _get_id_by_code(session, Question, 'question_code', request.question_code)
        global_logger.debug(f"Player ID: {player_id}, Match ID: {match_id}, Question ID: {question_id}")
        record_query = (
            select(Record)
            .where(
                Record.player_id == player_id, 
                Record.match_id == match_id, 
                Record.question_id == question_id
            )
        )
        execution = await session.execute(record_query)
        record_found = execution.scalar_one_or_none()
        if record_found is None:
            raise HTTPException(status_code=404, detail="Record not found for the given player_code, match_code and question_code.")
        old_score = int(record_found.d_score_earned or 0)
        new_score = int(request.d_score_earned)
        delta = new_score - old_score
        global_logger.debug(f"Score change computed: old={old_score}, new={new_score}, delta={delta}")
        record_found.d_score_earned = new_score
        await session.commit()
        await session.refresh(record_found)
        global_logger.info(f"Record updated successfully for player_code={request.player_code}, match_code={request.match_code}, question_code={request.question_code}")
        try:
            valkey_key = f"scoreboard:{request.match_code}"
            await cache.hincrby(valkey_key, request.player_code, delta)
            new_total_raw = await cache.hget(valkey_key, request.player_code)
            new_total_score = int(new_total_raw or 0)
            event = {
                "type": "player_score_updated",
                "match_code": request.match_code,
                "player_code": request.player_code,
                "d_score_earned": request.d_score_earned,
                "new_total_score": new_total_score
            }
            await publish_ws_event(cache, request.match_code, event)
            global_logger.info(f"Cache updated: {request.player_code} {old_score} -> {new_score} = {new_total_score} (match={request.match_code})")
        except Exception as valkey_err:
            global_logger.warning(f"Failed to update scoreboard for match={request.match_code}, player={request.player_code}: {valkey_err}")
        return PutRecordResponse(response={"message": "Record updated successfully!"})
    except HTTPException:
        raise
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during record update for player_code={request.player_code}, match_code={request.match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during record update.'
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
            .where(Record.player_id == player_found.id)
            .options(joinedload(Record.match))
            .options(joinedload(Record.question))
            .order_by(Record.created_at.desc())
        )
        execution = await session.execute(records_query)
        records_list = execution.scalars().all()
        
        global_logger.info(f"Successfully retrieved {len(records_list)} records for player: {player_code}.")
        
        return GetRecordsResponse(
            response={
                'data': {
                    'player_code': player_found.player_code,
                    'player_name': player_found.player_name,
                    'records': [
                        {
                            'match_code': record.match.match_code if record.match else 'N/A', # Access match_code via relationship
                            'question_code': record.question.question_code if record.question else 'N/A',
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
            .options(joinedload(Record.question))
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
                            'player_code': record.player.player_code if record.player else 'N/A',
                            'question_code': record.question.question_code if record.question else 'N/A',
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



async def get_all_records_from_match_code_from_db_exported_to_excel_file(match_code: str, session: AsyncSession) -> StreamingResponse:
    global_logger.info(f"GET request received for all records of match: {match_code}, exporting to Excel.")
    try:
        buffer = io.BytesIO()
        response_name = f'OGD3_{match_code}_records_exported.xlsx'
        
        # 1. Find Match ID and Info
        match_query = select(Match).where(Match.match_code == match_code)
        execution = await session.execute(match_query)
        match_found = execution.unique().scalar_one_or_none()
        if match_found is None:
            global_logger.warning(f"Match not found: match_code={match_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'Match with match_code={match_code} not found!'
            )

        # 2. Query Records
        records_query = (
            select(Record)
            .where(Record.match_id == match_found.id)
            .options(joinedload(Record.player))
            .options(joinedload(Record.question))
            .order_by(Record.created_at.desc())
        )
        execution = await session.execute(records_query)
        records_list = execution.scalars().all()
        
        global_logger.info(f"Successfully retrieved {len(records_list)} records for match: {match_code}.")
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data = []
            for record in records_list:
                data.append({
                    'Mốc thời gian cập nhật': record.updated_at.isoformat(),
                    'Mã câu hỏi': record.question.question_code if record.question else 'N/A',
                    'Mã thí sinh': record.player.player_code if record.player else 'N/A',
                    'Điểm D nhận được': record.d_score_earned,
                })
            
            # --- CRITICAL FIX START: Convert data to DataFrame and write to Excel ---
            if data:
                df = pd.DataFrame(data)
                df.to_excel(writer, index=False, sheet_name=match_found.match_code)
            # --- CRITICAL FIX END ---

        # --- CRITICAL FIX START: Seek buffer and return StreamingResponse ---
        buffer.seek(0)
        return StreamingResponse( 
            content=buffer,
            media_type=MEDIA_TYPE,
            headers={'Content-Disposition': f'attachment; filename="{response_name}"'}
        )
        # --- CRITICAL FIX END ---
        
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred while fetching records for match_code={match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching records.'
        )



async def delete_all_records_from_match_code_in_db(match_code: str, session: AsyncSession) -> DeleteRecordsResponse:
    global_logger.info(f"DELETE request received for player with match_code={match_code} (soft-delete).")
    # 1. Get the match_id subquery
    match_id_subquery = select(Match.id).where(Match.match_code == match_code).scalar_subquery()
    
    # 2. Check if any questions exist for the match (optional but good for 404 response)
    # Using a select(literal(1)) for existence check is often more efficient
    existence_query = select(Question.id).where(Question.match_id == match_id_subquery).limit(1)
    exists_result = await session.execute(existence_query)
    if not exists_result.scalar_one_or_none():
        global_logger.warning(f"No records found for match with match_code={match_code} in the database. Returning 404.")
        raise HTTPException(
            status_code=404,
            detail=f'No records found for match with match_code={match_code} in the database'
        )

    # 3. Perform the bulk soft-delete update
    try:
        update_query = (
            update(Record)
            .where(Record.match_id == match_id_subquery)
            .values(is_deleted=True)
            # Instructs SQLAlchemy to return the count of rows updated
            .returning(Record.id)
        )
        
        # execution_result contains the updated rows' primary keys (if supported/necessary)
        execution_result = await session.execute(update_query)
        deleted_count = execution_result.rowcount # Get the count of affected rows

        # CRITICAL: Commit the transaction to save the changes
        await session.commit() 
        global_logger.info(f"Successfully soft-deleted {deleted_count} records for match_code={match_code}.")
        return DeleteRecordsResponse(
            response={
                'message': f'Successfully soft-deleted {deleted_count} records for match_code={match_code}.'
            }
        )
    except HTTPException:
        # Re-raise explicit HTTPExceptions (like the 404 if placed inside the try block)
        raise
    except Exception:
        # Rollback in case of any other error
        await session.rollback()
        global_logger.exception(f'Unexpected error occurred during soft-deletion of records for match_code={match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during record deletion.'
        )