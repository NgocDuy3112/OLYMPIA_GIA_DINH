from app.schema.base import BaseRequest, BaseResponse



class PostTeamRequest(BaseRequest):
    team_code: str
    team_name: str



class PostTeamResponse(BaseResponse):
    pass



class GetTeamResponse(BaseResponse):
    pass



class DeleteTeamResponse(BaseResponse):
    pass