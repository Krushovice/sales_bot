from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.types import Message
from aiogram import Router
from app.api_v1.markups import get_on_start_kb, get_profile_kb
from app.api_v1.utils.lexicon import LEXICON_RU

from app.api_v1.core.crud import AsyncOrm


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await AsyncOrm.create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
    )

    await message.answer(
        text=markdown.bold(LEXICON_RU["/start"]),
        reply_markup=get_on_start_kb(),
    )


@router.message(Command("help", prefix="!/"))
async def command_help_handler(message: Message):
    await message.answer(text=LEXICON_RU["/help"])


@router.message(Command("account", prefix="!/"))
async def show_profile_handler(message: Message):
    user = await AsyncOrm.get_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
    )
    await message.answer(
        text=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"💰 Баланс: {user.balance}руб\n\n"
            f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
            f"<i>Для его пополнения используйте клавиши ниже</i>"
        ),
        reply_markup=get_profile_kb(),
    )


@router.message(Command("payment", prefix="!/"))
async def refill_user_balance(message: Message):
    user = await AsyncOrm.update_user(
        tg_id=message.from_user.id,
        cost=129,
        balance=200,
    )

    await message.answer(
        text=f"""Оплата прошла успешно!
Стоимость услуги: {user.cost},
Ваш баланс: {user.balance}"""
    )
    updated_user = await AsyncOrm.update_user(
        tg_id=message.from_user.id,
        subscription=True,
    )
    if updated_user.subscription:
        await message.answer("Подписка оформлена!")
    else:
        await message.answer("Что-то пошло не так")
