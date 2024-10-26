from datetime import datetime, timedelta
from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown

from aiogram.types import Message, FSInputFile
from aiogram import Router

from app.api_v2.markups import (
    build_main_kb,
    build_payment_kb,
)

from app.api_v1.orm import AsyncOrm, Key

from app.api_v1.config import settings

from app.api_v1.utils import (
    check_for_referral,
    outline_helper,
    check_time_delta,
)

from app.api_v1.utils.logging import setup_logger

router = Router(name=__name__)
logger = setup_logger(__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


@router.message(CommandStart())
async def command_start_handler(message: Message):
    try:
        tg_id = message.from_user.id
        user_exists = await AsyncOrm.get_user(tg_id=tg_id)

        # проверка на реферальную ссылку
        referrer_id = await check_for_referral(message)

        if user_exists:

            # Пользователь уже зарегистрирован, проверяем подписку
            if check_time_delta(date=user_exists.expiration_date):
                sub_info = f"Активна до {user_exists.expiration_date} ✅"
            else:
                sub_info = "Не активна ⛔️"

            if referrer_id:
                # Оповещение о недоступности реферальной ссылки для существующих пользователей
                await message.answer(
                    "Реферальная ссылка доступна только для новых пользователей.👀"
                    " Ваша подписка: " + sub_info
                )

        else:

            if referrer_id and referrer_id != tg_id:
                # Создание нового пользователя с реферальным бонусом
                today = datetime.now()
                expiration_date = today + timedelta(
                    days=10 if referrer_id == settings.ADVERTISER_ID else 5
                )

                key = outline_helper.create_new_key(name=tg_id)
                new_user = await AsyncOrm.create_user(
                    tg_id=tg_id,
                    username=message.from_user.username,
                    subscription=True,
                    subscribe_date=today.strftime("%d-%m-%Y"),
                    expiration_date=expiration_date.strftime("%d-%m-%Y"),
                )

                # Обновление сгенерированного ключа и реферала
                await AsyncOrm.update_user(
                    tg_id=new_user.tg_id,
                    key=Key(
                        api_id=int(key.key_id),
                        name=key.name,
                        user_id=new_user.id,
                        value=key.access_url,
                    ),
                )

                await AsyncOrm.update_user(
                    tg_id=referrer_id,
                    referral=new_user,
                )
            else:
                # Создание пользователя без реферальной ссылки
                await AsyncOrm.create_user(
                    tg_id=tg_id,
                    username=message.from_user.username,
                )
            sub_info = "Не активна ⛔️"

        # Настройки подписки и администрирования для кнопок
        sub = bool(user_exists.subscription if user_exists else False)
        is_admin = tg_id == int(settings.ADMIN_ID)

        # Отправка информации пользователю
        await message.answer_photo(
            photo=FSInputFile(path=file_path),
            caption=markdown.hbold(
                "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
                "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
                "🔥  Твой личный VPN по самой низкой цене\n\n"
                "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес\n\n"
                f"Ваша подписка: {sub_info}\n\n"
            ),
            reply_markup=build_main_kb(
                subscribe=sub,
                admin=is_admin,
            ),
        )
    except Exception as e:
        logger.error(f"Ошибка обработки кнопки старт: {e}")


@router.message(Command("payment", prefix="!/"))
async def refill_user_balance(message: Message):

    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption=markdown.hbold("💰 Варианты оплаты подписки:"),
        reply_markup=build_payment_kb(),
    )
