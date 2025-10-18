from fastapi import APIRouter, Depends

from app.dependencies.db import get_db
from app.dependencies.user import authorize_user
from app.core.team import *
from app.schema.team import *


team_router = APIRouter(prefix='/teams', tags=['Đội chơi'])



@team_router.get(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=GetTeamResponse,
    responses={
        200: {'model': GetTeamResponse, 'description': 'Successfully get all the teams'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_teams_with_players_info(session: AsyncSession=Depends(get_db)):
    return await get_all_teams_with_players_info_from_db(session)



@team_router.get(
    "/{team_code}",
    dependencies=[Depends(authorize_user)],
    response_model=GetTeamResponse,
    responses={
        200: {'model': GetTeamResponse, 'description': 'Successfully get the team'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_team_with_players_info_from_team_code(team_code: str, session: AsyncSession=Depends(get_db)):
    return await get_team_with_players_info_from_team_code_from_db(team_code, session)



@team_router.post(
    '/',
    dependencies=[Depends(authorize_user)],
    response_model=PostTeamResponse,
    responses={
        200: {'model': PostTeamResponse, 'description': 'Successfully post a team'},
        404: {'description': 'Not Found'},
        409: {'description': 'There is an existing record'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_team(request: PostTeamRequest, session: AsyncSession=Depends(get_db)):
    return await post_team_to_db(request, session)



@team_router.put(
    '/',
    dependencies=[Depends(authorize_user)],
    response_model=PutTeamResponse,
    responses={
        200: {'model': PutTeamResponse, 'description': 'Successfully post a team'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def put_team(request: PutTeamRequest, session: AsyncSession=Depends(get_db)):
    return await put_team_to_db(request, session)



@team_router.delete(
    "/{team_code}",
    dependencies=[Depends(authorize_user)],
    response_model=DeleteTeamResponse,
    responses={
        200: {'model': DeleteTeamResponse, 'description': 'Successfully get the team'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def delete_team_from_team_code(team_code: str, session: AsyncSession=Depends(get_db)):
    return await delete_team_from_team_code_from_db(team_code, session)