from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

import io
import re
import pandas as pd

from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.model.match import Match
from app.model.question import Question
from app.schema.question import *


SHEET_NAMES = ['LAM_NONG', 'VUOT_DEO', 'BUT_PHA', 'NUOC_RUT']
COLUMN_NAMES = ['Code', 'Câu hỏi', 'Media', 'Đáp án', 'Giải thích', 'Nguồn tham khảo', 'Ghi chú']
XLSX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"



def convert_sheet_name_to_round_code(sheet_name: str) -> str:
    parts = sheet_name.split("_")
    return "".join([part[0] for part in parts])



async def post_question_to_db(request: PostQuestionRequest, session: AsyncSession) -> PostQuestionResponse:
    try:
        match_id_query = select(Match).where(Match.match_code == request.match_code)
        execution = await session.execute(match_id_query)
        match_id = execution.scalar_one_or_none()
        if match_id is None:
            raise HTTPException(
                status_code=404,
                detail=f"Match with match_code={request.match_code} not found"
            )
        new_question = Question(
            match_id=match_id,
            question_code=request.question_code,
            content=request.content,
            media_sources=request.media_sources,
            correct_answers=request.correct_answers,
            explaination=request.explaination,
            citation=request.citation,
            note=request.note
        )
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        return PostQuestionResponse(
            response={
                'message': 'Add a new question successfully!'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )



async def post_questions_file_to_db(file: UploadFile, session: AsyncSession) -> PostQuestionResponse:
    try:
        original_filename = file.filename
        pattern = r'^OGD3_M\d{2}\.xls(x)?$'
        if not re.match(pattern, original_filename):
            raise HTTPException(
                status_code=400,
                detail='The Excel file name is not in the correct format: OGD3_Mxx.xls(x)'
            )
        match_code = original_filename.split(".")[0].split("_")[1]
        match_id_query = select(Match.id).where(Match.match_code == match_code)
        execution = await session.execute(match_id_query)
        match_id = execution.scalar_one_or_none()
        if match_id is None:
            raise HTTPException(
                status_code=404,
                detail=f"Match with match_code={match_code} not found"
            )
        content = await file.read()
        content_io = io.BytesIO(content)
        questions_list: list[Question] = []
        for sheet_name in SHEET_NAMES:
            content_io.seek(0)
            df = pd.read_excel(content_io, sheet_name)
            rows_as_dicts = df.to_dict('records')
            for row in rows_as_dicts:
                questions_list.append(Question(
                    match_id=match_id,
                    question_code=row['Code'],
                    content=row['Câu hỏi'],
                    media_sources=row['Media'],
                    correct_answers=row['Đáp án'],
                    explaination=row['Giải thích'],
                    citation=row['Nguồn tham khảo'],
                    note=row['Ghi chú']
                ))
        session.add_all(questions_list)
        await session.commit()
        return PostQuestionResponse(
            response={
                'message': f'Upload questions from file {original_filename} successfully'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )



async def get_all_questions_from_match_code_to_excel_file_from_db(match_code: str, session: AsyncSession) -> StreamingResponse:
    try:
        match_id_query = select(Match.id).where(Match.match_code == match_code)
        execution = await session.execute(match_id_query)
        match_id = execution.scalar_one_or_none()
        if match_id is None:
            raise HTTPException(
                status_code=404,
                detail=f"Match with match_code={match_code} not found"
            )
        response_file_name = f'OGD3_{match_code}.xlsx'
        excel_file_buffer = io.BytesIO()
        round_codes = [convert_sheet_name_to_round_code(sheet_name) for sheet_name in SHEET_NAMES]
        questions_by_round: dict[str, list] = {}
        for round_code in round_codes:
            questions_query = select(Question).where(Question.question_code.like(f'{round_code}%'))
            execution = await session.execute(questions_query)
            questions = execution.scalars().all()
            if len(questions) == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"No questions found from match_code={match_code}"
                )
            questions_by_round[round_code] = questions
        with pd.ExcelWriter(excel_file_buffer, engine='openpyxl') as writer:
            for sheet_name, questions_list in questions_by_round.items():
                data_for_df = [
                    {
                        'Code': question.question_code,
                        'Câu hỏi': question.content,
                        'Media': question.media_sources,
                        'Đáp án': question.correct_answers,
                        'Giải thích': question.explaination,
                        'Nguồn tham khảo': question.citation,
                        'Ghi chú': question.note
                    }
                    for question in questions_list
                ]
                df = pd.DataFrame(data_for_df)
                df.to_excel(writer, sheet_name=round_code, index=False)
        excel_file_buffer.seek(0)
        # Return the file using StreamingResponse
        # Content-Disposition header tells the browser to download the file and suggests a filename.
        return StreamingResponse(
            excel_file_buffer,
            media_type=XLSX_MIME_TYPE,
            headers={
                "Content-Disposition": f"attachment; filename={response_file_name}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )