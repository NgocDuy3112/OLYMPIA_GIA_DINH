from app.schema.base import BaseRequest, BaseResponse



class PostAnswerRequest(BaseRequest):
    player_code: str
    match_code: str
    question_code: str
    content: str
    timestamp: float



class PostAnswerResponse(BaseResponse):
    pass



class GetAnswerResponse(BaseResponse):
    pass