from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from app.api_v1.utils.chek_user import check_user


class ProfileActions(IntEnum):
    refill = auto()
    back = auto()
    show_key = auto()


class AccountCbData(CallbackData, prefix="account"):
    action: ProfileActions


def build_account_kb(tg_id=None) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пополнить баланс 💰",
        callback_data=AccountCbData(action=ProfileActions.refill).pack(),
    )
    # user = check_user(tg_id=tg_id)
    # if user:
    #     builder.button(
    #         text=f"VPN | {user.expiration_date} | Outline",
    #         callback_data=AccountCbData(action=ProfileActions.show_key).pack(),
    #     )
    builder.button(
        text="Назад 🔙",
        callback_data=AccountCbData(action=ProfileActions.back).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def root_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад 🔙",
        callback_data=AccountCbData(action=ProfileActions.back).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
