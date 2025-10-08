from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.player import Player
from app.schema.player import *



async def get_all_players_from_db(session: AsyncSession) -> GetPlayerResponse:
    try:
        players_query = (
            select(Player)
            .options(joinedload(Player.team))
            .join(Player.team)
        )
        execution = await session.execute(players_query)
        result = execution.scalars()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail='No players found!'
            )
        return GetPlayerResponse(
            response={
                'data': [
                {
                    'player_name': res.player_name,
                    'team_name': res.team.team_name
                }
                for res in result]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )



async def get_player_from_db(
    player_code: str, 
    session: AsyncSession
) -> GetPlayerResponse:
    try:
        # Start the base query with eager loading of the 'team' relationship
        player_query = (
            select(Player)
            .options(joinedload(Player.team))
            .join(Player.team)
        )
        player_query = player_query.where(Player.player_code == player_code)
        execution = await session.execute(player_query)
        result = execution.scalar_one_or_none()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'No player with player_code={player_code} existed'
            )
        return GetPlayerResponse(
            response={
                'data': {
                    'player_name': result.player_name,
                    'team_name': result.team.team_name
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