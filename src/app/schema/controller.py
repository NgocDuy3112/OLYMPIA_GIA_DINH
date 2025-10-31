from app.schema.base import BaseRequest, BaseResponse



class StartQuestionRequest(BaseRequest):
    match_code: str
    question_code: str
    time_limit: int



class StartQuestionResponse(BaseResponse):
    pass



class PickQuestionRequest(BaseRequest):
    match_code: str
    player_code: str
    question_code: str



class PickQuestionResponse(BaseResponse):
    pass