from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery

from app.api_v1.core.crud import AsyncOrm

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

from app.api_v1.utils import LEXICON_RU, payment_helper


router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.account))
async def handle_account_button(call: CallbackQuery):
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


# @router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
# async def handle_pay_button(call: CallbackQuery):
#     await call.answer()
#     payment = await payment_helper.create_payment(
#         tg_id=call.from_user.id,
#         price=150,
#     )

#     await call.message.edit_caption(
#         caption="Для оплаты VPN перейдите по ссылке:",
#         reply_markup=product_details_kb(
#             payment_cb_data=payment,
#             from_main_menu=True,
#         ),
#     )


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
async def handle_root_button(call: CallbackQuery):
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
