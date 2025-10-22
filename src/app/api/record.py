from fastapi import APIRouter, Depends

from app.dependencies.db import get_db
from app.dependencies.user import authorize_user
from app.schema.record import *
from app.core.record import *


record_router = APIRouter(prefix='/records', tags=['Diễn biến'])



@record_router.get(
    "/player",
    dependencies=[Depends(authorize_user)],
    response_model=GetRecordsResponse,
    responses={
        200: {'model': GetRecordsResponse, 'description': 'Successfully get all records from a player code'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_records_from_player_code(player_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_records_from_player_code_from_db(player_code, session)



@record_router.get(
    "/match",
    dependencies=[Depends(authorize_user)],
    response_model=GetRecordsResponse,
    responses={
        200: {'model': GetRecordsResponse, 'description': 'Successfully get all records from a match code'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_records_from_match_code(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_records_from_match_code_from_db(match_code, session)



@record_router.get(
    "/match/export",
    dependencies=[Depends(authorize_user)],
    responses={
        200: {'description': 'Successfully get all records from a match code to an Excel file'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_records_from_match_code_to_excel_file(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_records_from_match_code_from_db_exported_to_excel_file(match_code, session)



@record_router.post(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=PostRecordResponse,
    responses={
        200: {'model': PostRecordResponse, 'description': 'Successfully upload a match'},
        404: {'description': 'Not Found'},
        409: {'description': 'There is an existing record'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_record(request: PostRecordRequest, session: AsyncSession=Depends(get_db)):
    return await post_record_to_db(request, session)



@record_router.put(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=PutRecordResponse,
    responses={
        200: {'model': PutRecordResponse, 'description': 'Successfully update a match'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def put_record(request: PutRecordRequest, session: AsyncSession=Depends(get_db)):
    return await put_record_to_db(request, session)