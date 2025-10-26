from valkey.asyncio import Valkey
from fastapi import HTTPException


from app.schema.controller import StartQuestionRequest
from app.utils.auto_time import trigger_start_time
from app.logger import global_logger



async def trigger_start_question(
    request: StartQuestionRequest,
    pubsub: Valkey
):
    """
    Endpoint HTTP này dành cho Admin/Host để kích hoạt câu hỏi mới.
    """
    try:
        # Gọi hàm logic mà bạn đã viết
        result = await trigger_start_time(
            pubsub=pubsub,
            match_code=request.match_code,
            question_code=request.question_code,
            time_limit=request.time_limit
        )
        return result
    except Exception as e:
        global_logger.error(f"[API_START] There's an error when triggering the question {request.question_code} for match {request.match_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")