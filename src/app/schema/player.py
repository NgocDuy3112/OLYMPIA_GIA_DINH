from base import BaseRequest, BaseResponse



class GetPlayerInformationRequest(BaseRequest):
    code: str



class GetPlayerInformationResponse(BaseResponse):
    name: str
    team: str
    total_d_scores: int