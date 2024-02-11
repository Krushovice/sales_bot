from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from .schemas import UserCreate, UserUpdatePartial, UserUpdate


async def get_user(
    session: AsyncSession,
    tg_id: int,
) -> User | None:
    return await session.get(User, tg_id)


async def create_product(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def update_product(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    for name, val in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, val)
    await session.commit()
    return user


async def delete_product(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
