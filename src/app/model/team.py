import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Boolean, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.db import Base
from app.model import *


def utcnow():
    return datetime.now(timezone.utc)



class Team(Base):
    """
    SQLAlchemy model representing a team.
    Inherits from the common declarative Base.
    """
    __tablename__ = "teams"
    # Columns
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    team_code: Mapped[str] = mapped_column(String(length=20), unique=True, index=True)
    team_name: Mapped[str] = mapped_column(String(length=25))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    players: Mapped[list["Player"]] = relationship(back_populates="team", cascade="all, delete-orphan") # type: ignore