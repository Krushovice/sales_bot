from aiogram import Router
from .payment_callback_handlers import router as payment_router
from .main_menu_callback_handlers import router as main_menu_router
from .account_callback_handlers import router as account_router

router = Router(name=__name__)
router.include_routers(
    payment_router,
    main_menu_router,
    account_router,
)
