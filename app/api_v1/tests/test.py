import asyncio

# import time

# from sqlalchemy import select
# from sqlalchemy.orm import selectinload
# from sqlalchemy.engine import Result
# from sqlalchemy.ext.asyncio import AsyncSession
from app.api_v1.utils.payment.tinkoff_pay_helper import payment_manager

from app.api_v1.utils import (
    generate_order_number,
    get_receipt,
)

#     set_expiration_date,
#     get_subscribe_info,
#     create_token,
# )


# from app.api_v1.orm import AsyncOrm, User, db_helper, create_tables


async def create_payment():
    payment = await payment_manager.init_sbp_payment(
        amount=1000,
        order_id=generate_order_number(),
        description="Оплата платной подписки на канал",
        receipt=get_receipt(10),
    )
    return payment


async def check_status(payment):
    payment_id = payment["PaymentId"]

    payment_status = await payment_manager.check_payment_status(
        payment_id=payment_id,
    )
    return payment_status


async def main():
    payment = await create_payment()
    # status = await check_status(payment["PaymentId"])

    print(payment)
    return


if __name__ == "__main__":
    asyncio.run(main())
# async def get_user(session: AsyncSession, tg_id: int) -> User:

#     stmt = (
#         select(User)
#         .options(selectinload(User.referrals))
#         .options(selectinload(User.key))
#         .where(User.tg_id == tg_id)
#     )

#     result: Result = await session.execute(stmt)

#     user: User | None = result.scalar_one_or_none()
#     return user


# async def main():
#     await create_tables()
#     async with db_helper.session_factory() as session:  # try:
#         #     res = await check_pay()
#         #     print(res)
#         # except Exception as e:
#         #     print(f"Ошибка: {e}")
#         start_time = time.time()  # время начала выполнения
#         # referrals = await AsyncOrm.get_active_referrals(tg_id=1130398207)
#         # print(referrals)
#         user = await get_user(session=session, tg_id=1130398207)
#         print(user)
#         end_time = time.time()  # время окончания выполнения
#         execution_time = end_time - start_time  # вычисляем время выполнения

#         print(f"Время выполнения программы: {execution_time} секунд")


# users = await AsyncOrm.get_users_by_subscription()
# print(users)

# inactive = await AsyncOrm.get_inactive_users()
# print(inactive)
# sub_info = get_subscribe_info(user)
# print(sub_info)

# return sub_info


# from app.api_v1.utils import outline_helper
# from app.api_v1.utils.requests.dinamic_url import gen_outline_dynamic_link


# def test():
#     date = set_expiration_date(duration=2, rest="15-04-2024")
#     return date


# print(test())

# import asyncio
# from unittest.mock import AsyncMock, patch

# from app.api_v1.utils.tools import send_logs_email

# from app.api_v1.config import settings


# async def test_email_send():
#     await send_logs_email()


# if __name__ == "__main__":
#     asyncio.run(test_email_send())