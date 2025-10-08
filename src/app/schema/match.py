from pydantic import model_validator
from typing import Any
from uuid import UUID

from base import BaseRequest, BaseResponse



class PostMatchRequest(BaseRequest):
    match_code: str
    match_name: str

    @model_validator(mode='before')
    @classmethod
    def check_exactly_two_identifiers(cls, data: Any) -> Any:
        """Ensures that exactly one of player_id or player_code is provided."""
        code_provided = data.get('match_code') is not None
        name_provided = data.get('match_name') is not None
        if not (code_provided and name_provided):
            raise ValueError("Must provide both identifiers: 'code_provided' and 'name_provided'.")
        return data



class PostMatchResponse(BaseResponse):
    pass



class GetMatchRequest(BaseRequest):
    match_id: UUID
    match_code: str

    @model_validator(mode='before')
    @classmethod
    def check_exactly_one_identifier(cls, data: Any) -> Any:
        """Ensures that exactly one of player_id or player_code is provided."""
        # Note: data here is typically a dict from the request body/query params
        
        id_provided = data.get('match_id') is not None
        code_provided = data.get('match_code') is not None
        
        if id_provided and code_provided:
            raise ValueError("Must provide only one identifier: 'player_id' or 'player_code'.")
        
        if not id_provided and not code_provided:
            raise ValueError("Must provide at least one identifier: 'player_id' or 'player_code'.")
        return data



class GetMatchResponse(BaseResponse):
    pass