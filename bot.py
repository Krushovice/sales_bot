import asyncio
import logging
import sys
from app.config import settings

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
# from bot.core.models.orm import AsyncOrm
from app.routers import router as main_router

# Bot token can be obtained via https://t.me/BotFather
logger = logging.getLogger(__name__)


async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    dp = Dispatcher()
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    # Регистриуем роутеры в диспетчере
    dp.include_router(main_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.session.close()
    # await AsyncOrm.create_tables()
    await dp.start_polling(bot)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


if __name__ == "__main__":
    asyncio.run(main())
