from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PayActions(IntEnum):
    details = auto()
    pay = auto()
    back = auto()


class PaymentCbData(CallbackData, prefix="pay"):
    action: PayActions
    name: str


def build_payment_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for name in [
        "400р - 3мес🔸",
        "130р - 1мес🔹",
        "800р - 6мес🔻",
    ]:
        builder.button(
            text=name,
            callback_data=PaymentCbData(
                action=PayActions.details,
                name=name,
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
            **payment_cb_data.model_dump(include={"name"}),
        ),
    )

    builder.button(
        text="Назад🔙",
        callback_data=PaymentCbData(action=PayActions.back).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
