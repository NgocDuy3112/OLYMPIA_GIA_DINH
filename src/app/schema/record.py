from app.schema.base import BaseRequest, BaseResponse



class PostRecordRequest(BaseRequest):
    match_code: str
    player_code: str
    question_code: str
    d_score_earned: int



class PostRecordResponse(BaseResponse):
    pass



class GetRecordsResponse(BaseResponse):
    pass