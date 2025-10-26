from fastapi import APIRouter, Depends

from app.core.controller import *
from app.dependencies.db import get_valkey_pubsub
from app.dependencies.user import authorize_user


controller_router = APIRouter(prefix='/controller', tags=['Điều khiển'])



@controller_router.post(
    "/start_question",
    dependencies=[Depends(authorize_user)],
    responses={
        200: {'description': 'Successfully get the match'},
        500: {'description': 'Internal Server Error'}
    }
)
async def trigger_start_question_api(
    request_data: StartQuestionRequest,
    pubsub: Valkey=Depends(get_valkey_pubsub)
):
    return await trigger_start_question(request_data, pubsub)