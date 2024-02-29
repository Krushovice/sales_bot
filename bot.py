import asyncio

import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.api_v1.routers import router as main_router
from app.api_v1.core import create_tables
from app.api_v1.config import settings
from app.api_v1.utils import shredule_next_check


logger = logging.getLogger(__name__)


async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    # Добавляем обработчик для записи в файл
    file_handler = RotatingFileHandler("app.log", maxBytes=100000, backupCount=5)
    file_handler.setFormatter(
        logging.Formatter(
            "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
        )
    )
    logger.addHandler(file_handler)

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
    asyncio.create_task(shredule_next_check())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
