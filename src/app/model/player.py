import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Boolean, ForeignKey, CheckConstraint, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.db import Base
from app.model import *


def utcnow():
    return datetime.now(timezone.utc)




class Player(Base):
    """
    SQLAlchemy model representing a player.
    Inherits from the common declarative Base.
    """
    __tablename__ = "players"
    # Constraints
    __table_args__ = (
        CheckConstraint("player_code LIKE 'P%'", name='check_player_code_starts_with_P'),
    )
    # Columns
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    player_code: Mapped[str] = mapped_column(String(length=20), unique=True, index=True)
    player_name: Mapped[str] = mapped_column(String(length=25))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Keys
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="players") # type: ignore
    records: Mapped[list["Record"]] = relationship(back_populates="player") # type: ignore
    answers: Mapped[list["Answer"]] = relationship(back_populates='player') # type: ignore