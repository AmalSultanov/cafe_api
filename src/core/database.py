from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_settings
from src.core.logging import logger

settings = get_settings()

logger.info(
    f"Initializing database connection to: "
    f"{settings.postgres_host}:{settings.postgres_port}"
)
async_engine = create_async_engine(url=settings.postgres_url, echo=True)
async_session = async_sessionmaker(
    bind=async_engine, autoflush=False,
    autocommit=False, expire_on_commit=False
)
logger.info("Database engine and session factory were created")


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []

        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("Creating new database session")
    async with async_session() as session:
        try:
            yield session
        finally:
            logger.debug("Database session was closed")
