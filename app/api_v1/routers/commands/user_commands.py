from aiogram import Router
from aiogram.types import Message


from app.api_v1.markups import build_main_kb


router = Router(name=__name__)


@router.message()
async def any_text_handler(message: Message) -> None:

    await message.answer(
        text="Пожалуйста, воспользуйтесь меню для дальнейшей работы",
        reply_markup=build_main_kb(),
    ),
