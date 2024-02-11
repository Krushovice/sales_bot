from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.types import Message
from aiogram import Router
from app.markups import get_on_start_kb
from app.utils.lexicon import LEXICON_RU

from app.core import crud


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message):
    # user_id = await AsyncOrm.select_reader_by_username(
    #     username=message.from_user.username)

    # if not user_id:
    #     await AsyncOrm.insert_reader(first_name=message.from_user.first_name,
    #                                  last_name=message.from_user.last_name,
    #                                  username=message.from_user.username)

    await message.answer(
        text=markdown.bold(LEXICON_RU["/start"]),
        reply_markup=get_on_start_kb(),
    )


# @router.message(Command("help", prefix="!/"))
# async def command_help_handler(message: Message):
#     await message.answer(text=LEXICON_RU["/help"])


@router.message(Command("account", prefix="!/"))
async def show_profile_handler(message: Message):
    user = await AsyncOrm.get_user(tg_id=message.from_user.id,
                                   username=message.from_user.username)
    await message.answer(text=f"Привет, {message.from_user.username}")  #reply_markup=get_profile_kb())


@router.message(Command("payment", prefix="!/"))
async def refill_user_balance(message: Message):
    await AsyncOrm.update_user(tg_id=message.from_user.id,
                               cost=129,
                               balance=200)

    user = await AsyncOrm.get_user(tg_id=message.from_user.id,
                                   username=message.from_user.username)
    print(user.username)
    await message.answer(text=f"""Оплата прошла успешно!
                                  Стоимость услуги: {user.cost},
                                  Ваш баланс: {user.balance}""")
