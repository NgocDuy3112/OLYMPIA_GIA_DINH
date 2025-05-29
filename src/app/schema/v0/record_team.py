from pydantic import BaseModel, Field
from datetime import datetime


class RecordTeamSchemaIn(BaseModel):
    match_code: str = Field(unique=True)
    match_name: str = Field(min_length=1)
    team_code: str = Field(unique=True)
    point_score: int = Field(multiple_of=5)


class RecordTeamSchemaOut(BaseModel):
    updated_at: datetime
    match_name: str = Field(min_length=1)
    team_name: str = Field(min_length=1)
    point_score: int = Field(multiple_of=5)