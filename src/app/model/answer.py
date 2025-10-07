from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.dependencies import Base


def utcnow():
    return datetime.now(timezone.utc)



class Answer(Base):
    __tablename__ = "answers"
    # Columns
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    content: Mapped[str] = mapped_column(String, nullable=True)
    # Foreign Keys
    player_id: Mapped[UUID] = mapped_column(ForeignKey("players.id"), nullable=False)
    match_id: Mapped[UUID] = mapped_column(ForeignKey("matches.id"), nullable=False)