from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.player import Player
from app.model.team import Team
from app.schema.player import *
from app.logger import global_logger


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


async def post_player_to_db(request: PostPlayerRequest, session: AsyncSession) -> PostPlayerResponse:
    global_logger.info(f"POST request received to create player with code: {request.player_code} for team: {request.team_code}.")
    
    # 1. Find the required Team ID
    try:
        team_id = await _get_id_by_code(session, Team, 'team_code', request.team_code, 'Team')
        global_logger.debug(f"Team found. team_code: {request.team_code}, team_id: {team_id}")
    except HTTPException:
        raise # Re-raise 404
    except Exception as e:
        global_logger.error(f"Failed to query team ID for team_code={request.team_code}. Error: {e.__class__.__name__}")
        raise HTTPException(status_code=500, detail="Database query failed for team validation.")


    # 2. Create the new Player object
    new_player = Player(
        player_code=request.player_code,
        player_name=request.player_name,
        team_id=team_id
    )
    session.add(new_player)
    global_logger.debug(f"Player object created and added to session. player_code={request.player_code}")

    # 3. Commit and Handle Integrity Errors
    try:
        await session.commit()
        await session.refresh(new_player)
        global_logger.info(f"Player created successfully. player_id={new_player.id}, team_id={team_id}")
        
        return PostPlayerResponse(
            response={'message': f'Player {request.player_code} created successfully for team {request.team_code}.'}
        )

    except IntegrityError:
        await session.rollback()
        global_logger.warning(f"Failed to create player due to unique constraint violation. player_code={request.player_code}. Returning 409.")
        raise HTTPException(
            status_code=409,
            detail=f'A player with code "{request.player_code}" already exists.'
        )
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during player creation/commit for player_code={request.player_code}.')
        raise HTTPException(
            status_code=500,
            detail='An unexpected server error occurred during player creation.'
        )


async def get_all_players_from_db(session: AsyncSession) -> GetPlayerResponse:
    global_logger.info("GET request received for all players.")
    try:
        players_query = (
            select(Player)
            .options(joinedload(Player.team))
        )
        execution = await session.execute(players_query)
        result = execution.unique().scalars().all()
        if not result:
            global_logger.warning("No players found in the database. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail='No players found!'
            )
        global_logger.info(f"Successfully retrieved {len(result)} players.")
        return GetPlayerResponse(
            response={
                'data': [
                {
                    'player_code': res.player_code,
                    'player_name': res.player_name,
                    'team_code': res.team.team_code if res.team else 'N/A',
                    'team_name': res.team.team_name if res.team else 'N/A'
                }
                for res in result]
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception('Unexpected error occurred while fetching all players.')
        raise HTTPException(
            status_code=500,
            detail='An unexpected error occurred while fetching all players.'
        )


async def get_player_from_player_code_from_db(
    player_code: str, 
    session: AsyncSession
) -> GetPlayerResponse:
    global_logger.info(f"GET request received for player: {player_code}.")
    try:
        player_query = (
            select(Player)
            .options(joinedload(Player.team))
            .where(Player.player_code == player_code)
        )
        execution = await session.execute(player_query)
        result = execution.unique().scalar_one_or_none()
        if result is None:
            global_logger.warning(f"Player not found: player_code={player_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'No player with player_code={player_code} existed'
            )
            
        global_logger.info(f"Successfully retrieved player: {player_code}.")
            
        return GetPlayerResponse(
            response={
                'data': {
                    'player_code': player_code,
                    'player_name': result.player_name,
                    'team_code': result.team_code if result.team else 'N/A',
                    'team_name': result.team.team_name if result.team else 'N/A'
                }
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred while fetching player_code={player_code}.')
        raise HTTPException(
            status_code=500,
            detail='An unexpected error occurred while fetching a player.'
        )