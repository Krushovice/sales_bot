# import asyncio
# import hashlib

# from app.api_v1.utils.payment.tinkoff_pay_helper import payment_manager

# from app.api_v1.utils import (
#     generate_order_number,
#     get_receipt,
#     create_token,
# )


# async def create_payment():
#     payment = await payment_manager.init_payment(
#         amount=15000,
#         order_id=generate_order_number(),
#         description="Оплата платной подписки на канал",
#         receipt=get_receipt(150),
#     )
#     return payment


# async def check_status(payment):
#     payment_id = payment["PaymentId"]
#     token = create_token(payment_id)
#     payment_status = await payment_manager.check_payment_status(
#         payment_id=payment_id,
#         token=token,
#     )
#     return payment_status


# async def check_pay():
#     task1 = asyncio.create_task(create_payment())
#     task2 = asyncio.create_task(check_status(create_payment()))
#     asyncio.gather(task1, task2)


# async def main():
#     await check_pay()


# if __name__ == "__main__":
#     asyncio.run(main())

from app.api_v1.utils import outline_helper
from app.api_v1.utils.requests.dinamic_url import gen_outline_dynamic_link


def test():
    key = outline_helper.create_new_key(name="12345673")
    url = gen_outline_dynamic_link(key=key)
    return url


print(test())
