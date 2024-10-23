from datetime import datetime, timedelta
from aiogram import Router, F

from aiogram.types import Message, FSInputFile


from app.api_v2.markups import build_main_kb, root_kb

from app.api_v1.orm import AsyncOrm, Key

from app.api_v1.utils import outline_helper

from app.api_v1.config import settings

router = Router(name=__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


@router.message(F.text == "REALVPN2024CPG")
@router.message(F.text == "LEVITSKAYA")
async def user_promo_handler(message: Message) -> None:
    tg_id = message.from_user.id
    user = await AsyncOrm.get_user(tg_id=tg_id)
    if user.key:
        await message.answer_photo(
            photo=FSInputFile(
                path=file_path,
            ),
            caption="Промокод действует только для новых пользователей",
            reply_markup=root_kb(),
        )

    if not user:
        user = await AsyncOrm.create_user(
            tg_id=tg_id,
            username=message.from_user.username,
        )
    today = datetime.now()
    if message.text == "REALVPN2024CPG":
        delta = timedelta(days=7)
    elif message.text == "LEVITSKAYA":
        delta = timedelta(days=10)
        if not await AsyncOrm.get_referrer(tg_id=tg_id):
            await AsyncOrm.update_user(
                tg_id=int(settings.ADVERTISER_ID),
                referral=user,
            )
        with open("count_referrals.txt", "w+") as f:
            count = f.read()
            if not count:
                f.write("1")
            else:
                count = int(count)
                count += 1
                f.write(str(count))

    expiration_date = (today + delta).strftime("%d-%m-%Y")

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
