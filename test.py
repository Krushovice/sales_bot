import asyncio
import time

# import hashlib

from app.api_v1.utils.payment.tinkoff_pay_helper import payment_manager

from app.api_v1.utils import (
    generate_order_number,
    get_receipt,
    set_expiration_date,
    get_subscribe_info,
)

#     create_token,
# # )
from app.api_v1.orm import AsyncOrm


async def create_payment():
    payment = await payment_manager.init_payment(
        amount=15000,
        order_id=generate_order_number(),
        description="Оплата платной подписки на канал",
        receipt=get_receipt(150),
    )
    return payment


async def check_status(payment):
    payment_id = payment["PaymentId"]

    payment_status = await payment_manager.check_payment_status(
        payment_id=payment_id,
    )
    return payment_status


async def check_pay():
    payment = await create_payment()
    status = await check_status(payment)
    return status


async def main():
    # try:
    #     res = await check_pay()
    #     print(res)
    # except Exception as e:
    #     print(f"Ошибка: {e}")
    start_time = time.time()  # время начала выполнения
    # referrals = await AsyncOrm.get_active_referrals(tg_id=1130398207)
    # print(referrals)
    user = await AsyncOrm.get_user(tg_id=1130398207)
    print(user)
    end_time = time.time()  # время окончания выполнения
    execution_time = end_time - start_time  # вычисляем время выполнения

    print(f"Время выполнения программы: {execution_time} секунд")

    # users = await AsyncOrm.get_users_by_subscription()
    # print(users)

    # inactive = await AsyncOrm.get_inactive_users()
    # print(inactive)
    # sub_info = get_subscribe_info(user)
    # print(sub_info)

    # return sub_info


if __name__ == "__main__":
    asyncio.run(main())

# from app.api_v1.utils import outline_helper
# from app.api_v1.utils.requests.dinamic_url import gen_outline_dynamic_link


# def test():
#     date = set_expiration_date(duration=2, rest="15-04-2024")
#     return date


# print(test())