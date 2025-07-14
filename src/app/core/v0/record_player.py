from fastapi import HTTPException
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.schema.v0.record_player import RecordPlayerSchemaIn, RecordPlayerSchemaOut
from app.model.v0.record_player import RecordPlayerModel
from app.utils.v0.queries.record_player import *


async def get_player_records_from_db(session: AsyncSession) -> list[RecordPlayerSchemaOut]:
    query = text(GET_PLAYER_RECORDS_QUERY)
    result = await session.execute(query)
    records = result.fetchall()
    if not records:
        raise HTTPException(status_code=404, detail="Records not found!")
    return [
        RecordPlayerSchemaOut(
            updated_at=record.updated_at,
            match_name=record.match_name,
            player_name=record.player_name,
            point_score=record.point_score
        )
        for record in records
    ]


async def get_player_record_by_record_id_from_db(record_id: UUID, session: AsyncSession) -> RecordPlayerSchemaOut:
    query = text(GET_PLAYER_RECORDS_BY_ID_QUERY)
    result = await session.execute(query.bindparams(id=record_id))
    record = result.first()
    if not record:
        raise HTTPException(status_code=404, detail="Records not found!")
    return RecordPlayerSchemaOut(
        updated_at=record.updated_at,
        match_name=record.match_name,
        player_name=record.player_name,
        point_score=record.point_score
    )
    

async def get_player_records_by_match_code_from_db(match_code: str, session: AsyncSession) -> list[RecordPlayerSchemaOut]:
    query = text(GET_PLAYER_RECORDS_BY_MATCH_CODE_QUERY)
    result = await session.execute(query.bindparams(match_code=match_code))
    records = result.fetchall()
    if not records:
        raise HTTPException(status_code=404, detail="Records not found!")
    return [
        RecordPlayerSchemaOut(
            updated_at=record.updated_at,
            match_name=record.match_name,
            player_name=record.player_name,
            point_score=record.point_score
        )
        for record in records
    ]


async def create_player_record_in_db(record_schema: RecordPlayerSchemaIn, session: AsyncSession):
    player_id_query = text("SELECT id FROM player WHERE player_code = :player_code")
    player_id_query_result = await session.execute(player_id_query.bindparams(player_code=record_schema.player_code))
    player_row = player_id_query_result.first()
    if not player_row:
        raise HTTPException(status_code=404, detail="Player not found")
    
    record_model = RecordPlayerModel(
        player_id=player_row.id,
        match_code=record_schema.match_code,
        match_name=record_schema.match_name,
        point_score=record_schema.point_score
    )
    query = text("""
        INSERT INTO record_player (
            id,
            created_at,
            updated_at,
            player_id,
            match_code,
            match_name,
            point_score
        )
        VALUES (
            :id,
            :created_at,
            :updated_at,
            :player_id,
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
        player_id=record_model.player_id,
        match_code=record_model.match_code,
        match_name=record_model.match_name,
        point_score=record_model.point_score
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Record insert failed")
    await session.commit()


async def update_player_record_in_db(record_id: UUID, record_schema: RecordPlayerSchemaIn, session: AsyncSession):
    player_id_query = text("SELECT id FROM player WHERE player_code = :player_code")
    player_id_query_result = await session.execute(player_id_query.bindparams(player_code=record_schema.player_code))
    player_row = player_id_query_result.first()
    if not player_row:
        raise HTTPException(status_code=404, detail="Player not found")
    
    record_model = RecordPlayerModel(
        updated_at=datetime.now(timezone.utc),
        player_id=player_row.id,
        match_code=record_schema.match_code,
        match_name=record_schema.match_name,
        point_score=record_schema.point_score
    )
    query = text("""
        UPDATE record_player
        SET
            updated_at = :updated_at,
            player_id = :player_id,
            match_code = :match_code,
            match_name = :match_name,
            point_score = :point_score
        WHERE id = :id
        RETURNING id
    """)
    result = await session.execute(query.bindparams(
        updated_at=record_model.updated_at,
        player_id=record_model.player_id,
        match_code=record_model.match_code,
        match_name=record_model.match_name,
        point_score=record_model.point_score,
        id=record_id
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Record not found")
    await session.commit()
    

async def delete_player_record_in_db(record_id: UUID, session: AsyncSession):
    delete_query = text("DELETE FROM record_player WHERE id = :id RETURNING id")
    result = await session.execute(delete_query.bindparams(id=record_id))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Record not found")
    await session.commit()