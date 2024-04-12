import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from app.api_v1.orm.crud import AsyncOrm

from app.api_v1.admin import (
    build_admin_kb,
    build_stat_kb,
    back_to_admin_panel_kb,
    AdminActions,
    AdminCbData,
)
from app.api_v1.markups import build_main_kb

from app.api_v1.utils.logging import setup_logger

router = Router(name=__name__)

logger = setup_logger(__name__)


@router.callback_query(
    AdminCbData.filter(
        F.action == AdminActions.admin_panel,
    )
)
async def handle_admin_button(call: CallbackQuery):
    await call.answer()

    try:
        await call.message.edit_caption(
            caption="<b>Вы вошли в админ-панель</b>💻\n\n"
            f"Сервер работает {1} часов с последнего бэкапа\n"
            f"Файл логов за последние сутки {1}",
            reply_markup=build_stat_kb(),
        )
    except Exception as e:
        logger.error(f"Ошибка при переходе в админ панель: {e}")


@router.callback_query(AdminCbData.filter(F.action == AdminActions.statistic))
async def handle_stat_button(call: CallbackQuery):
    await call.answer()
    try:
        users = await AsyncOrm.get_users()

        today = datetime.datetime.now()
        count_users = len(users)
        active_users = 0
        subs_today = 0
        count_inactive = 0
        for user in users:
            if user.subscription:
                active_users += 1
                sub_date = datetime.datetime.strptime(
                    user.subscribe_date,
                    "%d-%m-%Y",
                )
                if sub_date == today:
                    subs_today += 1
            if not user.key:
                count_inactive += 1

        await call.message.edit_caption(
            caption=f"Cтатистика по пользователям на {today.strftime('%d-%m-%Y')}📊\n"
            f"Всего пользователей: {count_users}\n"
            f"Кол-во новых пользователей: {subs_today}\n"
            f"Кол-во активных пользователей: {active_users}\n"
            f"Кол-во не активных пользователей: {count_inactive}",
            reply_markup=back_to_admin_panel_kb(),
        )
    except Exception as e:
        logger.error(f"Ошибка при переходе к статистике: {e}")


@router.callback_query(
    AdminCbData.filter(
        F.action == AdminActions.back_to_main,
    )
)
async def handle_back_to_main_button(call: CallbackQuery):
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


@router.callback_query(
    AdminCbData.filter(
        F.action == AdminActions.back_to_root_panel,
    )
)
async def handle_root_panel_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(
        caption="Личный кабинет администратора 🥸",
        reply_markup=build_admin_kb(),
    )


@router.callback_query(
    AdminCbData.filter(
        F.action == AdminActions.back_root_admin,
    )
)
async def handle_back_to_admin_button(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.edit_caption(
            caption="<b>Вы вошли в админ-панель</b>💻\n\n"
            f"Сервер работает {1} часов с последнего бэкапа\n"
            f"Файл логов за последние сутки: {logs}",
            reply_markup=build_stat_kb(),
        )
    except Exception as e:
        logger.error(f"Ошибка при переходе в админ панель: {e}")
