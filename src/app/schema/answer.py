from base import BaseRequest, BaseResponse



class PostAnswerRequest(BaseRequest):
    player_code: str
    content: str
    timestamp: float



class PostAnswerResponse(BaseResponse):
    pass



class GetAnswerRequest(BaseRequest):
    player_code: str



class GetAnswerResponse(BaseResponse):
    player_code: str
    content: str
    timestamp: float