import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from aiogram.utils import markdown


from app.api_v1.orm import AsyncOrm, Key


from app.api_v1.markups import (
    PayActions,
    PaymentCbData,
    ProductActions,
    ProductCbData,
    build_payment_kb,
    product_details_kb,
    build_account_kb,
    build_main_kb,
    back_to_payment,
)


from app.api_v1.utils import (
    outline_helper,
    payment_manager,
    set_expiration_date,
    get_duration,
    get_receipt,
    generate_order_number,
    check_payment,
    check_time_delta,
)
from app.api_v1.utils.logging import setup_logger


router = Router(name=__name__)

logger = setup_logger(__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


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

    if check_time_delta(date=user.expiration_date):
        sub_info = f"Активна до {user.expiration_date}"
    else:
        sub_info = "Не активна"

    discount = user.discount if user.discount else 0
    url = markdown.hlink(
        "Ссылка",
        f"https://t.me/Real_vpnBot?start={user.tg_id}",
    )
    await call.message.edit_caption(
        caption=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"🗓 Подписка: <i>{sub_info}</i>📌\n"
            f"🎁 Скидка: <b>{discount}%</b>\n"
            f"📍Ваша реферальная ссылка: <i>{url}</i>\n\n"
            f"<i>На данной странице отображена основная информация о профиле.</i>\n"
            f"<i>Для оплаты и доступа к ключу используйте клавиши ниже⬇️</i>"
        ),
        reply_markup=build_account_kb(
            exp_date=user.expiration_date,
            is_key=True if user.key else False,
        ),
    )


@router.callback_query(
    ProductCbData.filter(F.action == ProductActions.details),
)
async def handle_product_actions__button(
    call: CallbackQuery,
    callback_data: ProductCbData,
):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )

    price = callback_data.price
    discount = user.discount if user.discount else 0
    total = int(price - (price * discount / 100))

    msg_text = markdown.text(
        markdown.hbold(f"💰 Сумма: {total} руб"),
        markdown.hitalic("Для оплаты перейдите по ссылке ниже ⬇️"),
        sep="\n\n",
    )
    try:
        payment = await payment_manager.init_payment(
            amount=total * 100,
            order_id=generate_order_number(),
            description=f"Оплата пользователя № {user.tg_id}",
            receipt=get_receipt(price=total),
        )
        if payment:
            await call.message.edit_caption(
                caption=msg_text,
                reply_markup=product_details_kb(
                    payment_cb_data=payment,
                ),
            )
        else:
            await call.message.edit_caption(
                caption="Возникла ошибка при выполнении платежа.\n"
                "Попробуйте немного позже",
                reply_markup=back_to_payment(
                    payment_data=callback_data,
                ),
            )

    except Exception as e:
        logger.error(f"Ошибка перехода к платежу: {e}. {payment}")


@router.callback_query(
    ProductCbData.filter(F.action == ProductActions.back_to_choice),
)
async def handle_back_to_choice_button(
    call: CallbackQuery,
):
    await call.answer()
    await call.message.edit_caption(
        caption="💰 Варианты оплаты подписки: ⬇️",
        reply_markup=build_payment_kb(),
    )


@router.callback_query(
    PaymentCbData.filter(F.action == PayActions.success),
)
async def handle_success_button(
    call: CallbackQuery,
    callback_data: PaymentCbData,
):

    payment_id = callback_data.payment_id
    tg_id = call.from_user.id
    try:

        user = await AsyncOrm.get_user(tg_id=tg_id)
        payment = await payment_manager.check_payment_status(
            payment_id=payment_id,
        )
        exp_date = user.expiration_date
        await call.answer()

        if payment["ErrorCode"] == "0":
            if check_payment(payment):

                payment_duration = get_duration(payment)

                expiration = set_expiration_date(
                    duration=payment_duration,
                    rest=exp_date if exp_date else None,
                )
                today = datetime.datetime.today().strftime("%d-%m-%Y")
                referrer_user = await AsyncOrm.get_referrer(tg_id=tg_id)
                if referrer_user:
                    exp_date = referrer_user.expiration_date
                    referrer_user_expiration = set_expiration_date(
                        duration=payment_duration,
                        rest=exp_date if exp_date else None,
                        is_referrer=True,
                    )
                    if referrer_user.discount == 5:
                        await AsyncOrm.update_user(
                            tg_id=referrer_user.tg_id,
                            expiration_date=referrer_user_expiration,
                        )
                    else:
                        await AsyncOrm.update_user(
                            tg_id=referrer_user.tg_id,
                            discount=5,
                            expiration_date=referrer_user_expiration,
                        )
                if not user.key:
                    key = outline_helper.create_new_key(name=tg_id)

                    await AsyncOrm.update_user(
                        tg_id=tg_id,
                        subscription=True,
                        subscribe_date=today,
                        expiration_date=expiration,
                        key=Key(
                            api_id=int(key.key_id),
                            name=key.name,
                            user_id=user.id,
                            value=key.access_url,
                        ),
                        payment=int(payment_id),
                    )

                    value = key.access_url
                    msg = ("Подписка успешно оплачена, ваш ключ\n"
                           f"📌<pre>{value}</pre>\n"
                           "Cкопируйте его ✅\n")

                    await call.message.edit_caption(
                        caption=msg,
                        reply_markup=build_account_kb(
                            exp_date=user.expiration_date,
                            is_key=True,
                        ),
                    )

                else:

                    await AsyncOrm.update_user(
                        tg_id=tg_id,
                        subscription=True,
                        expiration_date=expiration,
                        payment=int(payment_id),
                    )

                    outline_helper.remove_key_limit(key_id=user.key.api_id)
                    await call.message.edit_caption(
                        caption="Подписка оплачена, доступ не ограничен 🛜",
                        reply_markup=build_account_kb(
                            exp_date=expiration,
                            is_key=True if user.key else False,
                        ),
                    )

            else:
                await call.message.answer_photo(
                    photo=FSInputFile(
                        path=file_path,
                    ),
                    caption="Платеж вероятно всё еще обрабатывается, попробуйте\n"
                    "немного позже ⏳",
                    reply_markup=product_details_kb(
                        payment_cb_data=payment,
                        success=True,
                    ),
                )
        else:
            price = callback_data.price
            discount = user.discount if user.discount else 0
            total = int(price - (price * discount / 100))
            payment = await payment_manager.init_payment(
                amount=total * 100,
                order_id=generate_order_number(),
                description=f"Оплата пользователя № {tg_id}",
                receipt=get_receipt(price=price),
            )
            await call.message.edit_caption(
                caption="Возникла ошибка при выполнении платежа,\n"
                "Попробуйте немного позже",
                reply_markup=product_details_kb(
                    payment_cb_data=payment,
                ),
            )
    except Exception as e:
        logger.error(f"Ошибка проверки платежа пользователя {tg_id}: {e}")


@router.callback_query(
    ProductCbData.filter(
        F.action == ProductActions.back_to_root,
    )
)
async def handle_root_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=markdown.hbold(
            "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
            "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
            "🔥  Твой личный VPN по самой низкой цене\n\n"
            "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )
