import datetime
from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.types import Message
from aiogram import Router
from app.api_v1.markups import (
    build_main_kb,
    build_payment_kb,
    build_account_kb,
)


from app.api_v1.core.crud import AsyncOrm

# from app.api_v1.markups import PaymentCbData


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """Checking user if he is in the database"""
    user = await AsyncOrm.get_user(
        tg_id=message.from_user.id,
    )
    if user:
        if user.subscription:
            current_date = datetime.datetime.today()
            delta = current_date - user.expiration_date
            if 0 < delta <= 3:
                await message.answer(
                    text=markdown.hbold(
                        f"C возвращением, {message.from_user.first_name}!"
                        "Ваша подписка заканчивается. Пожалуйста, пополните баланс"
                    ),
                    reply_markup=build_account_kb(
                        tg_id=message.from_user.id,
                    ),
                )

    else:
        await AsyncOrm.create_user(
            tg_id=message.from_user.id,
            username=message.from_user.username,
        )

    await message.answer(
        text=markdown.hbold(
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
    await message.answer(
        text=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"💰 Баланс: {user.balance}руб\n\n"
            f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
            f"<i>Для его пополнения используйте клавиши ниже</i>"
        ),
        reply_markup=build_account_kb(),
    )


@router.message(Command("payment", prefix="!/"))
async def refill_user_balance(message: Message):
    await message.answer(
        text="💰 Укажите сумму пополнения баланса",
        reply_markup=build_payment_kb(),
    )
