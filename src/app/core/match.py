from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError, NoResultFound

from fastapi import HTTPException

from app.model.match import Match
from app.schema.match import *
from app.logger import global_logger


async def post_match_to_db(request: PostMatchRequest, session: AsyncSession) -> PostMatchResponse:
    global_logger.info(f"POST request received to create match with code: {request.match_code}.")
    new_match = Match(
        match_code = request.match_code,
        match_name = request.match_name
    )
    session.add(new_match)
    global_logger.debug(f"Match object created and added to session. match_code={request.match_code}")

    try:
        await session.commit()
        await session.refresh(new_match)
        global_logger.info(f"Match created successfully. match_code={request.match_code}, match_id={new_match.id}")
        return PostMatchResponse(
            response={'messsage': f'Add a match with match_code = {request.match_code} successfully!'}
        )
    except IntegrityError:
        await session.rollback()
        global_logger.warning(f"Failed to create match due to unique constraint violation. match_code={request.match_code}. Returning 409.")
        raise HTTPException(
            status_code=409,
            detail=f'A match with match_code={request.match_code} already exists.'
        )
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during match creation/commit for match_code={request.match_code}.')
        raise HTTPException(
            status_code=500,
            detail='An unexpected server error occurred during match creation.'
        )


async def get_all_matches_from_db(session: AsyncSession) -> GetMatchResponse:
    global_logger.info("GET request received for all matches with players info.")
    try:
        matches_query = select(Match)
        execution = await session.execute(matches_query)
        result = execution.unique().scalars().all()
        
        global_logger.info(f"Successfully retrieved {len(result)} matches.")
        
        return GetMatchResponse(
            response={
                'data': [
                    {
                        'match_name': res.match_name,
                        'match_code': res.match_code,
                    }
                for res in result
                ]
            }
        )
    except Exception:
        global_logger.exception('Unexpected error occurred while fetching all matches.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching all matches.'
        )


async def get_match_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetMatchResponse:
    global_logger.info(f"GET request received for match: {match_code} with players info.")
    try:
        match_query = select(Match).where(Match.match_code == match_code)
        execution = await session.execute(match_query)
        result = execution.unique().scalar_one_or_none()
        if result is None:
            global_logger.warning(f"Match not found: match_code={match_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'Match with match_code={match_code} not found'
            )
            
        global_logger.info(f"Successfully retrieved match: {match_code}.")
            
        return GetMatchResponse(
            response={
                'data': {
                    'match_code': match_code,
                    'match_name': result.match_name,
                    
                }
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred while fetching match from match_code={match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching match.'
        )


async def delete_match_from_db(match_code: str, session: AsyncSession) -> DeleteMatchResponse:
    """
    Deletes a match identified by its unique match_code.
    Raises 404 if not found or 409 if dependencies exist (e.g., questions, answers, records).
    """
    global_logger.info(f"DELETE request received for match: {match_code}.")
    
    try:
        # 1. Select the Match to ensure existence and get the ID
        match_query = select(Match.id).where(Match.match_code == match_code)
        execution = await session.execute(match_query)
        match_id = execution.scalar_one()

        # 2. Perform the deletion
        delete_statement = delete(Match).where(Match.id == match_id)
        await session.execute(delete_statement)
        await session.commit()
        
        global_logger.info(f"Match deleted successfully. match_code: {match_code}, ID: {match_id}.")
        return DeleteMatchResponse(
            response={'message': f'Match with match_code={match_code} deleted successfully!'}
        )
    except NoResultFound:
        # Match not found
        global_logger.warning(f"Match not found: match_code={match_code}. Returning 404.")
        raise HTTPException(
            status_code=404,
            detail=f'Match with match_code={match_code} not found.'
        )
    except IntegrityError:
        # Cannot delete due to existing foreign key dependencies (Questions, Answers, or Records belong to this Match)
        await session.rollback()
        global_logger.warning(f"Failed to delete Match {match_code} due to existing dependencies. Returning 409.")
        raise HTTPException(
            status_code=409,
            detail=f'Match with match_code={match_code} cannot be deleted because dependent records (Questions, Answers, or Records) exist. Remove dependent records first.'
        )
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during deletion of Match {match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected server error occurred during Match deletion.'
        )