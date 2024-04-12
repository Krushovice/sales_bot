import asyncio
import datetime


from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils import markdown


from app.api_v1.orm import AsyncOrm

from app.api_v1.utils.tools import send_logs_email

from app.api_v1.utils.logging import setup_logger
from . import outline_helper


from app.api_v1.markups import build_renewal_kb


file_path = "app/api_v1/utils/images/image2.jpg"

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
        current_date = datetime.datetime.now()

        for user in users:
            expiration_date = user.expiration_date
            if expiration_date is not None:
                # Преобразуем строку expiration_date в объект datetime для сравнения
                expiration_date = datetime.datetime.strptime(
                    expiration_date, "%d-%m-%Y"
                )

                if current_date > expiration_date:
                    if user.key:
                        outline_helper.set_key_limit(key_id=user.key.api_id)
            else:
                # Если expiration_date равен None, пропускаем этого пользователя
                logger.info(f"User {user.id} has no subscription expiration date set.")

    except Exception as e:
        error_msg = f"An error occurred in check_subscription_expiry: {e}"
        logger.error(error_msg)


async def schedule_next_check(bot: Bot):
    while True:
        await check_subscription_expiry()
        await send_subscription_reminder(bot)
        await send_logs_email()
        await asyncio.sleep(24 * 3600)


async def schedule_next_reminder(bot: Bot):
    while True:
        await send_reminder_for_inactive(bot)
        await asyncio.sleep(72 * 3600)


async def send_subscription_reminder(bot: Bot) -> None:
    users = await AsyncOrm.get_users_by_subscription()
    for user in users:
        try:
            tg_id = user.tg_id
            if await check_user_expiration(user):
                await bot.send_photo(
                    photo=FSInputFile(
                        path=file_path,
                    ),
                    chat_id=tg_id,
                    caption=(
                        "Привет! Напоминаю, что твоя подписка скоро закончится👋\n"
                        "Не забудь пожалуйста произвести оплату, чтобы продолжить пользоваться VPN✅"
                    ),
                    reply_markup=build_renewal_kb(),
                )
            else:
                await bot.send_photo(
                    photo=FSInputFile(
                        path=file_path,
                    ),
                    chat_id=tg_id,
                    caption=(
                        f"Привет! Твоя подписка закончилась {user.expiration_date}😢\n"
                        "Чтобы возобновить работу VPN, необходимо продлить подписку✅"
                    ),
                    reply_markup=build_renewal_kb(),
                )
        except TelegramBadRequest as e:
            error_msg = f"Ошибка при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)


async def send_reminder_for_inactive(bot: Bot) -> None:
    users = await AsyncOrm.get_inactive_users()

    text = (
        "Привет 👋\n"
        "Вижу, вы так и не воспользовались нашим VPN 😔\n"
        f"Ниже я оставлю инструкцию по подключению, а это - <code>REALVPN2024CPG</code> промокод на бесплатные 7 дней 🎁 "
        "Отправьте его мне.\nНажмите <b>Подключить со скидкой</b>, если готовы оплатить подписку, для вас действует "
        "единоразовая скидка в 5%."
    )
    for user in users:

        await bot.send_photo(
            photo=FSInputFile(
                path=file_path,
            ),
            chat_id=user.tg_id,
            caption=text,
            reply_markup=build_renewal_kb(need_help=True),
        )
