from typing import Union
from sqlalchemy import select

from .models import User
from .db_helper import db_helper


class AsyncOrm:

    @staticmethod
    async def create_user(tg_id: int, username: Union[str | None], **kwargs) -> None:
        async with db_helper.session_factory() as session:
            user = User(
                tg_id=tg_id,
                username=username,
                **kwargs,
            )
            session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def get_user(tg_id: int) -> User:
        async with db_helper.session_factory() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id),
            )

            if not user:
                return None
            return user

    @staticmethod
    async def get_users_by_subscription() -> list:
        async with db_helper.session_factory() as session:
            query = (
                select(User)
                .where(User.subscription)
                .order_by(
                    User.subscribe_date,
                )
            )
            result = await session.execute(query)
            users_with_subscription = result.scalars().all()
            return users_with_subscription

    @staticmethod
    async def update_user(tg_id: int, **kwargs):
        async with db_helper.session_factory() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id),
            )
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def delete_user(tg_id: int):
        async with db_helper.session_factory() as session:
            user = await session.get(User, tg_id)
            session.delete(user)
            await session.commit()
