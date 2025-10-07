from base import BaseRequest, BaseResponse



class PostRecordRequest(BaseRequest):
    player_code: str
    d_score_earned: int



class PostRecordResponse(BaseResponse):
    pass



class GetRecordRequest(BaseRequest):
    player_code: str



class GetRecordResopnse(BaseResponse):
    player_code: str
    d_score_earned: int