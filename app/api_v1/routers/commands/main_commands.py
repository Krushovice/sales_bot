from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown

from aiogram.types import Message, FSInputFile
from aiogram import Router

from app.api_v1.markups import (
    build_main_kb,
    build_payment_kb,
    build_account_kb,
    root_kb,
)


from app.api_v1.orm.crud import AsyncOrm


from app.api_v1.utils import (
    check_for_referral,
)

from app.api_v1.utils.logging import setup_logger

router = Router(name=__name__)
logger = setup_logger(__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """Checking user if he is in the database"""
    try:

        user_check = await AsyncOrm.get_user(
            tg_id=message.from_user.id,
        )
        referrer_id = check_for_referral(message)
        if not user_check:
            user = await AsyncOrm.create_user(
                tg_id=message.from_user.id,
                username=message.from_user.username,
            )
            if referrer_id:
                refferer = await AsyncOrm.get_user(
                    tg_id=referrer_id,
                )
                discount = refferer.discount + 1 if refferer.discount != 50 else 50
                await AsyncOrm.update_user(
                    tg_id=referrer_id,
                    referral=user,
                    discount=discount,
                )
        else:
            if referrer_id:
                refferer = await AsyncOrm.get_user(
                    tg_id=referrer_id,
                )
                discount = refferer.discount + 1 if refferer.discount != 50 else 50
                await AsyncOrm.update_user(
                    tg_id=referrer_id,
                    referral=user_check,
                    discount=discount,
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
    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption="В разработке!",
        reply_markup=root_kb(),
    )


@router.message(Command("account", prefix="!/"))
async def show_profile_handler(message: Message):
    try:

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
