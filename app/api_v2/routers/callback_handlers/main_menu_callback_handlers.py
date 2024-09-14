from datetime import datetime

from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from app.api_v1.config import settings
from app.api_v1.orm.crud import AsyncOrm

from app.api_v2.markups import (
    MenuActions,
    MenuCbData,
    PayActions,
    PaymentCbData,
    root_kb,
    build_payment_kb,
    build_next_kb,
    build_main_kb,
)

from app.api_v1.utils import LEXICON_RU, check_time_delta
from app.api_v1.utils.logging import setup_logger

router = Router(name=__name__)
logger = setup_logger(__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.promo))
async def handle_promo_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption="Отправьте пожалуйста в чат промокод на бесплатный 7-дневный триал 🎁",
        reply_markup=root_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.next))
async def handle_next_button(
    call: CallbackQuery,
):
    try:
        await call.answer()
        await call.message.edit_caption(
            caption="💰 Варианты оплаты подписки: ⬇️",
            reply_markup=build_payment_kb(),
        )

    except Exception as e:
        logger.error(f"Ошибка оплаты: {e}")


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_action_button(
    call: CallbackQuery,
):
    try:
        await call.answer()
        await call.message.edit_caption(
            caption=(
                "Отлично! Давайте для начала скачаем приложение Outline❇️ из AppStore или Google Play, "
                "в зависимости от вашей платформы📱. "
                "Как только скачаете, переходите к оплате по кнопке ниже💲"
            ),
            reply_markup=build_next_kb(),
        )

    except Exception as e:
        logger.error(f"Ошибка оплаты: {e}")


@router.callback_query(MenuCbData.filter(F.action == MenuActions.back_root))
async def handle_back_root_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(tg_id=call.from_user.id)
    if check_time_delta(date=user.expiration_date):
        sub_info = f"Активна до {user.expiration_date} ✅"
    else:
        sub_info = "Не активна ⛔️"
    sub = True if user.subscription else False
    is_admin = True if user.tg_id == int(settings.ADMIN_ID) else False
    await call.message.edit_caption(
        caption=markdown.hbold(
            "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
            "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
            "🔥  Твой личный VPN по самой низкой цене\n\n"
            "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес\n\n",
            f"Ваша подписка: {sub_info}\n\n",
        ),
        reply_markup=build_main_kb(
            subscribe=sub,
            admin=is_admin,
        ),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=LEXICON_RU["help_info"],
        reply_markup=root_kb(),
    )


@router.callback_query(
    MenuCbData.filter(
        F.action == MenuActions.key,
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
                caption=(f"Ваш ключ: 📌<pre>{key}</pre>\n\nСкопируйте его ☑️"),
                reply_markup=root_kb(),
            )

        except Exception as e:
            logger.error(f"Ошибка обработки кнопки доступа к ключу: {e}")
