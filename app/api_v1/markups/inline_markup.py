from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_on_start_kb() -> InlineKeyboardMarkup:
    pay_btn = InlineKeyboardButton(
        text="Купить VPN 💰",
        callback_data="buy",
    )
    to_account_btn = InlineKeyboardButton(
        text="Аккаунт 👤",
        callback_data="account",
    )
    help_btn = InlineKeyboardButton(
        text="Помощь ⚒",
        callback_data="help",
    )
    advantage_btn = InlineKeyboardButton(
        text="Преимущества ♻️",
        callback_data="advantage",
    )

    first_row = [pay_btn, help_btn]
    sec_row = [to_account_btn, advantage_btn]

    rows = [first_row, sec_row]

    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


def get_profile_kb() -> InlineKeyboardMarkup:
    refill_btn = InlineKeyboardButton(
        text="Пополнить баланс 💰",
        callback_data="refill_balance",
    )
    to_main_btn = InlineKeyboardButton(
        text="Назад 🔙",
        callback_data="back_main",
    )

    first_row = [refill_btn]
    sec_row = [to_main_btn]

    rows = [first_row, sec_row]

    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


def get_payment_kb() -> InlineKeyboardMarkup:

    first_btn = InlineKeyboardButton(
        text="130 - 1мес",
        callback_data="one_month",
    )
    sec_btn = InlineKeyboardButton(
        text="400 - 3мес",
        callback_data="three_months",
    )
    third_btn = InlineKeyboardButton(
        text="800 - 6мес",
        callback_data="six_months",
    )
    back_btn = InlineKeyboardButton(
        text="Назад🔙",
        callback_data="back_to_account",
    )

    first_row = [first_btn]
    sec_row = [sec_btn]
    third_row = [third_btn]
    last_row = [back_btn]
    rows = [first_row, sec_row, third_row, last_row]

    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
