__all__ = ("router",)

from aiogram import Router
from .main_commands import router as main_commands_router
from .user_commands import router as user_commands_router


router = Router(name=__name__)

router.include_routers(
    main_commands_router,
    user_commands_router,
)
