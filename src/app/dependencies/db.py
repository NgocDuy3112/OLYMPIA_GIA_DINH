# async SQLAlchemy engine + AsyncSession factory
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from valkey.asyncio import Valkey
from app.config import settings


engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session



async def get_valkey_cache() -> Valkey:
    return Valkey.from_url(settings.VALKEY_ANSWERS_CACHE_URL)