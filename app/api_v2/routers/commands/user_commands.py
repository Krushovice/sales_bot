from datetime import datetime, timedelta
from aiogram import Router, F

from aiogram.types import Message, FSInputFile


from app.api_v2.markups import build_main_kb, root_kb

from app.api_v1.orm import AsyncOrm, Key

from app.api_v1.utils import outline_helper

from app.api_v1.config import settings

from app.api_v1.utils.logging import setup_logger
from app.api_v2.routers.callback_handlers.main_menu_callback_handlers import logger

router = Router(name=__name__)

my_logger = setup_logger(__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


@router.message(F.text == "REALVPN2024CPG")
async def user_promo_handler(message: Message) -> None:
    tg_id = message.from_user.id
    user = await AsyncOrm.get_user(tg_id=tg_id)
    if not user:
        user = await AsyncOrm.create_user(
            tg_id=tg_id,
            username=message.from_user.username,
        )

    today = datetime.now()

    delta = timedelta(days=7)

    if not user.key:
        key = outline_helper.create_new_key(name=tg_id)
        await AsyncOrm.update_user(
            tg_id=tg_id,
            subscription=True,
            subscribe_date=today.strftime("%d-%m-%Y"),
            expiration_date=expiration_date,
            key=Key(
                api_id=int(key.key_id),
                name=key.name,
                user_id=user.id,
                value=key.access_url,
            ),
        )

        await message.answer_photo(
            photo=FSInputFile(
                path=file_path,
            ),
            caption=(
                "Пробная подписка активирована!\n"
                "Не забудьте потом оставить отзыв о нашем сервисе 💚\n\n"
                "Ваш пробный ключ \n"
                f"<code>{key.access_url}</code>"
                "👆Нажмите чтобы скопировать\n"
            ),
            reply_markup=root_kb(),
        )


@router.message()
async def any_text_handler(message: Message) -> None:

    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption="Пожалуйста, воспользуйтесь меню для дальнейшей работы",
        reply_markup=build_main_kb(),
    ),
