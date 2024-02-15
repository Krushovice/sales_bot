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
from app.api_v1.markups import PaymentCbData


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message):
    # await AsyncOrm.create_user(
    #     tg_id=message.from_user.id,
    #     username=message.from_user.username,
    # )
    await AsyncOrm.get_user(
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


@router.message(Command("help", prefix="!/"))
async def command_help_handler(message: Message):
    await message.answer()


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
        reply_markup=build_account_kb(),
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
        await message.answer(
            text="Подписка оформлена!",
            reply_markup=build_payment_kb(),
        )
    else:
        await message.answer("Что-то пошло не так")
