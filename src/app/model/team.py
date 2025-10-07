from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.dependencies import Base


def utcnow():
    return datetime.now(timezone.utc)



class Team(Base):
    """
    SQLAlchemy model representing a team.
    Inherits from the common declarative Base.
    """
    __tablename__ = "teams"
    # Columns
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    team_code: Mapped[str] = mapped_column(String(length=5), unique=True)
    team_name: Mapped[str] = mapped_column(String(length=25))

    # Relationships
    players: Mapped[list["Player"]] = relationship(back_populates="team", cascade="all, delete-orphan") # type: ignore