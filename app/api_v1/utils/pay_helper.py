from yoomoney import Client, Quickpay

from app.api_v1.config import settings


def check_balance_info():
    client = Client(settings.get_yookassa_token)

    user = client.account_info()

    balance = user.balance
    return balance


def get_quickpay_url(pay_in: int):
    quickpay = Quickpay(
        receiver="4100118302539544",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=pay_in,
    )
    return quickpay.base_url
