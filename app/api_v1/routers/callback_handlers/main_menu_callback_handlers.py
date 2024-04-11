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
    build_payment_kb,
    build_main_kb,
    build_questions_kb,
    build_back_info_kb,
)

from app.api_v1.utils import LEXICON_RU
from app.api_v1.utils.logging import setup_logger

router = Router(name=__name__)
logger = setup_logger(__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.account))
async def handle_account_button(call: CallbackQuery):
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
    except Exception as e:
        logger.error(f"Ошибка перехода в личный кабинет: {e}")


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=LEXICON_RU["help_info"],
        reply_markup=build_questions_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.promo))
async def handle_promo_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption="Отправьте пожалуйста в чат промокод на бесплатный 7-дневный триал 🎁",
        reply_markup=root_kb(),
    )


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_action_button(
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
            "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.questions))
async def handle_questions_button(call: CallbackQuery):
    await call.answer()
    text = LEXICON_RU["QA"]

    await call.message.edit_caption(
        caption=text,
        reply_markup=build_back_info_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.back_to_help))
async def handle_back_to_help_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(
        caption=LEXICON_RU["help_info"],
        reply_markup=build_questions_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.back_root))
async def handle_back_root_button(call: CallbackQuery):
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
