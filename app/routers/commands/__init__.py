__all__ = ('router',
           )

from aiogram import Router
from .main_commands import router as main_commands_router


router = Router(name=__name__)

router.include_router(main_commands_router)
