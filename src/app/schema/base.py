from typing import Literal, Any
from pydantic import BaseModel
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)



class BaseRequest(BaseModel):
    pass



class BaseResponse(BaseModel):
    response: dict[str, Any] | None = None