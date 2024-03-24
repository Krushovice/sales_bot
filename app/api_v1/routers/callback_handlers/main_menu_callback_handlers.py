import datetime
from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery

from app.api_v1.orm.crud import AsyncOrm

from app.api_v1.markups import (
    MenuActions,
    MenuCbData,
    ProfileActions,
    ProfileCbData,
    PayActions,
    PaymentCbData,
    build_account_kb,
    root_kb,
    build_main_kb,
    product_details_kb,
)

from app.api_v1.utils import (
    payment_manager,
    get_receipt,
    generate_order_number,
    LEXICON_RU,
    check_payment,
    get_user_info,
)


router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.account))
async def handle_account_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )

    user_info = get_user_info(user)

    await call.message.edit_caption(
        caption=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"🗓 Подписка: {user_info['sub_info']}\n\n"
            f"🎁 <b>Скидка:</b> {user_info['discount']}\n\n"
            f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
            f"<i>Для его пополнения используйте клавиши ниже</i>"
        ),
        reply_markup=build_account_kb(user=user),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=LEXICON_RU["help_info"],
        reply_markup=root_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.promo))
async def handle_promo_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption="Введите пожалуйста промокод на бесплатный 7-дневный триал 🎁",
        reply_markup=root_kb(),
    )


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_action_button(
    call: CallbackQuery,
):

    await call.answer()
    msg_text = markdown.text(
        markdown.hbold("Сумма: 150 руб"),
        markdown.hitalic("Для оплаты перейдите по ссылке ниже"),
        sep="\n\n",
    )
    payment = await payment_manager.init_payment(
        amount=15000,
        order_id=generate_order_number(),
        description=f"Оплата пользователя №{call.from_user.id}",
        receipt=get_receipt(price=150),
    )
    is_payment = check_payment(payment)
    await call.message.edit_caption(
        caption=msg_text,
        reply_markup=product_details_kb(
            payment_cb_data=payment,
            from_main_menu=True,
            success=True if is_payment else False,
        ),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.advantage))
async def handle_advantage_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=LEXICON_RU["advantage"],
        reply_markup=root_kb(),
    )


@router.callback_query(
    ProfileCbData.filter(
        F.action == ProfileActions.back_to_main,
    )
)
async def handle_back_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=markdown.hbold(
            "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
            "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
            "🔥  Твой личный VPN по самой низкой цене\n\n"
            "💰  Цена: 1̶9̶9̶руб 💥129 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )
