from fastapi import APIRouter, Depends
from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_postgresql_async_session
from app.service.v0 import player

v0_router = APIRouter(prefix="/v0/players", tags=['Players'])


@v0_router.get("/", response_model=Union[player.PlayerSchemaOut, list[player.PlayerSchemaOut]])
async def get_players(player_id: UUID | None = None, session: AsyncSession = Depends(get_postgresql_async_session)):
    if player_id:
        return await player.get_player_by_player_id_from_db(player_id, session)
    return await player.get_players_from_db(session)


@v0_router.get("/player-code/{player_code}", response_model=player.PlayerSchemaOut)
async def get_players_by_player_code(player_code: str, session: AsyncSession = Depends(get_postgresql_async_session)):
    return await player.get_player_by_player_code_from_db(player_code, session)


@v0_router.post("/", status_code=201)
async def create_player(player_schema: player.PlayerSchemaIn, session: AsyncSession = Depends(get_postgresql_async_session)):
    await player.create_player_in_db(player_schema, session)
    return {"message": "Player created successfully!"}


@v0_router.put("/{player_id}")
async def update_player(player_id: UUID, player_schema: player.PlayerSchemaIn, session: AsyncSession = Depends(get_postgresql_async_session)):
    await player.update_player_in_db(player_id, player_schema, session)
    return {'message': 'Player updated successfully!'}


@v0_router.delete("/{player_id}")
async def delete_player(player_id: UUID, session: AsyncSession = Depends(get_postgresql_async_session)):
    await player.delete_player_in_db(player_id, session)
    return {'message': 'Player deleted successfully!'}