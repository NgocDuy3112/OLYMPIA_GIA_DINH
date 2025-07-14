from fastapi import HTTPException
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.schema.v0.team import TeamSchemaIn, TeamSchemaOut
from app.model.v0.team import TeamModel


async def get_teams_from_db(session: AsyncSession) -> list[TeamSchemaOut]:
    result = await session.execute(text("SELECT team_name FROM team"))
    teams = result.fetchall()
    if not teams:
        raise HTTPException(status_code=404, detail="Teams not found")
    return [TeamSchemaOut(team_name=row.team_name) for row in teams]


async def get_team_by_team_id_from_db(team_id: UUID, session: AsyncSession) -> TeamSchemaOut:
    result = await session.execute(
        text("""
            SELECT team_name
            FROM team
            WHERE id = :team_id
        """).bindparams(team_id=team_id)
    )
    team = result.first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamSchemaOut(team_name=team.team_name)


async def get_team_by_team_code_from_db(team_code: str, session: AsyncSession) -> TeamSchemaOut:
    result = await session.execute(
        text("""
            SELECT team_name
            FROM team
            WHERE team_code = :team_code
        """).bindparams(team_code=team_code)
    )
    team = result.first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamSchemaOut(team_name=team.team_name)


async def create_team_in_db(team_schema: TeamSchemaIn, session: AsyncSession):
    team_model = TeamModel(
        team_code=team_schema.team_code,
        team_name=team_schema.team_name
    )
    query = text("""
        INSERT INTO team (id, created_at, updated_at, team_code, team_name)
        VALUES (:id, :created_at, :updated_at, :team_code, :team_name)
        RETURNING id
    """)

    result = await session.execute(query.bindparams(
        id=team_model.id,
        created_at=team_model.created_at,
        updated_at=team_model.updated_at,
        team_code=team_model.team_code,
        team_name=team_model.team_name
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Team creation failed")
    await session.commit()


async def update_team_in_db(team_id: UUID, team_schema: TeamSchemaIn, session: AsyncSession):
    query = text("""
        UPDATE team
        SET team_code = :team_code, team_name = :team_name, updated_at = :updated_at
        WHERE id = :team_id
        RETURNING id
    """)
    result = await session.execute(query.bindparams(
        team_id=team_id,
        updated_at=datetime.now(timezone.utc),
        team_code=team_schema.team_code,
        team_name=team_schema.team_name
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Team not found")
    await session.commit()


async def delete_team_in_db(team_id: UUID, session: AsyncSession):
    query = text("DELETE FROM team WHERE id = :team_id RETURNING id")
    result = await session.execute(query.bindparams(team_id=team_id))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Team not found")
    await session.commit()