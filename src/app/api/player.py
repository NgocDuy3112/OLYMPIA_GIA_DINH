from fastapi import APIRouter, Depends

from app.dependencies.db import get_db
from app.dependencies.user import authorize_user
from app.core.player import *
from app.schema.player import *


player_router = APIRouter(prefix='/players', tags=['Thí sinh'])



@player_router.get(
    "/",
    dependencies=[Depends(authorize_user)],
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
    dependencies=[Depends(authorize_user)],
    response_model=GetPlayerResponse,
    responses={
        200: {'model': GetPlayerResponse, 'description': 'Successfully get the player'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_player_from_player_code(player_code: str, session: AsyncSession=Depends(get_db)):
    return await get_player_from_player_code_from_db(player_code, session)



@player_router.post(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=PostPlayerResponse,
    responses={
        200: {'model': PostPlayerResponse, 'description': 'Successfully post a player'},
        404: {'description': 'Not Found'},
        409: {'description': 'There is an existing record'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_player(request: PostPlayerRequest, session: AsyncSession=Depends(get_db)):
    return await post_player_to_db(request, session)



@player_router.put(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=PutPlayerResponse,
    responses={
        200: {'model': PutPlayerResponse, 'description': 'Successfully post a player'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def put_player(request: PutPlayerRequest, session: AsyncSession=Depends(get_db)):
    return await put_player_to_db(request, session)



@player_router.delete(
    "/{player_code}",
    dependencies=[Depends(authorize_user)],
    response_model=DeletePlayerResponse,
    responses={
        200: {'model': DeletePlayerResponse, 'description': 'Successfully delete the player'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def delete_player_from_player_code(player_code: str, session: AsyncSession=Depends(get_db)):
    return await delete_player_from_player_code_from_db(player_code, session)