from fastapi import APIRouter, Depends

from app.core.controller import *
from app.dependencies.db import get_valkey_pubsub
from app.dependencies.user import authorize_user


controller_router = APIRouter(prefix='/controller', tags=['Điều khiển'])



@controller_router.post(
    "/start_timer",
    dependencies=[Depends(authorize_user)],
    response_model=StartQuestionResponse,
    responses={
        200: {'description': 'Successfully get the match'},
        500: {'description': 'Internal Server Error'}
    }
)
async def trigger_start_timer_api(request: StartQuestionRequest, pubsub: Valkey=Depends(get_valkey_pubsub)):
    return await trigger_start_timer(request, pubsub)



@controller_router.post(
    "/pick_question",
    dependencies=[Depends(authorize_user)],
    response_model=PickQuestionResponse,
    responses={
        200: {'description': 'Successfully get the match'},
        500: {'description': 'Internal Server Error'}
    }
)
async def trigger_pick_question_api(request: PickQuestionRequest, pubsub: Valkey=Depends(get_valkey_pubsub)):
    return await trigger_pick_question(request, pubsub)



@controller_router.websocket("/ws/match/{match_code}")
async def match_websocket_endpoint(
    websocket: WebSocket,
    match_code: str,
    valkey: Valkey = Depends(get_valkey_pubsub),
):
    await handle_match_websocket(websocket, match_code, valkey)