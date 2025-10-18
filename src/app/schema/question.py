from app.schema.base import BaseRequest, BaseResponse



class PostQuestionRequest(BaseRequest):
    match_code: str
    question_code: str
    content: str
    correct_answers: str
    media_sources: str | None = None
    explaination: str | None = None
    citation: str | None = None
    note: str | None = None



class PostQuestionResponse(BaseResponse):
    pass



class PutQuestionRequest(BaseRequest):
    match_code: str
    question_code: str
    content: str
    correct_answers: str
    media_sources: str | None = None
    explaination: str | None = None
    citation: str | None = None
    note: str | None = None



class PutQuestionResponse(BaseResponse):
    pass



class DeleteQuestionResponse(BaseResponse):
    pass



class GetQuestionResponse(BaseResponse):
    pass