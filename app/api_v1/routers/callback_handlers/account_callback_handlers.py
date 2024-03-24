from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.utils import markdown
from app.api_v1.orm.crud import AsyncOrm

from app.api_v1.markups import (
    ProfileActions,
    ProfileCbData,
    back_to_key_kb,
    build_payment_kb,
    help_kb,
)

from app.api_v1.utils import LEXICON_RU
from app.api_v1.utils.logging import setup_logger

router = Router(name=__name__)

logger = setup_logger(__name__)


@router.callback_query(ProfileCbData.filter(F.action == ProfileActions.refill))
async def handle_payment_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )
    await call.message.edit_caption(
        caption=(
            f"Ваш баланс: {user.balance}\n\n" "Укажите сумму пополнения баланса💰"
        ),
        reply_markup=build_payment_kb(),
    )


@router.callback_query(ProfileCbData.filter(F.action == ProfileActions.renewal))
async def handle_renewal_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(
        caption="💰 Укажите сумму пополнения баланса",
        reply_markup=build_payment_kb(),
    )


@router.callback_query(
    ProfileCbData.filter(
        F.action == ProfileActions.show_key,
    )
)
async def handle_show_key_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )
    if user.key:
        try:

            await call.message.edit_caption(
                caption=(f"Ваш ключ: <b>{user.key.value}<b>\n\nСкопируйте его ☑️"),
                reply_markup=help_kb(),
            )

        except Exception as e:
            logger.error(f"У данного пользователя отсутствует ключ, {e}")


@router.callback_query(
    ProfileCbData.filter(
        F.action == ProfileActions.tutorial,
    )
)
async def handle_help_button(call: CallbackQuery):
    await call.answer()
    text = LEXICON_RU["tutorial"]
    await call.message.edit_caption(
        caption=text,
        reply_markup=back_to_key_kb(),
    )


@router.callback_query(
    ProfileCbData.filter(
        F.action == ProfileActions.back_to_key,
    )
)
async def handle_back_to_key_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )
    if user.key:
        try:

            await call.message.edit_caption(
                caption=markdown.hbold(
                    f"Ваш ключ: {user.key.value}\n\nСкопируйте его ☑️"
                ),
                reply_markup=help_kb(),
            )

        except Exception as e:
            logger.error(f"У данного пользователя отсутствует ключ, {e}")
