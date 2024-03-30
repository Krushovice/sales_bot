import datetime
from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery

from app.api_v1.orm.crud import AsyncOrm

from app.api_v1.markups import (
    MenuActions,
    MenuCbData,
    ProfileActions,
    ProfileCbData,
    PayActions,
    PaymentCbData,
    build_account_kb,
    root_kb,
    build_main_kb,
    product_details_kb,
    build_questions_kb,
    build_back_info_kb,
)

from app.api_v1.utils import (
    payment_manager,
    get_receipt,
    generate_order_number,
    LEXICON_RU,
    get_subscribe_info,
)


router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.account))
async def handle_account_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )

    sub_info = await get_subscribe_info(user)
    url = markdown.hlink(
        "Ссылка",
        f"https://t.me/Real_vpnBot?start={user.tg_id}",
    )
    await call.message.edit_caption(
        caption=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"🗓 Подписка: <i>{sub_info['subscribe']}</i>\n"
            f"🎁 Скидка: <b>{sub_info['discount']}%</b>\n"
            f"Ваша реферальная ссылка: <i>{url}</i>\n\n"
            f"<i>На данной странице отображена основная информация о профиле.</i>"
            f"<i>Для оплаты и доступа к ключу используйте\n клавиши ниже ⬇️</i>"
        ),
        reply_markup=build_account_kb(
            exp_date=user.expiration_date,
            is_key=True if user.key else False,
        ),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=LEXICON_RU["help_info"],
        reply_markup=build_questions_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.promo))
async def handle_promo_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption="Введите пожалуйста промокод на бесплатный 7-дневный триал 🎁",
        reply_markup=root_kb(),
    )


@router.callback_query(PaymentCbData.filter(F.action == PayActions.pay))
async def handle_pay_action_button(
    call: CallbackQuery,
):
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )

    discount = user.discount if user.discount else 1
    total = int(150 - (150 * discount / 100))
    await call.answer()
    msg_text = markdown.text(
        markdown.hbold(f"💰 Сумма: {total} руб"),
        markdown.hitalic("Для оплаты перейдите по ссылке ниже ⬇️"),
        sep="\n\n",
    )
    payment = await payment_manager.init_payment(
        amount=total * 100,
        order_id=generate_order_number(),
        description=f"Оплата пользователя №{user.tg_id}",
        receipt=get_receipt(price=total),
    )
    await call.message.edit_caption(
        caption=msg_text,
        reply_markup=product_details_kb(
            payment_cb_data=payment,
            from_main_menu=True,
        ),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.advantage))
async def handle_advantage_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=LEXICON_RU["advantage"],
        reply_markup=root_kb(),
    )


@router.callback_query(
    ProfileCbData.filter(
        F.action == ProfileActions.back_to_main,
    )
)
async def handle_back_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=markdown.hbold(
            "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
            "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
            "🔥  Твой личный VPN по самой низкой цене\n\n"
            "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.questions))
async def handle_questions_button(call: CallbackQuery):
    await call.answer()
    text = LEXICON_RU["QA"]

    await call.message.edit_caption(
        caption=text,
        reply_markup=build_back_info_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.back_to_help))
async def handle_back_to_help_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(
        caption=LEXICON_RU["help_info"],
        reply_markup=build_questions_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.back_root))
async def handle_back_root_button(call: CallbackQuery):
    await call.answer()

    await call.message.edit_caption(
        caption=markdown.hbold(
            "🚀  Подключение в 1 клик, без ограничений скорости\n\n"
            "🛡  Отсутствие рекламы и полная конфиденциальность\n\n"
            "🔥  Твой личный VPN по самой низкой цене\n\n"
            "💰  Цена: 1̶9̶9̶руб 💥150 руб/мес",
        ),
        reply_markup=build_main_kb(),
    )
