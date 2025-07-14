from fastapi import APIRouter, Depends
from typing import Union, Callable, Awaitable, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_postgresql_async_session
from app.core.v0.leaderboard import *

LeaderboardLiteral = Literal['yellow', 'white', 'red', 'pink', 'blue', 'orange', 'green', 'team']
LeaderboardCallable = Callable[[AsyncSession], Awaitable[LeaderboardSchema]]
LEADERBOARD_FUNCTIONS_MAPPING: dict[LeaderboardLiteral, LeaderboardCallable] = {
    "yellow": get_yellow_leaderboard_from_db,
    "white": get_white_leaderboard_from_db,
    "red": get_red_leaderboard_from_db,
    "pink": get_pink_leaderboard_from_db,
    "blue": get_blue_leaderboard_from_db,
    "orange": get_orange_leaderboard_from_db,
    "green": get_green_leaderboard_from_db,
    "team": get_team_leaderboard_from_db
}


v0_router = APIRouter(prefix="/v0/leaderboards", tags=['Leaderboards - GLORYTEAM'])


@v0_router.get("/{leaderboard_type}", response_model=LeaderboardSchema)
async def get_leaderboard(leaderboard_type: LeaderboardLiteral, session=Depends(get_postgresql_async_session)):
    leaderboard_function = LEADERBOARD_FUNCTIONS_MAPPING[leaderboard_type]
    return await leaderboard_function(session)