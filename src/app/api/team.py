from fastapi import APIRouter, Depends

from app.db.dependencies import get_db
from app.core.team import *
from app.schema.team import *


team_router = APIRouter(prefix='/teams', tags=['Teams - Olympia Gia Định 3'])



@team_router.get(
    "/",
    response_model=GetTeamResponse,
    responses={
        200: {'model': GetTeamResponse, 'description': 'Successfully get all the teams'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_teams(session: AsyncSession=Depends(get_db)):
    return await get_all_teams_from_db(session)



@team_router.get(
    "/{team_code}",
    response_model=GetTeamResponse,
    responses={
        200: {'model': GetTeamResponse, 'description': 'Successfully get the team'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_team_from_team_code(team_code: str, session: AsyncSession=Depends(get_db)):
    return await get_team_from_team_code_from_db(team_code, session)