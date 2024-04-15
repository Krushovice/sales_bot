import asyncio


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


from app.api_v1.routers import router as main_router
from app.api_v1.admin import router as admin_router
from app.api_v1.orm import create_tables
from app.api_v1.config import settings
from app.api_v1.utils import (
    schedule_next_check,
    schedule_next_reminder,
    setup_logger,
)


async def check_users(bot: Bot):
    task1 = asyncio.create_task(schedule_next_check())
    task2 = asyncio.create_task(schedule_next_reminder(bot))
    asyncio.gather(task1, task2)


async def main() -> None:
    try:  # Конфигурируем логирование
        logger = setup_logger(__name__)

        dp = Dispatcher()
        bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
        # Регистриуем роутеры в диспетчере
        dp.include_routers(
            main_router,
            admin_router,
        )

        # Пропускаем накопившиеся апдейты и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.session.close()
        await create_tables()
        await check_users(bot)

        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Ошибка при запуске основного скрипта: {e}")


if __name__ == "__main__":
    asyncio.run(main())
