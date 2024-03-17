import uuid

import datetime

from app.api_v1.utils.logging import setup_logger

logger = setup_logger(__name__)


def generate_order_number():
    # Генерируем UUID (универсальный уникальный идентификатор)
    order_id = uuid.uuid4()
    # Преобразуем UUID в строку и убираем дефисы
    order_number = str(order_id).replace("-", "")
    # Обрезаем строку до 36 символов, если она слишком длинная
    order_number = order_number[:36]
    return order_number


def set_expiration_date(duration: int) -> str:
    today = datetime.datetime.today().strftime("%d-%m-%Y")
    delta = datetime.timedelta(days=31 * duration)
    expiration_date = (today + delta).strftime("%d-%m-%Y")
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
        logger.error(f"Something wrong with payment check: {e}")


def get_receipt(price):
    return {
        "Taxation": "usn_income",
        "Email": "list90@list.ru",
        "Items": [
            {
                "Name": "Подписка на канал",
                "Price": price * 100,
                "Quantity": 1.0,
                "Amount": price * 100,
                "PaymentMethod": "full_payment",
                "PaymentObject": "service",
                "Tax": "none",
            },
        ],
    }
