from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


class PlayerModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    team_id: str = Field(foreign_key="team.id")
    player_code: str = Field(unique=True)
    player_name: str = Field(min_length=1)
    birth_year: int = Field(default=2000)
    is_dnf: bool = Field(default=False)