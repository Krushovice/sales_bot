import datetime
import uuid
import logging


from yookassa import Payment, Configuration


from app.api_v1.config import settings


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
            logging.error(f"Error with payment create: {e}")

    @staticmethod
    async def get_payment(payment_id: int):
        try:
            payment = Payment.find_one(payment_id)
            if payment:
                return payment
            return None

        except Exception as e:
            logging.error(f"Something wrong with payment request: {e}")


payment_helper = PaymentHelper()


def set_expiration_date(duration: int) -> str:
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    delta = datetime.timedelta(days=31 * duration)
    expiration_date = (today + delta).strftime("%Y-%m-%d")
    return expiration_date


def get_duration(payment) -> int:
    try:
        if payment.amount.value == 150:
            return 1

        elif payment.amount.value == 270:
            return 2

        else:
            return 3
    except Exception as e:
        logging.error(f"Something wrong with payment check: {e}")
