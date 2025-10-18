from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

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
COLUMN_NAMES = ['Code', 'Câu hỏi', 'Media', 'Đáp án', 'Giải thích', 'Nguồn tham khảo', 'Ghi chú']
XLSX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def convert_sheet_name_to_round_code(sheet_name: str) -> str:
    parts = sheet_name.split("_")
    return "".join([part[0] for part in parts])



async def post_question_to_db(request: PostQuestionRequest, session: AsyncSession) -> PostQuestionResponse:
    global_logger.info(f"POST request received to create question with code: {request.question_code} for match: {request.match_code}.")
    try:
        # 1. Validate Match existence
        match_id = await _get_id_by_code(session, Match, 'match_code', request.match_code, 'Match')
        global_logger.debug(f"Match found. match_code: {request.match_code}, match_id: {match_id}")
        
        # 2. Create the new Question object
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
        global_logger.debug(f"Question object created and added to session. question_code={request.question_code}")
        
        # 3. Commit and Handle Errors
        await session.commit()
        await session.refresh(new_question)
        global_logger.info(f"Question created successfully. question_id={new_question.id}, match_id={match_id}")
        
        return PostQuestionResponse(
            response={
                'message': 'Add a new question successfully!'
            }
        )
    except HTTPException:
        raise
    except IntegrityError:
        await session.rollback()
        global_logger.warning(f"Failed to create question due to unique constraint violation. question_code={request.question_code}. Returning 409.")
        raise HTTPException(
            status_code=409,
            detail=f'A question with question_code={request.question_code} already exists.'
        )
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during question creation/commit for code={request.question_code}, match_code={request.match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during question creation.'
        )



async def post_questions_file_to_db(file: UploadFile, session: AsyncSession) -> PostQuestionResponse:
    original_filename = file.filename
    global_logger.info(f"POST request received to upload questions file: {original_filename}.")
    
    try:
        # 1. Validate File Name Format
        pattern = r'^OGD3_M\d{2}\.xls(x)?$'
        if not re.match(pattern, original_filename):
            global_logger.warning(f"Invalid file name format: {original_filename}. Returning 400.")
            raise HTTPException(
                status_code=400,
                detail='The Excel file name is not in the correct format: OGD3_Mxx.xls(x)'
            )
            
        # 2. Get Match ID
        match_code = original_filename.split(".")[0].split("_")[1]
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')
        global_logger.debug(f"File match code: {match_code}, Match ID: {match_id}")

        # 3. Process File Content
        content = await file.read()
        content_io = io.BytesIO(content)
        questions_list: list[Question] = []
        
        for sheet_name in SHEET_NAMES:
            content_io.seek(0)
            df = pd.read_excel(content_io, sheet_name)
            rows_as_dicts = df.to_dict('records')
            global_logger.debug(f"Processing sheet '{sheet_name}' with {len(rows_as_dicts)} rows.")
            
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
                
        # 4. Bulk Insert and Commit
        session.add_all(questions_list)
        await session.commit()
        global_logger.info(f'Successfully uploaded {len(questions_list)} questions from file {original_filename}.')
        return PostQuestionResponse(
            response={
                'message': f'Upload questions from file {original_filename} successfully'
            }
        )
    except HTTPException:
        raise
    except IntegrityError:
        await session.rollback()
        global_logger.warning(f"Failed to bulk upload questions due to unique constraint violation in file {original_filename}. Returning 409.")
        raise HTTPException(
            status_code=409,
            detail=f'One or more questions in the file already exist (unique code conflict).'
        )
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error occurred during bulk upload of file {original_filename}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during file upload.'
        )



async def get_all_questions_from_match_code_from_db(match_code: str, session: AsyncSession) -> GetQuestionResponse:
    global_logger.info(f"GET request received to get questions for match: {match_code}.")
    try:
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')
        global_logger.debug(f"Match ID: {match_id} for match_code: {match_code}")
        questions_query = select(Question).where(Question.match_id == match_id)
        execution = await session.execute(questions_query)
        result = execution.scalars().all()
        if not result:
            global_logger.warning(f"No questions found for match with match_code={match_code} in the database. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'No questions found for match with match_code={match_code} in the database'
            )
        return GetQuestionResponse(
            response={
                'data': {
                    'match_code': match_code,
                    'questions': [
                        {
                            'question_code': question.question_code,
                            'content': question.content,
                            'media_sources': question.media_sources,
                            'correct_answers': question.correct_answers,
                            'explaination': question.explaination,
                            'citation': question.citation,
                            'note': question.note
                        }
                    for question in result]
                }
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred during the fetching questions.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during file upload.'
        )



async def get_all_questions_from_match_code_to_excel_file_from_db(match_code: str, session: AsyncSession) -> StreamingResponse:
    global_logger.info(f"GET request received to download questions file for match: {match_code}.")
    try:
        # 1. Validate Match existence
        match_id = await _get_id_by_code(session, Match, 'match_code', match_code, 'Match')
        global_logger.debug(f"Match ID: {match_id} for match_code: {match_code}")
        response_file_name = f'OGD3_{match_code}.xlsx'
        excel_file_buffer = io.BytesIO()
        round_codes = [convert_sheet_name_to_round_code(sheet_name) for sheet_name in SHEET_NAMES]
        questions_by_round: dict[str, list] = {}
        total_questions = 0

        # 2. Fetch Questions by Round
        for sheet_name, round_code in zip(SHEET_NAMES, round_codes): # Use zip for better association
            # The query should check match_id AND the round code prefix
            questions_query = select(Question).where(
                Question.match_id == match_id,
                Question.question_code.like(f'{round_code}%')
            )
            execution = await session.execute(questions_query)
            questions = execution.unique().scalars().all()
            
            questions_by_round[sheet_name] = questions
            total_questions += len(questions)
            global_logger.debug(f"Fetched {len(questions)} questions for sheet '{sheet_name}'.")

        if total_questions == 0:
            global_logger.warning(f"No questions found for match_code={match_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f"No questions found from match_code={match_code}"
            )

        # 3. Write to Excel
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
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
        excel_file_buffer.seek(0)
        
        global_logger.info(f"Successfully generated and sending file {response_file_name} with {total_questions} questions.")
        
        # 4. Return the file using StreamingResponse
        return StreamingResponse(
            excel_file_buffer,
            media_type=XLSX_MIME_TYPE,
            headers={
                "Content-Disposition": f"attachment; filename={response_file_name}"
            }
        )
    except HTTPException:
        raise
    except Exception:
        global_logger.exception(f'Unexpected error occurred while generating Excel file for match_code={match_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during file generation.'
        )