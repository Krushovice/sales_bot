import re
import uuid
import hashlib
import datetime

from app.api_v1.utils.logging import setup_logger

from app.api_v1.config import settings

logger = setup_logger(__name__)


def generate_order_number():
    # Генерируем UUID (универсальный уникальный идентификатор)
    order_id = uuid.uuid4()
    # Преобразуем UUID в строку и убираем дефисы
    order_number = str(order_id).replace("-", "")
    # Обрезаем строку до 30 символов, если она слишком длинная
    order_number = order_number[:30]
    return order_number


def set_expiration_date(
    duration: int,
    rest: str | None,
    is_referrer: bool = False,
) -> str:
    today = datetime.datetime.today().date()

    if rest and datetime.datetime.strptime(rest, "%d-%m-%Y").date() > today:
        expiration = datetime.datetime.strptime(rest, "%d-%m-%Y").date()
        result = expiration - today
        rest = result.days
        days = 31 * duration if not is_referrer else duration * 7
        delta = datetime.timedelta(days=days + int(rest))
        expiration_date = (today + delta).strftime("%d-%m-%Y")
        return expiration_date
    else:
        days = 31 * duration if not is_referrer else duration * 7
        expiration = today + datetime.timedelta(days=days)
        return expiration.strftime("%d-%m-%Y")


def get_duration(payment) -> int:
    try:
        if 7500 <= payment["Amount"] <= 15000:
            return 1

        elif 13500 <= payment["Amount"] <= 27000:
            return 2

        else:
            return 3
    except Exception as e:
        logger.error(f"Something wrong with payment check: {e}")


def get_receipt(price):
    data = {
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
    return data


def create_token(payment_id):

    tokentr = settings.tinkoff_secret + payment_id + settings.tinkoff_terminal_key
    tokensha256 = str(hashlib.sha256(tokentr.encode()).hexdigest())
    return tokensha256


def generate_token(data, password):
    # Конвертация словаря в отсортированный список кортежей (ключ, значение)
    sorted_data = sorted(data.items(), key=lambda x: x[0])

    # Конкатенация значений пар в одну строку
    concatenated_values = "".join([str(value) for key, value in sorted_data])

    # Добавление пароля к конкатенированным значениям
    concatenated_values += password

    # Применение хеш-функции SHA-256
    hashed_token = hashlib.sha256(concatenated_values.encode()).hexdigest()

    return hashed_token


def check_payment_date(data: str) -> bool:
    today = datetime.datetime.today().date()
    pattern = r":\s*(\d{4}-\d{2}-\d{2})"

    # Извлекаем дату из строки, если она присутствует
    match = re.search(pattern, data)
    if match:
        string_date = match.group(1)
        # Преобразование строки даты в объект datetime
        pay_date = datetime.datetime.strptime(string_date, "%Y-%m-%d").date()
        if pay_date == today:
            return True
    return False


def check_payment(payment) -> bool:
    return True if payment["Status"] == "CONFIRMED" else False
