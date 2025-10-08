from base import BaseRequest, BaseResponse



class PostRecordRequest(BaseRequest):
    match_code: str
    player_code: str
    d_score_earned: int



class PostRecordResponse(BaseResponse):
    pass



class GetRecordsByMatchRequest(BaseRequest):
    match_code: str



class GetRecordsByPlayerRequest(BaseRequest):
    player_code: str



class GetRecordsResponse(BaseResponse):
    pass