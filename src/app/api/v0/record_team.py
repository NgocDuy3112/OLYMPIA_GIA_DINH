from fastapi import APIRouter, Depends
from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_postgresql_async_session
from app.service.v0 import record_team


v0_router = APIRouter(prefix="/v0/team-records", tags=['Team''s Records'])


@v0_router.get("/", response_model=Union[record_team.RecordTeamSchemaOut, list[record_team.RecordTeamSchemaOut]])
async def get_team_records(record_id: UUID | None = None, session: AsyncSession=Depends(get_postgresql_async_session)):
    if record_id:
        return await record_team.get_team_record_by_record_id_from_db(record_id, session)
    return await record_team.get_team_records_from_db(session)


@v0_router.get("/match-code/{match_code}", response_model=list[record_team.RecordTeamSchemaOut])
async def get_team_records_by_match_code(match_code: str, session: AsyncSession=Depends(get_postgresql_async_session)):
    return await record_team.get_team_records_by_match_code_from_db(match_code, session)


@v0_router.post("/", status_code=201)
async def create_player_record(record_schema: record_team.RecordTeamSchemaIn, session: AsyncSession=Depends(get_postgresql_async_session)):
    await record_team.create_team_record_in_db(record_schema, session)
    return {"message": "Record created successfully!"}


@v0_router.put("/{record_id}")
async def update_player_record(record_id: UUID, record_schema: record_team.RecordTeamSchemaIn, session: AsyncSession=Depends(get_postgresql_async_session)):
    await record_team.update_team_record_in_db(record_id, record_schema, session)
    return {"message": "Record updated successfully!"}


@v0_router.delete("/{record_id}")
async def delete_player_record(record_id: UUID, session: AsyncSession=Depends(get_postgresql_async_session)):
    await record_team.delete_team_record_in_db(record_id, session)
    return {"message": "Record deleted successfully!"}