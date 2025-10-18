import uuid
from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, CheckConstraint, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.db import Base
from app.model import *


def utcnow():
    return datetime.now(timezone.utc)



class Record(Base):
    """
    SQLAlchemy model representing a record.
    Inherits from the common declarative Base.
    """
    __tablename__ = "records"
    # Constraints
    __table_args__ = (
        CheckConstraint('d_score_earned >= 0', name='check_d_score_earned_non_negative'),
        CheckConstraint('d_score_earned % 5 = 0', name='check_d_score_earned_multiple_of_5'),
    )
    # Columns
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    d_score_earned: Mapped[int] = mapped_column(Integer)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    round_code: Mapped[str] = mapped_column(String)

    # Foreign Keys
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("players.id"), nullable=False)
    match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("matches.id"), nullable=False)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id"), nullable=False)

    # Relationships
    player: Mapped["Player"] = relationship(back_populates='records') # type: ignore
    match: Mapped["Match"] = relationship(back_populates='records') # type: ignore
    question: Mapped["Question"] = relationship(back_populates='records') # type: ignore