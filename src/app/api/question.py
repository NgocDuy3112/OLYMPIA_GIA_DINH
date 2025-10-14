from fastapi import APIRouter, Depends, File

from app.db.dependencies import get_db
from app.schema.question import *
from app.core.question import *



question_router = APIRouter(prefix='/questions', tags=['Câu hỏi'])



@question_router.post(
    "/",
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



@question_router.post(
    "/upload",
    response_model=PostQuestionResponse,
    responses={
        200: {'model': PostQuestionResponse, 'description': 'Successfully post all the questions from the question file'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def post_questions_file(file: UploadFile=File(...), session: AsyncSession=Depends(get_db)):
    return await post_questions_file_to_db(file, session)



@question_router.get(
    "/download",
    response_model=StreamingResponse,
    responses={
        200: {'model': StreamingResponse, 'description': 'Successfully get all the questions in a question file'},
        404: {'description': 'Not Found'},
        500: {'description': 'Internal Server Error'}
    }
)
async def get_all_questions_from_match_code_to_excel_file(match_code: str, session: AsyncSession=Depends(get_db)):
    return await get_all_questions_from_match_code_to_excel_file_from_db(match_code, session)