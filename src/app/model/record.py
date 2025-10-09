import uuid
from datetime import datetime, timezone

from sqlalchemy import Integer, DateTime, ForeignKey, CheckConstraint, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.dependencies import Base


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
    d_score_earned: Mapped[int] = mapped_column(Integer())

    # Foreign Keys
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("players.id"), nullable=False)
    match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("matches.id"), nullable=False)

    # Relationships
    player: Mapped["Player"] = relationship(back_populates='records') # type: ignore
    matches: Mapped[list["Match"]] = relationship(back_populates='records') # type: ignore