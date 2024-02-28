from enum import IntEnum, auto

from typing import TYPE_CHECKING

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.api_v1.utils.yoomoney_pay_helper import get_quickpay_url
from app.api_v1.utils.yookassa_pay_helper import payment_helper

if TYPE_CHECKING:
    from .account_kb import ProfileActions, ProfileCbData


class PayActions(IntEnum):
    pay = auto()
    back_to_account = auto()
    success = auto()


class ProductActions(IntEnum):
    details = auto()
    back_to_choice = auto()


class PaymentCbData(CallbackData, prefix="pay"):
    action: PayActions
    payment_id: int | None = None
    price: int | None = None


class ProductCbData(CallbackData, prefix="product"):
    action: ProductActions
    name: str | None = None
    price: int | None = None


def build_payment_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for name, price in [
        ("150р - 1мес🔹", 150),
        ("270р - 2мес🔸", 270),
        ("390р - 3мес🔻", 390),
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
    payment_cb_data,
    from_main_menu: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Оплатить",
        url=f"{payment_cb_data.confirmation.confirmation_url}",
        callback_data=PaymentCbData(
            action=PayActions.pay,
            payment_id=payment_cb_data.payment_id,
            price=payment_cb_data.amount.value,
        ),
    ),

    builder.button(
        text="Назад🔙",
        callback_data=(
            ProductCbData(
                action=ProductActions.back_to_choice,
            ).pack()
            if not from_main_menu
            else ProfileCbData(
                action=ProfileActions.back_to_main,
            )
        ),
    )
    builder.adjust(1)

    return builder.as_markup()


def get_success_pay_button(
    payment_id: int,
) -> InlineKeyboardMarkup:
    success_btn = InlineKeyboardButton(
        text="Я оплатил",
        callback_data=PaymentCbData(
            action=PayActions.success,
            payment_id=payment_id,
        ),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[success_btn]])
    return keyboard
