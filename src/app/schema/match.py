from pydantic import model_validator
from typing import Any

from app.schema.base import BaseRequest, BaseResponse



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
            raise ValueError("Must provide both identifiers: 'match_code' and 'match_name'.")
        return data



class PostMatchResponse(BaseResponse):
    pass



class DeleteMatchResponse(BaseResponse):
    pass



class GetMatchResponse(BaseResponse):
    pass