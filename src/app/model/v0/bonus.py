from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


class BonusModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    player_id: str = Field(foreign_key="player.id")
    point_score: int = Field(default=0, ge=0, multiple_of=5)
    g_score: int = Field(default=0, ge=0)
    d_score: int = Field(default=0, ge=0)