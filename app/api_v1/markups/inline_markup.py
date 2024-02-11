from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_on_start_kb() -> InlineKeyboardMarkup:
    pay_btn = InlineKeyboardButton(
        text="Купить VPN 💰",
        callback_data="buy"
    )
    to_account_btn = InlineKeyboardButton(
        text="Аккаунт 👤",
        callback_data="account"
    )
    help_btn = InlineKeyboardButton(
        text="Помощь ⚒",
        callback_data="help"
    )
    advantage_btn = InlineKeyboardButton(
        text="Преимущества ♻️",
        callback_data="advantage"
    )

    first_row = [pay_btn, help_btn]
    sec_row = [to_account_btn, advantage_btn]

    rows = [first_row,
            sec_row]

    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


def get_profile_kb() -> InlineKeyboardMarkup:
    pass


def get_payment_kb() -> InlineKeyboardMarkup:
    pass
