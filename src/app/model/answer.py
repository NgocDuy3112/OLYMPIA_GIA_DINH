import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, REAL, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.dependencies import Base


def utcnow():
    return datetime.now(timezone.utc)



class Answer(Base):
    __tablename__ = "answers"
    # Columns
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    content: Mapped[str] = mapped_column(String, nullable=True)
    timestamp: Mapped[float] = mapped_column(REAL)
    # Foreign Keys
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("players.id"), nullable=False)
    match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("matches.id"), nullable=False)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id"), nullable=False)
    # Relationships
    player: Mapped["Player"] = relationship(back_populates='players') # type: ignore
    question: Mapped["Question"] = relationship(back_populates='questions') # type: ignore