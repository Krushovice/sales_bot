import asyncio
import datetime


from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError


from app.api_v1.orm import AsyncOrm, User

from app.api_v1.utils.tools import send_logs_email

from app.api_v1.utils.logging import setup_logger
from . import outline_helper


from app.api_v2.markups import build_payment_kb


file_path = "app/api_v1/utils/images/image2.jpg"

logger = setup_logger(__name__)


def check_user_expiration(user: User) -> bool:
    if user.expiration_date:
        current_date = datetime.datetime.now().date()
        expiration_date = datetime.datetime.strptime(
            user.expiration_date,
            "%d-%m-%Y",
        ).date()
        delta = expiration_date - current_date
        if 0 < delta.days <= 3:
            return True
    return False


def check_user_for_sub_ended(user: User) -> bool:
    if user.expiration_date:
        current_date = datetime.datetime.now().date()
        expiration_date = datetime.datetime.strptime(
            user.expiration_date,
            "%d-%m-%Y",
        ).date()
        delta = expiration_date - current_date
        if -10 < delta.days < 0:
            return True
    return False


async def check_subscription_expiry():
    try:
        users = await AsyncOrm.get_users_by_subscription()
        current_date = datetime.datetime.now().date()

        for user in users:
            expiration_date = user.expiration_date
            if expiration_date is not None:
                # Преобразуем строку expiration_date в объект datetime для сравнения
                expiration_date = datetime.datetime.strptime(
                    expiration_date, "%d-%m-%Y"
                ).date()

                if current_date > expiration_date:
                    if user.key:
                        await AsyncOrm.update_user(
                            tg_id=user.tg_id,
                            subscription=False,
                        )
                        outline_helper.set_key_limit(key_id=user.key.api_id)
            else:
                # Если expiration_date равен None, пропускаем этого пользователя
                logger.error(f"User {user.id} has no subscription expiration date set.")

    except Exception as e:
        error_msg = f"An error occurred in check_subscription_expiry: {e}"
        logger.error(error_msg)


async def send_subscription_reminder(bot: Bot) -> None:
    users = await AsyncOrm.get_users_by_subscription()
    for user in users:
        tg_id = user.tg_id
        try:
            if check_user_expiration(user):
                await bot.send_photo(
                    photo=FSInputFile(
                        path=file_path,
                    ),
                    chat_id=tg_id,
                    caption=(
                        f"Привет! Напоминаю, что твоя подписка закончится {user.expiration_date}👋\n"
                        "Не забудь пожалуйста произвести оплату, чтобы продолжить пользоваться VPN✅"
                    ),
                    reply_markup=build_payment_kb(),
                )

        except TelegramAPIError as e:
            error_msg = f"Ошибка при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)

        except Exception as e:
            # Обработка других неожиданных исключений
            error_msg = f"Необработанное исключение при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)


async def weed_out_active_users(bot: Bot) -> None:
    users = await AsyncOrm.get_users()
    for user in users:
        try:
            tg_id = user.tg_id
            if check_user_for_sub_ended(user):
                await bot.send_photo(
                    photo=FSInputFile(
                        path=file_path,
                    ),
                    chat_id=tg_id,
                    caption=(
                        f"Привет! Ваша подписка закончилась {user.expiration_date}😢\n"
                        "Произведите оплату, чтобы возобновить работу VPN✅"
                    ),
                    reply_markup=build_payment_kb(),
                )

        except TelegramForbiddenError as e:
            # Обработка исключения TelegramForbiddenError (пользователь заблокировал бота)
            error_msg = f"Пользователь {tg_id} заблокировал бота: {e}"
            logger.warning(error_msg)

        except TelegramAPIError as e:
            # Обработка других исключений API Telegram
            error_msg = f"Ошибка при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)

        except Exception as e:
            # Обработка других неожиданных исключений
            error_msg = f"Необработанное исключение при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)


async def send_reminder_for_inactive(bot: Bot) -> None:
    users = await AsyncOrm.get_users()

    text = (
        "Чтобы активировать новое меню, отправьте в чат команду /start. Старые сообщения стали не активными"
    )
    for user in users:
        tg_id = user.tg_id

        try:

            await bot.send_photo(
                photo=FSInputFile(
                    path=file_path,
                ),
                chat_id=tg_id,
                caption=text,
            )

        except TelegramForbiddenError as e:
            error_msg = f"Пользователь {tg_id} заблокировал бота: {e}"
            logger.error(error_msg)
            await AsyncOrm.delete_user(tg_id=tg_id)

        except TelegramAPIError as e:
            # Обработка других исключений API Telegram
            error_msg = f"Ошибка при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)

        except Exception as e:
            # Обработка других неожиданных исключений
            error_msg = f"Необработанное исключение при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)


async def send_youtube_message(bot: Bot) -> None:
    users = await AsyncOrm.get_inactive_users()
    for user in users:
        tg_id = user.tg_id
        try:
            await bot.send_photo(
                photo=FSInputFile(
                    path=file_path,
                ),
                chat_id=tg_id,
                caption="Не работает или тормозит Youtube? Ты знаешь что делать✅",
                reply_markup=build_payment_kb(),
            )

        except TelegramForbiddenError as e:
            # Обработка исключения TelegramForbiddenError (пользователь заблокировал бота)
            error_msg = f"Пользователь {tg_id} заблокировал бота: {e}"
            logger.warning(error_msg)

        except TelegramAPIError as e:
            # Обработка других исключений API Telegram
            error_msg = f"Ошибка при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)

        except Exception as e:
            # Обработка других неожиданных исключений
            error_msg = f"Необработанное исключение при отправке сообщения пользователю {tg_id}: {e}"
            logger.error(error_msg)



async def schedule_next_check():
    while True:
        try:
            await check_subscription_expiry()
            await send_logs_email()
        except Exception as e:
            logger.error(f"Ошибка в schedule_next_check: {e}")
        await asyncio.sleep(24 * 3600)

async def schedule_next_reminder(bot: Bot):
    while True:
        try:
            await weed_out_active_users(bot)
        except Exception as e:
            logger.error(f"Ошибка в schedule_next_reminder: {e}")
        await asyncio.sleep(168 * 3600)

async def schedule_reminder_to_inactive(bot: Bot):
    while True:
        await send_reminder_for_inactive(bot)
        await asyncio.sleep(336 * 3600)
