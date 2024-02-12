from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ProfileActions(IntEnum):
    refill = auto()
    back = auto()


class AccountCbData(CallbackData, prefix="account"):
    action: ProfileActions


def build_account_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пополнить баланс 💰",
        callback_data=AccountCbData(action=ProfileActions.refill).pack(),
    )
    builder.button(
        text="Назад 🔙",
        callback_data=AccountCbData(action=ProfileActions.back).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
