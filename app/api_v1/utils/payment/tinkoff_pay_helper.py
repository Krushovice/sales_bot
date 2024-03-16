import requests

from app.api_v1.config import settings


class PaymentManager:
    def __init__(self, terminal_key, secret_key):
        self.terminal_key = terminal_key
        self.secret_key = secret_key
        self.api_url = "https://securepay.tinkoff.ru/v2/"

    def init_payment(self, amount, order_id, description):
        data = {
            "TerminalKey": self.terminal_key,
            "Amount": amount,
            "OrderId": order_id,
            "Description": description,
        }
        response = requests.post(self.api_url + "Init", json=data)
        return response.json()

    def check_payment_status(self, payment_id):
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
        }
        response = requests.post(self.api_url + "GetState", json=data)
        return response.json()

    def get_payment_info(self, payment_id):
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
        }
        response = requests.post(self.api_url + "GetReceipt", json=data)
        return response.json()


payment_manager = PaymentManager(
    terminal_key=settings.tinkoff_terminal_key,
    secret_key=settings.tinkoff_secret_key,
)
