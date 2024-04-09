from typing import Union

from sqlalchemy import select
from sqlalchemy.engine import Result

from .models import User, Referral, Key, Payment
from .db_helper import db_helper

""" Необходимо оптимизирвоать каждый запрос к БД
    Также добавить отдельные методы для создания ключей и рефералов
"""


class AsyncOrm:

    @staticmethod
    async def create_user(
        tg_id: int,
        username: Union[str | None],
        **kwargs,
    ) -> None:
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
            stmt = select(User).where(User.tg_id == tg_id)

            result: Result = await session.execute(stmt)

            user: User | None = result.scalar_one_or_none()
            return user

    @staticmethod
    async def get_users() -> list[User]:
        async with db_helper.session_factory() as session:
            stmt = select(User).order_by(User.id)

            result: Result = await session.execute(stmt)

            users: User = result.scalars()
            return users

    @staticmethod
    async def get_inactive_users() -> list[User]:
        async with db_helper.session_factory() as session:
            stmt = (
                select(User)
                .where(User.subscription == False)
                .where(User.key == None)
                .order_by(
                    User.tg_id,
                )
            )
            result: Result = await session.execute(stmt)
            users = result.scalars()
            return users

    @staticmethod
    async def get_users_by_subscription() -> list[User]:
        async with db_helper.session_factory() as session:
            stmt = (
                select(User)
                .where(User.subscription)
                .order_by(
                    User.subscribe_date,
                )
            )
            result: Result = await session.execute(stmt)
            users_with_subscription = result.scalars()
            return users_with_subscription

    @staticmethod
    async def update_user(
        tg_id: int,
        referral: User = None,
        payment_id: int = None,
        **kwargs,
    ):
        async with db_helper.session_factory() as session:
            stmt = select(User).where(User.tg_id == tg_id)

            result: Result = await session.execute(stmt)

            user: User | None = result.scalar_one_or_none()

            for key, value in kwargs.items():
                setattr(user, key, value)
            if referral:
                ref = Referral(
                    tg_id=referral.tg_id,
                    user_id=user.id,
                )
                user.referrals.append(ref)

            if payment_id:
                payment = Payment(
                    payment_id=payment_id,
                    user_id=user.id,
                )
                user.payments.append(payment)

            session.add(user)
            await session.commit()

    @staticmethod
    async def get_active_referrals(tg_id: int) -> list[int]:
        async with db_helper.session_factory() as session:
            stmt = select(User).where(User.tg_id == tg_id)

            result: Result = await session.execute(stmt)
            user = result.scalar()

            referrals = []
            for ref in user.referrals:
                if ref.user.subscription:
                    referrals.append(ref.tg_id)
            return referrals

    @staticmethod
    async def get_users_keys() -> list[Key]:
        async with db_helper.session_factory() as session:
            stmt = select(Key)

            result: Result = await session.execute(stmt)
            keys = result.scalars()

            return keys

    @staticmethod
    async def get_referrer(tg_id: int) -> User | None:
        async with db_helper.session_factory() as session:
            stmt = select(Referral).where(Referral.tg_id == tg_id)

            result: Result = await session.execute(stmt)
            referral = result.scalar()
            if referral:
                referrer_user = referral.user
                return referrer_user
            return None

    @staticmethod
    async def delete_user(tg_id: int):
        async with db_helper.session_factory() as session:
            stmt = select(User).where(User.tg_id == tg_id)

            result: Result = await session.execute(stmt)
            user = result.scalar()
            await session.delete(user)
            await session.commit()
