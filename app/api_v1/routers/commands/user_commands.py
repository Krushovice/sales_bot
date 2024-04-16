from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import Message, FSInputFile


from app.api_v1.markups import build_main_kb, root_kb

from app.api_v1.orm import AsyncOrm, Key

from app.api_v1.utils import outline_helper


router = Router(name=__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


@router.message(F.text == "REALVPN2024CPG")
async def user_promo_handler(message: Message) -> None:
    tg_id = message.from_user.id
    today = datetime.now()
    delta = timedelta(days=7)
    expiration_date = (today + delta).strftime("%d-%m-%Y")
    user = await AsyncOrm.get_user(tg_id=tg_id)
    if not user:
        user = await AsyncOrm.create_user(
            tg_id=tg_id,
            username=message.from_user.username,
        )
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
                "Вот ваш пробный ключ \n"
                f"<pre>{key.access_url}</pre>"
                "👆Нажмите чтобы скопировать\n"
                "Пожалуйста, не скачивайте торрент-файлы через наш VPN.‼️ "
                "Сервер Outline может заблокировать наш сервис за это. "
                "Cпасибо за ваше понимание и за то, что выбрали нас🫶🏻"
            ),
            reply_markup=root_kb(),
        )

    else:
        expiration_date = user.expiration_date
        await message.answer_photo(
            photo=FSInputFile(
                path=file_path,
            ),
            caption=(
                f"Промокод действует только для новых пользователей \n\n"
                f"Ваша подписка закончилась {expiration_date}"
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
