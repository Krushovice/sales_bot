import asyncio

# import hashlib

from app.api_v1.utils.payment.tinkoff_pay_helper import payment_manager

from app.api_v1.utils import (
    generate_order_number,
    get_receipt,
)

#     create_token,
# )
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
#     key = outline_helper.create_new_key(name="12345673")
#     url = gen_outline_dynamic_link(key=key)
#     return url


# print(test())
