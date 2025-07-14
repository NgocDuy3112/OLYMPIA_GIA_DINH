from fastapi import APIRouter, Depends
from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_postgresql_async_session
from app.core.v0 import bonus


v0_router = APIRouter(prefix="/v0/bonuses", tags=['Player''s Bonuses - GLORYTEAM'])


@v0_router.get("/", response_model=Union[bonus.BonusSchemaOut, list[bonus.BonusSchemaOut]])
async def get_bonuses(bonus_id: UUID | None = None, session: AsyncSession=Depends(get_postgresql_async_session)):
    if bonus_id:
        return await bonus.get_bonus_by_bonus_id_from_db(bonus_id, session)
    return await bonus.get_bonuses_from_db(session)


@v0_router.get("/player-code/{player_code}", response_model=list[bonus.BonusSchemaOut])
async def get_bonuses_by_player_code(player_code: str, session: AsyncSession=Depends(get_postgresql_async_session)):
    return await bonus.get_bonuses_by_player_code_from_db(player_code, session)


@v0_router.post("/", status_code=201)
async def create_bonus(bonus_schema: bonus.BonusSchemaIn, session: AsyncSession=Depends(get_postgresql_async_session)):
    return await bonus.create_bonus_in_db(bonus_schema, session)


@v0_router.put("/{bonus_id}")
async def update_bonus(bonus_id: UUID, session: AsyncSession=Depends(get_postgresql_async_session)):
    return await bonus.update_bonus_in_db(bonus_id, session)


@v0_router.delete("/{bonus_id}")
async def delete_bonus(bonus_id: UUID, session: AsyncSession=Depends(get_postgresql_async_session)):
    return await bonus.delete_bonus_in_db(bonus_id, session)