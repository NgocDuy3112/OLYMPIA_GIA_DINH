from fastapi import HTTPException
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.schema.v0.record_team import RecordTeamSchemaIn, RecordTeamSchemaOut
from app.model.v0.record_team import RecordTeamModel
from app.utils.v0.queries.record_team import *


async def get_team_records_from_db(session: AsyncSession) -> list[RecordTeamSchemaOut]:
    query = text(GET_TEAM_RECORDS_QUERY)
    result = await session.execute(query)
    records = result.fetchall()
    if not records:
        raise HTTPException(status_code=404, detail="Records not found!")
    return [
        RecordTeamSchemaOut(
            updated_at=record.updated_at,
            match_name=record.match_name,
            team_name=record.team_name,
            point_score=record.point_score
        )
        for record in records
    ]


async def get_team_record_by_record_id_from_db(record_id: UUID, session: AsyncSession) -> RecordTeamSchemaOut:
    query = text(GET_TEAM_RECORDS_BY_ID_QUERY)
    result = await session.execute(query.bindparams(id=record_id))
    record = result.first()
    if not record:
        raise HTTPException(status_code=404, detail="Records not found!")
    return RecordTeamSchemaOut(
        updated_at=record.updated_at,
        match_name=record.match_name,
        team_name=record.team_name,
        point_score=record.point_score
    )



async def get_team_records_by_match_code_from_db(match_code: str, session: AsyncSession) -> list[RecordTeamSchemaOut]:
    query = text(GET_TEAM_RECORDS_BY_MATCH_CODE_QUERY)
    result = await session.execute(query.bindparams(match_code=match_code))
    records = result.fetchall()
    if not records:
        raise HTTPException(status_code=404, detail="Records not found!")
    return [
        RecordTeamSchemaOut(
            updated_at=record.updated_at,
            match_name=record.match_name,
            team_name=record.team_name,
            point_score=record.point_score
        )
        for record in records
    ]


async def create_team_record_in_db(record_schema: RecordTeamSchemaIn, session: AsyncSession):
    team_id_query = text("SELECT id FROM team WHERE team_code = :team_code")
    team_id_query_result = await session.execute(team_id_query.bindparams(team_code=record_schema.team_code))
    team_row = team_id_query_result.first()
    if not team_row:
        raise HTTPException(status_code=404, detail="Team not found")
    
    record_model = RecordTeamModel(
        team_id=team_row.id,
        match_code=record_schema.match_code,
        match_name=record_schema.match_name,
        point_score=record_schema.point_score
    )
    query = text("""
        INSERT INTO record_team (
            id,
            created_at,
            updated_at,
            team_id,
            match_code,
            match_name,
            point_score
        )
        VALUES (
            :id,
            :created_at,
            :updated_at,
            :team_id,
            :match_code,
            :match_name,
            :point_score
        )
        RETURNING id
    """)
    result = await session.execute(query.bindparams(
        id=record_model.id,
        created_at=record_model.created_at,
        updated_at=record_model.updated_at,
        team_id=record_model.team_id,
        match_code=record_model.match_code,
        match_name=record_model.match_name,
        point_score=record_model.point_score
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Record insert failed")
    await session.commit()


async def update_team_record_in_db(record_id: UUID, record_schema: RecordTeamSchemaIn, session: AsyncSession):
    team_id_query = text("SELECT id FROM team WHERE team_code = :team_code")
    team_id_query_result = await session.execute(team_id_query.bindparams(player_code=record_schema.player_code))
    team_row = team_id_query_result.first()
    if not team_row:
        raise HTTPException(status_code=404, detail="Team not found")
    
    record_model = RecordTeamModel(
        updated_at=datetime.now(timezone.utc),
        team_id=team_row.id,
        match_code=record_schema.match_code,
        match_name=record_schema.match_name,
        point_score=record_schema.point_score
    )
    query = text("""
        UPDATE record_team
        SET
            updated_at = :updated_at,
            team_id = :team_id,
            match_code = :match_code,
            match_name = :match_name,
            point_score = :point_score
        WHERE id = :id
        RETURNING id
    """)
    result = await session.execute(query.bindparams(
        updated_at=record_model.updated_at,
        team_id=record_model.team_id,
        match_code=record_model.match_code,
        match_name=record_model.match_name,
        point_score=record_model.point_score,
        id=record_id
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Record not found")
    await session.commit()
    

async def delete_team_record_in_db(record_id: UUID, session: AsyncSession):
    delete_query = text("DELETE FROM record_team WHERE id = :id RETURNING id")
    result = await session.execute(delete_query.bindparams(id=record_id))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Record not found")
    await session.commit()