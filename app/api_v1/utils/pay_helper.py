from yoomoney import Client, Quickpay
from aiogram import Bot

from app.api_v1 import settings

from .request_api import outline_helper


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
        successURL="https://t.me/Real_vpnBot",
    )
    return quickpay.base_url


async def get_payment(tg_id: int, bot: Bot):

    key = outline_helper.create_new_key(name=tg_id)

    await bot.send_message(
        tg_id,
        text=(f"Подписка оплачена, вот ваш ключ: {key.access_url}"),
    )
