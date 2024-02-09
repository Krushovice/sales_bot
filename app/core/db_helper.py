from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from app.config import settings
from .base import Base


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.ECHO,
)


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
