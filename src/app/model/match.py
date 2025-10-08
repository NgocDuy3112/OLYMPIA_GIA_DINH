from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.dependencies import Base


def utcnow():
    return datetime.now(timezone.utc)



class Match(Base):
    __tablename__ = "matches"
    # Constraints
    __table_args__ = (
        CheckConstraint("match_code LIKE 'M%'", name='check_match_code_starts_with_M'),
    )

    # Columns
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    match_code: Mapped[str] = mapped_column(String(length=3), unique=True)
    match_name: Mapped[str] = mapped_column(String(length=100), unique=True)

    # Relationships
    players: Mapped[list[Player]] = relationship(back_populates="matches") # type: ignore