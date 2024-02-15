from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from app.api_v1.core.crud import AsyncOrm

from app.api_v1.markups import (
    MenuActions,
    MenuCbData,
    ProfileActions,
    AccountCbData,
    PayActions,
    PaymentCbData,
)
from app.api_v1.markups import (
    build_account_kb,
    root_kb,
    build_main_kb,
    build_pay_button,
)
from app.api_v1.utils.lexicon import LEXICON_RU


router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.account))
async def handle_account_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
        username=call.from_user.username,
    )

    await call.message.edit_text(
        text=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"💰 Баланс: {user.balance}руб\n\n"
            f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
            f"<i>Для его пополнения используйте клавиши ниже</i>"
        ),
        reply_markup=build_account_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_text(
        text=LEXICON_RU["help_info"],
        reply_markup=root_kb(),
    )


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_text(
        text="Для оплаты VPN перейдите по ссылке:",
        reply_markup=build_pay_button(
            tg_id=call.from_user.id,
        ),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.advantage))
async def handle_advantage_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_text(
        text="Почему мы?",
        reply_markup=root_kb(),
    )


@router.callback_query(AccountCbData.filter(F.action == ProfileActions.back))
async def handle_root_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_text(
        text=markdown.hbold(
            "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
            "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
            "🔥  Твой личный VPN по самой низкой цене\n\n"
            "💰  Цена: 1̶9̶9̶руб 💥129 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )
