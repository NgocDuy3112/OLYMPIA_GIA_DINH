import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, UUID
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
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    team_code: Mapped[str] = mapped_column(String(length=5), unique=True)
    team_name: Mapped[str] = mapped_column(String(length=25))

    # Relationships
    players: Mapped[list["Player"]] = relationship(back_populates="teams", cascade="all, delete-orphan") # type: ignore