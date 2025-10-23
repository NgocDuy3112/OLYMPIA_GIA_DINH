import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, UUID, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.db import Base


def utcnow():
    return datetime.now(timezone.utc)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    question_code: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    correct_answers: Mapped[str] = mapped_column(String)
    extra_info: Mapped[dict] = mapped_column(JSONB, nullable=True)  # JSONB column
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Keys
    match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('matches.id'), nullable=False)

    # Relationships
    match: Mapped["Match"] = relationship(back_populates='questions') # type: ignore
    answers: Mapped[list["Answer"]] = relationship(back_populates='question') # type: ignore
    records: Mapped[list["Record"]] = relationship(back_populates='question') # type: ignore
