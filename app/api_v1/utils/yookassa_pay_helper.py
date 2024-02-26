import datetime
import uuid


from yookassa import Payment, Configuration


from app.api_v1.config import settings


class PaymentHelper:

    Configuration.account_id = "Идентификатор магазина"
    Configuration.secret_key = "Секретный ключ"

    @staticmethod
    async def create_payment(tg_id: int, price: int):
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

    @staticmethod
    async def get_payment(payment_id: int):
        payment = Payment.find_one(payment_id)
        if payment:
            return payment
        return None


payment_helper = PaymentHelper()


def set_expiration_date():

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    delta = datetime.timedelta(days=31)
    expiration_date = (today + delta).strftime("%Y-%m-%d")
    return expiration_date


# async def create_payment(
#     username: str,
#     tg_id: int,
#     amount: int,
#     duration: int,
# ):
#     conn = http.client.HTTPSConnection("business.tinkoff.ru")
#     payload = json.dumps(
#         {
#             "TerminalKey": "TinkoffBankTest",
#             "Amount": amount,
#             "OrderId": "",
#             "Description": f"Оплата подписки на {duration} месяца",
#             "Token": "token",
#             "DATA": {
#                 "username": username,
#                 "tg_id": tg_id,
#                 "duration": duration,
#             },
#             "Receipt": {
#                 "username": username,
#                 "tg_id": tg_id,
#                 "duration": duration,
#                 "Taxation": "osn",
#                 "Items": ["VPN"],
#             },
#         }
#     )
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }
#     conn.request(
#         "POST",
#         "https://securepay.tinkoff.ru/v2/Init",
#         payload,
#         headers,
#     )
#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))
#     return data.decode("utf-8")


# async def get_status_payment(payment_id: int):
#     conn = http.client.HTTPSConnection("business.tinkoff.ru")
#     payload = json.dumps(
#         {
#             "TerminalKey": "TinkoffBankTest",
#             "PaymentId": payment_id,
#             "Token": "token",
#             "IP": "192.168.0.52",
#         },
#     )
#     headers = {"Accept": "application/json"}
#     conn.request(
#         "POST",
#         "https://securepay.tinkoff.ru/v2/GetState",
#         payload,
#         headers,
#     )
#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))
#     return data.decode("utf-8")
