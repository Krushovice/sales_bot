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


class ProductActions(IntEnum):
    details = auto()
    back_to_choice = auto()
    success = auto()


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
    pay_in: int = None,
    payment_cb_data=None,
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
        ).pack(),
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


# def build_pay_button(tg_id: int) -> InlineKeyboardMarkup:
#     pay_btn = InlineKeyboardButton(
#         text="Оплатить",
#         url=f"{get_quickpay_url(pay_in=150, tg_id=tg_id,)}",
#     )
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[pay_btn]])
#     return keyboard


def get_success_pay_button(
    payment_id: int,
) -> InlineKeyboardMarkup:
    success_btn = InlineKeyboardButton(
        text="Я оплатил",
        callback_data=ProductCbData(
            action=ProductActions.success,
            payment_id=payment_id,
        ).pack(),
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[success_btn]])
    return keyboard
