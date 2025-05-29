from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.v0.bonus import BonusSchemaIn, BonusSchemaOut
from app.model.v0.bonus import BonusModel


async def get_bonuses_from_db(session: AsyncSession) -> list[BonusSchemaOut]:
    query = text("""
        SELECT
            B.updated_at AS updated_at,
            P.player_name AS player_name,
            B.point_score AS point_score,
            B.g_score AS g_score,
            B.d_score AS d_score
        FROM
            bonus AS B
            JOIN player AS P
            ON B.player_id = P.id
    """)
    result = await session.execute(query)
    records = result.fetchall()
    if not records:
        raise HTTPException(status_code=404, detail="Bonuses not found!")
    return [
        BonusSchemaOut(
            updated_at=record.updated_at,
            player_name=record.player_name,
            point_score=record.point_score,
            g_score=record.g_score,
            d_score=record.d_score
        )
        for record in records
    ]


async def get_bonus_by_bonus_id_from_db(bonus_id: UUID, session: AsyncSession) -> BonusSchemaOut:
    query = text("""
        SELECT
            B.updated_at AS updated_at,
            P.player_name AS player_name,
            B.point_score AS point_score,
            B.g_score AS g_score,
            B.d_score AS d_score
        FROM
            bonus AS B
            JOIN player AS P
            ON B.player_id = P.id
        WHERE B.id = :id
    """)
    result = await session.execute(query.bindparams(id=bonus_id))
    record = result.first()
    if not record:
        raise HTTPException(status_code=404, detail="Bonus not found!")
    return BonusSchemaOut(
        updated_at=record.updated_at,
        player_name=record.player_name,
        point_score=record.point_score,
        g_score=record.g_score,
        d_score=record.d_score
    )


async def get_bonuses_by_player_code_from_db(player_code: str, session: AsyncSession) -> list[BonusSchemaOut]:
    query = text("""
        SELECT
            B.updated_at AS updated_at,
            P.player_name AS player_name,
            B.point_score AS point_score,
            B.g_score AS g_score,
            B.d_score AS d_score
        FROM
            bonus AS B
            JOIN player AS P
            ON B.player_id = P.id
        WHERE P.player_code = :player_code
    """)
    result = await session.execute(query.bindparams(player_code=player_code))
    records = result.fetchall()
    if not records:
        raise HTTPException(status_code=404, detail="Bonuses not found!")
    return [
        BonusSchemaOut(
            updated_at=record.updated_at,
            player_name=record.player_name,
            point_score=record.point_score,
            g_score=record.g_score,
            d_score=record.d_score
        )
        for record in records
    ]


async def create_bonus_in_db(bonus_schema: BonusSchemaIn, session: AsyncSession):
    player_id_query = text("SELECT id FROM player WHERE player_code = :player_code")
    player_id_query_result = await session.execute(player_id_query.bindparams(player_code=bonus_schema.player_code))
    player_id_row = player_id_query_result.first()
    if not player_id_row:
        raise HTTPException(status_code=404, detail="Player not found!")
    
    bonus_model = BonusModel(player_id=player_id_row.id)
    query = text("""
        INSERT INTO bonus (
            id,
            created_at,
            updated_at,
            player_id,
            point_score,
            g_score,
            d_score
        )
        VALUES (
            :id,
            :created_at,
            :updated_at,
            :player_id,
            :point_score,
            :g_score,
            :d_score
        )
        RETURNING id
    """)
    result = await session.execute(query.bindparams(
        id=bonus_model.id,
        created_at=bonus_model.created_at,
        updated_at=bonus_model.updated_at,
        player_id=bonus_model.player_id,
        point_score=bonus_schema.point_score,
        g_score=bonus_model.g_score,
        d_score=bonus_model.d_score
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Bonus insert failed")
    await session.commit()


async def update_bonus_in_db(bonus_id: UUID, bonus_schema: BonusSchemaIn, session: AsyncSession):
    player_id_query = text("SELECT id FROM player WHERE player_code = :player_code")
    player_id_query_result = await session.execute(player_id_query.bindparams(player_code=bonus_schema.player_code))
    player_id_row = player_id_query_result.first()
    if not player_id_row:
        raise HTTPException(status_code=404, detail="Player not found!")
    
    bonus_model = BonusModel(
        updated_at=datetime.now(timezone.utc),
        player_id=player_id_row.id
    )
    query = text("""
        UPDATE bonus
        SET
            updated_at = :updated_at,
            player_id = :player_id,
            point_score = :point_score,
            g_score = :g_score,
            d_score = :d_score
        WHERE id = :id
        RETURNING id
    """)
    result = await session.execute(query.bindparams(
        updated_at=bonus_model.updated_at,
        player_id=bonus_model.player_id,
        point_score=bonus_model.point_score,
        g_score=bonus_model.g_score,
        d_score=bonus_model.d_score,
        id=bonus_id
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Bonus update failed")
    await session.commit()


async def delete_bonus_in_db(bonus_id: UUID, session: AsyncSession):
    delete_query = text("DELETE FROM bonus WHERE id = :id RETURNING id")
    result = await session.execute(delete_query.bindparams(id=bonus_id))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Bonus not found")
    await session.commit()