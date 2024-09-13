from enum import IntEnum, auto


from app.api_v2.markups import MenuCbData, MenuActions

from aiogram.filters.callback_data import CallbackData

from aiogram.types import InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder


class AdminActions(IntEnum):
    admin_panel = auto()
    statistic = auto()
    back_to_main = auto()
    back_to_root_panel = auto()
    back_root_admin = auto()


class AdminCbData(CallbackData, prefix="admin"):
    action: AdminActions


def build_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="В админ панель 🔐",
        callback_data=AdminCbData(action=AdminActions.admin_panel).pack(),
    )

    builder.button(
        text="Назад 🔙",
        callback_data=MenuCbData(action=MenuActions.back_root).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def build_stat_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Статистика 〽️",
        callback_data=AdminCbData(action=AdminActions.statistic).pack(),
    )

    builder.button(
        text="Вернуться🔙",
        callback_data=AdminCbData(
            action=AdminActions.back_to_root_panel,
        ).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def back_to_admin_panel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Назад🔙",
        callback_data=AdminCbData(
            action=AdminActions.back_root_admin,
        ).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
