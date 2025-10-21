import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy import String, Enum, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.db import Base
from app.model import *



class RoleEnum(str, enum.Enum):
    guest = "guest"
    client = "client"
    admin = "admin"



class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.guest)