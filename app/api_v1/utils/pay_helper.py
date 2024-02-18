import datetime
from collections import namedtuple

from yoomoney import Client, Quickpay


from app.api_v1.config import settings


def check_balance_info():
    client = Client(settings.get_yookassa_token)

    user = client.account_info()

    balance = user.balance
    return balance


def get_quickpay_url(pay_in: int, tg_id: int):
    new = tg_id
    quickpay = Quickpay(
        receiver="4100118302539544",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=pay_in,
        label=new,
        successURL="https://t.me/Real_vpnBot?id={tg_id}",
    )
    return quickpay.base_url


def get_payment(tg_id: int):
    Payment = namedtuple("Payment", ["balance", "operation_date", "expiration_date"])
    today = datetime.datetime.today().strftime("%Y-%m-%d")

    client = Client(settings.get_yookassa_token)
    history = client.operation_history()

    for operation in history.operations:
        if operation.label == str(tg_id):
            if operation.status == "success":
                operation_date = operation.datetime.strftime("%Y-%m-%d")
                if today == operation_date:
                    delta = datetime.timedelta(days=31)
                    expiration_date = (operation.datetime + delta).strftime("%Y-%m-%d")
                    balance = operation.amount
                    payment = Payment(balance, operation_date, expiration_date)
                    print(payment)
                    return payment
                return None
