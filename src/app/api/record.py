from fastapi import APIRouter, Depends

from app.db.dependencies import get_db
from app.schema.record import *
from app.core.record import *


record_router = APIRouter(prefix='/records', tags=['Diễn biến'])



@record_router.post(
    "/",
    response_model=PostRecordResponse,
    responses={
        200: {'model': PostRecordResponse, 'description': 'Successfully upload a match'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_record(request: PostRecordRequest, session: AsyncSession=Depends(get_db)):
    return await post_record_to_db(request, session)



@record_router.get(
    "/",
    response_model=GetRecordsResponse,
    responses={
        200: {'model': GetRecordsResponse, 'description': 'Successfully get a record from a player code'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_records_from_player_code(player_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_records_from_player_code_from_db(player_code, session)