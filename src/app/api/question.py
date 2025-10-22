from fastapi import APIRouter, Depends, File

from app.dependencies.db import get_db
from app.dependencies.user import authorize_user
from app.schema.question import *
from app.core.question import *



question_router = APIRouter(prefix='/questions', tags=['Câu hỏi'])



@question_router.get(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=GetQuestionResponse,
    responses={
        200: {'model': GetQuestionResponse, 'description': 'Successfully post a question'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_questions_from_match_code(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_questions_from_match_code_from_db(match_code, session)



@question_router.get(
    "/download",
    dependencies=[Depends(authorize_user)],
    responses={
        200: {'description': 'Successfully get all the questions in a question file'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_questions_from_match_code_to_excel_file(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_questions_from_match_code_to_excel_file_from_db(match_code, session)



@question_router.post(
    "/upload",
    dependencies=[Depends(authorize_user)],
    response_model=PostQuestionResponse,
    responses={
        200: {'model': PostQuestionResponse, 'description': 'Successfully post all the questions from the question file'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_questions_file(file: UploadFile=File(...), session: AsyncSession=Depends(get_db)):
    return await post_questions_file_to_db(file, session)



@question_router.post(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=PostQuestionResponse,
    responses={
        200: {'model': PostQuestionResponse, 'description': 'Successfully post a question'},
        404: {'description': 'Not Found'},
        409: {'description': 'There is an existing record'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_question(request: PostQuestionRequest, session: AsyncSession=Depends(get_db)):
    return await post_question_to_db(request, session)



@question_router.put(
    "/",
    dependencies=[Depends(authorize_user)],
    response_model=PutQuestionResponse,
    responses={
        200: {'model': PutQuestionResponse, 'description': 'Successfully put a question'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def put_question(request: PutQuestionRequest, session: AsyncSession=Depends(get_db)):
    return await post_question_to_db(request, session)
