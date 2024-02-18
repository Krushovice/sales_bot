from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.api_v1.utils.pay_helper import get_quickpay_url, get_payment


class PayActions(IntEnum):
    pay = auto()
    back_to_account = auto()
    success = auto()


class ProductActions(IntEnum):
    details = auto()
    back_to_choice = auto()


class PaymentCbData(CallbackData, prefix="pay"):
    action: PayActions


class ProductCbData(CallbackData, prefix="product"):
    action: ProductActions
    name: str | None = None
    price: int | None = None


def build_payment_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for name, price in [
        ("150р - 1мес🔹", 150),
        ("400р - 3мес🔸", 400),
        ("800р - 6мес🔻", 800),
    ]:
        builder.button(
            text=name,
            callback_data=ProductCbData(
                action=ProductActions.details,
                name=name,
                price=price,
            ),
        )

    builder.button(
        text="Назад🔙",
        callback_data=PaymentCbData(action=PayActions.back_to_account).pack(),
    )

    builder.adjust(1)

    return builder.as_markup()


def product_details_kb(
    payment_cb_data: PaymentCbData,
    tg_id: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Оплатить",
        url=f"{get_quickpay_url(pay_in=payment_cb_data.price, tg_id=tg_id,)}",
    ),

    builder.button(
        text="Назад🔙",
        callback_data=ProductCbData(
            action=ProductActions.back_to_choice,
        ).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()


def build_pay_button(tg_id: int) -> InlineKeyboardMarkup:
    pay_btn = InlineKeyboardButton(
        text="Оплатить",
        url=f"{get_quickpay_url(pay_in=150, tg_id=tg_id,)}",
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[pay_btn]])
    return keyboard


def get_success_pay_button(
    product_data: ProductCbData,
) -> InlineKeyboardMarkup:
    success_btn = InlineKeyboardButton(
        text="Я оплатил",
        callback_data=ProductCbData(action=PayActions.success).pack(),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[success_btn]])
    return keyboard
