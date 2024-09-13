from enum import IntEnum, auto


from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .payment_kb import PayActions, PaymentCbData

from app.api_v1.admin.admin_kb import AdminCbData, AdminActions


class MenuActions(IntEnum):
    pay = auto()
    account = auto()
    support = auto()
    promo = auto()
    back_root = auto()
    next = auto()
    key = auto()
    back_to_key = auto()


class MenuCbData(CallbackData, prefix="main"):
    action: MenuActions


def build_main_kb(
    subscribe: bool = False,
    admin: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Купить VPN 💰",
        callback_data=PaymentCbData(action=PayActions.pay).pack(),
    )
    builder.button(
        text="Помощь ⚒",
        callback_data=MenuCbData(action=MenuActions.support).pack(),
    )
    if subscribe:
        builder.button(
            text="Ключ Outline🔑",
            callback_data=MenuCbData(action=MenuActions.key).pack(),
        )
    builder.button(
        text="Ввести промокод 👑",
        callback_data=MenuCbData(action=MenuActions.promo).pack(),
    )
    if admin:
        builder.button(
            text="Админка",
            callback_data=AdminCbData(action=AdminActions.admin_panel).pack(),
        )

    builder.adjust(2)

    return builder.as_markup()


def build_next_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="К оплате➡️",
        callback_data=MenuCbData(action=MenuActions.next).pack(),
    )
    builder.button(
        text="Назад 🔙",
        callback_data=MenuCbData(action=MenuActions.back_root).pack(),
    )
    builder.adjust(2)

    return builder.as_markup()


def root_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад 🔙",
        callback_data=MenuCbData(action=MenuActions.back_root).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
