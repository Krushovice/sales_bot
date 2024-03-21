from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    async_scoped_session,
)
from asyncio import current_task

from app.api_v1.config import settings

from .models import Base


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

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.ECHO,
)


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
