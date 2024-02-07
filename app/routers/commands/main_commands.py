from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.types import Message
from aiogram import Router
from app.markups import get_on_start_kb
from app.utils.lexicon import LEXICON_RU

# from bot.core import AsyncOrm


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



# @router.message(Command("account", prefix="!/"))
# async def show_profile_handler(message: Message):
#     await message.answer(text=LEXICON_RU["/profile"],
#                          reply_markup=get_profile_kb())

# @router.message(Command("payment", prefix="!/"))
# async def show_profile_handler(message: Message):
#     await message.answer(text=LEXICON_RU["/profile"],
#                          reply_markup=get_profile_kb())
