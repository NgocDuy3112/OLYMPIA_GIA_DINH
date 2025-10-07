from typing import Literal
from pydantic import BaseModel
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)



class BaseRequest(BaseModel):
    request_at: datetime = utcnow()



class BaseResponse(BaseModel):
    response_at: datetime = utcnow()
    status: Literal['success', 'error']
    detail: str | None = None # For error