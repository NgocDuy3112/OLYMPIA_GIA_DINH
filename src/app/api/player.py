from fastapi import APIRouter, Depends

from app.db.dependencies import get_db
from app.core.player import *
from app.schema.player import *


player_router = APIRouter(prefix='/players', tags=['Thí sinh'])



@player_router.get(
    "/",
    response_model=GetPlayerResponse,
    responses={
        200: {'model': GetPlayerResponse, 'description': 'Successfully get all the players'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_players(session: AsyncSession=Depends(get_db)):
    return await get_all_players_from_db(session)



@player_router.get(
    "/{player_code}",
    response_model=GetPlayerResponse,
    responses={
        200: {'model': GetPlayerResponse, 'description': 'Successfully get the player'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_player_from_player_code(player_code: str, session: AsyncSession=Depends(get_db)):
    return await get_player_from_player_code_from_db(player_code, session)