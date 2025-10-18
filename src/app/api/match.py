from fastapi import APIRouter, Depends

from app.dependencies.db import get_db
from app.dependencies.user import authorize_user
from app.schema.match import *
from app.core.match import *


match_router = APIRouter(prefix='/matches', tags=['Trận đấu'])



@match_router.get(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=GetMatchResponse,
    responses={
        200: {'model': GetMatchResponse, 'description': 'Successfully get all the matches'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_matches(session: AsyncSession=Depends(get_db)):
    return await get_all_matches_from_db(session)



@match_router.get(
    "/{match_code}",
    dependencies=[Depends(authorize_user)],
    response_model=GetMatchResponse,
    responses={
        200: {'model': GetMatchResponse, 'description': 'Successfully get the match'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_match_from_match_code(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_match_from_match_code_from_db(match_code, session)



@match_router.post(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=PostMatchResponse,
    responses={
        200: {'model': PostMatchResponse, 'description': 'Successfully upload a match'},
        404: {'description': 'Not Found'},
        409: {'description': 'There is an existing record'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_match(request: PostMatchRequest, session: AsyncSession=Depends(get_db)):
    return await post_match_to_db(request, session)



@match_router.delete(
    "/{match_code}",
    dependencies=[Depends(authorize_user)],
    response_model=DeleteMatchResponse,
    responses={
        200: {'model': DeleteMatchResponse, 'description': 'Successfully get the match'},
        404: {'description': 'Not Found'},
        409: {'description': 'There are dependent records need to be solved'},
        500: {'description': 'Internal Server Error'}
    }
)
async def delete_match_from_match_code(match_code: str, session: AsyncSession=Depends(get_db)):
    return await delete_match_from_match_code_from_db(match_code, session)