from fastapi import APIRouter, Depends

from app.dependencies.db import get_db, get_valkey_cache
from app.dependencies.user import authorize_user
from app.schema.answer import *
from app.core.answer import *


answer_router = APIRouter(prefix='/answers', tags=['Câu trả lời'])



@answer_router.post(
    "/", 
    response_model=PostAnswerResponse,
    responses={
        200: {'model': PostAnswerResponse, 'description': 'Successfully upload an answer'},
        404: {'description': 'Not Found'},
        409: {'description': 'There is an existing record'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_answer(request: PostAnswerRequest, session: AsyncSession=Depends(get_db), cache: Valkey=Depends(get_valkey_cache)):
    return await post_answer_to_db(request, session, cache)



@answer_router.get(
    "/{match_code}",
    dependencies=[Depends(authorize_user)],
    response_model=GetAnswerResponse,
    responses={
        200: {'model': GetAnswerResponse, 'description': 'Successfully get all the answers from the match_code'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_answers_from_match_code(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_answers_from_match_code_from_db(match_code, session)



@answer_router.get(
    "/recent/{match_code}",
    response_model=GetAnswerResponse,
    responses={
        200: {'model': GetAnswerResponse, 'description': 'Successfully get all the recent answers from the match_code'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_recent_answers_from_match_code(match_code: str, cache: Valkey=Depends(get_valkey_cache)):
    return await get_recent_answers_from_match_code_from_cache(match_code, cache)