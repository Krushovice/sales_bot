import asyncio

from app.api_v1.utils import payment_manager, generate_order_number, get_receipt


async def main():
    payment = await payment_manager.init_payment(
            amount=15000,
            order_id=generate_order_number(),
            description=f"Оплата пользователя № {123}",
            receipt=get_receipt(price=150),
        )
    print(payment)

if __name__ == "__main__":
    asyncio.run(main())
