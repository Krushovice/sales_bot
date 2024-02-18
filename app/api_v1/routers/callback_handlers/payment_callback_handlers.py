from aiogram import Router, F, Bot
from aiogram.enums.content_type import ContentType
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    PreCheckoutQuery,
)

from aiogram.utils import markdown


from app.api_v1.config import settings

from app.api_v1.core import AsyncOrm, Key


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
from app.api_v1.utils.request_api import outline_helper
from app.api_v1.utils.pay_helper import get_payment

router = Router(name=__name__)


@router.callback_query(AccountCbData.filter(F.action == ProfileActions.refill))
async def handle_payment_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(
        caption="💰 Укажите сумму пополнения баланса",
        reply_markup=build_payment_kb(),
    )


@router.callback_query(
    PaymentCbData.filter(
        F.action == PayActions.back_to_account,
    )
)
async def handle_back_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )
    await call.message.edit_caption(
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
    PaymentCbData.filter(F.action == PayActions.success),
)
async def handle_success_button(
    call: CallbackQuery,
):
    await call.answer()
    tg_id = call.from_user.id
    if get_payment(tg_id=tg_id):

        key = outline_helper.create_new_key(name=tg_id)
        await AsyncOrm.update_user(
            tg_id=tg_id,
            key=Key(
                name=key.name,
                value=key.access_url,
            ),
        )

        await call.message.answer(
            text=f"Подписка оплачена, вот ваш ключ: {key.access_url}",
            reply_markup=product_details_kb(
                tg_id=tg_id,
                payment_cb_data=PaymentCbData,
                success=True,
            ),
        )
    else:
        await call.message.answer(
            text="Ваша оплата не прошла, попробуйте немного позже",
            reply_markup=product_details_kb(
                tg_id=tg_id,
                payment_cb_data=PaymentCbData,
            ),
        )


@router.callback_query(
    AccountCbData.filter(
        F.action == ProfileActions.show_key,
    )
)
async def handle_show_key_button(call: CallbackQuery):
    user_key = await AsyncOrm.get_user_key(
        tg_id=call.from_user.id,
    )
    await call.answer()
    await call.message.edit_caption(
        caption=f"Ваш ключ: {user_key}",
        reply_markup=build_payment_kb(),
    )


@router.callback_query(
    ProductCbData.filter(F.action == ProductActions.details),
)
async def handle_product_actions__button(
    call: CallbackQuery,
    callback_data: ProductCbData,
):
    await call.answer()
    msg_text = markdown.text(
        markdown.hbold(f"Сумма: {callback_data.price} руб"),
        markdown.hitalic("Для оплаты перейдите по ссылке ниже"),
        sep="\n\n",
    )
    if get_payment(tg_id=call.from_user.id):
        await call.message.edit_caption(
            caption=msg_text,
            reply_markup=product_details_kb(
                tg_id=call.from_user.id,
                payment_cb_data=callback_data,
                success=True,
            ),
        )

    else:
        await call.message.edit_caption(
            caption=msg_text,
            reply_markup=product_details_kb(
                tg_id=call.from_user.id,
                payment_cb_data=callback_data,
            ),
        )


@router.callback_query(
    ProductCbData.filter(F.action == ProductActions.back_to_choice),
)
async def handle_back_to_choice_button(
    call: CallbackQuery,
):
    await call.answer()
    await call.message.edit_caption(
        caption="💰 Укажите сумму пополнения баланса",
        reply_markup=build_payment_kb(),
    )


# PRICE = LabeledPrice(label="Подписка на VPN", amount=150 * 100)


# @router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
# async def handle_pay_action_button(
#     call: CallbackQuery,
# ):
#     if settings.pay_token.split(":")[1] == "TEST":
#         await call.answer("Это тестовый платеж!")
#     await call.answer()
#     await call.bot.send_invoice(
#         call.from_user.id,
#         title="Оплата VPN",
#         description="Активация подписки",
#         provider_token=settings.pay_token,
#         currency="rub",
#         photo_url="",
#         photo_width=416,
#         photo_height=234,
#         photo_size=416,
#         is_flexible=False,
#         need_phone_number=False,
#         need_email=False,
#         need_name=False,
#         need_shipping_address=False,
#         prices=[PRICE],
#         start_parameter="subscription",
#         payload="test-invoice-payload",
#     )


# @router.pre_checkout_query(lambda query: True)
# async def handle_pre_checkout_query(
#     pre_checkout_q: PreCheckoutQuery,
#     bot: Bot,
# ):
#     await bot.answer_pre_checkout_query(
#         pre_checkout_q.id,
#         ok=True,
#     )


# @router.message(F.action == ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment(message: Message):
#     payment_info = message.successful_payment.to_python()
#     for key, value in payment_info.items():
#         print(f"{key} = {value}")
#     await message.answer(
#         (
#             f"Платеж на сумму {message.successful_payment.total_amount // 100}"
#             f"{message.successful_payment.currency} прошел успешно!"
#         )
#     )
