from aiogram import Router, F
from aiogram.types import CallbackQuery


from app.api_v1.orm.crud import AsyncOrm

from app.api_v1.markups import (
    ProfileActions,
    ProfileCbData,
    back_to_key_kb,
    build_payment_kb,
    help_kb,
)

from app.api_v1.utils import (
    LEXICON_RU,
    setup_logger,
)

router = Router(name=__name__)

logger = setup_logger(__name__)


@router.callback_query(ProfileCbData.filter(F.action == ProfileActions.refill))
async def handle_payment_button(call: CallbackQuery):
    await call.answer()
    try:

        user = await AsyncOrm.get_user(
            tg_id=call.from_user.id,
        )
        subscribe = user.expiration_date
        if subscribe:
            sub_info = f"Активна до {subscribe}"
        else:
            sub_info = "Не активна"

        await call.message.edit_caption(
            caption=(
                f"Ваша подписка: <i>{sub_info}</i>🗓\n"
                f"Когда ваш реферал оплачивает подписку, вы получаете бонусные дни. "
                f"Подробности тут /partners.\n"
                f"Выберите вариант продления подписки: ⬇️"
            ),
            reply_markup=build_payment_kb(),
        )
    except Exception as e:
        logger.error(f"Ошибка прехода к вариантам оплаты: {e}")


@router.callback_query(
    ProfileCbData.filter(F.action == ProfileActions.renewal),
)
async def handle_renewal_button(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.edit_caption(
            caption="💰 Варианты оплаты подписки: ⬇️",
            reply_markup=build_payment_kb(discount=True),
        )
    except Exception as e:
        logger.error(f"Ошибка перехода к оплате: {e}")


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
            key = user.key.value

            await call.message.edit_caption(
                caption=(f"Ваш ключ: 📌<code>{key}</code>\n\nСкопируйте его ☑️"),
                reply_markup=help_kb(),
            )

        except Exception as e:
            logger.error(f"Ошибка обработки кнопки доступа к ключу: {e}")


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
        key = user.key.value
        try:

            await call.message.edit_caption(
                caption=f"Ваш ключ: 📌<code>{key}</code>\n\nСкопируйте его ☑️",
                reply_markup=help_kb(),
            )

        except Exception as e:
            logger.error(f"У данного пользователя отсутствует ключ, {e}")
