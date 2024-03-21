import aiohttp

from app.api_v1.config import settings
from .payment_details import generate_token, create_token


class PaymentManager:
    def __init__(self, terminal_key, secret_key):
        self.terminal_key = terminal_key
        self.secret_key = secret_key
        self.api_url = "https://securepay.tinkoff.ru/v2/"

    async def init_payment(
        self,
        amount,
        order_id,
        description,
        receipt,
    ):

        data = {
            "TerminalKey": self.terminal_key,
            "Amount": amount,
            "OrderId": order_id,
            "Description": description,
            "Receipt": receipt,
        }

        token = generate_token(
            data=data,
            password=self.secret_key,
        )
        data.update({"Token": token})

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url + "Init",
                json=data,
                ssl=False,
            ) as response:
                result = await response.json()
                return result

    async def check_payment_status(self, payment_id):
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
        }
        token = create_token(str(data["PaymentId"]))
        data.update({"Token": token})

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url + "GetState",
                json=data,
                ssl=False,
            ) as response:
                result = await response.json()
                return result

    async def get_payment_info(self, payment_id):
        data = {
            "TerminalKey": self.terminal_key,
            "PaymentId": payment_id,
        }

        token = create_token(str(data["PaymentId"]))
        data.update({"Token": token})

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url + "GetReceipt",
                json=data,
                ssl=False,
            ) as response:
                result = await response.json()
                return result


payment_manager = PaymentManager(
    terminal_key=settings.tinkoff_terminal_key,
    secret_key=settings.tinkoff_secret,
)
