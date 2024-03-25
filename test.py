import asyncio

# import hashlib

from app.api_v1.utils.payment.tinkoff_pay_helper import payment_manager

from app.api_v1.utils import (
    generate_order_number,
    get_receipt,
    set_expiration_date,
)

#     create_token,
# # )
# from app.api_v1.orm import AsyncOrm


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
    try:
        res = await check_pay()
        print(res)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())

# from app.api_v1.utils import outline_helper
# from app.api_v1.utils.requests.dinamic_url import gen_outline_dynamic_link


# def test():
#     date = set_expiration_date(duration=2, rest="15-04-2024")
#     return date


# print(test())
