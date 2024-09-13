__all__ = (
    "build_admin_kb",
    "build_stat_kb",
    "back_to_admin_panel_kb",
    "show_users_statistic",
    "AdminCbData",
    "AdminActions",
    "router",
)


from aiogram import Router

from .admin_kb import (
    build_admin_kb,
    build_stat_kb,
    back_to_admin_panel_kb,
    AdminCbData,
    AdminActions,
)

from .admin_callbacks import router as admin_router

from .admin_utils import show_users_statistic

router = Router(name=__name__)

router.include_router(admin_router)
