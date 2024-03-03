from enum import IntEnum, auto


from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from .payment_kb import PayActions, PaymentCbData


class ProfileActions(IntEnum):
    refill = auto()
    back_to_main = auto()
    show_key = auto()
    tutorial = auto()
    back_to_key = auto()
    renewal = auto()


class ProfileCbData(CallbackData, prefix="account"):
    action: ProfileActions


def build_account_kb(user=None) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пополнить баланс 💰",
        callback_data=ProfileCbData(action=ProfileActions.refill).pack(),
    )
    if user and user.key:
        builder.button(
            text=f"VPN | {user.expiration_date} | Outline",
            callback_data=ProfileCbData(action=ProfileActions.show_key).pack(),
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


def build_renewal_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Подключить со скидкой ❇️",
        callback_data=ProfileCbData(action=ProfileActions.renewal).pack(),
    )

    builder.adjust(1)

    return builder.as_markup()
