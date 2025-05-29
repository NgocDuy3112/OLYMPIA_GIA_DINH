from pydantic import BaseModel, Field
from datetime import datetime


class BonusSchemaIn(BaseModel):
    player_code: str = Field(unique=True)
    point_score: int = Field(ge=0, multiple_of=5)
    g_score: int = Field(ge=0)
    d_score: int = Field(ge=0)


class BonusSchemaOut(BaseModel):
    updated_at: datetime
    player_name: str = Field(min_length=1)
    point_score: int = Field(ge=0, multiple_of=5)
    g_score: int = Field(ge=0)
    d_score: int = Field(ge=0)