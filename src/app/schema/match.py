from base import BaseRequest, BaseResponse



class PostMatchInformationRequest(BaseRequest):
    code: str
    name: str



class PostMatchInformationResponse(BaseResponse):
    name: str



class GetMatchInformationRequest(BaseRequest):
    code: str



class GetMatchInformationResponse(BaseResponse):
    name: str
    players: str