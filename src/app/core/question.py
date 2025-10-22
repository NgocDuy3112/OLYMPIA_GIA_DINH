from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import io
import re
import pandas as pd

from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.model.match import Match
from app.model.question import Question
from app.schema.question import *
from app.logger import global_logger
from app.utils.get_id_by_code import _get_id_by_code


SHEET_NAMES = ['LAM_NONG', 'VUOT_DEO', 'BUT_PHA', 'NUOC_RUT']
XLSX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"



def convert_sheet_name_to_round_code(sheet_name: str) -> str:
    parts = sheet_name.split("_")
    return "".join([part[0] for part in parts])



async def post_question_to_db(request: PostQuestionRequest, session: AsyncSession) -> PostQuestionResponse:
    global_logger.info(f"POST question {request.question_code} for match {request.match_code}")
    try:
        match_id = await _get_id_by_code(session, Match, 'match_code', request.match_code, 'Match')
        new_question = Question(
            match_id=match_id,
            question_code=request.question_code,
            content=request.content,
            correct_answers=request.correct_answers,
            extra_info=request.extra_info or {}
        )
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        return PostQuestionResponse(response={'message': 'Question added successfully'})
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, f'Question with code {request.question_code} already exists.')
    except Exception as e:
        await session.rollback()
        global_logger.exception("Error posting question")
        raise HTTPException(500, f'Unexpected error: {e}')



async def post_questions_file_to_db(file: UploadFile, session: AsyncSession) -> PostQuestionResponse:
    filename = file.filename
    global_logger.info(f"Uploading file: {filename}")
    try:
        pattern = r'^OGD3_M[\w-]+\.xls(x)?$'
        if not re.match(pattern, filename):
            raise HTTPException(400, 'Invalid file name format: OGD3_Mxx.xls(x)')
        match_code = filename.split(".")[0].split("_")[1]
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')
        content = await file.read()
        io_buf = io.BytesIO(content)
        questions = []
        for sheet in SHEET_NAMES:
            io_buf.seek(0)
            df = pd.read_excel(io_buf, sheet)
            for row in df.to_dict('records'):
                extra_info = {}
                for k, col_name in {
                    "media_sources": "Media",
                    "explaination": "Giải thích",
                    "citation": "Nguồn tham khảo",
                    "note": "Ghi chú"
                }.items():
                    val = row.get(col_name)
                    if pd.notna(val): extra_info[k] = val
                questions.append(Question(
                    match_id=match_id,
                    question_code=str(row['Code']),
                    content=str(row['Câu hỏi']),
                    correct_answers=str(row['Đáp án']),
                    extra_info=extra_info
                ))

        session.add_all(questions)
        await session.commit()
        return PostQuestionResponse(response={'message': f'Uploaded {len(questions)} questions for match_code={match_code} successfully'})
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, 'Duplicate question codes found in file')
    except Exception as e:
        await session.rollback()
        global_logger.exception("Error uploading questions file")
        raise HTTPException(500, f'Unexpected error: {e}')



async def get_all_questions_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetQuestionResponse:
    try:
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')
        result = await session.execute(select(Question).where(Question.match_id == match_id))
        questions = result.scalars().all()
        if not questions:
            raise HTTPException(404, f'No questions found for match {match_code}')
        return GetQuestionResponse(response={
            'data': {
                'match_code': match_code,
                'questions': [
                    {
                        'question_code': q.question_code,
                        'content': q.content,
                        'correct_answers': q.correct_answers,
                        **(q.extra_info or {})
                    }
                    for q in questions
                ]
            }
        })
    except HTTPException:
        raise
    except Exception as e:
        global_logger.exception("Error fetching questions")
        raise HTTPException(500, f'Unexpected error: {e}')



async def get_all_questions_from_match_code_to_excel_file_from_db(match_code: str, session: AsyncSession) -> StreamingResponse:
    try:
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')
        buffer = io.BytesIO()
        response_name = f'OGD3_{match_code}_exported.xlsx'
        total = 0

        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for sheet in SHEET_NAMES:
                code_prefix = convert_sheet_name_to_round_code(sheet)
                result = await session.execute(
                    select(Question).where(
                        Question.match_id == match_id,
                        Question.question_code.like(f'{code_prefix}%')
                    )
                )
                questions = result.scalars().all()
                total += len(questions)

                data = []
                for q in questions:
                    info = q.extra_info or {}
                    data.append({
                        'Code': q.question_code,
                        'Câu hỏi': q.content,
                        'Đáp án': q.correct_answers,
                        'Media': info.get('media_sources') if info.get('media_sources') else '',
                        'Giải thích': info.get('explaination') if info.get('explaination') else '',
                        'Nguồn tham khảo': info.get('citation') if info.get('citation') else '',
                        'Ghi chú': info.get('note') if info.get('note') else ''
                    })
                pd.DataFrame(data).to_excel(writer, sheet_name=sheet, index=False)

        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type=XLSX_MIME_TYPE,
            headers={"Content-Disposition": f"attachment; filename={response_name}"}
        )
    except Exception as e:
        global_logger.exception("Error exporting questions")
        raise HTTPException(500, f'Unexpected error: {e}')



async def delete_all_questions_from_match_code_in_db(match_code: str, session: AsyncSession) -> DeleteQuestionResponse:
    match_id_sub = select(Match.id).where(Match.match_code == match_code).scalar_subquery()
    exists = await session.execute(select(Question.id).where(Question.match_id == match_id_sub).limit(1))
    if not exists.scalar_one_or_none():
        raise HTTPException(404, f'No questions found for match {match_code}')
    try:
        q = update(Question).where(Question.match_id == match_id_sub).values(is_deleted=True)
        res = await session.execute(q)
        await session.commit()
        return DeleteQuestionResponse(response={'message': f'Soft-deleted {res.rowcount} questions'})
    except Exception as e:
        await session.rollback()
        global_logger.exception("Error deleting questions")
        raise HTTPException(500, f'Unexpected error: {e}')
