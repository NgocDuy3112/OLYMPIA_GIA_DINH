from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property

from app.db.dependencies import Base
from app.model.record import Record


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
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    player_code: Mapped[str] = mapped_column(String(length=5), unique=True)
    player_name: Mapped[str] = mapped_column(String(length=25))
    # Foreign Keys
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)
    # Relationships
    team: Mapped["Team"] = relationship(back_populates="players") # type: ignore