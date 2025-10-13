from app.schema.base import BaseRequest, BaseResponse



class PostQuestionRequest(BaseRequest):
    match_code: str
    question_code: str
    content: str
    media_sources: str | None = None
    correct_answers: str
    explaination: str | None = None
    citation: str | None = None
    note: str | None = None



class PostQuestionResponse(BaseResponse):
    pass



class GetQuestionResponse(BaseResponse):
    pass