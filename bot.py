import asyncio


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.api_v1.routers import router as main_router
from app.api_v1.core import create_tables
from app.api_v1.config import settings
from app.api_v1.utils import (
    schredule_next_check,
    schredule_user_subscription_expiry,
    setup_logger,
)


async def check_users(bot: Bot):
    task1 = asyncio.create_task(schredule_next_check(bot))
    task2 = asyncio.create_task(schredule_user_subscription_expiry())
    asyncio.gather(task1, task2)
    print("All tasks completed")


async def main() -> None:
    # Конфигурируем логирование
    logger = setup_logger()
    # scheduler = AsyncIOScheduler()
    # scheduler.add()
    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    dp = Dispatcher()
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)

    # Регистриуем роутеры в диспетчере
    dp.include_router(main_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    await create_tables()
    await check_users(bot)
    # asyncio.create_task(shredule_next_check())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
