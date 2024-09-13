from enum import IntEnum, auto


from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from .payment_kb import (
    PayActions,
    PaymentCbData,
)

from .main_kb import (
    MenuActions,
    MenuCbData,
)


class ProfileActions(IntEnum):
    refill = auto()
    back_to_main = auto()
    show_key = auto()
    tutorial = auto()
    back_to_key = auto()
    renewal = auto()


class ProfileCbData(CallbackData, prefix="account"):
    action: ProfileActions


def build_account_kb(
    exp_date: str = None,
    is_key: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_key and exp_date:
        builder.button(
            text="Оплатить подписку 💰",
            callback_data=ProfileCbData(action=ProfileActions.refill).pack(),
        )
        builder.button(
            text=f"VPN 🛡| {exp_date} | Outline♻️",
            callback_data=ProfileCbData(action=ProfileActions.show_key).pack(),
        )
    else:
        builder.button(
            text="Оплатить подписку 💰",
            callback_data=ProfileCbData(action=ProfileActions.refill).pack(),
        )
    builder.button(
        text="Назад 🔙",
        callback_data=ProfileCbData(action=ProfileActions.back_to_main).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def root_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад 🔙",
        callback_data=ProfileCbData(action=ProfileActions.back_to_main).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def back_to_key_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад 🔙",
        callback_data=ProfileCbData(action=ProfileActions.back_to_key).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def help_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Как установить 👋",
        callback_data=ProfileCbData(action=ProfileActions.tutorial).pack(),
    )

    builder.button(
        text="Назад 🔙",
        callback_data=PaymentCbData(action=PayActions.back_to_account).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def build_renewal_kb(
    need_help: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not need_help:
        builder.button(
            text="Подключить со скидкой ❇️",
            callback_data=ProfileCbData(action=ProfileActions.renewal).pack(),
        )

    else:
        builder.button(
            text="Помощь в подключении 🆘",
            callback_data=MenuCbData(action=MenuActions.support).pack(),
        )
        builder.button(
            text="Подключить со скидкой ❇️",
            callback_data=ProfileCbData(action=ProfileActions.renewal).pack(),
        )

    builder.adjust(1)
    return builder.as_markup()
