from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.v0.player import PlayerSchemaIn, PlayerSchemaOut
from app.model.v0.player import PlayerModel


async def get_players_from_db(session: AsyncSession) -> list[PlayerSchemaOut]:
    query = text("""
        SELECT
            t.team_name AS team_name,
            p.player_name AS player_name,
            p.birth_year AS birth_year,
            p.is_dnf AS is_dnf
        FROM
            player AS p
            JOIN team AS t ON p.team_id = t.id;
    """)
    result = await session.execute(query)
    players = result.fetchall()
    return [
        PlayerSchemaOut(
            team_name=player.team_name,
            player_name=player.player_name,
            birth_year=player.birth_year,
            is_dnf=player.is_dnf
        )
        for player in players
    ]


async def get_player_by_player_id_from_db(player_id: UUID, session: AsyncSession) -> PlayerSchemaOut:
    query = text("""
        SELECT
            t.team_name AS team_name,
            p.player_name AS player_name,
            p.birth_year AS birth_year,
            p.is_dnf AS is_dnf
        FROM player AS p
        JOIN team AS t ON p.team_id = t.id
        WHERE p.id = :player_id;
    """)
    result = await session.execute(query.bindparams(player_id=player_id))
    player = result.first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerSchemaOut(
        team_name=player.team_name,
        player_name=player.player_name,
        birth_year=player.birth_year,
        is_dnf=player.is_dnf
    )


async def get_player_by_player_code_from_db(player_code: str, session: AsyncSession) -> PlayerSchemaOut:
    query = text("""
        SELECT
            t.team_name AS team_name,
            p.player_name AS player_name,
            p.birth_year AS birth_year,
            p.is_dnf AS is_dnf
        FROM player AS p
        JOIN team AS t ON p.team_id = t.id
        WHERE p.player_code = :player_code;
    """)
    result = await session.execute(query.bindparams(player_code=player_code))
    player = result.first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerSchemaOut(
        team_name=player.team_name,
        player_name=player.player_name,
        birth_year=player.birth_year,
        is_dnf=player.is_dnf
    )


async def create_player_in_db(player_schema: PlayerSchemaIn, session: AsyncSession):
    # Get team_id from team_code
    team_id_query = text("SELECT id FROM team WHERE team_code = :team_code")
    team_result = await session.execute(team_id_query.bindparams(team_code=player_schema.team_code))
    team_row = team_result.first()
    if not team_row:
        raise HTTPException(status_code=404, detail="Team not found")
    player_model = PlayerModel(
        team_id=team_row.id,
        team_code=player_schema.team_code,
        player_code=player_schema.player_code,
        player_name=player_schema.player_name,
        birth_year=player_schema.birth_year,
        is_dnf=player_schema.is_dnf,
        is_afk=player_schema.is_afk,
    )
    insert_query = text("""
        INSERT INTO player (
            id, 
            created_at, 
            updated_at,
            team_id, 
            player_code,
            player_name, 
            birth_year, 
            is_dnf
        )
        VALUES (
            :id, 
            :created_at, 
            :updated_at,
            :team_id, 
            :team_code, 
            :player_code,
            :player_name, 
            :birth_year, 
            :is_dnf
        )
        RETURNING id
    """)
    result = await session.execute(insert_query.bindparams(
        id=player_model.id,
        created_at=player_model.created_at,
        updated_at=player_model.updated_at,
        team_id=player_model.team_id,
        player_code=player_model.player_code,
        player_name=player_model.player_name,
        birth_year=player_model.birth_year,
        is_dnf=player_model.is_dnf
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Player insert failed")
    await session.commit()
    

async def update_player_in_db(player_id: UUID, player_schema: PlayerSchemaIn, session: AsyncSession):
    # Get team_id from team_code
    team_id_query = text("SELECT id FROM team WHERE team_code = :team_code")
    team_result = await session.execute(team_id_query.bindparams(team_code=player_schema.team_code))
    team_row = team_result.first()
    if not team_row:
        raise HTTPException(status_code=404, detail="Team not found")
    
    player_model = PlayerModel(
        team_id=team_row.id,
        updated_at=datetime.now(timezone.utc),
        team_code=player_schema.team_code,
        player_code=player_schema.player_code,
        player_name=player_schema.player_name,
        birth_year=player_schema.birth_year,
        is_dnf=player_schema.is_dnf,
    )
    update_query = text("""
        UPDATE player
        SET
            updated_at = :updated_at,
            team_id = :team_id,
            player_code = :player_code,
            player_name = :player_name,
            birth_year = :birth_year,
            is_dnf = :is_dnf
        WHERE id = :player_id
        RETURNING id
    """)
    result = await session.execute(update_query.bindparams(
        team_id=player_model.team_id,
        player_code=player_model.player_code,
        player_name=player_model.player_name,
        birth_year=player_model.birth_year,
        updated_at=player_model.updated_at,
        is_dnf=player_model.is_dnf,
        player_id=player_id
    ))
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Player not found")
    await session.commit()


async def delete_player_in_db(player_id: UUID, session: AsyncSession):
    delete_query = text("DELETE FROM player WHERE id = :player_id RETURNING id")
    result = await session.execute(delete_query.bindparams(player_id=player_id))
    row = result.first()
    if not row:
        raise HTTPException(status_code=500, detail="Team not found")
    await session.commit()