import asyncio
import datetime


from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramBadRequest


from app.api_v1.orm import AsyncOrm

from app.api_v1.utils.tools import send_logs_email

from app.api_v1.utils.logging import setup_logger
from . import outline_helper


from app.api_v1.markups import build_renewal_kb

file_path1 = "app/api_v1/utils/images/image1.jpg"
file_path2 = "app/api_v1/utils/images/image2.jpg"

logger = setup_logger(__name__)


async def check_user_expiration(user):
    current_date = datetime.datetime.now()
    expiration_date = datetime.datetime.strptime(
        user.expiration_date,
        "%d-%m-%Y",
    )
    delta = expiration_date - current_date
    if 0 < delta.days <= 3:
        return True
    return False


async def check_subscription_expiry():
    try:
        users = await AsyncOrm.get_users_by_subscription()
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")

        for user in users:
            if current_date > user.expiration_date:
                if user.key:
                    outline_helper.set_key_limit(key_id=user.key.api_id)

    except Exception as e:
        error_msg = f"An error occurred in check_subscription_expiry: {e}"
        logger.error(error_msg)


async def schedule_next_check():
    while True:
        await check_subscription_expiry()
        await send_logs_email()
        await asyncio.sleep(24 * 3600)


async def schedule_next_reminder(bot: Bot):
    while True:
        await send_subscription_reminder(bot)
        await send_reminder_for_inactive(bot)
        await asyncio.sleep(72 * 3600)


async def send_subscription_reminder(bot: Bot) -> None:
    users = await AsyncOrm.get_users_by_subscription()
    for user in users:
        try:
            if await check_user_expiration(user):
                tg_id = user.tg_id
                await bot.send_photo(
                    photo=FSInputFile(
                        path=file_path2,
                    ),
                    chat_id=tg_id,
                    caption=(
                        "Привет! Напоминаю, что твоя подписка скоро закончится👋\n"
                        "Не забудь пожалуйста пополнить баланс, чтобы продолжить пользоваться VPN✅"
                    ),
                    reply_markup=build_renewal_kb(),
                )
        except TelegramBadRequest as e:
            error_msg = f"Ошибка при отправке сообщения пользователю {user.tg_id}: {e}"
            logger.error(error_msg)


async def send_reminder_for_inactive(bot: Bot) -> None:
    users = await AsyncOrm.get_inactive_users()
    for user in users:
        text = (
            "Привет 👋\n"
            "Вижу, вы так и не воспользовались нашим VPN 😔\n"
            "Ниже я оставлю инструкцию по подключению и промокод на бесплатные 7 дней 🎁\n"
            "Для подключения нажмите <b>Подключить со скидкой</b>"
        )
        await bot.send_photo(
            photo=FSInputFile(
                path=file_path1,
            ),
            chat_id=user.tg_id,
            caption=text,
            reply_markup=build_renewal_kb(need_help=True),
        )
