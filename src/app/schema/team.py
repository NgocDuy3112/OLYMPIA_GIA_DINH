from base import BaseRequest, BaseResponse



class GetTeamInformationRequest(BaseRequest):
    code: str



class GetTeamInformationResponse(BaseResponse):
    name: str
    players: list[str]
    total_g_scores: int