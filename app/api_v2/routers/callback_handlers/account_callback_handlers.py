from aiogram import Router, F
from aiogram.types import CallbackQuery


from app.api_v1.orm.crud import AsyncOrm

from app.api_v1.markups import (
    ProfileActions,
    ProfileCbData,
    build_payment_kb,
)

from app.api_v1.utils import (
    LEXICON_RU,
    setup_logger,
    check_time_delta,
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
        if check_time_delta(subscribe):
            sub_info = str(subscribe)
        else:
            sub_info = "Не активна"

        await call.message.edit_caption(
            caption=(
                f"Ваша подписка: <i>{sub_info}</i>🗓\n\n"
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
