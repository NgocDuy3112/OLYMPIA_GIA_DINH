from app.schema.base import BaseRequest



class StartQuestionRequest(BaseRequest):
    match_code: str
    question_code: str
    time_limit: int