from pydantic import BaseModel, Field
from datetime import datetime


class RecordPlayerSchemaIn(BaseModel):
    match_code: str = Field(unique=True)
    match_name: str = Field(min_length=1)
    player_code: str = Field(unique=True)
    point_score: int = Field(multiple_of=5)


class RecordPlayerSchemaOut(BaseModel):
    updated_at: datetime
    match_name: str = Field(min_length=1)
    player_name: str = Field(min_length=1)
    point_score: int = Field(multiple_of=5)