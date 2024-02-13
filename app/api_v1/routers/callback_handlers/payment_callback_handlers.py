from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from app.api_v1.core.crud import AsyncOrm

from app.api_v1.markups import (
    ProfileActions,
    AccountCbData,
    PayActions,
    PaymentCbData,
    ProductActions,
    ProductCbData,
    build_payment_kb,
    product_details_kb,
    build_account_kb,
)

router = Router(name=__name__)


@router.callback_query(AccountCbData.filter(F.action == ProfileActions.refill))
async def handle_payment_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        text="💰 Укажите сумму пополнения баланса",
        reply_markup=build_payment_kb(),
    )


@router.callback_query(PaymentCbData.filter(F.action == PayActions.back))
async def handle_back_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
        username=call.from_user.username,
    )
    await call.message.edit_text(
        (
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"💰 Баланс: {user.balance}руб\n\n"
            f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
            f"<i>Для его пополнения используйте клавиши ниже</i>"
        ),
        reply_markup=build_account_kb(),
    )


@router.callback_query(
    ProductCbData.filter(F.action == ProductActions.details),
)
async def handle_product_actions__button(
    call: CallbackQuery, callback_data: ProductCbData
):
    await call.answer()
    msg_text = markdown.text(
        markdown.hbold(f"Сумма: {callback_data.price} руб"),
        markdown.hbold("Для оплаты перейдите по ссылке ниже"),
        sep="\n\n",
    )
    await call.message.edit_text(
        text=msg_text,
        reply_markup=product_details_kb(callback_data),
    )


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_action__button(call: CallbackQuery):
    pass
