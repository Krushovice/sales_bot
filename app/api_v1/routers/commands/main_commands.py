from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.types import Message, FSInputFile
from aiogram import Router

from app.api_v1 import (
    build_main_kb,
    build_payment_kb,
    build_account_kb,
)


from app.api_v1.core.crud import AsyncOrm

from app.api_v1.utils.chek_user import check_user_expiration


router = Router(name=__name__)

file_path = "app/api_v1/utils/images/image1.jpg"


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """Checking user if he is in the database"""
    user = await AsyncOrm.get_user(
        tg_id=message.from_user.id,
    )
    if user:
        if await check_user_expiration(tg_id=user.tg_id):
            await message.answer_photo(
                photo=FSInputFile(
                    path=file_path,
                ),
                caption=markdown.hbold(
                    f"C возвращением, {message.from_user.first_name}!\n"
                    "Ваша подписка заканчивается. Пожалуйста, пополните баланс"
                ),
                reply_markup=build_account_kb(
                    user=user,
                ),
            )
            return

    else:
        await AsyncOrm.create_user(
            tg_id=message.from_user.id,
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
            "💰  Цена: 1̶9̶9̶руб 💥129 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )


@router.message(Command("partners", prefix="!/"))
async def command_help_handler(message: Message):
    await message.answer("В разработке!")


@router.message(Command("account", prefix="!/"))
async def show_profile_handler(message: Message):
    user = await AsyncOrm.get_user(
        tg_id=message.from_user.id,
    )

    text = (
        f"<b>Личный кабинет</b>\n\n"
        f"🆔 {user.tg_id} \n"
        f"💰 Баланс: {user.balance}руб\n\n"
        f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
        f"<i>Для его пополнения используйте клавиши ниже</i>"
    )
    if await check_user_expiration(tg_id=user.tg_id):
        await message.answer(
            text=text,
            reply_markup=build_account_kb(user=user),
        )

    else:
        await message.answer(
            text=text,
            reply_markup=build_account_kb(),
        )


@router.message(Command("payment", prefix="!/"))
async def refill_user_balance(message: Message):

    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption=markdown.hbold("💰 Укажите сумму пополнения баланса"),
        reply_markup=build_payment_kb(),
    )
