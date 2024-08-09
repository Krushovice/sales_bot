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


def calculate_expiration_date(
        date: str | None = None,
        duration: int | None = None,
        flag: bool = False,
) -> str:
    today = datetime.datetime.today().date()
    if flag:
        delta = datetime.timedelta(days=7)
        expiration_date = (today + delta).strftime("%d-%m-%Y")
        return expiration_date

    else:
        days = 31 * duration
    rest_of_sub = datetime.datetime.strptime(date, "%d-%m-%Y").date()
    expiration = (rest_of_sub - today).days

    if expiration > 0:
        delta = datetime.timedelta(days=days + int(expiration))
    else:
        delta = datetime.timedelta(days=days)

    expiration_date = (today + delta).strftime("%d-%m-%Y")

    return expiration_date


def check_time_delta(date: str | None) -> bool:
    if not date:
        return False
    today = datetime.datetime.today().date()
    rest_of_sub = datetime.datetime.strptime(date, "%d-%m-%Y").date()
    delta = (rest_of_sub - today).days
    if delta > 0:
        return True
    return False


def set_expiration_date(
    duration: int,
    rest: str | None,
    is_referrer: bool = False,
) -> str:

    if rest:
        if not is_referrer:
            return calculate_expiration_date(rest, duration)
        return calculate_expiration_date(flag=True)

    else:
        return calculate_expiration_date(duration=duration)


def get_duration(payment) -> int:
    try:
        if 7500 <= payment["Amount"] <= 15000:
            return 1

        elif 20000 <= payment["Amount"] <= 40000:
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

    data["Password"] = password

    # Исключаем вложенные объекты и массивы из расчета токена
    filtered_data = {k: v for k, v in data.items() if not isinstance(v, (dict, list))}

    # Конвертация словаря в отсортированный список кортежей (ключ, значение)
    sorted_data = sorted(filtered_data.items(), key=lambda x: x[0])
    # Конкатенация значений пар в одну строку
    concatenated_values = "".join([str(value) for _, value in sorted_data])

    hashed_token = hashlib.sha256(concatenated_values.encode("utf-8")).hexdigest()

    return str(hashed_token)


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
