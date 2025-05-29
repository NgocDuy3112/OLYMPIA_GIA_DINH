from pydantic import BaseModel, Field
from app.schema.v0.player import PlayerSchemaOut


class TeamSchemaIn(BaseModel):
    team_code: str = Field(unique=True)
    team_name: str = Field(min_length=1)


class TeamSchemaOut(BaseModel):
    team_name: str = Field(min_length=1)