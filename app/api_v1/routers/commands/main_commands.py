from datetime import datetime, timedelta
from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown

from aiogram.types import Message, FSInputFile
from aiogram import Router

from app.api_v1.markups import (
    build_main_kb,
    build_payment_kb,
    build_account_kb,
    build_account_menu,
)

from app.api_v1.admin import build_admin_kb

from app.api_v1.orm import AsyncOrm, Key

from app.api_v1.config import settings

from app.api_v1.utils import (
    check_for_referral,
    outline_helper,
)

from app.api_v1.utils.logging import setup_logger

router = Router(name=__name__)
logger = setup_logger(__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


@router.message(CommandStart())
async def command_start_handler(message: Message):

    try:
        tg_id = message.from_user.id
        today = datetime.now()
        delta = timedelta(days=7)
        expiration_date = (today + delta).strftime("%d-%m-%Y")
        user_exists = await AsyncOrm.get_user(tg_id=tg_id)

        if not user_exists:
            """Check user start command for referral link"""
            referrer_id = check_for_referral(message)

            if referrer_id and referrer_id != tg_id:
                key = outline_helper.create_new_key(name=tg_id)
                new_user = await AsyncOrm.create_user(
                    tg_id=tg_id,
                    username=message.from_user.username,
                    subscription=True,
                    subscribe_date=today.strftime("%d-%m-%Y"),
                    expiration_date=expiration_date,
                )
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
                await AsyncOrm.create_user(
                    tg_id=tg_id,
                    username=message.from_user.username,
                )

        await message.answer_photo(
            photo=FSInputFile(
                path=file_path,
            ),
            caption=markdown.hbold(
                "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
                "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
                "🔥  Твой личный VPN по самой низкой цене\n\n"
                "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес",
            ),
            reply_markup=build_main_kb(),
        )
    except Exception as e:
        logger.error(f"Ошибка обработки кнопки старт: {e}")


@router.message(Command("partners", prefix="!/"))
async def command_help_handler(message: Message):
    url = markdown.hlink(
        "Ваша реферальная ссылка",
        f"https://t.me/Real_vpnBot?start={message.from_user.id}",
    )
    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption="Чтобы стать нашим партнером и получать бонусы, необходимо приглашать "
        "новых пользователей по реферальной ссылке👥. За первого "
        "приглашенного начисляется скидка в размере 5%, за каждого "
        "последующего - 7, 14 или 21 бонусный день к вашей подписке, в зависимости от "
        "количества купленных месяцев у вашего реферала. "
        f"<b>{url}</b>, скопируйте её и разошлите своим друзьям 😎 "
        "Вы также можете найти реферальную ссылку в своем личном кабинете",
        reply_markup=build_account_menu(),
    )


@router.message(Command("account", prefix="!/"))
async def show_profile_handler(message: Message):
    try:
        if message.from_user.id == int(settings.ADMIN_ID):
            await message.answer_photo(
                photo=FSInputFile(
                    path=file_path,
                ),
                caption=(f"С возвращением, {message.from_user.username}!"),
                reply_markup=build_admin_kb(),
            )
        else:

            user = await AsyncOrm.get_user(
                tg_id=message.from_user.id,
            )
            if user:
                subscribe = user.expiration_date

                if subscribe:
                    sub_info = f"Активна до {subscribe}"
                else:
                    sub_info = "Не активна"

                discount = user.discount if user.discount else 0
            else:
                sub_info = "Не активна"
                discount = 0

            url = markdown.hlink(
                "Ссылка",
                f"https://t.me/Real_vpnBot?start={user.tg_id}",
            )
            text = (
                f"<b>Личный кабинет</b>\n\n"
                f"🆔 {user.tg_id} \n"
                f"🗓 Подписка: <i>{sub_info}</i>\n"
                f"🎁 Скидка: <b>{discount}%</b>\n"
                f"Ваша реферальная ссылка: <i>{url}</i>\n\n"
                f"<i>На данной странице отображена основная информация о профиле.</i>\n"
                f"<i>Для оплаты и доступа к ключу используйте клавиши ниже⬇️</i>"
            )
            if user:
                await message.answer_photo(
                    photo=FSInputFile(
                        path=file_path,
                    ),
                    caption=text,
                    reply_markup=build_account_kb(),
                )

            else:
                await message.answer_photo(
                    photo=FSInputFile(
                        path=file_path,
                    ),
                    caption=text,
                    reply_markup=build_account_kb(),
                )
    except Exception as e:
        logger.error(f"Ошибка при переходе в аккаунт: {e}")


@router.message(Command("payment", prefix="!/"))
async def refill_user_balance(message: Message):

    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption=markdown.hbold("💰 Варианты оплаты подписки:"),
        reply_markup=build_payment_kb(),
    )
