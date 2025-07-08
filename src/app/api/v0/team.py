from fastapi import APIRouter, Depends
from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_postgresql_async_session
from app.service.v0 import team


v0_router = APIRouter(prefix="/v0/teams", tags=['Teams- GLORYTEAM'])


@v0_router.get("/", response_model=Union[team.TeamSchemaOut, list[team.TeamSchemaOut]])
async def get_teams(team_id: UUID | None = None, session: AsyncSession=Depends(get_postgresql_async_session)):
    if team_id:
        return await team.get_team_by_team_id_from_db(team_id, session)
    return await team.get_teams_from_db(session)


@v0_router.get("/team-code/{team_code}", response_model=team.TeamSchemaOut)
async def get_team_by_team_code(team_code: str, session: AsyncSession=Depends(get_postgresql_async_session)):
    return await team.get_team_by_team_code_from_db(team_code, session)


@v0_router.post("/", status_code=201)
async def create_team(team_schema: team.TeamSchemaIn, session: AsyncSession=Depends(get_postgresql_async_session)):
    await team.create_team_in_db(team_schema, session)
    return {"message": "Team created successfully"}


@v0_router.put("/{team_id}")
async def update_team(team_id: UUID, team_schema: team.TeamSchemaIn, session: AsyncSession=Depends(get_postgresql_async_session)):
    await team.update_team_in_db(team_id, team_schema, session)
    return {"message": "Team updated successfully"}


@v0_router.delete("/{team_id}", status_code=204)
async def delete_team(team_id: UUID, session: AsyncSession=Depends(get_postgresql_async_session)):
    await team.delete_team_in_db(team_id, session)
    return {"message": "Team deleted successfully"}