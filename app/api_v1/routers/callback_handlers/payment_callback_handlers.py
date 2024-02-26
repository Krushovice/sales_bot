from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.utils import markdown


from app.api_v1.core import AsyncOrm, Key


from app.api_v1.markups import (
    PayActions,
    PaymentCbData,
    ProductActions,
    ProductCbData,
    build_payment_kb,
    product_details_kb,
    build_account_kb,
    build_main_kb,
    get_success_pay_button,
)

from app.api_v1.utils.request_api import outline_helper
from app.api_v1.utils.yookassa_pay_helper import (
    payment_helper,
    set_expiration_date,
)

router = Router(name=__name__)


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
        caption=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"💰 Баланс: {user.balance}руб\n\n"
            f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
            f"<i>Для его пополнения используйте клавиши ниже</i>"
        ),
        reply_markup=build_account_kb(user=user),
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
    payment = await payment_helper.create_payment(
        tg_id=call.from_user.id,
        price=callback_data.price,
    )
    await call.message.edit_caption(
        caption=msg_text,
        reply_markup=product_details_kb(
            payment_cb_data=payment,
        ),
    )
    # tg_id = call.from_user.id

    # payment = get_payment(tg_id=tg_id)
    # if payment:
    #     balance = payment.balance
    #     # operation = 2 - ((2 * 3) / 100)
    #     operation = callback_data.price - ((callback_data.price * 3) / 100)
    #     if balance == operation:
    #         await call.message.edit_caption(
    #             caption="Оптатил? Жми кнопку ✅",
    #             reply_markup=get_success_pay_button(),
    #         )
    #     else:
    #         user = await AsyncOrm.get_user(tg_id=tg_id)
    #         await AsyncOrm.update_user(
    #             id=user.id,
    #             tg_id=tg_id,
    #             balance=payment.balance,
    #         )

    #         await call.message.edit_caption(
    #             caption="Недостаточно средств для оплаты подписки 😢",
    #             reply_markup=product_details_kb(
    #                 tg_id=tg_id,
    #                 pay_in=operation,
    #             ),
    #         )


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_action_button(
    call: CallbackQuery,
):

    unpacked_data = PaymentCbData().unpack(call.data)

    payment_id = unpacked_data.payment_id
    price = unpacked_data.price
    payment = await payment_helper.get_status_payment(
        payment_id=payment_id,
    )
    status = payment.status
    if status == "succeeded":
        await call.message.edit_caption(
            caption="Оптатил? Жми кнопку ✅",
            reply_markup=get_success_pay_button(
                payment_id=payment_id,
            ),
        )

    else:
        await call.message.edit_caption(
            caption="Что-то пошло не так😢",
            reply_markup=product_details_kb(
                pay_in=price,
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


@router.callback_query(
    ProductCbData.filter(F.action == ProductActions.success),
)
async def handle_success_button(
    call: CallbackQuery,
):
    unpacked_data = ProductCbData().unpack(call.data)
    payment_id = unpacked_data.payment_id

    payment = await payment_helper.get_payment(
        payment_id=payment_id,
    )

    expiration = set_expiration_date()

    await call.answer()
    tg_id = call.from_user.id

    user = await AsyncOrm.get_user(tg_id=tg_id)
    if not user.key:
        key = await outline_helper.create_new_key(name=tg_id)
        current_balance = user.balance + payment.amount.value
        await AsyncOrm.update_user(
            tg_id=tg_id,
            balance=current_balance,
            subscription=True,
            subscribe_date=payment.created_at,
            expiration_date=expiration,
            key=Key(
                api_id=key.key_id,
                name=key.name,
                user_id=user.id,
                value=key.access_url,
            ),
        )

        await call.message.edit_caption(
            caption=(f"Подписка оплачена, вот ваш ключ \n\n" f"{key.access_url}"),
            reply_markup=build_main_kb(),
        )

    else:
        user = await AsyncOrm.get_user(tg_id=tg_id)
        await outline_helper.remove_key_limit(key_id=user.key.api_id)
        await call.message.edit_caption(
            caption="Подписка оплачена, доступ не ограничен 🛜",
            reply_markup=build_account_kb(user=user),
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
