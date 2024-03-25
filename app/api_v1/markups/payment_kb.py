from enum import IntEnum, auto

from typing import TYPE_CHECKING

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PayActions(IntEnum):
    pay = auto()
    back_to_account = auto()
    success = auto()


class ProductActions(IntEnum):
    details = auto()
    back_to_choice = auto()
    back_to_root = auto()


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
    success: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not success:
        builder.button(
            text="Оплатить",
            url=f"{payment_cb_data['PaymentURL']}",
            callback_data=PaymentCbData(
                action=PayActions.pay,
                payment_id=payment_cb_data["PaymentId"],
                price=payment_cb_data["Amount"] / 100,
            ),
        ),
        builder.button(
            text="Я оплатил✅",
            callback_data=PaymentCbData(
                action=PayActions.success,
                payment_id=payment_cb_data["PaymentId"],
            ),
        )
    else:
        builder.button(
            text="Проверить платеж 🔄",
            callback_data=PaymentCbData(
                action=PayActions.success,
                payment_id=payment_cb_data["PaymentId"],
            ),
        )
    builder.button(
        text="Назад🔙",
        callback_data=(
            ProductCbData(
                action=ProductActions.back_to_choice,
            ).pack()
            if not from_main_menu
            else ProductCbData(
                action=ProductActions.back_to_root,
            )
        ),
    )
    builder.adjust(1)

    return builder.as_markup()
