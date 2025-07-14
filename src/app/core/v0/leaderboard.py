from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.v0.leaderboard import *
from app.utils.v0.queries.leaderboard import *

LeaderboardSchema = YellowPlayerLeaderboardSchema | WhitePlayerLeaderboardSchema | RedPlayerLeaderboardSchema | PinkPlayerLeaderboardSchema | BluePlayerLeaderboardSchema | OrangePlayerLeaderboardSchema | GreenPlayerLeaderboardSchema | TeamLeaderboardSchema


async def get_yellow_leaderboard_from_db(session: AsyncSession) -> YellowPlayerLeaderboardSchema:
    query = text(YELLOW_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        PlayerPointJerseyStatisticsSchema(
            player_name=row.player_name,
            total_points=row.total_points,
            bonus_points=row.bonus_points
        )
        for row in rows
    ]
    return YellowPlayerLeaderboardSchema(leaderboard=leaderboard)


async def get_white_leaderboard_from_db(session: AsyncSession) -> WhitePlayerLeaderboardSchema:
    query = text(WHITE_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        PlayerPointJerseyStatisticsSchema(
            player_name=row.player_name,
            total_points=row.total_points,
            bonus_points=row.bonus_points
        )
        for row in rows
    ]
    return WhitePlayerLeaderboardSchema(leaderboard=leaderboard)


async def get_red_leaderboard_from_db(session: AsyncSession) -> RedPlayerLeaderboardSchema:
    query = text(RED_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        PlayerPointJerseyStatisticsSchema(
            player_name=row.player_name,
            total_points=row.total_points,
            bonus_points=row.bonus_points
        )
        for row in rows
    ]
    return RedPlayerLeaderboardSchema(leaderboard=leaderboard)


async def get_pink_leaderboard_from_db(session: AsyncSession) -> PinkPlayerLeaderboardSchema:
    query = text(PINK_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        PlayerPointBasicStatisticsSchema(
            player_name=row.player_name,
            total_points=row.max_points
        )
        for row in rows
    ]
    return PinkPlayerLeaderboardSchema(leaderboard=leaderboard)


async def get_blue_leaderboard_from_db(session: AsyncSession) -> BluePlayerLeaderboardSchema:
    query = text(BLUE_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        PlayerGBasicStatisticsSchema(
            player_name=row.player_name,
            total_g=row.total_g
        )
        for row in rows
    ]
    return BluePlayerLeaderboardSchema(leaderboard=leaderboard)


async def get_orange_leaderboard_from_db(session: AsyncSession) -> OrangePlayerLeaderboardSchema:
    query = text(ORANGE_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        PlayerDBasicStatisticsSchema(
            player_name=row.player_name,
            total_d=row.total_d
        )
        for row in rows
    ]
    return OrangePlayerLeaderboardSchema(leaderboard=leaderboard)


async def get_green_leaderboard_from_db(session: AsyncSession) -> GreenPlayerLeaderboardSchema:
    query = text(GREEN_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        PlayerCorrectnessBasicStatisticsSchema(
            player_name=row.player_name,
            total_correct_answers=row.total_correct_answers
        )
        for row in rows
    ]
    return GreenPlayerLeaderboardSchema(leaderboard=leaderboard)


async def get_team_leaderboard_from_db(session: AsyncSession) -> TeamLeaderboardSchema:
    query = text(TEAM_LEADERBOARD_QUERY)
    result = await session.execute(query)
    rows = result.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Leaderboard can not be created!")
    leaderboard = [
        TeamBasicStatisticsSchema(
            team_name=row.team_name,
            total_points=row.total_points
        )
        for row in rows
    ]
    return TeamLeaderboardSchema(leaderboard=leaderboard)