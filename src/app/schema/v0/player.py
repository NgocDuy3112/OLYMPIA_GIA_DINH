from pydantic import BaseModel, Field


class PlayerSchemaIn(BaseModel):
    team_code: str = Field(unique=True)
    player_code: str = Field(unique=True)
    player_name: str = Field(min_length=1)
    birth_year: int = Field(default=2000)
    is_dnf: bool = Field(default=False)


class PlayerSchemaOut(BaseModel):
    team_name: str = Field(min_length=1)
    player_name: str = Field(min_length=1)
    birth_year: int = Field(default=2000)
    is_dnf: bool = Field(default=False)