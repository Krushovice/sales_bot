from app.core.models import User, Referral
from app.core.db_helper import db_helper

from sqlalchemy import select, update, delete


class AsyncOrm():

    @staticmethod
    async def create_user(tg_id, username):
        async with db_helper.session_factory() as session:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

    @staticmethod
    async def get_user(tg_id, username):
        async with db_helper.session_factory() as session:
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id)
                )

            if not user:
                session.add(User(tg_id=tg_id, username=username))
                await session.commit()
            return user
