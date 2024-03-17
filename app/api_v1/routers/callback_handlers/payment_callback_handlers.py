import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

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


from app.api_v1.utils import (
    outline_helper,
    payment_manager,
    set_expiration_date,
    get_duration,
    get_receipt,
    generate_order_number,
    create_token,
)
from app.api_v1.utils.logging import setup_logger


router = Router(name=__name__)

logger = setup_logger(__name__)


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
    try:
        payment = await payment_manager.init_payment(
            amount=callback_data.price * 100,
            order_id=generate_order_number(),
            description=f"Оплата пользователя № {call.from_user.id}",
            receipt=get_receipt(price=callback_data.price),
        )
        await call.message.edit_caption(
            caption=msg_text,
            reply_markup=product_details_kb(
                payment_cb_data=payment,
            ),
        )

    except Exception as e:
        logger.error(f"Ошибка перехода к платежу: {e}")


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_action_button(
    call: CallbackQuery,
    callback_data: PaymentCbData,
):

    await call.answer()
    price = callback_data.price
    msg_text = markdown.text(
        markdown.hbold("Сумма: 150 руб"),
        markdown.hitalic("Для оплаты перейдите по ссылке ниже"),
        sep="\n\n",
    )
    payment = await payment_manager.init_payment(
        amount=price * 100,
        order_id=generate_order_number(),
        description=f"Оплата пользователя № {call.from_user.id}",
        receipt=get_receipt(price=price),
    )
    await call.message.edit_caption(
        caption=msg_text,
        reply_markup=product_details_kb(
            payment_cb_data=payment,
            from_main_menu=True,
        ),
    )
    # payment_id = callback_data["PaymentId"]
    # await call.message.answer_photo(
    #     photo=FSInputFile(
    #         path=file_path,
    #     ),
    #     caption="Оптатил? Жми кнопку ✅",
    #     reply_markup=get_success_pay_button(
    #         payment_id=payment_id,
    #     ),
    # )
    # try:
    #     payment_id = callback_data["PaymentId"]
    #     price = callback_data.price
    #     token = create_token(payment_id=payment_id)
    #     payment = await payment_manager.check_payment_status(
    #         payment_id=payment_id,
    #         token=token,
    #     )
    #     print(payment)
    #     if payment:
    #         if payment["Success"]:

    #             await call.message.edit_caption(
    #                 caption="Оптатил? Жми кнопку ✅",
    #                 reply_markup=get_success_pay_button(
    #                     payment_id=payment_id,
    #                 ),
    #             )

    #         else:

    #             await call.message.edit_caption(
    #                 caption="Что-то пошло не так😢",
    #                 reply_markup=product_details_kb(
    #                     payment_cb_data=payment,
    #                 ),
    #             )

    #     else:
    #         msg_text = markdown.text(
    #             markdown.hbold("Сумма: 150 руб"),
    #             markdown.hitalic("Для оплаты перейдите по ссылке ниже"),
    #             sep="\n\n",
    #         )
    #         payment = await payment_manager.init_payment(
    #             amount=price * 100,
    #             order_id=generate_order_number(),
    #             description=f"Оплата пользователя № {call.from_user.id}",
    #             receipt=get_receipt(price=price),
    #         )
    #         await call.message.edit_caption(
    #             caption=msg_text,
    #             reply_markup=product_details_kb(
    #                 payment_cb_data=payment,
    #                 from_main_menu=True,
    #             ),
    #         )
    # except Exception as e:
    #     logger.error(f"Error creating payment: {e}")


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
    PaymentCbData.filter(F.action == PayActions.success),
)
async def handle_success_button(
    call: CallbackQuery,
    callback_data: PaymentCbData,
):
    try:
        payment_id = callback_data.payment_id

        token = create_token(payment_id=str(payment_id))
        payment = await payment_manager.check_payment_status(
            payment_id=payment_id,
            token=token,
        )
        await call.answer()
        if payment["Status"] == "CONFIRMED":
            payment_duration = get_duration(payment)
            expiration = set_expiration_date(payment_duration)

            tg_id = call.from_user.id
            pay_amount = int(payment["Amount"]) / 100

            user = await AsyncOrm.get_user(tg_id=tg_id)
            if not user.key:
                key = await outline_helper.create_new_key(name=tg_id)
                current_balance = user.balance + pay_amount
                await AsyncOrm.update_user(
                    tg_id=tg_id,
                    balance=current_balance,
                    subscription=True,
                    subscribe_date=datetime.datetime.today().strftime("%d-%m-%Y"),
                    expiration_date=expiration,
                    key=Key(
                        api_id=int(key.key_id),
                        name=key.name,
                        user_id=user.id,
                        value=key.access_url,
                    ),
                )
                msg = markdown.hbold(
                    f"Подписка оплачена, вот ваш ключ \n\n" f"{key.access_url}"
                )
                await call.message.edit_caption(
                    caption=msg,
                    reply_markup=build_account_kb(user=user),
                )

            else:
                user = await AsyncOrm.get_user(tg_id=tg_id)
                await outline_helper.remove_key_limit(key_id=user.key.api_id)
                await call.message.edit_caption(
                    caption="Подписка оплачена, доступ не ограничен 🛜",
                    reply_markup=build_account_kb(user=user),
                )

        else:
            await call.message.edit_caption(
                caption="Платеж вероятно всё еще обрабатывается.\n\n"
                "Попробуйте немного позже",
                reply_markup=product_details_kb(
                    payment_cb_data=payment,
                ),
            )

    except Exception as e:
        logger.error(f"Error creating payment: {e}")


#
