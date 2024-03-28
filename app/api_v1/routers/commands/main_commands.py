from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown

from aiogram.types import Message, FSInputFile
from aiogram import Router

from app.api_v1.markups import (
    build_main_kb,
    build_payment_kb,
    build_account_kb,
    root_kb,
)


from app.api_v1.orm.crud import AsyncOrm


from app.api_v1.utils import (
    check_user_expiration,
    get_subscribe_info,
    check_for_referral,
)


router = Router(name=__name__)

file_path = "app/api_v1/utils/images/image2.jpg"


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """Checking user if he is in the database"""

    user_check = await AsyncOrm.get_user(
        tg_id=message.from_user.id,
    )
    referrer_id = check_for_referral(message)
    if not user_check:
        user = await AsyncOrm.create_user(
            tg_id=message.from_user.id,
            username=message.from_user.username,
        )
        if referrer_id:
            refferer = await AsyncOrm.get_user(
                tg_id=referrer_id,
            )

            await AsyncOrm.update_user(
                tg_id=referrer_id,
                referral=user,
                discount=refferer.discount + 1,
            )
    else:
        if referrer_id:
            refferer = await AsyncOrm.get_user(
                tg_id=referrer_id,
            )

            await AsyncOrm.update_user(
                tg_id=referrer_id,
                referral=user_check,
                discount=refferer.discount + 1,
            )
    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption=markdown.hbold(
            "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
            "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
            "🔥  Твой личный VPN по самой низкой цене\n\n"
            "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )


@router.message(Command("partners", prefix="!/"))
async def command_help_handler(message: Message):
    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption="В разработке!",
        reply_markup=root_kb(),
    )


@router.message(Command("account", prefix="!/"))
async def show_profile_handler(message: Message):
    user = await AsyncOrm.get_user(
        tg_id=message.from_user.id,
    )

    if user.subscription:
        subscribe_info = f"Активна до {user.expiration_date}"
    else:
        subscribe_info = "Не активна"
    url = markdown.hlink(
        "Ссылка",
        f"https://t.me/Real_vpnBot?start={user.tg_id}",
    )
    text = (
        f"<b>Личный кабинет</b>\n\n"
        f"🆔 {user.tg_id} \n"
        f"🗓 Подписка: <i>{subscribe_info}</i>\n"
        f"🎁 Скидка: <b>{user.discount if user.discount else 'Нет'}%</b>\n"
        f"Ваша реферальная ссылка: <i>{url}</i>\n\n"
        f"<i>На данной странице отображена основная информация о профиле.</i>"
        f"<i>Для оплаты и доступа к ключу\n используйте клавиши ниже⬇️</i>"
    )
    if user:
        await message.answer_photo(
            photo=FSInputFile(
                path=file_path,
            ),
            caption=text,
            reply_markup=build_account_kb(user=user),
        )

    else:
        await message.answer_photo(
            photo=FSInputFile(
                path=file_path,
            ),
            caption=text,
            reply_markup=build_account_kb(),
        )


@router.message(Command("payment", prefix="!/"))
async def refill_user_balance(message: Message):

    await message.answer_photo(
        photo=FSInputFile(
            path=file_path,
        ),
        caption=markdown.hbold("💰 Варианты оплаты подписки:"),
        reply_markup=build_payment_kb(),
    )
