from app.core.models import User
from app.core.db_helper import db_helper

from sqlalchemy import select


class AsyncOrm():

    @staticmethod
    async def create_user(tg_id: int, username: str) -> None:
        async with db_helper.session_factory() as session:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

    @staticmethod
    async def get_user(tg_id: int, username: str | None) -> User:
        async with db_helper.session_factory() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id)
                )

            if not user:
                session.add(User(tg_id=tg_id, username=username))
                await session.commit()
            return user
            print(type(user))

    @staticmethod
    async def update_user(tg_id: int, **kwargs):
        async with db_helper.session_factory() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id)
                )
            for key, value in kwargs.items():
                setattr(user, key, value)
            await session.add(user)
            await session.commit()

    @staticmethod
    async def delete_user(tg_id: int):
        async with db_helper.session_factory() as session:
            user = await session.get(User, tg_id)
            session.delete(user)
            await session.commit()
