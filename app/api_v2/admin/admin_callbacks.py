from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from app.api_v1.orm.crud import AsyncOrm

from .admin_kb import (
    build_admin_kb,
    build_stat_kb,
    back_to_admin_panel_kb,
    AdminActions,
    AdminCbData,
)
from app.api_v1.markups import build_main_kb
from .admin_utils import show_users_statistic

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
        users = await AsyncOrm.get_users()
        data = show_users_statistic(users)
        await call.message.edit_caption(
            caption="Вы вошли в админ-панель💻\n\n"
            f"Cтатистика по пользователям на {data['today']}📊\n"
            f"Всего пользователей: {data['count_users']}\n"
            f"Кол-во новых пользователей: {data['subs_today']}\n"
            f"Кол-во активных пользователей: {data['active_users']}\n"
            f"Кол-во не активных пользователей: {data['inactive']}",
            reply_markup=build_stat_kb(),
        )
    except Exception as e:
        logger.error(f"Ошибка при переходе в админ панель: {e}")


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
        users = await AsyncOrm.get_users()
        data = show_users_statistic(users)
        await call.message.edit_caption(
            caption="Вы вошли в админ-панель💻\n\n"
            f"Cтатистика по пользователям на {data['today']}📊\n"
            f"Всего пользователей: {data['count_users']}\n"
            f"Кол-во новых пользователей: {data['subs_today']}\n"
            f"Кол-во активных пользователей: {data['active_users']}\n"
            f"Кол-во не активных пользователей: {data['inactive']}",
            reply_markup=build_stat_kb(),
        )
    except Exception as e:
        logger.error(f"Ошибка при переходе в админ панель: {e}")


@router.callback_query(
    AdminCbData.filter(
        F.action == AdminActions.statistic,
    )
)
async def handle_statistic_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(
        caption="Здесь будет больше аналитики по продажам, наверное😁"
        "Пожалуйста, не скачивайте торрент-файлы через наш VPN‼️(<i>саму ссылку на скачивание загружать можно</i>). "
        "Сервер Outline может заблокировать наш сервис за это. "
        "Cпасибо за ваше понимание и за то, что выбрали нас 🫶🏻",
        reply_markup=back_to_admin_panel_kb(),
    )
