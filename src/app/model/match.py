import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Boolean, ForeignKey, CheckConstraint, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.db import Base
from app.model import *


def utcnow():
    return datetime.now(timezone.utc)



class Match(Base):
    __tablename__ = "matches"
    # Constraints
    __table_args__ = (
        CheckConstraint("match_code LIKE 'M%'", name='check_match_code_starts_with_M'),
    )

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    match_code: Mapped[str] = mapped_column(String(length=5), unique=True, index=True)
    match_name: Mapped[str] = mapped_column(String(length=100), unique=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    questions: Mapped[list["Question"]] = relationship(back_populates="match") # type: ignore
    records: Mapped[list["Record"]] = relationship(back_populates='match') # type: ignore