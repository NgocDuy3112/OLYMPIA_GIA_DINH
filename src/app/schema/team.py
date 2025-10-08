from pydantic import model_validator
from typing import Any
from uuid import UUID

from base import BaseRequest, BaseResponse



class GetTeamRequest(BaseRequest):
    team_id: UUID
    team_code: str

    @model_validator(mode='before')
    @classmethod
    def check_exactly_one_identifier(cls, data: Any) -> Any:
        """Ensures that exactly one of team_id or team_code is provided."""
        # Note: data here is typically a dict from the request body/query params
        
        id_provided = data.get('team_id') is not None
        code_provided = data.get('team_code') is not None
        
        if id_provided and code_provided:
            raise ValueError("Must provide only one identifier: 'team_id' or 'team_code'.")
        
        if not id_provided and not code_provided:
            raise ValueError("Must provide at least one identifier: 'team_id' or 'team_code'.")
        return data




class GetTeamResponse(BaseResponse):
    pass