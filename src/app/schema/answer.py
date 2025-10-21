from app.schema.base import BaseRequest, BaseResponse



class PostAnswerRequest(BaseRequest):
    player_code: str
    match_code: str
    question_code: str
    timestamp: float
    content: str | None = None
    is_buzzed: bool | None = None



class PostAnswerResponse(BaseResponse):
    pass



class PutAnswerRequest(BaseRequest):
    player_code: str
    match_code: str
    question_code: str
    timestamp: float
    content: str
    is_buzzed: bool



class PutAnswerResponse(BaseResponse):
    pass



class GetAnswerResponse(BaseResponse):
    pass