import datetime

# import logging
import uuid


from yookassa import Payment, Configuration


from app.api_v1.config import settings


from app.api_v1.utils.logging import setup_logger

logger = setup_logger(__name__)


class PaymentHelper:

    Configuration.account_id = "Идентификатор магазина"
    Configuration.secret_key = "Секретный ключ"

    @staticmethod
    async def create_payment(tg_id: int, price: int):
        try:
            payment = Payment.create(
                {
                    "amount": {"value": price, "currency": "RUB"},
                    "payment_method_data": {"type": "sbp"},
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://www.example.com/return_url",
                    },
                    "description": tg_id,
                    "capture": True,
                },
                str(uuid.uuid4()),
            )
            return payment
        except Exception as e:
            logger.error(f"Error with payment create: {e}")

    @staticmethod
    async def get_payment(payment_id: int):
        try:
            payment = Payment.find_one(payment_id)
            if payment:
                return payment
            return None

        except Exception as e:
            logger.error(f"Something wrong with payment request: {e}")


payment_helper = PaymentHelper()
