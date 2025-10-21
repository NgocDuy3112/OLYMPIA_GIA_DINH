from app.schema.base import BaseRequest, BaseResponse



class PostQuestionRequest(BaseRequest):
    match_code: str
    question_code: str
    content: str
    correct_answers: str
    extra_info: dict | None = None  # media_sources, explaination, citation, note


class PostQuestionResponse(BaseResponse):
    pass


class PutQuestionRequest(BaseRequest):
    match_code: str
    question_code: str
    content: str
    correct_answers: str
    extra_info:  dict | None = None


class PutQuestionResponse(BaseResponse):
    pass


class DeleteQuestionResponse(BaseResponse):
    pass


class GetQuestionResponse(BaseResponse):
    pass
