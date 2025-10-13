from app.schema.base import BaseRequest, BaseResponse



class PostPlayerRequest(BaseRequest):
    team_code: str
    player_code: str
    player_name: str



class PostPlayerResponse(BaseResponse):
    pass



class GetPlayerResponse(BaseResponse):
    pass