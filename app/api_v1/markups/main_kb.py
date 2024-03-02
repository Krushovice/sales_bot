from enum import IntEnum, auto

# from typing import TYPE_CHECKING

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .payment_kb import PayActions, PaymentCbData


class MenuActions(IntEnum):
    pay = auto()
    account = auto()
    support = auto()
    advantage = auto()
    promo = auto()


class MenuCbData(CallbackData, prefix="main"):
    action: MenuActions


def build_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Купить VPN 💰",
        callback_data=PaymentCbData(action=PayActions.pay).pack(),
    )
    builder.button(
        text="Помощь ⚒",
        callback_data=MenuCbData(action=MenuActions.support).pack(),
    )

    builder.button(
        text="Аккаунт 👤",
        callback_data=MenuCbData(action=MenuActions.account).pack(),
    )

    builder.button(
        text="Преимущества ♻️",
        callback_data=MenuCbData(action=MenuActions.advantage).pack(),
    )

    builder.button(
        text="Ввести промокод 👑",
        callback_data=MenuCbData(action=MenuActions.promo).pack(),
    )
    builder.adjust(2)

    return builder.as_markup()
