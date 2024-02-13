from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PayActions(IntEnum):
    pay = auto()
    back = auto()


class ProductActions(IntEnum):
    details = auto()


class PaymentCbData(CallbackData, prefix="pay"):
    action: PayActions


class ProductCbData(CallbackData, prefix="product"):
    action: ProductActions
    name: str
    price: int


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
        callback_data=PaymentCbData(action=PayActions.back).pack(),
    )

    builder.adjust(1)

    return builder.as_markup()


def product_details_kb(
    payment_cb_data: PaymentCbData,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Оплатить",
        callback_data=PaymentCbData(
            action=PayActions.pay,
            **payment_cb_data.model_dump(include={"price"}),
        ),
    )

    builder.button(
        text="Назад🔙",
        callback_data=PaymentCbData(action=PayActions.back).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
