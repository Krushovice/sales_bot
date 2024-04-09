from enum import IntEnum, auto


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
    questions = auto()
    back_to_help = auto()
    back_root = auto()


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


def build_questions_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Основные вопросы ❓",
        callback_data=MenuCbData(action=MenuActions.questions).pack(),
    )

    builder.button(
        text="Назад в меню 🔙",
        callback_data=MenuCbData(action=MenuActions.back_root).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def build_back_info_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад ⏪",
        callback_data=MenuCbData(action=MenuActions.back_to_help).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def build_account_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="В личный кабинет➡️",
        callback_data=MenuCbData(action=MenuActions.account).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()
