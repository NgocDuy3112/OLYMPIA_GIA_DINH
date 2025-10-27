from fastapi import APIRouter, Depends

from app.dependencies.db import get_db, get_valkey_cache
from app.dependencies.user import authorize_user
from app.core.scoreboard import *


scoreboard_router = APIRouter(prefix='/scoreboard', tags=['Bảng điểm'])



@scoreboard_router.get(
    "/recent",
    dependencies=[Depends(authorize_user)],
    responses={
        200: {'model': GetScoreboardResponse, 'description': 'Successfully retrieved the scoreboard Ezcel file'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_recent_cumulative_timeline_scoreboard(match_code: str, cache: Valkey=Depends(get_valkey_cache)):
    return await get_recent_cumulative_timeline_scoreboard_from_cache(match_code, cache)



@scoreboard_router.get(
    "/export",
    dependencies=[Depends(authorize_user)],
    responses={
        200: {'description': 'Successfully retrieved the scoreboard Ezcel file'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_cumulative_timeline_scoreboard_export_to_excel_file(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_cumulative_timeline_scoreboard_export_to_excel_file_from_db(match_code, session)